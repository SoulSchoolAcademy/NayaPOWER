#!/usr/bin/env python3
"""predicate≠perimeter — a checker is not enforcement until wired at the delivery boundary.

From the activation-gate arc (#1354, 2026-10-09): a pure predicate with
real false-acceptance paths — unbound repository identity, abbreviated
SHAs accepted, caller-supplied live tip, self-asserted receipt fields —
still "passed" its local fixtures. Local fixture passes therefore do NOT
establish activation authenticity or actual CI enforcement. The predicate
is the perimeter's blueprint, not the perimeter.

This is the claim-side companion to SN-0733 (delivery_boundary.py, the
mechanism-side law). This check governs the STATUS LABEL a seat puts on
its work: a checker whose predicate passes but which is not wired at a
delivery boundary may be called "predicate_only" / "candidate" — never
"enforced".

Validates a checker-claim record. The hard line: predicate_result ==
"pass" plus delivery_wired == false plus claimed == "enforced" fails —
that is the exact false-acceptance the law exists to kill.

Input record:
    {
      "checker": "tools/activation_gate.py::check",
      "predicate_result": "pass" | "fail",
      "claimed": "enforced" | "predicate_only" | "candidate",
      "delivery_wired": false,
      "wiring_evidence": "<workflow run/job id on the delivery path>"
    }

Checks:
  1. claimed == "enforced" requires delivery_wired == true AND
     wiring_evidence non-empty (a real observed run, not a local fixture).
  2. predicate_result == "pass" with delivery_wired false must be claimed
     "predicate_only" or "candidate" — claiming "enforced" fails.
  3. predicate_result == "fail" may never be claimed "enforced".

Usage:
    python3 tools/protocol/checks/predicate_vs_perimeter.py \
        --record '{"checker": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

HONEST_UNWIRED_CLAIMS = {"predicate_only", "candidate"}


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "PREDICATE-PERIMETER", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    checker = str(record.get("checker") or "(unnamed)").strip()
    predicate_result = str(record.get("predicate_result") or "").strip().lower()
    claimed = str(record.get("claimed") or "").strip().lower()
    wired = record.get("delivery_wired", False)
    evidence = str(record.get("wiring_evidence") or "").strip()

    details.update({"checker": checker, "claimed": claimed,
                    "predicate_result": predicate_result})

    if predicate_result not in {"pass", "fail"}:
        return fail(
            f"{checker}: predicate_result {predicate_result!r} — the predicate "
            "must declare 'pass' or 'fail'; an undeclared predicate proves nothing",
            details,
        )
    reasons.append(f"predicate declared '{predicate_result}'")

    if claimed not in {"enforced", *HONEST_UNWIRED_CLAIMS}:
        return fail(
            f"{checker}: claimed {claimed!r} — honest claims are 'enforced', "
            "'predicate_only', or 'candidate'",
            details,
        )

    if claimed == "enforced":
        if predicate_result != "pass":
            return fail(
                f"{checker}: claimed 'enforced' while the predicate FAILS — "
                "a failing predicate enforces nothing",
                details,
            )
        if wired is not True:
            return fail(
                f"{checker}: claimed 'enforced' with delivery_wired false — "
                "predicate≠perimeter: local fixture passes do not establish "
                "actual enforcement. Wire it at the delivery boundary first.",
                details,
            )
        if not evidence:
            return fail(
                f"{checker}: claimed 'enforced' without wiring_evidence — "
                "name the observed delivery-path run (workflow/run/job id) "
                "or retract the claim",
                details,
            )
        reasons.append("predicate passes AND wired at the delivery boundary")
        reasons.append(f"wiring observed: {evidence}")
        details["wiring_evidence"] = evidence
        reasons.append(f"{checker}: honestly ENFORCED")
        return result(True, reasons, details)

    # claimed predicate_only / candidate — the honest unwired states.
    if predicate_result == "pass" and wired is not True:
        reasons.append(
            "predicate passes but unwired — claimed honestly as "
            f"'{claimed}'; the perimeter is still open and this record says so"
        )
    elif predicate_result == "pass":
        reasons.append("predicate passes; not claiming enforcement")
    else:
        reasons.append("predicate fails; correctly not claiming enforcement")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="predicate!=perimeter check")
    parser.add_argument("--record", required=True,
                        help="JSON checker-claim record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "PREDICATE-PERIMETER"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
