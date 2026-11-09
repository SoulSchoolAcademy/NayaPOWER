#!/usr/bin/env python3
"""Standing regression battery for spawn_brief.py's brief-generation guards.

Mu w309 shipped the stale-LIVE-premise guard (gr-w307-mu-briefpremise:
--thinking must never declare a closed/expired area-list item LIVE —
fail-closed exit 2, zero stdout). Mu w312 replaced its coarse
sentence-window matching with token-proximity matching (gr-w309-mu-gapclose,
_PROX_N=32) and ran this battery 8/8 + poison smoke before shipping.

This wave (gr-w312-mu-gapclose) persists the battery as a file beside
spawn_brief.py so the guard cannot regress silently: any future edit that
weakens the guard fails LOUDLY here, in the local dispatcher path, instead
of quietly shipping dead-premise briefs to workers. The battery already
paid for itself on first run: it caught a live false-negative (sentence-
final "live." evaded the liveness fullmatch), fixed in spawn_brief.py the
same wave — see test_sentence_final_liveness_kill.

Every expectation below is pinned to a VERIFIED behavior, never invented
(Mu w312 miss law: battery expectations come from the old guard's verified
verdicts). Calibrated distances come from the w312 calibration note in
spawn_brief.py: w305 kill-shape at 3 tokens, cross-sentence catch at 7,
distant co-occurrence (18+) still passes.

Run:  python3 test_spawn_brief_guards.py
Stdlib only, zero API, deterministic unit cases (~instant). The two
end-to-end smokes shell out to the REAL generator and skip honestly if the
lane is unclaimed in the truth file (a brief on an unclaimed lane is a lie —
the generator itself dies there).
"""

import datetime
import importlib.util as _ilu
import json
import os
import subprocess
import sys
import unittest

BIN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BIN)
_spec = _ilu.spec_from_file_location("spawn_brief",
                                      os.path.join(BIN, "spawn_brief.py"))
_sb = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_sb)

# The w305 kill-shape item: briefed as live when it was closed w302.
# Any live-assertion of a done/closed/expired item with this n-id must die.
CLOSED_ID = "gr-w299-mu-note2-reexecute"


def _current_month():
    """Budget fixtures must name the CURRENT month: quota_throttle_decision
    compares the budget month against datetime.now(timezone.utc) %Y-%m, so
    a hardcoded month goes stale the month after it is written (w2896:
    "2026-10" fixtures failed in 2026-11 with 'budget month != current').
    Derive it exactly the way the code under test does."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m")


def _doc(items_extra=()):
    items = [
        {"n": CLOSED_ID, "status": "done",
         "item": "RE-EXECUTE ORDER (the w305 brief premise)",
         "closed_utc": "2026-10-16T13:01:02Z"},
        {"n": "gr-w312-mu-gapclose", "status": "open",
         "item": "persist the guard battery as a test file"},
    ]
    items.extend(items_extra)
    return {"area": "HUMAN_VALUE", "items": items}


def _token_distance(thinking):
    """Min token distance between the closed id and any liveness word.

    Mirrors the guard's matching semantics (sentence-final periods stripped)
    so the calibration assertions test the same token stream the guard sees.
    """
    toks = _sb._TOKEN_RE.findall(thinking)
    lows = [t.lower().rstrip(".") for t in toks]
    live = [i for i, t in enumerate(lows) if _sb._LIVE_WORDS.fullmatch(t)]
    ids = [i for i, t in enumerate(lows) if CLOSED_ID in t]
    return min((abs(a - b) for a in live for b in ids), default=None)


class TestProximityCalibration(unittest.TestCase):
    """The w312 calibration constant must not drift silently."""

    def test_prox_n_is_32(self):
        # N=32 rests on the w312 calibration (kill-shape at 3, cross-sentence
        # catch at 7, distant 18+ passes). A change here is a RECALIBRATION,
        # never a tweak — it must come with a new battery run, so it fails
        # loudly instead of drifting.
        self.assertEqual(_sb._PROX_N, 32)


class TestPreservedW309Behaviors(unittest.TestCase):
    """The 3 behaviors the w309 sentence-window guard verified. Never lost."""

    def test_w305_kill_shape_3_tokens(self):
        # The w305 failure: --thinking asserted a closed item live.
        # Calibrated distance: 3 tokens. MUST fail closed.
        th = "Re-run gr-w299-mu-note2-reexecute is now live today"
        self.assertEqual(_token_distance(th), 3)
        findings = _sb.thinking_live_premise_findings(th, _doc())
        self.assertTrue(findings, "w305 kill-shape at 3 tokens must be killed")
        self.assertEqual(findings[0][0], CLOSED_ID)

    def test_legitimate_closed_mention_passes(self):
        # "do not re-run X — it closed w302" keeps the WARNING path (the
        # Theta w250 stale-rec guard), never the fail-closed kill.
        th = "do not re-run gr-w299-mu-note2-reexecute - it closed w302"
        self.assertEqual(_sb.thinking_live_premise_findings(th, _doc()), [])

    def test_benign_brief_passes(self):
        # No liveness assertion, no closed id liveness — unaffected.
        th = "work the top items, focus on gr-w312-mu-gapclose this wave"
        self.assertEqual(_sb.thinking_live_premise_findings(th, _doc()), [])


class TestNewFalseNegativeCatches(unittest.TestCase):
    """The 5 shapes the old sentence-window guard MISSED (false negatives)
    that token-proximity matching catches. This is the w312 upgrade."""

    def test_cross_sentence_kill_7_tokens(self):
        # Id in sentence one, live-word in sentence two — the old splitter
        # never saw them together. Calibrated distance: 7 tokens.
        th = "Run gr-w299-mu-note2-reexecute first today. Then please mark it live now"
        self.assertEqual(_token_distance(th), 7)
        findings = _sb.thinking_live_premise_findings(th, _doc())
        self.assertTrue(findings, "cross-sentence live-assertion at 7 must be killed")
        self.assertEqual(findings[0][0], CLOSED_ID)

    def test_sentence_final_liveness_kill(self):
        # Mu w313: the battery CAUGHT this — the tokenizer glues a
        # sentence-final period onto the token ("live."), which used to
        # defeat the liveness fullmatch. A live-assertion at end of
        # sentence is still an assertion. Regression test for the fix.
        th = "Re-run gr-w299-mu-note2-reexecute is now live."
        self.assertEqual(_token_distance(th), 3)
        findings = _sb.thinking_live_premise_findings(th, _doc())
        self.assertTrue(findings,
                        "sentence-final live-assertion must be killed")
        self.assertEqual(findings[0][0], CLOSED_ID)

    def test_reversed_order_kill(self):
        # Liveness word BEFORE the id — order must not matter.
        th = "the live gr-w299-mu-note2-reexecute item goes first"
        self.assertEqual(_token_distance(th), 1)
        self.assertTrue(_sb.thinking_live_premise_findings(th, _doc()))

    def test_fresh_variant_kill(self):
        # "fresh" is a liveness word; a split-broken window still kills.
        th = "Treat gr-w299-mu-note2-reexecute as fresh; it stays top"
        self.assertEqual(_token_distance(th), 2)
        self.assertTrue(_sb.thinking_live_premise_findings(th, _doc()))

    def test_distant_cooccurrence_passes(self):
        # Same closed id and a liveness word, but beyond the window:
        # co-occurrence is not assertion. 18+ tokens still passes.
        th = ("gr-w299-mu-note2-reexecute was briefed once before; meanwhile "
              "the queue grew across many other lanes and seats and waves and "
              "boards and feeds and pulses and receipts and notes and lessons "
              "and checks and scans and gates and lanes and feeds and pulses "
              "and now the live plan changed")
        d = _token_distance(th)
        self.assertGreater(d, _sb._PROX_N,
                           "control case must sit beyond the window")
        self.assertEqual(_sb.thinking_live_premise_findings(th, _doc()), [])

    def test_negation_exemption_passes(self):
        # Negation inside the window keeps the exemption semantics.
        th = "gr-w299-mu-note2-reexecute is not live; skip it"
        self.assertEqual(_token_distance(th), 3)
        self.assertEqual(_sb.thinking_live_premise_findings(th, _doc()), [])


class TestStemRefRegression(unittest.TestCase):
    """Gamma w2882 (gr-w2883-gamma-gapclose): TIER 1 stem match.

    Recommendations reference items by wave-stem ("gr-w2873"), not by
    full id ("gr-w2873-gamma-gapclose"). The full-id-only check missed
    the w2877/w2882 recs even though the item was status=done, so the
    brief quoted a stale recommendation as live. The stem match fires
    on the token-bounded stem; a longer id sharing the prefix must not.
    """

    def _stem_doc(self):
        return {
            "area": "ACT",
            "seat": "Naya Gamma",
            "last_recommendation":
                "next Gamma takes gr-w2873 first only after a fresh "
                "director ruling naming it is re-read live in #2601",
            "items": [
                {"n": "gr-w2873-gamma-gapclose", "status": "done",
                 "item": "Close the gap on ACT top-down w2872 (9/10)",
                 "closed_utc": "2026-11-07T23:29:06Z"},
                {"n": "gr-w2883-gamma-gapclose", "status": "open",
                 "item": "Close the gap on ACT top-down w2882 (9/10)"},
            ],
        }

    def test_stem_ref_marks_stale(self):
        out = "\n".join(_sb.recommendation_block(self._stem_doc(), ""))
        self.assertIn("STALE, NOT QUOTED", out,
                      "stem-only rec of a done item must be stale, not quoted")
        self.assertIn("gr-w2873-gamma-gapclose", out,
                      "the verdict must name the full closed id")

    def test_longer_id_sharing_prefix_does_not_fire(self):
        doc = self._stem_doc()
        doc["last_recommendation"] = "next Gamma takes gr-w28730 first"
        out = "\n".join(_sb.recommendation_block(doc, ""))
        self.assertNotIn("STALE, NOT QUOTED", out,
                         "gr-w28730 must not fire the gr-w2873 stem")


class TestDeadOpenStemRefRegression(unittest.TestCase):
    """Gamma w2894 (refs-dead-open-stem-hole): TIER 1 stem match for the
    dead-premise guard.

    refs_dead_open carried the same full-id-only stem hole refs_done had:
    a recommendation referencing a dead-premise OPEN item (status=
    superseded) by wave-stem only ("gr-w1222") slipped past both the
    full-id check and the prose tier (<2 distinctive tokens), so the
    brief quoted it as freshness-checked. The stem match fires on the
    token-bounded stem; a longer id sharing the prefix must not.
    """

    def _dead_doc(self):
        return {
            "area": "ACT",
            "seat": "Naya Gamma",
            "last_recommendation":
                "next Gamma takes gr-w1222 first, it is the highest-value closure",
            "items": [
                {"n": "gr-w1222-gamma-gapclose", "status": "superseded",
                 "item": "Close the gap on ACT top-down w1222 (9/10): "
                         "gr-w1213/gr-w1209 gapcloses held"},
                {"n": "gr-w2883-gamma-gapclose", "status": "open",
                 "item": "Close the gap on ACT top-down w2882 (9/10)"},
            ],
        }

    def test_stem_ref_marks_dead_premise(self):
        out = "\n".join(_sb.recommendation_block(self._dead_doc(), ""))
        self.assertIn("DEAD PREMISE, NOT QUOTED", out,
                      "stem-only rec of a dead-premise OPEN item must not be quoted")
        self.assertIn("gr-w1222-gamma-gapclose", out,
                      "the verdict must name the full dead-premise id")

    def test_longer_id_sharing_prefix_does_not_fire(self):
        doc = self._dead_doc()
        doc["last_recommendation"] = "next Gamma takes gr-w12220 first"
        out = "\n".join(_sb.recommendation_block(doc, ""))
        self.assertNotIn("DEAD PREMISE, NOT QUOTED", out,
                         "gr-w12220 must not fire the gr-w1222 stem")


def _lane_claimed(lane):
    try:
        with open(os.path.join(_sb.SBRAIN, "lane-state.json")) as fh:
            st = json.load(fh)
        return bool((st.get("lanes") or {}).get(str(lane), {}).get("holder"))
    except Exception:
        return False


class TestEndToEndSmoke(unittest.TestCase):
    """The w312 poison smoke, persisted: through the REAL generator."""

    AREA_LIST = os.path.join(
        _sb.SBRAIN, "areas/top10/HUMAN_VALUE.json")

    def _gen(self, thinking):
        return subprocess.run(
            [sys.executable, os.path.join(BIN, "spawn_brief.py"),
             "--seat", "Naya Mu", "--lane", "3", "--area", "HUMAN_VALUE",
             "--time-box", "~1 min", "--thinking", thinking,
             "--area-list", self.AREA_LIST],
            capture_output=True, text=True, timeout=120)

    @unittest.skipUnless(_lane_claimed(3),
                         "lane 3 unclaimed — the generator itself refuses; "
                         "smoke would test the claim gate, not the guard")
    def test_poison_brief_dies_exit2_zero_stdout_window_in_stderr(self):
        r = self._gen("Re-run gr-w299-mu-note2-reexecute is now live today")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, "",
                         "fail-closed kill must emit ZERO stdout")
        self.assertIn("stale LIVE premise", r.stderr)
        self.assertIn(CLOSED_ID, r.stderr,
                      "the kill message must name the window's item")

    @unittest.skipUnless(_lane_claimed(3),
                         "lane 3 unclaimed — the generator itself refuses; "
                         "smoke would test the claim gate, not the guard")
    def test_benign_brief_generates(self):
        r = self._gen("Work the open items top-down; verify each premise first")
        self.assertEqual(r.returncode, 0)
        self.assertTrue(r.stdout.strip(), "benign brief must generate")


class TestLocalOnlyRender(unittest.TestCase):
    """Mu w474 (gr-w471-mu-localonly): the LOCAL-ONLY block must render
    mechanically with --local-only, be absent without it, and the
    --local-only-if-throttled flag must route the dispatcher's throttle
    decision (api-budget.json, >5000/day pace) into the brief without
    the dispatcher remembering anything."""
    AREA_LIST = os.path.join(
        _sb.SBRAIN, "areas/top10/HUMAN_VALUE.json")
    BUDGET = os.path.join(_sb.SBRAIN, "api-budget.json")
    THINKING = "Work the open items top-down; verify each premise first"

    def _gen(self, *extra):
        return subprocess.run(
            [sys.executable, os.path.join(BIN, "spawn_brief.py"),
             "--seat", "Naya Mu", "--lane", "2", "--area", "HUMAN_VALUE",
             "--time-box", "~1 min", "--thinking", self.THINKING,
             "--area-list", self.AREA_LIST] + list(extra),
            capture_output=True, text=True, timeout=120)

    @unittest.skipUnless(_lane_claimed(2),
                         "lane 2 unclaimed — the generator itself refuses")
    def test_block_renders_with_local_only_flag(self):
        r = self._gen("--local-only")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("==== LOCAL-ONLY WAVE", r.stdout)
        self.assertIn("ZERO API", r.stdout)
        self.assertIn("boom_flag.py check --local-only", r.stdout)
        self.assertIn("LOCAL-ONLY OVERRIDE", r.stdout,
                      "the governor override must follow the mode too")

    @unittest.skipUnless(_lane_claimed(2),
                         "lane 2 unclaimed — the generator itself refuses")
    def test_block_absent_without_flag(self):
        r = self._gen()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("==== LOCAL-ONLY WAVE", r.stdout,
                         "the block must never leak into a normal brief")

    def _write_budget(self, month, spent):
        with open(self.BUDGET, "w") as fh:
            json.dump({"month": month, "spent": spent}, fh)

    def test_throttle_decision_over_pace(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as tf:
            json.dump({"month": _current_month(), "spent": 200000}, tf)
            p = tf.name
        throttled, detail = _sb.quota_throttle_decision(p)
        os.unlink(p)
        self.assertTrue(throttled)
        self.assertIn("> 5000", detail)

    def test_throttle_decision_under_pace(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as tf:
            json.dump({"month": _current_month(), "spent": 1000}, tf)
            p = tf.name
        throttled, detail = _sb.quota_throttle_decision(p)
        os.unlink(p)
        self.assertFalse(throttled)
        self.assertIn("under pace", detail)

    def test_throttle_decision_missing_file(self):
        throttled, detail = _sb.quota_throttle_decision(
            "/nonexistent/api-budget.json")
        self.assertFalse(throttled)
        self.assertIn("no budget file", detail)

    def test_throttle_decision_stale_month(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as tf:
            json.dump({"month": "2026-09", "spent": 99999999}, tf)
            p = tf.name
        throttled, detail = _sb.quota_throttle_decision(p)
        os.unlink(p)
        self.assertFalse(throttled, "a stale month must reset, not throttle")
        self.assertIn("budget month", detail)

    def _swap_budget(self, month, spent):
        with open(self.BUDGET) as fh:
            original = fh.read()
        self._write_budget(month, spent)
        return original

    def _restore_budget(self, original):
        with open(self.BUDGET, "w") as fh:
            fh.write(original)
        with open(self.BUDGET) as fh:
            self.assertEqual(fh.read(), original,
                             "budget truth file must be byte-identical")

    @unittest.skipUnless(_lane_claimed(2),
                         "lane 2 unclaimed — the generator itself refuses")
    def test_throttle_flag_routes_over_pace(self):
        original = self._swap_budget(_current_month(), 200000)
        try:
            r = self._gen("--local-only-if-throttled")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("==== LOCAL-ONLY WAVE", r.stdout,
                          "over-pace throttle must render the block")
            self.assertIn("MODE DECIDED BY:", r.stdout,
                          "the block must stamp its provenance")
            self.assertIn("LOCAL-ONLY OVERRIDE", r.stdout)
        finally:
            self._restore_budget(original)

    @unittest.skipUnless(_lane_claimed(2),
                         "lane 2 unclaimed — the generator itself refuses")
    def test_throttle_flag_noop_under_pace(self):
        original = self._swap_budget(_current_month(), 1000)
        try:
            r = self._gen("--local-only-if-throttled")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn("==== LOCAL-ONLY WAVE", r.stdout,
                             "under pace the flag must be a no-op")
        finally:
            self._restore_budget(original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
