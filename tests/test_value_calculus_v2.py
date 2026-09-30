"""Tests for kernel/value_calculus_v2.py.

Covers the V2.1 spec behaviors plus adversarial cases from the spec's
attack list (section 13): prediction inflation, component gaming,
action-splitting / authorization laundering, delayed harm, collective vs
individual harm, uncertainty laundering, bad baseline selection, and
weight/rubric manipulation.
"""

import dataclasses

import pytest

from kernel.value_calculus_v2 import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Q_DIMS,
    DecisionContext,
    Option,
    PVComponents,
    V21Params,
    confirm_window,
    conservative_value,
    d_verified,
    decide,
    delta_v,
    evaluate_gate,
    evaluate_plan,
    inject_mandatory_baselines,
    ladder_step,
    observation_window_days,
    pareto_frontier,
    record_observation,
    relative_dominance,
    score_quality,
)


def _q(value=9.5, **over):
    d = {dim: value for dim in Q_DIMS}
    d.update(over)
    return d


def _c(value=0.9, **over):
    d = {dim: value for dim in Q_DIMS}
    d.update(over)
    return d


def make_option(id="opt", pv=None, evidence_count=10, reversibility=0.9,
                q_scores=None, q_confidence=None, **kw):
    return Option(
        id=id, label=id,
        q_scores=q_scores or _q(), q_confidence=q_confidence or _c(),
        pv=pv or PVComponents(benefit=8.0, harm=0.5, cost=1.0, risk=0.5),
        pv_confidence=kw.pop("pv_confidence", 0.9),
        evidence_count=evidence_count, reversibility=reversibility, **kw)


def make_ctx(**kw):
    baseline = kw.pop("baseline", None) or Option(
        id="baseline", label="current course",
        q_scores=_q(9.0), q_confidence=_c(0.85), evidence_count=10)
    return DecisionContext(objective="test objective", baseline=baseline, **kw)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_decide_is_deterministic():
    a = make_option("a")
    b = make_option("b", pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1)
    ctx = make_ctx()
    first = decide([a, b], ctx)
    second = decide([a, b], ctx)
    assert first == second


# ---------------------------------------------------------------------------
# N1: PV is not inside Q — correct inaction can clear the quality bar
# ---------------------------------------------------------------------------

def test_baseline_inaction_can_reach_q10():
    baseline = make_option("baseline", pv=PVComponents())  # PV = 0
    q = score_quality(baseline)
    assert q["q"] == pytest.approx(9.5)
    assert delta_v(baseline, baseline) == pytest.approx(0.0)


def test_high_value_cannot_rescue_low_quality():
    # Enormous claimed value, weak decision soundness -> Q stays low.
    o = make_option("gamer", pv=PVComponents(benefit=1000.0),
                    q_scores=_q(9.5, evidence_sufficiency=4.0, robustness=5.0))
    q = score_quality(o)
    assert q["q"] < 9.0
    assert q["band"] in ("BELOW_STANDARD", "REJECT")


def test_critical_proof_gap_caps_q():
    o = make_option("gap", q_scores=_q(9.8, objective_fit=6.0))
    q = score_quality(o)
    assert q["capped"] is True
    assert q["q"] <= 8.9


# ---------------------------------------------------------------------------
# Gates: hard boundaries precede optimization
# ---------------------------------------------------------------------------

def test_prohibited_beats_huge_value():
    o = make_option("nuke", pv=PVComponents(benefit=1e9),
                    p_unacceptable_harm={"physical_safety": 0.01})
    gate = evaluate_gate(o, make_ctx())
    assert gate["state"] == PROHIBITED
    res = decide([o], make_ctx())
    assert res["outcome"] in ("BRIEF", "RESEARCH", "REWORK")
    assert res["selected"] != "nuke" or res["outcome"] != "EXECUTE"


def test_zero_tolerance_class_refuses_material_probability():
    o = make_option("rights-risk", p_unacceptable_harm={"rights": 0.0001})
    assert evaluate_gate(o, make_ctx())["state"] == PROHIBITED


def test_unknown_harm_class_is_conservatively_prohibited():
    o = make_option("weird", p_unacceptable_harm={"jurisdiction_x": 0.01})
    assert evaluate_gate(o, make_ctx())["state"] == PROHIBITED


def test_tau_policy_routes_to_authority():
    o = make_option("info-risk", p_unacceptable_harm={"informational": 0.2})
    assert evaluate_gate(o, make_ctx())["state"] == NEEDS_AUTHORITY


def test_unauthorized_action_refused():
    o = make_option("auth", requires_authority=True)
    assert evaluate_gate(o, make_ctx())["state"] == NEEDS_AUTHORITY
    granted = make_option("auth", requires_authority=True, authority_granted=True)
    assert evaluate_gate(granted, make_ctx())["state"] == ADMISSIBLE


def test_evidence_floor_blocks_thin_estimates():
    o = make_option("thin", evidence_count=2)
    assert evaluate_gate(o, make_ctx())["state"] == NEEDS_EVIDENCE
    res = decide([o], make_ctx())
    assert res["outcome"] == "RESEARCH"


# ---------------------------------------------------------------------------
# Value, conservative value, tail risk
# ---------------------------------------------------------------------------

def test_delta_v_is_baseline_relative():
    base = make_option("b", pv=PVComponents(benefit=5.0, harm=1.0))
    opt = make_option("a", pv=PVComponents(benefit=9.0, harm=1.0))
    assert delta_v(opt, base) == pytest.approx(4.0)
    assert delta_v(base, base) == pytest.approx(0.0)


def test_prediction_inflation_is_penalized_and_visible():
    ctx = make_ctx()
    inflated = make_option(
        "inflated", pv=PVComponents(benefit=50.0), pv_confidence=0.3)
    cv = conservative_value(inflated, ctx.baseline)
    # LCB penalty applies: V_safe < raw dV, and the receipt exposes it.
    assert cv["v_safe"] < cv["dV_pred"]
    assert cv["v_safe"] == pytest.approx(50.0 - 0.7 * 9.0)


def test_inflated_claim_with_thin_evidence_is_not_rankable():
    o = make_option("inflated", pv=PVComponents(benefit=50.0),
                    pv_confidence=0.3, evidence_count=2)
    res = decide([o], make_ctx())
    assert all(s["id"] != "inflated" or not s["rankable"]
               for s in res["options"] if s["id"] == "inflated")


def test_tail_risk_subtracts_from_v_safe():
    ctx = make_ctx()
    clean = make_option("clean", p_unacceptable_harm={})
    risky = make_option("risky", p_unacceptable_harm={"informational": 0.04})
    v_clean = conservative_value(clean, ctx.baseline)["v_safe"]
    v_risky = conservative_value(risky, ctx.baseline)["v_safe"]
    assert v_risky < v_clean


def test_component_gaming_harm_is_not_averagable_away():
    # Attacker maxes benefit while hiding harm in the tail probability.
    o = make_option("gamer", pv=PVComponents(benefit=10.0, harm=0.0),
                    p_unacceptable_harm={"informational": 0.2})
    gate = evaluate_gate(o, make_ctx())
    assert gate["state"] == NEEDS_AUTHORITY  # tau for informational is 0.05


# ---------------------------------------------------------------------------
# Confidence: one unknown critical fact cannot be averaged away
# ---------------------------------------------------------------------------

def test_uncertainty_laundering_blocked_by_critical_floor():
    o = make_option("launder",
                    q_confidence=_c(1.0, evidence_sufficiency=0.2))
    res = decide([o], make_ctx())
    mine = next(s for s in res["options"] if s["id"] == "launder")
    assert mine["c_agg"] >= 0.80      # aggregate looks fine...
    assert mine["c_critical"] < 0.75  # ...but the critical floor fails
    assert mine["rankable"] is False


# ---------------------------------------------------------------------------
# Pareto, ranking, dominance
# ---------------------------------------------------------------------------

def test_pareto_excludes_dominated():
    scored = [
        {"id": "a", "v_safe": 5.0, "q": 9.5, "residual_risk": 0.2},
        {"id": "b", "v_safe": 4.0, "q": 9.0, "residual_risk": 0.3},
        {"id": "c", "v_safe": 3.0, "q": 9.9, "residual_risk": 0.1},
    ]
    frontier = pareto_frontier(scored)
    ids = [f["id"] for f in frontier]
    assert "b" not in ids            # dominated by a on all three
    assert set(ids) == {"a", "c"}    # neither dominates the other
    assert ids[0] == "a"             # ranked by V_safe desc


def test_relative_dominance_margin():
    assert relative_dominance(5.0, 3.0) == pytest.approx(0.4)
    assert relative_dominance(5.0, 4.9) < 0.25


def test_no_clear_dominance_briefs():
    a = make_option("a", pv=PVComponents(benefit=8.0, harm=0.5, cost=1.0, risk=0.5))
    b = make_option("b", pv=PVComponents(benefit=7.6, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.05)
    res = decide([a, b], make_ctx())
    assert res["outcome"] == "BRIEF"
    assert "NoClearDominantOption" in res["ask_human"]


def test_singleton_frontier_gets_no_auto_win():
    a = make_option("solo")
    res = decide([a], make_ctx())
    assert res["frontier"] == ["solo"]
    # No competitor -> dominance cannot be established -> BRIEF, not EXECUTE.
    assert res["outcome"] == "BRIEF"


def test_execute_happy_path():
    a = make_option("a", pv=PVComponents(benefit=8.0, harm=0.5, cost=1.0, risk=0.5),
                    residual_risk=0.2)
    b = make_option("b", pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1)
    res = decide([a, b], make_ctx())
    assert res["outcome"] == "EXECUTE"
    assert res["selected"] == "a"
    assert res["dominance_margin"] >= 0.25


def test_irreversible_action_is_non_autonomous():
    a = make_option("big-red", reversibility=0.5)
    res = decide([a], make_ctx())
    assert res["outcome"] == "BRIEF"
    assert any("reversibility" in r for r in res["outcome_reasons"])


def test_consequential_scope_needs_standing_contract():
    a = make_option("conseq", scope="consequential", evidence_count=25,
                    reversibility=0.9, residual_risk=0.2)
    b = make_option("b2", scope="consequential", evidence_count=25,
                    pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1, reversibility=0.95)
    res = decide([a, b], make_ctx())
    assert res["outcome"] == "BRIEF"  # no standing contract: human decides
    res2 = decide([a, b], make_ctx(standing_authority_contract=True))
    assert res2["outcome"] == "EXECUTE"
    assert res2["selected"] == "conseq"


def test_param_deviation_forces_brief():
    sneaky = dataclasses.replace(
        V21Params(), q_weights={**{d: 0.1 for d in Q_DIMS},
                                "simplicity": 0.4})
    # weights must still sum to 1: 6*0.1 + 0.4 = 1.0
    a = make_option("a")
    b = make_option("b", pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1)
    res = decide([a, b], make_ctx(params=sneaky))
    assert res["param_deviation"] is True
    assert res["outcome"] == "BRIEF"
    assert res["receipt"]["param_deviation"] is True


# ---------------------------------------------------------------------------
# N4: mandatory baselines are always in the candidate set
# ---------------------------------------------------------------------------

def test_mandatory_baselines_injected():
    a = make_option("a")
    ctx = make_ctx()
    injected = inject_mandatory_baselines([a], ctx)
    ids = {o.id for o in injected}
    assert ctx.baseline.id in ids
    assert "mandatory:gather-evidence" in ids
    assert "mandatory:reversible-probe" in ids
    assert "mandatory:rollback" in ids
    assert "mandatory:escalate" in ids


def test_bad_baseline_is_auditable():
    rigged = make_option("baseline",
                         pv=PVComponents(benefit=100.0))  # inflated baseline
    a = make_option("a")
    res = decide([a], make_ctx(baseline=rigged))
    # Everything looks negative against the rigged baseline...
    mine = next(s for s in res["options"] if s["id"] == "a")
    assert mine["dV_pred"] < 0
    # ...but the receipt exposes the baseline for audit.
    assert res["receipt"]["baseline_id"] == "baseline"


# ---------------------------------------------------------------------------
# Verification: provisional PASS, windows, calibration
# ---------------------------------------------------------------------------

def test_d_verified_clamps_display_scale():
    assert d_verified(25.0) == pytest.approx(9.0)
    assert d_verified(-12.5) == pytest.approx(-9.0)
    assert d_verified(3.25) == pytest.approx(3.25)


def test_ladder_advancing_neutral_degrading():
    assert ladder_step(0.0, 3.0)["state"] == "ADVANCING"
    assert ladder_step(0.0, 0.0)["state"] == "NEUTRAL"
    assert ladder_step(5.0, -2.0)["ladder"] == pytest.approx(3.0)


def test_observation_window_and_provisional_pass():
    assert observation_window_days("financial") == pytest.approx(7.0)
    a = make_option("a", pv=PVComponents(benefit=8.0, harm=0.5, cost=1.0, risk=0.5),
                    residual_risk=0.2)
    b = make_option("b", pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1)
    res = decide([a, b], make_ctx())
    rec = record_observation(res["receipt"], dV_actual=5.5,
                             harm_category="financial")
    v = rec["verification"]
    assert v["state"] == "PASS_PENDING_WINDOW"
    assert v["window_days"] == pytest.approx(7.0)
    assert v["d_verified"] == pytest.approx(5.5)
    assert v["calibration_error"] == pytest.approx(abs(6.0 - 5.5))
    confirmed = confirm_window(rec, harm_detected=False)
    assert confirmed["verification"]["state"] == "CONFIRMED"


def test_delayed_harm_reopens_record():
    a = make_option("a")
    res = decide([a], make_ctx())
    rec = record_observation(res["receipt"], dV_actual=4.0,
                             harm_category="reversible_low")
    reopened = confirm_window(rec, harm_detected=True)
    assert reopened["verification"]["state"] == "REOPENED"


def test_large_calibration_error_raises_learn_candidate():
    a = make_option("a", pv=PVComponents(benefit=8.0, harm=0.5, cost=1.0, risk=0.5),
                    residual_risk=0.2)
    b = make_option("b", pv=PVComponents(benefit=4.0, harm=0.5, cost=1.0, risk=0.5),
                    q_scores=_q(9.8), residual_risk=0.1)
    res = decide([a, b], make_ctx())
    rec = record_observation(res["receipt"], dV_actual=-5.0,
                             harm_category="reversible_low")
    assert rec["verification"]["learn_candidate"] is True


# ---------------------------------------------------------------------------
# Plan-level assessment: anti action-splitting / authorization laundering
# ---------------------------------------------------------------------------

def test_plan_value_laundering_flagged():
    s1 = make_option("s1", pv=PVComponents(benefit=6.0))
    s2 = make_option("s2", pv=PVComponents(benefit=6.0))
    plan = evaluate_plan("p1", [s1, s2], PVComponents(benefit=2.0, harm=8.0),
                         make_ctx())
    assert plan["value_laundering_suspected"] is True


def test_plan_authorization_laundering_flagged():
    s1 = make_option("s1", pv=PVComponents(benefit=6.0))
    s2 = make_option("s2", pv=PVComponents(benefit=6.0),
                     requires_authority=True)  # smuggled past the plan gate
    plan = evaluate_plan("p2", [s1, s2], PVComponents(benefit=10.0),
                         make_ctx())
    assert plan["authorization_laundering_suspected"] is True
    assert plan["plan_gate"] == NEEDS_AUTHORITY


def test_step_pvs_are_not_summed_into_plan_pv():
    s1 = make_option("s1", pv=PVComponents(benefit=6.0))
    plan = evaluate_plan("p3", [s1], PVComponents(benefit=1.0), make_ctx())
    assert plan["plan_pv"] == pytest.approx(1.0)
    assert plan["steps_pv_sum"] == pytest.approx(6.0)
