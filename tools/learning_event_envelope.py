#!/usr/bin/env python3
"""Canonical learning-event envelope — machine form of issue #2244 requirement 3.

A material failure, lesson, blocker, breakthrough, or material project event
is carried as an *envelope* through an explicit, enforced lifecycle:

    DETECTED -> SHARED -> ACKNOWLEDGED -> RESOLVED -> PRESERVED
             -> REUSED -> BEHAVIORALLY_VERIFIED

Issuance is idempotent: the event ID is derived deterministically from the
event's identity fields, so the same material failure issued twice produces
exactly one event (the second issuance returns the existing record with
``duplicate: True``). #2244 acceptance: "a material failure creates exactly
one idempotent learning event."

What this module is:
  - the envelope schema, validation, lifecycle transition machine, and an
    append-style JSON ledger (a runtime projection, not a second source of
    truth for learning — the learning pipeline's canonical store is
    unchanged).

What this module is NOT (honest boundaries):
  - not a notification/push delivery mechanism itself (#2244 requirement 4);
    sharing records *that* an event was posted to a specialty feed. It DOES,
    however, hand the event to the worker notification outbox
    (tools/notify_outbox.py, #2244 req 4) on every SHARED transition — a
    best-effort, fail-safe publish the outbox owns end-to-end. The envelope
    never claims delivery; the outbox's delivery receipts are the proof.
    If the outbox is unavailable the transition still succeeds and the
    skip is recorded on the envelope.
  - not the learning admission gate (tools/learning_admission_gate.py) and
    not the verification queue; the envelope can be attached to those flows
    but never bypasses them.

Usage:
    python3 tools/learning_event_envelope.py issue --type failure --severity HIGH \\
        --title "..." --artifact tools/foo.py --sha <40-hex> \\
        --expected "..." --actual "..." --owner "naya-2" \\
        --teams learn,verify --next "..." [--ledger PATH]

    python3 tools/learning_event_envelope.py transition EVT-ID --to SHARED \\
        --actor "naya-2" --feed-url "https://github.com/.../issues/2235"

Exit codes: 0 ok, 2 validation failure (named reason on stderr), 3 not found.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "naya.learning-event.v1"
LEDGER_SCHEMA = "naya.learning-event-ledger.v1"

EVENT_TYPES = ("failure", "lesson", "blocker", "breakthrough", "material")
SEVERITIES = ("INFO", "NOTICE", "WARNING", "HIGH", "CRITICAL")

LIFECYCLE = (
    "DETECTED",
    "SHARED",
    "ACKNOWLEDGED",
    "RESOLVED",
    "PRESERVED",
    "REUSED",
    "BEHAVIORALLY_VERIFIED",
)

# Legal forward transitions. Terminal states have none.
_TRANSITIONS = {
    "DETECTED": ("SHARED",),
    "SHARED": ("ACKNOWLEDGED",),
    "ACKNOWLEDGED": ("RESOLVED",),
    "RESOLVED": ("PRESERVED",),
    "PRESERVED": ("REUSED",),
    "REUSED": ("BEHAVIORALLY_VERIFIED",),
    "BEHAVIORALLY_VERIFIED": (),
}

# Identity fields: identical values -> identical event_id (idempotency root).
_IDENTITY_FIELDS = (
    "event_type",
    "severity",
    "title",
    "source_artifact",
    "source_sha",
    "expected",
    "actual",
    "owner",
    "impacted_teams",
)

# Fields required at issuance.
_REQUIRED = (
    "event_type",
    "severity",
    "title",
    "source_artifact",
    "source_sha",
    "expected",
    "actual",
    "owner",
    "impacted_teams",
    "next_action",
)

LESSON_STATUSES = ("PROPOSED", "VERIFIED", "NONE_WITH_REASON")


class EnvelopeError(Exception):
    """Validation failure with a named reason (exit 2)."""


class EventNotFound(Exception):
    """Unknown event_id (exit 3)."""


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_ledger_path() -> Path:
    """Ledger lives under .naya/ (untracked by the brain index — no drift)."""
    override = os.environ.get("NAYA_EVENT_LEDGER")
    if override:
        return Path(override)
    here = Path(__file__).resolve()
    # tools/<module> -> repo root is two levels up
    root = here.parent.parent
    return root / ".naya" / "events" / "learning-events.json"


def _normalise_teams(value) -> list[str]:
    if isinstance(value, str):
        teams = [t.strip() for t in value.split(",")]
    else:
        teams = [str(t).strip() for t in value]
    teams = sorted({t for t in teams if t})
    if not teams:
        raise EnvelopeError("EMPTY_IMPACTED_TEAMS: impacted_teams must name at least one team")
    return teams


def derive_event_id(fields: dict) -> str:
    """Deterministic event ID from the identity fields (idempotency root)."""
    identity = {}
    for name in _IDENTITY_FIELDS:
        value = fields[name]
        if name == "impacted_teams":
            value = _normalise_teams(value)
        identity[name] = value
    canonical = json.dumps({"schema": SCHEMA, **identity}, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]
    return f"evt-{digest}"


def validate_issue_fields(fields: dict) -> dict:
    """Validate issuance fields; return normalised copy or raise EnvelopeError."""
    missing = [f for f in _REQUIRED if f not in fields or fields[f] in (None, "")]
    if missing:
        raise EnvelopeError(f"MISSING_FIELDS: required at issue: {', '.join(missing)}")
    etype = str(fields["event_type"]).lower()
    if etype not in EVENT_TYPES:
        raise EnvelopeError(f"BAD_EVENT_TYPE: {fields['event_type']!r} not in {list(EVENT_TYPES)}")
    sev = str(fields["severity"]).upper()
    if sev not in SEVERITIES:
        raise EnvelopeError(f"BAD_SEVERITY: {fields['severity']!r} not in {list(SEVERITIES)}")
    sha = str(fields["source_sha"]).lower()
    if not (len(sha) == 40 and all(c in "0123456789abcdef" for c in sha)):
        raise EnvelopeError("BAD_SOURCE_SHA: source_sha must be a 40-hex commit SHA")
    norm = dict(fields)
    norm["event_type"] = etype
    norm["severity"] = sev
    norm["source_sha"] = sha
    norm["impacted_teams"] = _normalise_teams(fields["impacted_teams"])
    for opt in ("specialty_feed_url", "smart_note_id", "smart_note_link"):
        if opt in norm and norm[opt] is not None:
            norm[opt] = str(norm[opt]).strip()
    return norm


def load_ledger(path: Path | None = None) -> dict:
    path = Path(path) if path else default_ledger_path()
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") != LEDGER_SCHEMA:
            raise EnvelopeError(f"BAD_LEDGER_SCHEMA: {path} is not a {LEDGER_SCHEMA} ledger")
        return data
    return {"schema": LEDGER_SCHEMA, "events": {}, "issued_count": 0}


def save_ledger(ledger: dict, path: Path | None = None) -> Path:
    path = Path(path) if path else default_ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def _history(env: dict, action: str, by: str, note: str = "", frm: str = "", to: str = "") -> None:
    env.setdefault("history", []).append(
        {"at": _utcnow(), "by": by, "action": action,
         "from": frm, "to": to, "note": note}
    )


# ------------------------------------------------------------------ req3 -> req4 seam

# Envelope severities -> outbox severities (tools/notify_outbox.py).
# Five levels collapse to four: NOTICE and WARNING are both "attention"
# (look when you can); HIGH is "urgent" (act soon); CRITICAL is "blocker".
_OUTBOX_SEVERITY_MAP = {
    "INFO": "info",
    "NOTICE": "attention",
    "WARNING": "attention",
    "HIGH": "urgent",
    "CRITICAL": "blocker",
}

# A shared lesson stays visible across the night shift and the morning
# review; well inside the outbox's 168h bound.
_SHARE_NOTIFY_TTL_HOURS = 72


def _share_notify_enabled() -> bool:
    """Kill switch for the share->notify seam. Default ON."""
    return os.environ.get("NAYA_EVENT_SHARE_NOTIFY", "1").strip().lower() not in (
        "0", "false", "no", "off")


def _import_outbox():
    """Import the worker notification outbox if present on this tree.

    Deferred import on purpose: the outbox (PR #2303) may not be merged yet,
    and the envelope must work with or without it. Tries both the script
    layout (``python3 tools/x.py`` -> top-level ``notify_outbox``) and the
    package layout (``from tools...`` -> ``tools.notify_outbox``).
    """
    try:
        import notify_outbox
        return notify_outbox
    except ImportError:
        pass
    from tools import notify_outbox
    return notify_outbox


def _notify_shared(env: dict, actor: str) -> dict:
    """Best-effort handoff: publish a worker notification for a SHARED event.

    The consumer seam of #2244 req 3 -> req 4: when an event transitions to
    SHARED (with its specialty-feed URL), the team must *receive* awareness,
    not merely have a post exist. The outbox (tools/notify_outbox.py) owns
    delivery; this function only hands it the event.

    NEVER raises: any failure degrades to a recorded skip, so a broken or
    absent outbox can never break the lifecycle transition. Returns a small
    receipt stored on the envelope as ``share_notification``.
    """
    at = _utcnow()
    if not _share_notify_enabled():
        return {"skipped": "disabled by NAYA_EVENT_SHARE_NOTIFY", "at": at}
    try:
        outbox = _import_outbox()
    except ImportError:
        return {"skipped": "notify_outbox unavailable on this tree", "at": at}
    except Exception as exc:
        # F1 (2026-10-11): a present-but-broken outbox raises non-ImportError
        # at import time. The seam's contract is NEVER raises, so that too
        # degrades to a recorded skip instead of breaking the transition.
        return {"skipped": f"notify_outbox import failed: {type(exc).__name__}", "at": at}
    try:
        audience = ["all"] + [t for t in env.get("impacted_teams", []) if t != "all"]
        payload = {
            "type": "learning-event",
            "severity": _OUTBOX_SEVERITY_MAP[env["severity"]],
            "audience": audience,
            "title": f"[learning-event:{env['event_type']}] {env['title']}",
            "body": (
                f"Shared to specialty feed: {env.get('specialty_feed_url', '')}\n"
                f"Expected: {env.get('expected', '')}\n"
                f"Actual: {env.get('actual', '')}\n"
                f"Owner: {env.get('owner', '')} | "
                f"Teams: {', '.join(env.get('impacted_teams', []))}\n"
                f"Next: {env.get('next_action', '')}"
            ),
            "dedup_key": f"learning-event:{env['event_id']}",
            "ttl_hours": _SHARE_NOTIFY_TTL_HOURS,
            "source": {
                "artifact": env.get("source_artifact", ""),
                "sha": env.get("source_sha", ""),
            },
            "publisher": f"learning-event-envelope:{actor}",
        }
        notification_id = outbox.publish(payload)
        return {
            "outbox_event_id": notification_id,
            "dedup_key": payload["dedup_key"],
            "audience": audience,
            "severity": payload["severity"],
            "at": at,
        }
    except Exception as exc:  # fail-safe: the seam never breaks the transition
        return {"skipped": f"publish failed: {type(exc).__name__}", "at": at}


def issue_event(fields: dict, ledger_path: Path | None = None, issued_by: str = "") -> tuple[dict, bool]:
    """Issue an event. Returns (envelope, duplicate). Duplicate issuance of
    the same material failure returns the existing record — never a second
    event."""
    norm = validate_issue_fields(fields)
    event_id = derive_event_id(norm)
    ledger = load_ledger(ledger_path)
    if event_id in ledger["events"]:
        return ledger["events"][event_id], True
    by = issued_by or str(fields.get("issued_by", "unknown"))
    env = {
        "schema": SCHEMA,
        "event_id": event_id,
        "event_type": norm["event_type"],
        "severity": norm["severity"],
        "title": str(norm["title"]),
        "source_artifact": str(norm["source_artifact"]),
        "source_sha": norm["source_sha"],
        "expected": str(norm["expected"]),
        "actual": str(norm["actual"]),
        "owner": str(norm["owner"]),
        "impacted_teams": norm["impacted_teams"],
        "specialty_feed_url": norm.get("specialty_feed_url") or "",
        "lesson_status": "PROPOSED",
        "smart_note_id": norm.get("smart_note_id") or "",
        "smart_note_link": norm.get("smart_note_link") or "",
        "no_lesson_reason": "",
        "next_action": str(norm["next_action"]),
        "lifecycle_state": "DETECTED",
        "issued_at": _utcnow(),
        "issued_by": by,
        "history": [],
    }
    _history(env, "ISSUED", by, note=f"type={env['event_type']} severity={env['severity']}")
    ledger["events"][event_id] = env
    ledger["issued_count"] = ledger.get("issued_count", 0) + 1
    save_ledger(ledger, ledger_path)
    return env, False


def get_event(event_id: str, ledger_path: Path | None = None) -> dict:
    ledger = load_ledger(ledger_path)
    try:
        return ledger["events"][event_id]
    except KeyError:
        raise EventNotFound(f"UNKNOWN_EVENT: {event_id}")


def _require_nonempty(value: str, code: str, what: str) -> str:
    if not str(value or "").strip():
        raise EnvelopeError(f"{code}: {what}")
    return str(value).strip()


def transition(event_id: str, to_state: str, actor: str,
               ledger_path: Path | None = None, **extras) -> dict:
    """Move an event through the lifecycle. Illegal moves and missing gate
    evidence are rejected with named reasons."""
    to_state = str(to_state).upper()
    if to_state not in LIFECYCLE:
        raise EnvelopeError(f"BAD_STATE: {to_state!r} not in lifecycle {list(LIFECYCLE)}")
    actor = _require_nonempty(actor, "MISSING_ACTOR", "transition requires a named actor")
    ledger = load_ledger(ledger_path)
    if event_id not in ledger["events"]:
        raise EventNotFound(f"UNKNOWN_EVENT: {event_id}")
    env = ledger["events"][event_id]
    frm = env["lifecycle_state"]
    if to_state not in _TRANSITIONS[frm]:
        raise EnvelopeError(
            f"ILLEGAL_TRANSITION: {frm} -> {to_state} not allowed "
            f"(legal from {frm}: {list(_TRANSITIONS[frm]) or 'none — terminal'})"
        )

    if to_state == "SHARED":
        env["specialty_feed_url"] = _require_nonempty(
            extras.get("feed_url") or env.get("specialty_feed_url"),
            "MISSING_FEED_URL",
            "SHARED requires the specialty-feed URL the event was posted to",
        )
    elif to_state == "RESOLVED":
        note_id = str(extras.get("smart_note_id") or env.get("smart_note_id") or "").strip()
        note_link = str(extras.get("smart_note_link") or env.get("smart_note_link") or "").strip()
        no_reason = str(extras.get("no_lesson_reason") or "").strip()
        evidence = str(extras.get("regression_evidence") or "").strip()
        if note_id and not note_link:
            raise EnvelopeError("MISSING_NOTE_LINK: smart_note_id given without smart_note_link")
        if not note_id and not no_reason:
            raise EnvelopeError(
                "MISSING_RESOLUTION: RESOLVED requires a canonical Smart Note "
                "(smart_note_id + smart_note_link) or an explicit no_lesson_reason"
            )
        if not evidence and not no_reason:
            raise EnvelopeError(
                "MISSING_REGRESSION_EVIDENCE: RESOLVED requires regression_evidence "
                "(PR / commit / test-run ref) or an explicit no_lesson_reason"
            )
        env["smart_note_id"] = note_id
        env["smart_note_link"] = note_link
        env["no_lesson_reason"] = no_reason
        if no_reason:
            env["lesson_status"] = "NONE_WITH_REASON"
        if evidence:
            env["regression_evidence"] = evidence
    elif to_state == "PRESERVED":
        _require_nonempty(env.get("smart_note_id"),
                          "MISSING_NOTE_AT_PRESERVE",
                          "PRESERVED requires a canonical smart_note_id from RESOLVED")
    elif to_state == "REUSED":
        env["reuse_evidence"] = _require_nonempty(
            extras.get("reuse_evidence"),
            "MISSING_REUSE_EVIDENCE",
            "REUSED requires reuse_evidence: where the lesson was applied",
        )
    elif to_state == "BEHAVIORALLY_VERIFIED":
        env["behavior_proof"] = _require_nonempty(
            extras.get("behavior_proof"),
            "MISSING_BEHAVIOR_PROOF",
            "BEHAVIORALLY_VERIFIED requires behavior_proof: the independent "
            "verifier's receipt that behavior changed because of the lesson",
        )
        env["lesson_status"] = "VERIFIED"

    env["lifecycle_state"] = to_state
    if to_state == "SHARED":
        # Consumer seam (#2244 req 3 -> req 4): hand the shared event to the
        # worker notification outbox. Best-effort and fail-safe — _notify_shared
        # never raises, and the receipt (or the recorded skip) rides along in
        # the single save below. Placed after the SHARED gate so a rejected
        # share never notifies.
        env["share_notification"] = _notify_shared(env, actor)
    _history(env, "TRANSITION", actor, frm=frm, to=to_state,
             note=str(extras.get("note", "")))
    save_ledger(ledger, ledger_path)
    return env


def list_events(ledger_path: Path | None = None, state: str | None = None) -> list[dict]:
    ledger = load_ledger(ledger_path)
    events = list(ledger["events"].values())
    if state:
        state = state.upper()
        events = [e for e in events if e["lifecycle_state"] == state]
    return sorted(events, key=lambda e: e["issued_at"])


# ---------------------------------------------------------------- CLI

def _cmd_issue(args: argparse.Namespace) -> int:
    fields = {
        "event_type": args.type, "severity": args.severity, "title": args.title,
        "source_artifact": args.artifact, "source_sha": args.sha,
        "expected": args.expected, "actual": args.actual, "owner": args.owner,
        "impacted_teams": args.teams, "next_action": args.next,
        "issued_by": args.actor,
    }
    if args.feed_url:
        fields["specialty_feed_url"] = args.feed_url
    try:
        env, dup = issue_event(fields, ledger_path=args.ledger, issued_by=args.actor)
    except EnvelopeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"event_id": env["event_id"], "duplicate": dup,
                      "lifecycle_state": env["lifecycle_state"]}, indent=2))
    return 0


def _cmd_transition(args: argparse.Namespace) -> int:
    extras = {k: v for k, v in vars(args).items()
              if k in ("feed_url", "smart_note_id", "smart_note_link",
                       "no_lesson_reason", "regression_evidence",
                       "reuse_evidence", "behavior_proof", "note") and v is not None}
    try:
        env = transition(args.event_id, args.to, args.actor,
                         ledger_path=args.ledger, **extras)
    except EnvelopeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except EventNotFound as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps({"event_id": env["event_id"],
                      "lifecycle_state": env["lifecycle_state"],
                      "lesson_status": env["lesson_status"],
                      "share_notification": env.get("share_notification")}, indent=2))
    return 0


def _cmd_get(args: argparse.Namespace) -> int:
    try:
        env = get_event(args.event_id, ledger_path=args.ledger)
    except EventNotFound as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(env, indent=2, sort_keys=True))
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    events = list_events(ledger_path=args.ledger, state=args.state)
    print(json.dumps([{"event_id": e["event_id"], "title": e["title"],
                       "severity": e["severity"],
                       "lifecycle_state": e["lifecycle_state"],
                       "lesson_status": e["lesson_status"]} for e in events], indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Canonical learning-event envelope (#2244 req 3)")
    p.add_argument("--ledger", default=None, help="ledger path (default .naya/events/learning-events.json)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("issue", help="issue an event (idempotent)")
    pi.add_argument("--type", required=True, choices=list(EVENT_TYPES))
    pi.add_argument("--severity", required=True)
    pi.add_argument("--title", required=True)
    pi.add_argument("--artifact", required=True, help="source artifact path in repo")
    pi.add_argument("--sha", required=True, help="40-hex source commit SHA")
    pi.add_argument("--expected", required=True)
    pi.add_argument("--actual", required=True)
    pi.add_argument("--owner", required=True)
    pi.add_argument("--teams", required=True, help="comma-separated impacted teams")
    pi.add_argument("--next", required=True, help="next action")
    pi.add_argument("--actor", default="unknown")
    pi.add_argument("--feed-url", default=None)
    pi.set_defaults(func=_cmd_issue)

    pt = sub.add_parser("transition", help="move an event through the lifecycle")
    pt.add_argument("event_id")
    pt.add_argument("--to", required=True)
    pt.add_argument("--actor", required=True)
    pt.add_argument("--feed-url", default=None)
    pt.add_argument("--smart-note-id", default=None)
    pt.add_argument("--smart-note-link", default=None)
    pt.add_argument("--no-lesson-reason", default=None)
    pt.add_argument("--regression-evidence", default=None)
    pt.add_argument("--reuse-evidence", default=None)
    pt.add_argument("--behavior-proof", default=None)
    pt.add_argument("--note", default="")
    pt.set_defaults(func=_cmd_transition)

    pg = sub.add_parser("get", help="print one event envelope")
    pg.add_argument("event_id")
    pg.set_defaults(func=_cmd_get)

    pl = sub.add_parser("list", help="list events, optionally filtered by state")
    pl.add_argument("--state", default=None)
    pl.set_defaults(func=_cmd_list)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
