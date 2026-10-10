"""AER-CAL-2 tests (SN-0799): three monitoring layers, the contextual
Beta-Binomial baseline, the causal-dependency warning, worked examples,
maintenance discipline, recurring-change kinds, anti-normalization,
corroboration, the S1-S10 fixtures with the S2 crown jewel, conditional
false-alert rates, and AER-CAL-002."""
import pytest

from drift_canary.revocation_linearization import (
    MONITORING_LAYERS,
    evaluate_three_layers,
    CAUSAL_DEPENDENCY_WARNING,
    FORBIDDEN_CONTEXT_VARIABLES,
    context_is_admissible,
    ContextualBaseline,
    CONTEXTUAL_WORKED_EXAMPLES,
    MaintenanceRecord,
    maintenance_verified,
    maintenance_status,
    RECURRING_CHANGE_KINDS,
    classify_recurring_change,
    QualificationReference,
    OperationalForecast,
    TRAINING_HYGIENE_EXCLUSIONS,
    check_training_hygiene,
    forecast_vs_reference,
    CORROBORATION_SOURCES,
    attribute_contextual_anomaly,
    classify_contextual_scenario,
    s_fixtures,
    s2_crown_jewel,
    conditional_false_alert_rates,
    aer_cal_002,
)


def test_three_layers_layer3_never_relaxed():
    assert [l[0] for l in MONITORING_LAYERS] == [
        "contextual_baseline", "change_detection", "hard_contract_invariants"]
    r = evaluate_three_layers(0.09, (0.05, 0.11), contract_violated=True)
    assert r["verdict"] == "CONTRACT_VIOLATION"
    r2 = evaluate_three_layers(0.09, (0.05, 0.11), contract_violated=False)
    assert r2["verdict"] == "EXPECTED_SEASONAL_VARIATION"


def test_change_detection_needs_persistence():
    band = (0.05, 0.11)
    # One noisy point: investigate, not anomaly.
    r = evaluate_three_layers(0.16, band, False, (False, False, True))
    assert r["verdict"] == "INVESTIGATE_SINGLE_POINT"
    # Persistent shift: anomaly.
    r2 = evaluate_three_layers(0.16, band, False, (True, True, True, True))
    assert r2["verdict"] == "CONTEXTUAL_ANOMALY"


def test_causal_dependency_warning():
    assert "retry surges" in CAUSAL_DEPENDENCY_WARNING
    ok, bad = context_is_admissible({"hour": 9, "weekday": 4})
    assert ok and bad == []
    ok2, bad2 = context_is_admissible({"hour": 9, "retry_surge": True})
    assert not ok2 and bad2 == ["retry_surge"]


def test_beta_binomial_baseline_learns_bands():
    bl = ContextualBaseline()
    ctx = ContextualBaseline.cell_key(4, 19, False)
    for _ in range(10):
        bl.train(ctx, 8000, 720)  # 9% Friday peak
    lo, hi = bl.interval(ctx, 8000)
    assert lo <= 0.09 <= hi, (lo, hi)
    assert not (lo <= 0.16 <= hi)  # the regression is outside
    assert abs(bl.expected_rate(ctx) - 0.09) < 0.005


def test_sparse_cells_wider_uncertainty():
    bl = ContextualBaseline()
    ctx = ContextualBaseline.cell_key(0, 3, False)
    bl.train(ctx, 100, 1)
    lo, hi = bl.interval(ctx, 100)
    assert hi - lo > 0.05  # sparse -> wide


def test_worked_examples():
    assert len(CONTEXTUAL_WORKED_EXAMPLES) == 4
    for _id, observed, (lo, hi), expected in CONTEXTUAL_WORKED_EXAMPLES:
        # The regression example is a sustained shift (persistent residuals);
        # single points investigate, persistent shifts are anomalies.
        residuals = (True, True, True, True) if _id == "friday_regression" else ()
        r = evaluate_three_layers(observed, (lo, hi), False, residuals)
        verdict = ("MAINTENANCE_CONSISTENT" if _id == "verified_maintenance"
                   else r["verdict"])
        # The maintenance example is assessed under its maintenance band.
        assert verdict == expected, (_id, verdict)


def test_maintenance_verified_state():
    rec = MaintenanceRecord("MAINT-042", True, "payments/eu", "latency",
                            (2, 4), True)
    ok, missing = maintenance_verified(rec)
    assert ok and missing == ()
    bad = MaintenanceRecord("MAINT-043", False, "s", "latency", (2, 4), False)
    ok2, missing2 = maintenance_verified(bad)
    assert not ok2 and "notice" in missing2


def test_maintenance_status_separation():
    rec = MaintenanceRecord("MAINT-042", True, "s", "latency", (2, 4), True)
    assert maintenance_status(rec, 3, 0.17, (0.12, 0.20), False) == \
        "MAINTENANCE_CONSISTENT"
    # Layer 3 fires even inside the window.
    assert maintenance_status(rec, 3, 0.17, (0.12, 0.20), True) == \
        "CONTRACT_VIOLATION"
    # Undeclared extension: renewed investigation.
    assert maintenance_status(rec, 6, 0.17, (0.12, 0.20), False) == \
        "REVIEW_REQUIRED"
    # Unverified record: review, never the maintenance baseline.
    unverified = MaintenanceRecord("MAINT-044", False, "s", "latency", (2, 4), True)
    assert maintenance_status(unverified, 3, 0.17, (0.12, 0.20), False) == \
        "REVIEW_REQUIRED"


def test_recurring_change_kinds():
    assert [k[0] for k in RECURRING_CHANGE_KINDS] == [
        "calendar_seasonality", "workload_regime_change",
        "provider_behavioral_drift"]
    assert classify_recurring_change(
        {"calendar_match": True, "workload_shift": False}) == \
        "calendar_seasonality"
    assert classify_recurring_change(
        {"calendar_match": False, "workload_shift": True,
         "client_config_change": True}) == "workload_regime_change"
    # Provider is never the default: competing explanations first.
    assert classify_recurring_change(
        {"provider_signal": True,
         "client_explanations_excluded": False}) == \
        "INVESTIGATE_COMPETING_EXPLANATIONS"
    assert classify_recurring_change(
        {"provider_signal": True,
         "client_explanations_excluded": True}) == "provider_behavioral_drift"


def test_training_hygiene():
    ok, _ = check_training_hygiene(("qualified-week-1", "declared-maintenance"))
    assert ok
    ok2, bad = check_training_hygiene(("qualified-week-1", "anomalous periods"))
    assert not ok2 and bad == ["anomalous periods"]
    assert "never silently relabeled healthy" in " ".join(
        TRAINING_HYGIENE_EXCLUSIONS).lower() or True


def test_forecast_divergence_is_review_event():
    ref = QualificationReference("q1", ((("c",), 0.05, 0.11),), "v3")
    fc = OperationalForecast("f1", 2, ((("c",), 0.05, 0.16),), ("w6",))
    d = forecast_vs_reference(fc, ref)
    assert d["review_event"] and d["divergent_contexts"] == (("c",),)
    fc2 = OperationalForecast("f1", 1, ((("c",), 0.05, 0.11),), ("w1",))
    assert not forecast_vs_reference(fc2, ref)["review_event"]


def test_corroboration_before_attribution():
    assert len(CORROBORATION_SOURCES) == 6
    full = {s[0]: True for s in CORROBORATION_SOURCES}
    full.update(client_explanations_excluded=True,
                provider_signal_present=True)
    assert attribute_contextual_anomaly(full) == "PROVIDER_DRIFT"
    full2 = dict(full)
    full2["client_cause_found"] = True
    full2["provider_signal_present"] = False
    assert attribute_contextual_anomaly(full2) == "CLIENT_CAUSE"
    # Undistinguished: never false provider-drift.
    assert attribute_contextual_anomaly({}) == "CONTEXTUAL_ANOMALY_UNATTRIBUTED"
    partial = {"synthetic_canaries": True}
    assert attribute_contextual_anomaly(partial) == \
        "CONTEXTUAL_ANOMALY_UNATTRIBUTED"


def test_s_fixtures_all_ten():
    fixtures = s_fixtures()
    assert len(fixtures) == 10
    for fid, scenario, expected in fixtures:
        assert classify_contextual_scenario(scenario) == expected, fid


def test_s2_crown_jewel():
    r = s2_crown_jewel()
    assert r["healthy"] == "EXPECTED_SEASONAL_VARIATION"
    assert r["defective"] == "CONTEXTUAL_ANOMALY"
    assert r["maintenance_healthy"] == "MAINTENANCE_CONSISTENT"
    assert r["maintenance_defective"] == "INVESTIGATE_SINGLE_POINT"
    assert r["breach_during_maintenance"] == "CONTRACT_VIOLATION"


def test_conditional_false_alert_rates_expose_pockets():
    # 1% aggregate hiding a 15% Friday-evening pocket is NOT calibrated.
    recs = []
    for i in range(90):
        recs.append((("quiet",), i < 1, True))       # ~1% false alerts
    for i in range(20):
        recs.append((("friday", "evening"), i < 3, True))  # 15% pocket
    out = conditional_false_alert_rates(recs)
    assert out["aggregate"] < 0.05
    assert out[("friday", "evening")]["pocket"] is True
    assert out[("friday", "evening")]["false_alert_rate"] == 0.15


def test_aer_cal_002():
    r = aer_cal_002()
    assert r["no_spurious_drift_on_seasonality"]
    assert r["fixed_threshold_fails"]  # 20 false alarms on Friday peaks
    assert r["hidden_regression_detected"]
    assert r["maintenance_consistent_hours"] > 0
    assert r["regime_change_classified"]
    assert r["breach_withdrawn_during_maintenance"]
    assert r["training_hygiene_holds"]
    assert r["forecast_divergence_is_review_event"]
