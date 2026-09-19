import importlib.util
import unittest
import tempfile
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("evidence", Path(__file__).with_name("evidence_runtime.py"))
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.good = {
            "schema": evidence.EVIDENCE_SCHEMA,
            "evidence_id": "EV-1",
            "claim_id": "CL-1",
            "observed_at": "2026-08-24T02:00:00Z",
            "method": "ci_test",
            "command": "python -m unittest",
            "observed_output": "10 tests passed",
            "result": "PASS",
            "commit_sha": "abc123",
            "environment": "github-actions",
            "source": "workflow-run-1",
        }
        self.claim = {
            "schema": evidence.CLAIM_SCHEMA,
            "claim_id": "CL-1",
            "statement": "Runtime passes tests",
            "success_criteria": ["all tests pass"],
            "created_at": "2026-08-24T02:00:00Z",
            "status": "VERIFIED",
            "evidence_ids": ["EV-1"],
            "source": "test",
        }


    def test_persist_and_independently_recover_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp)
            created = evidence.persist_evidence(self.good, evidence_store=store)
            self.assertEqual(created["status"], "CREATED")
            recovered_item = evidence.load_evidence("EV-1", evidence_store=store)
            self.assertEqual(recovered_item, self.good)
            replay = evidence.persist_evidence(self.good, evidence_store=store)
            self.assertEqual(replay["status"], "REPLAY")

    def test_persist_rejects_conflicting_evidence_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp)
            evidence.persist_evidence(self.good, evidence_store=store)
            conflict = dict(self.good, observed_output="different real output")
            self.assertEqual(evidence.persist_evidence(conflict, evidence_store=store)["status"], "CONFLICT")

    def test_valid_verified_claim(self):
        self.assertEqual(evidence.verify_claim(self.claim, {"EV-1": self.good}, "abc123")["status"], "VERIFIED")

    def test_missing_evidence_rejected(self):
        self.assertEqual(evidence.verify_claim(self.claim, {}, "abc123")["status"], "REJECTED")

    def test_wrong_commit_rejected(self):
        self.assertEqual(evidence.verify_claim(self.claim, {"EV-1": self.good}, "different")["status"], "REJECTED")

    def test_model_assertion_rejected(self):
        self.assertTrue(evidence.validate_evidence(dict(self.good, method="model_assertion")))

    def test_memory_assertion_rejected(self):
        self.assertTrue(evidence.validate_evidence(dict(self.good, method="memory_assertion")))

    def test_retrieved_content_rejected(self):
        self.assertTrue(evidence.validate_evidence(dict(self.good, method="retrieved_content")))

    def test_failed_evidence_cannot_verify(self):
        self.assertEqual(evidence.verify_claim(self.claim, {"EV-1": dict(self.good, result="FAIL")}, "abc123")["status"], "REJECTED")

    def test_empty_observed_output_rejected(self):
        self.assertTrue(evidence.validate_evidence(dict(self.good, observed_output="")))

    def test_missing_command_rejected(self):
        self.assertTrue(evidence.validate_evidence(dict(self.good, command="")))

    def test_cross_claim_evidence_rejected(self):
        self.assertEqual(evidence.verify_claim(self.claim, {"EV-1": dict(self.good, claim_id="OTHER")}, "abc123")["status"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
