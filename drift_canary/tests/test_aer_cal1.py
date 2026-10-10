"""AER-CAL-1 tests (SN-0797) and the Alert Calibration Lab (SN-0798):
volume-adaptive strategies, safety/statistical separation, uncertainty
math, fleet-wide testing control, paired windows, materiality, versioned
profiles, replay calibration, and the five sealed histories A-E."""
import pytest

from drift_canary.revocation_linearization import (
    VOLUME_STRATEGIES,
    select_volume_strategy,
    SAFETY_STATISTICAL_SEPARATION,
    safety_or_statistical,
    se_proportion,
    zero_failure_upper_bound,
    ZERO_FAILURE_TABLE,
    n_eff_cluster_diagnostic,
    binomial_upper_p,
    STATISTICAL_MODELS,
    fleet_false_alarm_prob,
    alpha_budget_union,
    paging_decision,
    paired_window_decision,
    AlertCalibrationProfile,
    promote_profile,
    replay_period_metrics,
    replay_calibration,
    aer_cal_001,
    LAB_SETTINGS_NOTE,
    lab_histories,
    lab_diagnose,
    LAB_ACCEPTANCE_MATRIX,
    LAB_MATERIALITY_PP,
    LAB_ALPHA,
    calibration_lab,
)


def test_three_volume_strategies():
    assert [s[0] for s in VOLUME_STRATEGIES] == [
        "low_volume", "bursty", "high_volume"]
    assert select_volume_strategy(5, "low", "HIGH") == "low_volume"
    assert select_volume_strategy(500, "high", "MEDIUM") == "bursty"
    assert select_volume_strategy(100000, "low", "LOW") == "high_volume"
    # A provider may be high-volume overall yet low-volume for one endpoint.
    assert select_volume_strategy(12, "low", "HIGH") == "low_volume"


def test_safety_statistical_separation_table():
    kinds = [r[0] for r in SAFETY_STATISTICAL_SEPARATION]
    assert "confirmed duplicate" in kinds and "missing observability" in kinds


def test_safety_path_ignores_sample_size():
    for n in (1, 5, 100000):
        d = safety_or_statistical({"verified_duplicate_effects": 2,
                                   "sample_size": n})
        assert d["path"] == "safety"
        assert "ANY sample size" in d["action"]


def test_statistical_path_for_transport_errors():
    d = safety_or_statistical({"kind": "transport_burst"})
    assert d["path"] == "statistical"
    d2 = safety_or_statistical({"observability": "missing"})
    assert "never healthy" in d2["action"]


def test_se_proportion():
    assert abs(se_proportion(0.5, 100) - 0.05) < 1e-9
    assert se_proportion(0.1, 0) == float("inf")  # no data, no precision


def test_zero_failure_table():
    for n, expected in ZERO_FAILURE_TABLE:
        assert abs(zero_failure_upper_bound(n) - expected) < 0.002, n
    # Zero observed failures != zero risk: n=5 leaves a 45% upper bound.
    assert zero_failure_upper_bound(5) > 0.45


def test_n_eff_is_diagnostic_only():
    assert n_eff_cluster_diagnostic(400, 50) == 8.0


def test_binomial_upper_p_exact_small_n():
    # 5 requests, 1 timeout under a 2% baseline: 9.61%.
    assert abs(binomial_upper_p(5, 1, 0.02) - 0.0961) < 0.001


def test_statistical_model_table():
    assert len(STATISTICAL_MODELS) == 6
    assert STATISTICAL_MODELS[0][0] == "sparse"


def test_fleet_false_alarm_math():
    # 100 metrics x 1% -> 63%: per-metric control is not fleet control.
    assert abs(fleet_false_alarm_prob(100, 0.01) - 0.634) < 0.005


def test_alpha_budget_union_includes_restarts():
    assert abs(alpha_budget_union(100) - 0.0005) < 1e-12
    # Restarted tests spend budget again: the denominator grows.
    assert alpha_budget_union(100, restarts=100) < alpha_budget_union(100)


def test_paging_needs_all_three():
    assert paging_decision(0.001, True, True)
    assert not paging_decision(0.001, True, False)   # not actionable
    assert not paging_decision(0.001, False, True)   # not material
    assert not paging_decision(0.05, True, True)     # no signal: p alone never pages
    assert paging_decision(0.99, False, False, safety_invariant=True)  # exempt


def test_paired_windows():
    assert paired_window_decision(True, True, False) == "ALERT"
    assert paired_window_decision(False, True, False) == "OBSERVE"
    assert paired_window_decision(False, False, True) == "ACT_NOW"  # material overrides
    assert paired_window_decision(False, False, False, low_traffic=True) == \
        "EXTEND_WINDOW_AND_CANARY"


def test_profile_promotion_preserves_and_shadows():
    p0 = AlertCalibrationProfile("prof-1", 1, "low_volume", (("alpha", 0.01),),
                                 ("2026-09",), None, False, ("ev",))
    p1 = promote_profile(p0, (("alpha", 0.005),), ("ev2",))
    assert p1.version == 2
    assert p1.shadow_mode  # shadow first, no silent swaps
    assert p1.supersedes == "prof-1/v1"
    assert p1.baseline_periods == ("2026-09",)  # baselines carried, admissible only


def test_replay_period_metrics_five():
    recs = [
        {"truth": "healthy", "alert_raised": True, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
        {"truth": "drift", "alert_raised": True, "page_raised": False,
         "detection_delay": 3, "withdrawal": False},
        {"truth": "breach", "alert_raised": False, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
    ]
    m = replay_period_metrics(recs)
    assert m["false_incident_alerts"] == 1
    assert m["missed_material_incidents"] == 1
    assert m["detection_delay_median"] == 3
    assert m["unnecessary_withdrawals"] == 0


def test_replay_calibration_splits_periods():
    recs = [
        {"period": "t", "truth": "healthy", "alert_raised": False,
         "page_raised": False, "detection_delay": None, "withdrawal": False},
        {"period": "h", "truth": "drift", "alert_raised": True,
         "page_raised": False, "detection_delay": 2, "withdrawal": False},
    ]
    cal = replay_calibration(recs, ("t",), ("t",), ("h",))
    assert set(cal) == {"train", "calibration", "heldout"}
    assert cal["heldout"]["missed_material_incidents"] == 0
    assert cal["train"]["n"] == 1


def test_aer_cal_001():
    r = aer_cal_001()
    assert r["heldout_clean"]
    assert r["safety_ignores_sample_size"]
    assert r["zero_failure_table_verified"]
    assert r["profiles_stable"]
    assert abs(r["fleet_math"]["hundred_metrics_at_1pct"] - 0.634) < 0.005


def test_lab_settings_are_synthetic():
    assert "SYNTHETIC" in LAB_SETTINGS_NOTE
    assert "NOT validated production values" in LAB_SETTINGS_NOTE
    assert LAB_MATERIALITY_PP == 0.005 and LAB_ALPHA == 0.01


def test_lab_five_histories():
    hs = lab_histories()
    assert [h.history_id for h in hs] == ["A", "B", "C", "D", "E"]


def test_lab_only_E_breaches():
    rows = {h.history_id: lab_diagnose(h) for h in lab_histories()}
    breaches = [hid for hid, r in rows.items() if r["contract_breach_proven"]]
    assert breaches == ["E"]
    for hid, anomaly, breach, _retry in LAB_ACCEPTANCE_MATRIX:
        assert rows[hid]["statistical_anomaly"] == anomaly, hid
        assert rows[hid]["contract_breach_proven"] == breach, hid


def test_lab_A_sparse_no_drift():
    r = lab_diagnose(next(h for h in lab_histories() if h.history_id == "A"))
    assert r["statistical_anomaly"] is False
    assert "NO drift" in r["consequential_retry"]
    assert abs(r["p"] - 0.0961) < 0.005


def test_lab_B_one_correlated_incident():
    r = lab_diagnose(next(h for h in lab_histories() if h.history_id == "B"))
    assert "ONE correlated throttling incident" in r["consequential_retry"]
    assert "never 400 independent failures" in r["note"]


def test_lab_C_significant_but_immaterial():
    r = lab_diagnose(next(h for h in lab_histories() if h.history_id == "C"))
    assert r["statistical_anomaly"] is True
    assert r["p"] < 1e-4  # significant...
    assert r["material_pp"] == 0.15  # ...but immaterial
    assert "NO urgent page" in r["consequential_retry"]
    assert "NO drift from significance alone" in r["consequential_retry"]


def test_lab_D_material_but_drift_unproven():
    r = lab_diagnose(next(h for h in lab_histories() if h.history_id == "D"))
    assert r["material_pp"] == 1.5
    assert r["response"] == "L1-page"
    assert "drift REMAINS UNPROVEN" in r["consequential_retry"]


def test_lab_E_immediate_withdrawal():
    r = lab_diagnose(next(h for h in lab_histories() if h.history_id == "E"))
    assert r["statistical_anomaly"] == "bypassed"
    assert r["contract_breach_proven"] is True
    assert r["response"] == "L3"


def test_calibration_lab_full():
    r = calibration_lab()
    assert r["only_E_breaches"]
    assert r["safety_identical_across_volumes"]
    assert abs(r["low_volume_panel"]["p_ge_1_timeout_under_baseline"] - 0.0961) < 0.005
    assert abs(r["low_volume_panel"]["zero_failure_upper_bound_5"] - 0.451) < 0.005
    assert abs(r["fleet_math"]["hundred_metrics_at_1pct"] - 0.634) < 0.005
    assert abs(r["fleet_math"]["bonferroni_0_01_fleet"] - 0.0001) < 1e-12
    assert "SYNTHETIC" in r["settings_note"]
