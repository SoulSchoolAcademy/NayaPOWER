#!/usr/bin/env python3
"""Worker notification outbox — #2244 req 4: timely awareness as a real mechanism.

When a failure, lesson, blocker, or breakthrough occurs, affected workers must
*receive* awareness — not merely have a post exist that someone may later read.
This module is the delivery half of the Brain Communication Architecture:

- ``publish``   append a notification event to the outbox (idempotent on dedup_key)
- ``pending``   list unacknowledged, unexpired events for an audience
- ``ack``       record that an audience handled an event (stops redelivery)
- ``sweep``     purge expired events and their orphaned receipts
- ``deliver_pending``  what tools/worker_entry.py calls at activation: surfaces the
  pending digest and records per-run delivery receipts. NEVER raises.

Honesty bounds (what this does NOT claim):
- NOT real-time. Delivery is poll-based: a worker sees notifications when it
  activates (worker_entry.py runs first in every cron contract). #2244 forbids
  claiming "real-time" without an end-to-end runtime trace; the trace we claim is
  the two-process test in tests/test_notify_outbox.py (publish in one process,
  surface in another).
- Same-machine only. State is local JSONL, not a network service. The worker
  fleet shares this VM, which is the fleet's actual deployment.
- At-least-once, not exactly-once. An unacknowledged event is re-surfaced every
  run until acked or expired (that re-surfacing IS the retry behavior).
- No authentication. The trust boundary is the shared VM, same as every other
  file in the goal's hidden_files state dir. Never put secrets in a notification.

Storage: NAYA_NOTIFY_ROOT env, else
~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/notify-outbox/
(outbox.jsonl, deliveries.jsonl, acks.jsonl). Runtime state lives OUTSIDE the
repo on purpose: committing per-run notifications would dirty every worker's
tree. Only this code ships in the repo.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEVERITIES = ("info", "attention", "urgent", "blocker")
DEFAULT_TTL_HOURS = 24
MAX_TTL_HOURS = 168  # 7 days: retry is bounded, never forever

OUTBOX_FILE = "outbox.jsonl"
DELIVERIES_FILE = "deliveries.jsonl"
ACKS_FILE = "acks.jsonl"


def _default_root() -> Path:
    goal_state = (
        Path.home()
        / "workspace"
        / "goals"
        / "nayapower-10-10-completion-drive"
        / "hidden_files"
    )
    return goal_state / "notify-outbox"


def root() -> Path:
    """Resolve the outbox state root (env override wins, for tests)."""
    override = os.environ.get("NAYA_NOTIFY_ROOT")
    return Path(override).expanduser() if override else _default_root()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(value: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(value)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def _read_jsonl(path: Path) -> tuple[list[dict], int]:
    """Read JSONL, skipping corrupt lines. Returns (rows, corrupt_count).

    A corrupt line never crashes the reader: it is counted and skipped, because
    a poisoned state file must not break worker activation.
    """
    rows: list[dict] = []
    corrupt = 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    corrupt += 1
                    continue
                if isinstance(obj, dict):
                    rows.append(obj)
                else:
                    corrupt += 1
    except FileNotFoundError:
        pass
    return rows, corrupt


def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, separators=(",", ":")) + "\n")


def _rewrite_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for obj in rows:
            f.write(json.dumps(obj, separators=(",", ":")) + "\n")
    os.replace(tmp, path)


def _validate_event(event: dict) -> dict:
    """Validate + normalize a publish payload. Raises ValueError on rejection."""
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    etype = event.get("type")
    severity = event.get("severity")
    audience = event.get("audience")
    title = event.get("title")
    if not etype or not isinstance(etype, str):
        raise ValueError("event.type is required (string)")
    if severity not in SEVERITIES:
        raise ValueError(f"event.severity must be one of {SEVERITIES}")
    if isinstance(audience, str):
        audience = [audience]
    if not audience or not isinstance(audience, list) or not all(
        isinstance(a, str) and a for a in audience
    ):
        raise ValueError("event.audience is required (non-empty string or list)")
    if not title or not isinstance(title, str):
        raise ValueError("event.title is required (string)")

    now = _now()
    ttl_hours = event.get("ttl_hours", DEFAULT_TTL_HOURS)
    try:
        ttl_hours = float(ttl_hours)
    except (TypeError, ValueError):
        raise ValueError("event.ttl_hours must be a number")
    if not 0 < ttl_hours <= MAX_TTL_HOURS:
        raise ValueError(f"event.ttl_hours must be in (0, {MAX_TTL_HOURS}]")

    source = event.get("source")
    if source is not None:
        if not isinstance(source, dict) or not source.get("artifact"):
            raise ValueError("event.source must be {artifact, sha?} when present")

    return {
        "id": event.get("id") or uuid.uuid4().hex,
        "dedup_key": event.get("dedup_key") or event.get("id") or uuid.uuid4().hex,
        "ts": now.isoformat(),
        "type": etype,
        "severity": severity,
        "audience": sorted(set(audience)),
        "title": title,
        "body": event.get("body") or "",
        "source": source,
        "expires_at": (now + timedelta(hours=ttl_hours)).isoformat(),
        "publisher": event.get("publisher") or os.environ.get("NAYA_WORKER_ID", "unknown"),
    }


def _is_expired(event: dict, now: datetime) -> bool:
    exp = _parse_ts(event.get("expires_at", ""))
    return exp is None or exp <= now


def _events() -> list[dict]:
    rows, _ = _read_jsonl(root() / OUTBOX_FILE)
    return rows


def _acks() -> list[dict]:
    rows, _ = _read_jsonl(root() / ACKS_FILE)
    return rows


def find_by_dedup_key(dedup_key: str, now: datetime | None = None) -> dict | None:
    """Live (non-expired) event with this dedup_key, else None."""
    now = now or _now()
    for e in _events():
        if e.get("dedup_key") == dedup_key and not _is_expired(e, now):
            return e
    return None


def publish(event: dict) -> str:
    """Append an event; idempotent on dedup_key. Returns the event id.

    Re-publishing with the same dedup_key while the original is still live
    returns the original id and writes nothing (no duplicates).
    """
    norm = _validate_event(event)
    existing = find_by_dedup_key(norm["dedup_key"])
    if existing:
        return existing["id"]
    _append_jsonl(root() / OUTBOX_FILE, norm)
    return norm["id"]


def is_acknowledged(event_id: str, audience: str) -> bool:
    return any(
        a.get("event_id") == event_id and a.get("audience") == audience
        for a in _acks()
    )


def _addressed_to(event: dict, audience: str) -> bool:
    aud = event.get("audience") or []
    return audience in aud or "all" in aud


def pending(audience: str, now: datetime | None = None) -> list[dict]:
    """Unacknowledged, unexpired events addressed to this audience.

    Unacknowledged events re-appear on every call: that re-surfacing IS the
    retry. Expiry bounds it.
    """
    now = now or _now()
    return [
        e
        for e in _events()
        if _addressed_to(e, audience)
        and not _is_expired(e, now)
        and not is_acknowledged(e["id"], audience)
    ]


def ack(event_id: str, audience: str, worker: str, note: str = "") -> bool:
    """Record that an audience handled an event. Unknown id -> False, no write."""
    now = _now()
    if not any(e.get("id") == event_id and not _is_expired(e, now) for e in _events()):
        return False
    _append_jsonl(
        root() / ACKS_FILE,
        {
            "event_id": event_id,
            "audience": audience,
            "worker": worker,
            "note": note,
            "ts": now.isoformat(),
        },
    )
    return True


def sweep(now: datetime | None = None) -> dict:
    """Purge expired events + orphaned receipts. Returns counts."""
    now = now or _now()
    r = root()
    events, _ = _read_jsonl(r / OUTBOX_FILE)
    live = [e for e in events if not _is_expired(e, now)]
    live_ids = {e["id"] for e in live}
    _rewrite_jsonl(r / OUTBOX_FILE, live)

    deliveries, _ = _read_jsonl(r / DELIVERIES_FILE)
    kept_deliveries = [d for d in deliveries if d.get("event_id") in live_ids]
    _rewrite_jsonl(r / DELIVERIES_FILE, kept_deliveries)

    acks, _ = _read_jsonl(r / ACKS_FILE)
    kept_acks = [a for a in acks if a.get("event_id") in live_ids]
    _rewrite_jsonl(r / ACKS_FILE, kept_acks)

    return {
        "expired_events_purged": len(events) - len(live),
        "delivery_receipts_purged": len(deliveries) - len(kept_deliveries),
        "acks_purged": len(acks) - len(kept_acks),
        "live_events": len(live),
    }


def _format_digest(events: list[dict], audience: str) -> str:
    lines = [f"--- NOTIFICATIONS ({len(events)} pending for audience '{audience}') ---"]
    for e in events:
        exp = _parse_ts(e.get("expires_at", ""))
        ttl = f", expires {_fmt_delta(exp)}" if exp else ""
        lines.append(f"[{e['severity']}] {e['title']} (id {e['id'][:8]}{ttl})")
        if e.get("body"):
            lines.append(f"  {e['body'][:280]}")
        src = e.get("source") or {}
        if src.get("artifact"):
            sha = (src.get("sha") or "")[:8]
            lines.append(f"  source: {src['artifact']}" + (f"@{sha}" if sha else ""))
    lines.append(
        "--- end notifications "
        f"(ack handled items: python3 tools/notify_outbox.py ack <id> --audience {audience}) ---"
    )
    return "\n".join(lines)


def _fmt_delta(exp: datetime) -> str:
    delta = exp - _now()
    hours = delta.total_seconds() / 3600
    if hours < 1:
        return f"in {int(delta.total_seconds() / 60)}m"
    return f"in {hours:.1f}h"


def deliver_pending(audience: str, worker_label: str) -> str:
    """Surface pending notifications for a worker run. NEVER raises.

    Called by tools/worker_entry.py at activation. Records a delivery receipt
    per event per run (audit trail), returns the human-readable digest
    ("" when nothing is pending). Any internal failure yields "" — a broken
    outbox must never break worker activation.
    """
    try:
        events = pending(audience)
        if not events:
            return ""
        run_id = f"{worker_label}-{uuid.uuid4().hex[:8]}-{_now().isoformat()}"
        for e in events:
            _append_jsonl(
                root() / DELIVERIES_FILE,
                {
                    "event_id": e["id"],
                    "audience": audience,
                    "run_id": run_id,
                    "ts": _now().isoformat(),
                },
            )
        return _format_digest(events, audience)
    except Exception:
        return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", help="outbox state dir (overrides NAYA_NOTIFY_ROOT)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("publish", help="publish a notification event")
    p.add_argument("--type", required=True)
    p.add_argument("--severity", required=True, choices=SEVERITIES)
    p.add_argument("--audience", required=True, help="comma-separated, e.g. naya2,build (or 'all')")
    p.add_argument("--title", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--dedup-key", default=None)
    p.add_argument("--ttl-hours", type=float, default=DEFAULT_TTL_HOURS)
    p.add_argument("--source-artifact", default=None)
    p.add_argument("--source-sha", default=None)
    p.add_argument("--publisher", default=None)

    q = sub.add_parser("pending", help="list pending events for an audience")
    q.add_argument("--audience", required=True)

    k = sub.add_parser("ack", help="acknowledge an event for an audience")
    k.add_argument("event_id")
    k.add_argument("--audience", required=True)
    k.add_argument("--worker", default=None)
    k.add_argument("--note", default="")

    sub.add_parser("sweep", help="purge expired events and orphaned receipts")

    args = parser.parse_args(argv)
    if args.root:
        os.environ["NAYA_NOTIFY_ROOT"] = args.root

    def out(obj):
        if args.json:
            print(json.dumps(obj, indent=2))
        else:
            print(json.dumps(obj, indent=2) if isinstance(obj, (dict, list)) else obj)

    if args.cmd == "publish":
        event = {
            "type": args.type,
            "severity": args.severity,
            "audience": [a.strip() for a in args.audience.split(",") if a.strip()],
            "title": args.title,
            "body": args.body,
            "dedup_key": args.dedup_key,
            "ttl_hours": args.ttl_hours,
            "publisher": args.publisher,
        }
        if args.source_artifact:
            event["source"] = {"artifact": args.source_artifact, "sha": args.source_sha}
        try:
            eid = publish(event)
        except ValueError as ve:
            print(f"rejected: {ve}", file=sys.stderr)
            return 2
        out({"id": eid})
        return 0

    if args.cmd == "pending":
        out(pending(args.audience))
        return 0

    if args.cmd == "ack":
        worker = args.worker or os.environ.get("NAYA_WORKER_ID", "cli")
        ok = ack(args.event_id, args.audience, worker, args.note)
        if not ok:
            print(f"no live event {args.event_id}", file=sys.stderr)
            return 2
        out({"acked": args.event_id, "audience": args.audience})
        return 0

    if args.cmd == "sweep":
        out(sweep())
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
