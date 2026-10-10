"""Tests for drift_canary/d29_boundary.py — D29 decisive experiment.

Rule under test: "A component cannot convert its own failure into another
component's assumption. Responsibility follows control."

The experiment: a controlled KNOW → LAW → ACT → VERIFY workflow with
three injected failures. The independent verifier must classify all three
correctly from EVIDENCE ALONE — including when the failing component
falsely reports that another component was responsible — and the same
observable symptom (an uncompleted workflow) must classify differently
depending on the independently established evidence.
"""
import inspect

import pytest

from drift_canary.d29_boundary import (
    CONTROLLERS,
    OBLIGATION_ID,
    VERDICTS,
    WORKFLOW_ID,
    BoundaryCaseResult,
    ComponentReport,
    EnvironmentObservation,
    ResponsibilityRecord,
    classify_boundary,
    run_case,
    verify_against_ledger,
)
from drift_canary.fairness import (
    DeterministicScheduler,
    FairnessContract,
    FairnessLedger,
    event_adequate_service,
)
from drift_canary.liveness import detect_starvation


def false_blame_for(case):
    """The canonical false-blame injection per D29's three common failures."""
    if case == "A":
        # Environment failed; the worker blames the scheduler.
        return (ComponentReport("WORKER", "SCHEDULER_STARVATION", 1),
                ComponentReport("SCHEDULER", "WORKER_FAILURE", 1))
    if case == "B":
        # Scheduler failed; it calls its own allocation failure an
        # environment outage — D29 failure #1.
        return (ComponentReport("SCHEDULER", "DATABASE_UNAVAILABLE", 1),)
    # case C: worker failed; it calls repeated unsuccessful execution a
    # scheduler problem despite receiving usable service — D29 failure #2.
    return (ComponentReport("WORKER", "SCHEDULER_STARVATION", 1),)


# ---------------------------------------------------------------------------
# The three canonical cases.
# ---------------------------------------------------------------------------
def test_case_a_environment_blocker():
    r = run_case("A")
    assert r.verdict == "ENVIRONMENT_BLOCKER"
    assert r.record.controller == "ENVIRONMENT"
    assert r.record.classification == "ENVIRONMENT_BLOCKER"
    # The workflow is uncompleted — the observable symptom.
    assert r.obligation.state == "OUTSTANDING"
    # No false scheduler/worker blame: the verdict names the environment
    # even though scheduler debt accrued.
    assert r.verdict not in ("SCHEDULER_STARVATION",
                             "SCHEDULER_SERVICE_FAILURE", "WORKER_NONPROGRESS")


def test_case_b_scheduler_starvation():
    r = run_case("B")
    assert r.verdict == "SCHEDULER_STARVATION"
    assert r.record.controller == "SCHEDULER"
    assert r.obligation.state == "OUTSTANDING"
    # Environment assumptions cannot hide the failure: the resource was
    # available every round, and still no adequate service.
    assert all(o.available for o in r.env_observations)
    assert r.serviced_rounds == 0


def test_case_c_worker_nonprogress():
    r = run_case("C")
    assert r.verdict == "WORKER_NONPROGRESS"
    assert r.record.controller == "WORKER"
    assert r.obligation.state == "OUTSTANDING"
    # Scheduler fairness REMAINS qualified while progress fails: debt 0,
    # adequate service every round, nothing advanced.
    assert r.truths.fair_chance is True
    assert r.truths.advanced_on_service is False
    assert r.serviced_rounds > 0 and r.advanced_rounds == 0


def test_environment_takes_precedence_over_debt():
    """D29 precedence: in case A the scheduler accrues fairness debt
    (eligible, DISPATCHED-ONLY), yet the verdict must still be
    ENVIRONMENT_BLOCKER. Debt alone is not blame."""
    r = run_case("A")
    assert r.ledger.debt(OBLIGATION_ID) >= 3  # debt did accrue
    assert r.truths.fair_chance is False      # naive reading says "unfair"
    assert r.verdict == "ENVIRONMENT_BLOCKER"  # boundary says "environment"


def test_no_averaged_scores():
    """A strong dimension must not compensate a failed one. Case C has
    perfect scheduler fairness AND failed progress-on-service; both are
    reported independently, and the liveness claim stays unproven."""
    r = run_case("C")
    assert r.truths.fair_chance is True
    assert r.truths.advanced_on_service is False
    assert r.liveness_verdict == "LIVENESS_UNPROVEN"


# ---------------------------------------------------------------------------
# False blame and label manipulation must not move the verdict.
# ---------------------------------------------------------------------------
def test_false_blame_does_not_move_verdict():
    for case, expected in (("A", "ENVIRONMENT_BLOCKER"),
                           ("B", "SCHEDULER_STARVATION"),
                           ("C", "WORKER_NONPROGRESS")):
        clean = run_case(case)
        blamed = run_case(case, false_blame=false_blame_for(case))
        assert blamed.verdict == clean.verdict == expected, (
            f"case {case}: false blame moved the verdict "
            f"{clean.verdict} -> {blamed.verdict}")
        assert blamed.record.controller == clean.record.controller


def test_label_swap_verdict_stable():
    """Swap ENVIRONMENT_BLOCKER ↔ SCHEDULER_STARVATION labels with the
    evidence unchanged: the independently calculated verdict must not move."""
    labels_a = (ComponentReport("SCHEDULER", "SCHEDULER_STARVATION", 1),
                ComponentReport("ENVIRONMENT", "ENVIRONMENT_BLOCKER", 1))
    labels_b = (ComponentReport("SCHEDULER", "ENVIRONMENT_BLOCKER", 1),
                ComponentReport("ENVIRONMENT", "SCHEDULER_STARVATION", 1))
    r1 = run_case("A", false_blame=labels_a)
    r2 = run_case("A", false_blame=labels_b)
    assert r1.verdict == r2.verdict == "ENVIRONMENT_BLOCKER"
    r3 = run_case("B", false_blame=labels_a)
    r4 = run_case("B", false_blame=labels_b)
    assert r3.verdict == r4.verdict == "SCHEDULER_STARVATION"


def test_verifier_has_no_label_input():
    """Structural guard: the classifier's signature must offer no
    parameter through which a narrative label could enter. Labels are
    recorded on the result for the false-blame tests; they are never an
    input to classification."""
    params = inspect.signature(classify_boundary).parameters
    forbidden = {"label", "labels", "report", "reports", "narrative",
                 "component_report", "component_reports"}
    assert not (set(params) & forbidden), (
        f"classify_boundary accepts label-like inputs: "
        f"{set(params) & forbidden}")


# ---------------------------------------------------------------------------
# Same symptom, different classification.
# ---------------------------------------------------------------------------
def test_same_symptom_different_classification():
    results = {c: run_case(c) for c in ("A", "B", "C")}
    # Identical observable symptom: the workflow never completed.
    assert all(r.obligation.state == "OUTSTANDING" for r in results.values())
    assert all(r.liveness_verdict == "LIVENESS_UNPROVEN"
               for r in results.values())
    # Different independently-established causes.
    verdicts = {r.verdict for r in results.values()}
    assert verdicts == {"ENVIRONMENT_BLOCKER", "SCHEDULER_STARVATION",
                        "WORKER_NONPROGRESS"}, verdicts
    controllers = {r.record.controller for r in results.values()}
    assert controllers == {"ENVIRONMENT", "SCHEDULER", "WORKER"}


# ---------------------------------------------------------------------------
# Independent cross-checks using the other two contracts.
# ---------------------------------------------------------------------------
def test_independent_cross_check():
    for case in ("A", "B", "C"):
        r = run_case(case, false_blame=false_blame_for(case))
        ok, reason = verify_against_ledger(r)
        assert ok, f"case {case}: {reason}"


def test_liveness_starvation_corroborates_case_b():
    """liveness.py's detect_starvation independently corroborates the
    scheduler verdict: eligible, zero opportunities, others scheduled."""
    r = run_case("B")
    verdict, evidence = detect_starvation(
        eligible_since={WORKFLOW_ID: 1},
        opportunities={WORKFLOW_ID: 0},
        scheduled_others={WORKFLOW_ID: 5},
        age_threshold=3, now=6)
    assert verdict == "STARVATION_SUSPECTED", evidence
    assert r.verdict == "SCHEDULER_STARVATION"


def test_scheduler_service_failure_variant():
    """D29 adversarial row: the scheduler dispatches but provides no
    usable resources while the resource IS available. Evidence-based
    distinction from never-dispatched starvation."""
    env = tuple(EnvironmentObservation(seq=i, resource_id="DB-CONN",
                                       available=True)
                for i in range(1, 7))
    ledger = FairnessLedger()
    ledger.register(FairnessContract(
        obligation_id=OBLIGATION_ID, revision="v1", standard="WEAK",
        eligibility_predicate="ELIGIBLE_WHEN_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY"))
    sched = DeterministicScheduler(ledger)
    for i in range(1, 7):
        # DISPATCHED rung, but evidence lacks worker_ack and
        # resources_available: DISPATCHED-ONLY, debt accrues.
        sched.round(OBLIGATION_ID, "WF-D29", eligible=True,
                    rung="DISPATCHED",
                    evidence={"lease_id": f"L-V-{i}"})
    verdict, controller, _ = classify_boundary(
        env, ledger, OBLIGATION_ID,
        serviced_rounds=0, advanced_rounds=0, debt_threshold=3)
    assert verdict == "SCHEDULER_SERVICE_FAILURE"
    assert controller == "SCHEDULER"


def test_responsibility_record_wellformed():
    r = run_case("B", false_blame=false_blame_for("B"))
    rec = r.record
    assert isinstance(rec, ResponsibilityRecord)
    assert rec.controller in CONTROLLERS
    assert rec.classification in VERDICTS
    assert rec.classification == r.verdict
    assert rec.condition == "usable_execution_opportunity"
    assert rec.evidence_refs  # bound to evidence, not to labels
