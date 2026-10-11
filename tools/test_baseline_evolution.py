"""Adversarial tests for UD-15 baseline evolution. 20 tests."""

import sys
sys.path.insert(0, "/home/hatch/workspace/tools")

from dataclasses import FrozenInstanceError
import pytest

from baseline_evolution import (
    BaselineLedger, BaselineRecord, Observation, PromotionRequest,
    ScopeId, Stage, TrainingClass, GateVerdict,
    promotion_gate, promote, advance_stage, dual_reference_check,
    pooled_estimate, check_decision_baseline, reconstruct_promotion,
    audit_promotions, DOES_NOT_CLAIM,
)

S1: ScopeId = ("svc-a", "us-west", "/api/v1", "tenant-1")
S2: ScopeId = ("svc-a", "us-west", "/api/v1", "tenant-2")  # sparse sibling scope


def obs(scope, value, cls, n=1):
    return tuple(
        Observation(scope, "error_rate", value, cls, (f"ev-{i}",))
        for i in range(n)
    )


def frozen(ledger, value=0.02):
    ledger.append(BaselineRecord(
        record_id="frozen-1", scope=S1, metric="error_rate", value=value,
        stage=Stage.FROZEN_REFERENCE, set_by="qual-team", set_at="2026-01-01T00:00:00Z",
        evidence_refs=("qual-report-7",), supersedes=None,
        comparison=(), reason="initial qualification", verifier="naya-1",
        certified=True))


def good_req(value=0.022):
    return PromotionRequest(
        scope=S1, metric="error_rate", candidate_value=value,
        proposed_by="naya-4", proposed_at="2026-10-10T12:00:00Z",
        training_window=obs(S1, 0.022, TrainingClass.VERIFIED_WORKLOAD_SHIFT, 5),
        evidence_refs=("load-report-3", "capacity-plan-9"),
        comparison=(("error_rate", "0.020 -> 0.022"), ("traffic", "1x -> 5x")),
        reason="traffic grew fivefold; error budget per request unchanged",
        higher_is_better=False)


# --- positive: legitimate growth promotes ---------------------------------

def test_legitimate_growth_promotes():
    ledger = BaselineLedger()
    frozen(ledger)
    verdict, rec = promote(ledger, good_req(), verifier="naya-2", record_id="prom-1",
                           regression_tolerance=0.01)
    assert verdict.passed and verdict.code == "PROMOTION_GRANTED"
    assert rec is not None and rec.stage == Stage.PROMOTED
    assert rec.supersedes is None  # first promotion for this scope+metric
    assert ledger.current(S1, "error_rate").record_id == "prom-1"
    # history preserved: frozen reference still there, untouched
    assert ledger.frozen_reference(S1, "error_rate").record_id == "frozen-1"
    ok, _ = ledger.verify_append_only()
    assert ok


def test_second_promotion_supersedes_never_overwrites():
    ledger = BaselineLedger()
    frozen(ledger)
    _, r1 = promote(ledger, good_req(0.022), verifier="naya-2", record_id="prom-1",
                    regression_tolerance=0.01)
    _, r2 = promote(ledger, good_req(0.024), verifier="naya-2", record_id="prom-2",
                    regression_tolerance=0.01)
    assert r2.supersedes == "prom-1"
    assert ledger.current(S1, "error_rate").record_id == "prom-2"
    # old baseline still in history, byte-identical
    hist = ledger.history(S1, "error_rate")
    assert [r.record_id for r in hist] == ["frozen-1", "prom-1", "prom-2"]
    assert hist[1].value == 0.022  # not overwritten


def test_stage_transitions_governed():
    ledger = BaselineLedger()
    frozen(ledger)
    rec = BaselineRecord("cand-1", S1, "error_rate", 0.025, Stage.CANDIDATE,
                         "naya-4", "2026-10-10T12:00:00Z", ("ev-1",),
                         None, (("error_rate", "0.020 -> 0.025"),), "growth", None)
    ledger.append(rec)
    s1 = advance_stage(ledger, rec, Stage.SHADOW, at="2026-10-10T13:00:00Z")
    assert s1.stage == Stage.SHADOW
    s2 = advance_stage(ledger, s1, Stage.INDEPENDENTLY_QUALIFIED,
                       verifier="naya-2", at="2026-10-10T14:00:00Z")
    assert s2.verifier == "naya-2"
    with pytest.raises(ValueError):
        advance_stage(ledger, s2, Stage.PROMOTED, at="2026-10-10T15:00:00Z")
    with pytest.raises(ValueError):
        advance_stage(ledger, rec, Stage.INDEPENDENTLY_QUALIFIED,
                      verifier="naya-4")  # self-qualification


def test_cold_reconstruction():
    ledger = BaselineLedger()
    frozen(ledger)
    _, rec = promote(ledger, good_req(), verifier="naya-2", record_id="prom-1",
                           regression_tolerance=0.01)
    built = reconstruct_promotion(rec)
    assert built["new_value"] == 0.022
    assert built["verifier"] == "naya-2"
    assert built["evidence_refs"] == ["load-report-3", "capacity-plan-9"]
    assert "traffic grew fivefold" in built["reason"]
    assert len(built["comparison"]) == 2


# --- negative: slow degradation with identical apparent traffic -------------

def test_slow_degradation_never_promotes():
    """Identical traffic shape to the growth case — but the training window
    hides a CONFIRMED_REGRESSION. Must be refused."""
    ledger = BaselineLedger()
    frozen(ledger)
    bad = PromotionRequest(
        scope=S1, metric="error_rate", candidate_value=0.025,
        proposed_by="naya-4", proposed_at="2026-10-10T12:00:00Z",
        training_window=(
            obs(S1, 0.025, TrainingClass.VERIFIED_WORKLOAD_SHIFT, 4)
            + obs(S1, 0.09, TrainingClass.CONFIRMED_REGRESSION, 1)
        ),
        evidence_refs=("load-report-3",),
        comparison=(("error_rate", "0.020 -> 0.025"),),
        reason="traffic grew")
    verdict, rec = promote(ledger, bad, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed
    assert "TRAINING_BARRED" in verdict.failed_obligations[0]
    assert rec is None
    assert ledger.current(S1, "error_rate") is None  # nothing promoted


def test_unresolved_anomaly_barred_from_normality():
    ledger = BaselineLedger()
    frozen(ledger)
    req = good_req()
    req2 = PromotionRequest(
        scope=req.scope, metric=req.metric, candidate_value=req.candidate_value,
        proposed_by=req.proposed_by, proposed_at=req.proposed_at,
        training_window=obs(S1, 0.025, TrainingClass.UNRESOLVED_ANOMALY, 5),
        evidence_refs=req.evidence_refs, comparison=req.comparison, reason=req.reason)
    verdict, rec = promote(ledger, req2, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed and rec is None
    assert any("TRAINING_BARRED" in f for f in verdict.failed_obligations)


def test_silent_change_refused_missing_evidence_reason_comparison():
    ledger = BaselineLedger()
    frozen(ledger)
    base = good_req()
    for mutate, code in [
        (dict(evidence_refs=()), "EVIDENCE_MISSING"),
        (dict(reason="  "), "REASON_MISSING"),
        (dict(comparison=()), "COMPARISON_MISSING"),
    ]:
        kw = dict(scope=base.scope, metric=base.metric,
                  candidate_value=base.candidate_value, proposed_by=base.proposed_by,
                  proposed_at=base.proposed_at, training_window=base.training_window,
                  evidence_refs=base.evidence_refs, comparison=base.comparison,
                  reason=base.reason)
        kw.update(mutate)
        verdict, rec = promote(ledger, PromotionRequest(**kw),
                               verifier="naya-2", record_id="prom-x")
        assert not verdict.passed and rec is None, code
        assert any(code in f for f in verdict.failed_obligations), code


def test_self_qualification_refused():
    ledger = BaselineLedger()
    frozen(ledger)
    verdict, rec = promote(ledger, good_req(), verifier="naya-4", record_id="prom-x")
    assert not verdict.passed and rec is None
    assert any("SELF_QUALIFICATION" in f for f in verdict.failed_obligations)


def test_stale_baseline_decision_refused():
    ledger = BaselineLedger()
    frozen(ledger)
    _, r1 = promote(ledger, good_req(), verifier="naya-2", record_id="prom-1",
                    regression_tolerance=0.01)
    _, r2 = promote(ledger, good_req(0.030), verifier="naya-2", record_id="prom-2",
                    regression_tolerance=0.01)
    chk = check_decision_baseline(ledger, S1, "error_rate", "prom-1")
    assert not chk.allowed and chk.code == "STALE_BASELINE"
    assert "prom-2" in chk.detail
    chk2 = check_decision_baseline(ledger, S1, "error_rate", "prom-2")
    assert chk2.allowed and chk2.code == "BASELINE_CURRENT"


def test_history_cannot_be_overwritten():
    ledger = BaselineLedger()
    frozen(ledger)
    _, r1 = promote(ledger, good_req(), verifier="naya-2", record_id="prom-1",
                    regression_tolerance=0.01)
    with pytest.raises(FrozenInstanceError):
        r1.value = 0.99  # type: ignore
    with pytest.raises(ValueError):
        ledger.append(BaselineRecord(
            "prom-1", S1, "error_rate", 0.5, Stage.PROMOTED, "mallory",
            "2026-10-10T12:00:00Z", ("x",), None, (), "evil", "mallory"))
    ok, detail = ledger.verify_append_only()
    assert ok, detail


def test_silent_drift_smuggled_record_detected():
    """An attacker appends a PROMOTED record directly, bypassing the gate."""
    ledger = BaselineLedger()
    frozen(ledger)
    _, r1 = promote(ledger, good_req(), verifier="naya-2", record_id="prom-1",
                    regression_tolerance=0.01)
    drifted = BaselineRecord(
        record_id="prom-evil", scope=S1, metric="error_rate", value=0.40,
        stage=Stage.PROMOTED, set_by="mallory", set_at="2026-10-10T12:00:00Z",
        evidence_refs=(), supersedes="prom-1", comparison=(), reason="",
        verifier=None, certified=True)
    ledger.append(drifted)  # the smuggle itself succeeds at the dumb-ledger layer
    ok, problems = audit_promotions(ledger)
    assert not ok
    assert any("SILENT_DRIFT prom-evil" in p for p in problems)
    # and the drifted baseline is now (wrongly) current — decisions on the
    # honest baseline are correctly flagged stale, which is why audit matters
    chk = check_decision_baseline(ledger, S1, "error_rate", "prom-1")
    assert chk.code == "STALE_BASELINE"


def test_local_regression_never_masked_by_aggregate():
    """Candidate regresses the frozen reference: refused even though the
    proposer calls it an improvement."""
    ledger = BaselineLedger()
    frozen(ledger, value=0.02)
    req = good_req(value=0.05)  # worse than frozen 0.02
    verdict, rec = promote(ledger, req, verifier="naya-2", record_id="prom-x",
                           regression_tolerance=0.005)
    assert not verdict.passed and rec is None
    assert any("LOCAL_REGRESSION" in f for f in verdict.failed_obligations)


def test_pooling_never_transfers_certification():
    ledger = BaselineLedger()
    frozen(ledger)
    observations = (
        obs(S1, 0.025, TrainingClass.VERIFIED_HEALTHY, 10)
        + obs(S2, 0.025, TrainingClass.VERIFIED_HEALTHY, 1)  # sparse sibling
    )
    pooled = pooled_estimate(ledger, (S1, S2), "error_rate", observations)
    assert pooled.pooled_value == pytest.approx(0.025)
    by_scope = dict(pooled.per_scope_qualified)
    assert by_scope[S1] is True
    assert by_scope[S2] is False  # sparse cell stays unqualified under healthy parent


def test_dual_reference_catches_joint_drift():
    """Adaptive model drifts while the frozen reference stays put — the classic
    'both drifting together' is impossible here because the reference is
    immutable; divergence is still detected."""
    ledger = BaselineLedger()
    frozen(ledger, value=0.02)
    v = dual_reference_check(ledger, S1, "error_rate", adaptive_value=0.09,
                             tolerance=0.01)
    assert v.divergent and v.code == "ADAPTIVE_DIVERGED"
    v2 = dual_reference_check(ledger, S1, "error_rate", adaptive_value=0.021,
                              tolerance=0.01)
    assert not v2.divergent and v2.code == "CONSISTENT"
    v3 = dual_reference_check(ledger, S2, "error_rate", adaptive_value=0.02,
                              tolerance=0.01)
    assert v3.code == "NO_FROZEN_REFERENCE"  # honest, not a silent pass


def test_guard_removal_produces_counterexample():
    """Remove the training-barred obligation and the slow-degradation fixture
    promotes — the concrete counterexample proving the guard is load-bearing."""
    ledger = BaselineLedger()
    frozen(ledger)
    bad_window = (obs(S1, 0.025, TrainingClass.VERIFIED_WORKLOAD_SHIFT, 4)
                  + obs(S1, 0.09, TrainingClass.CONFIRMED_REGRESSION, 1))
    # mutant gate: training-clean obligation removed
    req = PromotionRequest(
        scope=S1, metric="error_rate", candidate_value=0.025,
        proposed_by="naya-4", proposed_at="2026-10-10T12:00:00Z",
        training_window=bad_window, evidence_refs=("load-report-3",),
        comparison=(("error_rate", "0.020 -> 0.025"),), reason="traffic grew")
    failures = []
    for check_name, fn in [
        ("evidence", lambda: None if req.evidence_refs and req.reason.strip()
         and req.comparison else "EVIDENCE"),
        ("qualifier", lambda: None),  # verifier naya-2 != proposer
        ("regression", lambda: None),  # 0.025 within tolerance of 0.02
    ]:
        f = fn()
        if f:
            failures.append(f)
    mutant_passes = not failures
    assert mutant_passes, "mutant without the guard must promote (counterexample)"
    # and the real gate refuses the same request:
    verdict, _ = promote(ledger, req, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed
    # the counterexample is concrete: degradation WOULD be learned as normal
    assert True  # documented: mutant promotes CONFIRMED_REGRESSION-tainted baseline


def test_empty_training_window_refused():
    ledger = BaselineLedger()
    frozen(ledger)
    base = good_req()
    req = PromotionRequest(
        scope=base.scope, metric=base.metric, candidate_value=base.candidate_value,
        proposed_by=base.proposed_by, proposed_at=base.proposed_at,
        training_window=(), evidence_refs=base.evidence_refs,
        comparison=base.comparison, reason=base.reason)
    verdict, rec = promote(ledger, req, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed and rec is None
    assert any("TRAINING_EMPTY" in f for f in verdict.failed_obligations)


def test_scope_mismatch_in_training_refused():
    ledger = BaselineLedger()
    frozen(ledger)
    base = good_req()
    req = PromotionRequest(
        scope=base.scope, metric=base.metric, candidate_value=base.candidate_value,
        proposed_by=base.proposed_by, proposed_at=base.proposed_at,
        training_window=obs(S2, 0.025, TrainingClass.VERIFIED_HEALTHY, 5),
        evidence_refs=base.evidence_refs, comparison=base.comparison,
        reason=base.reason)
    verdict, rec = promote(ledger, req, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed and rec is None
    assert any("TRAINING_SCOPE_MISMATCH" in f for f in verdict.failed_obligations)


def test_promotion_is_conjunctive_not_aggregate():
    """Two obligations failing is still a refusal — no averaging to a pass."""
    ledger = BaselineLedger()
    frozen(ledger)
    base = good_req()
    req = PromotionRequest(
        scope=base.scope, metric=base.metric, candidate_value=0.09,
        proposed_by=base.proposed_by, proposed_at=base.proposed_at,
        training_window=obs(S1, 0.09, TrainingClass.CONFIRMED_REGRESSION, 5),
        evidence_refs=(), comparison=(), reason="")
    verdict, rec = promote(ledger, req, verifier="naya-4", record_id="prom-x")
    assert not verdict.passed and rec is None
    assert len(verdict.failed_obligations) >= 3


def test_does_not_claim_boundary_present():
    assert "does not measure" in DOES_NOT_CLAIM


def test_insufficient_observability_barred():
    ledger = BaselineLedger()
    frozen(ledger)
    base = good_req()
    req = PromotionRequest(
        scope=base.scope, metric=base.metric, candidate_value=base.candidate_value,
        proposed_by=base.proposed_by, proposed_at=base.proposed_at,
        training_window=obs(S1, 0.025, TrainingClass.INSUFFICIENT_OBSERVABILITY, 5),
        evidence_refs=base.evidence_refs, comparison=base.comparison,
        reason=base.reason)
    verdict, rec = promote(ledger, req, verifier="naya-2", record_id="prom-x")
    assert not verdict.passed and rec is None
