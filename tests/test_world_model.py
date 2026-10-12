#!/usr/bin/env python3
"""
Tests for tools/world_model.py — the World Model (Layer 1).

Covers:
  - snapshot correctness (all sections present, no guessing)
  - incremental refresh (no redundant API calls when fresh)
  - UNKNOWN marking on API failures (never fills gaps with assumptions)
  - query accuracy (correct answers from cached data)
  - freshness annotations
"""

import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

# Import the module under test
TOOLS_DIR = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import world_model as wm


class TestSectionStatus(unittest.TestCase):
    def test_fresh_within_limit(self):
        ts = time.time() - 10
        self.assertEqual(wm.section_status(ts, 300), "FRESH")

    def test_stale_beyond_limit(self):
        ts = time.time() - 400
        self.assertEqual(wm.section_status(ts, 300), "STALE")

    def test_unknown_when_no_timestamp(self):
        self.assertEqual(wm.section_status(None, 300), "UNKNOWN")

    def test_boundary(self):
        ts = time.time() - 299  # just inside the limit
        self.assertEqual(wm.section_status(ts, 300), "FRESH")


class TestMarkUnknown(unittest.TestCase):
    def test_unknown_has_reason_and_timestamp(self):
        s = wm.mark_unknown("tip", "API exploded")
        self.assertEqual(s["status"], "UNKNOWN")
        self.assertEqual(s["reason"], "API exploded")
        self.assertIn("as_of_utc", s)
        self.assertIn("as_of_ts", s)

    def test_unknown_never_guesses_data(self):
        # UNKNOWN sections must not contain fabricated data fields
        s = wm.mark_unknown("prs", "failed")
        self.assertNotIn("prs", s)
        self.assertNotIn("count", s)
        self.assertNotIn("sha", s)


class TestLawsSection(unittest.TestCase):
    def test_laws_from_local_file(self):
        # Laws come from the local briefing — no API needed
        section = wm.build_laws_section()
        if not wm.BRIEFING_PATH.exists():
            self.assertEqual(section["status"], "UNKNOWN")
        else:
            self.assertEqual(section["status"], "OK")
            self.assertIn("sha12", section)
            self.assertIn("headers", section)
            self.assertGreater(len(section["headers"]), 0)

    def test_laws_unknown_when_missing(self):
        with patch.object(wm, "BRIEFING_PATH", Path("/nonexistent/briefing.md")):
            section = wm.build_laws_section()
            self.assertEqual(section["status"], "UNKNOWN")
            self.assertIn("reason", section)


class TestEmptyModel(unittest.TestCase):
    def test_empty_model_structure(self):
        m = wm.empty_model()
        self.assertIn("version", m)
        self.assertIn("sections", m)
        self.assertEqual(m["sections"], {})


class TestPRPagination(unittest.TestCase):
    def test_pagination_fetches_all_pages(self):
        """PR builder must paginate beyond 100."""
        page1 = [{"number": i, "title": f"PR {i}", "head": {"sha": "abc", "ref": "b"},
                  "mergeable": True, "draft": False,
                  "created_at": "", "user": {"login": "x"}} for i in range(100)]
        page2 = [{"number": 101, "title": "PR 101", "head": {"sha": "abc", "ref": "b"},
                  "mergeable": True, "draft": False,
                  "created_at": "", "user": {"login": "x"}}]

        def fake_gh(method, path, body_file=None):
            # Exact page matching — avoid "page=1" matching "page=10"
            import re
            m = re.search(r"[?&]page=(\d+)", path)
            page = int(m.group(1)) if m else 1
            if page == 1:
                return True, page1
            elif page == 2:
                return True, page2
            return True, []

        with patch.object(wm, "gh_api", side_effect=fake_gh):
            section = wm.build_prs_section()
            self.assertEqual(section["status"], "OK")
            self.assertEqual(section["count"], 101)

    def test_pr_api_failure_first_page_unknown(self):
        with patch.object(wm, "gh_api", return_value=(False, "boom")):
            section = wm.build_prs_section()
            self.assertEqual(section["status"], "UNKNOWN")
            self.assertIn("boom", section["reason"])


class TestCIStatusQuery(unittest.TestCase):
    def test_ci_query_needs_pr_number(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "OK", "prs": []}}}
        with patch.object(wm, "load_model", return_value=fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": ["ci", "status"]})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            self.assertIn("Specify a PR", buf.getvalue())

    def test_ci_query_unknown_pr(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "OK", "prs": []}}}
        with patch.object(wm, "load_model", return_value=fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": ["ci", "status", "#9999"]})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            self.assertIn("UNKNOWN", buf.getvalue())

    def test_ci_query_returns_check_runs(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {
            "sections": {
                "prs": {
                    "status": "OK",
                    "prs": [{"number": 2410, "title": "Test", "head_sha": "abc",
                             "head_branch": "b", "mergeable": True,
                             "draft": False, "created_at": "",
                             "user": "x"}],
                }
            }
        }
        def fake_gh(method, path, body_file=None):
            if "/pulls/2410" in path:
                return True, {"head": {"sha": "fullsha123"}}
            if "/check-runs" in path:
                return True, {"check_runs": [
                    {"name": "test-gate", "status": "completed",
                     "conclusion": "success"},
                    {"name": "other-gate", "status": "completed",
                     "conclusion": "failure"},
                ]}
            return False, "unexpected"

        with patch.object(wm, "load_model", return_value=fake_model), \
             patch.object(wm, "gh_api", side_effect=fake_gh):
            buf = io.StringIO()
            args = type("Args", (), {"question": ["ci", "status", "#2410"]})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            out = buf.getvalue()
            self.assertIn("2 checks", out)
            self.assertIn("test-gate", out)


class TestQueryRouting(unittest.TestCase):
    def setUp(self):
        # Build a fake cached model
        self.fake_model = {
            "version": 1,
            "sections": {
                "tip": {
                    "status": "OK",
                    "sha": "abc123def456",
                    "short": "abc123de",
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
                "prs": {
                    "status": "OK",
                    "count": 2,
                    "prs": [
                        {
                            "number": 2410,
                            "title": "Consolidate decision engine",
                            "head_sha": "8de2ac16",
                            "head_branch": "naya5/decision-engine-consolidation",
                            "mergeable": True,
                            "draft": False,
                            "created_at": "2026-10-12T00:00:00Z",
                            "user": "SoulSchoolAcademy",
                        },
                        {
                            "number": 2407,
                            "title": "Brain index re-stamp",
                            "head_sha": "b2653895",
                            "head_branch": "naya5/brain-index-regen",
                            "mergeable": None,
                            "draft": False,
                            "created_at": "2026-10-12T00:00:00Z",
                            "user": "SoulSchoolAcademy",
                        },
                    ],
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
                "lanes": {
                    "status": "OK",
                    "lanes": {
                        "alpha": {
                            "status": "OK", "issue": 1713, "state": "FREE",
                            "occupant": "", "last_activity": "",
                            "comment_count": 270,
                        },
                        "beta": {
                            "status": "OK", "issue": 1714, "state": "OCCUPIED",
                            "occupant": "world-model build",
                            "last_activity": "2026-10-12T00:39:00Z",
                            "comment_count": 132,
                        },
                        "gamma": {
                            "status": "OK", "issue": 1715, "state": "FREE",
                            "occupant": "", "last_activity": "",
                            "comment_count": 119,
                        },
                    },
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
                "ledger": {
                    "status": "OK", "issue": 2396, "title": "Smart Ledger",
                    "state": "open", "comment_count": 42,
                    "updated_at": "2026-10-12T00:00:00Z",
                    "url": "https://github.com/x/issues/2396",
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
                "mission": {
                    "status": "OK", "issue": 2154, "title": "Mission State",
                    "state": "open", "comment_count": 10,
                    "updated_at": "2026-10-12T00:00:00Z",
                    "body_preview": "Priority 1: engine consolidation",
                    "url": "https://github.com/x/issues/2154",
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
                "laws": {
                    "status": "OK",
                    "source": "/fake/briefing.md",
                    "sha12": "abc123",
                    "line_count": 207,
                    "headers": ["WHO YOU ARE", "THE ONE QUESTION"],
                    "as_of_utc": "2026-10-12T00:00:00+00:00",
                    "as_of_ts": time.time(),
                },
            },
        }

    def _run_query(self, question):
        import io
        from contextlib import redirect_stdout
        with patch.object(wm, "load_model", return_value=self.fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": question.split()})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            return buf.getvalue()

    def test_query_mergeable_prs(self):
        out = self._run_query("what PRs are mergeable?")
        self.assertIn("#2410", out)
        self.assertIn("1 mergeable", out)

    def test_query_free_lanes(self):
        out = self._run_query("which lanes are free?")
        self.assertIn("alpha", out)
        self.assertIn("FREE", out)
        self.assertIn("OCCUPIED", out)

    def test_query_tip(self):
        out = self._run_query("what is the live tip?")
        self.assertIn("abc123def456", out)

    def test_query_unknown_question(self):
        out = self._run_query("what is the meaning of life?")
        self.assertIn("don't know how to answer", out)

    def test_query_unknown_section(self):
        # If PR data is UNKNOWN, query says UNKNOWN — never guesses
        self.fake_model["sections"]["prs"] = wm.mark_unknown("prs", "API down")
        out = self._run_query("what PRs are mergeable?")
        self.assertIn("UNKNOWN", out)


class TestRefreshSkipsFresh(unittest.TestCase):
    def test_refresh_skips_fresh_sections(self):
        """Refresh must not call builders for fresh sections (API economy)."""
        now = time.time()
        cached = {
            "version": 1,
            "sections": {
                # laws is fresh (local file, 24h limit) — should be skipped
                "laws": {
                    "status": "OK",
                    "sha12": "fakesha12",
                    "as_of_ts": now - 100,
                    "as_of_utc": "x",
                },
                # tip is always refreshed (critical, cheap)
                "tip": {
                    "status": "OK",
                    "sha": "oldsha",
                    "as_of_ts": now - 10,
                    "as_of_utc": "x",
                },
            },
        }

        builder_calls = []

        def fake_tip_builder(cached=None):
            builder_calls.append("tip")
            return {"status": "OK", "sha": "newsha",
                    "as_of_ts": now, "as_of_utc": "x"}

        def fake_laws_builder(cached=None):
            builder_calls.append("laws")
            return {"status": "OK", "sha12": "fakesha12",
                    "as_of_ts": now, "as_of_utc": "x"}

        with patch.object(wm, "load_model", return_value=cached), \
             patch.object(wm, "save_model", return_value="/fake/path"), \
             patch.dict(wm.SECTION_BUILDERS, {"tip": fake_tip_builder,
                                              "laws": fake_laws_builder}):
            # Only tip and laws in builders for this test
            args = type("Args", (), {})()
            wm.cmd_refresh(args)

        # tip should be refreshed (always), laws should be skipped (fresh)
        self.assertIn("tip", builder_calls)
        self.assertNotIn("laws", builder_calls)


class TestSnapshotStructure(unittest.TestCase):
    def test_snapshot_writes_all_sections(self):
        """Snapshot must include all six sections."""
        fake_sections = {}
        for name in wm.SECTION_BUILDERS:
            fake_sections[name] = {"status": "OK", "as_of_ts": time.time()}

        def make_builder(name):
            def b(cached=None):
                return fake_sections[name]
            return b

        builders = {n: make_builder(n) for n in wm.SECTION_BUILDERS}
        saved = {}

        def fake_save(model):
            saved.update(model)
            return "/fake/path"

        with patch.dict(wm.SECTION_BUILDERS, builders), \
             patch.object(wm, "save_model", side_effect=fake_save):
            args = type("Args", (), {})()
            wm.cmd_snapshot(args)

        for name in wm.SECTION_BUILDERS:
            self.assertIn(name, saved["sections"], f"missing section: {name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
