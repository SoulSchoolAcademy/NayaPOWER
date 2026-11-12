"""AER-DRIFT-1 tests (SN-0795): the drift state machine, atomic race-safe
withdrawal, current-use checks, exposure windows, selective containment,
the D1-D10 silent mutations, the two decisive properties, and AER-DRIFT-001."""
import pytest

from drift_canary.revocation_linearization import (
    DRIFT_TYPES,
    DRIFT_CAUSES,
    DRIFT_STATES,
    DRIFT_TRANSITIONS,
    DRIFT_SIGNALS,
    RISK_CLASSES,
    SELECTIVE_CONTAINMENT,
    ProviderQualificationManifest,
    make_manifest,
    PROVIDER_CONTRACT_DIMENSIONS,
    DriftResponseCoordinator,
    authorize_recovery_retry,
    exposure_window,
    window_covers_operation,
    containment_plan,
    detection_budget,
    freshness_ok,
    apply_drift_mutation,
    DriftMonitor,
    detection_soundness,
    containment_safety,
    aer_drift_001,
    MockExternalProvider,
    LogicalOperation,
)


def _manifest(scope="r1"):
    dims = tuple((d[0], d[1]) for d in PROVIDER_CONTRACT_DIMENSIONS)
    return make_manifest("mock-provider", "payments.charge", "v1", scope, dims)


def _coord(scope="r1"):
    return DriftResponseCoordinator(_manifest(scope))


def _op(key="OP-X"):
    return LogicalOperation(key, "payments", "hash",
                            authorization_rev=1, created_at_seq=1)


def test_four_drift_types_and_causes():
    assert [t[0] for t in DRIFT_TYPES] == [
        "scope_drift", "retention_drift", "concurrency_drift", "downstream_drift"]
    assert "INSUFFICIENT_EVIDENCE" in DRIFT_CAUSES  # the qualification may never have had it


def test_manifest_is_versioned_scope_bound_revocable():
    m = _manifest()
    assert m.manifest_id.startswith("PROVIDER-QUAL-27/")
    assert m.contract_revision == 1 and m.qualification_revision == 1
    assert m.scope == "r1" and m.current_status == "QUALIFIED_IN_SCOPE"


def test_five_signals_plus_freshness():
    assert len(DRIFT_SIGNALS) == 6
    assert DRIFT_SIGNALS[-1][0] == "evidence_freshness"


def test_state_machine_legal_path():
    c = _coord()
    assert c.transition("REVIEW_REQUIRED", "e1")["accepted"]
    assert c.transition("SUSPECTED_DRIFT", "e2")["accepted"]
    r = c.transition("QUALIFICATION_SUSPENDED", "e3")
    assert r["accepted"] and c.state == "QUALIFICATION_SUSPENDED"
    # Atomic with the fence: the same commit advances the revision AND fences.
    assert r["qualification_revision"] == 2
    assert c.fence == {"r1": 2}


def test_state_machine_illegal_transitions_rejected():
    c = _coord()
    r = c.transition("QUALIFICATION_SUSPENDED", "skip")
    assert not r["accepted"]
    assert c.state == "QUALIFIED_IN_SCOPE"


def test_requalified_scope_can_drift_again():
    c = _coord()
    c.withdraw_now("setup")
    c.transition("REQUALIFIED_IN_NEW_SCOPE", "requal")
    r = c.transition("REVIEW_REQUIRED", "new anomaly")
    assert r["accepted"], "the law has no statute of limitations"


def test_withdraw_now_fast_path():
    c = _coord()
    w = c.withdraw_now("L3: confirmed duplicate")
    assert w["state"] == "QUALIFICATION_SUSPENDED"
    assert [s for s, ok in w["steps"]] == [
        "REVIEW_REQUIRED", "SUSPECTED_DRIFT", "QUALIFICATION_SUSPENDED"]
    assert all(ok for _, ok in w["steps"])
    assert w["fence"] == {"r1": 2}


def test_authorize_retry_current_use_checks():
    c = _coord()
    ok = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                  "LAW-1", "RECONCILED")
    assert ok["authorized"], ok
    # Unknown outcome never authorizes.
    d = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                 "LAW-1", "UNKNOWN")
    assert not d["authorized"] and any("reconcile" in r for r in d["reasons"])
    # No LAW receipt never authorizes.
    d2 = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                  "", "RECONCILED")
    assert not d2["authorized"]


def test_authorize_retry_blocked_under_review_and_suspension():
    c = _coord()
    c.transition("REVIEW_REQUIRED", "anomaly")
    d = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                 "LAW-1", "RECONCILED")
    assert not d["authorized"]
    c.transition("SUSPECTED_DRIFT", "confirmed gap")
    c.transition("QUALIFICATION_SUSPENDED", "confirmed")
    d2 = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                  "LAW-1", "RECONCILED")
    assert not d2["authorized"]


def test_authorize_retry_old_revision_fence():
    c = _coord()
    c.withdraw_now("setup")
    c.transition("REQUALIFIED_IN_NEW_SCOPE", "requal")  # rev is now 2, fence r1=2
    # A worker presenting the OLD revision cannot rely on the fence being absent:
    # the fence demands >= 2 and the manifest carries 2 -- eligible again.
    d = authorize_recovery_retry(c, _op(), "r1", {"concurrency": True},
                                 "LAW-1", "RECONCILED")
    assert d["authorized"] and d["qualification_revision"] == 2


def test_exposure_window_unknown_start_requires_review():
    w = exposure_window(last_ok=None, first_bad=10, first_suspected=8,
                        declared=None, affected_scopes=("r1",))
    assert w.classification == "REQUIRES_REVIEW"
    assert w.earliest_plausible_boundary == 8  # never an invented start time


def test_exposure_window_bounded_and_per_operation():
    w = exposure_window(last_ok=5, first_bad=10, first_suspected=8,
                        declared=9, affected_scopes=("r1",))
    assert w.classification == "BOUNDED"
    covers, _ = window_covers_operation(w, "r1")
    assert covers
    covers2, why2 = window_covers_operation(w, "r2")
    assert not covers2  # never blanket-marked


def test_selective_containment_only_material_reliance():
    plan = containment_plan("scope_drift", "r2",
                            {"op-a": ("r1",), "op-b": ("r2",)})
    assert plan["contained"] == ("op-b",)
    assert plan["preserved"] == ("op-a",)
    assert len(plan["capabilities"]) == len(SELECTIVE_CONTAINMENT) == 6


def test_risk_classes_and_detection_budget():
    assert [r[0] for r in RISK_CLASSES] == ["HIGH", "MEDIUM", "LOW"]
    assert detection_budget("HIGH") == 1
    assert detection_budget("LOW") == 100


def test_freshness_expired_is_evidence_gap_not_misconduct():
    c = _coord()
    c.record_verification(0)
    ok, why = freshness_ok(c.manifest, now=50, risk_class="HIGH")
    assert not ok and "evidence gap" in why and "not provider misconduct" in why
    ok2, _ = freshness_ok(c.manifest, now=1, risk_class="HIGH")
    assert ok2


def test_drift_mutations_apply_silently():
    p = MockExternalProvider()
    assert apply_drift_mutation(p, "D3_atomic_guard_removal")["changed"]
    assert p.guard_mode == "broken_record_after_effect"
    assert p.contract_text_version == 1  # docs unchanged: behavior-only
    before = p.contract_text_version
    apply_drift_mutation(p, "D6_doc_only_change")
    assert p.contract_text_version == before + 1
    assert p.guard_mode == "broken_record_after_effect"  # behavior untouched
    with pytest.raises(ValueError):
        apply_drift_mutation(p, "DX_nope")


def test_detection_soundness():
    ok, _ = detection_soundness({
        "D3_atomic_guard_removal": {"confirmed_drift": True, "evidence": "canary"},
        "D6_doc_only_change": {"confirmed_drift": False},
        "D8_unrelated_errors": {"confirmed_drift": False},
    })
    assert ok
    bad, why = detection_soundness({
        "D3_atomic_guard_removal": {"confirmed_drift": True, "evidence": None},
    })
    assert not bad and "without independent evidence" in why
    bad2, why2 = detection_soundness({
        "D6_doc_only_change": {"confirmed_drift": True, "evidence": "vibes"},
    })
    assert not bad2 and "false attribution" in why2


def test_containment_safety_immediate_at_withdrawal():
    c = _coord()
    c.withdraw_now("L3")
    safe, why = containment_safety(c, "r1", _op())
    assert safe, why
    assert "immediately at withdrawal" in why


def test_containment_safety_precondition():
    c = _coord()
    safe, why = containment_safety(c, "r1", _op())
    assert not safe and "not suspended" in why


def test_monitor_is_blind_to_hidden_switches():
    p = MockExternalProvider()
    c = _coord()
    apply_drift_mutation(p, "D3_atomic_guard_removal")
    monitor = DriftMonitor(c, p)
    # The monitor never reads guard_mode / hidden switches -- only canaries.
    obs = monitor.canary_forced_race()
    assert obs["anomaly"] and obs["effects"] == 2
    assert not hasattr(monitor, "guard_mode")


def test_aer_drift_001():
    r = aer_drift_001()
    assert r["concurrency_drift_suspended"] == "QUALIFICATION_SUSPENDED"
    assert "immediately at withdrawal" in r["old_revision_retry_rejected"]
    assert r["restoration_does_not_restore"]
    assert r["requalified_retry_eligible"] == 2
    assert r["retention_drift_suspended"]
    assert r["scope_drift_selective_containment"]["preserved"] == ("op-a",)
    assert r["scope_drift_selective_containment"]["contained"] == ("op-b", "op-c")
    assert r["downstream_drift_suspended"]
    assert r["healthy_with_timeouts_no_violation"]
    assert r["doc_only_change_no_suspension"]
    assert r["detection_soundness"].startswith("sound")
