"""Tests for the Naya Decision Principle (kernel/decision_principle.py).

Proves, in order:
  (a) a prohibited action with otherwise-high value is DISQUALIFIED, not outscored
  (b) uncertainty alone never disqualifies
  (c) "I don't know" is a valid, honest output
  (d) disqualified actions never enter the Phase-2 ranking (exclusion proof)
  (e) the existing value-calculus pipeline excludes before it optimizes
  (f) two independent implementations agree on every scenario
"""

import pytest

from kernel import decision_principle as dp
from kernel.decision_principle import (
    Action, DecisionEngine,
    ADMISSIBLE, DISQUALIFIED, DEFERRED,
    ACT, ABSTAIN, REFUSE, ASK,
    gate_protect_people, gate_tell_truth, gate_respect_authority,
    run_hard_gates, verdict_from_calculus_gate,
    verify_pipeline_excludes_first, cross_verify,
    random_scenarios, scenario_battery,
)


def _clean(aid="a", **kw):
    """A fully admissible action with verified value 5.0 by default."""
    d = dict(action_id=aid, unacceptable_harm=False, deceptive=False,
             authorized=True, verified_value=5.0)
    d.update(kw)
    return Action(**d)


ENGINE = DecisionEngine()


# ---------------------------------------------------------------------------
# (a) Disqualification, not zero-scoring
# ---------------------------------------------------------------------------

def test_high_value_harmful_action_is_disqualified_not_outscored():
    harmful = _clean("harmful", unacceptable_harm=True, verified_value=100.0)
    safe = _clean("safe", verified_value=5.0)
    d = ENGINE.decide([harmful, safe])

    assert d.outcome == ACT
    assert d.chosen_action_id == "safe"
    assert d.chosen_value == 5.0
    assert d.disqualified_ids == ("harmful",)
    # The disqualified action never entered the ranking at all.
    assert "harmful" not in d.ranking
    assert d.ranking == ("safe",)


def test_deceptive_action_disqualified_despite_value():
    liar = _clean("liar", deceptive=True, verified_value=99.0)
    honest = _clean("honest", verified_value=1.0)
    d = ENGINE.decide([liar, honest])
    assert d.chosen_action_id == "honest"
    assert d.disqualified_ids == ("liar",)


def test_forbidden_scope_disqualified_despite_value():
    rogue = _clean("rogue", forbidden_scope=True, verified_value=42.0)
    ok = _clean("ok", verified_value=2.0)
    d = ENGINE.decide([rogue, ok])
    assert d.chosen_action_id == "ok"
    assert d.disqualified_ids == ("rogue",)


def test_all_disqualified_means_refuse():
    h1 = _clean("h1", unacceptable_harm=True, verified_value=10.0)
    h2 = _clean("h2", deceptive=True, verified_value=10.0)
    d = ENGINE.decide([h1, h2])
    assert d.outcome == REFUSE
    assert d.chosen_action_id is None
    assert set(d.disqualified_ids) == {"h1", "h2"}


def test_disqualified_action_cannot_be_rescued_by_other_gates():
    # Passes truth and authority gates; still disqualified by protect-people.
    # Phase-1 verdict is all-or-nothing on disqualification.
    verdict, results = run_hard_gates(
        _clean("x", unacceptable_harm=True, verified_value=1000.0))
    assert verdict == DISQUALIFIED
    by_gate = {r.gate: r.verdict for r in results}
    assert by_gate["protect_people"] == DISQUALIFIED
    assert by_gate["tell_truth"] == ADMISSIBLE
    assert by_gate["respect_authority"] == ADMISSIBLE


# ---------------------------------------------------------------------------
# (b) Uncertainty alone never disqualifies
# ---------------------------------------------------------------------------

def test_unknown_harm_defers_never_disqualifies():
    r = gate_protect_people(_clean("u", unacceptable_harm=None,
                                   harm_severity=None, harm_probability=None))
    assert r.verdict == DEFERRED
    assert r.verdict != DISQUALIFIED


def test_unknown_truthfulness_defers():
    r = gate_tell_truth(_clean("u", deceptive=None))
    assert r.verdict == DEFERRED


def test_missing_authority_defers_not_disqualifies():
    r = gate_respect_authority(_clean("u", authorized=False))
    assert r.verdict == DEFERRED
    assert r.verdict != DISQUALIFIED


def test_all_unknown_yields_ask_not_refuse():
    d = ENGINE.decide([_clean("u", unacceptable_harm=None, deceptive=None,
                              authorized=False)])
    assert d.outcome == ASK
    assert d.deferred_ids == ("u",)
    assert d.disqualified_ids == ()


def test_empty_input_abstains_honestly():
    d = ENGINE.decide([])
    assert d.outcome == ABSTAIN
    assert d.chosen_action_id is None
    assert "No actions were proposed" in d.note


def test_mixed_deferred_and_disqualified_asks_not_refuses():
    dq = _clean("dq", unacceptable_harm=True, verified_value=100.0)
    waiting = _clean("waiting", authorized=False, verified_value=50.0)
    d = ENGINE.decide([dq, waiting])
    assert d.outcome == ASK
    assert d.disqualified_ids == ("dq",)
    assert d.deferred_ids == ("waiting",)


def test_evidence_only_deferred_abstains():
    # Deferred purely on unknown evidence (authority held, honesty known):
    # the honest output is "I don't know yet", not ASK.
    unknown = _clean("unknown", unacceptable_harm=None, harm_severity=None,
                     harm_probability=None, deceptive=False, authorized=True,
                     verified_value=None)
    d = ENGINE.decide([unknown])
    assert d.outcome == ABSTAIN
    assert d.deferred_ids == ("unknown",)
    assert "don't know" in d.note


def test_consented_mitigated_residual_risk_is_admissible():
    # Shawn's refinement: helping involves trade-offs. Minimized residual
    # risk with informed consent passes the protect-people gate.
    risky = _clean("risky", harm_severity=9.0, harm_probability=0.5,
                   harm_mitigated=True, informed_consent=True,
                   verified_value=8.0)
    r = gate_protect_people(risky)
    assert r.verdict == ADMISSIBLE
    d = ENGINE.decide([risky, _clean("plain", verified_value=3.0)])
    assert d.chosen_action_id == "risky"


def test_unmitigated_high_risk_assessment_disqualifies():
    reckless = _clean("reckless", unacceptable_harm=None, harm_severity=9.0,
                      harm_probability=0.5, verified_value=50.0)
    modest = _clean("modest", verified_value=3.0)
    d = ENGINE.decide([reckless, modest])
    assert d.chosen_action_id == "modest"
    assert d.disqualified_ids == ("reckless",)


def test_low_severity_uncertainty_does_not_disqualify():
    mild = _clean("mild", unacceptable_harm=None, harm_severity=2.0,
                  harm_probability=0.9, verified_value=4.0)
    # Below the severity bar: not established unacceptable harm -> defers
    # on unknown, does not disqualify.
    r = gate_protect_people(mild)
    assert r.verdict != DISQUALIFIED


# ---------------------------------------------------------------------------
# (c) Honest abstention is a valid output
# ---------------------------------------------------------------------------

def test_no_verified_value_means_abstain_not_guess():
    a = _clean("a", verified_value=None)
    b = _clean("b", verified_value=None)
    d = ENGINE.decide([a, b])
    assert d.outcome == ABSTAIN
    assert d.chosen_action_id is None
    assert d.admissible_ids == ("a", "b")


def test_explicit_honest_abstention_can_win_phase_two():
    guess = _clean("bold-guess", verified_value=None)
    honest = _clean("say-i-dont-know", honest_abstention=True,
                    verified_value=0.5,
                    value_evidence="honesty avoids acting on unverified value")
    d = ENGINE.decide([guess, honest])
    assert d.outcome == ACT
    assert d.chosen_action_id == "say-i-dont-know"


def test_abstention_is_not_a_failure_state():
    # The engine must be able to SAY it abstains with a clear note.
    d = ENGINE.decide([_clean("a", verified_value=None)])
    assert d.outcome == ABSTAIN
    assert "don't know" in d.note or "abstain" in d.note


# ---------------------------------------------------------------------------
# (d) Exclusion proof — Phase 2 never sees disqualified actions
# ---------------------------------------------------------------------------

def test_phase_two_ranking_contains_only_admissible():
    actions = [
        _clean("dq1", unacceptable_harm=True, verified_value=100.0),
        _clean("dq2", deceptive=True, verified_value=90.0),
        _clean("dq3", forbidden_scope=True, verified_value=80.0),
        _clean("ok1", verified_value=7.0),
        _clean("ok2", verified_value=9.0),
        _clean("deferred1", authorized=False, verified_value=50.0),
    ]
    d = ENGINE.decide(actions)
    assert d.chosen_action_id == "ok2"   # argmax over admissible only
    assert set(d.ranking) == {"ok1", "ok2"}
    assert set(d.disqualified_ids) == {"dq1", "dq2", "dq3"}
    assert d.deferred_ids == ("deferred1",)
    for dq in d.disqualified_ids:
        assert dq not in d.ranking


def test_argmax_over_admissible_verified_value():
    actions = [_clean(f"c{i}", verified_value=float(v))
               for i, v in enumerate([3.0, 9.0, 9.0, 1.0])]
    d = ENGINE.decide(actions)
    # Tie 9.0/9.0 breaks deterministically by action_id: c1 < c2.
    assert d.chosen_action_id == "c1"
    assert d.ranking == ("c1", "c2", "c0", "c3")


# ---------------------------------------------------------------------------
# Gate mapping sanity
# ---------------------------------------------------------------------------

def test_verdict_mapping_from_calculus():
    assert verdict_from_calculus_gate("PROHIBITED") == DISQUALIFIED
    assert verdict_from_calculus_gate("NEEDS_AUTHORITY") == DEFERRED
    assert verdict_from_calculus_gate("NEEDS_EVIDENCE") == DEFERRED
    assert verdict_from_calculus_gate("ADMISSIBLE") == ADMISSIBLE
    with pytest.raises(ValueError):
        verdict_from_calculus_gate("BOGUS")


# ---------------------------------------------------------------------------
# (e) The existing pipeline already excludes before optimizing
# ---------------------------------------------------------------------------

def _vc_candidate(cid, **kw):
    from kernel.value_calculus import Candidate, PVEstimate
    base = dict(
        candidate_id=cid,
        quality={d: 8.0 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        confidence={d: 0.9 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        pv=PVEstimate(B=8.0, H=1.0, C=1.0, R=0.5,
                      confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
                      evidence_count=3),
        authorized=True, lawful=True, rights_safe=True,
        privacy_safe=True, safety_safe=True,
    )
    base.update(kw)
    return Candidate(**base)


def _vc_profile():
    from kernel.value_calculus import QualityProfile
    return QualityProfile(profile_id="dp-test", version="1",
                          objective="decision principle integration")


def test_existing_pipeline_excludes_prohibited_before_optimizing():
    from kernel.value_calculus import RiskPolicy
    profile = _vc_profile()
    baseline = _vc_candidate("base", is_baseline=True)
    prohibited = _vc_candidate("bad", hard_violation=True)   # PROHIBITED
    noauth = _vc_candidate("noauth", authorized=False)        # NEEDS_AUTHORITY
    good = _vc_candidate("good")
    evidence = verify_pipeline_excludes_first(
        [baseline, prohibited, noauth, good], "base", profile, RiskPolicy())
    assert evidence["gates"]["bad"] == "PROHIBITED"
    assert evidence["gates"]["noauth"] == "NEEDS_AUTHORITY"
    assert evidence["violations"] == []
    assert "bad" not in evidence["ranked_ids"]
    assert "bad" not in evidence["top3_ids"]
    # NEEDS_AUTHORITY is deferred, not disqualified — but it still must
    # never compete in optimization.
    assert "noauth" not in evidence["ranked_ids"]
    assert "noauth" not in evidence["top3_ids"]
    # Verdict mapping keeps the semantics straight across the seam.
    assert verdict_from_calculus_gate(evidence["gates"]["bad"]) == DISQUALIFIED
    assert verdict_from_calculus_gate(evidence["gates"]["noauth"]) == DEFERRED


# ---------------------------------------------------------------------------
# (f) Cross-implementation verification — the principle must govern
#     behavior across multiple implementations, not just one.
# ---------------------------------------------------------------------------

def test_cross_implementation_agrees_on_handbuilt_battery():
    evidence = cross_verify(scenario_battery())
    assert evidence["agreed"]
    assert evidence["scenarios"] == 10
    assert evidence["divergences"] == []


def test_cross_implementation_agrees_on_randomized_scenarios():
    scenarios = random_scenarios(seed=20261011, count=300, max_actions=5)
    evidence = cross_verify(scenarios)
    assert evidence["agreed"]
    assert evidence["divergences"] == []


def test_cross_implementation_second_seed():
    scenarios = random_scenarios(seed=777, count=200, max_actions=6)
    evidence = cross_verify(scenarios)
    assert evidence["agreed"]
