import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("oscar", Path(__file__).with_name("oscar.py"))
oscar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oscar)


class OscarTests(unittest.TestCase):
    def setUp(self):
        self.claim = {
            "schema": "naya-power-claim/v1",
            "claim_id": "CL-OSCAR-1",
            "statement": "Runtime satisfies its acceptance criteria",
            "success_criteria": ["tests pass", "current commit is verified"],
            "status": "VERIFIED",
        }
        self.evidence = {
            "schema": "naya-power-evidence/v1",
            "evidence_id": "EV-OSCAR-1",
            "claim_id": "CL-OSCAR-1",
            "observed_at": "2026-08-24T02:30:00Z",
            "method": "ci_test",
            "command": "python tests.py",
            "observed_output": "all tests passed",
            "result": "PASS",
            "commit_sha": "abc123",
            "environment": "github-actions",
            "source": "workflow-run-1",
            "criteria_covered": ["tests pass", "current commit is verified"],
        }

    def test_accepts_independently_sufficient_package(self):
        result = oscar.challenge(self.claim, [self.evidence], "abc123")
        self.assertEqual(result["verdict"], "ACCEPT")
        self.assertTrue(result["independent"])
        self.assertTrue(result["promotion_allowed"])

    def test_rejects_model_assertion(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, method="model_assertion")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_memory_assertion(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, method="memory_assertion")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_user_assertion(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, method="user_assertion")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_retrieved_content(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, method="retrieved_content")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_wrong_commit(self):
        result = oscar.challenge(self.claim, [self.evidence], "different")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_stale_or_missing_criteria_coverage(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, criteria_covered=["tests pass"])], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_contradictory_result(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, result="FAIL")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_empty_output(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, observed_output="")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_missing_command(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, command="")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_cross_claim_evidence(self):
        result = oscar.challenge(self.claim, [dict(self.evidence, claim_id="OTHER")], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_unverified_claim(self):
        result = oscar.challenge(dict(self.claim, status="UNVERIFIED"), [self.evidence], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def test_rejects_no_evidence(self):
        result = oscar.challenge(self.claim, [], "abc123")
        self.assertEqual(result["verdict"], "REJECT")

    def _provenanced_accept(self):
        root = Path(__file__).resolve().parents[2]
        commit = oscar.git_head(root)
        evidence = [dict(self.evidence, commit_sha=commit)]
        base = oscar.challenge(self.claim, evidence, commit)
        return oscar.attach_provenance(base, self.claim, evidence, commit, root, "TEST-RUN-1")

    def test_accept_contains_reproducible_provenance(self):
        result = self._provenanced_accept()
        self.assertEqual(result["provenance"]["schema"], "naya-power-oscar-provenance/v1")
        self.assertEqual(result["provenance"]["expected_commit"], result["expected_commit"])
        self.assertEqual(result["provenance"]["implementation_path"], ".naya/runtime/oscar.py")
        self.assertEqual(result["provenance"]["execution_run_id"], "TEST-RUN-1")

    def test_result_digest_changes_when_acceptance_is_tampered(self):
        result = self._provenanced_accept()
        tampered = copy.deepcopy(result)
        tampered["promotion_allowed"] = False
        self.assertNotEqual(tampered["result_sha256"], oscar.sha256_json({k: v for k, v in tampered.items() if k != "result_sha256"}))

    def test_provenance_binds_claim_hash(self):
        result = self._provenanced_accept()
        tampered_claim = copy.deepcopy(self.claim)
        tampered_claim["statement"] = "forged"
        self.assertNotEqual(result["provenance"]["claim_sha256"], oscar.sha256_json(tampered_claim))

    def test_provenance_binds_evidence_hash(self):
        result = self._provenanced_accept()
        tampered = dict(self.evidence, commit_sha=result["expected_commit"], observed_output="forged")
        self.assertNotEqual(result["provenance"]["evidence_sha256"], oscar.sha256_json([tampered]))

    def test_provenance_records_exact_implementation(self):
        result = self._provenanced_accept()
        root = Path(__file__).resolve().parents[2]
        self.assertEqual(result["provenance"]["implementation_commit"], oscar.git_head(root))
        self.assertEqual(result["provenance"]["implementation_sha256"], oscar.git_blob_sha(Path(__file__).with_name("oscar.py"), root))


if __name__ == "__main__":
    unittest.main()
