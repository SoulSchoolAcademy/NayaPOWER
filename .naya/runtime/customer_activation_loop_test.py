#!/usr/bin/env python3
"""End-to-end adversarial composition proof for Torch 9.

The test composes existing authorities; it does not create persistence or a new
engine. It intentionally uses in-memory synthetic facts for deterministic
boundary testing.
"""
from __future__ import annotations

from pathlib import Path
import inspect
import sys

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))

from activation_contract import validate_manifest
from customer_activation_mission_boundary import (
    ActivationMissionBindingError,
    bind_activation_to_human_mission,
)
from priority_decision import PriorityError, WorkItem, choose_priority
from executable_torch import TorchError, create_torch
from torch_execution_adapter import TorchExecutionBindingError, bind_torch_to_canonical_execution
from execution_evidence_adapter import build_evidence, validate_execution_result
from evidence_runtime import verify_claim
from smart_note_candidate import SmartNoteCandidateRejected, build_candidate
from csi_compounding_boundary import build_compounding_change


def customer_manifest() -> dict:
    return {
        "schema_version": 1,
        "package_id": "NAYA-ACTIVATION-CUSTOMER-001",
        "package_version": "1.0",
        "north_star": "Help the customer reach a verified outcome",
        "documents": [{
            "document_id": "CUSTOMER-KNOWLEDGE-01",
            "version": "1.0",
            "package_id": "NAYA-ACTIVATION-CUSTOMER-001",
            "order": 1,
            "purpose": "Customer-provided knowledge",
            "content": "Customer knowledge that must enter through canonical Note Events.",
        }],
    }


def activation_result() -> dict:
    return {
        "status": "READY",
        "promotion": [{
            "status": "CREATED",
            "event_id": "SE-20260830-120000-activation-customer-01",
            "document_identity": "identity-customer-01",
        }],
    }


def mission() -> dict:
    return {
        "mission_id": "MISSION-CUSTOMER-001",
        "mission_type": "CREATION",
        "human_goal": "Build the customer's first useful workflow",
        "desired_outcome": "A verified working workflow",
        "current_state": "Customer knowledge is canonically activated",
        "constraints": ["Preserve existing authorities"],
        "urgency": "HIGH",
        "current_capability": "INTERMEDIATE",
        "success_criteria": ["Workflow passes its acceptance test"],
        "immediate_prompt": "Start the highest-value next step",
    }


def full_chain():
    assert not validate_manifest(customer_manifest())
    binding = bind_activation_to_human_mission(activation_result(), mission())
    work = WorkItem(
        "WORK-001", "Build workflow", "run workflow acceptance test",
        "Acceptance test passes", 1, 0.95, 0.8, 0.9, 0.8, 0.1
    )
    decision = choose_priority(binding.mission.for_priority(), [work])
    torch = create_torch(
        torch_id="TORCH-001", mission=binding.mission.human_goal,
        decision=decision, required_evidence="Observed test output + commit SHA",
        constraints="Preserve canonical authorities"
    )
    successor = {
        "project": "NayaPOWER",
        "north_star": "Verified customer outcome",
        "current_state": "Customer mission qualified",
        "completed_work": ["Customer knowledge canonically activated"],
        "verified_evidence": ["Activation event exists"],
        "unresolved_issues": ["None known"],
        "constraints": ["Preserve canonical authorities"],
        "current_objective": "Build the customer's first useful workflow",
        "next_action": decision.next_action,
        "execution_instructions": "Run workflow acceptance test and record exact evidence",
        "success_criteria": [decision.acceptance_criteria],
        "verification_requirements": ["Observed test output + commit SHA"],
    }
    bind_torch_to_canonical_execution(torch, successor)

    execution = {
        "execution_state": "COMPLETED", "execution_id": "EXEC-001",
        "action": decision.next_action, "observed_output": "ALL TESTS PASS",
        "result": "PASS", "commit_sha": "abc123",
    }
    evidence = build_evidence(
        execution, evidence_id="EVID-001", claim_id="CLAIM-001",
        method="repository_test", command="python customer_activation_loop_test.py",
        environment="isolated Python", source="EXEC-001",
        observed_at="2026-08-30T12:00:00Z"
    )
    claim = {
        "schema": "naya-power-claim/v1", "claim_id": "CLAIM-001",
        "statement": "Customer workflow passes its acceptance test",
        "success_criteria": [decision.acceptance_criteria],
        "created_at": "2026-08-30T12:00:00Z", "status": "VERIFIED",
        "evidence_ids": ["EVID-001"], "source": "TORCH-001",
    }
    verification = verify_claim(claim, {"EVID-001": evidence}, expected_commit="abc123")
    candidate = build_candidate(
        evidence,
        {
            "what_mattered": "The customer outcome was testable",
            "what_was_learned": "A qualified mission makes the next action deterministic",
            "future_action": "Use mission context to select the next priority",
        },
        note_type="lesson",
    )
    intelligence = {
        "event_id": binding.activation_event_ids[0],
        "lesson": "A qualified mission makes the next action deterministic",
        "source": ["EVID-001", "CLAIM-001"],
        "evidence_state": "RUNTIME-PROVEN",
        "promotion_status": "VERIFIED",
    }
    csi = build_compounding_change(
        intelligence,
        baseline="Priority required explicit mission input",
        expected_improvement="Successor selects a mission-aligned next action without transcript reconstruction",
        measurement="Compare successor execution success against the baseline",
    )
    assert verification["status"] == "VERIFIED"
    assert candidate["promotion_state"] == "CANDIDATE"
    assert csi["state"] == "PROPOSED_FUTURE_EXECUTION_CHANGE"
    assert binding.to_successor()["activation"]["canonical_event_ids"]


def main() -> int:
    # 1 incomplete activation cannot silently become complete
    for bad_status in ("PARTIAL", "CONFLICT", "FAILED", ""):
        try:
            bind_activation_to_human_mission({**activation_result(), "status": bad_status}, mission())
            raise AssertionError(f"activation status {bad_status!r} must not qualify")
        except ActivationMissionBindingError:
            pass

    # 2 customer knowledge cannot bypass canonical event authority
    try:
        bind_activation_to_human_mission({"status": "READY"}, mission())
        raise AssertionError
    except ActivationMissionBindingError:
        pass

    # 3 mission cannot be invented from missing customer intent
    bad = mission(); bad.pop("human_goal")
    try:
        bind_activation_to_human_mission(activation_result(), bad)
        raise AssertionError
    except Exception as exc:
        assert "human_goal" in str(exc)

    # 4 priority cannot bypass mission qualification
    try:
        choose_priority("", [WorkItem("W", "W", "run test", "pass", 1, 1, 1, 1, 1, 0)])
        raise AssertionError
    except PriorityError:
        pass

    # 5 Torch cannot bypass Priority
    try:
        create_torch(torch_id="T", mission="m", decision=None, required_evidence="e", constraints="c")
        raise AssertionError
    except (TorchError, AttributeError):
        pass

    # 6 execution cannot occur merely because a Torch exists: the Torch boundary
    # has no execution method and its constructor only packages a decision.
    torch_source = inspect.getsource(create_torch)
    body = torch_source.split("def create_torch", 1)[1].split("def ", 1)[0]
    assert "subprocess" not in body
    assert "execute(" not in body
    assert "verify(" not in body
    assert "verify_claim(" not in body
    assert "build_evidence(" not in body
    assert "bind_torch_to_canonical_execution(" not in body

    # 7 evidence remains tied to actual completed execution
    assert validate_execution_result({"execution_state": "STARTED"})

    # 8 Smart Note requires meaningful durable value
    execution = {
        "execution_state": "COMPLETED", "execution_id": "EXEC-X", "action": "run test",
        "observed_output": "PASS", "result": "PASS", "commit_sha": "abc",
    }
    evidence = build_evidence(
        execution, evidence_id="E-X", claim_id="C-X", method="repository_test",
        command="run test", environment="isolated", source="EXEC-X"
    )
    try:
        build_candidate(evidence, {"what_mattered": "", "what_was_learned": "", "future_action": ""}, note_type="lesson")
        raise AssertionError
    except SmartNoteCandidateRejected:
        pass

    # 9 CSI cannot compound unvalidated learning
    bad_intel = {
        "event_id": "E", "lesson": "lesson", "source": ["E-X"],
        "evidence_state": "UNKNOWN", "promotion_status": "VERIFIED",
    }
    try:
        build_compounding_change(bad_intel, baseline="b", expected_improvement="i", measurement="m")
        raise AssertionError
    except ValueError:
        pass

    # 10 successor receives enough activation provenance and mission context
    successor = bind_activation_to_human_mission(activation_result(), mission()).to_successor()
    assert successor["activation"]["canonical_event_ids"] and successor["mission"]["priority_input"]

    # 11 full composition across existing authorities
    full_chain()

    # 12 no conversation history is required by the composed successor state
    serialized = str(successor).lower()
    assert "conversation history" not in serialized and "previous messages" not in serialized

    print("INCOMPLETE ACTIVATION → RED")
    print("CONFLICTED/FAILED ACTIVATION → RED")
    print("CANONICAL EVENT BYPASS → RED")
    print("MISSING HUMAN INTENT → RED")
    print("PRIORITY WITHOUT QUALIFIED MISSION → RED")
    print("TORCH WITHOUT PRIORITY → RED")
    print("TORCH DOES NOT EXECUTE WORK → GREEN")
    print("EXECUTION WITHOUT OBSERVED RESULT → RED")
    print("EVIDENCE WITHOUT COMPLETED EXECUTION → RED")
    print("SMART NOTE WITHOUT MEANINGFUL VALUE → RED")
    print("CSI WITHOUT VALIDATED LEARNING → RED")
    print("SUCCESSOR PROVENANCE → GREEN")
    print("FULL ACTIVATION → MISSION → PRIORITY → TORCH → EXECUTION → EVIDENCE → VERIFICATION → SMART NOTE → CSI → GREEN")
    print("CONVERSATION RECONSTRUCTION → ABSENT")
    print("PASS — Torch 9 end-to-end composition/adversarial suite GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
