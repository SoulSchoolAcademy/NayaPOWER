#!/usr/bin/env python3
"""Authorize consequential actions only inside a claimed execution context.

The execution gateway is a hard boundary: a CLAIMED state is necessary but not
sufficient. The action must also resolve an explicit, current authority from the
canonical registry and pass the canonical governance kernel immediately before
transitioning to EXECUTING.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any

from execution_controller import load, transition
from risk_engine import classify

from governance_kernel import (  # noqa: E402
    DecisionObject,
    Epistemic,
    Risk,
    VerificationPlan,
    evaluate,
    load_authority_registry,
    resolve_authority,
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / ".naya" / "governance" / "authority-registry.json"
REQUIRED_ACTION = ("action_id", "action_type", "target", "purpose", "risk", "protected_baseline", "observation_target", "evidence_requirement", "verification_requirement", "authority_id", "actor_id", "scope")
ALLOWED_RISK = {"L1", "L2", "L3"}


def _risk_object(declared: str) -> Risk:
    return {"L1": Risk(uncertainty=1, consequence=2, irreversibility=1), "L2": Risk(uncertainty=2, consequence=4, irreversibility=2), "L3": Risk(uncertainty=3, consequence=6, irreversibility=3)}[declared]


def authorize(action: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_ACTION if action.get(key) in (None, "", [], {})]
    if missing:
        raise AssertionError("action request missing required fields: " + ", ".join(missing))
    declared = str(action["risk"]).upper()
    if declared not in ALLOWED_RISK:
        raise AssertionError("action risk must be L1, L2, or L3")
    derived = classify(action)
    if declared != derived:
        raise AssertionError(f"declared risk {declared} does not match derived risk {derived}")

    state = load()
    if state.get("status") != "CLAIMED":
        raise AssertionError(f"action gateway requires CLAIMED execution state, got {state.get('status')}")
    for key in ("claim_id", "block_id", "owner", "scope", "start_head"):
        if state.get(key) in (None, "", [], {}):
            raise AssertionError("execution context missing " + key)
    if action["protected_baseline"] != state["start_head"]:
        raise AssertionError("protected baseline does not match claimed execution baseline")
    if action["scope"] != state["scope"] and action["scope"] not in state["scope"]:
        raise AssertionError("action scope is not bound to claimed execution scope")
    if action["actor_id"] != state["owner"]:
        raise AssertionError("action actor does not match claimed execution owner")

    registry = load_authority_registry(REGISTRY_PATH)
    try:
        authority = resolve_authority(registry, authority_id=str(action["authority_id"]), actor_id=str(action["actor_id"]), purpose=str(action["purpose"]), action=str(action["action_type"]), scope=str(action["scope"]))
    except RuntimeError as exc:
        raise AssertionError(str(exc)) from exc

    decision = DecisionObject(
        decision_id=f"tool:{action['action_id']}", mission=f"execute governed tool action {action['action_id']}", actor_id=authority.principal_id,
        action=action["action_type"], purpose=authority.purpose, scope=authority.scope,
        current_truth=f"CLAIMED execution block {state['block_id']}", gap=str(action["purpose"]),
        evidence=tuple(str(x) for x in action["evidence_requirement"]) or ("claimed execution context",),
        epistemic=frozenset({Epistemic.OBSERVED}), consequence=f"tool action target={action['target']}", reversible=True,
        risk=_risk_object(declared), alternatives=("do_not_execute",), expected_value="bounded tool execution",
        required_permission=action["action_type"],
        verification=VerificationPlan(observation=str(action["observation_target"]), success_criteria="tool result satisfies verification requirement", stop_conditions=("authority revoked or expired", "scope mismatch", "verification failure")),
        necessary_power=frozenset({action["action_type"]}), requested_power=frozenset({action["action_type"]}),
    )
    result = evaluate(decision, authority, now=datetime.now(timezone.utc).isoformat())
    if not result.allowed:
        raise AssertionError("canonical governance denied tool execution: " + "; ".join(result.reasons))

    updated = transition("EXECUTING", action=action, derived_risk=derived, authority_id=authority.authority_id, authority_expires_at=authority.expires_at)
    return {"status": "AUTHORIZED", "action_id": action["action_id"], "execution_status": updated["status"], "claim_id": updated["claim_id"], "block_id": updated["block_id"], "risk": derived, "authority_id": authority.authority_id, "authority_expires_at": authority.expires_at, "side_effect_authorized": True, "side_effect_executed": False, "proof_required_after_action": True}


def self_test() -> int:
    from execution_controller import STATE
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    try:
        if STATE.exists(): STATE.unlink()
        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="SoulSchoolAcademy", scope=["repo:SoulSchoolAcademy/NayaPOWER"], start_head="test-head")
        action = {"action_id": "ACT-TEST-001", "action_type": "repo_write", "target": "docs/Naya", "purpose": "governed maintenance and verification of NayaPOWER", "risk": "L2", "protected_baseline": "test-head", "observation_target": "changed file state", "evidence_requirement": ["commit_sha"], "verification_requirement": ["runtime_or_ci"], "authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", "actor_id": "SoulSchoolAcademy", "scope": "repo:SoulSchoolAcademy/NayaPOWER"}
        stale = dict(action, protected_baseline="stale-head")
        try: authorize(stale)
        except AssertionError as exc: assert "protected baseline" in str(exc)
        else: raise AssertionError("gateway accepted a stale protected baseline")
        result = authorize(action)
        assert result["status"] == "AUTHORIZED" and result["execution_status"] == "EXECUTING" and result["authority_id"] == action["authority_id"]
        invalid = dict(action, authority_id="FABRICATED")
        try: authorize(invalid)
        except AssertionError as exc: assert "unknown authority_id" in str(exc)
        else: raise AssertionError("gateway accepted fabricated authority")
        print("PASS — model/tool gateway canonical authority self-test GREEN")
        return 0
    finally:
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["self-test"])
    args = parser.parse_args()
    raise SystemExit(self_test())
