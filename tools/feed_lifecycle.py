#!/usr/bin/env python3
"""
feed_lifecycle.py — Specialty-feed lifecycle registry (#2244 requirement 2).

The nine standing team feeds (#1865-#1873) exist today only as GitHub issue
titles; focused feeds get created ad hoc with no lifecycle at all. #2244 req 2
says: reuse existing feeds when they fit; create a focused feed only for a
material project/problem; keep it open while unresolved/ongoing; close it with
a resolution receipt and a canonical Smart Note link.

This module is the machine form of that rule — a fail-closed registry:

  OPEN -> RESOLVED -> CLOSED          (focused feeds only)

  * create:  a focused feed needs a title, an owner, a material justification
             (>= 40 chars — a real reason, not "misc"), and a parent standing
             feed that exists and is OPEN. Idempotent: re-creating the same
             title under the same parent while OPEN returns the existing feed.
  * resolve: OPEN -> RESOLVED needs a resolution receipt: outcome, a
             Smart-Note id (SN-NNNN), and a Smart-Note link. No receipt, no
             resolve. This is the #2244 close rule, enforced.
  * close:   RESOLVED -> CLOSED is archival. OPEN -> CLOSED is illegal — a feed
             cannot skip its resolution receipt.
  * reopen:  RESOLVED -> OPEN (regression). The prior resolution is kept in
             resolution_history, never silently dropped.
  * standing feeds (#1865-#1873) are seeded by `init` and are PROTECTED: they
             are standing by ratified protocol and can never be resolved,
             closed, or reopened by this tool. Learning events may still be
             linked to them.

Fail-closed: a missing/corrupt registry, an unknown feed id, or an illegal
transition raises a named error — never a silent default. The registry records
claims (receipts, links); it does not verify Smart Notes exist — that check
belongs to a live verifier, not this ledger.

Store: ~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/feed-registry.json
by default (goal runtime-state dir — outside BRAIN/, so zero brain-index
drift); `registry_path(root)` / `--root` override it (tests use a temp dir).
Like the #2296 event ledger, runtime state only — never canonical repo content.

Seam (not wired): match() resolves a feed by id, issue number, or issue URL —
the lookup #2296's envelope SHARED gate ("requires the specialty-feed URL")
can consult once that PR lands. This PR does not touch #2296.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone

SCHEMA = "naya.feed_registry.v1"

# The nine standing specialty feeds, from the ratified Team Naya Operating
# Protocol. Titles verified against the live issues 2026-10-11.
STANDING_FEEDS = [
    (1865, "[TEAM FEED] Learning"),
    (1866, "[TEAM FEED] Brain / Memory"),
    (1867, "[TEAM FEED] Law / Governance"),
    (1868, "[TEAM FEED] Architecture / Engineering / Operations"),
    (1869, "[TEAM FEED] Evolution / Succession"),
    (1870, "[TEAM FEED] Interfaces / Hub"),
    (1871, "[TEAM FEED] Knowledge / Intelligence"),
    (1872, "[TEAM FEED] Proving / Verifying"),
    (1873, "[TEAM FEED] Innovation"),
]

REPO = "SoulSchoolAcademy/NayaPOWER"
MIN_JUSTIFICATION = 40
MIN_OUTCOME = 20
SMART_NOTE_RE = re.compile(r"^SN-\d{2,}$")
URL_RE = re.compile(r"^https?://\S+$")


class FeedRegistryError(Exception):
    """Base: the registry cannot be trusted or used. Fail closed."""


class RegistryNotInitializedError(FeedRegistryError):
    """No registry exists yet — run `init` first. Never auto-created."""


class RegistryCorruptError(FeedRegistryError):
    """Registry exists but is unreadable or misshapen. Fix by hand, not by guess."""


class UnknownFeedError(FeedRegistryError):
    """No feed with that id / issue number / URL."""


class IllegalTransitionError(FeedRegistryError):
    """The lifecycle move is not allowed from the feed's current state."""


class StandingFeedProtectedError(IllegalTransitionError):
    """Standing feeds are ratified-law persistent; they cannot resolve or close."""


class ValidationError(FeedRegistryError):
    """A field failed its contract (empty title, short justification, bad note id...)."""


def _utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _default_root():
    home = os.path.expanduser("~")
    return os.path.join(
        home, "workspace/goals/nayapower-10-10-completion-drive/hidden_files"
    )


def registry_path(root=None):
    root = root or _default_root()
    return os.path.join(root, "feed-registry.json")


def _issue_url(number):
    return f"https://github.com/{REPO}/issues/{number}"


def _slug(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
    return slug or "feed"


def _norm_title(title):
    return re.sub(r"\s+", " ", title.strip().casefold())


# ---------------------------------------------------------------------------
# Registry IO (fail-closed, atomic writes)
# ---------------------------------------------------------------------------

def _blank_registry():
    return {"schema": SCHEMA, "feeds": []}


def load_registry(root=None):
    path = registry_path(root)
    if not os.path.exists(path):
        raise RegistryNotInitializedError(
            f"no feed registry at {path}; run `feed_lifecycle.py init` first"
        )
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        raise RegistryCorruptError(f"registry at {path} unreadable: {e}")
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise RegistryCorruptError(
            f"registry at {path}: expected schema {SCHEMA!r}, "
            f"got {doc.get('schema')!r}" if isinstance(doc, dict) else
            f"registry at {path}: top-level JSON is not an object"
        )
    feeds = doc.get("feeds")
    if not isinstance(feeds, list):
        raise RegistryCorruptError(f"registry at {path}: 'feeds' is not a list")
    seen = set()
    for feed in feeds:
        if not isinstance(feed, dict):
            raise RegistryCorruptError(f"registry at {path}: feed entry not an object")
        for key in ("feed_id", "title", "kind", "status"):
            if key not in feed:
                raise RegistryCorruptError(
                    f"registry at {path}: feed missing required key {key!r}"
                )
        if feed["feed_id"] in seen:
            raise RegistryCorruptError(
                f"registry at {path}: duplicate feed_id {feed['feed_id']!r}"
            )
        seen.add(feed["feed_id"])
    return doc


def save_registry(doc, root=None):
    path = registry_path(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".feed-registry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _find(doc, feed_id):
    for feed in doc["feeds"]:
        if feed["feed_id"] == feed_id:
            return feed
    raise UnknownFeedError(f"unknown feed_id {feed_id!r}")


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def init_registry(root=None, actor="unknown"):
    """Seed the nine standing feeds. Idempotent: never duplicates, never overwrites."""
    path = registry_path(root)
    if os.path.exists(path):
        doc = load_registry(root)  # fail closed on corrupt existing
    else:
        doc = _blank_registry()
    existing = {f["feed_id"] for f in doc["feeds"]}
    now = _utcnow()
    added = []
    for number, title in STANDING_FEEDS:
        feed_id = f"feed-{number}"
        if feed_id in existing:
            continue
        doc["feeds"].append({
            "feed_id": feed_id,
            "title": title,
            "kind": "standing",
            "issue_number": number,
            "issue_url": _issue_url(number),
            "status": "OPEN",
            "created_at": now,
            "created_by": actor,
            "material_justification": "standing feed per ratified Team Naya Operating Protocol",
            "parent_feed": None,
            "resolution": None,
            "resolution_history": [],
            "linked_events": [],
        })
        added.append(feed_id)
    save_registry(doc, root)
    return {"initialized": True, "path": path, "added": added,
            "standing_feeds": len(STANDING_FEEDS)}


def _require_nonempty(value, name, maximum=200):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    if len(value.strip()) > maximum:
        raise ValidationError(f"{name} exceeds {maximum} chars")
    return value.strip()


def create_focused_feed(title, owner, material_justification, parent_feed,
                        issue_number=None, root=None):
    """Create a focused feed. Idempotent on (normalized title, parent) while OPEN."""
    doc = load_registry(root)
    title = _require_nonempty(title, "title")
    owner = _require_nonempty(owner, "owner", maximum=120)
    if not isinstance(material_justification, str) or \
            len(material_justification.strip()) < MIN_JUSTIFICATION:
        raise ValidationError(
            f"material_justification needs >= {MIN_JUSTIFICATION} chars of real "
            f"reason (got {len((material_justification or '').strip())}) — "
            f"a focused feed is only for a material project/problem"
        )
    material_justification = material_justification.strip()
    parent = _find(doc, parent_feed)
    if parent["kind"] != "standing":
        raise ValidationError(
            f"parent_feed {parent_feed!r} is not a standing feed — focused feeds "
            f"split from a standing feed, not from another focused feed"
        )
    if parent["status"] != "OPEN":
        raise ValidationError(f"parent_feed {parent_feed!r} is not OPEN")
    if issue_number is not None:
        if not isinstance(issue_number, int) or issue_number <= 0:
            raise ValidationError("issue_number must be a positive int")

    norm = _norm_title(title)
    for feed in doc["feeds"]:
        if (feed["kind"] == "focused" and feed["status"] == "OPEN"
                and feed.get("parent_feed") == parent["feed_id"]
                and _norm_title(feed["title"]) == norm):
            return {"feed_id": feed["feed_id"], "duplicate": True,
                    "feed": feed}

    base = f"feed-{_slug(title)}-{_utcnow()[:10].replace('-', '')}"
    feed_id = base
    n = 2
    taken = {f["feed_id"] for f in doc["feeds"]}
    while feed_id in taken:
        feed_id = f"{base}-{n}"
        n += 1

    feed = {
        "feed_id": feed_id,
        "title": title,
        "kind": "focused",
        "issue_number": issue_number,
        "issue_url": _issue_url(issue_number) if issue_number else None,
        "status": "OPEN",
        "created_at": _utcnow(),
        "created_by": owner,
        "material_justification": material_justification,
        "parent_feed": parent["feed_id"],
        "resolution": None,
        "resolution_history": [],
        "linked_events": [],
    }
    doc["feeds"].append(feed)
    save_registry(doc, root)
    return {"feed_id": feed_id, "duplicate": False, "feed": feed}


def link_issue(feed_id, issue_number, root=None):
    """Bind the GitHub issue venue to a feed (created separately by a seat)."""
    doc = load_registry(root)
    feed = _find(doc, feed_id)
    if not isinstance(issue_number, int) or issue_number <= 0:
        raise ValidationError("issue_number must be a positive int")
    feed["issue_number"] = issue_number
    feed["issue_url"] = _issue_url(issue_number)
    save_registry(doc, root)
    return {"feed_id": feed_id, "issue_url": feed["issue_url"]}


def _check_receipt(outcome, smart_note_id, smart_note_link, evidence_refs):
    if not isinstance(outcome, str) or len(outcome.strip()) < MIN_OUTCOME:
        raise ValidationError(
            f"resolution outcome needs >= {MIN_OUTCOME} chars (got "
            f"{len((outcome or '').strip())})"
        )
    if not isinstance(smart_note_id, str) or not SMART_NOTE_RE.match(smart_note_id.strip()):
        raise ValidationError(
            f"smart_note_id must look like SN-NNNN (got {smart_note_id!r})"
        )
    if not isinstance(smart_note_link, str) or not URL_RE.match(smart_note_link.strip()):
        raise ValidationError("smart_note_link must be an http(s) URL")
    refs = evidence_refs or []
    if not isinstance(refs, list) or any(not isinstance(r, str) or not r.strip() for r in refs):
        raise ValidationError("evidence_refs must be a list of non-empty strings")
    return {
        "outcome": outcome.strip(),
        "smart_note_id": smart_note_id.strip(),
        "smart_note_link": smart_note_link.strip(),
        "evidence_refs": [r.strip() for r in refs],
    }


def resolve_feed(feed_id, outcome, smart_note_id, smart_note_link,
                 evidence_refs=None, actor="unknown", root=None):
    """OPEN -> RESOLVED. Requires the #2244 resolution receipt. Standing feeds: refused."""
    doc = load_registry(root)
    feed = _find(doc, feed_id)
    if feed["kind"] == "standing":
        raise StandingFeedProtectedError(
            f"{feed_id!r} is a standing feed (ratified protocol) — it stays OPEN; "
            f"resolve/close do not apply"
        )
    if feed["status"] != "OPEN":
        raise IllegalTransitionError(
            f"cannot resolve {feed_id!r}: status is {feed['status']}, need OPEN"
        )
    receipt = _check_receipt(outcome, smart_note_id, smart_note_link, evidence_refs)
    receipt["resolved_at"] = _utcnow()
    receipt["resolved_by"] = actor
    feed["resolution"] = receipt
    feed["status"] = "RESOLVED"
    save_registry(doc, root)
    return {"feed_id": feed_id, "status": "RESOLVED", "resolution": receipt}


def close_feed(feed_id, actor="unknown", root=None):
    """RESOLVED -> CLOSED (archival). OPEN -> CLOSED is illegal: no skipping the receipt."""
    doc = load_registry(root)
    feed = _find(doc, feed_id)
    if feed["kind"] == "standing":
        raise StandingFeedProtectedError(
            f"{feed_id!r} is a standing feed (ratified protocol) — it stays OPEN"
        )
    if feed["status"] != "RESOLVED":
        raise IllegalTransitionError(
            f"cannot close {feed_id!r}: status is {feed['status']}, need RESOLVED "
            f"(a feed closes only with its resolution receipt)"
        )
    feed["status"] = "CLOSED"
    feed["closed_at"] = _utcnow()
    feed["closed_by"] = actor
    save_registry(doc, root)
    return {"feed_id": feed_id, "status": "CLOSED"}


def reopen_feed(feed_id, reason, actor="unknown", root=None):
    """RESOLVED -> OPEN (regression). Prior resolution kept in resolution_history."""
    doc = load_registry(root)
    feed = _find(doc, feed_id)
    if feed["kind"] == "standing":
        raise StandingFeedProtectedError(
            f"{feed_id!r} is a standing feed — always OPEN, nothing to reopen"
        )
    if feed["status"] != "RESOLVED":
        raise IllegalTransitionError(
            f"cannot reopen {feed_id!r}: status is {feed['status']}, need RESOLVED"
        )
    reason = _require_nonempty(reason, "reason", maximum=500)
    feed["resolution_history"].append(feed["resolution"])
    feed["resolution"] = None
    feed["status"] = "OPEN"
    feed["reopened_at"] = _utcnow()
    feed["reopened_by"] = actor
    feed["reopen_reason"] = reason
    save_registry(doc, root)
    return {"feed_id": feed_id, "status": "OPEN"}


def link_event(feed_id, event_id, root=None):
    """Attach a learning-event id (from #2296's envelope) to a feed. Deduped."""
    doc = load_registry(root)
    feed = _find(doc, feed_id)
    event_id = _require_nonempty(event_id, "event_id", maximum=200)
    if event_id not in feed["linked_events"]:
        feed["linked_events"].append(event_id)
        save_registry(doc, root)
        return {"feed_id": feed_id, "linked": True, "event_id": event_id}
    return {"feed_id": feed_id, "linked": False, "event_id": event_id,
            "note": "already linked"}


def get_feed(feed_id, root=None):
    return _find(load_registry(root), feed_id)


def list_feeds(status=None, kind=None, root=None):
    doc = load_registry(root)
    out = doc["feeds"]
    if status:
        out = [f for f in out if f["status"] == status]
    if kind:
        out = [f for f in out if f["kind"] == kind]
    return out


def match(query, root=None):
    """Resolve a feed by feed_id, issue number ("1868"/"#1868"), or issue URL.

    Returns the feed in whatever status it holds (OPEN/RESOLVED/CLOSED) — the
    caller decides what a status means. The seam #2296's envelope SHARED gate
    can consult: a specialty-feed URL is only meaningful if it resolves to a
    known feed; whether the gate also requires OPEN is the gate's own check,
    not this lookup's.
    """
    doc = load_registry(root)
    q = query.strip()
    for feed in doc["feeds"]:
        if feed["feed_id"] == q or feed.get("issue_url") == q:
            return feed
    m = re.fullmatch(r"#?(\d+)", q)
    if m:
        for feed in doc["feeds"]:
            if feed.get("issue_number") == int(m.group(1)):
                return feed
    raise UnknownFeedError(f"no feed matches {query!r}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _emit(obj, as_json):
    if as_json:
        # Compact single-line JSON for machines (pipelines, jq).
        print(json.dumps(obj, ensure_ascii=False))
    else:
        # Indented JSON for humans reading the terminal.
        print(json.dumps(obj, indent=2, ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Specialty-feed lifecycle registry (#2244 req 2)")
    ap.add_argument("--root", default=None, help="registry dir override (tests)")
    ap.add_argument("--json", action="store_true",
                      help="compact single-line JSON output (for machines); "
                           "default is indented JSON for humans")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="seed the nine standing feeds (idempotent)")

    p = sub.add_parser("create", help="create a focused feed")
    p.add_argument("--title", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--justification", required=True)
    p.add_argument("--parent", required=True, help="parent standing feed id, e.g. feed-1868")
    p.add_argument("--issue", type=int, default=None)

    p = sub.add_parser("link-issue", help="bind a GitHub issue venue to a feed")
    p.add_argument("--feed", required=True)
    p.add_argument("--issue", type=int, required=True)

    p = sub.add_parser("resolve", help="OPEN -> RESOLVED with a resolution receipt")
    p.add_argument("--feed", required=True)
    p.add_argument("--outcome", required=True)
    p.add_argument("--smart-note-id", required=True)
    p.add_argument("--smart-note-link", required=True)
    p.add_argument("--evidence", action="append", default=[])
    p.add_argument("--actor", default="unknown")

    p = sub.add_parser("close", help="RESOLVED -> CLOSED (archival)")
    p.add_argument("--feed", required=True)
    p.add_argument("--actor", default="unknown")

    p = sub.add_parser("reopen", help="RESOLVED -> OPEN (regression)")
    p.add_argument("--feed", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--actor", default="unknown")

    p = sub.add_parser("link-event", help="attach a learning-event id to a feed")
    p.add_argument("--feed", required=True)
    p.add_argument("--event", required=True)

    p = sub.add_parser("get", help="show one feed")
    p.add_argument("--feed", required=True)

    p = sub.add_parser("list", help="list feeds, optionally filtered")
    p.add_argument("--status", choices=["OPEN", "RESOLVED", "CLOSED"], default=None)
    p.add_argument("--kind", choices=["standing", "focused"], default=None)

    p = sub.add_parser("match", help="resolve a feed by id, issue number, or URL")
    p.add_argument("query")

    args = ap.parse_args(argv)
    try:
        if args.cmd == "init":
            out = init_registry(root=args.root)
        elif args.cmd == "create":
            out = create_focused_feed(args.title, args.owner, args.justification,
                                      args.parent, issue_number=args.issue, root=args.root)
        elif args.cmd == "link-issue":
            out = link_issue(args.feed, args.issue, root=args.root)
        elif args.cmd == "resolve":
            out = resolve_feed(args.feed, args.outcome, args.smart_note_id,
                               args.smart_note_link, evidence_refs=args.evidence,
                               actor=args.actor, root=args.root)
        elif args.cmd == "close":
            out = close_feed(args.feed, actor=args.actor, root=args.root)
        elif args.cmd == "reopen":
            out = reopen_feed(args.feed, args.reason, actor=args.actor, root=args.root)
        elif args.cmd == "link-event":
            out = link_event(args.feed, args.event, root=args.root)
        elif args.cmd == "get":
            out = get_feed(args.feed, root=args.root)
        elif args.cmd == "list":
            out = {"feeds": list_feeds(status=args.status, kind=args.kind, root=args.root)}
        elif args.cmd == "match":
            out = match(args.query, root=args.root)
    except FeedRegistryError as e:
        print(f"FEED_LIFECYCLE_REFUSED: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    _emit(out, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
