#!/usr/bin/env python3
"""Adversarial tests for the execution -> evidence boundary."""
import unittest
from execution_evidence_adapter import build_evidence, validate_execution_result, validate_evidence_boundary

BASE = {
    "execution_state": "COMPLETED",
    "execution_id": "EX-001",
    "action": "run deterministic suite",
    "observed_output": "Ran 7 tests in 0.001s\nOK",
    "result": "PASS",
    "commit_sha": "abc123",
}

class ExecutionEvidenceBoundaryTests(unittest.TestCase):
    def test_unexecuted_action_rejected(self):
        item = dict(BASE, execution_state="PLANNED")
        self.assertIn("COMPLETED", " ".join(validate_execution_result(item)))

    def test_missing_observable_result_rejected(self):
        item = dict(BASE, observed_output="")
        self.assertIn("observed_output", " ".join(validate_execution_result(item)))

    def test_evidence_identifies_execution_and_action(self):
        evidence = build_evidence(BASE, evidence_id="EV-001", claim_id="CL-001", method="command_execution", command="python test.py", environment="local", source="execution")
        self.assertEqual(evidence["execution_id"], "EX-001")
        self.assertEqual(evidence["action"], "run deterministic suite")
        self.assertEqual(validate_evidence_boundary(evidence), [])

    def test_boundary_never_sets_verification(self):
        evidence = build_evidence(BASE, evidence_id="EV-002", claim_id="CL-001", method="command_execution", command="python test.py", environment="local", source="execution")
        self.assertNotIn("verification_status", evidence)
        self.assertNotIn("verified", evidence)

    def test_malformed_evidence_rejected(self):
        evidence = build_evidence(BASE, evidence_id="EV-003", claim_id="CL-001", method="command_execution", command="python test.py", environment="local", source="execution")
        evidence.pop("execution_id")
        self.assertTrue(validate_evidence_boundary(evidence))

    def test_valid_evidence_is_successor_consumable(self):
        evidence = build_evidence(BASE, evidence_id="EV-004", claim_id="CL-001", method="command_execution", command="python test.py", environment="local", source="execution")
        required = {"schema", "evidence_id", "claim_id", "observed_at", "method", "command", "observed_output", "result", "commit_sha", "environment", "source", "execution_id", "action"}
        self.assertTrue(required.issubset(evidence))

    def test_forbidden_method_rejected(self):
        with self.assertRaises(ValueError):
            build_evidence(BASE, evidence_id="EV-005", claim_id="CL-001", method="model_assertion", command="model", environment="local", source="execution")

if __name__ == "__main__":
    unittest.main(verbosity=2)
