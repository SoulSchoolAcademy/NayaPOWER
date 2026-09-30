import json

import pytest

from kernel.value_calculus import (
    ACT,
    ASK,
    READ_MORE,
    REFUSE,
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    build_contribution_receipt,
    build_decision_receipt,
    build_recalibration_receipt,
    calibration_summary,
    contribution_points,
    contribution_value_score,
    delta_value,
    evaluate_candidates,
    gate_candidate,
    independent_recompute,
    promote_recalibration,
    score_quality,
    value_interval,
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
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    hard.update({k: kwargs.pop(k) for k in list(kwargs) if k in hard})
    return Candidate(
        cid, q, c, pv(B=B, conf=conf), authorized=True, reversible=True,
        human_authorized=False, is_baseline=baseline, **hard, **kwargs
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
    assert gate_candidate(Candidate("x", q, c, pv(), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True), profile, RiskPolicy())[0] == ADMISSIBLE


def test_critical_confidence_cannot_be_averaged_away(profile):
    q, c = quality()
    c["robustness"] = 0.1
    x = Candidate("x", q, c, pv(), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "CRITICAL_CONFIDENCE_FLOOR" in reasons


def test_component_confidence_floor_blocks_uncertainty_laundering(profile):
    q, c = quality()
    x = Candidate("x", q, c, pv(conf=0.4), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "PV_COMPONENT_CONFIDENCE_FLOOR" in reasons


def test_tail_risk_cannot_be_outscored(profile):
    q, c = quality(10, 1)
    x = Candidate(
        "x", q, c, pv(B=100, conf=1), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        tails=(TailRisk(10, 0.10, "catastrophic"),),
    )
    assert gate_candidate(x, profile, RiskPolicy())[0] == PROHIBITED


def test_action_splitting_inherits_plan_stakes(profile):
    q, c = quality()
    step = Candidate(
        "step", q, c, pv(), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True, stakes="low", plan_stakes="consequential",
        human_authorized=False,
    )
    gate, reasons, _ = gate_candidate(step, profile, RiskPolicy())
    assert gate == NEEDS_AUTHORITY
    assert "CONSEQUENTIAL_OR_IRREVERSIBLE" in reasons


def test_distributional_harm_beats_aggregate_value(profile):
    q, c = quality()
    x = Candidate(
        "x", q, c, pv(B=100), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        stakeholder_harms={"minority": 9.5},
    )
    assert gate_candidate(x, profile, RiskPolicy(max_stakeholder_harm=9))[0] == PROHIBITED


@pytest.mark.parametrize("flag", ["principal_conflict", "coordination_conflict", "jurisdiction_conflict"])
def test_multi_principal_ai_and_jurisdiction_conflicts_escalate(profile, flag):
    q, c = quality()
    x = Candidate("x", q, c, pv(), authorized=True, lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True, **{flag: True})
    assert gate_candidate(x, profile, RiskPolicy())[0] == NEEDS_AUTHORITY


def test_pareto_and_relative_margin_select_clear_low_risk_winner(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9)
    b = cand("b", B=7)
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == ACT
    assert ev["selected"] == "a"
    assert ev["relative_margin"] >= profile.relative_margin


def test_near_tie_briefs_instead_of_auto_execution(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9.0)
    b = cand("b", B=8.8)
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == READ_MORE


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
    assert ev["relative_margin"] == pytest.approx(1.0)
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
    json.dumps(receipt, allow_nan=False)
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


def test_contribution_receipt_unverified_activity_gets_no_reward():
    receipt = build_contribution_receipt(
        contribution_id="C-raw-like",
        action_class="REACTION",
        provenance={"source": "feed"},
        privacy={"classification": "PRIVATE"},
        raw_activity={"reaction": "LIKE"},
        quality=0.9,
        relevance=0.9,
        verification_strength=0.9,
        impact=0.9,
        novelty=0.9,
        verified_delta=10,
        scoring_profile_id="NETWORK-VALUE-CANDIDATE",
        scoring_profile_version="0.1",
        points_per_unit=100,
        repeat_decay=1,
        evidence_refs=["event:1"],
        explanation="Activity is recorded but not verified contribution.",
        verification="UNVERIFIED",
    )
    assert receipt["receipt_type"] == "CONTRIBUTION_VALUE"
    assert receipt["cvs"] == 0
    assert receipt["points_awarded"] == 0
    json.dumps(receipt, allow_nan=False)


def test_verified_contribution_receipt_is_deterministic_and_rewardable():
    args = dict(
        contribution_id="C-verified-help",
        action_class="VERIFIED_HELP",
        provenance={"source": "smart-note"},
        privacy={"classification": "SHARED", "consent_state": "ACTIVE"},
        raw_activity={"kind": "answer"},
        quality=0.9,
        relevance=0.95,
        verification_strength=1.0,
        impact=0.8,
        novelty=0.85,
        verified_delta=5,
        scoring_profile_id="NETWORK-VALUE-CANDIDATE",
        scoring_profile_version="0.1",
        points_per_unit=100,
        repeat_decay=1,
        evidence_refs=["outcome:1"],
        explanation="Verified useful outcome.",
        verification="VERIFIED",
    )
    a = build_contribution_receipt(**args)
    b = build_contribution_receipt(**args)
    assert a == b
    assert a["cvs"] > 0
    assert a["points_awarded"] > 0
    assert a["scoring_profile"]["version"] == "0.1"


def test_repeat_decay_prevents_repetitive_activity_from_farming_points():
    common = dict(
        contribution_id="C-repeat",
        action_class="VERIFIED_HELP",
        provenance={"source": "feed"},
        privacy={"classification": "PUBLIC"},
        raw_activity={"kind": "reply"},
        quality=1,
        relevance=1,
        verification_strength=1,
        impact=1,
        novelty=1,
        verified_delta=1,
        scoring_profile_id="NETWORK-VALUE-CANDIDATE",
        scoring_profile_version="0.1",
        points_per_unit=100,
        evidence_refs=["outcome:2"],
        explanation="Repeat-decay test.",
        verification="VERIFIED",
    )
    first = build_contribution_receipt(**common, repeat_decay=1)
    repeated = build_contribution_receipt(**common, repeat_decay=0.1)
    assert repeated["points_awarded"] == pytest.approx(first["points_awarded"] * 0.1)


def test_negative_verified_contribution_is_evidence_not_automatic_point_punishment():
    receipt = build_contribution_receipt(
        contribution_id="C-negative",
        action_class="CORRECTION_CASE",
        provenance={"source": "review"},
        privacy={"classification": "PRIVATE"},
        raw_activity={"kind": "submission"},
        quality=1,
        relevance=1,
        verification_strength=1,
        impact=1,
        novelty=1,
        verified_delta=-2,
        scoring_profile_id="NETWORK-VALUE-CANDIDATE",
        scoring_profile_version="0.1",
        points_per_unit=100,
        repeat_decay=1,
        evidence_refs=["outcome:negative"],
        explanation="Negative outcome is preserved as evidence.",
        verification="VERIFIED",
    )
    assert receipt["cvs"] < 0
    assert receipt["points_awarded"] == 0


def test_explicit_value_interval_and_nonoverlap_rule(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9, uncertainty_penalty=0.2)
    b = cand("b", B=7, uncertainty_penalty=0.2)
    ia = value_interval(a, base, profile)
    ib = value_interval(b, base, profile)
    assert ia["v_low"] < ia["v_high"]
    assert ia["v_low"] > ib["v_high"]
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == ACT
    assert ev["interval_gap"] > profile.interval_epsilon


def test_overlapping_value_intervals_trigger_read_more(profile):
    base = cand("base", baseline=True, B=5)
    a = cand("a", B=9.0, uncertainty_penalty=0.5)
    b = cand("b", B=8.8, uncertainty_penalty=0.5)
    ev = evaluate_candidates([base, a, b], "base", profile)
    assert ev["decision"] == READ_MORE
    assert ev["interval_gap"] <= profile.interval_epsilon


def test_all_prohibited_is_explicit_refuse(profile):
    base = cand("base", baseline=True, B=5)
    q, c = quality()
    x = Candidate("x", q, c, pv(B=100), authorized=True, hard_violation=True)
    ev = evaluate_candidates([base, x], "base", profile)
    assert ev["decision"] == REFUSE
    row = next(r for r in ev["rows"] if r["candidate_id"] == "x")
    assert "JUDGMENT_RULE_HARD_STOP" in row["gate_reasons"]


def test_authority_boundary_is_explicit_ask(profile):
    base = cand("base", baseline=True, B=5)
    q, c = quality()
    x = Candidate("x", q, c, pv(B=9), authorized=False)
    ev = evaluate_candidates([base, x], "base", profile)
    assert ev["decision"] == ASK


def test_recalibration_is_versioned_and_cannot_self_promote(profile):
    records = [
        {"delta_v_predicted": 8, "delta_v_actual": 2},
        {"delta_v_predicted": 7, "delta_v_actual": 3},
        {"delta_v_predicted": 6, "delta_v_actual": 2},
    ]
    receipt = build_recalibration_receipt(
        current_profile=profile,
        proposed_version="2.1-cal-1",
        records=records,
        proposed_thresholds={"interval_epsilon": 0.1},
        evidence_refs=["ledger:1", "ledger:2", "ledger:3"],
    )
    assert receipt["state"] == "LEARN_CANDIDATE"
    assert receipt["automatic_promotion"] is False
    with pytest.raises(PermissionError):
        promote_recalibration(receipt, profile, verified=False, authorized=True)
    with pytest.raises(PermissionError):
        promote_recalibration(receipt, profile, verified=True, authorized=False)
    promoted = promote_recalibration(receipt, profile, verified=True, authorized=True)
    assert promoted.version == "2.1-cal-1"
    assert promoted.interval_epsilon == pytest.approx(0.1)


def test_unknown_hard_flags_never_silently_pass(profile):
    # Spec: "UNKNOWN never silently becomes PASS". A candidate whose hard
    # flags were never assessed must route to NEEDS_EVIDENCE, not ADMISSIBLE.
    q, c = quality()
    x = Candidate("x", q, c, pv(), authorized=True)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "HARD_GATE_UNKNOWN" in reasons
    for flag in ("UNKNOWN_LAW", "UNKNOWN_RIGHTS", "UNKNOWN_PRIVACY", "UNKNOWN_SAFETY"):
        assert flag in reasons


def test_hard_flag_defaults_are_unknown_not_true():
    # The insecure default (True) is gone: constructing without flags leaves
    # them unassessed instead of silently passing.
    q, c = quality()
    x = Candidate("x", q, c, pv(), authorized=True)
    assert x.lawful is None
    assert x.rights_safe is None
    assert x.privacy_safe is None
    assert x.safety_safe is None


@pytest.mark.parametrize("flag", ["lawful", "rights_safe", "privacy_safe", "safety_safe"])
def test_explicit_false_hard_flag_prohibits(profile, flag):
    q, c = quality()
    kwargs = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    kwargs[flag] = False
    x = Candidate("x", q, c, pv(), authorized=True, **kwargs)
    assert gate_candidate(x, profile, RiskPolicy())[0] == PROHIBITED


def test_unknown_hard_flags_yield_to_authority_routing(profile):
    # Gate precedence is preserved: an unauthorized candidate routes to
    # NEEDS_AUTHORITY even when hard flags are also unassessed.
    q, c = quality()
    x = Candidate("x", q, c, pv(), authorized=False)
    gate, reasons, _ = gate_candidate(x, profile, RiskPolicy())
    assert gate == NEEDS_AUTHORITY
    assert "AUTHORITY_MISSING" in reasons
