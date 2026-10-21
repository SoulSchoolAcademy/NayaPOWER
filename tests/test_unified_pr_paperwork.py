"""Regression tests for the tier thresholds used by the unified paperwork gate."""
import unittest

from tools.check_unified_pr_paperwork import _scorecard_for_current_head


class UnifiedPaperworkThresholdTests(unittest.TestCase):
    def test_tier_a_requires_95_and_different_seat(self):
        head = "a" * 40
        comments = [
            {"body": f"## SCORECARD\nScore: 9.4/10\nHead: {head}\nSeat: Naya Delta"},
            {"body": f"## SCORECARD\nScore: 10/10\nHead: {head}\nSeat: Naya Alpha"},
        ]
        ok, _ = _scorecard_for_current_head(comments, head, "Naya Alpha", 9.5)
        self.assertFalse(ok)

    def test_tier_b_accepts_9_from_different_seat_on_exact_head(self):
        head = "b" * 40
        diff_hash = "d" * 64
        comments = [{"body": f"## SCORECARD\nScore: 9/10\nHead: {head}\nDiff-SHA256: {diff_hash}\nVerification: tests run and replay behavior independently inspected\nSeat: Naya Delta"}]
        ok, _ = _scorecard_for_current_head(comments, head, "Naya Alpha", 9.0, tier="B", diff_hash=diff_hash)
        self.assertTrue(ok)

    def test_stale_head_is_rejected(self):
        current = "c" * 40
        stale = "d" * 40
        comments = [{"body": f"## SCORECARD\nScore: 10/10\nHead: {stale}\nSeat: Naya Delta"}]
        ok, _ = _scorecard_for_current_head(comments, current, "Naya Alpha", 9.0)
        self.assertFalse(ok)

    def test_score_above_ten_is_rejected(self):
        head = "f" * 40
        comments = [{"body": f"## SCORECARD\nScore: 11/10\nHead: {head}\nSeat: Naya Delta"}]
        ok, _ = _scorecard_for_current_head(comments, head, "Naya Alpha", 9.5)
        self.assertFalse(ok)

    def test_tier_b_rejects_below_nine(self):
        head = "b" * 40
        comments = [{"body": f"## SCORECARD\nScore: 8.9/10\nHead: {head}\nSeat: Naya Delta"}]
        ok, _ = _scorecard_for_current_head(comments, head, "Naya Alpha", 9.0)
        self.assertFalse(ok)

    def test_author_cannot_score_own_work(self):
        head = "e" * 40
        comments = [{"body": f"## SCORECARD\nScore: 10/10\nHead: {head}\nSeat: Naya Alpha"}]
        ok, _ = _scorecard_for_current_head(comments, head, "Naya Alpha", 9.0)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
