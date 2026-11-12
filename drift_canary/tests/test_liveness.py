"""Tests: multi-node liveness & guaranteed progress.

Safety prevents wrong actions; liveness ensures eligible work makes
progress. Neither may be sacrificed to satisfy the other.

Covers: the state machine (WAITING_AUTHORITY can never become COMPLETED),
three-failure detection (deadlock / livelock / starvation), progress
witnesses (no invented progress), recovery validity (never weakens LAW),
the conditional guarantee, the ten adversarial cases, and the three-run
decisive experiment with cold-successor reconstruction.
"""
import pytest

from ..liveness import (
    LivenessObligation, WorkflowState, ProgressWitness, RecoveryAction,
    LivenessReceipt,
    LIVENESS_TYPES, WORKFLOW_STATES, LEGAL_TRANSITIONS, FAILURE_CLASSES,
    LIVENESS_TECHNIQUES, FAIRNESS_ASSUMPTIONS, NON_PROGRESS_EVENTS,
    STANDARD_MILESTONES, RECOVERY_MECHANISMS,
    transition, find_wait_cycles, detect_deadlock, detect_livelock,
    detect_starvation, is_genuine_progress, witness_coverage,
    recovery_valid, check_conditional_liveness, assess_liveness,
    cold_successor_reconstruct,
)
from ..propagation import MeaningEnvelope


def std_obligation(liveness_type="TASK_COMPLETION", obligation_id="LIVE-001"):
    return LivenessObligation(
        obligation_id=obligation_id, revision="v1",
        liveness_type=liveness_type,
        participants=("KNOW", "LAW", "ACT", "VERIFY"),
        trigger="AUTHORIZED_WORKFLOW_ACCEPTED",
        progress_target="VERIFIED_EXECUTION_OUTCOME",
        dependency_graph=(("KNOW", "LAW"), ("LAW", "ACT"), ("ACT", "VERIFY")),
        enabled_conditions=("authorization_remains_valid",
                            "required_evidence_remains_eligible",
                            "dependencies_available"),
        fairness_assumptions=("weak_fairness",),
        progress_witnesses=("KNOW_RECEIPT", "LAW_RECEIPT",
                            "ACT_EXECUTION_RECEIPT", "VERIFY_RECEIPT"),
        deadline_policy=(("know_stage", 30), ("law_stage", 30)),
        recovery_policy=("bounded_retry", "reassignment", "escalation"),
        external_blockers=("human_approval", "outage"),
        environment=MeaningEnvelope())


def wf(workflow_id="W-1", state="RUNNABLE", since_seq=0):
    return WorkflowState(workflow_id, state, since_seq)


# ---------------------------------------------------------------------------
# State machine: the hard gates.
# ---------------------------------------------------------------------------

def test_waiting_authority_can_never_become_completed():
    """The liveness machinery has no edge WAITING_AUTHORITY -> COMPLETED."""
    st = wf(state="WAITING_AUTHORITY")
    assert "COMPLETED" not in LEGAL_TRANSITIONS["WAITING_AUTHORITY"]
    ok, reason = transition(st, "COMPLETED")
    assert not ok
    assert "never" in reason or "illegal" in reason


def test_waiting_authority_leaves_only_on_real_authorization():
    st = wf(state="WAITING_AUTHORITY")
    ok, reason = transition(st, "RUNNABLE", authorization="")
    assert not ok
    assert "authorization" in reason.lower()
    ok, new = transition(st, "RUNNABLE", authorization="LAW-RECEIPT-77")
    assert ok
    assert new.state == "RUNNABLE"


def test_completed_is_terminal():
    st = wf(state="COMPLETED")
    for target in WORKFLOW_STATES:
        ok, _ = transition(st, target)
        assert not ok, f"COMPLETED -> {target} must be impossible"


def test_happy_path_transitions():
    st = wf()
    ok, st = transition(st, "IN_PROGRESS")
    assert ok and st.state == "IN_PROGRESS"
    ok, st = transition(st, "COMPLETED")
    assert ok and st.state == "COMPLETED"


def test_deadlock_suspected_recovers_via_governed_path():
    st = wf(state="DEADLOCK_SUSPECTED")
    ok, new = transition(st, "BLOCKED_RECOVERABLE")
    assert ok and new.state == "BLOCKED_RECOVERABLE"
    ok, new = transition(new, "RUNNABLE")
    assert ok


def test_unknown_target_rejected():
    ok, reason = transition(wf(), "VANISHED")
    assert not ok


# ---------------------------------------------------------------------------
# Deadlock detection.
# ---------------------------------------------------------------------------

def test_three_node_cycle_no_escape_is_deadlock():
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",),
                "VERIFY": ("ACT",)}
    verdict, evidence = detect_deadlock(wait_for, {})
    assert verdict == "DEADLOCK"
    assert evidence


def test_cycle_with_timeout_escape_is_not_deadlock():
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",)}
    escapes = {"KNOW": ("timeout",), "LAW": ("timeout",), "ACT": ("timeout",)}
    verdict, _ = detect_deadlock(wait_for, escapes)
    assert verdict == "CYCLE_WITH_ESCAPE"


def test_no_cycle_no_deadlock():
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": (),
                "VERIFY": ("ACT",)}
    verdict, _ = detect_deadlock(wait_for, {})
    assert verdict == "NO_DEADLOCK"


def test_find_wait_cycles_deduplicates_rotations():
    wait_for = {"A": ("B",), "B": ("C",), "C": ("A",)}
    cycles = find_wait_cycles(wait_for)
    assert len(cycles) == 1


def test_partial_escape_still_deadlock():
    """One trapped member is enough: the cycle cannot drain."""
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",)}
    escapes = {"KNOW": ("timeout",), "LAW": ("timeout",)}  # ACT trapped
    verdict, evidence = detect_deadlock(wait_for, escapes)
    assert verdict == "DEADLOCK"
    assert "ACT" in evidence[0]


# ---------------------------------------------------------------------------
# Livelock detection.
# ---------------------------------------------------------------------------

def test_retries_without_progress_is_livelock():
    history = tuple((i, "BLOCKED_RECOVERABLE") for i in range(6))
    verdict, evidence = detect_livelock(history, ())
    assert verdict == "LIVELOCK_SUSPECTED"
    assert evidence


def test_retries_with_progress_marks_is_not_livelock():
    history = ((0, "BLOCKED_RECOVERABLE"), (1, "IN_PROGRESS"),
               (2, "BLOCKED_RECOVERABLE"), (3, "IN_PROGRESS"))
    verdict, _ = detect_livelock(history, (1, 3))
    assert verdict == "NO_LIVELOCK"


def test_empty_history_is_not_livelock():
    assert detect_livelock((), ())[0] == "NO_LIVELOCK"


# ---------------------------------------------------------------------------
# Starvation detection.
# ---------------------------------------------------------------------------

def test_eligible_denied_opportunity_is_starvation():
    verdict, evidence = detect_starvation(
        {"W-low": 0}, {"W-low": 0}, {"W-low": 25}, age_threshold=10, now=50)
    assert verdict == "STARVATION_SUSPECTED"
    assert "W-low" in evidence[0]


def test_eligible_with_opportunities_is_not_starvation():
    verdict, _ = detect_starvation(
        {"W-low": 0}, {"W-low": 5}, {"W-low": 25}, age_threshold=10)
    assert verdict == "NO_STARVATION"


def test_young_request_is_not_starvation():
    verdict, _ = detect_starvation(
        {"W-new": 95}, {"W-new": 0}, {"W-new": 25}, age_threshold=10)
    assert verdict == "NO_STARVATION"


# ---------------------------------------------------------------------------
# Progress witnesses: no invented progress.
# ---------------------------------------------------------------------------

def test_heartbeat_is_never_progress():
    genuine, reason = is_genuine_progress("heartbeat", "", False)
    assert not genuine
    assert "not progress" in reason


def test_status_rewrite_is_never_progress():
    genuine, _ = is_genuine_progress("status_rewrite", "", False)
    assert not genuine


def test_bare_retry_is_never_progress():
    genuine, _ = is_genuine_progress("retry_attempt", "", False)
    assert not genuine


def test_obligation_state_change_is_progress():
    genuine, _ = is_genuine_progress("evidence_returned",
                                     "KNOW: evidence qualified", True)
    assert genuine


def test_activity_without_outcome_movement_is_not_progress():
    genuine, reason = is_genuine_progress("requeued", "", False)
    assert not genuine
    assert "activity is not progress" in reason


def test_witness_coverage_reports_missing():
    obl = std_obligation()
    witnesses = (ProgressWitness("W-1", "KNOW", "KNOW_RECEIPT", "R-1", 3,
                                 obligation_delta="KNOW: qualified"),)
    covered, missing = witness_coverage(obl, witnesses)
    assert covered == ("KNOW_RECEIPT",)
    assert set(missing) == {"LAW_RECEIPT", "ACT_EXECUTION_RECEIPT",
                            "VERIFY_RECEIPT"}


def test_witness_requires_milestone():
    with pytest.raises(AssertionError):
        ProgressWitness("W-1", "KNOW", "", "R-1", 3)


def test_standard_milestones_cover_nine_nodes():
    for node in ("SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT",
                 "VERIFY", "LEARN", "EVOLVE"):
        assert node in STANDARD_MILESTONES


# ---------------------------------------------------------------------------
# Recovery: never weakens LAW.
# ---------------------------------------------------------------------------

def test_recovery_weakening_law_is_invalid():
    action = RecoveryAction("REC-1", "W-1", "bounded_retry",
                            law_receipt="LAW-R-1",
                            preserves_authority=False)
    ok, reason = recovery_valid(action)
    assert not ok
    assert "INVALID REPAIR" in reason


def test_recovery_without_law_receipt_is_invalid():
    action = RecoveryAction("REC-1", "W-1", "reassignment", law_receipt="")
    ok, _ = recovery_valid(action)
    assert not ok


def test_valid_bounded_retry():
    action = RecoveryAction("REC-1", "W-1", "bounded_retry",
                            law_receipt="LAW-R-1")
    ok, _ = recovery_valid(action)
    assert ok


def test_reassignment_without_idempotency_is_invalid():
    action = RecoveryAction("REC-1", "W-1", "reassignment",
                            law_receipt="LAW-R-1",
                            preserves_idempotency=False)
    ok, reason = recovery_valid(action)
    assert not ok
    assert "duplicate" in reason


def test_unknown_mechanism_rejected():
    with pytest.raises(AssertionError):
        RecoveryAction("REC-1", "W-1", "weaken_law")


# ---------------------------------------------------------------------------
# Conditional guarantee: [](Eligible & Fair => <>Completed).
# ---------------------------------------------------------------------------

def test_ineligible_work_has_no_liveness_duty():
    """WAITING_AUTHORITY is not a liveness failure. Liveness does not
    create permission and must not pressure ACT across the boundary."""
    obl = std_obligation()
    verdict, evidence = check_conditional_liveness(
        obl, wf(state="WAITING_AUTHORITY"), eligible=False,
        fairness_holds=True)
    assert verdict == "NO_VIOLATION"
    assert "liveness requires nothing" in evidence[0]


def test_broken_fairness_is_assumption_failure_not_violation():
    obl = std_obligation()
    verdict, _ = check_conditional_liveness(
        obl, wf(state="IN_PROGRESS"), eligible=True, fairness_holds=False)
    assert verdict == "ASSUMPTION_FAILED"


def test_eligible_stuck_with_fairness_is_violation():
    obl = std_obligation()
    verdict, _ = check_conditional_liveness(
        obl, wf(state="DEADLOCK_SUSPECTED"), eligible=True,
        fairness_holds=True)
    assert verdict == "LIVENESS_VIOLATION"


def test_completed_is_no_violation():
    obl = std_obligation()
    verdict, _ = check_conditional_liveness(
        obl, wf(state="COMPLETED"), eligible=True, fairness_holds=True)
    assert verdict == "NO_VIOLATION"


# ---------------------------------------------------------------------------
# Ten adversarial cases.
# ---------------------------------------------------------------------------

def _four_node_obligation():
    return std_obligation()


def test_adv1_three_node_circular_dependency_detected():
    """Three-node circular dependency: detect and classify genuine deadlock."""
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",)}
    verdict, _ = detect_deadlock(wait_for, {})
    assert verdict == "DEADLOCK"


def test_adv2_repeated_retries_identified_as_livelock():
    """Repeated retries without new progress: livelock; stop retries."""
    history = tuple((i, "WAITING_DEPENDENCY") for i in range(8))
    verdict, evidence = detect_livelock(history, (), retry_threshold=3)
    assert verdict == "LIVELOCK_SUSPECTED"
    assert evidence


def test_adv3_starved_low_priority_task_detected():
    """Low-priority authorized task never scheduled: starvation."""
    verdict, _ = detect_starvation({"W-low": 0}, {"W-low": 0},
                                   {"W-low": 40}, age_threshold=10, now=50)
    assert verdict == "STARVATION_SUSPECTED"


def test_adv4_crashed_worker_reassigned_safely():
    """Worker crashes after accepting: reassign without duplicate effect."""
    action = RecoveryAction("REC-4", "W-1", "reassignment",
                            law_receipt="LAW-R-4", preserves_idempotency=True)
    ok, _ = recovery_valid(action)
    assert ok
    dup = RecoveryAction("REC-4b", "W-1", "reassignment",
                         law_receipt="LAW-R-4", preserves_idempotency=False)
    ok, _ = recovery_valid(dup)
    assert not ok


def test_adv5_law_refusal_is_valid_disposition_not_completion():
    """LAW refuses: governed refusal satisfies disposition, not completion."""
    obl = std_obligation()
    # A refusal is a governed terminal disposition for DISPOSITION...
    disp = std_obligation(liveness_type="DISPOSITION")
    v, _ = check_conditional_liveness(disp, wf(state="COMPLETED"),
                                      eligible=True, fairness_holds=True)
    assert v == "NO_VIOLATION"
    # ...but TASK_COMPLETION for a refused task is not eligible work.
    v, e = check_conditional_liveness(obl, wf(state="WAITING_AUTHORITY"),
                                      eligible=False, fairness_holds=True)
    assert v == "NO_VIOLATION"
    assert obl.liveness_type == "TASK_COMPLETION"


def test_adv6_human_approval_pending_preserved_not_bypassed():
    """Human approval pending: preserve waiting state; never bypass."""
    st = wf(state="WAITING_AUTHORITY")
    ok, _ = transition(st, "COMPLETED")
    assert not ok
    ok, _ = transition(st, "IN_PROGRESS")
    assert not ok  # cannot skip the authorization either


def test_adv7_ineligible_evidence_suspends_dependents_only():
    """Evidence ineligible mid-workflow: suspend dependent work; unrelated
    work keeps progressing."""
    obl = _four_node_obligation()
    dep = wf("W-dep", "WAITING_DEPENDENCY")
    other = wf("W-other", "IN_PROGRESS")
    v_dep, _ = check_conditional_liveness(obl, dep, eligible=False,
                                          fairness_holds=True)
    v_other, _ = check_conditional_liveness(obl, other, eligible=True,
                                            fairness_holds=True)
    assert v_dep == "NO_VIOLATION"      # governed waiting, not a failure
    assert v_other == "NO_VIOLATION"    # unrelated work unaffected


def test_adv8_missing_verify_handoff_detected():
    """VERIFY never receives ACT's receipt: missing handoff in the
    dependency graph is a progress failure, recoverable or escalated."""
    obl = _four_node_obligation()
    assert ("ACT", "VERIFY") in obl.dependency_graph
    # No VERIFY_RECEIPT witness produced -> coverage reports it missing.
    covered, missing = witness_coverage(obl, (
        ProgressWitness("W-1", "ACT", "ACT_EXECUTION_RECEIPT", "R-A", 9,
                        obligation_delta="ACT: executed"),))
    assert "VERIFY_RECEIPT" in missing


def test_adv9_two_successors_enforce_idempotency():
    """Two successors attempt the same work: valid ownership + idempotency."""
    first = RecoveryAction("REC-9a", "W-1", "reassignment",
                           law_receipt="LAW-R-9", preserves_idempotency=True)
    second = RecoveryAction("REC-9b", "W-1", "reassignment",
                            law_receipt="LAW-R-9", preserves_idempotency=True)
    assert recovery_valid(first)[0] and recovery_valid(second)[0]
    # Same action id twice would be a duplicate effect at the ledger layer;
    # the mechanism requires idempotency to make the second a no-op.
    assert first.action_id != second.action_id


def test_adv10_normal_workflow_completes_with_witnesses():
    """Normal eligible workflow: independently verified completion."""
    obl = _four_node_obligation()
    witnesses = (
        ProgressWitness("W-1", "KNOW", "KNOW_RECEIPT", "R-K", 1,
                        obligation_delta="KNOW: evidence qualified"),
        ProgressWitness("W-1", "LAW", "LAW_RECEIPT", "R-L", 2,
                        obligation_delta="LAW: authorized"),
        ProgressWitness("W-1", "ACT", "ACT_EXECUTION_RECEIPT", "R-A", 3,
                        obligation_delta="ACT: executed target T-1"),
        ProgressWitness("W-1", "VERIFY", "VERIFY_RECEIPT", "R-V", 4,
                        obligation_delta="VERIFY: outcome confirmed"),
    )
    covered, missing = witness_coverage(obl, witnesses)
    assert not missing
    assert len(covered) == 4
    result = assess_liveness(
        obl, {"W-1": wf("W-1", "COMPLETED", 4)},
        {"KNOW": (), "LAW": (), "ACT": (), "VERIFY": ()}, {},
        {"W-1": ((1, "IN_PROGRESS"), (4, "COMPLETED"))},
        {"W-1": (1, 2, 3, 4)},
        {"W-1": 0}, {"W-1": 4}, {"W-1": 0},
        True, witnesses)
    assert result["overall"] == "QUALIFIED"
    assert result["type_verdicts"]["TASK_COMPLETION"] == "HOLDS"


# ---------------------------------------------------------------------------
# Three-run decisive experiment.
# ---------------------------------------------------------------------------

def _experiment_obligation():
    return std_obligation(obligation_id="LIVE-EXP-001")


def test_exp_run1_stalled_but_safe_detected():
    """Run 1: every node satisfies safety, but a wait-for dependency
    prevents completion. The auditor detects the stall; zero safety
    violations are claimed."""
    obl = _experiment_obligation()
    # Safety is clean (assumed: assess_multi_party would say QUALIFIED).
    # Liveness: the four-node cycle with no escape.
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",),
                "VERIFY": ("ACT",)}
    states = {n: wf(f"W-{n}", "WAITING_DEPENDENCY", 5) for n in
              ("KNOW", "LAW", "ACT", "VERIFY")}
    result = assess_liveness(
        obl, states, wait_for, {},
        {f"W-{n}": ((5, "WAITING_DEPENDENCY"),) for n in
         ("KNOW", "LAW", "ACT", "VERIFY")},
        {}, {f"W-{n}": 0 for n in ("KNOW", "LAW", "ACT", "VERIFY")},
        {f"W-{n}": 1 for n in ("KNOW", "LAW", "ACT", "VERIFY")},
        {f"W-{n}": 0 for n in ("KNOW", "LAW", "ACT", "VERIFY")},
        True, ())
    assert result["deadlock"][0] == "DEADLOCK"
    assert result["type_verdicts"]["WORKFLOW_PROGRESS"] == "VIOLATED"
    assert result["overall"] == "NOT_QUALIFIED"
    # And safety is a separate assessment — this module claims nothing
    # about safety violations either way.


def test_exp_run2_authorized_recovery_progresses():
    """Run 2: bounded timeout + safe reassignment. The request progresses
    to the correct outcome without fabricated evidence or LAW bypass."""
    obl = _experiment_obligation()
    action = RecoveryAction("REC-EXP-2", "W-KNOW", "timeout_release",
                            law_receipt="LAW-R-EXP",
                            preserves_idempotency=True)
    ok, _ = recovery_valid(action)
    assert ok
    # After recovery the wait-for graph is acyclic and witnesses advance.
    wait_for = {"KNOW": (), "LAW": ("KNOW",), "ACT": ("LAW",),
                "VERIFY": ("ACT",)}
    verdict, _ = detect_deadlock(wait_for, {})
    assert verdict == "NO_DEADLOCK"
    witnesses = (
        ProgressWitness("W-1", "KNOW", "KNOW_RECEIPT", "R-K2", 11,
                        obligation_delta="KNOW: evidence qualified"),
        ProgressWitness("W-1", "LAW", "LAW_RECEIPT", "R-L2", 12,
                        obligation_delta="LAW: authorized"),
        ProgressWitness("W-1", "ACT", "ACT_EXECUTION_RECEIPT", "R-A2", 13,
                        obligation_delta="ACT: executed target T-1"),
        ProgressWitness("W-1", "VERIFY", "VERIFY_RECEIPT", "R-V2", 14,
                        obligation_delta="VERIFY: outcome confirmed"),
    )
    result = assess_liveness(
        obl, {"W-1": wf("W-1", "COMPLETED", 14)}, wait_for, {},
        {"W-1": ((11, "IN_PROGRESS"), (14, "COMPLETED"))},
        {"W-1": (11, 12, 13, 14)},
        {"W-1": 10}, {"W-1": 4}, {"W-1": 0}, True, witnesses)
    assert result["overall"] == "QUALIFIED"


def test_exp_run3_human_auth_withheld_is_governed_waiting():
    """Run 3: required human authorization withheld. The workflow stays
    correctly blocked in WAITING_AUTHORITY — NOT a liveness failure for a
    task no longer eligible for automatic execution. The promised
    escalation keeps its own measurable obligation."""
    obl = _experiment_obligation()
    st = wf("W-1", "WAITING_AUTHORITY", 20)
    verdict, _ = check_conditional_liveness(obl, st, eligible=False,
                                            fairness_holds=True)
    assert verdict == "NO_VIOLATION"
    # The escalation itself is a separate disposition obligation.
    esc = std_obligation(liveness_type="DISPOSITION",
                         obligation_id="LIVE-ESC-001")
    assert esc.liveness_type == "DISPOSITION"
    assert "human_approval" in obl.external_blockers


def test_exp_cold_successor_reconstructs():
    """Cold successor receives only receipts + obligation versions and
    reconstructs which guarantee failed, what stayed intact, and whether
    recovery achieved the verified outcome."""
    obl = _experiment_obligation()
    good = LivenessReceipt(
        obligation_id="LIVE-EXP-001", revision="v1", workflow_id="W-1",
        liveness_type="TASK_COMPLETION",
        witnesses=(ProgressWitness("W-1", "KNOW", "KNOW_RECEIPT", "R-K",
                                   1, obligation_delta="KNOW: qualified"),
                   ProgressWitness("W-1", "LAW", "LAW_RECEIPT", "R-L", 2,
                                   obligation_delta="LAW: authorized"),
                   ProgressWitness("W-1", "ACT", "ACT_EXECUTION_RECEIPT",
                                   "R-A", 3, obligation_delta="ACT: executed"),
                   ProgressWitness("W-1", "VERIFY", "VERIFY_RECEIPT", "R-V",
                                   4, obligation_delta="VERIFY: confirmed")),
        techniques_applied=("fault_injection", "runtime_monitoring"),
        independent_verification="Coda-1 independent replay",
        qualification="REQUALIFIED")
    ok, gaps = cold_successor_reconstruct((good,), (obl,))
    assert ok, gaps
    # A receipt claiming qualification with missing witnesses is caught.
    bad = LivenessReceipt(
        obligation_id="LIVE-EXP-001", revision="v1", workflow_id="W-2",
        liveness_type="TASK_COMPLETION", witnesses=(),
        techniques_applied=("runtime_monitoring",),
        independent_verification="Coda-1 independent replay",
        qualification="REQUALIFIED")
    ok, gaps = cold_successor_reconstruct((bad,), (obl,))
    assert not ok
    assert any("witnesses missing" in g for g in gaps)
    # Unknown obligation version is caught.
    orphan = LivenessReceipt(
        obligation_id="LIVE-UNKNOWN", revision="v9", workflow_id="W-3",
        liveness_type="TASK_COMPLETION",
        independent_verification="Coda-1 independent replay",
        qualification="REQUALIFIED")
    ok, gaps = cold_successor_reconstruct((orphan,), (obl,))
    assert not ok


# ---------------------------------------------------------------------------
# Composition with safety: same interaction, separate verdicts.
# ---------------------------------------------------------------------------

def test_liveness_and_safety_verdicts_are_independent():
    """A workflow can be safety-clean and liveness-violated simultaneously.
    assess_liveness never asserts anything about safety."""
    obl = _experiment_obligation()
    wait_for = {"KNOW": ("LAW",), "LAW": ("ACT",), "ACT": ("KNOW",)}
    result = assess_liveness(
        obl, {"W-1": wf("W-1", "DEADLOCK_SUSPECTED", 7)}, wait_for, {},
        {"W-1": ((7, "DEADLOCK_SUSPECTED"),)}, {"W-1": ()},
        {"W-1": 0}, {"W-1": 1}, {"W-1": 0}, True, ())
    assert result["overall"] == "NOT_QUALIFIED"
    # assess_liveness reports only liveness facts: no safety verdict keys.
    assert "safety" not in {k.lower() for k in result}
    assert result["deadlock"][0] == "DEADLOCK"


def test_obligation_validation():
    with pytest.raises(AssertionError):
        LivenessObligation(obligation_id="X", revision="v1",
                           liveness_type="EVERYTHING_ALWAYS",
                           participants=("KNOW",), trigger="T",
                           progress_target="P")
    with pytest.raises(AssertionError):
        LivenessObligation(obligation_id="X", revision="v1",
                           liveness_type="DISPOSITION", participants=(),
                           trigger="T", progress_target="P")
    with pytest.raises(AssertionError):
        LivenessObligation(obligation_id="X", revision="v1",
                           liveness_type="DISPOSITION",
                           participants=("KNOW",), trigger="T",
                           progress_target="P",
                           fairness_assumptions=("vibes",))
