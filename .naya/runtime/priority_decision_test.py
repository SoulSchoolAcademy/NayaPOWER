"""Adversarial tests for the deterministic Priority Decision boundary."""

import unittest

from priority_decision import PriorityError, WorkItem, choose_priority


class PriorityDecisionTests(unittest.TestCase):
    def item(self, work_id, **overrides):
        values = dict(
            work_id=work_id,
            title=work_id,
            next_action=f"execute {work_id}",
            acceptance_criteria=f"{work_id} verified",
            mission_alignment=0.5,
            expected_value=0.5,
            urgency=0.5,
            dependency_impact=0.5,
            reversibility=0.5,
            risk=0.1,
        )
        values.update(overrides)
        return WorkItem(**values)

    def test_selects_one_highest_value_action(self):
        decision = choose_priority(
            "ship the mission",
            [
                self.item("low", mission_alignment=0.4, expected_value=0.3),
                self.item("high", mission_alignment=1.0, expected_value=1.0, dependency_impact=1.0),
            ],
        )
        self.assertEqual(decision.priority, 1)
        self.assertEqual(decision.work_id, "high")
        self.assertEqual(decision.next_action, "execute high")

    def test_blocked_item_cannot_win(self):
        decision = choose_priority(
            "advance",
            [
                self.item("blocked", mission_alignment=1.0, expected_value=1.0, blocked=True),
                self.item("available", mission_alignment=0.6, expected_value=0.6),
            ],
        )
        self.assertEqual(decision.work_id, "available")

    def test_non_executable_item_cannot_win(self):
        decision = choose_priority(
            "advance",
            [
                self.item("unavailable", mission_alignment=1.0, expected_value=1.0, executable=False),
                self.item("available", mission_alignment=0.6, expected_value=0.6),
            ],
        )
        self.assertEqual(decision.work_id, "available")

    def test_requires_mission(self):
        with self.assertRaises(PriorityError):
            choose_priority("", [self.item("x")])

    def test_requires_actionable_work(self):
        with self.assertRaises(PriorityError):
            choose_priority("advance", [self.item("x", next_action="")])

    def test_requires_acceptance_criteria(self):
        with self.assertRaises(PriorityError):
            choose_priority("advance", [self.item("x", acceptance_criteria="")])

    def test_rejects_out_of_range_scores(self):
        with self.assertRaises(PriorityError):
            choose_priority("advance", [self.item("x", risk=2.0)])

    def test_risk_reduces_priority_when_other_factors_match(self):
        decision = choose_priority(
            "advance",
            [
                self.item("safe", risk=0.0),
                self.item("risky", risk=1.0),
            ],
        )
        self.assertEqual(decision.work_id, "safe")

    def test_output_contract_is_complete(self):
        decision = choose_priority("advance", [self.item("x")])
        self.assertTrue(decision.why)
        self.assertEqual(decision.priority, 1)
        self.assertTrue(decision.next_action)
        self.assertTrue(decision.acceptance_criteria)
        self.assertGreaterEqual(decision.expected_value, 0)


if __name__ == "__main__":
    unittest.main()
