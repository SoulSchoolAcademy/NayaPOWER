#!/usr/bin/env python3
"""Unit tests for the strengthened check_merge_consensus.py.

Proves:
1. Review WITHOUT head SHA → FAIL (stale review)
2. Review WITH head SHA → PASS (fresh review)
3. Unresolved CHANGES_REQUESTED → FAIL (contested)
4. CHANGES_REQUESTED superseded by later APPROVAL → PASS
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_merge_consensus as cmc

HEAD = "abc123def456"


class FakeAPI:
    def __init__(self, pr, reviews, comments):
        self.pr = pr
        self.reviews = reviews
        self.comments = comments

    def get(self, path, token):
        if path.endswith(f"/pulls/9999"):
            return self.pr
        if "/reviews" in path:
            return self.reviews
        if "/comments" in path:
            return self.comments
        raise ValueError(path)


def run(pr_body, reviews, comments):
    fake = FakeAPI(
        {"user": {"login": "soulschool"}, "body": pr_body},
        reviews, comments)
    orig = cmc.api_get
    cmc.api_get = fake.get
    os.environ.update({"GH_TOKEN": "x", "REPO": "r", "PR_NUMBER": "9999",
                       "HEAD_SHA": HEAD})
    try:
        cmc.main()
        return 0
    except SystemExit as e:
        return e.code
    finally:
        cmc.api_get = orig


def test_stale_review_without_sha_fails():
    """Review comment lacking the head SHA is stale → FAIL."""
    code = run(
        "Seat: Naya 5",
        [],
        [{"body": "[NAYA 4 · REVIEW] APPROVED — looks good."}])
    assert code == 1, "stale review should fail"
    print("PASS: stale review (no SHA) → exit 1")


def test_fresh_review_with_sha_passes():
    """Review comment naming the head SHA → PASS."""
    code = run(
        "Seat: Naya 5",
        [],
        [{"body": f"[NAYA 4 · REVIEW] APPROVED head {HEAD[:10]}"},
         {"body": f"## SCORECARD\nhead: {HEAD}\nSeat: Naya 3\nmerge: APPROVED"}])
    assert code == 0, "fresh review should pass"
    print("PASS: fresh review (with SHA) → exit 0")


def test_unresolved_objection_fails():
    """CHANGES_REQUESTED with no later approval → FAIL."""
    code = run(
        "Seat: Naya 5",
        [{"user": {"login": "reviewer"}, "state": "CHANGES_REQUESTED",
          "body": "This breaks X", "submitted_at": "2026-10-10T22:00:00Z"}],
        [{"body": f"[NAYA 4 · REVIEW] APPROVED head {HEAD[:10]}"},
         {"body": f"## SCORECARD\nhead: {HEAD}\nSeat: Naya 3\nmerge: APPROVED"}])
    assert code == 1, "unresolved objection should fail"
    print("PASS: unresolved objection → exit 1")


def test_superseded_objection_passes():
    """CHANGES_REQUESTED followed by APPROVAL from same seat → PASS."""
    code = run(
        "Seat: Naya 5",
        [{"user": {"login": "reviewer"}, "state": "CHANGES_REQUESTED",
          "body": "Fix X", "submitted_at": "2026-10-10T22:00:00Z"},
         {"user": {"login": "reviewer"}, "state": "APPROVED",
          "body": f"Fixed, approving {HEAD[:10]}",
          "submitted_at": "2026-10-10T23:00:00Z"}],
        [{"body": f"## SCORECARD\nhead: {HEAD}\nSeat: Naya 3\nmerge: APPROVED"}])
    # Note: Path A picks up the native approval; needs SHA in body
    assert code == 0, "superseded objection should pass"
    print("PASS: superseded objection → exit 0")


if __name__ == "__main__":
    test_stale_review_without_sha_fails()
    test_fresh_review_with_sha_passes()
    test_unresolved_objection_fails()
    test_superseded_objection_passes()
    print("\nAll 4 consensus-strengthening tests passed.")
