"""Adversarial tests for the thin Torch-to-canonical-execution adapter."""

import unittest

from executable_torch import ExecutableTorch
from project_execution_contract import NEXT_FIELDS
from torch_execution_adapter import TorchExecutionBindingError, bind_torch_to_canonical_execution


class TorchExecutionAdapterTests(unittest.TestCase):
    def torch(self):
        return ExecutableTorch(
            torch_id="torch-003",
            mission="make the Superbrain excellent",
            priority=1,
            work_id="priority-2",
            why="highest-value available work",
            next_action="verify priority boundary",
            expected_value=0.9,
            acceptance_criteria="deterministic suite passes",
            required_evidence="exact test output",
            constraints="do not weaken contracts",
            successor_instruction="run the next gate and pass the next torch",
        )

    def successor(self):
        return {
            "project": "Naya Power Superbrain",
            "north_star": "make the Superbrain excellent",
            "current_state": "Priority boundary is verified locally",
            "completed_work": ["implemented PriorityDecision"],
            "verified_evidence": ["9/9 deterministic priority tests"],
            "unresolved_issues": ["authoritative Actions verification pending"],
            "constraints": "do not weaken contracts",
            "current_objective": "verify priority boundary",
            "next_action": "verify priority boundary",
            "execution_instructions": "Run the deterministic suite; verify the result; record exact test output.",
            "success_criteria": "deterministic suite passes; acceptance criteria: deterministic suite passes",
            "verification_requirements": "exact test output is recorded",
        }

    def test_valid_binding_uses_existing_contract(self):
        binding = bind_torch_to_canonical_execution(self.torch(), self.successor())
        self.assertEqual(binding.torch_id, "torch-003")
        self.assertEqual(binding.work_id, "priority-2")
        self.assertEqual(tuple(binding.successor), NEXT_FIELDS)

    def test_rejects_invalid_canonical_successor(self):
        successor = self.successor()
        successor.pop("success_criteria")
        with self.assertRaises(TorchExecutionBindingError):
            bind_torch_to_canonical_execution(self.torch(), successor)

    def test_rejects_next_action_divergence(self):
        successor = self.successor()
        successor["next_action"] = "different action"
        with self.assertRaises(TorchExecutionBindingError):
            bind_torch_to_canonical_execution(self.torch(), successor)

    def test_rejects_evidence_divergence(self):
        successor = self.successor()
        successor["verification_requirements"] = "record a receipt"
        with self.assertRaises(TorchExecutionBindingError):
            bind_torch_to_canonical_execution(self.torch(), successor)

    def test_rejects_constraint_divergence(self):
        successor = self.successor()
        successor["constraints"] = "weaken contracts"
        with self.assertRaises(TorchExecutionBindingError):
            bind_torch_to_canonical_execution(self.torch(), successor)

    def test_rejects_acceptance_divergence(self):
        successor = self.successor()
        successor["success_criteria"] = "different criterion"
        with self.assertRaises(TorchExecutionBindingError):
            bind_torch_to_canonical_execution(self.torch(), successor)

    def test_does_not_execute_work(self):
        binding = bind_torch_to_canonical_execution(self.torch(), self.successor())
        self.assertEqual(binding.successor["next_action"], "verify priority boundary")
        self.assertNotIn("executed", binding.successor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
