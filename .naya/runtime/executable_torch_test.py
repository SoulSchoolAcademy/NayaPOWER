"""Adversarial tests for the durable executable Torch boundary."""

import unittest

from executable_torch import TorchError, create_torch
from priority_decision import PriorityDecision


class ExecutableTorchTests(unittest.TestCase):
    def decision(self, **overrides):
        values = dict(
            priority=1,
            work_id="priority-2",
            why="highest-value available work",
            next_action="verify priority boundary",
            expected_value=0.9,
            acceptance_criteria="deterministic suite passes",
            score=0.8,
        )
        values.update(overrides)
        return PriorityDecision(**values)

    def test_creates_self_contained_successor_torch(self):
        torch = create_torch(
            torch_id="torch-003",
            mission="make the Superbrain excellent",
            decision=self.decision(),
            required_evidence="exact test output",
            constraints="do not weaken contracts",
        )
        self.assertEqual(torch.work_id, "priority-2")
        self.assertEqual(torch.next_action, "verify priority boundary")
        self.assertIn("exact test output", torch.required_evidence)
        self.assertIn("next highest-value continuation Torch", torch.successor_instruction)

    def test_rejects_missing_mission(self):
        with self.assertRaises(TorchError):
            create_torch(
                torch_id="torch-003", mission="", decision=self.decision(),
                required_evidence="evidence", constraints="constraints",
            )

    def test_rejects_missing_evidence(self):
        with self.assertRaises(TorchError):
            create_torch(
                torch_id="torch-003", mission="mission", decision=self.decision(),
                required_evidence="", constraints="constraints",
            )

    def test_rejects_missing_constraints(self):
        with self.assertRaises(TorchError):
            create_torch(
                torch_id="torch-003", mission="mission", decision=self.decision(),
                required_evidence="evidence", constraints="",
            )

    def test_rejects_incomplete_decision_fields(self):
        with self.assertRaises(TorchError):
            create_torch(
                torch_id="torch-003", mission="mission",
                decision=self.decision(next_action=""),
                required_evidence="evidence", constraints="constraints",
            )

    def test_rejects_invalid_priority(self):
        with self.assertRaises(TorchError):
            create_torch(
                torch_id="torch-003", mission="mission",
                decision=self.decision(priority=0),
                required_evidence="evidence", constraints="constraints",
            )

    def test_custom_successor_instruction_is_preserved(self):
        instruction = "Run the next gate and preserve exact evidence."
        torch = create_torch(
            torch_id="torch-003", mission="mission", decision=self.decision(),
            required_evidence="evidence", constraints="constraints",
            successor_instruction=instruction,
        )
        self.assertEqual(torch.successor_instruction, instruction)


if __name__ == "__main__":
    unittest.main(verbosity=2)
