import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import restore_context as rc


class RestoreContextTests(unittest.TestCase):
    def test_current_restore_has_required_contract(self):
        result = rc.build_restore()
        self.assertIn(result["status"], {"VERIFIED", "UNKNOWN"})
        self.assertEqual(result["schema"], "naya-power-restore-context/v1")
        self.assertIn("current_state", result)
        self.assertIn("repository_reality", result)
        self.assertIn("memory", result)
        self.assertIn("next_best_action", result)

    def test_repository_reality_is_observed_not_inferred(self):
        result = rc.repository_reality()
        self.assertTrue(result["available"])
        self.assertRegex(result["head_sha"], r"^[0-9a-f]{40}$")

    def test_temporal_restore_selects_only_effective_memory(self):
        notes = [
            (Path("old.json"), {
                "id": "SN-20260820-000000-old", "status": "ACTIVE",
                "effective_at": "2026-08-20T00:00:00+00:00"
            }),
            (Path("new.json"), {
                "id": "SN-20260825-000000-new", "status": "ACTIVE",
                "effective_at": "2026-08-25T00:00:00+00:00"
            }),
        ]
        target = datetime(2026, 8, 23, tzinfo=timezone.utc)
        with patch.object(rc, "notes", return_value=notes):
            snap = rc.memory_snapshot("", target, 10)
        ids = [n["id"] for n in snap["selected"]]
        self.assertIn("SN-20260820-000000-old", ids)
        self.assertNotIn("SN-20260825-000000-new", ids)

    def test_superseded_memory_is_not_active_current_truth(self):
        notes = [
            (Path("old.json"), {
                "id": "SN-20260820-000000-old", "status": "SUPERSEDED",
                "effective_at": "2026-08-20T00:00:00+00:00",
                "superseded_at": "2026-08-22T00:00:00+00:00"
            })
        ]
        with patch.object(rc, "notes", return_value=notes):
            snap = rc.memory_snapshot("", None, 10)
        self.assertEqual(snap["selected"], [])

    def test_checkpoint_contains_integrity_hash_without_writing_repo(self):
        result = rc.build_restore()
        fake_path = rc.CHECKPOINT_DIR / "test-checkpoint.json"
        with patch.object(rc, "write_artifact", return_value=fake_path):
            payload = rc.checkpoint(result)["checkpoint"]
        self.assertEqual(len(payload["integrity_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
