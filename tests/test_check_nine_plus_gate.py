#!/usr/bin/env python3
"""Tests for tools/check_nine_plus_delivery.py (SN-0526, first mechanical rung).

Positive and negative controls against the real decision seam:
evaluate() on deliverable texts. Exit codes: 0 PASS, 1 FAIL, 2 NOT_SHAWN_FACING,
3 usage/input error.
"""

import os
import subprocess
import sys
import unittest

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "..", "tools")
TOOL = os.path.join(TOOLS_DIR, "check_nine_plus_delivery.py")

sys.path.insert(0, TOOLS_DIR)
import importlib.util

spec = importlib.util.spec_from_file_location("check_nine_plus_delivery", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestEvaluate(unittest.TestCase):
    def test_shawn_facing_nine_five_passes(self):
        body = (
            "## Delivery to Shawn\n\n"
            "Shawn, here is the merge link. ## Scorecard receipt\n"
            "Honest score: 9.5/10. Enumerate, score, gate, decide, receipt."
        )
        code, verdict = mod.evaluate(body)
        self.assertEqual(code, 0)
        self.assertTrue(verdict["shawn_facing"])
        self.assertTrue(verdict["nine_plus"])
        self.assertEqual(verdict["best_score"], 9.5)

    def test_boundary_nine_passes(self):
        code, verdict = mod.evaluate("Shawn, delivering. Scorecard: 9/10.")
        self.assertEqual(code, 0)
        self.assertTrue(verdict["nine_plus"])

    def test_ten_passes(self):
        code, _ = mod.evaluate("For your review, Shawn. Final score 10/10.")
        self.assertEqual(code, 0)

    def test_eight_nine_fails(self):
        code, verdict = mod.evaluate("Shawn, here is the delivery. Score: 8.9/10.")
        self.assertEqual(code, 1)
        self.assertFalse(verdict["nine_plus"])

    def test_seven_two_fails(self):
        code, _ = mod.evaluate("Merge link for Shawn. Honest score 7.2/10.")
        self.assertEqual(code, 1)

    def test_shawn_facing_unscored_fails(self):
        # The law: scorecarded BEFORE it reaches him. Unscored = FAIL.
        code, verdict = mod.evaluate("Shawn, please merge this PR.")
        self.assertEqual(code, 1)
        self.assertTrue(verdict["shawn_facing"])
        self.assertIsNone(verdict["best_score"])

    def test_lane_traffic_neutral(self):
        body = "[NAYA 4] [LAW-DRIVER] SIGN IN - re-anchored tip, no other seat on LAW."
        code, verdict = mod.evaluate(body)
        self.assertEqual(code, 2)
        self.assertFalse(verdict["shawn_facing"])

    def test_multiple_scores_best_wins(self):
        code, _ = mod.evaluate("Shawn, delivery. Draft scored 7.5/10, final 9.2/10.")
        self.assertEqual(code, 0)

    def test_multiple_scores_all_below_fail(self):
        code, _ = mod.evaluate("Shawn, delivery. Areas: 8.0/10 and 7.5/10.")
        self.assertEqual(code, 1)

    def test_deliverable_assertion_fail_closed(self):
        # --deliverable with unscored text: FAIL, never PASS on UNKNOWN.
        code, verdict = mod.evaluate("some notes without any score", asserted_deliverable=True)
        self.assertEqual(code, 1)
        self.assertTrue(verdict["shawn_facing"])

    def test_none_body_is_usage_error(self):
        code, verdict = mod.evaluate(None)
        self.assertEqual(code, 3)

    def test_score_in_words_not_counted(self):
        # "nine out of ten" is not a machine-readable claimed score.
        code, _ = mod.evaluate("Shawn, delivery. I rate it nine out of ten.")
        self.assertEqual(code, 1)

    def test_spaced_score_format(self):
        code, _ = mod.evaluate("For Shawn. Scorecard: 9.5 / 10")
        self.assertEqual(code, 0)


class TestCLI(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, TOOL, *args],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_cli_pass_exit_zero(self):
        r = self.run_tool("--body", "Shawn, merge link. Scorecard 9.5/10.")
        self.assertEqual(r.returncode, 0)
        self.assertIn("PASS", r.stdout)

    def test_cli_fail_exit_one(self):
        r = self.run_tool("--body", "Shawn, merge link. Scorecard 8/10.")
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL", r.stdout)

    def test_cli_neutral_exit_two(self):
        r = self.run_tool("--body", "lane sign-in, nothing for anyone")
        self.assertEqual(r.returncode, 2)

    def test_cli_no_args_exits_argparse_error(self):
        r = self.run_tool()
        self.assertEqual(r.returncode, 2)  # argparse exits 2 on missing required args
        self.assertIn("usage", r.stderr.lower())

    def test_cli_summary_flag(self):
        r = self.run_tool("--body", "Shawn delivery 9/10", "--summary")
        self.assertEqual(r.returncode, 0)
        self.assertIn("9+ Delivery Gate", r.stdout)

    def test_cli_missing_file_is_error(self):
        r = self.run_tool("--body-file", "/nonexistent/path/body.txt")
        self.assertEqual(r.returncode, 3)


if __name__ == "__main__":
    unittest.main()
