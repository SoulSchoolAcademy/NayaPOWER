#!/usr/bin/env python3
"""Targeted constitutional tests for the NayaPOWER Governance Kernel V1."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".naya/control-plane/governance_kernel.py"
spec = importlib.util.spec_from_file_location("governance_kernel", MODULE_PATH)
assert spec and spec.loader
kernel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel_module)

GovernanceKernel = kernel_module.GovernanceKernel
GovernanceViolation = kernel_module.GovernanceViolation
assess_risk = kernel_module.assess_risk
receipt = kernel_module.receipt
transition = kernel_module.transition
validate_authority = kernel_module.validate_authority
validate_decision = kernel_module.validate_decision


def authority(**overrides):
    value = {
        "authority_id": "AUTH-001",
        "issuer": "human",
        "holder": "naya",
        "actor": "naya",
        "purpose": "repository-governance",
        "permissions": ["repo.read", "repo.write"],
        "scope": ["SoulSchoolAcademy/NayaPOWER"],
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "revoked_at": None,
        "status": "ACTIVE",
    }
    value.update(overrides)
    return value


def decision(**overrides):
    value = {
        "decision_id": "DEC-001",
        "mission": "govern NayaPOWER",
        "actor": "naya",
        "request": "update governed artifact",
        "purpose": "repository-governance",
        "authority": authority(),
        "scope": ["SoulSchoolAcademy/NayaPOWER"],
        "boundaries": ["constitutional"],
        "evidence": ["source-inspection"],
        "uncertainty": 1,
        "consequence": 2,
        "reversibility": 1,
        "risk": {"prohibited": False},
        "alternatives": ["inspect-only"],
        "value": {"responsible": True},
        "required_permission": "repo.write",
        "decision": "PROCEED",
        "execution_plan": ["surgical update"],
        "verification_plan": ["targeted test", "read-back"],
        "stop_conditions": ["authority invalid", "verification fails"],
        "receipt_requirements": ["all"],
        "learning_output": ["record failure if any"],
    }
    value.update(overrides)
    return value


def test_missing_mandatory_field_fails_closed():
    bad = decision()
    del bad["verification_plan"]
    try:
        validate_decision(bad)
    except GovernanceViolation:
        return
    raise AssertionError("missing mandatory field was accepted")


def test_expired_authority_fails_closed():
    expired = authority(expires_at=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat())
    try:
        validate_authority(expired, actor="naya", purpose="repository-governance", permission="repo.write")
    except GovernanceViolation:
        return
    raise AssertionError("expired authority was accepted")


def test_wrong_scope_purpose_actor_or_permission_fails_closed():
    cases = [
        authority(actor="other"),
        authority(holder="other"),
        authority(purpose="different"),
        authority(permissions=["repo.read"]),
    ]
    for item in cases:
        try:
            validate_authority(item, actor="naya", purpose="repository-governance", permission="repo.write")
        except GovernanceViolation:
            continue
        raise AssertionError("invalid authority was accepted")


def test_invalid_verification_state_promotion_fails_closed():
    for current, target in [("EXECUTED", "VERIFIED"), ("FAILED", "VERIFIED"), ("DEFERRED", "EXECUTING"), ("STOPPED", "EXECUTING")]:
        try:
            transition(current, target)
        except GovernanceViolation:
            continue
        raise AssertionError(f"illegal transition accepted: {current} -> {target}")


def test_stop_dominates_continuation():
    kernel = GovernanceKernel()
    kernel.halt("verified stop condition")
    assert kernel.halted is True
    try:
        transition("AUTHORIZED", "EXECUTING", halted=kernel.halted)
    except GovernanceViolation:
        pass
    else:
        raise AssertionError("halt did not block execution")
    try:
        kernel.clear_halt(authorized=False)
    except GovernanceViolation:
        pass
    else:
        raise AssertionError("unauthorized halt clear was accepted")


def test_risk_routing_is_deterministic():
    assert assess_risk(1, 1, 1).tier == "R0"
    assert assess_risk(2, 2, 2).tier == "R1"
    assert assess_risk(3, 3, 3).tier == "R2"
    assert assess_risk(4, 4, 4).tier == "R3"
    assert assess_risk(5, 5, 5).tier == "R4"
    assert assess_risk(1, 1, 1, prohibited=True).tier == "R5"


def test_canonical_gate_requires_authority_and_decision():
    kernel = GovernanceKernel()
    valid = decision()
    risk = kernel.gate(valid, valid["authority"])
    assert risk.tier in {"R0", "R1", "R2", "R3", "R4"}
    try:
        kernel.gate(valid, authority(permissions=["repo.read"]))
    except GovernanceViolation:
        pass
    else:
        raise AssertionError("canonical gate allowed excessive/missing permission")


def test_receipt_is_reconstructable_and_integrity_bearing():
    r = receipt(decision(), state="VERIFIED", result="ok", observation="observed", verification="independent", next_action="continue")
    required = {"receipt_id", "decision_id", "actor", "authority_id", "request", "decision", "state", "result", "observation", "verification", "timestamp", "uncertainty", "failure", "repair", "next_action", "integrity_hash"}
    assert required.issubset(r)
    assert len(r["integrity_hash"]) == 64


def main():
    tests = [
        test_missing_mandatory_field_fails_closed,
        test_expired_authority_fails_closed,
        test_wrong_scope_purpose_actor_or_permission_fails_closed,
        test_invalid_verification_state_promotion_fails_closed,
        test_stop_dominates_continuation,
        test_risk_routing_is_deterministic,
        test_canonical_gate_requires_authority_and_decision,
        test_receipt_is_reconstructable_and_integrity_bearing,
    ]
    for test in tests:
        test()
    print(f"GOVERNANCE_KERNEL_TESTS=GREEN count={len(tests)}")


if __name__ == "__main__":
    main()
