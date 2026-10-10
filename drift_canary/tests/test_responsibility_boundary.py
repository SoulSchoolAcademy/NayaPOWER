"""Tests for drift_canary/responsibility_boundary.py — the responsibility-boundary
contract spec.

Principle under test: "Control determines responsibility. Contracts
define guarantees. Independent evidence establishes what occurred."

Covers: ownership table, proof composition (A_E/\\S |= G_S,
A_E/\\G_S/\\W |= G_W), versioned responsibility records (controller
primary), interface compatibility, two-sided boundary evidence,
enforcement contract, adversarial fault injection (10 rows +
mislabeled-ownership + 3 fault models + component-supplied assumptions),
boundary migration receipts, three indicators + consistency verdict
(never averaged), and the decisive A/B/C experiment with false blame.
Every negative test has a positive control.
"""
import pytest

from drift_canary.responsibility_boundary import (
    BOUNDARY_VERDICTS,
    COMPONENTS,
    DATABASE_UNAVAILABLE_CASES,
    ENFORCEMENT_CONSTRAINTS,
    FAULT_INJECTION_TABLE,
    FAULT_MODELS,
    FAILURE_CLASSIFICATIONS,
    GUARANTEE_STRENGTH,
    INDICATORS,
    OWNERSHIP,
    STAGE_OWNER,
    STAGES,
    AccountabilityScorecard,
    BoundaryMigrationReceipt,
    BoundaryWitnesses,
    InterfaceEdge,
    ProofContract,
    ResponsibilityBoundaryContract,
    ResponsibilityRecord,
    check_component_supplied_assumption,
    check_constraint,
    check_interface,
    check_law_not_assumed,
    check_no_retroactive_absolution,
    check_worker_assumption,
    classify_with_narrative,
    correlate_witnesses,
    decompose_shared,
    decisive_experiment_case,
    detect_circular_chain,
    guarantee_strength,
    link_assumption,
    run_fault_scenario,
)


def _w(**kw):
    base = {"producer": "t", "timestamp": 1}
    d = {"environment": dict(base), "scheduler": dict(base),
         "worker": dict(base)}
    d.update(kw)
    return BoundaryWitnesses(**d)


# ---------------------------------------------------------------------------
# 1. Ownership table.
# ---------------------------------------------------------------------------

def test_all_components_present():
    assert set(COMPONENTS) == {"ENVIRONMENT", "SCHEDULER", "WORKER",
                               "VERIFY", "LAW"}
    for c in COMPONENTS:
        o = OWNERSHIP[c]
        assert o["owns"] and o["must_establish"]
        assert "cannot_claim" in o


def test_scheduler_cannot_claim_service_completed_task():
    assert "service completed the task" in OWNERSHIP["SCHEDULER"][
        "cannot_claim"][0]


def test_worker_cannot_claim_dispatch_proves_success():
    assert "dispatch alone proves its work succeeded" in OWNERSHIP[
        "WORKER"]["cannot_claim"][0]


def test_verify_cannot_weaken_requirements():
    assert "weaken" in OWNERSHIP["VERIFY"]["cannot_claim"][0]


def test_law_never_assumable_away():
    assert OWNERSHIP["LAW"]["never_assumable_away"] is True


def test_stages_owned_by_components():
    assert len(STAGES) == 5
    assert STAGE_OWNER["ENVIRONMENTAL_POSSIBILITY"] == "ENVIRONMENT"
    assert STAGE_OWNER["SCHEDULER_OPPORTUNITY"] == "SCHEDULER"
    assert STAGE_OWNER["ACTUAL_SERVICE"] == "SCHEDULER"
    assert STAGE_OWNER["VERIFIED_ADVANCEMENT"] == "VERIFY"
    assert STAGE_OWNER["TERMINAL_DISPOSITION"] == "VERIFY"


# Canonical demo: same label, three owners.
def test_database_unavailable_three_owners():
    by_case = {c["case"]: c for c in DATABASE_UNAVAILABLE_CASES}
    assert len(by_case) == 3
    controllers = {c["controller"] for c in DATABASE_UNAVAILABLE_CASES}
    assert controllers == {"ENVIRONMENT", "SCHEDULER", "WORKER"}
    # Positive control: the label alone is not the classification.
    for c in DATABASE_UNAVAILABLE_CASES:
        assert c["classification"] == c["controller"]


# ---------------------------------------------------------------------------
# 2. Proof composition.
# ---------------------------------------------------------------------------

def test_proof_contract_ok():
    ProofContract(
        contract_id="PC-1",
        environmental_assumptions=("resource recurs occasionally",),
        scheduler_model="S",
        worker_model="W",
        scheduler_guarantee="eligible work fairly serviced",
        worker_guarantee="service yields progress or disposition",
    )


def test_scheduler_fairness_cannot_be_environmental_assumption():
    with pytest.raises(AssertionError):
        ProofContract(
            contract_id="PC-BAD",
            environmental_assumptions=("scheduler is fair",),
            scheduler_model="S",
            worker_model="W",
            scheduler_guarantee="eligible work fairly serviced",
            worker_guarantee="service yields progress or disposition",
        )


def test_worker_may_assume_usable_service():
    ok, _ = check_worker_assumption("the worker receives genuine usable service")
    assert ok


def test_worker_cannot_assume_own_output():
    ok, finding = check_worker_assumption("the task completed successfully")
    assert not ok and "CIRCULAR" in finding


def test_law_not_assumed_ok():
    ok, _ = check_law_not_assumed(("resource available occasionally",))
    assert ok


def test_law_assumed_away_rejected():
    ok, finding = check_law_not_assumed(("assume LAW bypass for speed",))
    assert not ok and "LAW cannot be assumed away" in finding


# ---------------------------------------------------------------------------
# 3. Responsibility records: controller is primary.
# ---------------------------------------------------------------------------

def _record(**kw):
    d = dict(condition="db connection available",
             controller="SCHEDULER",
             producer_guarantee="allocation of available connections",
             consumer_assumption="worker receives assigned usable connection",
             observation_boundary="assignment event",
             evidence=("receipt-1",),
             failure_classification="SCHEDULER",
             applicable_version="rt-2.1")
    d.update(kw)
    return ResponsibilityRecord(**d)


def test_record_ok():
    assert _record().controller == "SCHEDULER"


def test_record_rejects_unknown_controller():
    with pytest.raises(AssertionError):
        _record(controller="NOBODY")


def test_shared_must_be_decomposed():
    with pytest.raises(AssertionError):
        _record(failure_classification="SHARED")


def test_narrative_cannot_override_controller():
    r = _record()
    cls, reason = classify_with_narrative(r, narrative_blame="ENVIRONMENT")
    assert cls == "SCHEDULER"
    assert "control" in reason and "narrative" in reason


def test_agreeing_narrative_ok():
    r = _record()
    cls, _ = classify_with_narrative(r, narrative_blame="SCHEDULER")
    assert cls == "SCHEDULER"


def test_decompose_shared_gives_per_component_records():
    recs = decompose_shared(
        "db connection",
        (("ENVIRONMENT", "connections establishable under conditions",
          "scheduler may request", "offer event", ("env-receipt",)),
         ("SCHEDULER", "allocation of available connections",
          "worker receives assigned usable connection",
          "assignment event", ("sched-receipt",)),
         ("WORKER", "appropriate use of allocated connections",
          "verifier sees recorded outcomes", "outcome event",
          ("worker-receipt",))),
        "rt-2.1")
    assert len(recs) == 3
    assert {r.controller for r in recs} == {"ENVIRONMENT", "SCHEDULER",
                                           "WORKER"}
    for r in recs:
        assert r.failure_classification == r.controller


def test_link_assumption_join_point():
    class FakeAssumption:
        assumption_id = "A-1"
        control_boundary = "ENVIRONMENT"
    ok, _ = link_assumption(FakeAssumption())
    assert ok


def test_link_assumption_missing_boundary():
    class FakeAssumption:
        assumption_id = "A-2"
    ok, finding = link_assumption(FakeAssumption())
    assert not ok and "control_boundary" in finding


def test_link_assumption_unknown_component():
    class FakeAssumption:
        assumption_id = "A-3"
        control_boundary = "THE_ETHER"
    ok, _ = link_assumption(FakeAssumption())
    assert not ok


# ---------------------------------------------------------------------------
# 4. Interface compatibility.
# ---------------------------------------------------------------------------

def _edge(**kw):
    d = dict(edge_id="e1", producer="ENVIRONMENT", consumer="SCHEDULER",
             producer_guarantee="resource available repeatedly",
             consumer_assumption="scheduler receives genuine opportunities repeatedly",
             scope="prod/us-east/2026")
    d.update(kw)
    return InterfaceEdge(**d)


def test_interface_ok_when_guarantee_meets_assumption():
    ok, _ = check_interface(_edge())
    assert ok


def test_interface_mismatch_when_weaker():
    ok, findings = check_interface(_edge(
        producer_guarantee="resource available occasionally",
        consumer_assumption="connection always available"))
    assert not ok
    assert any("MISMATCH" in f for f in findings)


def test_interface_never_silently_strengthened():
    # Positive control: mismatch is reported, not repaired.
    ok, _ = check_interface(_edge(
        producer_guarantee="resource available occasionally",
        consumer_assumption="connection always available"))
    assert not ok  # still failing on re-check: no silent strengthening


def test_circular_chain_rejected():
    edges = (
        _edge(edge_id="e1", producer="ENVIRONMENT", consumer="SCHEDULER",
              producer_guarantee="fair availability",
              consumer_assumption="scheduler fairness holds"),
        _edge(edge_id="e2", producer="SCHEDULER", consumer="ENVIRONMENT",
              producer_guarantee="fair service",
              consumer_assumption="fair availability"),
    )
    ok, findings = detect_circular_chain(edges)
    assert not ok and any("CIRCULAR" in f for f in findings)


def test_acyclic_chain_ok():
    edges = (
        _edge(edge_id="e1", producer="ENVIRONMENT", consumer="SCHEDULER"),
        _edge(edge_id="e2", producer="SCHEDULER", consumer="WORKER",
              producer_guarantee="usable execution lease delivered",
              consumer_assumption="worker receives valid service"),
    )
    ok, _ = detect_circular_chain(edges)
    assert ok


def test_guarantee_strength_unknown():
    assert guarantee_strength("something vague") is None
    assert guarantee_strength("always on") == GUARANTEE_STRENGTH["always"]


# ---------------------------------------------------------------------------
# 5. Two-sided boundary evidence.
# ---------------------------------------------------------------------------

def test_scheduler_allocation_failure():
    verdict, _ = correlate_witnesses(_w(
        environment={"producer": "t", "timestamp": 1,
                     "resource_available": True},
        scheduler={"producer": "t", "timestamp": 1,
                   "resource_requested": True, "resource_assigned": False},
    ))
    assert verdict == "SCHEDULER"


def test_environment_failure():
    verdict, _ = correlate_witnesses(_w(
        environment={"producer": "t", "timestamp": 1,
                     "resource_available": False},
        scheduler={"producer": "t", "timestamp": 1,
                   "resource_requested": True},
    ))
    assert verdict == "ENVIRONMENT"


def test_dispatch_without_service_is_scheduler_failure():
    verdict, _ = correlate_witnesses(_w(
        scheduler={"producer": "t", "timestamp": 1, "dispatched": True,
                   "usable_resources_provided": False},
    ))
    assert verdict == "SCHEDULER"


def test_service_without_progress_is_worker_failure():
    verdict, _ = correlate_witnesses(_w(
        scheduler={"producer": "t", "timestamp": 1,
                   "usable_service_delivered": True},
        worker={"producer": "t", "timestamp": 1, "attempted": True,
                "ranking_reduced": False, "valid_disposition": False},
    ))
    assert verdict == "WORKER"


def test_worker_false_success_report():
    verdict, _ = correlate_witnesses(_w(
        worker={"producer": "t", "timestamp": 1, "reported_success": True,
                "outcome_present": False},
    ))
    assert verdict == "WORKER"


def test_missing_provenance_is_undetermined():
    verdict, _ = correlate_witnesses(BoundaryWitnesses(
        environment={"timestamp": 1}, scheduler={"producer": "t",
                                                 "timestamp": 1},
        worker={"producer": "t", "timestamp": 1}))
    assert verdict == "BOUNDARY_UNDETERMINED"


def test_missing_timestamp_is_undetermined():
    verdict, _ = correlate_witnesses(_w(
        environment={"producer": "t"},
    ))
    assert verdict == "BOUNDARY_UNDETERMINED"


def test_unavailable_without_request_is_undetermined():
    # Cannot distinguish environment outage from scheduler never asking.
    verdict, _ = correlate_witnesses(_w(
        environment={"producer": "t", "timestamp": 1,
                     "resource_available": False},
        scheduler={"producer": "t", "timestamp": 1,
                   "resource_requested": False},
    ))
    assert verdict == "BOUNDARY_UNDETERMINED"


# ---------------------------------------------------------------------------
# 6. Enforcement contract.
# ---------------------------------------------------------------------------

def _contract(**kw):
    d = dict(contract_id="RESPONSIBILITY-BOUNDARY-001", revision="v1",
             condition="usable_execution_opportunity",
             interfaces=(_edge(),))
    d.update(kw)
    return ResponsibilityBoundaryContract(**d)


def test_contract_starts_unproven():
    c = _contract()
    assert c.qualification == "UNPROVEN"
    assert set(c.constraints) == set(ENFORCEMENT_CONSTRAINTS)


def test_all_five_constraints_named():
    assert "dispatch_is_not_service" in ENFORCEMENT_CONSTRAINTS
    assert "service_is_not_proof_progress" in ENFORCEMENT_CONSTRAINTS
    assert ("scheduler_controlled_blocking_is_not_environment_failure"
            in ENFORCEMENT_CONSTRAINTS)
    assert ("responsibility_transfer_requires_verified_contract"
            in ENFORCEMENT_CONSTRAINTS)
    assert "human_authority_cannot_be_assumed" in ENFORCEMENT_CONSTRAINTS


def test_dispatch_without_service_violates():
    ok, _ = check_constraint(_contract(), "dispatch_is_not_service",
                             {"dispatched": True,
                              "usable_service_delivered": False})
    assert not ok


def test_dispatch_with_service_ok():
    ok, _ = check_constraint(_contract(), "dispatch_is_not_service",
                             {"dispatched": True,
                              "usable_service_delivered": True})
    assert ok


def test_unverified_progress_claim_violates():
    ok, _ = check_constraint(_contract(), "service_is_not_proof_progress",
                             {"usable_service_delivered": True,
                              "claimed_progress": True,
                              "verifier_confirmed_progress": False})
    assert not ok


def test_scheduler_blocking_mislabeled_rejected():
    ok, finding = check_constraint(
        _contract(),
        "scheduler_controlled_blocking_is_not_environment_failure",
        {"blocked_by": "SCHEDULER", "labeled_as": "ENVIRONMENT"})
    assert not ok and "responsibility-boundary violation" in finding


def test_transfer_without_receipt_rejected():
    ok, _ = check_constraint(
        _contract(), "responsibility_transfer_requires_verified_contract",
        {"controller_changed": True, "migration_receipt": None})
    assert not ok


def test_human_authority_assumption_rejected():
    ok, _ = check_constraint(_contract(), "human_authority_cannot_be_assumed",
                             {"assumes_human_authority": True})
    assert not ok


def test_unknown_constraint():
    ok, _ = check_constraint(_contract(), "nope", {})
    assert not ok


# ---------------------------------------------------------------------------
# 7. Adversarial fault injection.
# ---------------------------------------------------------------------------

def test_fault_table_has_ten_rows_and_three_models():
    assert len(FAULT_INJECTION_TABLE) == 10
    assert set(FAULT_MODELS) == {"ENVIRONMENT_BROKEN", "SCHEDULER_BROKEN",
                                 "WORKER_BROKEN"}
    for defect, diag in FAULT_INJECTION_TABLE:
        assert defect and diag


def test_mislabeled_ownership_rejected():
    # Scheduler marks its own blocked queue as externally ineligible:
    # the auditor must see through the label.
    verdict, _, label_ok = run_fault_scenario(
        "scheduler marks its own blocked queue as externally ineligible",
        _w(environment={"producer": "t", "timestamp": 1,
                        "resource_available": True},
           scheduler={"producer": "t", "timestamp": 1,
                      "resource_requested": True,
                      "resource_assigned": False}),
        claimed_owner="ENVIRONMENT")
    assert verdict == "SCHEDULER"
    assert label_ok is False


def test_correct_label_accepted():
    _, _, label_ok = run_fault_scenario(
        "external resource never becomes available",
        _w(environment={"producer": "t", "timestamp": 1,
                        "resource_available": False},
           scheduler={"producer": "t", "timestamp": 1,
                      "resource_requested": True}),
        claimed_owner="ENVIRONMENT")
    assert label_ok is True


def test_component_supplied_assumption_insufficient():
    ok, _ = check_component_supplied_assumption(
        assumption_owner="SCHEDULER", verified_component="SCHEDULER",
        independently_justified=False, conditional=False)
    assert not ok


def test_component_supplied_assumption_ok_if_conditional():
    ok, _ = check_component_supplied_assumption(
        assumption_owner="SCHEDULER", verified_component="SCHEDULER",
        independently_justified=False, conditional=True)
    assert ok


def test_component_supplied_assumption_ok_if_independent():
    ok, _ = check_component_supplied_assumption(
        assumption_owner="SCHEDULER", verified_component="WORKER",
        independently_justified=True, conditional=False)
    assert ok


# ---------------------------------------------------------------------------
# 8. Migration receipts.
# ---------------------------------------------------------------------------

def _receipt(**kw):
    d = dict(receipt_id="MIG-1", previous_controller="SCHEDULER",
             new_controller="WORKER",
             guarantee_transferred="connection pool allocation",
             new_producer_assumption="worker pool offers connections",
             new_consumer_assumption="tasks draw from worker pool",
             interface_evidence=("pool-handoff-receipt",),
             old_receipts_applicable=("R-old-1",),
             new_tests_required=("fairness-pool",),
             effective_revision="v3")
    d.update(kw)
    return BoundaryMigrationReceipt(**d)


def test_receipt_ok():
    assert _receipt().effective_revision == "v3"


def test_receipt_rejects_same_controller():
    with pytest.raises(AssertionError):
        _receipt(new_controller="SCHEDULER")


def test_no_retroactive_absolution():
    ok, finding = check_no_retroactive_absolution(
        _receipt(), "SCHEDULER starved eligible work", "SCHEDULER")
    assert ok and "not retroactive" in finding


# ---------------------------------------------------------------------------
# 9. Three indicators; never averaged.
# ---------------------------------------------------------------------------

def test_all_qualified():
    s = AccountabilityScorecard("JUSTIFIED", "COMPLIANT", "COMPLIANT",
                                True, True)
    verdict, _ = s.overall()
    assert verdict == "QUALIFIED_IN_SCOPE"


def test_law_violation_rejects_despite_perfect_scores():
    s = AccountabilityScorecard("JUSTIFIED", "COMPLIANT", "COMPLIANT",
                                True, False)
    verdict, reason = s.overall()
    assert verdict == "REJECTED" and "LAW" in reason


def test_unjustified_assumptions_reject():
    s = AccountabilityScorecard("UNJUSTIFIED", "COMPLIANT", "COMPLIANT",
                                True, True)
    verdict, _ = s.overall()
    assert verdict == "REJECTED"


def test_interface_mismatch_rejects():
    s = AccountabilityScorecard("JUSTIFIED", "COMPLIANT", "COMPLIANT",
                                False, True)
    verdict, _ = s.overall()
    assert verdict == "REJECTED"


def test_worker_violation_not_averaged_away():
    s = AccountabilityScorecard("JUSTIFIED", "COMPLIANT", "VIOLATED",
                                True, True)
    verdict, reason = s.overall()
    assert verdict == "REJECTED" and "does not compensate" in reason


def test_undetermined_stays_undetermined():
    s = AccountabilityScorecard("JUSTIFIED", "COMPLIANT", "UNDETERMINED",
                                True, True)
    verdict, _ = s.overall()
    assert verdict == "UNDETERMINED"


def test_indicators_are_three():
    assert len(INDICATORS) == 3


# ---------------------------------------------------------------------------
# 10. Decisive experiment: A/B/C with false blame.
# ---------------------------------------------------------------------------

def test_case_a_environment_no_false_blame():
    verdict, _, ok = decisive_experiment_case("A")
    assert ok and verdict == "ENVIRONMENT"


def test_case_b_scheduler_no_false_blame():
    verdict, _, ok = decisive_experiment_case("B")
    assert ok and verdict == "SCHEDULER"


def test_case_c_worker_no_false_blame():
    verdict, _, ok = decisive_experiment_case("C")
    assert ok and verdict == "WORKER"


def test_case_a_sees_through_false_blame():
    verdict, _, ok = decisive_experiment_case("A", false_blame="SCHEDULER")
    assert ok and verdict == "ENVIRONMENT"


def test_case_b_sees_through_false_blame():
    verdict, _, ok = decisive_experiment_case("B", false_blame="ENVIRONMENT")
    assert ok and verdict == "SCHEDULER"


def test_case_c_sees_through_false_blame():
    verdict, _, ok = decisive_experiment_case("C", false_blame="SCHEDULER")
    assert ok and verdict == "WORKER"


def test_case_c_scheduler_fairness_may_stay_qualified():
    # In case C the scheduler delivered usable service: its fairness
    # verdict is not the worker's failure.
    verdict, _, ok = decisive_experiment_case("C")
    assert ok and verdict == "WORKER"  # not SCHEDULER


def test_unknown_case_rejected():
    with pytest.raises(AssertionError):
        decisive_experiment_case("Z")
