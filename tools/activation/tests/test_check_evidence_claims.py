#!/usr/bin/env python3
"""Tests for check_evidence_claims.py — Laws 4.6 / 8.3.

3 passing + 3 failing cases. Stdlib only (unittest).
"""
import os
import subprocess
import sys
import tempfile
import unittest

CHECK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "check_evidence_claims.py")


def run_check(workdir, *extra):
    return subprocess.run(
        [sys.executable, CHECK, "--workdir", workdir, *extra],
        capture_output=True, text=True)


def write_md(workdir, name, text):
    path = os.path.join(workdir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TestEvidenceClaims(unittest.TestCase):
    # ---- passing cases ----
    def test_pass_cited_percentage(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Report\n\nTest pass rate is 100% (see CI run "
                     "https://example.com/ci/42, all 58 tests green).\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_pass_cited_score_and_pr(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Scorecard\n\nScore: 9.2/10 per independent review, "
                     "evidence: scorecard receipt in PR #1967.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_pass_no_claims(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Notes\n\nWe discussed the plan and agreed on next "
                     "steps. Nothing is decided yet.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    # ---- failing cases ----
    def test_fail_bare_verified_claim(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Report\n\nThe migration ledger is VERIFIED and the "
                     "deploy is PROVEN safe.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("VERIFIED", r.stdout)

    def test_fail_bare_score(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Scorecard\n\nHonest self-score: 9.5/10. Ship it.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("9.5/10", r.stdout)

    def test_fail_bare_count(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# Report\n\nAll 58 tests pass with zero failures.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("58 tests", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
