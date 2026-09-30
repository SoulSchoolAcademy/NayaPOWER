import pytest

from kernel.value_calculus import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    build_decision_receipt,
    calibration_summary,
    contribution_points,
    contribution_value_score,
    delta_value,
    evaluate_candidates,
    gate_candidate,
    independent_recompute,
    score_quality,
    verification_state,
)


@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


def pv(B=8, H=0, C=1, R=0.2, conf=0.95, evidence_count=3):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def quality(score=9.5, conf=0.95, **overrides):
    dims = {
        "objective_fit": score,
        "evidence_sufficiency": score,
        "applicability": score,
        "robustness": score,
        "reversibility": score,
        "blast_containment": score,
        "simplicity": score,
    }
    dims.update(overrides)
    return dims, {k: conf for k in dims}


def cand(cid, *, baseline=False, B=8, score=9.5, conf=0.95, **kwargs):
    q, c = quality(score, conf)
    return Candidate(
        cid, q, c, pv(B=B, conf=conf), authorized=True, reversible=True,
        human_authorized=False, is_baseline=baseline, **kwargs
    )


def test_q_is_pure_decision_quality_not_value(profile):
    q, c = quality(9.5, 0.95)
    low_value = Candidate("low", q, c, pv(B=2), authorized=True)
    high_value = Candidate("high", q, c, pv(B=200), authorized=True)
    assert score_quality(low_value, profile)["Q"] == pytest.approx(score_quality(high_value, profile)["Q"])


def test_baseline_relative_delta(profile):
    base = cand("base", baseline=True, B=5)
    option = cand("option", B=8)
    assert delta_value(base, base, profile) == pytest.approx(0)
    assert delta_value(option, base, profile) > 0


def test_four_state_gates(profile):
    q, c = quality()
    assert gate_candidate(Candidate("x", q, c, pv(), authorized=True, hard_violation=True), profile, RiskPolicy())[0] == PROHIBITED
    assert gate_candidate(Candidate("x", q, c, pv(), authorized=False), profile, RiskPolicy())[0] == NEEDS_AUTHORITY
    assert gate_candidate(Candidate("x", q, c, pv(evidence_count=0), authorized=True), profile, RiskPolicy())[0] == NEEDS_EVIDENCE
    assert gate_candidate(Candidate("x", q, c, pv(), authorized=True), profile, RiskPolicy())[0] == ADMISSIBLE


def test_critical_confidence_cannot_be_averaged_away(profile):
    q, c = quality()
    c["robustness"] = 0.1
    x = Candidate("x", q, c, pv(), authorized=True)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "CRITICAL_CONFIDENCE_FLOOR" in reasons


def test_component_confidence_floor_blocks_uncertainty_laundering(profile):
    q, c = quality()
    x = Candidate("x", q, c, pv(conf=0.4), authorized=True)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "PV_COMPONENT_CONFIDENCE_FLOOR" in reasons


def test_tail_risk_cannot_be_outscored(profile):
    q, c = quality(10, 1)
    x = Candidate(
        "x", q, c, pv(B=100, conf=1), authorized=True,
        tails=(TailRisk(10, 0.10, "catastrophic"),),
    )
    assert gate_candidate(x, profile, RiskPolicy())[0] == PROHIBITED


def test_action_splitting_inherits_plan_stakes(profile):
    q, c = quality()
    step = Candidate(
        "step", q, c, pv(), authorized=True, stakes="low", plan_stakes="consequential",
        human_authorized=False,
    )
    gate, reasons, _ = gate_candidate(step, profile, RiskPolicy())
    assert gate == NEEDS_AUTHORITY
    assert "CONSEQUENTIAL_OR_IRREVERSIBLE" in reasons


def test_distributional_harm_beats_aggregate_value(profile):
    q, c = quality()
    x = Candidate(
        "x", q, c, pv(B=100), authorized=True,
        stakeholder_harms={"minority": 9.5},
    )
    assert gate_candidate(x, profile, RiskPolicy(max_stakeholder_harm=9))[0] == PROHIBITED


@pytest.mark.parametrize("flag", ["principal_conflict", "coordination_conflict", "jurisdiction_conflict"])
def test_multi_principal_ai_and_jurisdiction_conflicts_escalate(profile, flag):
    q, c = quality()
    x = Candidate("x", q, c, pv(), authorized=True, **{flag: True})
    assert gate_candidate(x, profile, RiskPolicy())[0] == NEEDS_AUTHORITY


def test_pareto_and_relative_margin_select_clear_low_risk_winner(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9)
    b = cand("b", B=7)
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == "EXECUTE"
    assert ev["selected"] == "a"
    assert ev["relative_margin"] >= profile.relative_margin


def test_near_tie_briefs_instead_of_auto_execution(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9.0)
    b = cand("b", B=8.8)
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == "BRIEF"


def test_bad_baseline_is_rejected(profile):
    with pytest.raises(ValueError):
        evaluate_candidates([cand("x")], "missing", profile)


def test_provisional_pass_reopens_for_delayed_harm_window():
    assert verification_state(True, False, True) == "PASS_PENDING_WINDOW"
    assert verification_state(True, True, True) == "VERIFIED_PASS"
    assert verification_state(False, False, True) == "FAIL"


def test_decision_receipt_and_independent_recompute(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9)
    ev = evaluate_candidates([base, a], "base", profile)
    receipt = build_decision_receipt(
        decision_id="D-1",
        objective=profile.objective,
        baseline_id="base",
        stakeholders=["human-director"],
        horizon="bounded-run",
        evaluation=ev,
        authority_basis="standing low-risk authority",
        evidence_refs=["test:e1"],
        observation_window={"status": "open", "ends_at": None},
        verification="PASS_PENDING_WINDOW",
    )
    assert receipt["receipt_type"] == "ALIGNMENT_DECISION"
    reread = independent_recompute(receipt, [base, a], profile)
    assert reread["matches_decision"]
    assert reread["matches_selected"]


def test_prediction_inflation_detected_after_sampled_records():
    records = [
        {"delta_v_predicted": 8, "delta_v_actual": 2},
        {"delta_v_predicted": 7, "delta_v_actual": 2},
        {"delta_v_predicted": 6, "delta_v_actual": 1},
    ]
    cal = calibration_summary(records)
    assert cal["overprediction_detected"]
    assert cal["confidence_multiplier"] < 1


def test_reward_hacking_prediction_accuracy_does_not_create_contribution_points():
    cvs = contribution_value_score(
        quality=1, relevance=1, verification=0, impact=1, novelty=1, verified_delta=100
    )
    assert cvs == 0
    assert contribution_points(cvs, points_per_unit=100) == 0


def test_spam_like_low_novelty_is_strongly_discounted():
    high = contribution_value_score(
        quality=1, relevance=1, verification=1, impact=1, novelty=1, verified_delta=5
    )
    repeat = contribution_value_score(
        quality=1, relevance=1, verification=1, impact=1, novelty=0.01, verified_delta=5
    )
    assert repeat < high / 2


def test_negative_contribution_never_auto_subtracts_profile_points():
    cvs = contribution_value_score(
        quality=1, relevance=1, verification=1, impact=1, novelty=1, verified_delta=-5
    )
    assert cvs < 0
    assert contribution_points(cvs, points_per_unit=100) == 0


def test_weight_manipulation_cannot_add_unknown_dimensions():
    bad = QualityProfile("x", "2.1", "o", priorities={"objective_fit": 1, "pet_option": 999})
    with pytest.raises(ValueError):
        bad.weights()
