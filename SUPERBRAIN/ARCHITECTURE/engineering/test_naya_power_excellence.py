import json
import unittest
from pathlib import Path

from naya_power_excellence import evaluate_excellence, load_policy


class ExcellenceByDefaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_policy()
        cls.dimensions = cls.policy["quality"]["exceptional_dimensions"]
        cls.perfect = {name: 10.0 for name in cls.dimensions}

    def test_exceptional_result(self):
        result = evaluate_excellence(
            self.perfect,
            evidence={"runtime_observation": True},
            policy=self.policy,
        )
        self.assertEqual(result.status, "EXCEPTIONAL")
        self.assertTrue(result.deliverable)
        self.assertGreaterEqual(result.score, 9.5)

    def test_below_threshold_requires_improvement(self):
        scores = {name: 8.0 for name in self.dimensions}
        result = evaluate_excellence(scores, evidence={"runtime_observation": True}, policy=self.policy)
        self.assertEqual(result.status, "IMPROVE")
        self.assertFalse(result.deliverable)

    def test_hard_gate_overrides_high_score(self):
        result = evaluate_excellence(
            self.perfect,
            gates={"fabricated_evidence": True},
            evidence={"runtime_observation": True},
            policy=self.policy,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertFalse(result.deliverable)
        self.assertIn("fabricated_evidence", result.hard_gate_failures)

    def test_missing_dimension_does_not_silently_pass(self):
        scores = dict(self.perfect)
        scores.pop("verification")
        result = evaluate_excellence(scores, evidence={"runtime_observation": True}, policy=self.policy)
        self.assertEqual(result.status, "INSUFFICIENT_EVIDENCE")
        self.assertFalse(result.deliverable)
        self.assertIn("verification", result.missing_evidence)

    def test_missing_evidence_does_not_silently_pass(self):
        result = evaluate_excellence(
            self.perfect,
            evidence={"runtime_observation": False},
            policy=self.policy,
        )
        self.assertEqual(result.status, "INSUFFICIENT_EVIDENCE")
        self.assertFalse(result.deliverable)


if __name__ == "__main__":
    unittest.main()
