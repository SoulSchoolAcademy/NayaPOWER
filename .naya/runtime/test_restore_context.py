import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import restore_context as rc


class RestoreContextTests(unittest.TestCase):
    def test_current_restore_has_required_contract(self):
        result = rc.build_restore()
        self.assertIn(result["status"], {"VERIFIED", "UNKNOWN"})
        self.assertEqual(result["schema"], "naya-power-restore-context/v4")
        self.assertIn("current_state", result)
        self.assertIn("repository_reality", result)
        self.assertIn("memory", result)
        self.assertIn("next_best_action", result)

    def test_repository_reality_is_observed_not_inferred(self):
        result = rc.repository_reality()
        self.assertTrue(result["available"])
        self.assertRegex(result["head_sha"], r"^[0-9a-f]{40}$")

    def test_temporal_restore_selects_only_effective_memory(self):
        canonical = [
            {"intelligent_block_id": "IB-OLD", "date": "2026-08-20", "status": "CANONICAL", "canonical": True, "content": "old"},
            {"intelligent_block_id": "IB-NEW", "date": "2026-08-25", "status": "CANONICAL", "canonical": True, "content": "new"},
        ]
        target = datetime(2026, 8, 23, tzinfo=timezone.utc)
        with patch.object(rc, "retrieve_canonical_ibs", return_value=canonical):
            snap = rc.memory_snapshot("", target, 10, principal_id="cold-naya", scope="system", project="NayaPOWER", principal_project="NayaPOWER")
        ids = [n["intelligent_block_id"] for n in snap["selected"]]
        self.assertIn("IB-OLD", ids)
        self.assertNotIn("IB-NEW", ids)

    def test_superseded_memory_is_not_active_current_truth(self):
        canonical = [
            {"intelligent_block_id": "IB-OLD", "date": "2026-08-20", "status": "SUPERSEDED", "canonical": True, "content": "old"},
        ]
        with patch.object(rc, "retrieve_canonical_ibs", return_value=canonical):
            snap = rc.memory_snapshot("", None, 10, principal_id="cold-naya", scope="system", project="NayaPOWER", principal_project="NayaPOWER")
        self.assertEqual([x["intelligent_block_id"] for x in snap["selected"]], ["IB-OLD"])

    def test_checkpoint_contains_integrity_hash_without_writing_repo(self):
        result = rc.build_restore()
        fake_path = rc.CHECKPOINT_DIR / "test-checkpoint.json"
        with patch.object(rc, "write_artifact", return_value=fake_path):
            payload = rc.checkpoint(result)["checkpoint"]
        self.assertEqual(len(payload["integrity_sha256"]), 64)

    def test_memory_snapshot_uses_canonical_ib_retrieval_not_legacy_notes(self):
        canonical = [
            {
                "intelligent_block_id": "IB-000001",
                "canonical": True,
                "date": "2026-09-24",
                "status": "CANONICAL",
                "content": "# SMART NOTE\\ncanonical intelligence",
                "source": {"registry": ".naya/memory/smart-notes/REGISTRY.json", "intelligent_block_id": "IB-000001"},
            }
        ]
        with patch.object(rc, "retrieve_canonical_ibs", return_value=canonical) as retrieve_mock:
            snap = rc.memory_snapshot("canonical intelligence", None, 10, principal_id="cold-naya", scope="system", project="NayaPOWER", principal_project="NayaPOWER")
        retrieve_mock.assert_called_once_with(
            "canonical intelligence",
            limit=30,
            root=rc.ROOT,
            principal_id="cold-naya",
            scope="system",
            project="NayaPOWER",
            principal_project="NayaPOWER",
            grants=(),
        )
        self.assertEqual([x["intelligent_block_id"] for x in snap["selected"]], ["IB-000001"])
        self.assertEqual(snap["source"], "canonical_ib_registry")

    def test_temporal_canonical_restore_does_not_use_event_lineage_as_memory(self):
        canonical = [
            {"intelligent_block_id": "IB-OLD", "canonical": True, "date": "2026-08-20", "status": "CANONICAL", "content": "old"},
            {"intelligent_block_id": "IB-NEW", "canonical": True, "date": "2026-08-25", "status": "CANONICAL", "content": "new"},
        ]
        with patch.object(rc, "retrieve_canonical_ibs", return_value=canonical):
            snap = rc.memory_snapshot("", datetime(2026, 8, 23, tzinfo=timezone.utc), 10, principal_id="cold-naya", scope="system", project="NayaPOWER", principal_project="NayaPOWER")
        self.assertEqual([x["intelligent_block_id"] for x in snap["selected"]], ["IB-OLD"])


if __name__ == "__main__":
    unittest.main()
