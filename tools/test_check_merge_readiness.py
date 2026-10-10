#!/usr/bin/env python3
"""Unit tests for check_merge_readiness.py — prove the gate logic works.

Tests the decision logic with mocked GitHub API responses:
1. All green → PASS
2. One check failing → FAIL (names the check)
3. Required check missing → FAIL
4. PR not open → FAIL
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_merge_readiness as cmr


class FakeAPI:
    """Mock GitHub API returning canned responses."""
    def __init__(self, pr_data, check_runs):
        self.pr_data = pr_data
        self.check_runs = check_runs

    def get(self, path, token):
        if "/pulls/" in path:
            return self.pr_data
        if "/check-runs" in path:
            return {"check_runs": self.check_runs}
        if "/status" in path:
            return {"state": "success"}
        raise ValueError(f"unexpected path: {path}")


def run_with_mock(pr_data, check_runs):
    """Run main() with mocked API, capture exit code."""
    fake = FakeAPI(pr_data, check_runs)
    orig_api_get = cmr.api_get
    cmr.api_get = fake.get
    # Set env
    os.environ["GH_TOKEN"] = "fake"
    os.environ["REPO"] = "SoulSchoolAcademy/NayaPOWER"
    os.environ["PR_NUMBER"] = "9999"
    try:
        cmr.main()
        return 0
    except SystemExit as e:
        return e.code
    finally:
        cmr.api_get = orig_api_get


def test_all_green_passes():
    pr = {"head": {"sha": "abc123"}, "state": "open", "merged": False}
    runs = [
        {"name": "test", "status": "completed", "conclusion": "success",
         "completed_at": "2026-10-10T23:00:00Z"},
        {"name": "Team review + scorecard receipt", "status": "completed",
         "conclusion": "success", "completed_at": "2026-10-10T23:00:00Z"},
    ]
    assert run_with_mock(pr, runs) == 0
    print("PASS: all green → exit 0")


def test_failing_check_blocks():
    pr = {"head": {"sha": "abc123"}, "state": "open", "merged": False}
    runs = [
        {"name": "test", "status": "completed", "conclusion": "failure",
         "completed_at": "2026-10-10T23:00:00Z"},
        {"name": "Team review + scorecard receipt", "status": "completed",
         "conclusion": "success", "completed_at": "2026-10-10T23:00:00Z"},
    ]
    assert run_with_mock(pr, runs) == 1
    print("PASS: failing 'test' → exit 1 (merge blocked)")


def test_missing_check_blocks():
    pr = {"head": {"sha": "abc123"}, "state": "open", "merged": False}
    runs = [
        {"name": "test", "status": "completed", "conclusion": "success",
         "completed_at": "2026-10-10T23:00:00Z"},
        # consensus gate hasn't run yet
    ]
    assert run_with_mock(pr, runs) == 1
    print("PASS: missing consensus check → exit 1 (merge blocked)")


def test_closed_pr_blocks():
    pr = {"head": {"sha": "abc123"}, "state": "closed", "merged": False}
    runs = []
    assert run_with_mock(pr, runs) == 1
    print("PASS: closed PR → exit 1 (merge blocked)")


def test_in_progress_check_blocks():
    pr = {"head": {"sha": "abc123"}, "state": "open", "merged": False}
    runs = [
        {"name": "test", "status": "in_progress", "conclusion": None,
         "completed_at": None},
        {"name": "Team review + scorecard receipt", "status": "completed",
         "conclusion": "success", "completed_at": "2026-10-10T23:00:00Z"},
    ]
    assert run_with_mock(pr, runs) == 1
    print("PASS: in-progress check → exit 1 (merge blocked)")


if __name__ == "__main__":
    test_all_green_passes()
    test_failing_check_blocks()
    test_missing_check_blocks()
    test_closed_pr_blocks()
    test_in_progress_check_blocks()
    print("\nAll 5 merge-readiness tests passed.")
