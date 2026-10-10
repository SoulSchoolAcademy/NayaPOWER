"""Tests for the Failure-to-Prevention Acceptance Contract."""
import sys
sys.path.insert(0, "drift_canary")

from failure_prevention import (
    FailureFamily,
    FailureRecord,
    LoopStep,
    PriorityClass,
    RecordState,
    acceptance_contract,
    binding_for,
    classify_failure,
    next_step,
    prioritize,
    step_ready,
)


def _full_record(**overrides):
    base = dict(
        expected_behavior="agent verifies file changed before claiming completion",
        actual_behavior="agent claimed completion without verifying",
        failure_family=FailureFamily.F6_VERIFICATION,
        root_cause="no verification step in the execution workflow",
        evidence_provenance="task run 2026-10-10, tool result showed no file write",
        prevention_control="mandatory post-action state check",
        acceptance_test="claim without verification is rejected by the gate",
        behavioral_test="held-out task: agent verifies before claiming, 5/5 trials",
        canonical_owner="tools/check_merge_consensus.py",
        state=RecordState.OBSERVED,
        recurrence="seen twice this week",
    )
    base.update(overrides)
    return FailureRecord(**base)


# --- classify_failure ---

def test_classify_safety_first():
    # F8 signal anywhere takes precedence over other families
    assert classify_failure("agent leaked private data while verifying tool output") == FailureFamily.F8_ALIGNMENT


def test_classify_truth():
    assert classify_failure("the model hallucinated a citation that does not exist") == FailureFamily.F2_TRUTH


def test_classify_verification():
    assert classify_failure("no acceptance test was run before the handoff") == FailureFamily.F6_VERIFICATION


def test_classify_understanding():
    assert classify_failure("misunderstood the requirement and built the wrong format") == FailureFamily.F1_UNDERSTANDING


def test_classify_reasoning():
    assert classify_failure("missed the edge case where the bound is zero") == FailureFamily.F3_REASONING


def test_classify_planning():
    assert classify_failure("optimized a local task instead of the mission priority") == FailureFamily.F4_PLANNING


def test_classify_tool_use():
    assert classify_failure("called the tool with invalid arguments and it failed") == FailureFamily.F5_TOOL_USE


def test_classify_memory():
    assert classify_failure("the lesson was stored but never retrieved at decision time") == FailureFamily.F7_MEMORY


def test_classify_communication():
    assert classify_failure("produced a verbose explanation with no clear answer") == FailureFamily.F9_COMMUNICATION


def test_classify_improvement():
    assert classify_failure("made the same mistake again after the fix") == FailureFamily.F10_IMPROVEMENT


def test_classify_default_is_verification_gap():
    # No signal at all -> F6: an unclassifiable failure is a verification gap
    assert classify_failure("something felt off about the deployment") == FailureFamily.F6_VERIFICATION


# --- step_ready / next_step ---

def test_observe_requires_evidence():
    r = _full_record(expected_behavior="", actual_behavior="", evidence_provenance="")
    ready, missing = step_ready(r, LoopStep.OBSERVE)
    assert not ready
    assert set(missing) == {"expected_behavior", "actual_behavior", "evidence_provenance"}


def test_observe_ready():
    r = _full_record()
    ready, missing = step_ready(r, LoopStep.OBSERVE)
    assert ready and missing == ()


def test_diagnose_requires_family_and_cause():
    r = _full_record(failure_family=None, root_cause="")  # type: ignore[arg-type]
    ready, missing = step_ready(r, LoopStep.DIAGNOSE)
    assert not ready
    assert "root_cause" in missing


def test_next_step_walks_in_order():
    # Empty-ish record: first unmet step is OBSERVE
    r = FailureRecord(
        expected_behavior="", actual_behavior="",
        failure_family=FailureFamily.F1_UNDERSTANDING,
        root_cause="", evidence_provenance="",
    )
    assert next_step(r) == LoopStep.OBSERVE


def test_next_step_none_when_complete():
    r = _full_record()
    assert next_step(r) is None


def test_repair_requires_control_and_owner():
    r = _full_record(prevention_control="", canonical_owner="")
    ready, missing = step_ready(r, LoopStep.REPAIR)
    assert not ready
    assert set(missing) == {"prevention_control", "canonical_owner"}


def test_prove_transfer_requires_behavioral_test():
    r = _full_record(behavioral_test="")
    ready, missing = step_ready(r, LoopStep.PROVE_TRANSFER)
    assert not ready
    assert missing == ("behavioral_test",)


# --- prioritize ---

def test_f8_always_class_a():
    assert prioritize(FailureFamily.F8_ALIGNMENT) == PriorityClass.A_HARD_BOUNDARY
    # Even when recurrent or high-leverage: hard boundary wins
    assert prioritize(FailureFamily.F8_ALIGNMENT, is_recurrent=True, spans_multiple_families=True) == PriorityClass.A_HARD_BOUNDARY


def test_recurrent_is_class_b():
    assert prioritize(FailureFamily.F6_VERIFICATION, is_recurrent=True) == PriorityClass.B_RECURRENT


def test_multi_family_is_class_c():
    assert prioritize(FailureFamily.F3_REASONING, spans_multiple_families=True) == PriorityClass.C_HIGH_LEVERAGE


def test_unestablished_cause_is_class_d():
    assert prioritize(FailureFamily.F4_PLANNING, cause_established=False) == PriorityClass.D_UNCERTAIN


def test_default_is_class_c():
    assert prioritize(FailureFamily.F9_COMMUNICATION) == PriorityClass.C_HIGH_LEVERAGE


def test_b_beats_c_and_d():
    # Recurrence outranks leverage and uncertainty
    assert prioritize(FailureFamily.F1_UNDERSTANDING, is_recurrent=True, spans_multiple_families=True, cause_established=False) == PriorityClass.B_RECURRENT


# --- acceptance_contract ---

def test_contract_accepts_complete_repair():
    result = acceptance_contract(_full_record())
    assert result.accepted
    assert result.missing == ()


def test_contract_rejects_missing_control():
    result = acceptance_contract(_full_record(prevention_control=""))
    assert not result.accepted
    assert "prevention_control" in result.missing
    assert "not a repair" in result.reason


def test_contract_rejects_missing_behavioral_test():
    result = acceptance_contract(_full_record(behavioral_test=""))
    assert not result.accepted
    assert result.missing == ("behavioral_test",)


def test_contract_rejects_missing_owner():
    result = acceptance_contract(_full_record(canonical_owner=""))
    assert not result.accepted
    assert "canonical_owner" in result.missing


def test_contract_rejects_missing_provenance():
    result = acceptance_contract(_full_record(evidence_provenance=""))
    assert not result.accepted
    assert "evidence_provenance" in result.missing


def test_contract_lists_all_missing():
    result = acceptance_contract(_full_record(
        prevention_control="", acceptance_test="", behavioral_test="",
        canonical_owner="", evidence_provenance="",
    ))
    assert not result.accepted
    assert len(result.missing) == 5


# --- binding_for ---

def test_binding_known():
    b = binding_for("behavioral_proof")
    assert b is not None and "learning_evidence_ladder" in b


def test_binding_authority():
    b = binding_for("authority_safety")
    assert b is not None and "Constitution" in b


def test_binding_unknown_returns_none():
    assert binding_for("quantum_entanglement") is None


# --- record immutability / state ---

def test_record_defaults_to_observed():
    r = FailureRecord(
        expected_behavior="x", actual_behavior="y",
        failure_family=FailureFamily.F2_TRUTH,
        root_cause="z", evidence_provenance="p",
    )
    assert r.state == RecordState.OBSERVED
    assert r.prevention_control == ""


def test_record_immutable():
    import dataclasses
    r = _full_record()
    try:
        r.root_cause = "changed"  # type: ignore[misc]
        raise AssertionError("record should be frozen")
    except dataclasses.FrozenInstanceError:
        pass
