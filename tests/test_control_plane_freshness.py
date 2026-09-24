import importlib.util
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate-control-plane-freshness.py"
SPEC = importlib.util.spec_from_file_location("control_plane_freshness", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
BATON_MODULE_PATH = ROOT / ".naya/runtime/baton.py"
BATON_SPEC = importlib.util.spec_from_file_location("canonical_baton", BATON_MODULE_PATH)
BATON_MODULE = importlib.util.module_from_spec(BATON_SPEC)
assert BATON_SPEC.loader is not None
BATON_SPEC.loader.exec_module(BATON_MODULE)


class UnknownResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    def registry(self):
        return {
            "status": "CANONICAL",
            "entries": [
                {
                    "id": "UNKNOWN-MODEL-LEARNING",
                    "statement": "Universal model/provider learning quality remains unproven.",
                    "status": "UNKNOWN",
                    "resolution": None,
                }
            ],
        }

    def state_unknown(self):
        return [{"id": None, "statement": "Universal model/provider learning quality remains unproven.", "declared_status": None}]

    def ledger(self, records=None):
        return {"status": "CANONICAL", "resolutions": records or []}

    def resolve(self, state_unknowns, ledger, proof=None):
        return MODULE.resolve_unknowns(self.registry(), state_unknowns, ledger, ROOT, self.head, proof)

    def test_unrelated_known_statement_does_not_resolve(self):
        result = self.resolve(
            self.state_unknown(),
            self.ledger(),
            {"known": ["An unrelated learning quality report was recorded."]},
        )
        self.assertEqual(result["statuses"]["UNKNOWN-MODEL-LEARNING"], "UNKNOWN")
        self.assertEqual(result["resolved"], [])

    def test_exact_proof_reference_resolves(self):
        result = self.resolve(
            [],
            self.ledger([
                {
                    "resolves_unknown": "UNKNOWN-MODEL-LEARNING",
                    "status": "RESOLVED",
                    "source_commit": self.head,
                    "evidence": [{"kind": "workflow_run", "id": "test-run"}],
                }
            ]),
        )
        self.assertEqual(result["statuses"]["UNKNOWN-MODEL-LEARNING"], "RESOLVED")
        self.assertEqual(result["resolved"], ["UNKNOWN-MODEL-LEARNING"])

    def test_partially_related_statement_does_not_resolve(self):
        result = self.resolve(
            self.state_unknown(),
            self.ledger(),
            {"current_evidence": {"learning_quality": "partial evidence only"}},
        )
        self.assertEqual(result["statuses"]["UNKNOWN-MODEL-LEARNING"], "UNKNOWN")

    def test_stale_proof_does_not_resolve(self):
        with self.assertRaises(MODULE.FreshnessError):
            self.resolve(
                [],
                self.ledger([
                    {
                        "resolves_unknown": "UNKNOWN-MODEL-LEARNING",
                        "status": "RESOLVED",
                        "source_commit": "0" * 40,
                        "evidence": [{"kind": "workflow_run", "id": "stale-run"}],
                    }
                ]),
            )

    def test_superseded_replacement_resolves(self):
        result = self.resolve(
            [],
            self.ledger([
                {
                    "resolves_unknown": "UNKNOWN-MODEL-LEARNING",
                    "status": "SUPERSEDED",
                    "source_commit": self.head,
                    "evidence": [{"kind": "proof", "id": "replacement-proof"}],
                    "replacement": {
                        "statement": "A narrower model-learning claim is now tracked separately.",
                        "evidence_ref": "replacement-proof",
                    },
                }
            ]),
        )
        self.assertEqual(result["statuses"]["UNKNOWN-MODEL-LEARNING"], "SUPERSEDED")
        self.assertEqual(result["superseded"], ["UNKNOWN-MODEL-LEARNING"])


class BatonIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    def test_builder_emits_canonical_identity(self):
        baton = BATON_MODULE.build_baton()
        self.assertEqual(baton["identity"], baton["repository"])
        self.assertEqual(baton["identity"], "SoulSchoolAcademy/NayaPOWER")

    def test_committed_baton_contains_canonical_identity(self):
        baton = MODULE.load_json(ROOT / ".naya/control-plane/BATON.json")
        self.assertEqual(baton["identity"], baton["repository"])

    def test_freshness_rejects_missing_identity(self):
        with self.assertRaisesRegex(MODULE.FreshnessError, "BATON_FIELD_MISSING: identity"):
            MODULE.validate_baton(ROOT, {}, {}, {}, {}, {}, self.head)


class FreshnessOutcomeTests(unittest.TestCase):
    def test_contract_failure_is_expected_red(self):
        report = MODULE.failure_report(ROOT, MODULE.FreshnessError("BATON_FIELD_MISSING: evidence"))
        self.assertEqual(report["outcome"], "EXPECTED_RED")
        self.assertEqual(report["status"], "RED")

    def test_infrastructure_failure_is_not_expected_red(self):
        report = MODULE.failure_report(ROOT, MODULE.InfrastructureError("GIT_FAILED"))
        self.assertEqual(report["outcome"], "INFRASTRUCTURE_FAILURE")
        self.assertEqual(report["status"], "RED")


if __name__ == "__main__":
    unittest.main()
