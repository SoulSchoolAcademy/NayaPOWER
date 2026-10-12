#!/usr/bin/env python3
"""Tests for tools/option_miner.py — Layer 3 of the Ultimate Decision Machine.

The miner must never invent options: every test asserts that every returned
option is traceable to a fixture source (world model section or user text).
"""

import json
import os
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import option_miner as om


# ---------------------------------------------------------------------------
# Fixtures — a realistic cached world model (controlled, local, no network)
# ---------------------------------------------------------------------------

def fixture_model(as_of_ts=None):
    """A realistic cached world model (controlled, local, no network).

    Sections carry as_of_ts stamped fresh by default — Layer 1's freshness
    contract (status OK *and* age within FRESHNESS_LIMITS) requires it;
    without as_of_ts every section reads UNKNOWN and mining refuses.
    Pass as_of_ts explicitly to build stale/aged fixtures.
    """
    ts = time.time() if as_of_ts is None else as_of_ts
    utc = datetime.now(timezone.utc).isoformat()
    return {
        "version": 1,
        "created_utc": "2026-10-12T03:50:00+00:00",
        "sections": {
            "tip": {"status": "OK", "sha": "abc123def456",
                    "as_of_utc": utc, "as_of_ts": ts},
            "prs": {"status": "OK", "count": 5, "as_of_utc": utc, "as_of_ts": ts,
                     "prs": [
                         {"number": 2410, "title": "Consolidation: one decision engine",
                          "head_sha": "8de2ac16", "head_branch": "naya5/decision-engine-consolidation",
                          "mergeable": True, "draft": False,
                          "created_at": "2026-10-11T00:30:00Z"},
                         {"number": 2418, "title": "Consolidation: retire competing DecisionEngine",
                          "head_sha": "9f8e7d6c", "head_branch": "naya5/consolidation-alt",
                          "mergeable": True, "draft": False,
                          "created_at": "2026-10-12T01:00:00Z"},
                         {"number": 2407, "title": "Brain index re-stamp at tip",
                          "head_sha": "a1b2c3d4", "head_branch": "naya5/brain-index",
                          "mergeable": False, "draft": False,
                          "created_at": "2026-10-10T12:00:00Z"},
                         {"number": 2422, "title": "[DRAFT] World Model V1",
                          "head_sha": "8e336940", "head_branch": "naya5/world-model",
                          "mergeable": None, "draft": True,
                          "created_at": "2026-10-12T02:00:00Z"},
                         {"number": 2412, "title": "Auto decision calculator",
                          "head_sha": "51e99c0d", "head_branch": "naya5/auto-decision-calculator",
                          "mergeable": True, "draft": False,
                          "created_at": "2026-10-11T01:05:00Z"},
                     ]},
            "lanes": {"status": "OK", "as_of_utc": utc, "as_of_ts": ts,
                      "lanes": {"alpha": {"state": "FREE"},
                                "beta": {"state": "OCCUPIED"},
                                "gamma": {"state": "FREE"}}},
            "mission": {"status": "OK", "as_of_utc": utc, "as_of_ts": ts,
                        "priorities": ["Close the merge queue", "Validate layer 2"]},
        },
    }


def run_mine(intent, model, user_options=None, todo_items=None, warnings=None):
    """Run mine_options with the world-model loader patched to a fixture."""
    if warnings is None:
        warnings = []
    with mock.patch.object(om, "load_world_model", return_value=(model, warnings)), \
         mock.patch.object(om, "load_grand_todo", return_value=(todo_items or [], [])):
        return om.mine_options(intent, user_options=user_options)


def warnings_for(model):
    """Compute the age-aware warnings load_world_model would produce."""
    sections = model.get("sections", {})
    out = []
    for name in sections:
        usable, state = om.section_usable(name, sections)
        if not usable:
            out.append(f"world model section '{name}' is {state} — too stale")
    return out


# ---------------------------------------------------------------------------
# Intent helpers
# ---------------------------------------------------------------------------

def intent_what_next():
    return {"ok": True, "exit_hint": 0, "intent_type": "what_next",
            "objective": "Identify the single highest-value action available right now",
            "references": {}, "grounded_references": {"prs": []},
            "constraints": [], "decision_weight": "standard"}


def intent_should_merge():
    return {"ok": True, "exit_hint": 0, "intent_type": "should_merge",
            "objective": "Determine whether the change is safe and ready to merge — specifically: PR #2410",
            "references": {"pr_numbers": [2410]},
            "grounded_references": {"prs": [
                {"number": 2410, "title": "Consolidation: one decision engine",
                 "mergeable": True, "found": True}]},
            "constraints": [], "decision_weight": "standard"}


def intent_which_option():
    return {"ok": True, "exit_hint": 0, "intent_type": "which_option",
            "objective": "Rank the given options and recommend the best one",
            "references": {"pr_numbers": [2410, 2418]},
            "grounded_references": {"prs": [
                {"number": 2410, "title": "Consolidation: one decision engine", "found": True},
                {"number": 2418, "title": "Consolidation: retire competing DecisionEngine", "found": True}]},
            "constraints": [], "decision_weight": "standard"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestWhatNext(unittest.TestCase):
    def test_mines_mergeable_prs(self):
        r = run_mine(intent_what_next(), fixture_model())
        self.assertEqual(r["exit_hint"], 0)
        pr_ids = [o["id"] for o in r["options"] if o["source_type"] == "pr"]
        # 2410, 2418, 2412 mergeable; 2407 not mergeable but still an option
        self.assertIn("pr-2410", pr_ids)
        self.assertIn("pr-2412", pr_ids)
        # Drafts are NOT next-action options
        self.assertNotIn("pr-2422", pr_ids)

    def test_mines_free_lanes(self):
        r = run_mine(intent_what_next(), fixture_model())
        lane_opts = [o for o in r["options"] if o["source_type"] == "lane"]
        sources = [o["source"] for o in lane_opts]
        self.assertIn("lane alpha", sources)
        self.assertIn("lane gamma", sources)
        self.assertNotIn("lane beta", sources)  # occupied

    def test_no_invented_options(self):
        r = run_mine(intent_what_next(), fixture_model())
        known_prs = {2410, 2418, 2407, 2412}
        for o in r["options"]:
            if o["source_type"] == "pr":
                num = int(o["source"].split("#")[1])
                self.assertIn(num, known_prs, f"invented option: {o['source']}")
            # Every option must cite a source
            self.assertTrue(o["source"], f"option without source: {o['id']}")
            self.assertTrue(o["evidence_links"], f"option without evidence: {o['id']}")

    def test_mines_todo_items(self):
        todos = [{"title": "Fix the parser", "file": "x.md", "line": 42}]
        r = run_mine(intent_what_next(), fixture_model(), todo_items=todos)
        todo_opts = [o for o in r["options"] if o["source_type"] == "todo"]
        self.assertEqual(len(todo_opts), 1)
        self.assertEqual(todo_opts[0]["source"], "grand-todo line 42")


class TestShouldMerge(unittest.TestCase):
    def test_primary_is_referenced_pr(self):
        r = run_mine(intent_should_merge(), fixture_model())
        self.assertEqual(r["exit_hint"], 0)
        self.assertEqual(r["options"][0]["id"], "merge-pr-2410")
        self.assertIn("#2410", r["options"][0]["title"])

    def test_competing_candidates_included(self):
        r = run_mine(intent_should_merge(), fixture_model())
        ids = [o["id"] for o in r["options"]]
        self.assertIn("pr-2418", ids)   # mergeable competitor
        self.assertIn("pr-2412", ids)   # mergeable competitor
        self.assertNotIn("pr-2407", ids)  # not mergeable → not a candidate

    def test_stale_cache_note(self):
        intent = intent_should_merge()
        intent["grounded_references"]["prs"].append(
            {"number": 9999, "found": True})
        r = run_mine(intent, fixture_model())
        self.assertTrue(any("9999" in n and "stale" in n for n in r["notes"]))


class TestWhichOption(unittest.TestCase):
    def test_both_grounded_options_present(self):
        r = run_mine(intent_which_option(), fixture_model())
        ids = [o["id"] for o in r["options"]]
        self.assertIn("opt-pr-2410", ids)
        self.assertIn("opt-pr-2418", ids)

    def test_single_option_warns(self):
        intent = intent_which_option()
        intent["grounded_references"]["prs"] = intent["grounded_references"]["prs"][:1]
        r = run_mine(intent, fixture_model())
        self.assertTrue(any("Fewer than two" in n for n in r["notes"]))

    def test_quoted_options_flagged(self):
        intent = intent_which_option()
        intent["references"]["quoted_options"] = ["minimal", "full"]
        r = run_mine(intent, fixture_model())
        quoted = [o for o in r["options"] if o["source"] == "the question text"]
        self.assertEqual(len(quoted), 2)
        self.assertEqual(quoted[0]["source_type"], "user_added")
        self.assertIsNone(quoted[0]["relevance"])

    def test_numeric_lane_keys_normalized(self):
        model = fixture_model()
        model["sections"]["lanes"]["lanes"] = {
            "1713": {"state": "FREE", "issue": 1713, "occupant": ""},
            "1714": {"state": "OCCUPIED", "issue": 1714, "occupant": "worker x"},
        }
        r = run_mine(intent_what_next(), model)
        lanes = {o["source"]: o for o in r["options"] if o["source_type"] == "lane"}
        self.assertIn("lane alpha", lanes)
        self.assertIn("issues/1713", lanes["lane alpha"]["evidence_links"][0])
        # Occupant shows up in the why for blocking intents
        r2 = run_mine({"ok": True, "intent_type": "what_blocking", "references": {},
                       "grounded_references": {"prs": []}}, model)
        occ = [o for o in r2["options"] if o["source"] == "lane beta"]
        self.assertIn("worker x", occ[0]["why"])

    def test_empty_add_option_filtered(self):
        r = run_mine(intent_what_next(), fixture_model(),
                     user_options=["", "  "])
        user_opts = [o for o in r["options"] if o["source_type"] == "user_added"]
        self.assertEqual(user_opts, [])


class TestWhatBlocking(unittest.TestCase):
    def test_mines_stuck_prs(self):
        intent = {"ok": True, "intent_type": "what_blocking", "references": {},
                  "grounded_references": {"prs": []}}
        r = run_mine(intent, fixture_model())
        ids = [o["id"] for o in r["options"]]
        self.assertIn("unblock-pr-2407", ids)  # mergeable False
        self.assertIn("unblock-pr-2422", ids)  # draft
        self.assertNotIn("unblock-pr-2410", ids)  # mergeable, not blocked

    def test_occupied_lanes_included(self):
        intent = {"ok": True, "intent_type": "what_blocking", "references": {},
                  "grounded_references": {"prs": []}}
        r = run_mine(intent, fixture_model())
        lanes = [o["source"] for o in r["options"] if o["source_type"] == "lane"]
        self.assertIn("lane beta", lanes)


class TestHonesty(unittest.TestCase):
    def test_status_check_returns_no_options(self):
        intent = {"ok": True, "intent_type": "status_check", "references": {},
                  "grounded_references": {"prs": []}}
        r = run_mine(intent, fixture_model())
        self.assertEqual(r["exit_hint"], 0)
        self.assertEqual(r["options"], [])
        self.assertTrue(any("no options" in n for n in r["notes"]))

    def test_should_build_refuses_to_invent(self):
        intent = {"ok": True, "intent_type": "should_build", "references": {},
                  "grounded_references": {"prs": []}}
        r = run_mine(intent, fixture_model())
        self.assertEqual(r["options"], [])
        self.assertTrue(any("no code-inventory" in n for n in r["notes"]))

    def test_missing_cache_exit_2(self):
        with mock.patch.object(om, "load_world_model", return_value=(None, ["missing"])):
            r = om.mine_options(intent_what_next())
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])
        self.assertTrue(any("snapshot" in n for n in r["notes"]))

    def test_bad_intent_exit_2(self):
        r = run_mine({"ok": False, "clarifying_questions": ["which PR?"]}, fixture_model())
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])

    def test_unknown_intent_type_exit_2(self):
        intent = {"ok": True, "intent_type": "teleport", "references": {},
                  "grounded_references": {"prs": []}}
        r = run_mine(intent, fixture_model())
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])

    def test_stale_section_warns(self):
        # Honest path: write a temp world model with a STALE section and let
        # the REAL loader produce the warning (the mock bypasses it).
        import tempfile
        model = fixture_model()
        model["sections"]["prs"]["status"] = "STALE"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(model, f)
            tmp = f.name
        try:
            with mock.patch.object(om, "WORLD_MODEL_PATH", Path(tmp)), \
                 mock.patch.object(om, "load_grand_todo", return_value=([], [])):
                r = om.mine_options(intent_what_next())
        finally:
            os.unlink(tmp)
        self.assertTrue(any("STALE" in w for w in r["warnings"]))
        # Stale NEEDED section refuses the run — UNKNOWN + READ_MORE,
        # exit 2. Mining a partial option set with a warning footnote is
        # the false-confidence failure P0-F1 forbids.
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])
        self.assertTrue(any("UNKNOWN" in n for n in r["notes"]))
        self.assertTrue(any("READ_MORE" in n for n in r["notes"]))

    def test_stale_tip_warns(self):
        model = fixture_model()
        model["sections"]["tip"]["status"] = "STALE"
        r = run_mine(intent_what_next(), model)
        self.assertTrue(any("tip is STALE" in w for w in r["warnings"]))

    def test_missing_mission_section_honest(self):
        model = fixture_model()
        del model["sections"]["mission"]
        r = run_mine(intent_what_next(), model)
        # Missing NEEDED section refuses — UNKNOWN + READ_MORE, exit 2.
        # A "mission options unavailable" footnote on a mined set would be
        # a positive answer from incomplete data.
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])
        self.assertTrue(any("UNKNOWN" in n and "mission" in n
                            for n in r["notes"]))
        self.assertTrue(any("READ_MORE" in n for n in r["notes"]))


class TestDuplicates(unittest.TestCase):
    def test_same_branch_deduped(self):
        model = fixture_model()
        model["sections"]["prs"]["prs"][1]["head_branch"] = "naya5/decision-engine-consolidation"
        r = run_mine(intent_which_option(), model)
        ids = [o["id"] for o in r["options"] if o["source_type"] == "pr"]
        self.assertEqual(len(ids), 1)
        self.assertEqual(ids[0], "opt-pr-2410")  # older = primary
        self.assertTrue(any("Duplicate" in n for n in r["notes"]))

    def test_same_title_deduped(self):
        model = fixture_model()
        prs = model["sections"]["prs"]["prs"]
        prs[1]["head_branch"] = "naya5/other"
        prs[1]["title"] = "Consolidation: one decision engine"
        r = run_mine(intent_which_option(), model)
        ids = [o["id"] for o in r["options"] if o["source_type"] == "pr"]
        self.assertEqual(len(ids), 1)

    def test_different_work_not_deduped(self):
        r = run_mine(intent_which_option(), fixture_model())
        ids = [o["id"] for o in r["options"] if o["source_type"] == "pr"]
        self.assertEqual(len(ids), 2)


class TestUserAdded(unittest.TestCase):
    def test_user_options_flagged(self):
        r = run_mine(intent_what_next(), fixture_model(),
                     user_options=["what about rewriting everything?"])
        user_opts = [o for o in r["options"] if o["source_type"] == "user_added"]
        self.assertEqual(len(user_opts), 1)
        self.assertIsNone(user_opts[0]["relevance"])
        self.assertTrue(any("user_added" in n for n in r["notes"]))

    def test_user_options_survive_dedupe(self):
        model = fixture_model()
        model["sections"]["prs"]["prs"][1]["head_branch"] = "naya5/decision-engine-consolidation"
        r = run_mine(intent_which_option(), model,
                     user_options=["what about a third engine?"])
        user_opts = [o for o in r["options"] if o["source_type"] == "user_added"]
        self.assertEqual(len(user_opts), 1)


class TestFreshnessSeam(unittest.TestCase):
    """The L1→L3 freshness seam: the miner reads the SAME cache file Layer 1
    refuses to answer from when stale. A section whose status is "OK" but
    whose as_of_ts is older than Layer 1's FRESHNESS_LIMITS is STALE — the
    miner must refuse (UNKNOWN + READ_MORE, exit 2), never mine confidently
    from stale bytes. That confident mining is the exact false-confidence
    failure Layer 1's P0-F1 was built to kill."""

    def aged_model(self, section_name, age_seconds, status="OK"):
        m = fixture_model()
        sec = m["sections"][section_name]
        sec["as_of_ts"] = time.time() - age_seconds
        sec["status"] = status
        return m

    def test_stale_prs_refuses(self):
        # 3h-aged prs (limit 600s): the rehearsal's exact defect.
        r = run_mine(intent_what_next(), self.aged_model("prs", 3 * 3600))
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)
        self.assertEqual(r["options"], [])
        notes = "\n".join(r["notes"])
        self.assertIn("UNKNOWN", notes)
        self.assertIn("READ_MORE", notes)
        self.assertIn("prs", notes)

    def test_stale_lanes_refuses_what_blocking(self):
        r = run_mine(
            {"ok": True, "intent_type": "what_blocking", "references": {},
             "grounded_references": {"prs": []}},
            self.aged_model("lanes", 3600))
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)
        self.assertIn("lanes", "\n".join(r["notes"]))

    def test_stale_mission_refuses_what_next(self):
        r = run_mine(intent_what_next(), self.aged_model("mission", 7200))
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)

    def test_should_merge_needs_only_prs(self):
        # lanes stale but prs fresh: should_merge doesn't mine lanes,
        # so it proceeds (with a loud warning, not a refusal).
        m = self.aged_model("lanes", 3600)
        r = run_mine(intent_should_merge(), m, warnings=warnings_for(m))
        self.assertEqual(r["exit_hint"], 0)
        self.assertTrue(any("lanes" in w and "STALE" in w
                            for w in r["warnings"]))

    def test_ttl_boundary(self):
        # prs limit is 600s: 590s old mines, 610s old refuses.
        r_fresh = run_mine(intent_what_next(), self.aged_model("prs", 590))
        self.assertEqual(r_fresh["exit_hint"], 0, r_fresh["notes"])
        r_stale = run_mine(intent_what_next(), self.aged_model("prs", 610))
        self.assertEqual(r_stale["exit_hint"], 2)

    def test_partial_prs_refuses(self):
        m = self.aged_model("prs", 0, status="PARTIAL")
        m["sections"]["prs"]["pr_count_lower_bound"] = 100
        r = run_mine(intent_should_merge(), m)
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)
        self.assertIn("PARTIAL", "\n".join(r["notes"]))

    def test_missing_section_refuses(self):
        m = fixture_model()
        del m["sections"]["prs"]
        r = run_mine(intent_should_merge(), m)
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)
        self.assertIn("UNKNOWN", "\n".join(r["notes"]))

    def test_section_without_timestamp_refuses(self):
        # as_of_ts missing entirely: Layer 1 reads it as UNKNOWN.
        m = fixture_model()
        del m["sections"]["prs"]["as_of_ts"]
        r = run_mine(intent_should_merge(), m)
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)

    def test_unneeded_stale_section_warns_not_refuses(self):
        # ledger is not mined by what_next: stale ledger warns loudly,
        # mining proceeds from the fresh needed sections.
        m = fixture_model()
        m["sections"]["ledger"] = {"status": "OK",
                                   "as_of_ts": time.time() - 7200}
        r = run_mine(intent_what_next(), m, warnings=warnings_for(m))
        self.assertEqual(r["exit_hint"], 0)
        self.assertTrue(any("ledger" in w and "STALE" in w
                            for w in r["warnings"]))

    def test_stale_tip_warns_not_refuses(self):
        m = self.aged_model("tip", 3600)
        r = run_mine(intent_what_next(), m, warnings=warnings_for(m))
        self.assertEqual(r["exit_hint"], 0)
        self.assertTrue(any("tip" in w and "STALE" in w
                            for w in r["warnings"]))

    def test_fresh_fixture_mines_normally(self):
        r = run_mine(intent_what_next(), fixture_model())
        self.assertEqual(r["exit_hint"], 0)
        self.assertTrue(r["options"])

    def test_ttl_agreement_with_layer1(self):
        # The miner must never disagree with Layer 1 about "stale".
        from world_model import FRESHNESS_LIMITS as L1_LIMITS
        from world_model import section_usable as l1_usable
        self.assertEqual(om.FRESHNESS_LIMITS, L1_LIMITS)
        now = time.time()
        for name, limit in L1_LIMITS.items():
            sections = {name: {"status": "OK", "as_of_ts": now - limit - 1}}
            self.assertEqual(l1_usable(name, sections), (False, "STALE"))
            mine_usable, _ = om.section_usable(name, sections)
            self.assertFalse(mine_usable, f"miner disagrees with L1 on {name}")
            sections[name]["as_of_ts"] = now
            self.assertEqual(l1_usable(name, sections), (True, "FRESH"))

    def test_cli_stale_cache_exit_2(self):
        # End-to-end through the real CLI: a 3h-stale cache on disk
        # refuses with exit 2 and UNKNOWN + READ_MORE, never options.
        import subprocess
        import tempfile
        tmp = tempfile.TemporaryDirectory()
        home = Path(tmp.name)
        (home / ".naya").mkdir()
        (home / ".naya" / "world-model.json").write_text(
            json.dumps(fixture_model(as_of_ts=time.time() - 3 * 3600)))
        script = str(Path(__file__).resolve().parents[1]
                     / "tools" / "option_miner.py")
        env = dict(os.environ, HOME=str(home))
        try:
            p = subprocess.run(
                [sys.executable, script, "mine", "--intent",
                 json.dumps(intent_what_next())],
                capture_output=True, text=True, env=env)
            self.assertEqual(p.returncode, 2, p.stderr)
            r = json.loads(p.stdout)
            self.assertFalse(r["ok"])
            self.assertEqual(r["options"], [])
            notes = "\n".join(r["notes"])
            self.assertIn("UNKNOWN", notes)
            self.assertIn("READ_MORE", notes)
        finally:
            tmp.cleanup()

    def test_cli_fresh_cache_exit_0(self):
        import subprocess
        import tempfile
        tmp = tempfile.TemporaryDirectory()
        home = Path(tmp.name)
        (home / ".naya").mkdir()
        (home / ".naya" / "world-model.json").write_text(
            json.dumps(fixture_model()))
        script = str(Path(__file__).resolve().parents[1]
                     / "tools" / "option_miner.py")
        env = dict(os.environ, HOME=str(home))
        try:
            p = subprocess.run(
                [sys.executable, script, "mine", "--intent",
                 json.dumps(intent_what_next())],
                capture_output=True, text=True, env=env)
            self.assertEqual(p.returncode, 0, p.stderr)
            r = json.loads(p.stdout)
            self.assertTrue(r["ok"])
            self.assertTrue(r["options"])
        finally:
            tmp.cleanup()


class TestCLI(unittest.TestCase):
    """Regression tests for every documented CLI form.

    F1 lesson: the builder's tests never touched the CLI, so the documented
    `mine --intent '<json>'` form died with argparse's "unrecognized
    arguments". Every documented form gets a subprocess test here.
    """

    def test_plain_words_renders_mined_options(self):
        # (Was the old "test_cli_end_to_end": it never touched the CLI.
        # Kept as a plain-words rendering check; real CLI coverage is below.)
        with mock.patch.object(om, "load_world_model",
                               return_value=(fixture_model(), [])), \
             mock.patch.object(om, "load_grand_todo", return_value=([], [])):
            r = om.mine_options(intent_what_next())
        out = om.plain_words(r)
        self.assertIn("Mined", out)
        self.assertIn("[pr-2410]", out)

    def setUp(self):
        import tempfile, subprocess  # noqa: F401 (used by helpers)
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        (self.home / ".naya").mkdir()
        (self.home / ".naya" / "world-model.json").write_text(
            json.dumps(fixture_model()))
        self.script = str(Path(__file__).resolve().parents[1]
                          / "tools" / "option_miner.py")
        self.env = dict(os.environ, HOME=str(self.home))

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *argv, stdin_text=None):
        import subprocess
        p = subprocess.run(
            [sys.executable, self.script, *argv],
            input=stdin_text, capture_output=True, text=True, env=self.env)
        return p

    def intent(self):
        return json.dumps(intent_what_next())

    def test_documented_intent_flag_form(self):
        p = self.run_cli("mine", "--intent", self.intent())
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertTrue(r["ok"])
        self.assertTrue(all(o["source"] for o in r["options"]))

    def test_positional_form(self):
        p = self.run_cli("mine", self.intent())
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertTrue(r["ok"])

    def test_stdin_form(self):
        p = self.run_cli("mine", "--stdin", stdin_text=self.intent())
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertTrue(r["ok"])

    def test_all_three_forms_agree(self):
        outs = []
        outs.append(self.run_cli("mine", "--intent", self.intent()).stdout)
        outs.append(self.run_cli("mine", self.intent()).stdout)
        outs.append(self.run_cli("mine", "--stdin",
                                 stdin_text=self.intent()).stdout)
        ids = [sorted(o["id"] for o in json.loads(o)["options"]) for o in outs]
        self.assertEqual(ids[0], ids[1])
        self.assertEqual(ids[1], ids[2])

    def test_intent_flag_wins_over_positional(self):
        p = self.run_cli("mine", "--intent", self.intent(),
                         json.dumps(intent_should_merge()))
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertEqual(r["intent_type"], "what_next")

    def test_add_option_via_cli(self):
        p = self.run_cli("mine", "--intent", self.intent(),
                         "--add-option", "what about a merge queue?")
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        user_opts = [o for o in r["options"]
                     if o.get("source_type") == "user_added"]
        self.assertEqual(len(user_opts), 1)
        self.assertIn("merge queue", user_opts[0]["title"])

    def test_plain_flag_via_cli(self):
        p = self.run_cli("mine", "--intent", self.intent(), "--plain")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Mined", p.stdout)

    def test_bad_json_exit_2(self):
        p = self.run_cli("mine", "--intent", "this is not json")
        self.assertEqual(p.returncode, 2)
        r = json.loads(p.stdout)
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_hint"], 2)

    def test_non_object_intent_exit_2(self):
        # Valid JSON but not an intent object: fail closed, never traceback.
        for raw in ('[1, 2]', '"hello"', '42'):
            p = self.run_cli("mine", "--intent", raw)
            self.assertEqual(p.returncode, 2, raw)
            self.assertNotIn("Traceback", p.stderr, raw)
            r = json.loads(p.stdout)
            self.assertFalse(r["ok"])
            self.assertEqual(r["exit_hint"], 2)

    def test_stdin_wins_over_intent_flag(self):
        p = self.run_cli("mine", "--stdin", "--intent", self.intent(),
                         stdin_text=json.dumps(intent_should_merge()))
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertEqual(r["intent_type"], "should_merge")

    def test_no_intent_exit_1(self):
        p = self.run_cli("mine")
        self.assertEqual(p.returncode, 1)

    def test_missing_cache_exit_2(self):
        import tempfile
        bare = tempfile.TemporaryDirectory()
        env = dict(os.environ, HOME=bare.name)
        import subprocess
        p = subprocess.run([sys.executable, self.script, "mine", "--intent",
                            self.intent()],
                           capture_output=True, text=True, env=env)
        bare.cleanup()
        self.assertEqual(p.returncode, 2)
        r = json.loads(p.stdout)
        self.assertFalse(r["ok"])
        self.assertTrue(any("world model" in n.lower()
                            for n in r.get("notes", [])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
