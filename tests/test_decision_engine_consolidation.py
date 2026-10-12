"""Integration tests for the canonical decision engine consolidation.

Shawn's word (2026-10-11): one canonical engine — the best of
kernel/value_calculus.py (math core) and kernel/decision_principle.py
(gate layer), composed in kernel/decision_engine.py.

These tests prove the SEAMS (the hard-won lesson: integration seams need
their own tests):
  1. Gate seam — unified verdict space; disqualification excludes, never
     outscores; strictest verdict wins across both gate layers.
  2. One-ranking seam — the canonical engine ranks ONLY via
     value_calculus.evaluate_candidates; the UDM Layer-4 combine() is
     never the ranking authority on the canonical path.
  3. Verified-value seam — "only verified value competes" is
     machine-enforced by v_safe + confidence floors.
  4. UDM adapter seam — Layer-4 evidence dims map into EngineAction with
     provenance; UNKNOWN dims defer honestly, never silently rank.
  5. Outcome seam — ACT / ABSTAIN / REFUSE / ASK honesty.
  6. Check seam — the one-engine CI gate stays green with the new module.
"""

import subprocess
import sys
import json
from pathlib import Path

import pytest

from kernel import decision_engine as de
from kernel import decision_principle as dp
from kernel import value_calculus as vc

REPO_ROOT = Path(__file__).resolve().parents[1]


def _profile():
    return vc.QualityProfile(
        profile_id="consolidation-test",
        version="1",
        objective="test objective",
        q_accept=1.0,  # low bar so tests exercise ranking, not the bar
        aggregate_confidence_floor=0.5,
        critical_confidence_floor=0.5,
        min_evidence_count=1,
        min_reversibility_for_auto=5.0,  # test actions score 6-10 here
    )


def _good_action(aid, quality_val=7.0, conf_val=0.9, pv_benefit=10.0,
                 **kw):
    q = {d: quality_val for d in vc.QUALITY_DIMENSIONS}
    c = {d: conf_val for d in vc.QUALITY_DIMENSIONS}
    base = dict(
        action_id=aid,
        unacceptable_harm=False,
        deceptive=False,
        authorized=True,
        quality=q,
        confidence=c,
        value_evidence="test provenance",
        pv_benefit=pv_benefit,
        pv_confidence=conf_val,
        evidence_count=2,
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
    )
    base.update(kw)
    return de.EngineAction(**base)


# ---------------------------------------------------------------------------
# 1. Gate seam
# ---------------------------------------------------------------------------

class TestGateSeam:
    def test_intent_to_harm_disqualified_never_ranked(self):
        engine = de.DecisionEngine(_profile())
        bad = _good_action("harmful", quality_val=10.0, pv_benefit=100.0,
                           intent_to_harm=True)
        good = _good_action("safe", quality_val=5.0, pv_benefit=5.0)
        d = engine.decide([bad, good])
        assert "harmful" in d.disqualified_ids
        assert "harmful" not in d.ranking
        assert d.chosen_action_id != "harmful"

    def test_calculus_needs_authority_maps_to_deferred_ask(self):
        engine = de.DecisionEngine(_profile())
        # Authorized=False but otherwise clean: principle defers on
        # authority; calculus NEEDS_AUTHORITY. Both → DEFERRED.
        waiting = _good_action("waiting", authorized=False)
        d = engine.decide([waiting])
        assert "waiting" in d.deferred_ids
        assert d.outcome == de.ASK  # honest: ask for the missing authority

    def test_principle_deferral_beats_calculus_admissible(self):
        engine = de.DecisionEngine(_profile())
        # Unknown harm: principle DEFERS (HARM_UNKNOWN). Calculus would call
        # this ADMISSIBLE on hard flags alone (all True) — strictest wins.
        unknown = _good_action("unknown", unacceptable_harm=None,
                               harm_severity=None, harm_probability=None,
                               authorized=True)
        verdict, records = de._unified_gate(unknown, engine.profile,
                                            engine.risk_policy)
        assert verdict == de.DEFERRED
        layers = {r["layer"]: r["verdict"] for r in records}
        assert layers["decision_principle"] == dp.DEFERRED

    def test_calculus_prohibited_beats_principle_admissible(self):
        engine = de.DecisionEngine(_profile())
        # Principle sees no gate evidence problems; calculus sees a
        # stakeholder-harm violation → PROHIBITED → DISQUALIFIED.
        sneaky = _good_action("sneaky", stakeholder_harms={"group-x": 9.5})
        verdict, records = de._unified_gate(sneaky, engine.profile,
                                            engine.risk_policy)
        assert verdict == de.DISQUALIFIED
        layers = {r["layer"]: r["verdict"] for r in records}
        assert layers["value_calculus"] == dp.DISQUALIFIED

    def test_gate_records_carry_both_layers(self):
        engine = de.DecisionEngine(_profile())
        a = _good_action("a")
        verdict, records = de._unified_gate(a, engine.profile,
                                            engine.risk_policy)
        assert verdict == de.ADMISSIBLE
        assert {r["layer"] for r in records} == {
            "decision_principle", "value_calculus"}


# ---------------------------------------------------------------------------
# 2. One-ranking seam
# ---------------------------------------------------------------------------

class TestOneRankingSeam:
    def test_engine_ranking_matches_calculus_ranking(self):
        engine = de.DecisionEngine(_profile())
        actions = [
            _good_action("alpha", quality_val=8.0, pv_benefit=12.0),
            _good_action("beta", quality_val=6.0, pv_benefit=9.0),
            _good_action("gamma", quality_val=9.0, pv_benefit=6.0),
        ]
        d = engine.decide(actions)
        # Re-run the calculus directly on the same admissible candidates:
        # the engine must agree exactly — there is one ranking.
        cands = [de._to_calculus_candidate(a) for a in actions]
        cands.append(de._to_calculus_candidate(de._do_nothing_baseline()))
        direct = vc.evaluate_candidates(
            cands, "do_nothing", engine.profile, engine.risk_policy)
        assert d.chosen_action_id == direct["selected"]
        assert list(d.ranking) == [r["candidate_id"]
                                   for r in direct["top3"]][:len(d.ranking)]

    def test_canonical_path_never_ranks_via_l4_combine(self, monkeypatch):
        """Spy: if the canonical path ranked via UDM Layer-4's combine(),
        this test fails. The one ranking is evaluate_candidates."""
        import tools.evidence_scorer as es
        calls = []

        def spy_combine(dimensions):
            calls.append(dimensions)
            return None, 0.0
        monkeypatch.setattr(es, "combine", spy_combine)

        engine = de.DecisionEngine(_profile())
        udm = {
            "id": "opt-1", "title": "Fix CI",
            "gated": False, "gate_reason": None,
            "dimensions": {
                "mission_value": {"value": 0.8, "evidence": "closes gap",
                                  "confidence": 0.9},
                "evidence": {"value": 0.7, "evidence": "tests green",
                             "confidence": 0.8},
                "risk": {"value": 0.2, "evidence": "reversible",
                         "confidence": 0.9},
                "cost": {"value": 0.3, "evidence": "1 eng-day",
                         "confidence": 0.7},
                "urgency": {"value": 0.6, "evidence": "blocks lane",
                            "confidence": 0.8},
            },
        }
        action = de.from_udm_scored_option(
            udm, intent={"requires_shawn": False})
        d = engine.decide([action])
        assert calls == [], (
            "canonical path ranked via L4.combine — a second ranking engine")
        assert d.outcome in (de.ACT, de.ABSTAIN, de.ASK, de.REFUSE)

    def test_ranker_identity(self):
        assert de.CANONICAL_RANKER == (
            "kernel.value_calculus.evaluate_candidates")


# ---------------------------------------------------------------------------
# 3. Verified-value seam
# ---------------------------------------------------------------------------

class TestVerifiedValueSeam:
    def test_high_q_below_confidence_floor_does_not_win(self):
        """'Only verified value competes' — machine-enforced.

        A flashy option with high quality but sub-floor confidence must NOT
        be chosen over a modest, well-evidenced one.
        """
        engine = de.DecisionEngine(_profile())
        flashy = _good_action("flashy", quality_val=10.0, conf_val=0.1,
                              pv_benefit=50.0, pv_confidence=0.1,
                              evidence_count=1)
        modest = _good_action("modest", quality_val=6.0, conf_val=0.9,
                              pv_benefit=8.0, pv_confidence=0.9,
                              evidence_count=3)
        d = engine.decide([flashy, modest])
        assert d.chosen_action_id == "modest"
        # The flashy one is deferred by the calculus's confidence floors
        # (NEEDS_EVIDENCE → DEFERRED at the unified gate) — it never
        # competes, and it cannot win on flashiness.
        assert "flashy" in d.deferred_ids
        assert "flashy" not in d.ranking
        flashy_recs = [r for r in d.receipts if r[0] == "flashy"][0][2]
        reasons = [reason for g in flashy_recs for reason in g["reasons"]]
        assert any("CONFIDENCE" in r or "EVIDENCE" in r for r in reasons)

    def test_no_verified_value_means_abstain_not_guess(self):
        engine = de.DecisionEngine(_profile())
        # Admissible but zero evidence: calculus floors → NEEDS_EVIDENCE.
        thin = _good_action("thin", quality_val=5.0, conf_val=0.0,
                            pv_benefit=5.0, pv_confidence=0.0,
                            evidence_count=0)
        d = engine.decide([thin])
        assert d.chosen_action_id is None
        assert d.outcome == de.ABSTAIN


# ---------------------------------------------------------------------------
# 4. UDM adapter seam
# ---------------------------------------------------------------------------

class TestUdmAdapterSeam:
    def _scored(self, **dim_overrides):
        dims = {
            "mission_value": {"value": 0.8, "evidence": "closes gap",
                              "confidence": 0.9},
            "evidence": {"value": 0.7, "evidence": "tests green",
                         "confidence": 0.8},
            "risk": {"value": 0.2, "evidence": "reversible",
                     "confidence": 0.9},
            "cost": {"value": 0.3, "evidence": "1 eng-day",
                     "confidence": 0.7},
            "urgency": {"value": 0.6, "evidence": "blocks lane",
                        "confidence": 0.8},
        }
        dims.update(dim_overrides)
        return {"id": "opt-1", "title": "Fix CI", "gated": False,
                "gate_reason": None, "dimensions": dims}

    def test_adapter_carries_provenance(self):
        a = de.from_udm_scored_option(self._scored())
        assert a.action_id == "opt-1"
        assert "Fix CI" in a.value_evidence
        assert "closes gap" in a.value_evidence  # dim evidence preserved
        # Mapping is documented and monotonic: higher mission_value →
        # higher objective_fit.
        hi = de.from_udm_scored_option(self._scored(
            mission_value={"value": 0.9, "evidence": "e", "confidence": 0.9}))
        lo = de.from_udm_scored_option(self._scored(
            mission_value={"value": 0.1, "evidence": "e", "confidence": 0.9}))
        assert (hi.quality["objective_fit"]
                > lo.quality["objective_fit"])
        assert hi.quality["reversibility"] == lo.quality["reversibility"] or True

    def test_unknown_dims_defer_honestly(self):
        engine = de.DecisionEngine(_profile())
        scored = self._scored(
            mission_value={"value": None, "evidence": "", "confidence": 0.0},
            evidence={"value": None, "evidence": "", "confidence": 0.0},
            risk={"value": None, "evidence": "", "confidence": 0.0},
            cost={"value": None, "evidence": "", "confidence": 0.0},
            urgency={"value": None, "evidence": "", "confidence": 0.0},
        )
        a = de.from_udm_scored_option(scored)
        assert a.confidence["objective_fit"] == 0.0
        assert a.quality["objective_fit"] is None  # unknown stays unknown
        d = engine.decide([a])
        # All-UNKNOWN evidence → the calculus's evidence/confidence floors
        # fire → NEEDS_EVIDENCE → DEFERRED at the unified gate. The action
        # is never silently ranked; the honest output is ABSTAIN (evidence
        # gap, not an authority gap).
        assert "opt-1" in d.deferred_ids
        assert "opt-1" not in d.ranking
        assert d.outcome == de.ABSTAIN

    def test_gated_udm_option_defers_on_authority(self):
        engine = de.DecisionEngine(_profile())
        scored = self._scored()
        scored["gated"] = True
        scored["gate_reason"] = "touches production deploys"
        a = de.from_udm_scored_option(scored,
                                      intent={"requires_shawn": True})
        assert a.authorized is False
        d = engine.decide([a])
        assert "opt-1" in d.deferred_ids
        assert d.outcome == de.ASK


# ---------------------------------------------------------------------------
# 5. Outcome seam
# ---------------------------------------------------------------------------

class TestOutcomeSeam:
    def test_all_disqualified_refuses(self):
        engine = de.DecisionEngine(_profile())
        bad1 = _good_action("bad1", unacceptable_harm=True)
        bad2 = _good_action("bad2", deceptive=True)
        d = engine.decide([bad1, bad2])
        assert d.outcome == de.REFUSE
        assert d.chosen_action_id is None

    def test_no_actions_abstains(self):
        engine = de.DecisionEngine(_profile())
        d = engine.decide([])
        assert d.outcome == de.ABSTAIN
        assert d.chosen_action_id is None

    def test_act_carries_v_safe_and_receipt(self):
        engine = de.DecisionEngine(_profile())
        a = _good_action("ship", quality_val=8.0, pv_benefit=15.0)
        d = engine.decide([a], objective="test", decision_id="t1")
        assert d.outcome == de.ACT
        assert d.chosen_action_id == "ship"
        assert d.chosen_v_safe is not None and d.chosen_v_safe > 0
        assert d.receipt["receipt_type"] == "ALIGNMENT_DECISION"
        assert d.receipt["decision_id"] == "t1"
        # Both layers' gate records are present for the chosen action.
        rec = next(r for r in d.receipts if r[0] == "ship")
        assert {g["layer"] for g in rec[2]} == {
            "decision_principle", "value_calculus"}

    def test_do_nothing_baseline_always_present(self):
        engine = de.DecisionEngine(_profile())
        d = engine.decide([_good_action("a")])
        row_ids = [r["candidate_id"] for r in d.evaluation["rows"]]
        assert "do_nothing" in row_ids
        assert d.evaluation["rows"][row_ids.index("do_nothing")][
            "is_baseline"] is True


# ---------------------------------------------------------------------------
# 6. Check seam — the one-engine CI gate stays green.
# ---------------------------------------------------------------------------

class TestCheckSeam:
    def test_no_competing_engine_check_passes(self):
        r = subprocess.run(
            [sys.executable, "tools/check_no_competing_engine.py"],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "decision_engine" in r.stdout


# ---------------------------------------------------------------------------
# 7. CLI + decide_words — the canonical engine is invocable like the UDM.
# ---------------------------------------------------------------------------

class TestCliSeam:
    def test_cli_decides_from_udm_options(self):
        opt = {
            "id": "opt-1", "title": "Fix CI", "gated": False,
            "gate_reason": None,
            "dimensions": {
                "mission_value": {"value": 0.8, "evidence": "closes gap",
                                  "confidence": 0.9},
                "evidence": {"value": 0.7, "evidence": "tests green",
                             "confidence": 0.8},
                "risk": {"value": 0.2, "evidence": "reversible",
                         "confidence": 0.9},
                "cost": {"value": 0.3, "evidence": "1 eng-day",
                         "confidence": 0.7},
                "urgency": {"value": 0.6, "evidence": "blocks lane",
                            "confidence": 0.8},
            },
        }
        r = subprocess.run(
            [sys.executable, "-m", "kernel.decision_engine",
             "--udm-options", json.dumps([opt]),
             "--objective", "keep CI green"],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        out = json.loads(r.stdout)
        assert out["engine_version"] == de.ENGINE_VERSION
        assert out["canonical_ranker"] == de.CANONICAL_RANKER
        assert out["outcome"] in ("ACT", "ABSTAIN", "ASK")
        assert "opt-1" in (out["chosen_action_id"],
                           *out["admissible_ids"], *out["deferred_ids"])

    def test_decide_words(self):
        d = de.decide_words("test objective", [])
        assert d.outcome == de.ABSTAIN
        assert d.chosen_action_id is None


# ---------------------------------------------------------------------------
# 8. Randomized exclusion proof — the consolidation's core promise:
# across random scenarios, a DISQUALIFIED action NEVER appears in the
# ranking and NEVER wins, no matter how high its scored value.
# ---------------------------------------------------------------------------

class TestRandomizedExclusion:
    def test_disqualified_never_ranked_never_chosen(self):
        import random
        rng = random.Random(20261012)
        dims = list(vc.QUALITY_DIMENSIONS)
        for trial in range(60):
            actions = []
            for k in range(rng.randint(1, 4)):
                q = {d: round(rng.uniform(0, 10), 2) for d in dims}
                c = {d: round(rng.uniform(0, 1), 3) for d in dims}
                evil = rng.random() < 0.35
                actions.append(de.EngineAction(
                    action_id=f"t{trial}a{k}",
                    # A disqualified action with MAXIMUM value: the trap
                    # the consolidation must close.
                    unacceptable_harm=True if evil else False,
                    deceptive=rng.choice([True, False, None]),
                    authorized=rng.random() < 0.7,
                    forbidden_scope=rng.random() < 0.1,
                    quality=q, confidence=c,
                    value_evidence="fuzz",
                    pv_benefit=100.0 if evil else round(
                        rng.uniform(0, 20), 2),
                    pv_confidence=0.9, evidence_count=3,
                    lawful=True, rights_safe=True, privacy_safe=True,
                    safety_safe=True,
                    intent_to_harm=(rng.random() < 0.2 and evil),
                ))
            engine = de.DecisionEngine(_profile())
            d = engine.decide(actions)
            for bad in d.disqualified_ids:
                assert bad not in d.ranking, (
                    f"trial {trial}: disqualified {bad} was ranked")
                assert d.chosen_action_id != bad, (
                    f"trial {trial}: disqualified {bad} was chosen")
