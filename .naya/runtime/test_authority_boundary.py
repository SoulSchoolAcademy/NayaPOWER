from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
GOVERNANCE = ROOT / ".naya" / "governance"
for path in (RUNTIME, GOVERNANCE, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import execution_controller as ec
import model_tool_gateway as gateway
import naya_power_kernel as runtime_kernel

BASE_AUTHORITY = {"authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", "actor_id": "SoulSchoolAcademy", "purpose": "governed maintenance and verification of NayaPOWER", "scope": "repo:SoulSchoolAcademy/NayaPOWER"}


def candidate(**overrides):
    value = {"id": "safe-action", "description": "perform a governed repository maintenance action", "expected_benefit": 90, "necessary_cost": 20, "risk_loss": 5, "authorization": "approved", "required_permission": "repo_write", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": False}
    value.update(overrides)
    return value


def request(**overrides):
    value = {"request_id": "BOUNDARY-TEST", "mission": "prove runtime authority closure", "context": {"test": True}, "authority": dict(BASE_AUTHORITY), "constitution_version": "1.0.0", "candidates": [candidate()]}
    value.update(overrides)
    return value


def test_runtime_kernel_accepts_real_registry_authority():
    receipt = runtime_kernel.evaluate(request())
    assert receipt["decision"] == "SELECT", receipt
    assert receipt["selected_candidate"] == "safe-action", receipt
    assert receipt["authorization_authority"] == "canonical registry + .naya/governance/governance_kernel.py"


def test_runtime_kernel_rejects_fabricated_authority_even_when_model_says_approved():
    receipt = runtime_kernel.evaluate(request(authority={**BASE_AUTHORITY, "authority_id": "FABRICATED-AUTHORITY"}))
    assert receipt["decision"] == "ESCALATE", receipt
    assert receipt["selected_candidate"] is None, receipt


def test_runtime_kernel_rejects_permission_not_granted_by_authority():
    receipt = runtime_kernel.evaluate(request(candidates=[candidate(required_permission="deploy_public_runtime")]))
    assert receipt["decision"] == "ESCALATE", receipt
    assert receipt["selected_candidate"] is None, receipt


def test_runtime_kernel_rejects_missing_authority_id():
    missing = dict(BASE_AUTHORITY)
    missing.pop("authority_id")
    receipt = runtime_kernel.evaluate(request(authority=missing))
    assert receipt["decision"] == "ESCALATE", receipt


def _claimed(path: Path, *, reset: bool = False):
    ec.STATE = path
    if reset and path.exists():
        path.unlink()
    ec.transition("CLAIMED", claim_id="CL-BOUNDARY", block_id="B-BOUNDARY", owner="SoulSchoolAcademy", scope=["repo:SoulSchoolAcademy/NayaPOWER"], start_head="head-1")


def test_tool_gateway_requires_registry_authority_and_claim_binding():
    original_state = ec.STATE
    try:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "EXECUTION-STATE.json"
            _claimed(state_path)
            action = {"action_id": "ACT-BOUNDARY", "action_type": "repo_write", "target": "docs", "purpose": "governed maintenance and verification of NayaPOWER", "risk": "L3", "protected_baseline": "head-1", "observation_target": "files", "evidence_requirement": ["commit"], "verification_requirement": ["ci"], "authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", "actor_id": "SoulSchoolAcademy", "scope": "repo:SoulSchoolAcademy/NayaPOWER"}
            result = gateway.authorize(action)
            assert result["status"] == "AUTHORIZED", result
            assert result["authority_id"] == action["authority_id"]
            assert result["execution_status"] == "EXECUTING"
            _claimed(state_path, reset=True)
            forged = dict(action, authority_id="FABRICATED-AUTHORITY")
            try:
                gateway.authorize(forged)
            except AssertionError as exc:
                assert "unknown authority_id" in str(exc)
            else:
                raise AssertionError("tool gateway accepted fabricated authority")
    finally:
        ec.STATE = original_state


if __name__ == "__main__":
    tests = [test_runtime_kernel_accepts_real_registry_authority, test_runtime_kernel_rejects_fabricated_authority_even_when_model_says_approved, test_runtime_kernel_rejects_permission_not_granted_by_authority, test_runtime_kernel_rejects_missing_authority_id, test_tool_gateway_requires_registry_authority_and_claim_binding]
    for test in tests:
        test()
        print(f"PASS — {test.__name__}")
    print(json.dumps({"status": "PASS", "tests": len(tests)}))
