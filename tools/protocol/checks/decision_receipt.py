#!/usr/bin/env python3
"""The Decision Receipt Law (Shawn, 2026-10-09).

"A decision without homework is guessing, not autonomy. Be fully aware of
the decision: you know it's right because you did the math."

Report format: "I chose X. I looked at A, B, C. X won because [evidence].
This is what I did." The scorecard is the receipt; correctness is the job.
Decisive on clear winners, honest on close calls. If the winner isn't
clear or evidence is missing, say so plainly instead of bluffing.

This is the REPORT half of decision governance. decision_log.py holds the
math half (options, scores, winner == argmax, authority gates). This
module holds the receipt half: the record must carry the alternatives that
were looked at, the evidence that made the winner win, and the
plain-words receipt naming both. A decision with no named alternatives
and no winning evidence is guessing, not a decision.

Input record:
    {
      "decision": "<what was decided>",
      "chosen": "b",
      "alternatives": [
        {"id": "a", "description": "..."},
        {"id": "b", "description": "..."},
        {"id": "c", "description": "..."}
      ],
      "winning_evidence": "<the evidence that made the winner win>",
      "receipt": "I chose b. I looked at a, b, c. b won because <evidence>.",
      "seat": "<deciding seat>",
      "close_call": false,
      "uncertainty_declared": false   # required true when close_call is true
    }

Checks:
  1. decision and seat present and non-empty (anonymous decisions are void).
  2. alternatives is a list of >= 2, each with a non-empty id and description.
     One option is not a decision; a decision without homework is guessing.
  3. chosen is non-empty and is one of the alternatives' ids.
  4. winning_evidence is non-empty — "X won because [evidence]". Missing
     evidence is not a receipt; say so plainly instead of bluffing.
  5. receipt is non-empty and names the chosen id and every alternative id
     (the receipt must say what was chosen AND what was looked at).
  6. If close_call is true, uncertainty_declared must be true —
     "honest on close calls".

Usage:
    python3 tools/protocol/checks/decision_receipt.py \
        --record '{"decision": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402


def _names_id(text_lower: str, ident: str) -> bool:
    """True if ident appears in text_lower as a bounded token, not as a
    substring of a larger word. Substring matching lets 'c' pass inside
    'considered' and 'd' pass inside 'evidence' — that is the same
    absence-as-exploit class the fail-closed-shape law exists to kill."""
    return re.search(
        r"(?<![a-z0-9_])" + re.escape(ident) + r"(?![a-z0-9_])", text_lower
    ) is not None


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "DECISION-RECEIPT-LAW", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    decision = _nonempty_str(record.get("decision"))
    seat = _nonempty_str(record.get("seat"))
    chosen = _nonempty_str(record.get("chosen"))
    alternatives = record.get("alternatives")
    winning_evidence = _nonempty_str(record.get("winning_evidence"))
    receipt = _nonempty_str(record.get("receipt"))
    close_call = record.get("close_call", False)
    uncertainty_declared = record.get("uncertainty_declared", False)

    # 1. The decision and the decider must be named.
    if not decision:
        return fail(
            "decision missing or empty — a receipt for an unnamed decision "
            "is not a receipt",
            details,
        )
    if not seat:
        return fail(
            f"{decision}: seat unnamed — anonymous decisions are void; "
            "autonomy without a named decider is guessing with no owner",
            details,
        )
    details["decision"] = decision
    details["seat"] = seat

    # 2. Homework is mandatory: >= 2 alternatives, each identified.
    if not isinstance(alternatives, list):
        return fail(
            f"{decision}: alternatives is not a list — the law requires "
            "naming what was looked at (A, B, C); absence is the cheapest "
            "exploit, so a missing alternatives field fails closed",
            details,
        )
    if len(alternatives) < 2:
        return fail(
            f"{decision}: only {len(alternatives)} alternative(s) considered — "
            "one option is not a decision; a decision without homework is "
            "guessing, not autonomy",
            details,
        )
    alt_ids: list[str] = []
    for i, alt in enumerate(alternatives):
        if not isinstance(alt, dict):
            return fail(
                f"{decision}: alternative #{i} is not an object — every "
                "alternative must carry an id and a description",
                details,
            )
        alt_id = _nonempty_str(alt.get("id"))
        alt_desc = _nonempty_str(alt.get("description"))
        if not alt_id:
            return fail(
                f"{decision}: alternative #{i} has no id — an unnamed "
                "alternative was not really considered",
                details,
            )
        if not alt_desc:
            return fail(
                f"{decision}: alternative {alt_id!r} has no description — "
                "a listed-but-undescribed option is homework theater",
                details,
            )
        alt_ids.append(alt_id)
    reasons.append(f"homework done: looked at {', '.join(alt_ids)}")

    # 3. The choice must be one of the things that was looked at.
    if not chosen:
        return fail(
            f"{decision}: chosen missing — the receipt must say what was "
            "chosen (I chose X)",
            details,
        )
    if chosen not in alt_ids:
        return fail(
            f"{decision}: chosen {chosen!r} is not among the alternatives "
            f"considered ({', '.join(alt_ids)}) — choosing what you never "
            "looked at is guessing, not a decision",
            details,
        )
    reasons.append(f"chose {chosen}")

    # 4. X won because [evidence] — the scorecard is the receipt.
    if not winning_evidence:
        return fail(
            f"{decision}: winning_evidence missing — 'X won because "
            "[evidence]' is the law's load-bearing sentence. If the evidence "
            "is missing, say so plainly instead of bluffing.",
            details,
        )
    reasons.append("winning evidence cited")
    details["winning_evidence"] = winning_evidence

    # 5. The plain-words receipt names the choice AND the field.
    if not receipt:
        return fail(
            f"{decision}: receipt missing — the law's report format is "
            "'I chose X. I looked at A, B, C. X won because [evidence]. "
            "This is what I did.' A decision record without the receipt "
            "sentence is homework with no report.",
            details,
        )
    receipt_lower = receipt.lower()
    if not _names_id(receipt_lower, chosen.lower()):
        return fail(
            f"{decision}: receipt does not name the chosen option "
            f"{chosen!r} — 'I chose X' must say X",
            details,
        )
    missing_alts = [a for a in alt_ids if not _names_id(receipt_lower, a.lower())]
    if missing_alts:
        return fail(
            f"{decision}: receipt does not name every alternative looked at "
            f"(missing: {', '.join(missing_alts)}) — 'I looked at A, B, C' "
            "must name the field, not gesture at it",
            details,
        )
    reasons.append("receipt names the choice and the full field")

    # 6. Honest on close calls.
    if close_call is True and uncertainty_declared is not True:
        return fail(
            f"{decision}: close_call is true but uncertainty_declared is not "
            "— 'honest on close calls. If the winner isn't clear or evidence "
            "is missing, say so plainly instead of bluffing.'",
            details,
        )
    if close_call is True:
        reasons.append("close call declared honestly")

    reasons.append(f"{decision}: decision receipt complete — chosen, field, "
                   "evidence, report")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Decision Receipt Law check")
    parser.add_argument("--record", required=True,
                        help="JSON decision-receipt record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "DECISION-RECEIPT-LAW"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
