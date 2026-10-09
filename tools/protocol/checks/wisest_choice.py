#!/usr/bin/env python3
"""The Wisest Choice Law (Shawn, 2026-10-09 — his standing command).

"Wish not to be the smartest but the wisest — always make the wisest,
most intelligent choice every single time."

The protocol: understand the goal/mission/objective → analyze the
options against it → measure → decide by knowing, not guessing.
The protocol, rubrics, and maps ARE the authority — act on what they
grant, stop asking for permission they already confer.
Questions only for genuine protected gates or true ambiguity the protocol
cannot resolve. Everything else: act, then show receipts.

This is the JUDGMENT contract half of decision governance. decision_log.py
checks the math; decision_receipt.py checks the report. This module
checks the thinking: a decision record must name the objective it
optimizes, cite the protocol/rubric/measurement its basis comes from
(never vibes), and — if it asked a human a question — name the
protected gate or the genuine ambiguity that made the question
necessary. "Never ask A, B, or C?" is a hard line, not a suggestion.

Input record:
    {
      "decision": "<what was decided>",
      "objective": "<the goal/mission/objective this optimizes>",
      "options_analyzed": ["a", "b", "c"],
      "basis": {
        "type": "protocol" | "rubric" | "scorecard" | "measurement" | "law",
        "ref": "<named: e.g. 'value-calculus V2.1', 'SN-0523 scorecard', 'DECISION-RECEIPT-LAW'>"
      },
      "question_asked": false,
      // required when question_asked is true (either one):
      "protected_gate": "<named protected gate>",
      "genuine_ambiguity": "<the true ambiguity the protocol cannot resolve>",
      "close_call": false,
      "uncertainty_declared": false   # required true when close_call is true
    }

Checks:
  1. decision and objective present and non-empty — understand the goal
     FIRST; an objective-less decision cannot be the wisest choice.
  2. options_analyzed is a list of >= 2 — analyze the options against the
     objective; the protocol never picks from one.
  3. basis present with type in the admitted set and a non-empty ref —
     decide by KNOWING, not guessing; the protocol/rubrics/maps are the
     authority, and the authority must be named. type "opinion", "vibes",
     or a missing ref fails: that is guessing with formatting.
  4. If question_asked is true, protected_gate or genuine_ambiguity must
     be non-empty — questions only for genuine protected gates or true
     ambiguity; "A, B, or C?" without naming the gate is a violation.
  5. If close_call is true, uncertainty_declared must be true —
     decisive on clear winners, honest on close calls.

Usage:
    python3 tools/protocol/checks/wisest_choice.py \
        --record '{"decision": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

ADMITTED_BASIS_TYPES = {"protocol", "rubric", "scorecard", "measurement", "law"}


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "WISEST-CHOICE-LAW", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    decision = _nonempty_str(record.get("decision"))
    objective = _nonempty_str(record.get("objective"))
    options_analyzed = record.get("options_analyzed")
    basis = record.get("basis")
    question_asked = record.get("question_asked", False)
    protected_gate = _nonempty_str(record.get("protected_gate"))
    genuine_ambiguity = _nonempty_str(record.get("genuine_ambiguity"))
    close_call = record.get("close_call", False)
    uncertainty_declared = record.get("uncertainty_declared", False)

    # 1. Name the goal first. Understanding the objective IS the job.
    if not decision:
        return fail("decision missing or empty", details)
    if not objective:
        return fail(
            f"{decision}: objective missing — 'understand the "
            "goal/mission/objective' is the law's first step. An "
            "objective-less decision is guessing, and guessing is never "
            "the wisest choice.",
            details,
        )
    details["decision"] = decision
    details["objective"] = objective
    reasons.append(f"objective named: {objective}")

    # 2. Analyze the options against the objective.
    if not isinstance(options_analyzed, list):
        return fail(
            f"{decision}: options_analyzed is not a list — 'analyze the "
            "options against it' requires the options to exist. Absence "
            "fails closed.",
            details,
        )
    if len(options_analyzed) < 2:
        return fail(
            f"{decision}: only {len(options_analyzed)} option(s) analyzed — "
            "the wisest choice among one option is a ceremony, not a "
            "decision",
            details,
        )
    if any(not _nonempty_str(o) for o in options_analyzed):
        return fail(
            f"{decision}: options_analyzed contains a blank option — "
            "unnamed options were not analyzed",
            details,
        )
    reasons.append(f"options analyzed against objective: "
                   f"{', '.join(str(o) for o in options_analyzed)}")

    # 3. Decide by knowing, not guessing. Name the authority.
    if not isinstance(basis, dict):
        return fail(
            f"{decision}: basis is not an object — 'decide by knowing, not "
            "guessing' requires naming the protocol/rubric/scorecard/"
            "measurement/law the decision rests on. A missing basis fails "
            "closed.",
            details,
        )
    basis_type = _nonempty_str(basis.get("type")).lower()
    basis_ref = _nonempty_str(basis.get("ref"))
    if basis_type not in ADMITTED_BASIS_TYPES:
        return fail(
            f"{decision}: basis.type {basis_type!r} is not admitted "
            f"(admitted: {', '.join(sorted(ADMITTED_BASIS_TYPES))}) — "
            "opinion, instinct, and vibes are not authority. The protocol, "
            "rubrics, and maps ARE the authority; name them.",
            details,
        )
    if not basis_ref:
        return fail(
            f"{decision}: basis.ref missing — a basis type with no named "
            "source is authority theater. Name the protocol, the rubric, "
            "the scorecard, the measurement, or the law.",
            details,
        )
    reasons.append(f"basis: {basis_type} — {basis_ref}")
    details["basis"] = {"type": basis_type, "ref": basis_ref}

    # 4. Questions only for genuine protected gates or true ambiguity.
    if question_asked is True:
        if not protected_gate and not genuine_ambiguity:
            return fail(
                f"{decision}: question_asked is true but neither "
                "protected_gate nor genuine_ambiguity is named — 'never ask "
                "A, B, or C?'. Questions are only for genuine protected "
                "gates or true ambiguity the protocol cannot resolve. "
                "Everything else: act, then show receipts.",
                details,
            )
        reasons.append(
            "question justified: "
            + (f"protected gate {protected_gate}" if protected_gate
               else f"genuine ambiguity: {genuine_ambiguity}")
        )

    # 5. Honest on close calls.
    if close_call is True and uncertainty_declared is not True:
        return fail(
            f"{decision}: close_call is true but uncertainty_declared is "
            "not — 'decisive on clear winners, honest on close calls.' "
            "If the winner isn't clear, say so plainly instead of bluffing.",
            details,
        )
    if close_call is True:
        reasons.append("close call declared honestly")

    reasons.append(f"{decision}: wisest-choice contract met — objective "
                   "named, options analyzed, basis cited, no unjustified "
                   "questions")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Wisest Choice Law check")
    parser.add_argument("--record", required=True,
                        help="JSON wisest-choice record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "WISEST-CHOICE-LAW"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
