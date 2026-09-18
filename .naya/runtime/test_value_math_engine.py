import unittest

from value_math_engine import (
    MAX_VALUE,
    MIN_VALUE,
    ValueContext,
    bounded_value,
    choose_best_action,
    constitutional_eligibility,
    mvpa,
    rank_actions,
    weighted_value,
)


class ValueMathEngineTests(unittest.TestCase):
    def test_scale_is_bounded(self):
        self.assertEqual(MIN_VALUE, -9)
        self.assertEqual(MAX_VALUE, 9)

    def test_invalid_is_not_zero(self):
        self.assertEqual(
            constitutional_eligibility(constitution_ok=False), "INVALID"
        )
        self.assertEqual(
            constitutional_eligibility(constitution_ok=True), "ELIGIBLE"
        )

    def test_weighted_value_and_bounded_score(self):
        context = ValueContext(
            objective="Create an excellent useful result",
            weights={"usefulness": 0.5, "quality": 0.5},
        )
        self.assertAlmostEqual(
            weighted_value({"usefulness": 9, "quality": 7}, context), 8.0
        )
        self.assertEqual(
            bounded_value({"usefulness": 9, "quality": 7}, context), 8
        )

    def test_mvpa_prefers_more_verified_value_per_cost(self):
        self.assertAlmostEqual(mvpa(verified_responsible_value=8, resource_cost=2), 4)
        self.assertAlmostEqual(mvpa(verified_responsible_value=9, resource_cost=1), 9)

    def test_invalid_action_is_excluded_not_penalized(self):
        actions = [
            {"id": "invalid-high-value", "eligibility_state": "INVALID", "verified_value": 9, "resource_cost": 1},
            {"id": "valid", "eligibility_state": "ELIGIBLE", "verified_value": 5, "resource_cost": 1},
        ]
        ranked = rank_actions(actions)
        self.assertEqual([item["id"] for item in ranked], ["valid"])

    def test_best_action_is_highest_mvpa(self):
        actions = [
            {"id": "a", "eligibility_state": "ELIGIBLE", "verified_value": 8, "resource_cost": 2},
            {"id": "b", "eligibility_state": "ELIGIBLE", "verified_value": 7, "resource_cost": 1},
        ]
        self.assertEqual(choose_best_action(actions)["id"], "b")

    def test_no_eligible_action_fails_explicitly(self):
        with self.assertRaises(ValueError):
            choose_best_action([
                {"id": "x", "eligibility_state": "INVALID", "verified_value": 9, "resource_cost": 1}
            ])

    def test_zero_cost_is_rejected(self):
        with self.assertRaises(ValueError):
            mvpa(verified_responsible_value=9, resource_cost=0)


if __name__ == "__main__":
    unittest.main()
