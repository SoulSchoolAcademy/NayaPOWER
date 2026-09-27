import unittest
from unittest.mock import patch

from scripts.verify_evaluator_source import inspect_source


class EvaluatorSourceGateTests(unittest.TestCase):
    def test_current_clean_origin_main_is_accepted(self):
        responses = {
            ("rev-parse", "--show-toplevel"): "/repo",
            ("rev-parse", "HEAD"): "abc123\n",
            ("rev-parse", "origin/main"): "abc123\n",
            ("symbolic-ref", "--short", "-q", "HEAD"): "main\n",
            ("status", "--porcelain"): "\n",
        }

        def run_git(*args):
            class R:
                stdout = responses[args]
            return R()

        with patch("scripts.verify_evaluator_source.run_git", side_effect=run_git):
            result = inspect_source()

        self.assertTrue(result.ok)
        self.assertEqual(result.freshness, "CURRENT")

    def test_stale_checkout_is_rejected(self):
        responses = {
            ("rev-parse", "--show-toplevel"): "/repo",
            ("rev-parse", "HEAD"): "oldsha\n",
            ("rev-parse", "origin/main"): "newsha\n",
            ("symbolic-ref", "--short", "-q", "HEAD"): "coda1/evaluation\n",
            ("status", "--porcelain"): "\n",
        }

        def run_git(*args):
            class R:
                stdout = responses[args]
            return R()

        with patch("scripts.verify_evaluator_source.run_git", side_effect=run_git):
            result = inspect_source()

        self.assertFalse(result.ok)
        self.assertEqual(result.freshness, "STALE")
        self.assertIn("HEAD", " ".join(result.reasons))

    def test_dirty_checkout_is_rejected(self):
        responses = {
            ("rev-parse", "--show-toplevel"): "/repo",
            ("rev-parse", "HEAD"): "abc123\n",
            ("rev-parse", "origin/main"): "abc123\n",
            ("symbolic-ref", "--short", "-q", "HEAD"): "main\n",
            ("status", "--porcelain"): " M .naya/control-plane/STATE.json\n",
        }

        def run_git(*args):
            class R:
                stdout = responses[args]
            return R()

        with patch("scripts.verify_evaluator_source.run_git", side_effect=run_git):
            result = inspect_source()

        self.assertFalse(result.ok)
        self.assertEqual(result.freshness, "DIRTY")

    def test_missing_origin_main_is_not_assumed_current(self):
        responses = {
            ("rev-parse", "--show-toplevel"): "/repo",
            ("rev-parse", "HEAD"): "abc123\n",
            ("rev-parse", "origin/main"): "",
            ("symbolic-ref", "--short", "-q", "HEAD"): "main\n",
            ("status", "--porcelain"): "\n",
        }

        def run_git(*args):
            class R:
                stdout = responses[args]
            return R()

        with patch("scripts.verify_evaluator_source.run_git", side_effect=run_git):
            result = inspect_source()

        self.assertFalse(result.ok)
        self.assertEqual(result.freshness, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
