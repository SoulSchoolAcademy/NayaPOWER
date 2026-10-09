#!/usr/bin/env python3
"""Falsifier suite for tools/merge_authority_receipt.py.

DELEGATED-MERGE-AUTHORITY-V1 (Shawn, 2026-10-08): Naya 5 may merge to main
without per-merge approval IFF all five conditions hold. Every test below
tries to break one condition; the gate must DENY each break and ALLOW only
the fully-proven receipt. A manufactured 9.0 on a theater receipt must
never authorize a merge.
"""

import copy
import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools")
sys.path.insert(0, TOOLS_DIR)

from merge_authority_receipt import may_merge_under_delegation  # noqa: E402


def _valid_five_step_receipt():
    """A genuinely valid Scorecard Law five-step receipt (passes _check_receipt)."""
    return {
        "decision_id": "naya5/merge-authority-receipt-gate",
        "engine": "value_calculus_v2.1",
        "decided_at": "2026-10-08T15:50:00Z",
        "decided_by": "naya-5",
        "rigor_tier": "LIGHT",
        "lane": "authority-governance",
        "owner_seat": "naya-5",
        "author_seat": "naya-5",
        "author_lane": "authority-governance",
        "step1_enumerate": {
            "options": [
                {"id": "a", "description": "build delegated-merge receipt gate"},
                {"id": "b", "description": "bridge forgery binding only"},
                {"id": "c", "description": "survey only, no build"},
            ]
        },
        "step2_score": {
            "scores": {
                "a": {"value": 9.5, "consequences": 9.0,
                      "mission_vision_alignment": 9.0, "situational_awareness": 9.5},
                "b": {"value": 8.0, "consequences": 7.5,
                      "mission_vision_alignment": 8.0, "situational_awareness": 7.5},
                "c": {"value": 5.0, "consequences": 6.0,
                      "mission_vision_alignment": 6.0, "situational_awareness": 5.0},
            }
        },
        "step3_gate": {"reversible": True, "no_major_damage": True,
                       "positive_forward_effect": True},
        "step4_decide": {
            "winner": "a",
            "strongest_alternative": {"summary": "bridge forgery binding is real but DEPLOY is Shawn-gated, so it ships no machine value this shift"},
            "falsifier": "if Naya 4's independent review finds the gate accepts a forged receipt, the 9.0 claim is void",
        },
        "step5_receipt": {"receipt_posted_comment_id": 6063575482},
    }


def _valid_receipt():
    return {
        "decision_id": "naya5/merge-authority-receipt-gate-20261008",
        "branch": "naya5/merge-authority-receipt-gate",
        "base_sha": "aacbcc9a566c913e37a5f19f1a47b3e5d719d3ba",
        "tip_sha_at_intent": "aacbcc9a566c913e37a5f19f1a47b3e5d719d3ba",
        "author_seat": "naya-5",
        "self_scorecard": {
            "score": 9.2,
            "comment_id": 6063575482,
            "calculus_profile_id": "authgov-shift-20261008-1542",
            "scorecard_receipt": _valid_five_step_receipt(),
        },
        "tests": {
            "green": True,
            "suites": ["tests/test_merge_authority_receipt.py"],
            "evidence": "21/21 green @ 9f3c2a11 (isolated checkout, stdlib only)",
        },
        "independent_validation": {
            "validator_seat": "naya-4",
            "validator_score": 9.1,
            "confirms_most_intelligent_action": True,
            "ref": "#1606 comment 6063001234",
        },
        "intent_post": {"issue": 1354, "comment_id": 6063005678},
        "consensus": {"window_closed_at": "2026-10-08T16:00:00Z", "objections": []},
        "merge_report": {"will_report_after": True},
    }


class TestDelegatedMergeReceiptGate(unittest.TestCase):
    def allow(self, receipt):
        allowed, reasons = may_merge_under_delegation(receipt)
        return allowed, reasons

    def test_valid_receipt_allows(self):
        allowed, reasons = self.allow(_valid_receipt())
        self.assertTrue(allowed, f"valid receipt denied: {reasons}")

    def test_missing_receipt_denies(self):
        allowed, reasons = self.allow(None)
        self.assertFalse(allowed)

    def test_branch_main_denies(self):
        r = _valid_receipt()
        r["branch"] = "main"
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("writes ON main" in x for x in reasons))

    def test_tip_moved_denies(self):
        r = _valid_receipt()
        r["base_sha"] = "0000000000000000000000000000000000000000"
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("SN-0493" in x for x in reasons))

    def test_tests_not_green_denies(self):
        r = _valid_receipt()
        r["tests"]["green"] = False
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_missing_test_evidence_denies(self):
        r = _valid_receipt()
        r["tests"]["evidence"] = "green"
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_score_8_9_denies(self):
        r = _valid_receipt()
        r["self_scorecard"]["score"] = 8.9
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("9.0" in x for x in reasons))

    def test_score_exactly_9_0_allows_boundary(self):
        r = _valid_receipt()
        r["self_scorecard"]["score"] = 9.0
        allowed, reasons = self.allow(r)
        self.assertTrue(allowed, f"boundary 9.0 denied: {reasons}")

    def test_unposted_scorecard_denies(self):
        r = _valid_receipt()
        del r["self_scorecard"]["comment_id"]
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_theater_receipt_with_inflated_score_denies(self):
        """9.6 on a receipt whose five steps are theater must NOT authorize."""
        r = _valid_receipt()
        r["self_scorecard"]["score"] = 9.6
        r["self_scorecard"]["scorecard_receipt"]["step4_decide"]["falsifier"] = "ok"
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("theater" in x for x in reasons))

    def test_winner_not_highest_total_denies(self):
        r = _valid_receipt()
        r["self_scorecard"]["scorecard_receipt"]["step4_decide"]["winner"] = "b"
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_missing_calculus_profile_denies(self):
        r = _valid_receipt()
        del r["self_scorecard"]["calculus_profile_id"]
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_validator_is_author_denies(self):
        r = _valid_receipt()
        r["independent_validation"]["validator_seat"] = "naya-5"
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("cannot validate itself" in x for x in reasons))

    def test_validator_score_8_9_denies(self):
        r = _valid_receipt()
        r["independent_validation"]["validator_score"] = 8.9
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_validator_not_confirming_intelligence_denies(self):
        r = _valid_receipt()
        r["independent_validation"]["confirms_most_intelligent_action"] = False
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_intent_wrong_issue_denies(self):
        r = _valid_receipt()
        r["intent_post"]["issue"] = 1606
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_objection_denies(self):
        r = _valid_receipt()
        r["consensus"]["objections"] = [{"seat": "naya-1", "ref": "#1354 comment 1"}]
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed)
        self.assertTrue(any("objection" in x for x in reasons))

    def test_missing_consensus_window_denies(self):
        r = _valid_receipt()
        del r["consensus"]["window_closed_at"]
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_no_report_commitment_denies(self):
        r = _valid_receipt()
        r["merge_report"]["will_report_after"] = False
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_non_numeric_score_denies(self):
        r = _valid_receipt()
        r["self_scorecard"]["score"] = True
        allowed, _ = self.allow(r)
        self.assertFalse(allowed)

    def test_future_window_denies(self):
        """Validator reproduction (#1354 c6088678545): a consensus window
        closing in the FUTURE must not read as closed — objections cannot
        exist yet, so condition 4 (team consensus) is unproven. Probes the
        time dimension the 20-test suite never varied: both the validator's
        far-future literal and a near-future window must deny."""
        for label, closed_at in (
            ("validator-far-future", "2099-12-31T23:59:59Z"),
            ("near-future", (datetime.now(timezone.utc).replace(microsecond=0)
                             + timedelta(hours=1)).isoformat()),
        ):
            with self.subTest(window=label):
                r = _valid_receipt()
                r["consensus"]["window_closed_at"] = closed_at
                allowed, reasons = self.allow(r)
                self.assertFalse(allowed, f"{label} window ALLOWED: {reasons}")
                self.assertTrue(any("future" in x for x in reasons), reasons)

    def test_bool_comment_id_denies(self):
        """isinstance(True, int) is True in Python: a bool is not a posted
        comment id. Both comment_id fields must exclude bools, matching the
        bool-exclusion the gate already applies to score fields."""
        for label, block in (("scorecard", "self_scorecard"),
                             ("intent", "intent_post")):
            with self.subTest(field=label):
                r = _valid_receipt()
                r[block]["comment_id"] = True
                allowed, _ = self.allow(r)
                self.assertFalse(allowed, f"bool {label}.comment_id ALLOWED")

    def test_bool_receipt_posted_comment_id_denies(self):
        """#1943 B5: the five-step checker this gate delegates C2 to is the
        canonical seam — a bool where the posted comment id belongs must
        deny there, not be worked around in the caller. A bare True is not
        a written-and-posted receipt."""
        r = _valid_receipt()
        r["self_scorecard"]["scorecard_receipt"]["step5_receipt"]["receipt_posted_comment_id"] = True
        allowed, reasons = self.allow(r)
        self.assertFalse(allowed, "bool receipt_posted_comment_id ALLOWED")
        self.assertTrue(any("receipt_posted_comment_id" in x for x in reasons), reasons)


if __name__ == "__main__":
    unittest.main()
