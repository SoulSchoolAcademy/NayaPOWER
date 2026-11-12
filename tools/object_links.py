#!/usr/bin/env python3
"""object_links.py — Linked everything, the service layer (Best-of-Best #14).

Before this module, linkage was an appearance: Faces derives people by
name-matching at read time, lists hold device-local text, and a note
could not belong to a person or sit in a list as data. This module is
the link made real, mirroring migration 20261022211500_object_links_v1:

  * A link is ONE stored row: a subject object (kind + ref) filed under
    a target (a person, a list, or a mail thread) by its owner. The
    object itself is never copied — every home resolves the same row.
  * file_under() is the write operation the surfaces call — "file this
    under Mary", "file this under Launch" — by tap today, by voice
    tomorrow. It enforces the migration's ownership rules: the subject
    must be the caller's own and the target person must be the caller's
    own; cross-owner attempts are refused, never silently scoped away.
  * Owner-named facts (element #19) ride the same model: plain key/value
    words on an object, at most FACT_LIMIT of them — a handful, not a
    field editor.
  * unfile() removes a link row and nothing else: deleting a link never
    deletes the object.

The store below is an in-memory model of the tables (the production
runtime is Postgres + RLS + the file_object_under RPC; the rules here
are the same rules, kept pure so they are provable by tests). Fetching
rows from Supabase is the caller's job.

Refs are the stores' own durable keys, as text:
  naya_note -> naya_notes.id · smart_link -> smart_links.id ·
  person -> person_identities.person_key (the timeline model's key,
  tools/person_timeline.py) · mail_thread -> thread_key ·
  smart_note -> the note's brain-estate id · list -> the list's name in
  owner scope (step 15 gives lists durable ids; text refs carry either).

Usage as a library:
    from tools.object_links import LinkStore
    store = LinkStore(naya_notes=[...], persons=[...], lists=[...])
    store.file_under(actor_id="u1", actor_alias="shawn",
                     subject=("naya_note", note_id),
                     target=("person", "n:mary jones@shawn"))

CLI (JSON in, JSON out — inspection and pipeline use): the input file
carries the store rows plus an "ops" list of file_under / set_fact
operations to apply as the actor:
    python3 tools/object_links.py --input store.json --actor-id u1 \
        --actor-alias shawn
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid

# ── The model (mirrors the migration's checks, exactly) ─────────────────

SUBJECT_KINDS = ("smart_note", "naya_note", "mail_thread", "smart_link",
                 "person", "list")
TARGET_KINDS = ("person", "list", "mail_thread")
RELATION_FILED_UNDER = "filed_under"
FACT_LIMIT = 12
_FACT_KEY = re.compile(r"^[a-z0-9][a-z0-9 _-]{0,63}$")
_FACT_VALUE_MAX = 500

# Which store holds each subject kind, and how ownership is proven there:
# "id" stores carry owner_id (naya_notes, smart_links, person_identities);
# "alias" stores key by owner_alias alone (smart_notes, mail threads,
# lists) — the same split the migration documents.
_STORE_OF_KIND = {
    "naya_note": "naya_notes",
    "smart_link": "smart_links",
    "person": "persons",
    "smart_note": "smart_notes",
    "mail_thread": "mail_threads",
    "list": "lists",
}
_REF_OF_STORE = {
    "naya_notes": "id",
    "smart_links": "id",
    "persons": "person_key",
    "smart_notes": "ref",
    "mail_threads": "thread_key",
    "lists": "name",
}
_ID_STORES = {"naya_notes", "smart_links", "persons"}


class ObjectLinkError(Exception):
    """Base for every refusal this module raises."""


class UnknownKindError(ObjectLinkError):
    """A kind outside SUBJECT_KINDS / TARGET_KINDS."""


class ObjectNotFoundError(ObjectLinkError):
    """The ref does not exist in any owner's store."""


class OwnershipError(ObjectLinkError):
    """Cross-owner attempt: the subject or target is someone else's."""


class FactLimitError(ObjectLinkError):
    """The object already carries FACT_LIMIT facts."""


def normalize_fact_key(key: str) -> str:
    """Owner-named, plain: lowercase, collapsed whitespace, trimmed.
    Must satisfy the migration's key shape or the write is refused."""
    normalized = re.sub(r"\s+", " ", (key or "").strip().lower())
    if not _FACT_KEY.match(normalized):
        raise ObjectLinkError(f"fact key {key!r} is not a plain owner-named key")
    return normalized


class LinkStore:
    """The link + fact tables over in-memory models of the stores."""

    def __init__(
        self,
        *,
        naya_notes: list[dict] | None = None,
        smart_links: list[dict] | None = None,
        persons: list[dict] | None = None,
        smart_notes: list[dict] | None = None,
        mail_threads: list[dict] | None = None,
        lists: list[dict] | None = None,
    ) -> None:
        self.stores: dict[str, list[dict]] = {
            "naya_notes": list(naya_notes or []),
            "smart_links": list(smart_links or []),
            "persons": list(persons or []),
            "smart_notes": list(smart_notes or []),
            "mail_threads": list(mail_threads or []),
            "lists": list(lists or []),
        }
        self.links: list[dict] = []
        self.facts: list[dict] = []

    # — Store resolution ─────────────────────────────────────────────────

    def _find_all(self, kind: str, ref: str) -> list[dict]:
        store = self.stores[_STORE_OF_KIND[kind]]
        ref_field = _REF_OF_STORE[_STORE_OF_KIND[kind]]
        return [row for row in store if str(row.get(ref_field)) == ref]

    def _find(self, kind: str, ref: str) -> dict | None:
        matches = self._find_all(kind, ref)
        return matches[0] if matches else None

    def _is_mine(self, kind: str, row: dict, *, actor_id: str,
                 actor_alias: str) -> bool:
        if _STORE_OF_KIND[kind] in _ID_STORES:
            return row.get("owner_id") == actor_id
        return row.get("owner_alias") == actor_alias

    def _owned_row(self, kind: str, ref: str, *, actor_id: str,
                   actor_alias: str, role: str) -> dict:
        """Resolve a ref AND prove the caller owns it. Refs are scoped:
        a list name (or thread key) may exist under several owners — the
        caller's own row wins. A ref that exists only under another
        owner is an OwnershipError (the cross-owner refusal), not a
        quiet miss; a ref that exists nowhere is ObjectNotFoundError."""
        matches = self._find_all(kind, ref)
        if not matches:
            raise ObjectNotFoundError(f"{role} {kind} {ref!r} does not exist")
        for row in matches:
            if self._is_mine(kind, row, actor_id=actor_id,
                             actor_alias=actor_alias):
                return row
        raise OwnershipError(
            f"{role} {kind} {ref!r} belongs to another owner")

    # — The write operation: "file this under …" ─────────────────────────

    def file_under(self, *, actor_id: str, actor_alias: str,
                   subject: tuple[str, str], target: tuple[str, str],
                   at: str | None = None) -> dict:
        """File subject under target for the caller. Idempotent: filing
        the same pair twice returns the existing row (the migration's
        ON CONFLICT DO NOTHING, mirrored)."""
        subject_kind, subject_ref = subject
        target_kind, target_ref = target
        if subject_kind not in SUBJECT_KINDS:
            raise UnknownKindError(f"subject kind {subject_kind!r} is not linkable")
        if target_kind not in TARGET_KINDS:
            raise UnknownKindError(f"target kind {target_kind!r} cannot be filed under")
        if subject_kind == target_kind and subject_ref == target_ref:
            raise ObjectLinkError("an object cannot be filed under itself")
        self._owned_row(subject_kind, subject_ref, actor_id=actor_id,
                        actor_alias=actor_alias, role="subject")
        self._owned_row(target_kind, target_ref, actor_id=actor_id,
                        actor_alias=actor_alias, role="target")
        for link in self.links:
            if (link["owner_alias"] == actor_alias
                    and link["subject_kind"] == subject_kind
                    and link["subject_ref"] == subject_ref
                    and link["target_kind"] == target_kind
                    and link["target_ref"] == target_ref):
                return link
        link = {
            "id": str(uuid.uuid4()),
            "owner_alias": actor_alias,
            "owner_id": actor_id,
            "subject_kind": subject_kind,
            "subject_ref": subject_ref,
            "target_kind": target_kind,
            "target_ref": target_ref,
            "relation": RELATION_FILED_UNDER,
            "created_at": at,
        }
        self.links.append(link)
        return link

    def unfile(self, *, actor_id: str, actor_alias: str,
               subject: tuple[str, str], target: tuple[str, str]) -> bool:
        """Remove the caller's link row. Returns False when no such
        filing existed. The object row is never touched — deleting a
        link deletes the link, nothing else."""
        subject_kind, subject_ref = subject
        target_kind, target_ref = target
        for i, link in enumerate(self.links):
            if (link["owner_id"] == actor_id
                    and link["owner_alias"] == actor_alias
                    and link["subject_kind"] == subject_kind
                    and link["subject_ref"] == subject_ref
                    and link["target_kind"] == target_kind
                    and link["target_ref"] == target_ref):
                del self.links[i]
                return True
        return False

    # — Owner-named facts (element #19, on the same rows' model) ────────

    def set_fact(self, *, actor_id: str, actor_alias: str,
                 obj: tuple[str, str], key: str, value: str,
                 at: str | None = None) -> dict:
        """Write one plain fact on an object the caller owns. Upserts by
        (object, normalized key); a NEW key beyond FACT_LIMIT is refused
        (the migration's trigger, mirrored)."""
        kind, ref = obj
        if kind not in SUBJECT_KINDS:
            raise UnknownKindError(f"kind {kind!r} cannot carry facts")
        self._owned_row(kind, ref, actor_id=actor_id,
                        actor_alias=actor_alias, role="object")
        fact_key = normalize_fact_key(key)
        if len(value or "") > _FACT_VALUE_MAX:
            raise ObjectLinkError("fact value exceeds 500 characters")
        for fact in self.facts:
            if (fact["owner_alias"] == actor_alias
                    and fact["object_kind"] == kind
                    and fact["object_ref"] == ref
                    and fact["fact_key"] == fact_key):
                fact["fact_value"] = value
                fact["updated_at"] = at
                return fact
        mine = [f for f in self.facts
                if f["owner_alias"] == actor_alias
                and f["object_kind"] == kind and f["object_ref"] == ref]
        if len(mine) >= FACT_LIMIT:
            raise FactLimitError(
                f"{kind} {ref!r} already carries {FACT_LIMIT} facts")
        fact = {
            "id": str(uuid.uuid4()),
            "owner_alias": actor_alias,
            "owner_id": actor_id,
            "object_kind": kind,
            "object_ref": ref,
            "fact_key": fact_key,
            "fact_value": value,
            "created_at": at,
            "updated_at": at,
        }
        self.facts.append(fact)
        return fact

    def facts_for(self, *, actor_alias: str, obj: tuple[str, str]) -> dict:
        """The object's facts as {key: value}, in the owner's scope."""
        kind, ref = obj
        return {f["fact_key"]: f["fact_value"] for f in self.facts
                if f["owner_alias"] == actor_alias
                and f["object_kind"] == kind and f["object_ref"] == ref}

    # — Reads: one object, many homes, no copies ────────────────────────

    def read_object(self, obj: tuple[str, str]) -> dict:
        """The object's own surface: its store row itself."""
        kind, ref = obj
        if kind not in SUBJECT_KINDS:
            raise UnknownKindError(f"kind {kind!r} is not readable")
        row = self._find(kind, ref)
        if row is None:
            raise ObjectNotFoundError(f"{kind} {ref!r} does not exist")
        return row

    def _resolve_owned(self, *, actor_alias: str,
                       obj: tuple[str, str]) -> dict:
        """Resolve a ref inside one owner's scope (every Phase-0 store
        row carries owner_alias). Falls back to the bare ref match for
        rows that predate the stamp."""
        kind, ref = obj
        for row in self._find_all(kind, ref):
            if row.get("owner_alias") == actor_alias:
                return row
        return self.read_object(obj)

    def filed_under(self, *, actor_alias: str,
                    target: tuple[str, str]) -> list[dict]:
        """Every object filed under a target, resolved to the objects'
        own store rows — references resolved, never copies: the dicts
        returned ARE the store rows, so an edit made once is read
        everywhere."""
        target_kind, target_ref = target
        out: list[dict] = []
        for link in self.links:
            if (link["owner_alias"] == actor_alias
                    and link["target_kind"] == target_kind
                    and link["target_ref"] == target_ref):
                out.append(self._resolve_owned(
                    actor_alias=actor_alias,
                    obj=(link["subject_kind"], link["subject_ref"])))
        return out

    def homes_of(self, *, actor_alias: str,
                 obj: tuple[str, str]) -> list[tuple[str, str]]:
        """The targets an object is filed under — its homes."""
        kind, ref = obj
        return [(link["target_kind"], link["target_ref"]) for link in self.links
                if link["owner_alias"] == actor_alias
                and link["subject_kind"] == kind
                and link["subject_ref"] == ref]

    def person_home(self, *, actor_alias: str, person_key: str,
                    timeline_events: list[dict]) -> list[dict]:
        """The person's home: their timeline (the read model from
        tools/person_timeline.py — events in, filtered to this person)
        merged with everything filed under them, one chronological
        stream. Filed entries carry the object's own row under "object"
        — the same row its own surface reads."""
        entries: list[dict] = []
        for event in timeline_events:
            if event.get("person_key") == person_key:
                entries.append({"home_kind": "timeline_event",
                                "at": event.get("event_at"), "event": event})
        for link in self.links:
            if (link["owner_alias"] == actor_alias
                    and link["target_kind"] == "person"
                    and link["target_ref"] == person_key):
                entries.append({
                    "home_kind": "filed_object",
                    "at": link["created_at"],
                    "object": self._resolve_owned(
                        actor_alias=actor_alias,
                        obj=(link["subject_kind"], link["subject_ref"])),
                    "subject_kind": link["subject_kind"],
                    "subject_ref": link["subject_ref"],
                })
        entries.sort(key=lambda e: (e["at"] is None, e["at"] or ""))
        return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True,
                        help="JSON file of store rows + optional ops")
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--actor-alias", required=True)
    args = parser.parse_args()
    data = json.loads(open(args.input, encoding="utf-8").read())
    store = LinkStore(
        naya_notes=data.get("naya_notes", []),
        smart_links=data.get("smart_links", []),
        persons=data.get("persons", []),
        smart_notes=data.get("smart_notes", []),
        mail_threads=data.get("mail_threads", []),
        lists=data.get("lists", []),
    )
    for link in data.get("links", []):
        store.links.append(link)
    for fact in data.get("facts", []):
        store.facts.append(fact)
    for op in data.get("ops", []):
        if op["op"] == "file_under":
            store.file_under(
                actor_id=args.actor_id, actor_alias=args.actor_alias,
                subject=(op["subject_kind"], op["subject_ref"]),
                target=(op["target_kind"], op["target_ref"]),
                at=op.get("at"))
        elif op["op"] == "set_fact":
            store.set_fact(
                actor_id=args.actor_id, actor_alias=args.actor_alias,
                obj=(op["object_kind"], op["object_ref"]),
                key=op["key"], value=op["value"], at=op.get("at"))
        else:
            raise SystemExit(f"unknown op {op['op']!r}")
    json.dump({"links": store.links, "facts": store.facts},
              sys.stdout, indent=1, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
