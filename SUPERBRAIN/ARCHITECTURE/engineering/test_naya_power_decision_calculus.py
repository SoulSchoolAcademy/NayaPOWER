#!/usr/bin/env python3
from __future__ import annotations

import unittest
from naya_power_decision_calculus import Candidate, decision


class DecisionCalculusTests(unittest.TestCase):
    def test_protected_boundary_overrides_benefit(self):
        result = decision([
            Candidate("forbidden", 100, 100, 100, 100, 100, 100, 100, 0, "PRODUCTION-PROVEN", violates_boundary=True),
            Candidate("safe", 80, 90, 90, 90, 80, 70, 70, 10, "VERIFIED"),
        ])
        self.assertNotEqual(result["chosen"], "forbidden")
        self.assertIn("forbidden", result["boundary_rejections"])

    def test_high_consequence_uncertain_action_defers(self):
        result = decision([Candidate("risky", 100, 20, 10, 90, 20, 90, 90, 90, "TESTED", consequence=95)])
        self.assertEqual(result["disposition"], "DEFER_FOR_VERIFICATION")
        self.assertFalse(result["verified_claim_allowed"])

    def test_verified_responsible_action_can_be_chosen(self):
        result = decision([
            Candidate("verified", 90, 95, 95, 95, 80, 80, 80, 5, "VERIFIED", consequence=20),
            Candidate("unknown", 100, 60, 5, 90, 20, 90, 90, 70, "UNKNOWN", consequence=60),
        ])
        self.assertEqual(result["chosen"], "verified")
        self.assertTrue(result["verified_claim_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
