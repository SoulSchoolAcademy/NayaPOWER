#!/usr/bin/env python3
"""person_timeline.py — the per-person timeline builder (Best-of-Best #1).

Faces (the flagship People door) derives people by name-matching across
the wall, mail, and invites at read time. This module is that derivation
made explicit, durable, and testable — the data half of map element #1:

  * Identity resolution lives HERE (and, mirrored, in the SQL function
    resolve_person_key): email hash wins when known; otherwise the
    normalized name keys the person; an alias registry can override.
  * The event stream has ONE shape (see docs/person-timeline-read-model.md)
    whether an event came from a wall note, a mail thread/message, or an
    invite — so the People UI, search, and morning briefs all read the
    same thing.
  * ZERO manual logging: every field is derived from existing rows.
    Anything that cannot be derived is an honest None, never a guess.
  * Rows that cannot be resolved to a person are QUARANTINED and counted
    in the build report — never silently attached to someone.

Input rows are plain dicts shaped like the source tables (the columns the
repo evidences; see the migration header for the source-column contract).
The builder is pure: rows in, (events, identities, report) out. Fetching
rows from Supabase is the caller's job; keeping this pure is what makes
the derivation provable by tests.

Usage as a library:
    from tools.person_timeline import build_timeline
    events, identities, report = build_timeline(
        owner_alias="shawn", wall_notes=[...], mail_threads=[...],
        mail_messages=[...], invites=[...], owner_names={"Shawn Vibert"})

CLI (JSON in, JSON out — for inspection and pipeline use):
    python3 tools/person_timeline.py --input rows.json --owner-alias shawn
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys

# ── Identity ─────────────────────────────────────────────────────────────

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalize_person_name(name: str | None) -> str:
    """Mirror of public.normalize_person_name in the migration."""
    return _NON_ALNUM.sub(" ", (name or "").lower()).strip()


def person_key(owner_alias: str, display_name: str | None, email_hash: str | None) -> str:
    """Mirror of public.resolve_person_key: email hash wins, else name."""
    owner = (owner_alias or "").lower()
    if email_hash:
        return f"h:{email_hash}@{owner}"
    return f"n:{normalize_person_name(display_name)}@{owner}"


def email_hash_of(email: str | None) -> str | None:
    """Invites are hash-only by canon (never raw email). If a caller holds
    a raw email from another source, this is the one hashing rule."""
    if not email:
        return None
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


# ── Source-row parsing helpers ───────────────────────────────────────────

def _parse_participants(raw) -> list[dict]:
    """Thread participants arrive as a JSON array, a JSON string, or a
    delimited name string depending on the writer. Tolerate all three;
    each participant becomes {"name": ..., "email_hash": ...|None}."""
    if raw is None:
        return []
    items = raw
    if isinstance(raw, str):
        text = raw.strip()
        if text.startswith("["):
            try:
                items = json.loads(text)
            except json.JSONDecodeError:
                items = [text]
        else:
            items = re.split(r"[;,]", text)
    out: list[dict] = []
    for item in items or []:
        if isinstance(item, dict):
            name = item.get("name") or item.get("sender_name") or item.get("email")
            out.append({"name": name, "email_hash": item.get("email_hash")
                        or email_hash_of(item.get("email"))})
        elif isinstance(item, str) and item.strip():
            out.append({"name": item.strip(), "email_hash": None})
    return [p for p in out if p["name"]]


def _is_owner(name: str | None, owner_names: set[str]) -> bool:
    return normalize_person_name(name) in owner_names


# ── The builder ──────────────────────────────────────────────────────────

def build_timeline(
    *,
    owner_alias: str,
    wall_notes: list[dict] | None = None,
    mail_threads: list[dict] | None = None,
    mail_messages: list[dict] | None = None,
    invites: list[dict] | None = None,
    owner_names: set[str] | None = None,
    aliases: dict[str, str] | None = None,
    include_owner: bool = False,
) -> tuple[list[dict], list[dict], dict]:
    """Derive (events, identities, report) from existing source rows.

    aliases: {alias_key: person_key} — alias_key is a resolved key that
    should fold into another person (the durable registry from
    person_identity_aliases; alias_key form is the same person_key shape).
    owner_names: the owner's own display names (normalized internally);
    the owner is excluded from people unless include_owner=True.
    """
    owner_norm = {normalize_person_name(n) for n in (owner_names or set())}
    aliases = aliases or {}
    events: list[dict] = []
    people: dict[str, dict] = {}
    report = {"input_rows": 0, "events": 0, "quarantined": 0,
              "quarantine_reasons": {}, "people": 0}

    def quarantine(reason: str) -> None:
        report["quarantined"] += 1
        report["quarantine_reasons"][reason] = \
            report["quarantine_reasons"].get(reason, 0) + 1

    def resolve(name: str | None, ehash: str | None) -> str | None:
        if not name and not ehash:
            return None
        key = person_key(owner_alias, name, ehash)
        return aliases.get(key, key)

    def touch(key: str, name: str | None, ehash: str | None, at, source: str) -> None:
        person = people.get(key)
        if person is None:
            person = people[key] = {
                "person_key": key, "owner_alias": owner_alias,
                "display_name": name or "", "normalized_name": normalize_person_name(name),
                "email_hash": ehash, "first_seen_at": at, "last_seen_at": at,
                "sources": {},
            }
        if name and (not person["display_name"] or len(name) > len(person["display_name"])):
            person["display_name"] = name
            person["normalized_name"] = normalize_person_name(name)
        if ehash and not person["email_hash"]:
            person["email_hash"] = ehash
        if at is not None:
            if person["first_seen_at"] is None or at < person["first_seen_at"]:
                person["first_seen_at"] = at
            if person["last_seen_at"] is None or at > person["last_seen_at"]:
                person["last_seen_at"] = at
        person["sources"][source] = person["sources"].get(source, 0) + 1

    def emit(key, name, ehash, at, kind, source_table, title, body,
             direction, thread_key=None, status=None) -> None:
        events.append({
            "person_key": key, "owner_alias": owner_alias, "event_at": at,
            "event_kind": kind, "source_table": source_table,
            "source_id": None, "title": title, "body": body,
            "direction": direction, "counterparty_name": name,
            "thread_key": thread_key, "status": status,
        })
        touch(key, name, ehash, at, source_table)
        report["events"] += 1

    # — Wall notes: person = the note's author (Faces COALESCE pattern).
    # Notes authored by the owner are the owner's own wall posts; they are
    # not a relationship event and are skipped (counted in input only).
    for note in wall_notes or []:
        report["input_rows"] += 1
        name = note.get("author_name") or note.get("sender_name")
        if not name:
            quarantine("wall_note_without_author")
            continue
        if _is_owner(name, owner_norm):
            continue
        key = resolve(name, None)
        emit(key, name, None, note.get("created_at"), "wall_note",
             "smart_notes", None, note.get("content"), "outbound")

    # — Mail: threads give the roster; messages are the events.
    threads = {t.get("thread_key"): t for t in (mail_threads or [])}
    for thread in mail_threads or []:
        report["input_rows"] += 1
    for msg in mail_messages or []:
        report["input_rows"] += 1
        thread = threads.get(msg.get("thread_key")) or {}
        direction = msg.get("direction")
        at = msg.get("created_at")
        if direction == "inbound":
            name = msg.get("sender_name") or msg.get("sender")
            if not name:
                quarantine("inbound_message_without_sender")
                continue
            if _is_owner(name, owner_norm):
                continue
            key = resolve(name, None)
            emit(key, name, None, at, "mail_message", "smart_mail_messages",
                 thread.get("subject"), msg.get("body"), "inbound",
                 thread_key=msg.get("thread_key"))
        elif direction == "outbound":
            others = [p for p in _parse_participants(thread.get("participants"))
                      if not _is_owner(p["name"], owner_norm)]
            if not others:
                quarantine("outbound_message_without_counterparty")
                continue
            for person in others:
                key = resolve(person["name"], person["email_hash"])
                emit(key, person["name"], person["email_hash"], at,
                     "mail_message", "smart_mail_messages",
                     thread.get("subject"), msg.get("body"), "outbound",
                     thread_key=msg.get("thread_key"))
        else:
            quarantine("message_without_direction")

    # — Invites: hash-keyed people; no name is ever invented for them.
    for invite in invites or []:
        report["input_rows"] += 1
        ehash = invite.get("invitee_email_hash")
        if not ehash:
            quarantine("invite_without_email_hash")
            continue
        key = resolve(None, ehash)
        emit(key, None, ehash, invite.get("created_at"), "invite",
             "invites", None, None, "outbound",
             status=invite.get("status"))

    events.sort(key=lambda e: (e["event_at"] is None, e["event_at"] or ""))
    report["people"] = len(people)
    return events, sorted(people.values(), key=lambda p: p["person_key"]), report


def summarize_person(events_for_person: list[dict]) -> dict:
    """The derived person summary every consumer reads: last spoke (the
    counterparty's most recent event), waiting (the latest event is theirs
    and newer than any reply — the conversation is waiting on the owner),
    open threads, invite state. All derived; None when underivable."""
    ordered = sorted(events_for_person,
                     key=lambda e: (e["event_at"] is None, e["event_at"] or ""))
    last_spoke = None
    for event in reversed(ordered):
        if event["event_kind"] in ("mail_message", "wall_note"):
            last_spoke = event["event_at"]
            break
    latest = ordered[-1] if ordered else None
    waiting = bool(
        latest and latest["event_kind"] == "mail_message"
        and latest["direction"] == "inbound"
    )
    open_threads = sorted({
        e["thread_key"] for e in ordered
        if e["event_kind"] == "mail_message" and e["thread_key"]
    })
    invite_status = None
    for event in reversed(ordered):
        if event["event_kind"] == "invite":
            invite_status = event["status"]
            break
    return {
        "last_spoke_at": last_spoke,
        "waiting_on_owner": waiting,
        "open_thread_keys": open_threads,
        "invite_status": invite_status,
        "event_count": len(ordered),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="JSON file of source rows")
    parser.add_argument("--owner-alias", required=True)
    parser.add_argument("--owner-name", action="append", default=[],
                        help="owner display name (repeatable)")
    args = parser.parse_args()
    data = json.loads(open(args.input, encoding="utf-8").read())
    events, identities, report = build_timeline(
        owner_alias=args.owner_alias,
        wall_notes=data.get("smart_notes", []),
        mail_threads=data.get("smart_mail_threads", []),
        mail_messages=data.get("smart_mail_messages", []),
        invites=data.get("invites", []),
        owner_names=set(args.owner_name),
    )
    json.dump({"events": events, "identities": identities, "report": report},
              sys.stdout, indent=1, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
