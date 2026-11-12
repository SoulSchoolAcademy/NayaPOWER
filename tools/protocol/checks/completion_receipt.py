#!/usr/bin/env python3
"""The Completion Receipt (PROTOCOL.md, Final Acceptance).

PROTOCOL.md (ratified 2026-10-20), FINAL ACCEPTANCE — before any
substantive task is called complete:

    "The Value Verdict, first, before every other question: did a human
    get value from this? Name who benefits and how. If what was produced
    is not useful, it has no value — and the cycle failed, no matter how
    clean the process was or how high the intermediate scores read."

Then: What was required? What actually changed? What evidence proves
the result? What remains unknown, blocked, or unverified? Was it
recorded and handed off correctly? What was learned? What is the single
highest-value next action? If required proof is missing, the task is
not complete.

This module is that acceptance in machine form. The VALUE VERDICT is
checked FIRST, after basic shape — before claim polish, before
evidence, before the scorecard loop, before the next action. A receipt
with perfect process and no named human value fails here, on the
verdict, because Final Acceptance says the verdict comes before every
other question: no named human value = no completion, no matter how
clean the process was.

The scorecard half of the receipt is not re-implemented here. It is
validated by the sibling scorecard_loop.py — Step 15's loop in its
completion-receipt form — and a failing loop fails this receipt, with
the loop's reasons carried through prefixed "scorecard loop: ". One
quality loop, never two: this module owns the verdict, the evidence,
and the handoff; the sibling owns the loop arithmetic. (The other
sibling, builder_scorer_loop.py, owns the merge-packet form; a
completion receipt is not a merge packet.)

Input record:
    {
      "claim": "<what is claimed complete>",
      "seat": "<completing seat>",
      "value_verdict": {
        "beneficiary": "<the named human who got value>",
        "how": "<how they benefit — the value, in plain words>"
      },
      "evidence": "<proof the result is real>" | ["<proof>", ...],
      "scorecard_loop": {
        "objective": "<named ultimate objective scored against>",
        "weight": "full" | "compressed",
        "compression_reason": "<required when compressed>",
        "rounds": [ ...scorecard_loop rounds... ],
        "final_score": 9.5,
        "failure_note_ref": "<optional; see scorecard_loop>"
        # "claim" / "seat" may also ride here; when absent, this
        # receipt's own claim / seat are supplied to the loop check,
        # because a nested loop record names its fields, not its
        # envelope twice.
      },
      "next_action": "<the single highest-value next action>"
    }

Checks:
  1. Basic shape: the record is a JSON object.
  2. THE VALUE VERDICT, FIRST: value_verdict is present and is an
     object, its beneficiary is a non-empty string, and its how is a
     non-empty string. Any failure here fails the receipt with a
     reason naming VALUE VERDICT — before any other check runs.
  3. claim and seat are present and non-empty — an anonymous or
     unnamed completion is not a receipt.
  4. evidence is non-empty: a non-empty string, or a non-empty list of
     non-empty strings. "If required proof is missing, the task is not
     complete" — a completion with no evidence is a claim, not a proof.
  5. next_action is present and non-empty — Final Acceptance ends with
     the single highest-value next action; a receipt with no next
     action strands the next Naya.
  6. scorecard_loop is present, is an object, and passes the sibling
     scorecard_loop check (with this receipt's claim / seat supplied
     when the nested record omits them). A failing loop fails the
     receipt, the loop's reasons prefixed "scorecard loop: ". When the
     loop passes on its honest-failure path (below 9, failure filed as
     the note), this receipt passes the loop step but records
     details["loop_shipped"] = false — the receipt is honest, and what
     it receipts is explicitly work that did not ship.

Honest bounds: this check verifies that a verdict was NAMED (a
beneficiary and a how), that evidence was CITED, and that the loop
receipt is well-formed. It cannot judge whether the named value is
real, whether the cited evidence proves what it claims, or whether the
next action really is the highest-value one. That judgment is Step 11's
independent verification by a different mind — this receipt makes the
claim verifiable; it never verifies itself.

Usage:
    python3 tools/protocol/checks/completion_receipt.py \
        --record '{"claim": "...", "seat": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

try:  # sibling import: package form first, bare-module form as fallback
    from checks.scorecard_loop import check as _loop_check  # noqa: E402
except ImportError:  # pragma: no cover - depends on invocation layout
    from scorecard_loop import check as _loop_check  # noqa: E402


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {
        "law": "COMPLETION-RECEIPT / FINAL-ACCEPTANCE",
        "law_status": "RATIFIED (PROTOCOL.md Final Acceptance, 2026-10-20)",
    }

    # 1. Basic shape only. Everything substantive waits for the verdict.
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    # 2. THE VALUE VERDICT — FIRST, before every other question.
    value_verdict = record.get("value_verdict")
    if not isinstance(value_verdict, dict):
        return fail(
            "VALUE VERDICT missing or not an object — Final Acceptance "
            "opens with the Value Verdict, before every other question: "
            "did a human get value? Name who benefits and how. No named "
            "human value = no completion, no matter how clean the "
            "process was",
            details,
        )
    beneficiary = _nonempty_str(value_verdict.get("beneficiary"))
    how = _nonempty_str(value_verdict.get("how"))
    if not beneficiary:
        return fail(
            "VALUE VERDICT: beneficiary missing or empty — the verdict "
            "must name who benefits; value to no one in particular is "
            "value to no one",
            details,
        )
    if not how:
        return fail(
            "VALUE VERDICT: how missing or empty — the verdict must say "
            "how the named human benefits; a beneficiary with no stated "
            "benefit is a name, not a verdict",
            details,
        )
    details["value_verdict"] = {"beneficiary": beneficiary, "how": how}
    reasons.append(
        f"VALUE VERDICT: {beneficiary} benefits — {how}"
    )

    # 3. The completion and its owner must be named.
    claim = _nonempty_str(record.get("claim"))
    seat = _nonempty_str(record.get("seat"))
    if not claim:
        return fail(
            "claim missing or empty — a completion receipt for an "
            "unnamed claim receipts nothing",
            details,
        )
    if not seat:
        return fail(
            f"{claim}: seat missing or empty — anonymous completions "
            "are void; a receipt needs its owner",
            details,
        )
    details["claim"] = claim
    details["seat"] = seat

    # 4. Evidence: missing proof means not complete.
    evidence = record.get("evidence")
    if isinstance(evidence, str):
        if not evidence.strip():
            return fail(
                f"{claim}: evidence is empty — Final Acceptance: if "
                "required proof is missing, the task is not complete",
                details,
            )
        evidence_items = [evidence.strip()]
    elif isinstance(evidence, list):
        if not evidence:
            return fail(
                f"{claim}: evidence list is empty — Final Acceptance: "
                "if required proof is missing, the task is not complete",
                details,
            )
        evidence_items = []
        for i, item in enumerate(evidence):
            if not _nonempty_str(item):
                return fail(
                    f"{claim}: evidence entry #{i} is blank or not a "
                    "string — cited proof must say what it is",
                    details,
                )
            evidence_items.append(_nonempty_str(item))
    else:
        return fail(
            f"{claim}: evidence missing or not a string / list of "
            "strings — a completion receipt must cite its proof",
            details,
        )
    details["evidence"] = evidence_items
    reasons.append(f"evidence cited: {len(evidence_items)} item(s)")

    # 5. The single highest-value next action.
    next_action = _nonempty_str(record.get("next_action"))
    if not next_action:
        return fail(
            f"{claim}: next_action missing or empty — Final Acceptance "
            "ends with the single highest-value next action; a receipt "
            "with none strands the next Naya",
            details,
        )
    details["next_action"] = next_action
    reasons.append(f"next action named: {next_action}")

    # 6. The scorecard loop, validated by the sibling — never rebuilt.
    loop_record = record.get("scorecard_loop")
    if not isinstance(loop_record, dict):
        return fail(
            f"{claim}: scorecard_loop missing or not an object — a "
            "completion claim must carry its Step 15 loop receipt "
            "(objective, rounds, final_score)",
            details,
        )
    # A nested loop names its own fields; supply the envelope's
    # claim / seat when the nested record omits them.
    loop_input = dict(loop_record)
    loop_input.setdefault("claim", claim)
    loop_input.setdefault("seat", seat)
    if not _nonempty_str(loop_input.get("claim")):
        loop_input["claim"] = claim
    if not _nonempty_str(loop_input.get("seat")):
        loop_input["seat"] = seat

    loop = _loop_check(loop_input)
    if not loop.get("pass"):
        loop_reasons = [
            f"scorecard loop: {r}" for r in loop.get("reasons", [])
        ] or ["scorecard loop: failed with no reasons recorded"]
        details["scorecard_loop"] = loop.get("details", {})
        return result(False, loop_reasons, details)
    loop_details = loop.get("details", {})
    details["scorecard_loop"] = loop_details
    if "final_score" in loop_details:
        details["loop_final_score"] = loop_details["final_score"]
    if "shipped" in loop_details:
        details["loop_shipped"] = loop_details["shipped"]
    reasons.append("scorecard loop passed (validated by scorecard_loop)")
    if loop_details.get("shipped") is False:
        reasons.append(
            "scorecard loop recorded the honest-failure path: below the "
            "9 bar, failure filed as the note — this receipt is honest "
            "and the work it receipts did NOT ship"
        )

    reasons.append(
        f"{claim}: completion receipt complete — value verdict first, "
        "evidence cited, loop on the record, next action named"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Completion Receipt check")
    parser.add_argument("--record", required=True,
                        help="JSON completion-receipt record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "COMPLETION-RECEIPT / FINAL-ACCEPTANCE"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
