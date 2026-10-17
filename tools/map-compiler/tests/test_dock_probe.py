#!/usr/bin/env python3
"""Regression tests for the honesty-critical dock-probe state mapping.

Covers every branch VERIFY/Chi confirmed at head 9f4aaf18 (PR #2687, receipt
comment 6234995308): the mapping must never report green for work that did
not land, and must never go silently green when it cannot measure.

Runs on stdlib unittest only:  python3 -m unittest discover -s tools/map-compiler/tests
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import map_compiler
from map_compiler import dock_pr_status, probe_dock


def _check(conclusion):
    return {"conclusion": conclusion, "status": "completed", "name": "gate"}


class TestDockPrStatus(unittest.TestCase):
    """Pure-function branch coverage for dock_pr_status()."""

    def test_merged_open_is_green(self):
        self.assertEqual(dock_pr_status("open", True, "green"), "green")

    def test_merged_closed_is_green(self):
        # merged wins over state: the planned work landed
        self.assertEqual(dock_pr_status("closed", True, "failing"), "green")

    def test_open_ci_green_is_amber(self):
        self.assertEqual(dock_pr_status("open", False, "green"), "amber")

    def test_open_ci_failing_is_amber(self):
        self.assertEqual(dock_pr_status("open", False, "failing"), "amber")

    def test_open_ci_pending_is_amber(self):
        self.assertEqual(dock_pr_status("open", False, "pending"), "amber")

    def test_open_ci_no_checks_is_amber(self):
        self.assertEqual(dock_pr_status("open", False, "no checks"), "amber")

    def test_closed_unmerged_with_green_ci_is_red(self):
        # THE honesty case: rejected/abandoned work is never green,
        # even when its CI was green.
        self.assertEqual(dock_pr_status("closed", False, "green"), "red")

    def test_closed_unmerged_with_failing_ci_is_red(self):
        self.assertEqual(dock_pr_status("closed", False, "failing"), "red")

    def test_unknown_state_is_unknown(self):
        self.assertEqual(dock_pr_status("draft", False, "green"), "unknown")

    def test_empty_state_is_unknown(self):
        self.assertEqual(dock_pr_status("", False, "pending"), "unknown")


def _pr(state, merged, sha="abc123"):
    return {"state": state, "merged": merged, "head": {"sha": sha}, "number": 2678}


def _gh_get_for(pr_payload=None, pr_err=None, checks=()):
    def fake(path, token):
        if "/pulls/" in path:
            return pr_payload, pr_err
        return {"check_runs": list(checks)}, None

    return fake


class TestProbeDock(unittest.TestCase):
    """probe_dock() integration: worst-rollup + loud-unknown behavior."""

    def test_no_token_is_unknown(self):
        out = probe_dock({"gh_token": ""})
        self.assertEqual(out["status"], "unknown")
        self.assertIn("no GH_TOKEN", out["evidence"])

    def test_unreadable_pr_is_unknown_not_green(self):
        with patch.object(
            map_compiler, "gh_get", _gh_get_for(pr_payload=None, pr_err={"http_status": 404})
        ), patch.object(map_compiler, "DOCK_PRS", [2678]):
            out = probe_dock({"gh_token": "x"})
        self.assertEqual(out["status"], "unknown")
        self.assertIn("unreadable", out["evidence"])

    def test_open_pr_green_ci_is_amber(self):
        with patch.object(
            map_compiler,
            "gh_get",
            _gh_get_for(_pr("open", False), checks=[_check("success")]),
        ), patch.object(map_compiler, "DOCK_PRS", [2678]):
            out = probe_dock({"gh_token": "x"})
        self.assertEqual(out["status"], "amber")

    def test_closed_unmerged_pr_green_ci_is_red(self):
        # End-to-end honesty: abandoned dock PR with green CI must surface red.
        with patch.object(
            map_compiler,
            "gh_get",
            _gh_get_for(_pr("closed", False), checks=[_check("success")]),
        ), patch.object(map_compiler, "DOCK_PRS", [2678]):
            out = probe_dock({"gh_token": "x"})
        self.assertEqual(out["status"], "red")

    def test_merged_pr_is_green(self):
        with patch.object(
            map_compiler,
            "gh_get",
            _gh_get_for(_pr("closed", True), checks=[_check("success")]),
        ), patch.object(map_compiler, "DOCK_PRS", [2678]):
            out = probe_dock({"gh_token": "x"})
        self.assertEqual(out["status"], "green")

    def test_worst_wins_across_prs(self):
        prs = {
            2678: _pr("closed", True, sha="aaa"),
            2679: _pr("closed", False, sha="bbb"),
        }

        def fake(path, token):
            if "/pulls/" in path:
                num = int(path.rsplit("/", 1)[-1])
                return prs[num], None
            return {"check_runs": [_check("success")]}, None

        with patch.object(map_compiler, "gh_get", fake), patch.object(
            map_compiler, "DOCK_PRS", [2678, 2679]
        ):
            out = probe_dock({"gh_token": "x"})
        # one merged (green) + one abandoned (red) -> red wins
        self.assertEqual(out["status"], "red")


if __name__ == "__main__":
    unittest.main()
