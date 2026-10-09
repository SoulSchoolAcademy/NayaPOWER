#!/usr/bin/env python3
"""Delegated Merge Authority (Shawn, 2026-10-08 — ratified delegation).

"Naya 5 may merge to main WITHOUT Shawn's per-merge approval iff ALL hold:
(1) built + tests green; (2) honest evidence-backed self-scorecard >= 9.0
with value-calculus run ('most intelligent thing wins'); (3) independent
validation by a DIFFERENT seat; (4) intent + scorecard + validation posted
on #1354, team consensus (no seat objects); (5) merge, then report after:
what, why, scorecard, who validated.

Below 9.0, no independent validation, or any team objection → still needs
Shawn's word. Other protected gates (production deploys, credentials/money,
destructive actions, security/privacy/consent/authority changes) are
UNCHANGED — this delegation covers merges to main ONLY."

This check verifies a merge-to-main packet carries every condition of the
delegation. Every field the delegation's hard line depends on is REQUIRED:
absence fails closed, never defaults to permitted. The check never grants
authority — it verifies the packet that claims it.

Input record:
    {
      "target": "main",              # the ref being merged into
      "branch": "<branch name>",
      "seat": "<merging seat>",
      "tests_green": true,
      "test_evidence": "<CI run / command output ref — the proof>",
      "self_scorecard": {
        "score": 9.2,
        "evidence_backed": true,
        "value_calculus_run": true
      },
      "independent_validator": "<different seat id>",
      "posted_to_1354": true,
      "team_objections": 0,
      "post_merge_report_planned": true
    }

Checks:
  1. Scope: target != "main" → PASS (not applicable; the delegation covers
     merges to main only). This is the law's own scope, not a loophole.
  2. tests_green is True AND test_evidence non-empty — "built + tests
     green" needs the proof, not the claim.
  3. self_scorecard: score >= 9.0, evidence_backed true, value_calculus_run
     true — honest, evidence-backed, and the math was run.
  4. independent_validator named and != seat — validation by a DIFFERENT
     seat; self-validation is not validation.
  5. posted_to_1354 true AND team_objections == 0 — intent + scorecard +
     validation posted, team consensus, no seat objects.
  6. post_merge_report_planned true — merge, THEN report after.

Usage:
    python3 tools/protocol/checks/merge_authority.py \
        --record '{"target": "main", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

MIN_SELF_SCORE = 9.0


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "DELEGATED-MERGE-AUTHORITY", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    target = _nonempty_str(record.get("target"))
    branch = _nonempty_str(record.get("branch"))
    seat = _nonempty_str(record.get("seat"))
    tests_green = record.get("tests_green")
    test_evidence = _nonempty_str(record.get("test_evidence"))
    scorecard = record.get("self_scorecard")
    independent_validator = _nonempty_str(record.get("independent_validator"))
    posted_to_1354 = record.get("posted_to_1354")
    team_objections = record.get("team_objections")
    report_planned = record.get("post_merge_report_planned")

    # 1. Scope: the delegation covers merges to main ONLY.
    if not target:
        return fail(
            "target missing — the delegation's scope is merges to main; "
            "an unnamed target fails closed",
            details,
        )
    if target != "main":
        reasons.append(f"target is {target!r}, not main — delegation not "
                       "applicable (it covers merges to main only); PASS "
                       "by scope, not by permission")
        details["target"] = target
        return result(True, reasons, details)
    details["target"] = "main"

    if not branch:
        return fail("branch missing — the merge packet must name the branch", details)
    if not seat:
        return fail(
            f"{branch}: seat unnamed — delegated authority is granted to a "
            "named seat, not to an anonymous merge",
            details,
        )
    details["branch"] = branch
    details["seat"] = seat

    # 2. Built + tests green — with the proof, not the claim.
    if tests_green is not True:
        return fail(
            f"{branch}: tests_green is not true — condition (1) 'built + "
            "tests green' is not met; below the bar, the merge still needs "
            "Shawn's word",
            details,
        )
    if not test_evidence:
        return fail(
            f"{branch}: test_evidence missing — 'tests green' without a CI "
            "run or command-output reference is a claim, not proof",
            details,
        )
    reasons.append(f"built + tests green ({test_evidence})")

    # 3. Honest evidence-backed self-scorecard >= 9.0, value calculus run.
    if not isinstance(scorecard, dict):
        return fail(
            f"{branch}: self_scorecard missing — condition (2) requires an "
            "honest evidence-backed self-scorecard >= 9.0 with the value "
            "calculus run. Absence fails closed.",
            details,
        )
    score = scorecard.get("score")
    evidence_backed = scorecard.get("evidence_backed")
    vc_run = scorecard.get("value_calculus_run")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        return fail(
            f"{branch}: self_scorecard.score is not a number — the 9.0 bar "
            "cannot be evaluated on a non-number",
            details,
        )
    if score < MIN_SELF_SCORE:
        return fail(
            f"{branch}: self_scorecard.score {score} < {MIN_SELF_SCORE} — "
            "below 9.0 the merge still needs Shawn's word",
            details,
        )
    if evidence_backed is not True:
        return fail(
            f"{branch}: self_scorecard.evidence_backed is not true — 'honest "
            "EVIDENCE-BACKED self-scorecard'; scores move only on evidence, "
            "never optimism",
            details,
        )
    if vc_run is not True:
        return fail(
            f"{branch}: self_scorecard.value_calculus_run is not true — the "
            "delegation requires the value calculus run ('most intelligent "
            "thing wins')",
            details,
        )
    reasons.append(f"self-scorecard {score} >= 9.0, evidence-backed, value "
                   "calculus run")
    details["self_score"] = score

    # 4. Independent validation by a DIFFERENT seat.
    if not independent_validator:
        return fail(
            f"{branch}: independent_validator unnamed — condition (3) "
            "'independent validation by a different seat'; without it, the "
            "merge still needs Shawn's word",
            details,
        )
    if independent_validator.lower() == seat.lower():
        return fail(
            f"{branch}: independent_validator == seat ({seat}) — "
            "self-validation is not independent validation; 10/10 is never "
            "self-declared",
            details,
        )
    reasons.append(f"independently validated by {independent_validator}")
    details["independent_validator"] = independent_validator

    # 5. Posted on #1354, team consensus, no objections.
    if posted_to_1354 is not True:
        return fail(
            f"{branch}: posted_to_1354 is not true — condition (4) 'intent + "
            "scorecard + validation posted on #1354'; unposted intent is "
            "not team consensus",
            details,
        )
    if not isinstance(team_objections, int) or isinstance(team_objections, bool):
        return fail(
            f"{branch}: team_objections is not an integer count — 'no seat "
            "objects' must be an explicit zero, not an absent field",
            details,
        )
    if team_objections != 0:
        return fail(
            f"{branch}: team_objections = {team_objections} — a seat "
            "objects; the delegation requires team consensus, so this merge "
            "still needs Shawn's word",
            details,
        )
    reasons.append("intent + scorecard + validation posted on #1354; no "
                   "team objections")

    # 6. Report after.
    if report_planned is not True:
        return fail(
            f"{branch}: post_merge_report_planned is not true — condition "
            "(5) 'merge, then report after: what, why, scorecard, who "
            "validated'",
            details,
        )
    reasons.append("post-merge report planned (what, why, scorecard, who "
                   "validated)")

    reasons.append(f"{branch}: all 5 delegation conditions met — merge to "
                   "main authorized under the delegation")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Delegated Merge Authority check")
    parser.add_argument("--record", required=True,
                        help="JSON merge packet (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "DELEGATED-MERGE-AUTHORITY"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
