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
from execution_preflight_gate import approved_preflight
from universal_execution_gate import DecisionObject, Epistemic, Risk, UniversalExecutionGate, VerificationPlan, load_registry

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
    original_sessions = (ec.SESSIONS_ROOT, ec.SESSIONS_INDEX_PATH)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "EXECUTION-STATE.json"
            ec.SESSIONS_ROOT = Path(tmp) / "sessions"
            ec.SESSIONS_INDEX_PATH = ec.SESSIONS_ROOT / "INDEX.json"
            registry = load_registry()
            authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
            gate = UniversalExecutionGate(registry)
            decision = DecisionObject(
                decision_id="BOUNDARY-DECISION",
                mission="prove runtime authority closure",
                actor_id=authority.principal_id,
                action="repo_write",
                purpose=authority.purpose,
                scope=authority.scope,
                current_truth="repository mutation requested",
                gap="gateway requires canonical gate-issued authorization",
                evidence=("evidence:registry-grant",),
                epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
                consequence="governed repository write",
                reversible=True,
                risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
                alternatives=("do_not_execute",),
                expected_value="authorized bounded mutation",
                required_permission="repo_write",
                verification=VerificationPlan("post-write state", "verification passes", ("stop",)),
                necessary_power=frozenset({"repo_write"}),
                requested_power=frozenset({"repo_write"}),
            )
            action = {
                "action_id": "ACT-BOUNDARY",
                "action_type": "repository_write",
                "target": "docs/Naya",
                "purpose": authority.purpose,
                "risk": "L2",
                "protected_baseline": "head-1",
                "observation_target": "changed file state",
                "evidence_requirement": ["commit_sha"],
                "verification_requirement": ["runtime_or_ci"],
                "authority_id": authority.authority_id,
                "decision_id": decision.decision_id,
                "actor_id": decision.actor_id,
                "scope": decision.scope,
                "permission": decision.action,
            }
            issued = gate.authorize(authority=authority, decision=decision, action=action)
            assert issued.allowed and issued.authorization is not None
            _claimed(state_path)
            result = gateway.authorize(
                action,
                execution_authorization=issued.authorization,
                gate=gate,
                preflight=approved_preflight(),
            )
            assert result["status"] == "AUTHORIZED", result
            assert result["authority_id"] == action["authority_id"]
            assert result["execution_status"] == "EXECUTING"

            _claimed(state_path, reset=True)
            forged = dict(action, authority_id="FABRICATED-AUTHORITY")
            try:
                gateway.authorize(
                    forged,
                    execution_authorization=issued.authorization,
                    gate=gate,
                    preflight=approved_preflight(),
                )
            except AssertionError as exc:
                assert "authority_id does not match" in str(exc)
            else:
                raise AssertionError("tool gateway accepted forged authority binding")
    finally:
        ec.STATE = original_state
        ec.SESSIONS_ROOT, ec.SESSIONS_INDEX_PATH = original_sessions


if __name__ == "__main__":
    tests = [test_runtime_kernel_accepts_real_registry_authority, test_runtime_kernel_rejects_fabricated_authority_even_when_model_says_approved, test_runtime_kernel_rejects_permission_not_granted_by_authority, test_runtime_kernel_rejects_missing_authority_id, test_tool_gateway_requires_registry_authority_and_claim_binding]
    for test in tests:
        test()
        print(f"PASS — {test.__name__}")
    print(json.dumps({"status": "PASS", "tests": len(tests)}))
