from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("current_truth_integration.py")
SPEC = importlib.util.spec_from_file_location("current_truth_integration", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class CurrentTruthIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = MODULE.build_receipt()

    def test_feature_branch_is_not_claimed_as_current_source(self) -> None:
        self.assertEqual(self.receipt["source_identity"]["source_scope"], "NON_MAIN_SOURCE_SCOPE")
        self.assertEqual(self.receipt["truth_status"], "NOT_CURRENT_SOURCE_SCOPE")
        self.assertEqual(self.receipt["verification_status"], "VERIFIED_MECHANISM")
        self.assertEqual(self.receipt["verification_scope"], "RECONSTRUCTION_RECEIPT_ONLY")
        self.assertFalse(self.receipt["source_identity"]["recorded_heads_are_authoritative"])

    def test_reconstruction_is_reproducible_and_truth_is_not_promoted(self) -> None:
        self.assertEqual(self.receipt["reconstruction_status"], "RECONSTRUCTED")
        self.assertEqual(self.receipt["reconstruction"]["status"], "RECONSTRUCTED")
        self.assertTrue(self.receipt["reconstruction"]["reproducible"])
        self.assertEqual(self.receipt["reconstruction"]["counts"]["current"], 0)
        self.assertEqual(self.receipt["reconstruction"]["counts"]["unknown"], 12)
        self.assertEqual({item["classification"] for item in self.receipt["reconstruction"]["current_items"]}, {"UNKNOWN"})
        self.assertIn("STATUS_NOT_CURRENT_ELIGIBLE:VERIFIED_REPOSITORY_RECORD", {
            reason
            for item in self.receipt["reconstruction"]["current_items"]
            for reason in item["reason_codes"]
        })

    def test_control_plane_next_action_blocker_is_carried_forward(self) -> None:
        control = self.receipt["control_plane"]
        self.assertEqual(control["map_current_next_action_status"], "BLOCKED")
        self.assertEqual(control["baton_next_action_status"], "BLOCKED")
        self.assertIn("intelligence_commit", control["next_action"])
        self.assertTrue(any(snapshot["matches_live_head"] is False for snapshot in control["snapshots"]))

    def test_snapshot_matrix_reports_all_five_sources_without_authority_promotion(self) -> None:
        snapshots = self.receipt["control_plane"]["snapshots"]
        self.assertEqual(
            {snapshot["path"] for snapshot in snapshots},
            {
                ".naya/control-plane/STATE.json",
                ".naya/control-plane/BLOCKS.json",
                ".naya/control-plane/MAP.json",
                ".naya/control-plane/PROOF.json",
                ".naya/control-plane/BATON.json",
            },
        )
        self.assertTrue(all(snapshot["authority"] in {"SNAPSHOT_ONLY", "MISSING"} for snapshot in snapshots))
        self.assertTrue(any(snapshot["currentness"] == "CURRENTNESS_UNPROVEN" for snapshot in snapshots))
        self.assertTrue(any(snapshot["currentness"] == "STALE" for snapshot in snapshots))

    def test_ambiguous_status_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.receipt)
        tampered["status"] = "VERIFIED"
        self.assertIn("ambiguous top-level status field is forbidden", MODULE.validate_receipt(tampered))

    def test_existing_execution_boundary_is_referenced_not_executed(self) -> None:
        boundary = self.receipt["canonical_execution_boundary"]
        self.assertEqual(boundary["status"], "NOT_EXECUTED")
        self.assertEqual(boundary["required_chain"], [
            "actor",
            "authority",
            "decision",
            "execution",
            "intelligence_commit",
            "persistence",
            "receipt",
        ])
        self.assertEqual(boundary["authority_registry"], ".naya/governance/authority-registry.json")

    def test_receipt_digest_and_tamper_detection(self) -> None:
        self.assertEqual(MODULE.validate_receipt(self.receipt), [])
        tampered = copy.deepcopy(self.receipt)
        tampered["reconstruction"]["counts"]["current"] = 1
        self.assertIn("receipt digest is invalid", MODULE.validate_receipt(tampered))

    def test_truth_boundary_is_explicit(self) -> None:
        serialized = json.dumps(self.receipt, sort_keys=True)
        self.assertIn("does not promote UNKNOWN", serialized)
        self.assertIn("execute authority", serialized)
        self.assertIn("persist intelligence", serialized)


if __name__ == "__main__":
    unittest.main()
