#!/usr/bin/env python3
"""Self-test for tools/pr_body_selfcheck.py.

Runs the tool as a subprocess against crafted bodies and asserts the
verdict matches the receipt gate's own verdict. Stdlib only.
Run from the repo root: python3 -m pytest tools/test_pr_body_selfcheck.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "pr_body_selfcheck.py")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def real_sha():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def run(body, via_stdin=False):
    if via_stdin:
        return subprocess.run([sys.executable, TOOL], input=body, cwd=REPO,
                              capture_output=True, text=True)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        path = f.name
    try:
        return subprocess.run([sys.executable, TOOL, path], cwd=REPO,
                              capture_output=True, text=True)
    finally:
        os.unlink(path)


class TestSelfcheck(unittest.TestCase):
    def test_pass_path_handle(self):
        body = ("Seat: Naya Gamma\n\n## Evidence\n\n"
                "- `tools/check_pr_receipt.py` — the gate itself\n")
        r = run(body)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("SELFCHECK PASS", r.stdout)
        self.assertNotIn("warning", r.stdout)

    def test_pass_sha_handle(self):
        body = ("Seat: Naya Gamma\n\n## Evidence\n\n"
                "- head %s\n" % real_sha())
        r = run(body)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("SELFCHECK PASS", r.stdout)

    def test_fail_bold_evidence(self):
        # The #2612 recurring class: **Evidence** is not ## Evidence.
        body = ("**Evidence**\n\n- `tools/check_pr_receipt.py`\n")
        r = run(body)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("SELFCHECK FAIL", r.stdout)
        self.assertIn("no `## Evidence` section", r.stdout)

    def test_fail_h3_evidence(self):
        body = ("### Evidence\n\n- `tools/check_pr_receipt.py`\n")
        r = run(body)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no `## Evidence` section", r.stdout)

    def test_fail_no_handles(self):
        body = "## Evidence\n\nJust prose, no handles.\n"
        r = run(body)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no verifiable artifact handle", r.stdout)

    def test_fail_dead_sha(self):
        body = "## Evidence\n\n- " + "f" * 40 + "\n"
        r = run(body)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("dead artifact handle", r.stdout)

    def test_evidence_cut_at_next_heading(self):
        # Handles after the next ## heading do not count for the section.
        body = ("## Evidence\n\nprose only\n\n## Notes\n\n"
                "- `tools/check_pr_receipt.py`\n")
        r = run(body)
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_seat_warning_passes(self):
        body = "## Evidence\n\n- `tools/check_pr_receipt.py`\n"
        r = run(body)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("warning", r.stdout)

    def test_heading_case_insensitive(self):
        body = ("Seat: Naya Gamma\n\n## evidence\n\n"
                "- `tools/check_pr_receipt.py`\n")
        r = run(body)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_stdin(self):
        body = ("Seat: Naya Gamma\n\n## Evidence\n\n"
                "- `tools/check_pr_receipt.py`\n")
        r = run(body, via_stdin=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("SELFCHECK PASS", r.stdout)


if __name__ == "__main__":
    unittest.main()
