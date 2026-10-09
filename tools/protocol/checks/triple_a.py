#!/usr/bin/env python3
"""Triple-A Excellence — Awesome 24/7 (Shawn, 2026-10-09).

"Being awesome 24/7 is the job. Not a goal, not a stretch target — the
job. Producing awesomeness all the time, every day. If output is not
awesome, that is a seriously serious problem needing immediate attention."

"Demonstrated, not promised."

Validates a deliverable record against the excellence contract. The hard
lines: a DONE claim without existing evidence is a promise, not a
demonstration; a score by the builder is not independent verification —
10/10 is never self-declared.

Input record:
    {
      "deliverable": "<name/description>",
      "claimed": "done" | "awesome",
      "demonstrated": true,
      "evidence_ref": "<smart link / artifact id — the proof>",
      "evidence_verified_exists": true,
      "builder": "<seat that built it>",
      "scorer": "<independent seat or human who scored it>"
    }

Checks:
  1. claimed done/awesome requires demonstrated == true.
  2. evidence_ref present AND evidence_verified_exists true
     (smart-link discipline: verify the artifact exists before linking).
  3. scorer present, named, and != builder
     (independent verification; a 10/10 is never self-declared).

This complements the SN-0526 quality gate (score >= 9.0): Triple-A is
the demonstrated-not-promised + independently-verified half.

Usage:
    python3 tools/protocol/checks/triple_a.py \
        --record '{"deliverable": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "TRIPLE-A-EXCELLENCE", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    deliverable = str(record.get("deliverable") or "(unnamed)").strip()
    claimed = str(record.get("claimed") or "").strip().lower()
    demonstrated = record.get("demonstrated", False)
    evidence_ref = str(record.get("evidence_ref") or "").strip()
    evidence_exists = record.get("evidence_verified_exists", False)
    builder = str(record.get("builder") or "").strip().lower()
    scorer = str(record.get("scorer") or "").strip().lower()

    details["deliverable"] = deliverable

    if claimed not in {"done", "awesome"}:
        return fail(
            f"{deliverable}: claimed {claimed!r} — Triple-A only admits "
            "'done' or 'awesome'; anything else is not a deliverable state",
            details,
        )
    reasons.append(f"claimed '{claimed}'")

    if demonstrated is not True:
        return fail(
            f"{deliverable}: demonstrated is not true — a DONE claim without "
            "demonstration is a promise, not proof. Demonstrated, not promised.",
            details,
        )
    reasons.append("demonstrated, not promised")

    if not evidence_ref:
        return fail(
            f"{deliverable}: evidence_ref missing — no smart link, no proof shipped",
            details,
        )
    if evidence_exists is not True:
        return fail(
            f"{deliverable}: evidence_ref {evidence_ref!r} not verified to exist — "
            "smart-link discipline: verify the artifact exists before linking, "
            "never manufacture a link",
            details,
        )
    reasons.append(f"evidence exists and verified: {evidence_ref}")
    details["evidence_ref"] = evidence_ref

    if not scorer:
        return fail(
            f"{deliverable}: scorer unnamed — anonymous scores are not scores",
            details,
        )
    if builder and scorer == builder:
        return fail(
            f"{deliverable}: scorer == builder ({builder}) — independent "
            "verification required; 10/10 is never self-declared",
            details,
        )
    reasons.append(f"independently scored by {scorer}")
    details["scorer"] = scorer

    reasons.append(f"{deliverable}: Triple-A contract met — demonstrated, evidenced, independent")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Triple-A Excellence check")
    parser.add_argument("--record", required=True,
                        help="JSON deliverable record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "TRIPLE-A-EXCELLENCE"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
