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

    def test_governance_title_escalates_even_without_path_list(self):
        self.assertEqual(classify_tier("Governance contract ratification", [])["tier"], "A")

    def test_unknown_note_path_does_not_get_tier_c(self):
        self.assertEqual(classify_tier("SN-1234 filing", ["BRAIN/other/place.md"])["tier"], "B")


if __name__ == "__main__":
    unittest.main()
