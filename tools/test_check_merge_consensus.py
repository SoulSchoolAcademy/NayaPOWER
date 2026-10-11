#!/usr/bin/env python3
"""Tests for tools/check_merge_consensus.py — the merge-consensus gate.

Covers the F1/F2 fix-forward (2026-10-11, Naya 2 build lane):

- F1 (fail-closed operational break): SEAT_RE was r"naya\\s*([2345])", so
  seat_of("Seat: Naya 1") returned None — a Naya-1-authored PR could never
  pass the gate, and the Coda seats were excluded entirely.
- F2 (fail-open logic hole): the Path-B check was a raw substring test
  ("APPROVED" in body.upper()), so "NOT APPROVED" / "DISAPPROVED" counted
  as an approving review.

Negative controls throughout: the old logic shapes are replicated inline
to prove the tests would have caught the flaws (if you can't break it,
you didn't test it). Stdlib only (unittest).
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_merge_consensus as cmc


# ---------------------------------------------------------------------------
# F1: seat recognition
# ---------------------------------------------------------------------------

class TestSeatOf(unittest.TestCase):
    def test_naya_1_recognized(self):
        # F1 repro on the old regex: r"naya\s*([2345])" never matched "Naya 1".
        self.assertIsNone(
            __import__("re").compile(r"naya\s*([2345])", __import__("re").I)
            .search("Seat: Naya 1"))
        self.assertEqual(cmc.seat_of("Seat: Naya 1"), "Naya 1")

    def test_naya_2_through_5_still_recognized(self):
        for n in ("2", "3", "4", "5"):
            with self.subTest(n=n):
                self.assertEqual(cmc.seat_of(f"Seat: Naya {n}"), f"Naya {n}")

    def test_active_coda_seats_recognized(self):
        for n in ("1", "3", "4"):
            with self.subTest(n=n):
                self.assertEqual(cmc.seat_of(f"Seat: Coda {n}"), f"Coda {n}")

    def test_voided_coda_2_not_recognized(self):
        # Coda 2's lane is voided (off the team 2026-10-04): a tag claiming
        # it must not confer seat authority — fail-closed.
        self.assertIsNone(cmc.seat_of("Seat: Coda 2"))

    def test_no_tag_gives_none(self):
        self.assertIsNone(cmc.seat_of("hello world"))
        self.assertIsNone(cmc.seat_of(""))
        self.assertIsNone(cmc.seat_of(None))

    def test_case_insensitive(self):
        self.assertEqual(cmc.seat_of("seat: naya 1"), "Naya 1")
        self.assertEqual(cmc.seat_of("SEAT: CODA 3"), "Coda 3")

    def test_no_false_positives_on_longer_numbers(self):
        self.assertIsNone(cmc.seat_of("Seat: Naya 12"))
        self.assertIsNone(cmc.seat_of("Seat: Naya 5x"))

    def test_review_style_tags(self):
        self.assertEqual(cmc.seat_of("[NAYA 1 · REVIEW] APPROVED"), "Naya 1")
        self.assertEqual(cmc.seat_of("[CODA 4 · REVIEW] APPROVED"), "Coda 4")


# ---------------------------------------------------------------------------
# F2: negated approvals must not count
# ---------------------------------------------------------------------------

class TestPositiveApproval(unittest.TestCase):
    def test_plain_approved(self):
        self.assertTrue(cmc._has_positive_approval("APPROVED"))

    def test_not_approved_rejected(self):
        # F2 repro: the old check ("APPROVED" in body.upper()) was True here.
        self.assertTrue("APPROVED" in "NOT APPROVED".upper())
        self.assertFalse(cmc._has_positive_approval("NOT APPROVED"))
        self.assertFalse(cmc._has_positive_approval("not approved"))
        self.assertFalse(cmc._has_positive_approval("Review: NOT  APPROVED"))

    def test_disapproved_rejected(self):
        self.assertTrue("APPROVED" in "DISAPPROVED".upper())
        self.assertFalse(cmc._has_positive_approval("DISAPPROVED"))

    def test_never_approved_rejected(self):
        self.assertFalse(cmc._has_positive_approval("NEVER APPROVED"))

    def test_approved_in_sentence(self):
        self.assertTrue(
            cmc._has_positive_approval("Reviewed the diff — approved, ship it."))

    def test_mixed_negated_and_positive(self):
        # A negated approval elsewhere in the text must not cancel a real one.
        self.assertTrue(cmc._has_positive_approval(
            "NOT APPROVED in the old sense; re-reviewed: APPROVED"))


class TestReviewApprovalComment(unittest.TestCase):
    def test_naya_review_comment_counts(self):
        self.assertTrue(
            cmc.is_review_approval_comment("[NAYA 4 · REVIEW] APPROVED"))

    def test_naya1_review_comment_counts(self):
        # F1 closed for Path B as well: Naya 1 can review.
        self.assertTrue(
            cmc.is_review_approval_comment("[NAYA 1 · REVIEW] APPROVED"))

    def test_coda_review_comment_counts(self):
        # F1 closed for Path B as well: Coda reviewers count.
        self.assertTrue(
            cmc.is_review_approval_comment("[CODA 3 · REVIEW] APPROVED"))

    def test_not_approved_comment_rejected(self):
        # F2 end-to-end at the comment level.
        self.assertFalse(
            cmc.is_review_approval_comment("[NAYA 4 · REVIEW] NOT APPROVED"))
        self.assertFalse(
            cmc.is_review_approval_comment("[NAYA 4 · REVIEW] DISAPPROVED"))

    def test_missing_review_marker_rejected(self):
        self.assertFalse(cmc.is_review_approval_comment("[NAYA 4] APPROVED"))

    def test_missing_seat_tag_rejected(self):
        self.assertFalse(cmc.is_review_approval_comment("REVIEW APPROVED"))

    def test_voided_seat_review_rejected(self):
        self.assertFalse(
            cmc.is_review_approval_comment("[CODA 2 · REVIEW] APPROVED"))

    def test_empty_and_none(self):
        self.assertFalse(cmc.is_review_approval_comment(""))
        self.assertFalse(cmc.is_review_approval_comment(None))


# ---------------------------------------------------------------------------
# End-to-end: main() with a stubbed api_get (no network)
# ---------------------------------------------------------------------------

HEAD = "a" * 40
REPO = "o/r"
PRN = "1234"


def _stub_api(pr_body, comments, reviews=()):
    def fake(path, token):
        if path.endswith(f"/pulls/{PRN}") and "reviews" not in path:
            return {"user": {"login": "SoulSchoolAcademy"}, "body": pr_body}
        if path.endswith(f"/pulls/{PRN}/reviews"):
            return list(reviews)
        if path.endswith(f"/issues/{PRN}/comments"):
            return list(comments)
        raise AssertionError(f"unexpected api path: {path}")
    return fake


def _run_main(pr_body, comments, reviews=()):
    env = {"GH_TOKEN": "t", "REPO": REPO, "PR_NUMBER": PRN, "HEAD_SHA": HEAD}
    with mock.patch.dict(os.environ, env, clear=False), \
         mock.patch.object(cmc, "api_get", _stub_api(pr_body, comments, reviews)):
        cmc.main()


def _scorecard(seat, head=HEAD):
    return {"body": f"## SCORECARD\nhead: {head}\nmerge: APPROVED\nSeat: {seat}"}


class TestMainEndToEnd(unittest.TestCase):
    def test_not_approved_fails_the_gate(self):
        # F2 at the gate level: a "NOT APPROVED" review must not pass.
        comments = [
            {"body": "[NAYA 4 · REVIEW] NOT APPROVED"},
            _scorecard("Naya 4"),
        ]
        with self.assertRaises(SystemExit) as ctx:
            _run_main("Seat: Naya 2", comments)
        self.assertEqual(ctx.exception.code, 1)

    def test_naya1_reviewer_now_passes(self):
        # F1 at the gate level: Naya 1 can review and score.
        comments = [
            {"body": "[NAYA 1 · REVIEW] APPROVED"},
            _scorecard("Naya 1"),
        ]
        _run_main("Seat: Naya 2", comments)  # no SystemExit = pass

    def test_coda_reviewer_and_scorer_pass(self):
        comments = [
            {"body": "[CODA 3 · REVIEW] APPROVED"},
            _scorecard("Coda 3"),
        ]
        _run_main("Seat: Naya 2", comments)  # no SystemExit = pass

    def test_author_cannot_review_own_work(self):
        comments = [
            {"body": "[NAYA 2 · REVIEW] APPROVED"},
            _scorecard("Naya 2"),
        ]
        with self.assertRaises(SystemExit) as ctx:
            _run_main("Seat: Naya 2", comments)
        self.assertEqual(ctx.exception.code, 1)

    def test_naya1_authored_pr_now_passes(self):
        # F1's headline case: a Naya-1-authored PR can pass the gate.
        comments = [
            {"body": "[NAYA 4 · REVIEW] APPROVED"},
            _scorecard("Naya 4"),
        ]
        _run_main("Seat: Naya 1", comments)  # no SystemExit = pass

    def test_stale_head_scorecard_still_rejected(self):
        # Requirement 2 unchanged: scorecard must name the exact head SHA.
        comments = [
            {"body": "[NAYA 4 · REVIEW] APPROVED"},
            _scorecard("Naya 4", head="b" * 40),
        ]
        with self.assertRaises(SystemExit) as ctx:
            _run_main("Seat: Naya 2", comments)
        self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
