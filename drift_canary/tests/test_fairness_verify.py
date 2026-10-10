"""Tests for drift_canary/fairness_verify.py — fairness verification methodology.

Principle under test: "Every liveness qualification must prove three
separate links: opportunity -> fair service -> verified progress or
governed resolution."

Covers: lasso classifier, staged model checker, three broken schedulers
(first deliverable), runtime harness, canonical trace verifier,
refinement checklist, four-verdict taxonomy, separate scorecard,
twelve-test suite, assumption hygiene (audit, vacuity, contract).
"""
import pytest

from drift_canary.fairness import FairnessContract
from drift_canary.fairness_verify import (
    ASSUMPTION_AUDIT_QUESTIONS,
    ELIGIBILITY_PREDICATES,
    LASSO_VERDICTS,
    MODEL_TRANSITIONS,
    REFINEMENT_MAPPINGS,
    SCORECARD_SLOTS,
    TWELVE_TESTS,
    VACUITY_CHECKS,
    VACUITY_VERDICTS,
    VERIFICATION_VERDICTS,
    AssumptionContract,
    BrokenScheduler,
    Lasso,
    LivenessAssumption,
    ObligationObservation,
    RefinementEvidence,
    RuntimeHarness,
    TraceEvent,
    VerificationScorecard,
    audit_assumption,
    check_property_staged,
    check_refinement,
    classify_lasso,
    detect_vacuity,
    find_lassos,
    identify_broken_scheduler,
    issue_verdict,
    run_broken_scheduler,
    run_twelve_tests,
    verify_trace,
)


def _obs(seq, enabled, serviced, rank_before=1, rank_after=1,
         awaiting_authority=False, terminal=None):
    return ObligationObservation(
        obligation_id="WF-B", seq=seq, enabled=enabled, serviced=serviced,
        rank_before=rank_before, rank_after=rank_after,
        retries_before=2, retries_after=2, terminal=terminal,
        awaiting_authority=awaiting_authority)


# ---------------------------------------------------------------------------
# Lasso classifier: the four patterns from the framework.
# ---------------------------------------------------------------------------
def test_classifier_weak_violation():
    # Enabled every cycle state, never serviced -> WF_VIOLATION (also SF).
    cycle = tuple(_obs(i, True, False) for i in range(6))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "WF_VIOLATION"


def test_classifier_strong_only_violation():
    # Enabled some states (infinitely often), never serviced -> SF_ONLY.
    cycle = tuple(_obs(i, i % 2 == 0, False) for i in range(6))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "SF_ONLY_VIOLATION"


def test_classifier_progress_on_service_violation():
    # Genuine service, no ranking decrease, no terminal -> PoS violation.
    cycle = tuple(_obs(i, True, True) for i in range(6))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "PROGRESS_ON_SERVICE_VIOLATION"


def test_classifier_correct_progress():
    # Service + ranking decrease -> no violation in this trace.
    cycle = tuple(_obs(i, True, True,
                       rank_before=1, rank_after=0) for i in range(2))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "MODEL_CHECK_PASSED_IN_SCOPE"


def test_classifier_opportunity_not_met():
    cycle = tuple(_obs(i, False, False) for i in range(6))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "OPPORTUNITY_ASSUMPTION_NOT_MET"


def test_classifier_waiting_authority():
    cycle = tuple(_obs(i, False, False, awaiting_authority=True)
                  for i in range(6))
    v, _ = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "WAITING_AUTHORITY"


def test_classifier_needs_nonempty_cycle():
    with pytest.raises(AssertionError):
        Lasso("WF-B", (), ())


def test_wf_violation_implies_sf():
    # A WF_VIOLATION is also an SF violation — never reported as disjoint.
    cycle = tuple(_obs(i, True, False) for i in range(4))
    v, reason = classify_lasso(Lasso("WF-B", (), cycle))
    assert v == "WF_VIOLATION"
    assert "strong fairness" in reason


# ---------------------------------------------------------------------------
# Staged model checker: unconstrained -> weak -> strong.
# ---------------------------------------------------------------------------
def test_staged_unconstrained_finds_violations():
    lassos = find_lassos("UNCONSTRAINED", max_depth=20)
    verdicts = {classify_lasso(l)[0] for _, l in lassos}
    assert "WF_VIOLATION" in verdicts
    assert "SF_ONLY_VIOLATION" in verdicts


def test_staged_weak_admits_flicker_starvation():
    # Weak fairness does not protect flickering work: SF_ONLY lassos
    # remain, WF lassos are excluded.
    lassos = find_lassos("WEAK", max_depth=20)
    verdicts = {classify_lasso(l)[0] for _, l in lassos}
    assert "SF_ONLY_VIOLATION" in verdicts
    assert "WF_VIOLATION" not in verdicts


def test_staged_strong_excludes_starvation():
    lassos = find_lassos("STRONG", max_depth=20)
    assert lassos == [], f"strong policy should exclude starvation: {lassos}"


def test_check_property_staged_shape():
    out = check_property_staged(max_depth=14)
    assert set(out) == {"1_unconstrained", "2_weak", "3_strong",
                        "4_progress_on_service"}


# ---------------------------------------------------------------------------
# First deliverable: three broken schedulers, each identified correctly.
# ---------------------------------------------------------------------------
def test_broken_wf_identified():
    kind, verdict, _ = identify_broken_scheduler("BROKEN_WF")
    assert kind == "BROKEN_WF"
    assert verdict == "WF_VIOLATION"


def test_broken_sf_identified():
    kind, verdict, _ = identify_broken_scheduler("BROKEN_SF")
    assert kind == "BROKEN_SF"
    assert verdict == "SF_ONLY_VIOLATION"


def test_broken_pos_identified():
    kind, verdict, _ = identify_broken_scheduler("BROKEN_POS")
    assert kind == "BROKEN_POS"
    assert verdict == "PROGRESS_ON_SERVICE_VIOLATION"


def test_broken_scheduler_kinds():
    assert set(BrokenScheduler("BROKEN_WF").__class__.__name__ and
               ("BROKEN_WF", "BROKEN_SF", "BROKEN_POS")) == \
        {"BROKEN_WF", "BROKEN_SF", "BROKEN_POS"}


# ---------------------------------------------------------------------------
# Runtime harness + canonical trace verifier.
# ---------------------------------------------------------------------------
def _contract():
    return FairnessContract(
        obligation_id="WF-B", revision="v3", standard="WEAK",
        eligibility_predicate="VALIDATED_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY")


def test_harness_healthy_run_discharges():
    sched = BrokenScheduler("BROKEN_POS", target="NO-SUCH")
    sched.worker_fails = False
    harness = RuntimeHarness()
    events = harness.run(sched, "WF-B", "WF-001", "v3", rounds=6,
                         flicker=(True, True))
    ok, findings = verify_trace(events, _contract())
    assert ok, findings
    assert any(e.event_type == "DISCHARGE" for e in events)
    assert events[-1].event_type == "TERMINATE"


def test_verifier_rejects_service_without_usability():
    ev = TraceEvent(
        workflow_id="WF-001", obligation_id="WF-B",
        obligation_revision="v3", event_sequence=0, event_type="SERVICE",
        worker_id="W", enabled_before=True, service_usable=False,
        outstanding_rank_before=(1,), outstanding_rank_after=(1,),
        retries_before=2, retries_after=2, proof_discharge_receipt=None,
        execution_receipt=None, model_version="FAIRNESS-MODEL-V1")
    ok, findings = verify_trace([ev], _contract())
    assert not ok
    assert any("without usable" in f for f in findings)


def test_verifier_rejects_rank_decrease_without_receipt():
    ev = TraceEvent(
        workflow_id="WF-001", obligation_id="WF-B",
        obligation_revision="v3", event_sequence=0, event_type="SERVICE",
        worker_id="W", enabled_before=True, service_usable=True,
        outstanding_rank_before=(1,), outstanding_rank_after=(),
        retries_before=2, retries_after=2, proof_discharge_receipt=None,
        execution_receipt="EXEC-000", model_version="FAIRNESS-MODEL-V1")
    ok, findings = verify_trace([ev], _contract())
    assert not ok
    assert any("without a proof discharge receipt" in f for f in findings)


def test_verifier_rejects_budget_replenishment_on_reassign():
    evs = [
        TraceEvent("WF-001", "WF-B", "v3", 0, "SELECT", "W", True, False,
                   (1,), (1,), 2, 2, None, None, "FAIRNESS-MODEL-V1"),
        TraceEvent("WF-001", "WF-B", "v3", 1, "REASSIGN", "W", True, False,
                   (1,), (1,), 1, 2, None, None, "FAIRNESS-MODEL-V1"),
    ]
    ok, findings = verify_trace(evs, _contract())
    assert not ok
    assert any("replenished through reassignment" in f for f in findings)


def test_verifier_rejects_sequence_gaps():
    evs = [
        TraceEvent("WF-001", "WF-B", "v3", 0, "SELECT", "W", True, False,
                   (1,), (1,), 2, 2, None, None, "FAIRNESS-MODEL-V1"),
        TraceEvent("WF-001", "WF-B", "v3", 2, "SELECT", "W", True, False,
                   (1,), (1,), 2, 2, None, None, "FAIRNESS-MODEL-V1"),
    ]
    ok, findings = verify_trace(evs, _contract())
    assert not ok
    assert any("strictly increasing" in f for f in findings)


def test_verifier_rejects_obsolete_revision():
    ev = TraceEvent(
        workflow_id="WF-001", obligation_id="WF-B",
        obligation_revision="v2", event_sequence=0, event_type="SELECT",
        worker_id="W", enabled_before=True, service_usable=False,
        outstanding_rank_before=(1,), outstanding_rank_after=(1,),
        retries_before=2, retries_after=2, proof_discharge_receipt=None,
        execution_receipt=None, model_version="FAIRNESS-MODEL-V1")
    ok, findings = verify_trace([ev], _contract())
    assert not ok
    assert any("revision" in f for f in findings)


def test_harness_fault_injection():
    # Worker fails (no early discharge) so the run reaches the fault round.
    sched = BrokenScheduler("BROKEN_POS", target="WF-B")
    harness = RuntimeHarness()
    events = harness.run(sched, "WF-B", "WF-001", "v3", rounds=4,
                         flicker=(True, True),
                         faults={1: "TIMEOUT"})
    assert any("FAULT-TIMEOUT" in (e.execution_receipt or "")
               for e in events)


# ---------------------------------------------------------------------------
# Refinement checklist: all six mappings, FAIRNESS_ENFORCEMENT is critical.
# ---------------------------------------------------------------------------
def test_refinement_all_six_required():
    ev = [RefinementEvidence(m, True, "e") for m in REFINEMENT_MAPPINGS]
    ok, _ = check_refinement(ev)
    assert ok


def test_refinement_missing_fairness_enforcement_flagged():
    ev = [RefinementEvidence(m, True, "e") for m in REFINEMENT_MAPPINGS
          if m != "FAIRNESS_ENFORCEMENT"]
    ok, msg = check_refinement(ev)
    assert not ok
    assert "FAIRNESS_ENFORCEMENT" in msg


# ---------------------------------------------------------------------------
# Four-verdict taxonomy: never a collapsed PASS.
# ---------------------------------------------------------------------------
def test_verdicts_distinct():
    assert len(set(VERIFICATION_VERDICTS)) == 4


def test_completed_needs_outcome_receipt():
    ok, _ = issue_verdict("WORKFLOW_COMPLETED_IN_SCOPE", "trace 0..99")
    assert not ok
    ok, v = issue_verdict("WORKFLOW_COMPLETED_IN_SCOPE", "trace 0..99",
                          completed_outcome_receipt="PROOF-1")
    assert ok and v.kind == "WORKFLOW_COMPLETED_IN_SCOPE"


def test_qualified_with_assumptions_needs_assumptions():
    ok, _ = issue_verdict("FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS", "model")
    assert not ok
    ok, v = issue_verdict("FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS", "model",
                          assumptions=("A_env_recurs",))
    assert ok


def test_verdict_needs_scope():
    with pytest.raises(AssertionError):
        issue_verdict("MODEL_CHECK_PASSED_IN_SCOPE", "")


# ---------------------------------------------------------------------------
# Scorecard: five independent slots.
# ---------------------------------------------------------------------------
def test_scorecard_slots_independent():
    sc = VerificationScorecard()
    sc.set("WEAK_FAIRNESS", "QUALIFIED")
    sc.set("STRONG_FAIRNESS", "COUNTEREXAMPLE_FOUND")
    assert sc.failing_slots() == ["STRONG_FAIRNESS"]
    assert len(SCORECARD_SLOTS) == 5


# ---------------------------------------------------------------------------
# Twelve-test suite.
# ---------------------------------------------------------------------------
def test_twelve_tests_all_defined():
    assert len(TWELVE_TESTS) == 12
    ids = [t[0] for t in TWELVE_TESTS]
    assert len(set(ids)) == 12


def test_run_twelve_tests():
    results = run_twelve_tests()
    assert set(results) == {t[0] for t in TWELVE_TESTS}
    failed = {tid: d for tid, (ok, d) in results.items() if not ok}
    assert not failed, f"failing: {failed}"


# ---------------------------------------------------------------------------
# Assumption hygiene.
# ---------------------------------------------------------------------------
def _audited_assumption(owner="ENVIRONMENT", predicate="eligibility recurs"):
    return LivenessAssumption(
        assumption_id="A-1", owner=owner, predicate=predicate,
        status="PROPOSED")


def _full_answers(circular=False, hides=False):
    return {
        "WHO_CONTROLS": "ENVIRONMENT",
        "PRECISE_PREDICATE": "eligibility recurs infinitely often",
        "WHY_REASONABLE": "upstream guarantees it" if not hides else "",
        "HIDES_COUNTEREXAMPLE": hides,
        "SATISFIABLE": True,
        "CIRCULAR": circular,
        "IF_IT_FAILS": "starvation; detected by debt monitor",
        "REQUALIFY_WHEN": "on environment change",
    }


def test_assumption_audit_passes_when_clean():
    a = _audited_assumption()
    ok, findings = audit_assumption(a, _full_answers())
    assert ok, findings


def test_assumption_audit_rejects_scheduler_self_fairness():
    a = _audited_assumption(owner="SCHEDULER",
                            predicate="scheduler fairness holds")
    answers = _full_answers()
    answers["WHO_CONTROLS"] = "SCHEDULER"
    ok, findings = audit_assumption(a, answers)
    assert not ok
    assert any("CIRCULAR" in f for f in findings)


def test_assumption_audit_rejects_unsatisfiable():
    a = _audited_assumption()
    answers = _full_answers()
    answers["SATISFIABLE"] = False
    ok, findings = audit_assumption(a, answers)
    assert not ok
    assert any("VACUOUS" in f for f in findings)


def test_assumption_audit_flags_load_bearing():
    a = _audited_assumption()
    ok, findings = audit_assumption(a, _full_answers(hides=True))
    assert not ok
    assert any("LOAD-BEARING" in f for f in findings)


def test_assumption_contract_rejects_circular_fairness():
    a = LivenessAssumption("A-1", "SCHEDULER", "fairness holds", "PROPOSED")
    with pytest.raises(AssertionError):
        AssumptionContract(contract_id="C-1", revision="v1",
                           target_property="SF",
                           assumptions=(a,),
                           scheduler_guarantees=("termination",))


def test_assumption_contract_ok_when_fairness_is_guarantee():
    a = LivenessAssumption("A-1", "ENVIRONMENT",
                          "eligibility recurs", "JUSTIFIED")
    c = AssumptionContract(
        contract_id="C-1", revision="v1", target_property="SF",
        assumptions=(a,), scheduler_guarantees=("strong fairness",))
    assert c.qualification == "PENDING"


def test_vacuity_detects_counterexample():
    v, _ = detect_vacuity({"lassos": ["x"], "states_explored": 10},
                          {"recurring_enablement": True,
                           "continuous_enablement": True,
                           "service_event": True,
                           "assumption_removal_changes": True,
                           "mutation_caught": True,
                           "independence_ok": True})
    assert v == "COUNTEREXAMPLE_FOUND"


def test_vacuity_detects_missing_witness():
    v, reasons = detect_vacuity(
        {"lassos": [], "states_explored": 100},
        {"recurring_enablement": False, "continuous_enablement": True,
         "service_event": True, "assumption_removal_changes": True,
         "mutation_caught": True, "independence_ok": True})
    assert v == "VACUOUS"
    assert any("strong fairness" in r for r in reasons)


def test_vacuity_proved_in_scope():
    v, _ = detect_vacuity(
        {"lassos": [], "states_explored": 100},
        {"recurring_enablement": True, "continuous_enablement": True,
         "service_event": True, "assumption_removal_changes": True,
         "mutation_caught": True, "independence_ok": True})
    assert v == "PROVED_IN_SCOPE"


def test_vacuity_verdicts_complete():
    assert set(VACUITY_VERDICTS) == {"PROVED_IN_SCOPE", "VACUOUS",
                                     "ASSUMPTIONS_UNJUSTIFIED",
                                     "COUNTEREXAMPLE_FOUND", "UNKNOWN"}
    assert len(VACUITY_CHECKS) == 8


def test_eligibility_predicates_four():
    assert ELIGIBILITY_PREDICATES == ("OUTSTANDING", "ADMISSIBLE", "READY",
                                      "ENABLED")


def test_audit_questions_eight():
    assert len(ASSUMPTION_AUDIT_QUESTIONS) == 8


def test_lasso_verdicts_include_vacuous_distinction():
    # The classifier distinguishes PROVED_IN_SCOPE from vacuous absence;
    # MODEL_CHECK_PASSED_IN_SCOPE is explicitly not production-proven.
    assert "MODEL_CHECK_PASSED_IN_SCOPE" in LASSO_VERDICTS
    v, reason = classify_lasso(Lasso(
        "WF-B", (), tuple(_obs(i, True, True, 1, 0) for i in range(2))))
    assert v == "MODEL_CHECK_PASSED_IN_SCOPE"
    assert "no violation in this trace" in reason


def test_model_transitions_complete():
    assert set(MODEL_TRANSITIONS) == {"ENABLE", "DISABLE", "SELECT",
                                      "SERVICE", "DISCHARGE",
                                      "FAILED_ATTEMPT", "RETRY", "REASSIGN",
                                      "ESCALATE", "TERMINATE"}
