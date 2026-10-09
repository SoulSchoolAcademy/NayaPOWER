#!/usr/bin/env python3
"""SN-0732 — What it means to be a Naya (Shawn ratified 2026-10-09).

"Do the right thing all the time. Do the most intelligent thing at all
times. Produce value at all times."

And the duty that follows: intelligence capture is identity, not
assignment. Every conversation, every feed thread, every correction is
a capture surface — capture it, share it with the team, do not wait to
be told. One Naya's lesson is every Naya's lesson.

"If a lesson needs Shawn to say 'capture that,' the identity has not
compounded yet."

Validates a lesson record. The hard lines: a lesson captured only
because Shawn said "capture that" fails — capture is identity, not
obedience; a captured-but-unshared lesson fails — one Naya's lesson is
every Naya's lesson.

Input record:
    {
      "lesson": "<the durable lesson, in plain words>",
      "captured": true,
      "capture_trigger": "proactive" | "shawn_said_capture_that" | "teammate_relay",
      "shared_with_team": true,
      "share_surface": "#1354"
    }

Checks:
  1. lesson non-empty (produce value at all times — emptiness is not value).
  2. captured == true.
  3. capture_trigger != "shawn_said_capture_that" (identity, not assignment).
  4. shared_with_team == true and share_surface non-empty
     (one Naya's lesson is every Naya's lesson).

Usage:
    python3 tools/protocol/checks/naya_identity.py \
        --record '{"lesson": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

DEPENDENT_TRIGGER = "shawn_said_capture_that"


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0732", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    lesson = str(record.get("lesson") or "").strip()
    captured = record.get("captured", False)
    trigger = str(record.get("capture_trigger") or "").strip().lower()
    shared = record.get("shared_with_team", False)
    surface = str(record.get("share_surface") or "").strip()

    if not lesson:
        return fail("lesson empty — 'produce value at all times'; emptiness is not value",
                    details)
    reasons.append("lesson carries value")

    if captured is not True:
        return fail("captured is not true — every correction is a capture surface",
                    details)
    reasons.append("captured")

    if trigger == DEPENDENT_TRIGGER:
        return fail(
            "capture_trigger is 'shawn_said_capture_that' — capture is identity, "
            "not assignment. If a lesson needs Shawn to say 'capture that,' "
            "the identity has not compounded yet.",
            details,
        )
    if not trigger:
        return fail("capture_trigger missing — state how this lesson was captured",
                    details)
    reasons.append(f"captured proactively ({trigger})")
    details["capture_trigger"] = trigger

    if shared is not True:
        return fail(
            "shared_with_team is not true — one Naya's lesson is every Naya's lesson; "
            "a captured-but-unshared lesson dies with its seat",
            details,
        )
    if not surface:
        return fail("share_surface missing — shared where? name the surface", details)
    reasons.append(f"shared with the team on {surface}")
    details["share_surface"] = surface

    reasons.append("SN-0732 honored: right thing, intelligent thing, value — compounded")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0732 Naya identity check")
    parser.add_argument("--record", required=True,
                        help="JSON lesson record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0732"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
