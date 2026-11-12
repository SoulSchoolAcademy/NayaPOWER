"""AER-CAL-3 tests (SN-0800): three references, two-speed learning,
training-data classification, demand vs failure acceptance, the promotion
gate, dual-reference comparison, settlement watermarks, race-safe promotion,
the B1-B6 fixtures, the six mutation tests, learning receipts, AER-CAL-003."""
import pytest

from drift_canary.revocation_linearization import (
    AdaptiveCandidate,
    PromotedBaseline,
    CANDIDATE_STATUSES,
    TWO_SPEED_LEARNING,
    learning_speed,
    TRAINING_DATA_STATES,
    training_eligible,
    assess_distribution_change,
    PROMOTION_OBLIGATIONS,
    PROMOTE_CONJUNCTS,
    check_promotion_obligations,
    promote_bn,
    IncidentExposureRecord,
    dual_reference_evaluate,
    w1_w6_illustration,
    settlement_eligible,
    claim_data_eligible,
    BaselinePromotionLog,
    BaselineCandidateReceipt,
    b_fixtures,
    classify_b_fixture,
    b_blind_pair,
    cal3_mutation_tests,
    aer_cal_003,
    QualificationReference,
    OperationalForecast,
)


def _full_obligations(**overrides):
    ev = {ob: True for ob in PROMOTION_OBLIGATIONS}
    ev.update(overrides)
    return ev


def test_three_references_and_statuses():
    assert list(CANDIDATE_STATUSES) == [
        "CANDIDATE", "SHADOW", "INDEPENDENTLY_QUALIFIED", "PROMOTED"]
    c = AdaptiveCandidate("c1", 1, (), ("VERIFIED_HEALTHY",), True, "SHADOW")
    assert c.shadow and c.status == "SHADOW"  # shadow never grants qualification


def test_two_speed_learning():
    assert [s[0] for s in TWO_SPEED_LEARNING] == [
        "demand_timing_mix", "error_latency_failure"]
    assert learning_speed("demand") == "fast"
    assert learning_speed("failure") == "evidence_gated"
    assert learning_speed("latency") == "evidence_gated"


def test_seven_training_states():
    assert len(TRAINING_DATA_STATES) == 7
    for eligible_state in ("VERIFIED_HEALTHY", "VERIFIED_WORKLOAD_SHIFT",
                           "DECLARED_MAINTENANCE", "INDEPENDENTLY_CLEARED"):
        ok, _ = training_eligible(eligible_state)
        assert ok, eligible_state
    for forbidden in ("UNRESOLVED_ANOMALY", "CONFIRMED_REGRESSION",
                      "INSUFFICIENT_OBSERVABILITY"):
        ok, why = training_eligible(forbidden)
        assert not ok, forbidden
        assert "not admissible" in why


def test_demand_vs_failure_acceptance():
    d = assess_distribution_change("demand", 10000, 50000,
                                   justification="capacity verified")
    assert d["accepted"] and d["path"] == "fast"
    f = assess_distribution_change("failure", 0.01, 0.03, justification="")
    assert not f["accepted"]
    assert "not evidence it became acceptable" in f["note"]
    f2 = assess_distribution_change("failure", 0.01, 0.03,
                                    justification="independent root-cause + fix verified")
    assert f2["accepted"]


def test_eight_obligations_no_aggregate_score():
    res = check_promotion_obligations(_full_obligations())
    assert all(res.values()) and len(res) == 8
    res2 = check_promotion_obligations(
        _full_obligations(independent_qualification=False))
    assert not res2["independent_qualification"]
    # 7/8 is not "almost promotable".
    holds, missing = promote_bn(res2)
    assert not holds and missing == ("independent_qualification",)


def test_promote_bn_six_conjuncts():
    assert len(PROMOTE_CONJUNCTS) == 6
    holds, missing = promote_bn(_full_obligations())
    assert holds and missing == ()
    # predictive_quality / false_alert_control are continuous, not conjuncts.
    assert "predictive_quality" not in PROMOTE_CONJUNCTS
    assert "false_alert_control" not in PROMOTE_CONJUNCTS


def test_dual_reference_divergence_is_the_signal():
    d = dual_reference_evaluate(0.13, (0.05, 0.11), (0.06, 0.15))
    assert d["verdict"] == "DIVERGENCE_IS_THE_SIGNAL"
    assert d["qualified"] == "ANOMALY" and d["forecast"] == "normal"


def test_w1_w6_forecast_adapts_reference_holds():
    weeks = w1_w6_illustration()
    assert len(weeks) == 6
    assert weeks[0].disposition == "AGREE_NORMAL"
    assert weeks[-1].disposition == "DIVERGENCE_IS_THE_SIGNAL"
    assert all(isinstance(w, IncidentExposureRecord) for w in weeks)


def test_settlement_watermark():
    assert settlement_eligible(100.0, 50.0, 150.0)
    assert not settlement_eligible(100.0, 50.0, 149.9)
    ok, why = claim_data_eligible("OP-127", 100.0, 50.0, 120.0)
    assert not ok and "not yet settled" in why


def test_promotion_cas_and_status_gate():
    log = BaselinePromotionLog()
    cand = AdaptiveCandidate("c1", 1, (), ("VERIFIED_HEALTHY",), True, "SHADOW")
    log.propose(cand)
    r = log.promote_candidate(cand, 1, 1, 1, 1, "receipt-1")
    assert not r["promoted"]  # SHADOW cannot promote itself
    qual = AdaptiveCandidate("c1", 2, (), ("VERIFIED_HEALTHY",), True,
                             "INDEPENDENTLY_QUALIFIED")
    r2 = log.promote_candidate(qual, 999, 1, 1, 1, "receipt-1")
    assert not r2["promoted"] and "CAS mismatch" in r2["reason"]
    r3 = log.promote_candidate(qual, 2, 1, 1, 1, "",
                               unresolved_blockers=("INC-1",))
    assert not r3["promoted"]
    r4 = log.promote_candidate(qual, 2, 1, 1, 1, "receipt-1")
    assert r4["promoted"]
    assert isinstance(r4["baseline"], PromotedBaseline)
    assert r4["baseline"].calibration_receipt == "receipt-1"


def test_rollback_preserves_history():
    log = BaselinePromotionLog()
    cand = AdaptiveCandidate("c1", 1, (), ("VERIFIED_HEALTHY",), True,
                             "INDEPENDENTLY_QUALIFIED")
    log.promote_candidate(cand, 1, 1, 1, 1, "receipt-1")
    n = len(log.entries)
    rb = log.rollback("c1", "regression found", "receipt-2")
    assert rb["rolled_back"]
    assert len(log.entries) > n  # nothing erased
    assert rb["history_preserved"] == len(log.entries)


def test_b_fixtures_all_six():
    fixtures = b_fixtures()
    assert len(fixtures) == 6
    for fid, scenario, expected in fixtures:
        assert classify_b_fixture(scenario) == expected, fid


def test_b1_vs_b2_blind():
    r = b_blind_pair()
    assert r["distinguished"]


def test_b5_late_duplicate_withdraws():
    s = [s for i, s, _ in b_fixtures() if i == "B5"][0]
    assert classify_b_fixture(s) == "WITHDRAW_AND_REASSESS"


def test_cal3_mutation_tests_all_caught():
    results = cal3_mutation_tests()
    assert len(results) == 6
    assert all(v["caught"] for v in results.values())


def test_learning_receipt_reconstructability():
    r = BaselineCandidateReceipt(
        "BASELINE-CANDIDATE-018", "c1", 3, "verified demand growth",
        ("VERIFIED_WORKLOAD_SHIFT",), ("CONFIRMED_REGRESSION weeks",),
        "independent seat", ("failure deviations > 0.5pp",))
    assert r.receipt_id == "BASELINE-CANDIDATE-018"
    assert r.what_excluded and r.must_remain_detectable and r.verified_by


def test_aer_cal_003():
    r = aer_cal_003()
    assert r["lanes_distinguished"] == {"growth": "MAY_PROMOTE",
                                        "regression": "NEVER_NORMALIZE"}
    assert r["demand_adapts_in_both"]
    assert r["growth_promoted"] == 2
    assert r["mutated_model_normalizes_regression"]["detected"]
    assert r["receipt"]["id"] == "BASELINE-CANDIDATE-018"
    assert r["history_preserved_entries"] >= 1
    assert all(r["mutation_tests"].values())
