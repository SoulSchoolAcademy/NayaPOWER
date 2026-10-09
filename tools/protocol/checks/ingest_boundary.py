#!/usr/bin/env python3
"""The ingest-boundary law — guarding the state-ingest boundary (ratified via #1354, 2026-10-09).

From the report-score independent validation: the three Phase-2 attacks
were closed, but a fourth poison path lived in the same ingest boundary —
a fresh heuristic claim overwrote an AUTHORITATIVE score's VALUE while
keeping the "authoritative" LABEL. The "Never downgrade" logic guarded the
label; the score column was the payload.

The law, in three clauses:
  1. History never overwrites a current claim: a heuristic/history point
     must never write score/as_of/source over an authoritative state.
     Guard EVERY field the attacker controls, not just the label.
  2. Future-dated scores are rejected at ingest: a point dated beyond
     now + skew is refused, never immortalized.
  3. Pins keep real timestamps: a pinned point's as_of is never mutated
     by a later window.

Validates one ingest DECISION — what collect() did with one incoming
point against existing state. The hard line: ingest_action == "wrote"
under any clause violation fails.

Input record:
    {
      "existing": {"status": "authoritative" | "heuristic" | "history" | "seed",
                   "score": 9.0, "as_of": "<ISO-8601>", "pinned": false},
      "point":    {"status": "authoritative" | "heuristic" | "history",
                   "score": 2.0, "as_of": "<ISO-8601>", "source": "worker-log"},
      "ingest_action": "wrote" | "skipped" | "rejected",
      "now": "<ISO-8601 UTC — the ingest instant>",
      "future_skew_seconds": 300
    }

Checks:
  1. existing.status == "authoritative" and point.status != "authoritative"
     and ingest_action == "wrote" → FAIL (clause 1: heuristic/history
     never overwrites authoritative — the label-guard hole, closed).
  2. point.as_of > now + skew and ingest_action != "rejected" → FAIL
     (clause 2: future-dated refused at ingest).
  3. existing.pinned and point.status != "authoritative" and
     ingest_action == "wrote" → FAIL (clause 3: pins keep real timestamps).

Usage:
    python3 tools/protocol/checks/ingest_boundary.py \
        --record '{"existing": {...}, ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402


def _parse_ts(value) -> datetime | None:
    if not value:
        return None
    try:
        ts = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts
    except ValueError:
        return None


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "INGEST-BOUNDARY", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    existing = record.get("existing")
    point = record.get("point")
    action = str(record.get("ingest_action") or "").strip().lower()
    now = _parse_ts(record.get("now"))
    skew = record.get("future_skew_seconds", 300)

    if not isinstance(existing, dict) or not isinstance(point, dict):
        return fail("existing and point must both be objects", details)
    if action not in {"wrote", "skipped", "rejected"}:
        return fail(
            f"ingest_action {action!r} — the decision must be 'wrote', "
            "'skipped', or 'rejected'; silence about the decision is a hole",
            details,
        )
    if now is None:
        return fail("now missing or unparseable — ingest is a temporal act", details)
    try:
        skew = int(skew)
    except (TypeError, ValueError):
        return fail("future_skew_seconds must be an integer", details)

    existing_status = str(existing.get("status") or "").strip().lower()
    point_status = str(point.get("status") or "").strip().lower()
    pinned = existing.get("pinned", False)
    point_as_of = _parse_ts(point.get("as_of"))

    details.update({
        "existing_status": existing_status,
        "point_status": point_status,
        "ingest_action": action,
        "pinned": bool(pinned),
    })

    # Clause 3: pins keep real timestamps. Pins are immune entirely — a
    # pin's as_of is real history, never mutated by a later window. Checked
    # first because pin immunity is the sharpest reason when it applies.
    if pinned and point_status != "authoritative" and action == "wrote":
        return fail(
            "ingest wrote a non-authoritative point over PINNED state — pins "
            "are immune; a pin's as_of is real history and is never mutated "
            "by a later window. PINNED_AUTHORITATIVE skips heuristic points "
            "entirely.",
            details,
        )
    reasons.append("clause 3: pinned state untouched by lesser point")

    # Clause 1: history never overwrites a current authoritative claim.
    if existing_status == "authoritative" and point_status != "authoritative" \
            and action == "wrote":
        return fail(
            "ingest wrote a non-authoritative point over authoritative state — "
            "the label-guard hole: guarding the STATUS label while writing "
            "score/as_of/source lets a false number drive the report wearing "
            "the most-trusted badge. Heuristic/history never overwrites "
            "authoritative. The fix: skip, don't write.",
            details,
        )
    reasons.append("clause 1: authoritative state not overwritten by lesser point")

    # Clause 2: future-dated scores rejected at ingest.
    if point_as_of is not None and point_as_of > now + timedelta(seconds=skew):
        if action != "rejected":
            return fail(
                f"point dated {point.get('as_of')} beyond now+{skew}s skew was "
                f"{action!r}, not 'rejected' — future-dated scores are refused "
                "at ingest, never immortalized",
                details,
            )
        reasons.append("clause 2: future-dated point rejected at ingest")
    else:
        reasons.append("clause 2: point not future-dated")

    reasons.append(f"ingest decision '{action}' honors the boundary")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="ingest-boundary check")
    parser.add_argument("--record", required=True,
                        help="JSON ingest-decision record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "INGEST-BOUNDARY"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
