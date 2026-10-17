#!/usr/bin/env python3
"""Tests for check_plain_words.py — Law 2.1.

3 passing + 3 failing cases. Stdlib only (unittest).
"""
import os
import subprocess
import sys
import tempfile
import unittest

CHECK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "check_plain_words.py")


def run_check(workdir):
    return subprocess.run(
        [sys.executable, CHECK, "--workdir", workdir],
        capture_output=True, text=True)


def write_md(workdir, name, text):
    path = os.path.join(workdir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TestPlainWords(unittest.TestCase):
    # ---- passing cases ----
    def test_pass_plain_lead_and_explained_ref(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "## What happened\n\n"
                     "Fixed the merge conflict (#1709): the base branch had "
                     "moved while we worked, so the tree was rebuilt on the "
                     "new tip.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_pass_glossed_jargon(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "## Summary\n\n"
                     "The deploy step is idempotent (i.e. running it twice "
                     "changes nothing), so retries are safe.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_pass_tldr_plain_prose(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "# TL;DR\n\n"
                     "We agreed to postpone the launch until the scorecard "
                     "is finished. Nothing else changed.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 0, r.stdout)

    # ---- failing cases ----
    def test_fail_no_plain_lead(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "## Technical details\n\n"
                     "PR #1709 merged. Tree rebuilt via git-data API calls.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("LEAD-WITH-MEANING", r.stdout)

    def test_fail_bare_pr_numbers(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "## What changed\n\n"
                     "#1709, #1701, #1700\n\n"
                     "All three merged cleanly.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("BARE-PR-NUMBER", r.stdout)

    def test_fail_jargon_without_gloss(self):
        with tempfile.TemporaryDirectory() as d:
            write_md(d, "r.md",
                     "## What happened\n\n"
                     "We made the pipeline idempotent and orthogonal to the "
                     "old flow.\n")
            r = run_check(d)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("JARGON-WITHOUT-GLOSS", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
