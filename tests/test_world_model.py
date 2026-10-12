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


class TestAtomicSave(unittest.TestCase):
    def test_save_is_atomic(self):
        # save_model must write via temp + os.replace so a concurrent
        # reader never sees a half-written file.
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "world-model.json"
            with patch.object(wm, "MODEL_PATH", target):
                wm.save_model({"version": 1, "sections": {}})
                self.assertTrue(target.exists())
                self.assertEqual(json.loads(target.read_text())["version"], 1)
                # No temp file left behind
                self.assertEqual(list(Path(d).glob("*.tmp")), [])


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
        fake_model = {"sections": {"prs": {"status": "OK", "prs": [],
                                          "as_of_ts": time.time()}}}
        with patch.object(wm, "load_model", return_value=fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": ["ci", "status"]})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            self.assertIn("Specify a PR", buf.getvalue())

    def test_ci_query_unknown_pr(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "OK", "prs": [],
                                          "as_of_ts": time.time()}}}
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
                    "as_of_ts": time.time(),
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


def make_fresh_model():
    """Fresh (FRESH-timestamped) fake world-model for query tests."""
    return {
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
                    "lease_note": "OBSERVED coordination only — not a mutex.",
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


class TestQueryRouting(unittest.TestCase):
    def setUp(self):
        self.fake_model = make_fresh_model()

    def _run_query(self, question):
        import io
        from contextlib import redirect_stdout
        with patch.object(wm, "load_model", return_value=self.fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": question.split()})()
            with redirect_stdout(buf):
                wm.cmd_query(args)
            return buf.getvalue()

    def test_query_mergeable_prs_directive(self):
        # P0-F2: mergeability can never be claimed from the PR list — even
        # fresh list data must refuse and point at the evidence path.
        # (Old code printed "N mergeable PRs" from list data; that claim is
        #  false because GitHub's list API never returns `mergeable`.)
        out = self._run_query("what PRs are mergeable?")
        self.assertIn("READ_MORE", out)
        self.assertIn("merge check #", out)
        self.assertNotIn("mergeable PRs:", out)

    def test_query_free_lanes(self):
        out = self._run_query("which lanes are free?")
        self.assertIn("alpha", out)
        self.assertIn("FREE", out)
        self.assertIn("OCCUPIED", out)
        # Lane feed is observed coordination, not a mutex — the note must
        # travel with every lane answer (reviewer minimum-test 5).
        self.assertIn("not a mutex", out)

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


class TestLaneSignInPrecedence(unittest.TestCase):
    """Regression: sign-in takes precedence over sign-out within the scan window.

    Real incident (IV, 2026-10-12): the lane parser reported a lane FREE while
    a validator was in flight, because the validator's sign-in comment cited
    the prior sign-out ("lane free — last sign-out ...") and the parser
    checked "sign-out" first.
    """

    def _run_lanes(self, alpha_comments):
        def fake_gh(method, path, body_file=None):
            if "/issues/1713/comments" in path:
                return True, alpha_comments
            if "/issues/1713" in path:
                return True, {"comments": len(alpha_comments)}
            return False, "unexpected"  # other lanes: UNKNOWN

        with patch.object(wm, "gh_api", side_effect=fake_gh):
            section = wm.build_lanes_section()
        return section["lanes"]["alpha"]

    def test_signout_then_signin_citing_signout_reports_occupied(self):
        """A sign-out followed by a later sign-in (that mentions the sign-out)
        must report the lane OCCUPIED — this is the exact defect case."""
        signout = {"body": "## SIGN-OUT 01:05Z\nPR is open, work complete.",
                   "created_at": "2026-10-12T01:04:39Z"}
        signin = {"body": "## [NAYA 5 — Lane Alpha | SIGN-IN 2026-10-12 01:12Z]\n"
                          "Lane free — last sign-out 01:04:39Z, verified via API.",
                  "created_at": "2026-10-12T01:12:25Z"}
        lane = self._run_lanes([signout, signin])
        self.assertEqual(lane["status"], "OK")
        self.assertEqual(lane["state"], "OCCUPIED")
        self.assertIn("SIGN-IN", lane["occupant"])
        self.assertEqual(lane["last_activity"], "2026-10-12T01:12:25Z")

    def test_plain_signout_still_reports_free(self):
        """Precedence change must not break the normal sign-out path."""
        signout = {"body": "## [NAYA BETA · KNOW | SIGN-OUT 2026-10-12 01:31Z] "
                           "merge-prep COMPLETE",
                   "created_at": "2026-10-12T01:31:00Z"}
        lane = self._run_lanes([signout])
        self.assertEqual(lane["status"], "OK")
        self.assertEqual(lane["state"], "FREE")

    def test_plain_signin_still_reports_occupied(self):
        signin = {"body": "## SIGN-IN 00:59Z\nOpening the PR.",
                  "created_at": "2026-10-12T00:59:00Z"}
        lane = self._run_lanes([signin])
        self.assertEqual(lane["status"], "OK")
        self.assertEqual(lane["state"], "OCCUPIED")
        self.assertEqual(lane["last_activity"], "2026-10-12T00:59:00Z")

    def test_no_signal_stays_unknown(self):
        lane = self._run_lanes([{"body": "just a note", "created_at": "2026-10-12T00:00:00Z"}])
        self.assertEqual(lane["status"], "OK")
        self.assertEqual(lane["state"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main(verbosity=2)


# ---------------------------------------------------------------------------
# P0 regression tests — independent source review (issue #1869, 2026-10-12)
#
# Each test below FAILS on the pre-fix code and PASSES on the fixed code.
# They prove the four false-confidence paths are closed behaviorally.
# ---------------------------------------------------------------------------


class TestP0F1StaleRefused(unittest.TestCase):
    """P0-F1: stale data must be REFUSED, not warned-and-answered.

    Falsifier from the review: seed cached prs status OK with a timestamp
    older than FRESHNESS_LIMITS, mock upstream 403, ask "ready to merge".
    Old code claimed a mergeable PR. Fixed code answers UNKNOWN/READ_MORE.
    """

    def _stale_model(self, section):
        import copy
        model = copy.deepcopy(make_fresh_model())
        model["sections"][section]["as_of_ts"] = time.time() - 3600  # stale
        return model

    def _run_query(self, model, question):
        import io
        from contextlib import redirect_stdout
        with patch.object(wm, "load_model", return_value=model):
            buf = io.StringIO()
            args = type("Args", (), {"question": question.split()})()
            rc = None
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
            return buf.getvalue(), rc

    def test_stale_prs_count_refused(self):
        out, rc = self._run_query(self._stale_model("prs"), "how many PRs are open?")
        self.assertIn("UNKNOWN", out)
        self.assertIn("READ_MORE", out)
        self.assertNotIn("open PRs:", out.replace("OBSERVED — ", "").replace("UNKNOWN", ""))
        self.assertEqual(rc, 2)

    def test_stale_prs_mergeable_refused(self):
        out, rc = self._run_query(self._stale_model("prs"), "what PRs are mergeable?")
        self.assertIn("UNKNOWN", out)
        self.assertNotIn("mergeable PRs:", out)
        self.assertEqual(rc, 2)

    def test_stale_tip_refused_with_historical_only(self):
        out, rc = self._run_query(self._stale_model("tip"), "what is the live tip?")
        self.assertIn("UNKNOWN", out)
        self.assertNotIn("Live tip:", out)
        # Last-known data may appear ONLY in a clearly HISTORICAL field.
        self.assertIn("HISTORICAL", out)
        self.assertEqual(rc, 2)

    def test_stale_lanes_refused(self):
        out, rc = self._run_query(self._stale_model("lanes"), "which lanes are free?")
        self.assertIn("UNKNOWN", out)
        self.assertNotIn("Lane states:", out)
        self.assertEqual(rc, 2)

    def test_fresh_data_still_answers(self):
        import io
        from contextlib import redirect_stdout
        model = make_fresh_model()
        with patch.object(wm, "load_model", return_value=model):
            buf = io.StringIO()
            args = type("Args", (), {"question": "how many PRs are open?".split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
        out = buf.getvalue()
        self.assertIn("OBSERVED", out)
        self.assertIn("#2410", out)
        self.assertEqual(rc, 0)


class TestP0F2MergeabilityEvidence(unittest.TestCase):
    """P0-F2: the PR LIST never knows `mergeable` (verified live by the
    reviewer). The model must never assert readiness from list data; only a
    per-PR detail fetch (/pulls/{n}) qualifies as evidence."""

    def _page(self, with_mergeable_field=False):
        prs = []
        for i in (1, 2):
            pr = {"number": 2400 + i, "title": f"PR {i}",
                  "head": {"sha": "abc", "ref": "b"},
                  "draft": False, "created_at": "",
                  "user": {"login": "x"}}
            if with_mergeable_field:
                pr["mergeable"] = True  # some proxies inject this; ignore it
            prs.append(pr)
        return prs

    def test_list_data_mergeable_never_claimed(self):
        # Even if a response smuggles a mergeable field, the builder must
        # not record it as a readiness claim.
        def fake_gh(method, path, body_file=None):
            import re
            m = re.search(r"[?&]page=(\d+)", path)
            return (True, self._page(with_mergeable_field=True)) if (m and int(m.group(1)) == 1) else (True, [])

        with patch.object(wm, "gh_api", side_effect=fake_gh):
            section = wm.build_prs_section()
        self.assertEqual(section["status"], "OK")
        for pr in section["prs"]:
            self.assertIsNone(pr["mergeable"])
            self.assertEqual(pr["mergeable_source"], "list-data-never-knows")

    def test_merge_check_verdict_from_detail(self):
        # A per-PR detail fetch returning mergeable=true is evidence.
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "OK", "count": 1,
                                           "prs": [{"number": 2410}],
                                           "as_of_ts": time.time()}}}

        def fake_gh(method, path, body_file=None):
            if "/pulls/2410" in path:
                return True, {"number": 2410, "title": "Consolidation",
                              "mergeable": True, "mergeable_state": "clean",
                              "head": {"sha": "8de2ac16"}}
            return False, "unexpected"

        with patch.object(wm, "load_model", return_value=fake_model), \
             patch.object(wm, "gh_api", side_effect=fake_gh):
            buf = io.StringIO()
            args = type("Args", (), {"question": "merge check #2410".split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
        out = buf.getvalue()
        self.assertIn("mergeability: TRUE", out)
        self.assertIn("NOT a", out)  # not-a-merge-authorization note
        self.assertEqual(rc, 0)

    def test_merge_check_null_is_unknown(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "OK", "count": 1,
                                           "prs": [{"number": 2410}],
                                           "as_of_ts": time.time()}}}

        def fake_gh(method, path, body_file=None):
            if "/pulls/2410" in path:
                return True, {"number": 2410, "title": "X",
                              "mergeable": None,
                              "head": {"sha": "abc"}}
            return False, "unexpected"

        with patch.object(wm, "load_model", return_value=fake_model), \
             patch.object(wm, "gh_api", side_effect=fake_gh):
            buf = io.StringIO()
            args = type("Args", (), {"question": "merge check #2410".split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
        out = buf.getvalue()
        self.assertIn("UNKNOWN", out)
        self.assertEqual(rc, 2)


class TestP0F3PartialPagination(unittest.TestCase):
    """P0-F3: a page-2 failure after first-page success must mark the
    section PARTIAL and refuse completeness claims (no totals, no
    'all PRs' language)."""

    def test_page2_failure_marks_partial(self):
        page1 = [{"number": i, "title": f"PR {i}", "head": {"sha": "abc", "ref": "b"},
                  "draft": False, "created_at": "", "user": {"login": "x"}}
                 for i in range(100)]

        def fake_gh(method, path, body_file=None):
            import re
            m = re.search(r"[?&]page=(\d+)", path)
            page = int(m.group(1)) if m else 1
            if page == 1:
                return True, page1
            return False, "403 on page 2"

        with patch.object(wm, "gh_api", side_effect=fake_gh):
            section = wm.build_prs_section()
        self.assertEqual(section["status"], "PARTIAL")
        self.assertEqual(section["fetch_failed_page"], 2)
        self.assertEqual(section["pr_count_lower_bound"], 100)
        self.assertNotIn("count", section)  # no exact total claim

    def test_partial_query_refuses_total(self):
        import io
        from contextlib import redirect_stdout
        fake_model = {"sections": {"prs": {"status": "PARTIAL",
                                           "reason": "API failed on page 2",
                                           "fetch_failed_page": 2,
                                           "pr_count_lower_bound": 100,
                                           "prs": [],
                                           "as_of_ts": time.time()}}}
        with patch.object(wm, "load_model", return_value=fake_model):
            buf = io.StringIO()
            args = type("Args", (), {"question": "how many PRs are open?".split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
        out = buf.getvalue()
        self.assertIn("PARTIAL", out)
        self.assertIn("At least 100", out)
        self.assertNotIn("100 open PRs:", out)
        self.assertEqual(rc, 2)

    def test_safety_cap_marks_partial(self):
        # 10 full pages then the cap — old code said OK + "truncated".
        def fake_gh(method, path, body_file=None):
            import re
            m = re.search(r"[?&]page=(\d+)", path)
            page = int(m.group(1)) if m else 1
            return True, [{"number": page * 100 + i, "title": "x",
                           "head": {"sha": "a", "ref": "b"}, "draft": False,
                           "created_at": "", "user": {"login": "u"}}
                          for i in range(100)]

        with patch.object(wm, "gh_api", side_effect=fake_gh):
            section = wm.build_prs_section()
        self.assertEqual(section["status"], "PARTIAL")
        self.assertTrue(section["truncated"])
        self.assertEqual(section["pr_count_lower_bound"], 1000)


class TestP0F4BriefingNotLaw(unittest.TestCase):
    """P0-F4: cached briefing headings are ORIENTATION, not law. Any output
    touching permission/authority/consent must live re-read authoritative
    state or carry an explicit 'cached — verify before acting' marker."""

    def test_laws_section_marked_orientation(self):
        section = wm.build_laws_section()
        if section.get("status") != "OK":
            self.skipTest("briefing file not present in this environment")
        self.assertEqual(section.get("source_kind"), "BRIEFING_ORIENTATION")
        self.assertFalse(section.get("permission_evidence"))
        self.assertIn("verify before acting", section.get("cached_note", ""))

    def _run_query(self, question):
        import io
        from contextlib import redirect_stdout
        model = make_fresh_model()
        with patch.object(wm, "load_model", return_value=model):
            buf = io.StringIO()
            args = type("Args", (), {"question": question.split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
            return buf.getvalue(), rc

    def test_permission_question_refuses_cached_answer(self):
        for q in ["am I allowed to merge this?",
                  "do I have permission to deploy?",
                  "can I delete the branch?"]:
            out, rc = self._run_query(q)
            self.assertIn("UNKNOWN", out, f"question: {q}")
            self.assertIn("cached", out.lower(), f"question: {q}")
            self.assertIn("permission", out.lower(), f"question: {q}")
            self.assertEqual(rc, 2, f"question: {q}")

    def test_law_listing_carries_cached_marker(self):
        out, rc = self._run_query("what are the standing laws?")
        self.assertIn("CACHED", out)
        self.assertIn("verify before acting", out)
        self.assertEqual(rc, 0)


# ---------------------------------------------------------------------------
# B-41 regression tests — mission-preview truncation false-completeness
# (bottleneck B-41, PR #2477 review comment 6128553449, 2026-10-12)
#
# Falsification test (reviewer's exact test): a mission whose priorities 6
# and 7 live beyond character 2000 of the issue body. Pre-fix the world
# model caches body[:2000] with no completeness marker, so a Board consumer
# can present its orientation as current while the decisive priorities are
# missing from the preview. These tests FAIL on the pre-fix code (no
# completeness metadata, OBSERVED answers from a partial preview) and PASS
# on the fixed code (MISSION_PRIORITIES_PARTIAL + fail-closed gate).
# ---------------------------------------------------------------------------


def _b41_long_mission_body():
    """Mission body with priorities 6 and 7 strictly beyond char 2000."""
    filler = "orientation boilerplate, milestones, and parked items. "
    header = "MISSION STATE — priorities of the team.\n"
    early = ("Priority 1: engine consolidation.\nPriority 2: ledger proof.\n"
             "Priority 3: hub currency.\nPriority 4: compass wiring.\n"
             "Priority 5: feed loop.\n")
    body = header + early
    while len(body) < 2200:
        body += filler
    body += ("\nPriority 6: symbolic layer — the decisive missing priority.\n"
             "Priority 7: smart connect — the second missing priority.\n")
    assert len(body) > 2000
    assert "Priority 6" not in body[:2000]
    assert "Priority 7" not in body[:2000]
    return body


def _b41_fresh_model(mission_section):
    import copy
    model = copy.deepcopy(make_fresh_model())
    model["sections"]["mission"] = mission_section
    return model


class TestB41MissionPreviewCompleteness(unittest.TestCase):
    """Builder tests: the cache layer itself must carry completeness."""

    def _build_section(self, body):
        def fake_gh(method, path, body_file=None):
            return True, {
                "title": "Mission State", "state": "open", "comments": 10,
                "updated_at": "2026-10-12T00:00:00Z",
                "body": body, "html_url": "https://github.com/x/issues/2154",
            }
        with patch.object(wm, "gh_api", side_effect=fake_gh):
            return wm.build_mission_section()

    def test_long_body_marked_partial(self):
        """A mission body over 2000 chars is visibly partial."""
        section = self._build_section(_b41_long_mission_body())
        self.assertEqual(section["status"], "OK")
        self.assertFalse(section["body_preview_complete"])
        self.assertEqual(section["preview_completeness"], "PARTIAL")
        self.assertGreater(section["body_chars_total"], 2000)
        self.assertEqual(section["body_preview_chars"], 2000)
        # The decisive priorities are missing from the cached preview.
        self.assertNotIn("Priority 6", section["body_preview"])
        self.assertNotIn("Priority 7", section["body_preview"])

    def test_short_body_marked_complete(self):
        section = self._build_section("Priority 1: only one, short.")
        self.assertTrue(section["body_preview_complete"])
        self.assertEqual(section["preview_completeness"], "COMPLETE")
        self.assertEqual(section["body_chars_total"],
                         section["body_preview_chars"])

    def test_exact_boundary_2000_is_complete(self):
        section = self._build_section("x" * 2000)
        self.assertTrue(section["body_preview_complete"])
        self.assertEqual(section["preview_completeness"], "COMPLETE")

    def test_boundary_2001_is_partial(self):
        section = self._build_section("x" * 2001)
        self.assertFalse(section["body_preview_complete"])
        self.assertEqual(section["preview_completeness"], "PARTIAL")

    def test_preview_limit_is_named(self):
        # The magic 2000 must be a named constant, not an inline literal.
        self.assertEqual(getattr(wm, "MISSION_PREVIEW_LIMIT", None), 2000)

    def test_api_failure_still_unknown(self):
        with patch.object(wm, "gh_api", return_value=(False, "boom")):
            section = wm.build_mission_section()
        self.assertEqual(section["status"], "UNKNOWN")


class TestB41Falsification(unittest.TestCase):
    """The exact falsification test from PR #2477 review 6128553449.

    RED-before: a mission with priorities 6/7 beyond char 2000 — the world
    model's mission section answers priority questions as OBSERVED from the
    truncated preview with no partial marker.
    GREEN-after: the same section is labeled MISSION_PRIORITIES_PARTIAL and
    any completeness-requiring question fails closed (UNKNOWN + READ_MORE).
    """

    def _run_query(self, model, question):
        import io
        from contextlib import redirect_stdout
        with patch.object(wm, "load_model", return_value=model):
            buf = io.StringIO()
            args = type("Args", (), {"question": question.split()})()
            with redirect_stdout(buf):
                rc = wm.cmd_query(args)
            return buf.getvalue(), rc

    def _partial_model(self):
        body = _b41_long_mission_body()
        now = time.time()
        return _b41_fresh_model({
            "status": "OK", "issue": 2154, "title": "Mission State",
            "state": "open", "comment_count": 10,
            "updated_at": "2026-10-12T00:00:00Z",
            "body_preview": body[:2000],
            "body_preview_chars": 2000,
            "body_chars_total": len(body),
            "body_preview_complete": False,
            "preview_completeness": "PARTIAL",
            "url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2154",
            "as_of_utc": "2026-10-12T00:00:00+00:00",
            "as_of_ts": now,
        })

    def test_falsifier_partial_preview_visibly_marked(self):
        """(a) partial preview is visibly marked partial in query output."""
        out, rc = self._run_query(self._partial_model(), "what is the mission state?")
        self.assertIn("MISSION_PRIORITIES_PARTIAL", out)
        self.assertIn("2000", out)  # char counts visible
        self.assertIn("PARTIAL PREVIEW", out)
        # The banner explicitly forbids treating it as complete.
        self.assertIn("do not treat it as", out.lower())
        self.assertIn("complete mission", out.lower())
        # Limited orientation still answers (fresh data), no fail-closed here.
        self.assertEqual(rc, 0)

    def test_falsifier_completeness_question_fails_closed(self):
        """(b) 'highest priority' from a partial preview → UNKNOWN + READ_MORE."""
        out, rc = self._run_query(self._partial_model(), "what is the highest priority?")
        self.assertIn("UNKNOWN", out)
        self.assertIn("MISSION_PRIORITIES_PARTIAL", out)
        self.assertIn("READ_MORE", out)
        self.assertEqual(rc, 2)

    def test_falsifier_complete_mission_still_answers(self):
        """Positive control: a complete preview answers priority questions."""
        model = make_fresh_model()
        m = model["sections"]["mission"]
        m.update({
            "body_preview": "Priority 1: engine consolidation",
            "body_preview_chars": 30,
            "body_chars_total": 30,
            "body_preview_complete": True,
            "preview_completeness": "COMPLETE",
        })
        out, rc = self._run_query(model, "what is the highest priority?")
        self.assertIn("OBSERVED", out)
        self.assertNotIn("MISSION_PRIORITIES_PARTIAL", out)
        self.assertEqual(rc, 0)

    def test_falsifier_legacy_snapshot_fails_closed(self):
        """Legacy snapshots (no completeness field) cannot prove completeness."""
        model = make_fresh_model()  # mission section lacks the B-41 fields
        out, rc = self._run_query(model, "what is the highest priority?")
        self.assertIn("UNKNOWN", out)
        self.assertIn("READ_MORE", out)
        self.assertEqual(rc, 2)

    def test_falsifier_adversarial_phrasings_fail_closed(self):
        """Regression: unseen priority phrasings must fail closed, not slip
        through intent detection to a positive answer from partial data.
        (Round-1 scorer adversarial probe: the intent detector is
        fail-closed-by-default — ANY mention of priorities routes through
        the gate.)"""
        for q in ["what are all the priorities?",
                  "list the priorities",
                  "give me every priority",
                  "what are the priorities?",
                  "rank the priorities",
                  "which priorities matter most?",
                  "is priority 6 on the list?",
                  "what is priority 7?"]:
            out, rc = self._run_query(self._partial_model(), q)
            self.assertIn("UNKNOWN", out, f"question: {q}")
            self.assertIn("READ_MORE", out, f"question: {q}")
            self.assertIn("MISSION_PRIORITIES_PARTIAL", out, f"question: {q}")
            self.assertEqual(rc, 2, f"question: {q}")

    def test_bare_orientation_still_answers_from_partial(self):
        """Bare orientation (no priority mention) still answers with the
        PARTIAL banner — only priority/completeness mentions fail closed."""
        for q in ["what is the mission state?",
                  "what are the blockers?",
                  "show me the mission"]:
            out, rc = self._run_query(self._partial_model(), q)
            self.assertIn("MISSION_PRIORITIES_PARTIAL", out, f"question: {q}")
            self.assertEqual(rc, 0, f"question: {q}")

    def test_complete_preview_answers_adversarial_phrasings(self):
        """Positive control: with a COMPLETE preview the same phrasings
        answer — fail-closed must not become fail-always."""
        model = make_fresh_model()
        m = model["sections"]["mission"]
        m.update({
            "body_preview": "Priority 1: engine consolidation",
            "body_preview_chars": 30,
            "body_chars_total": 30,
            "body_preview_complete": True,
            "preview_completeness": "COMPLETE",
        })
        out, rc = self._run_query(model, "what are all the priorities?")
        self.assertIn("OBSERVED", out)
        self.assertEqual(rc, 0)

    def test_gate_helper_fail_closed(self):
        """The module-level gate is the single fail-closed decision point."""
        ok, _ = wm.require_complete_mission(self._partial_model()["sections"])
        self.assertFalse(ok)
        model = make_fresh_model()
        m = model["sections"]["mission"]
        m.update({"body_preview_complete": True})
        ok, _ = wm.require_complete_mission(model["sections"])
        self.assertTrue(ok)
