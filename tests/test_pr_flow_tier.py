"""Regression tests for the PR flow tier classifier."""
import unittest

from tools.pr_flow_tier import classify_tier


class TierClassificationTests(unittest.TestCase):
    def test_pure_note_filing_is_tier_c(self):
        self.assertEqual(
            classify_tier("SN-1771 — Already Built", ["BRAIN/05-MEMORY/SMART-NOTES/SN-1771.md"])["tier"],
            "C",
        )

    def test_pure_index_regeneration_is_tier_c(self):
        self.assertEqual(classify_tier("Index regeneration", ["BRAIN/NAYAPOWER-BRAIN-INDEX.json"])["tier"], "C")

    def test_mixed_note_and_code_is_not_tier_c(self):
        self.assertEqual(
            classify_tier("Smart Note bridge fix", ["BRAIN/05-MEMORY/SMART-NOTES/SN-1.md", "tools/note_bridge_live.py"])["tier"],
            "B",
        )

    def test_workflow_path_escalates_to_tier_a(self):
        self.assertEqual(classify_tier("button fix", ["HUB/button.tsx", ".github/workflows/deploy.yml"])["tier"], "A")

    def test_gate_machinery_escalates_to_tier_a(self):
        self.assertEqual(classify_tier("gate helper", ["tools/check_pr_flow_gate.py"])["tier"], "A")

    def test_ordinary_code_is_tier_b(self):
        self.assertEqual(classify_tier("button fix", ["HUB/button.tsx"])["tier"], "B")

    def test_empty_changed_path_list_fails_safe_to_tier_a(self):
        self.assertEqual(classify_tier("ordinary title", [])["tier"], "A")

    def test_governance_title_escalates_even_without_path_list(self):
        self.assertEqual(classify_tier("Governance contract ratification", [])["tier"], "A")

    def test_governance_path_is_tier_a(self):
        self.assertEqual(classify_tier("ordinary doc", ["BRAIN/01-GOVERNANCE/0025.md"])["tier"], "A")

    def test_supabase_function_path_is_tier_a(self):
        self.assertEqual(classify_tier("intake change", ["supabase/functions/nayanet-github-intake/index.ts"])["tier"], "A")

    def test_learning_event_path_is_tier_c(self):
        path = "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026-10-20-LEARNING-EVENT.md"
        self.assertEqual(classify_tier("learning event filing", [path])["tier"], "C")

    def test_single_ordinary_file_deletion_escalates_to_tier_a(self):
        files = [{"filename": "HUB/button.tsx", "status": "removed", "additions": 0, "deletions": 80}]
        self.assertEqual(classify_tier("button cleanup", ["HUB/button.tsx"], changed_files=files, expected_changed_files=1)["tier"], "A")

    def test_single_note_deletion_escalates_to_tier_a(self):
        path = "BRAIN/05-MEMORY/SMART-NOTES/SN-1234.md"
        files = [{"filename": path, "status": "removed", "additions": 0, "deletions": 20}]
        self.assertEqual(classify_tier("SN-1234 cleanup", [path], changed_files=files, expected_changed_files=1)["tier"], "A")

    def test_eleven_file_deletions_escalate_to_tier_a(self):
        paths = [f"docs/old-{i}.md" for i in range(11)]
        files = [{"filename": p, "status": "removed", "additions": 0, "deletions": 1} for p in paths]
        self.assertEqual(classify_tier("cleanup", paths, changed_files=files, expected_changed_files=11)["tier"], "A")

    def test_rename_out_of_protected_path_escalates_to_tier_a(self):
        files = [{"filename": "docs/new.md", "previous_filename": "BRAIN/01-GOVERNANCE/law.md", "status": "renamed", "additions": 1, "deletions": 1}]
        self.assertEqual(classify_tier("docs move", ["docs/new.md"], changed_files=files, expected_changed_files=1)["tier"], "A")

    def test_missing_file_status_escalates_to_tier_a(self):
        files = [{"filename": "HUB/button.tsx"}]
        self.assertEqual(classify_tier("button fix", ["HUB/button.tsx"], changed_files=files, expected_changed_files=1)["tier"], "A")

    def test_truncated_file_list_escalates_to_tier_a(self):
        files = [{"filename": "HUB/button.tsx", "status": "modified"}]
        self.assertEqual(classify_tier("button fix", ["HUB/button.tsx"], changed_files=files, expected_changed_files=2)["tier"], "A")

    def test_unknown_note_path_does_not_get_tier_c(self):
        self.assertEqual(classify_tier("SN-1234 filing", ["BRAIN/other/place.md"])["tier"], "B")


if __name__ == "__main__":
    unittest.main()
