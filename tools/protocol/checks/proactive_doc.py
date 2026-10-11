#!/usr/bin/env python3
"""SN-PROACTIVE-DOC — Proactive Documentation.

"When any agent sees something valuable — lesson, pattern, fix, insight —
it MUST be documented without waiting to be told. Not documenting
discovered value is a disservice."

This module is the executable check this law was missing (the audit's WEAK
finding: "SN-PROACTIVE-DOC has no CLI"). The semantic core stays in
kernel/protocol/learning_capture.py — check_lesson() remains the canonical
lesson/provenance rule, and this module delegates to it rather than
reimplementing it. What this module adds:

  1. A real CLI (main(): --record JSON/@file, --json, exit 0 PASS / 1 FAIL)
     so the law is enforceable from CI and from any worker's shell.
  2. The PROACTIVE dimension: a lesson carries captured_at and
     work_completed_at. A lesson written weeks after the work is not
     proactive — late capture fails unless a late_reason is stated.
  3. The DOCUMENTED dimension: a lesson must name its destination (file
     path, smart-note id, memory log) — "documented" means written
     somewhere retrievable, not claimed in chat.

Input record:
    {
      "work_description": "<what work was done>",
      "lesson": "<the durable, reusable insight>" | "",
      "no_lesson_reason": "<why there is none>" | "",
      "provenance": "<evidence the lesson rests on>",
      "captured_at": "<ISO-8601 UTC timestamp>",
      "work_completed_at": "<ISO-8601 UTC timestamp>",
      "destination": "<where it was written>",
      "late_reason": "<why capture lagged>" | "",
      "max_lag_hours": 72            # optional override of the lag budget
    }

Checks:
  1. work_description present and non-empty.
  2. Kernel core (delegated): lesson XOR no_lesson_reason — silence fails;
     a captured lesson requires provenance.
  3. captured_at present and ISO-8601-parseable when a lesson is captured.
  4. Proactive timing: captured_at - work_completed_at <= max_lag_hours
     (default 72). Late capture without a late_reason fails.
  5. destination present and non-empty when a lesson is captured.

Fail-closed: any malformed record fails with a specific reason.

Usage:
    python3 tools/protocol/checks/proactive_doc.py --record '{"work_description": "...", ...}' [--json]
    python3 tools/protocol/checks/proactive_doc.py --record @cycle.json [--json]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_CHECK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_CHECK_DIR.parent))          # tools/protocol/checks helpers
sys.path.insert(0, str(_CHECK_DIR.parents[2]))     # repo root, for kernel.*
from checks import emit, fail, load_record, result  # noqa: E402

try:
    from kernel.protocol.learning_capture import CycleLesson, check_lesson
    _KERNEL_CORE = True
except Exception:  # kernel unavailable — local rules still enforced, flagged
    _KERNEL_CORE = False

DEFAULT_MAX_LAG_HOURS = 72.0


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_ts(value, field: str) -> datetime:
    """Parse an ISO-8601 timestamp; raise ValueError naming the field."""
    if not _nonempty(value):
        raise ValueError(f"{field} missing — a captured lesson must be timestamped")
    text = value.strip()
    try:
        # fromisoformat handles offsets; a trailing Z is normalized first.
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"{field} is not ISO-8601: {value!r}") from None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _max_lag_hours(record: dict) -> float:
    raw = record.get("max_lag_hours", DEFAULT_MAX_LAG_HOURS)
    try:
        hours = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"max_lag_hours must be numeric, got {raw!r}") from None
    if hours <= 0:
        raise ValueError(f"max_lag_hours must be positive, got {raw!r}")
    return hours


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-PROACTIVE-DOC"}
    subject = (record.get("work_description") or "").strip() or "(undescribed work)"
    details["work"] = subject[:120]

    if not _nonempty(record.get("work_description")):
        return fail(f"{subject}: work_description missing — a cycle with no "
                    f"described work cannot be checked for capture", details)
    reasons.append("work described")

    # Fail-closed on wrong types: a non-string lesson/excuse/provenance/
    # destination is malformed, not absent.
    for field in ("lesson", "no_lesson_reason", "provenance", "destination"):
        value = record.get(field)
        if value is not None and not isinstance(value, str):
            return fail(f"{subject}: {field} must be a string, got "
                        f"{type(value).__name__} — malformed record", details)

    lesson = record.get("lesson")
    if _nonempty(lesson):
        details["lesson_chars"] = len(lesson.strip())
    else:
        details["lesson_chars"] = 0

    # --- kernel core: lesson XOR no_lesson_reason; lesson -> provenance ---
    if _KERNEL_CORE:
        kernel_res = check_lesson(
            CycleLesson(
                work_description=record.get("work_description", ""),
                lesson=lesson if isinstance(lesson, str) else "",
                no_lesson_reason=record.get("no_lesson_reason")
                if isinstance(record.get("no_lesson_reason"), str) else "",
                provenance=record.get("provenance")
                if isinstance(record.get("provenance"), str) else "",
            )
        )
        details["kernel_delegated"] = True
        if not kernel_res.passed:
            return fail(
                f"{subject}: kernel learning_capture rejects the cycle — "
                f"{'; '.join(kernel_res.reasons)}",
                details,
            )
        reasons.append("kernel core: lesson declared or honestly excused, "
                       "provenance present")
    else:
        details["kernel_delegated"] = False
        has_lesson = _nonempty(lesson)
        has_excuse = _nonempty(record.get("no_lesson_reason"))
        if has_lesson == has_excuse:  # both or neither
            return fail(
                f"{subject}: give exactly one of lesson / no_lesson_reason — "
                f"silence is not documentation",
                details,
            )
        if has_lesson and not _nonempty(record.get("provenance")):
            return fail(f"{subject}: lesson captured without provenance — "
                        f"evidence required", details)
        reasons.append("local core: lesson declared or honestly excused, "
                       "provenance present (kernel unavailable — flagged)")

    if not _nonempty(lesson):
        reasons.append("no lesson claimed; reason stated — cycle honestly closed")
        return result(True, reasons, details)

    # --- proactive timing ---
    try:
        captured = _parse_ts(record.get("captured_at"), "captured_at")
    except ValueError as e:
        return fail(f"{subject}: {e}", details)
    try:
        completed = _parse_ts(record.get("work_completed_at"), "work_completed_at")
    except ValueError as e:
        return fail(f"{subject}: {e}", details)
    if captured < completed:
        return fail(f"{subject}: captured_at predates work_completed_at — "
                    f"a lesson cannot be captured before the work", details)
    try:
        budget = _max_lag_hours(record)
    except ValueError as e:
        return fail(f"{subject}: {e}", details)
    lag_hours = (captured - completed).total_seconds() / 3600.0
    details["lag_hours"] = round(lag_hours, 2)
    details["max_lag_hours"] = budget
    if lag_hours > budget:
        if not _nonempty(record.get("late_reason")):
            return fail(
                f"{subject}: lesson captured {lag_hours:.1f}h after the work "
                f"(budget {budget:g}h) with no late_reason — a lesson written "
                f"this late is not proactive documentation",
                details,
            )
        reasons.append(f"late capture ({lag_hours:.1f}h) excused with a reason")
    else:
        reasons.append(f"captured {lag_hours:.1f}h after the work (budget {budget:g}h)")

    # --- documented means written somewhere retrievable ---
    destination = record.get("destination")
    if not _nonempty(destination):
        return fail(
            f"{subject}: destination missing — a lesson with nowhere written "
            f"down (file path, smart-note id, memory log) is not documentation",
            details,
        )
    details["destination"] = destination.strip()
    reasons.append(f"destination named: {destination.strip()[:80]}")

    reasons.append(f"{subject}: lesson captured proactively and documented")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-PROACTIVE-DOC capture check")
    parser.add_argument("--record", required=True,
                        help="JSON work-cycle record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-PROACTIVE-DOC"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
