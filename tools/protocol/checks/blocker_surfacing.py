#!/usr/bin/env python3
"""Proactive Blocker Surfacing (Shawn, 2026-10-09 — part of the Two-Layer ask).

"Every Naya watches for what's broken/blocked and comes saying
'this won't work because X — here's what unblocks it,' in the two-layer
format. Not silence while stuck, not a report after it broke."

A seat that is BLOCKED — or STALLED (no progress inside the stall window)
— with no blocker post in its recent reports FAILS. Silence while stuck
is the violation.

The blocker post must itself honor the Two-Layer Law (reused, not
re-invented: blocker_post is a consequential report type in two_layer.py)
AND it must name two things explicitly:
  - blocker_x: WHAT is broken/blocked (the X)
  - unblock_action: WHAT unblocks it

Record:
    {
      "seat": "naya-5",
      "status": "blocked" | "working" | "stalled" | "done" | "idle",
      "checked_at": "<ISO timestamp>",
      "last_progress_at": "<ISO timestamp>",
      "stall_window_hours": 3,
      "recent_reports": [
        {
          "report_type": "blocker_post",
          "title": "...",
          "technical": "...",
          "plain_human": "...",
          "blocker_x": "<what is broken>",
          "unblock_action": "<what unblocks it>"
        }
      ]
    }

Checks (fail-closed: shape first via shape_closed.validate_shape):
  1. seat, status, checked_at present; status in the known set.
     Unknown status fails closed — it is never treated as "fine".
  2. done/idle -> PASS (nothing stuck).
  3. working -> needs last_progress_at within stall_window_hours of
     checked_at; otherwise the seat is STALLED and needs a blocker post.
  4. blocked/stalled -> a qualifying blocker post must exist in
     recent_reports: names blocker_x AND unblock_action AND passes
     the Two-Layer check. Otherwise FAIL (blocked-with-silence).

Usage:
    python3 tools/protocol/checks/blocker_surfacing.py \\
        --record '{"seat": "naya-5", "status": "blocked", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402
from checks.shape_closed import validate_shape  # noqa: E402
from checks.two_layer import check as two_layer_check  # noqa: E402

STATUSES = {"working", "blocked", "stalled", "done", "idle"}
DEFAULT_STALL_WINDOW_HOURS = 3


def _parse_ts(value) -> datetime | None:
    try:
        ts = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts
    except Exception:
        return None


def _qualifying_blocker_post(post: dict) -> tuple[bool, str]:
    """A blocker post qualifies iff it names X, names the unblock action,
    and passes the Two-Layer Law (blocker_post is consequential)."""
    if not isinstance(post, dict):
        return False, "not a record"
    ok, reasons = validate_shape(
        post,
        {
            "required": ["blocker_x", "unblock_action"],
            "types": {"blocker_x": "str", "unblock_action": "str"},
            "non_empty": ["blocker_x", "unblock_action"],
        },
    )
    if not ok:
        return False, reasons[0]
    tl = two_layer_check(post)
    if not tl["pass"]:
        return False, "two-layer failure: " + tl["reasons"][0]
    return True, "names blocker_x and unblock_action, two-layer honored"


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "BLOCKER-SURFACING", "law_status": "RATIFIED"}
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    ok, shape_reasons = validate_shape(
        record,
        {
            "required": ["seat", "status", "checked_at"],
            "types": {
                "seat": "str",
                "status": "str",
                "checked_at": "str",
                "stall_window_hours": "int",
            },
            "non_empty": ["seat", "status", "checked_at"],
            "allowed": {"status": sorted(STATUSES)},
        },
    )
    if not ok:
        return fail(
            "shape failure: " + shape_reasons[0]
            + " — an unknown/absent status is never treated as 'fine'",
            details,
        )
    reasons.extend(shape_reasons)

    seat = str(record["seat"]).strip()
    status = str(record["status"]).strip().lower()
    details["seat"] = seat
    details["status"] = status

    checked_at = _parse_ts(record["checked_at"])
    if checked_at is None:
        return fail(
            f"{seat}: checked_at is not a parseable timestamp — "
            "fail closed, cannot assess staleness",
            details,
        )
    window = record.get("stall_window_hours", DEFAULT_STALL_WINDOW_HOURS)
    if not isinstance(window, (int, float)) or window <= 0:
        window = DEFAULT_STALL_WINDOW_HOURS
    details["stall_window_hours"] = window

    if status in {"done", "idle"}:
        reasons.append(f"{seat}: status {status!r} — nothing stuck, nothing to surface")
        return result(True, reasons, details)

    needs_post = False
    if status == "working":
        last = _parse_ts(record.get("last_progress_at"))
        if last is None:
            return fail(
                f"{seat}: status 'working' but last_progress_at is missing or "
                "unparseable — progress cannot be proven, so the seat is "
                "STALLED until proven otherwise",
                details,
            )
        age = checked_at - last
        if age <= timedelta(hours=window):
            reasons.append(
                f"{seat}: working, progress {age} ago — inside the "
                f"{window}h window, not stalled"
            )
            return result(True, reasons, details)
        needs_post = True
        details["stalled"] = True
        reasons.append(
            f"{seat}: working but no progress for {age} — STALLED "
            "(exceeds the 3h window); a blocker post is now required"
        )
    else:  # blocked or stalled
        needs_post = True
        reasons.append(f"{seat}: status {status!r} — a blocker post is required")

    # Blocked/stalled: silence is the violation. Look for a qualifying post.
    reports = record.get("recent_reports")
    if not isinstance(reports, list) or not reports:
        return fail(
            f"{seat}: {status} with NO recent reports — blocked/stalled with "
            "silence. The law: come saying 'this won't work because X — "
            "here's what unblocks it,' in the two-layer format.",
            details,
        )

    failures: list[str] = []
    for i, post in enumerate(reports):
        ok_post, why = _qualifying_blocker_post(post)
        if ok_post:
            reasons.append(
                f"qualifying blocker post found (report #{i}): {why}"
            )
            details["blocker_post_index"] = i
            return result(True, reasons, details)
        failures.append(f"report #{i}: {why}")

    return fail(
        f"{seat}: {status} with {len(reports)} recent report(s) but NONE "
        "qualifies as a blocker post — " + "; ".join(failures),
        details,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Proactive blocker surfacing check")
    parser.add_argument("--record", required=True,
                        help="JSON seat-status record (or @file)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "BLOCKER-SURFACING"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
