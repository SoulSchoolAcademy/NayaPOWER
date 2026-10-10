#!/usr/bin/env python3
"""Hermetic tests for tools/evolve_receipt.py.

Builds a throwaway git fixture repo; the tool must only ever read it.
The real repo is never touched.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "evolve_receipt.py"


def _sh(cwd, *args, env=None):
    e = dict(os.environ)
    e.update({
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
        "GIT_CONFIG_NOSYSTEM": "1",
    })
    if env:
        e.update(env)
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, env=e)
    assert p.returncode == 0, f"git {' '.join(args)}: {p.stderr[:200]}"
    return p.stdout


class FixtureRepo:
    """A temp git repo with three commits: tools-only, docs-only, tests+tools."""

    def __init__(self):
        self.d = tempfile.mkdtemp(prefix="evolve-receipt-fixture-")
        self.root = Path(self.d)
        _sh(self.d, "init", "-q")
        _sh(self.d, "commit", "--allow-empty", "-q", "-m", "root")
        self.base = _sh(self.d, "rev-parse", "HEAD").strip()
        (self.root / "tools").mkdir()
        (self.root / "tools" / "x.py").write_text("X=1\n")
        _sh(self.d, "add", ".")
        _sh(self.d, "commit", "-q", "-m", "feat(evolve): tools-only change")
        self.c_tools = _sh(self.d, "rev-parse", "HEAD").strip()
        (self.root / "docs.md").write_text("docs\n")
        _sh(self.d, "add", ".")
        _sh(self.d, "commit", "-q", "-m", "docs: words only")
        self.c_docs = _sh(self.d, "rev-parse", "HEAD").strip()
        (self.root / "tests").mkdir()
        (self.root / "tests" / "test_x.py").write_text("def test_x(): pass\n")
        (self.root / "tools" / "x.py").write_text("X=2\n")
        _sh(self.d, "add", ".")
        _sh(self.d, "commit", "-q", "-m", "feat(evolve): tools change with tests")
        self.c_tests = _sh(self.d, "rev-parse", "HEAD").strip()


def run_tool(*args):
    p = subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, timeout=120,
    )
    return p


class TestEvolveReceipt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fix = FixtureRepo()

    def _build(self, since, until="HEAD"):
        out = Path(self.fix.d) / "receipt.json"
        p = run_tool("build", "--repo", self.fix.d,
                     "--since", since, "--until", until, "--out", str(out))
        self.assertEqual(p.returncode, 0, p.stderr[:500])
        return json.loads(out.read_text())

    def test_only_surface_commits_listed(self):
        r = self._build(self.fix.base)
        shas = {i["sha"] for i in r["improvements"]}
        self.assertIn(self.fix.c_tools, shas)
        self.assertIn(self.fix.c_tests, shas)
        self.assertNotIn(self.fix.c_docs, shas)
        self.assertNotIn(self.fix.base, shas)

    def test_fields_and_evidence(self):
        r = self._build(self.fix.base)
        by_sha = {i["sha"]: i for i in r["improvements"]}
        tools_item = by_sha[self.fix.c_tools]
        self.assertEqual(tools_item["subject"], "feat(evolve): tools-only change")
        self.assertFalse(tools_item["has_tests"])
        self.assertIn(self.fix.c_tools, tools_item["evidence"])
        tests_item = by_sha[self.fix.c_tests]
        self.assertTrue(tests_item["has_tests"])
        self.assertIn("tools/x.py", tests_item["surface_files"])
        self.assertIn("tests/test_x.py", tests_item["surface_files"])

    def test_summary_counts(self):
        r = self._build(self.fix.base)
        self.assertEqual(r["summary"]["improvement_commits"], 2)
        self.assertEqual(r["summary"]["improvement_commits_with_tests"], 1)
        self.assertEqual(r["commits_scanned"], 3)

    def test_tip_and_window_provenance(self):
        r = self._build(self.fix.base)
        self.assertEqual(r["tip"], self.fix.c_tests)
        self.assertEqual(r["since"], self.fix.base)
        self.assertEqual(r["until"], "HEAD")

    def test_narrow_window(self):
        r = self._build(self.fix.c_tools, self.fix.c_docs)
        shas = {i["sha"] for i in r["improvements"]}
        self.assertEqual(shas, set())  # docs-only commit is not an improvement

    def test_caveats_present(self):
        r = self._build(self.fix.base)
        self.assertTrue(any("NOT proof" in c for c in r["caveats"]))
        self.assertTrue(any("human" in c for c in r["caveats"]))

    def test_bad_repo_exit_1(self):
        out = Path(self.fix.d) / "r2.json"
        p = run_tool("build", "--repo", "/no/such/dir",
                     "--since", "HEAD", "--out", str(out))
        self.assertEqual(p.returncode, 1)

    def test_bad_rev_exit_2(self):
        out = Path(self.fix.d) / "r3.json"
        p = run_tool("build", "--repo", self.fix.d,
                     "--since", "no-such-rev-xyz", "--out", str(out))
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
