#!/usr/bin/env python3
"""Enforcement predicate for DELEGATED-MERGE-AUTHORITY-V1.

Shawn ratified (2026-10-08, #1354): Naya 5 may merge to main WITHOUT his
per-merge approval, if and only if ALL hold:

  1. built + tests green;
  2. honest self-scorecard >= 9.0, evidence-backed, value-calculus run
     ("most intelligent thing wins");
  3. independent validation — a different seat confirms the 9.0+ and that it
     is the most intelligent action;
  4. intent posted on #1354 with scorecard + validation; team consensus
     (no seat objects);
  5. merge, then report after: what, why, scorecard, who validated.

Below 9.0, no independent validation, or any team objection -> still needs
Shawn's word. The other protected gates (production deploys,
credentials/money, destructive actions, security/privacy/consent/authority
changes) are UNCHANGED — this delegation covers merges to main only, never
writes ON main.

Usage:
    python3 tools/merge_authority_receipt.py <merge_receipt.json> [--json]

Reads a merge-authority receipt (schema below), checks every condition
mechanically, and prints a verdict.

Exit code 0: ALLOW (all five conditions proven on the receipt).
Exit code 1: DENY (at least one condition unproven; reasons printed).
Exit code 2: usage / input error.

Fail-closed: any missing, malformed, or unresolvable field denies. UNKNOWN
!= PASS. A denied merge goes back to Shawn's word — this gate never invents
authority, it only verifies the delegation's own conditions.

The self-scorecard's five steps are validated by the same mechanical checker
as the full auto-merge law (tools/auto_merge_gate.py::_check_receipt), so
the two gates cannot drift: an inflated 9.0 on a theater receipt still
denies.

Receipt schema:
    {
      "decision_id": "<unique id>",
      "branch": "naya5/<item>",          # must NOT be "main"
      "base_sha": "<branch base commit>",
      "tip_sha_at_intent": "<live main tip when intent was posted>",  # must == base_sha (SN-0493)
      "author_seat": "naya-5",
      "self_scorecard": {
        "score": 9.2,                    # numeric, >= 9.0
        "comment_id": 6063575482,        # posted, not private
        "calculus_profile_id": "...",    # the value-calculus run that chose it
        "scorecard_receipt": { ... }     # the Scorecard Law's five steps
      },
      "tests": {
        "green": true,
        "suites": ["tests/test_merge_authority_receipt.py"],
        "evidence": "21/21 green @ <sha> (min 20 chars)"
      },
      "independent_validation": {
        "validator_seat": "naya-4",      # must differ from author_seat
        "validator_score": 9.1,          # numeric, >= 9.0
        "confirms_most_intelligent_action": true,
        "ref": "<comment id or feed ref where validation lives>"
      },
      "intent_post": {"issue": 1354, "comment_id": 6063000000},
      "consensus": {"window_closed_at": "<ISO-8601>", "objections": []},
      "merge_report": {"will_report_after": true}
    }

Stdlib only.
"""

import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

LAW_ID = "DELEGATED-MERGE-AUTHORITY-V1"
MIN_MERGE_SCORE = 9.0
INTENT_FEED_ISSUE = 1354
MIN_EVIDENCE_LEN = 20

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_check_receipt():
    """Import the canonical scorecard-receipt checker without side effects."""
    path = os.path.join(_TOOLS_DIR, "auto_merge_gate.py")
    spec = importlib.util.spec_from_file_location("auto_merge_gate_seam", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._check_receipt


def _parse_ts(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def _norm_seat(value):
    return str(value or "").strip().lower()


def _check_delegated_merge_receipt(receipt, check_receipt, reasons):
    """Check Shawn's five delegated-merge conditions. Fail-closed."""
    if not isinstance(receipt, dict):
        reasons.append("receipt: missing or not an object — no receipt, no merge")
        return

    get = receipt.get

    # ---- C0: structural bindings (branch target, tip currency — SN-0493)
    branch = get("branch")
    if not isinstance(branch, str) or not branch.strip():
        reasons.append("C0: branch missing — merges to main only from a named branch")
    elif branch.strip().lower() == "main":
        reasons.append("C0: branch is 'main' — delegated authority covers merges TO main, never writes ON main")
    base_sha = get("base_sha")
    tip_sha = get("tip_sha_at_intent")
    if not isinstance(base_sha, str) or not base_sha.strip():
        reasons.append("C0: base_sha missing — the merge decision must pin its tip")
    if not isinstance(tip_sha, str) or not tip_sha.strip():
        reasons.append("C0: tip_sha_at_intent missing — the intent must name the live tip it was decided on")
    if (isinstance(base_sha, str) and isinstance(tip_sha, str)
            and base_sha.strip() and tip_sha.strip()
            and base_sha.strip() != tip_sha.strip()):
        reasons.append("C0: base_sha != tip_sha_at_intent — decisions expire when the tip moves (SN-0493)")

    author_seat = _norm_seat(get("author_seat"))
    if not author_seat:
        reasons.append("C0: author_seat missing — anonymous merges are void")

    # ---- C1: built + tests green, with evidence
    tests = get("tests")
    if not isinstance(tests, dict):
        reasons.append("C1: tests block missing — unbuilt or untested work is not mergeable")
    else:
        if tests.get("green") is not True:
            reasons.append("C1: tests.green is not true — green CI is required")
        suites = tests.get("suites")
        if not isinstance(suites, list) or not suites:
            reasons.append("C1: tests.suites empty — name the green suites")
        evidence = tests.get("evidence")
        if not isinstance(evidence, str) or len(evidence.strip()) < MIN_EVIDENCE_LEN:
            reasons.append("C1: tests.evidence missing or too thin — green must be evidenced")

    # ---- C2: honest self-scorecard >= 9.0, posted, calculus-run, five steps
    sc = get("self_scorecard")
    if not isinstance(sc, dict):
        reasons.append("C2: self_scorecard missing — no scorecard, no merge")
    else:
        score = sc.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            reasons.append("C2: self_scorecard.score must be numeric 0-10")
        elif not (MIN_MERGE_SCORE <= score <= 10):
            reasons.append(f"C2: self_scorecard.score {score} < {MIN_MERGE_SCORE} — nothing under 9.0 ships")
        if not isinstance(sc.get("comment_id"), int):
            reasons.append("C2: self_scorecard.comment_id missing — a private scorecard is not authority")
        if not isinstance(sc.get("calculus_profile_id"), str) or not sc.get("calculus_profile_id").strip():
            reasons.append("C2: self_scorecard.calculus_profile_id missing — the math must be run and recorded")
        five_steps = sc.get("scorecard_receipt")
        sub_reasons = []
        # _check_receipt reports pass/fail via the reasons list it fills (the
        # full auto-merge law reads it the same way); a returned tier alone
        # does not mean the steps passed.
        if five_steps is not None:
            check_receipt(five_steps, sub_reasons)
        if five_steps is None or sub_reasons:
            reasons.append("C2: self_scorecard.scorecard_receipt fails the Scorecard Law's five steps — "
                           "an inflated 9.0 on a theater receipt is not authority")
            reasons.extend(f"C2(receipt): {r}" for r in sub_reasons)

    # ---- C3: independent validation by a different seat
    iv = get("independent_validation")
    if not isinstance(iv, dict):
        reasons.append("C3: independent_validation missing — self-declared 9.0 is a claim, not authority")
    else:
        validator = _norm_seat(iv.get("validator_seat"))
        if not validator:
            reasons.append("C3: validator_seat missing — validation must be attributed")
        elif validator == author_seat:
            reasons.append("C3: validator_seat == author_seat — a seat cannot validate itself")
        vscore = iv.get("validator_score")
        if isinstance(vscore, bool) or not isinstance(vscore, (int, float)):
            reasons.append("C3: validator_score must be numeric 0-10")
        elif not (MIN_MERGE_SCORE <= vscore <= 10):
            reasons.append(f"C3: validator_score {vscore} < {MIN_MERGE_SCORE} — independent confirmation must also be 9.0+")
        if iv.get("confirms_most_intelligent_action") is not True:
            reasons.append("C3: validator must confirm this is the most intelligent action, not just a high score")
        if not isinstance(iv.get("ref"), str) or not iv.get("ref").strip():
            reasons.append("C3: ref missing — independent validation must be locatable on the feed")

    # ---- C4: intent posted on #1354; team consensus (no objections)
    intent = get("intent_post")
    if not isinstance(intent, dict):
        reasons.append("C4: intent_post missing — the team must see the intent before the merge")
    else:
        if intent.get("issue") != INTENT_FEED_ISSUE:
            reasons.append(f"C4: intent_post.issue must be {INTENT_FEED_ISSUE} (the coordination feed)")
        if not isinstance(intent.get("comment_id"), int):
            reasons.append("C4: intent_post.comment_id missing — intent must be posted, not claimed")
    consensus = get("consensus")
    if not isinstance(consensus, dict):
        reasons.append("C4: consensus block missing — no-objection must be recorded, not assumed")
    else:
        if _parse_ts(consensus.get("window_closed_at")) is None:
            reasons.append("C4: consensus.window_closed_at missing or unparsable — the objection window must be closed")
        objections = consensus.get("objections")
        if not isinstance(objections, list):
            reasons.append("C4: consensus.objections must be a list (empty if none)")
        elif objections:
            reasons.append(f"C4: {len(objections)} team objection(s) on record — consensus broken, merge needs Shawn's word")

    # ---- C5: post-merge report commitment (the law's fifth condition)
    mr = get("merge_report")
    if not isinstance(mr, dict) or mr.get("will_report_after") is not True:
        reasons.append("C5: merge_report.will_report_after must be true — merge, THEN report after (what, why, scorecard, validator)")


def may_merge_under_delegation(receipt):
    """Return (allowed: bool, reasons: list[str])."""
    check_receipt = _load_check_receipt()
    reasons = []
    _check_delegated_merge_receipt(receipt, check_receipt, reasons)
    return (len(reasons) == 0, reasons)


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if len(paths) != 2:
        print("usage: python3 tools/merge_authority_receipt.py <merge_receipt.json> [--json]",
              file=sys.stderr)
        return 2
    try:
        with open(paths[1], "r", encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"law": LAW_ID, "allowed": False, "error": str(exc)}))
        return 2
    allowed, reasons = may_merge_under_delegation(receipt)
    print(json.dumps({"law": LAW_ID, "allowed": allowed, "reasons": reasons}, indent=2))
    return 0 if allowed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
