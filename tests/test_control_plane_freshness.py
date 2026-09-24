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


if __name__ == "__main__":
    unittest.main()
