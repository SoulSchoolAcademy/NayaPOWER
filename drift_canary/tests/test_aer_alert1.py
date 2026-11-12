"""AER-ALERT-1 tests (SN-0796): the two-field incident model, the L0-L4
ladder, denominator-correct metrics, the 6-point evidence checklist,
attribution, the HTTP symptom classifier, the two-stage engine, the T1-T10
suite, and AER-ALERT-001."""
import pytest

from drift_canary.revocation_linearization import (
    ALERT_RESPONSES,
    ALERT_DIAGNOSES,
    ALERT_LADDER,
    L1_STATISTICAL_GATE,
    ProviderIncident,
    alert_metrics,
    DUPLICATE_COUNTEREXAMPLE_CHECKLIST,
    check_duplicate_counterexample,
    attribute_duplicate,
    HTTP_SYMPTOM_TABLE,
    classify_http_symptom,
    WITHDRAWAL_NODE_ROLES,
    evaluate_provider_signal,
    run_t_suite,
    t_suite_metrics,
    aer_alert_001,
    DriftResponseCoordinator,
    make_manifest,
    PROVIDER_CONTRACT_DIMENSIONS,
    MockExternalProvider,
)


def _coord():
    dims = tuple((d[0], d[1]) for d in PROVIDER_CONTRACT_DIMENSIONS)
    return DriftResponseCoordinator(
        make_manifest("mock-provider", "payments.charge", "v1", "r1", dims))


def _full_evidence(**overrides):
    ev = {i: True for i in DUPLICATE_COUNTEREXAMPLE_CHECKLIST}
    ev["client_misuse_excluded"] = True
    ev.update(overrides)
    return ev


def test_two_fields_distinguish_precaution_from_fact():
    inc = ProviderIncident("INC-9", "HOLD_AFFECTED_RETRIES", "SUSPECTED_DRIFT",
                           ("canary anomaly",), True)
    assert inc.response in ALERT_RESPONSES
    assert inc.diagnosis in ALERT_DIAGNOSES
    assert inc.precaution_before_diagnosis  # containment preceded proof: on the record


def test_ladder_shape_and_l1_gate_is_proposed_not_ratified():
    levels = [l[0] for l in ALERT_LADDER]
    assert levels == ["L0", "L1", "L2", "L3", "L4"]
    l3 = [l for l in ALERT_LADDER if l[0] == "L3"][0]
    assert "bypasses statistical thresholds" in l3[4]
    assert L1_STATISTICAL_GATE["min_comparable_requests"] == 100
    assert "not ratified settings" in L1_STATISTICAL_GATE["note"]


def test_metrics_denominators_are_logical_operations():
    # One operation retried 20x != 20 provider failures.
    subs = [("OP-M", "TIMEOUT_RAISED")] * 3 + [("OP-M", "COMMITTED")]
    subs += [("OP-N", "RATE_LIMITED"), ("OP-N", "COMMITTED")]
    m = alert_metrics(subs, {"OP-M": 1, "OP-N": 1}, {"OP-M", "OP-N"})
    assert m["distinct_logical_operations"] == 2
    assert m["timeout_rate"] == 0.5
    assert m["rate_limit_rate"] == 0.5
    assert m["confirmed_duplicate_effect_rate"] == 0.0


def test_metrics_disclose_unobserved_outcomes():
    subs = [("OP-A", "COMMITTED"), ("OP-B", "SUBMIT_RAISED")]
    m = alert_metrics(subs, {"OP-A": 1}, {"OP-A"})
    assert m["unobserved_outcomes_disclosed"] == ["OP-B"]
    assert m["observation_coverage"] == 0.5
    assert m["eligible_observably_reconciled"] == 1


def test_checklist_all_six_confirms():
    ok, missing = check_duplicate_counterexample(_full_evidence())
    assert ok and missing == ()


def test_checklist_missing_one_does_not_confirm():
    ev = _full_evidence()
    ev["not_duplicate_webhooks_or_logs_of_one_effect"] = False
    ok, missing = check_duplicate_counterexample(ev)
    assert not ok
    assert missing == ("not_duplicate_webhooks_or_logs_of_one_effect",)


def test_attribution_distinguishes_client_misuse():
    assert attribute_duplicate(
        _full_evidence(client_changed_key_per_retry=True,
                       client_misuse_excluded=False)) == "CLIENT_MISUSE"
    assert attribute_duplicate(_full_evidence()) == "PROVIDER_BREACH"
    ev = _full_evidence()
    ev["two_distinct_prohibited_material_effects"] = False
    assert attribute_duplicate(ev) == "UNDETERMINED"


def test_http_symptoms_are_inputs_never_verdicts():
    r = classify_http_symptom("403-installation-token")
    r2 = classify_http_symptom("403-policy-refusal")
    assert r["reading"] != r2["reading"]  # same family, different actions
    assert r["is_verdict"] is False
    assert "installation-token 403 vs comment-lock 403" in r["reflexive_note"]
    r3 = classify_http_symptom("two-verified-effects")
    assert "L3" in r3["reading"]


def test_withdrawal_node_roles_cover_all_seven():
    assert set(WITHDRAWAL_NODE_ROLES) == {
        "KNOW", "CONNECT", "VERIFY", "PROVE", "LAW", "ACT", "LEARN"}
    assert "never auto-restore provider-wide trust" in WITHDRAWAL_NODE_ROLES["LEARN"]


def test_engine_confirmed_duplicate_l3_immediate():
    c = _coord()
    r = evaluate_provider_signal(
        {"kind": "confirmed_duplicate", "evidence": _full_evidence(),
         "summary": "2 prohibited effects"}, c)
    assert r["level"] == "L3"
    assert r["diagnosis"] == "CONFIRMED_CONTRACT_BREACH"
    assert r["attribution"] == "PROVIDER_BREACH"
    assert c.state == "QUALIFICATION_SUSPENDED"
    assert c.fence == {"r1": 2}


def test_engine_incomplete_checklist_holds_undetermined():
    c = _coord()
    ev = _full_evidence()
    ev["authentic_complete_records"] = False
    r = evaluate_provider_signal(
        {"kind": "confirmed_duplicate", "evidence": ev, "summary": "?"}, c)
    assert r["level"] == "L2" and r["diagnosis"] == "UNDETERMINED"
    assert c.state == "QUALIFIED_IN_SCOPE"  # no withdrawal without proof
    assert "authentic_complete_records" in r["missing_checklist"]


def test_engine_telemetry_loss_never_healthy():
    c = _coord()
    r = evaluate_provider_signal({"kind": "telemetry_loss"}, c)
    assert r["diagnosis"] == "UNDETERMINED"
    assert "never 'healthy'" in r["note"]


def test_engine_single_unclear_canary_is_l1():
    c = _coord()
    r = evaluate_provider_signal({"kind": "single_unclear_canary"}, c)
    assert r["level"] == "L1" and c.state == "QUALIFIED_IN_SCOPE"


def test_t_suite_all_pass():
    results = run_t_suite()
    assert len(results) == 10
    for r in results:
        assert r["pass"], (r["id"], r)


def test_t_suite_metrics_with_honesty_clause():
    results = run_t_suite()
    m = t_suite_metrics(results)
    assert m["false_drift_attribution_rate"] == 0.0
    assert m["unsafe_continuation_rate"] == 0
    assert m["unnecessary_qualification_loss"] == 0
    assert m["suite_pass"]
    assert "finite corpus" in m["honesty_clause"]


def test_aer_alert_001():
    r = aer_alert_001()
    assert r["identical_transport_assessment"] in ("L0", "L1")
    assert r["h1_healthy_stays"] in ("L0", "L1")
    assert r["h2_duplicating_withdrawn"]["level"] == "L3"
    assert r["h2_duplicating_withdrawn"]["state"] == "QUALIFICATION_SUSPENDED"
    assert r["rate_limit_repeat"] in ("L0", "L1")
    assert r["expired_retention_repeat"] == "QUALIFIED"
    ds = r["downstream_only_duplication"]
    assert ds["root"] == 1 and ds["downstream"] == 2
