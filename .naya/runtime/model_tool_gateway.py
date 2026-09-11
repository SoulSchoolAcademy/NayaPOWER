#!/usr/bin/env python3
"""Authorize consequential actions only inside a claimed execution context."""
from __future__ import annotations

import argparse
from typing import Any

from execution_controller import load, transition
from risk_engine import classify

REQUIRED_ACTION = ("action_id", "action_type", "target", "purpose", "risk", "protected_baseline", "observation_target", "evidence_requirement", "verification_requirement")
ALLOWED_RISK = {"L1", "L2", "L3"}


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
    updated = transition("EXECUTING", action=action, derived_risk=derived)
    return {"status": "AUTHORIZED", "action_id": action["action_id"], "execution_status": updated["status"], "claim_id": updated["claim_id"], "block_id": updated["block_id"], "risk": derived, "side_effect_allowed": True, "proof_required_after_action": True}


def self_test() -> int:
    from execution_controller import STATE
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    try:
        if STATE.exists(): STATE.unlink()
        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="Naya-Test", scope=["test/block"], start_head="test-head")
        action = {"action_id": "ACT-TEST-001", "action_type": "repository_write", "target": "docs/Naya", "purpose": "prove gateway authorization", "risk": "L2", "protected_baseline": "test-head", "observation_target": "changed file state", "evidence_requirement": ["commit_sha"], "verification_requirement": ["runtime_or_ci"]}
        result = authorize(action)
        assert result["status"] == "AUTHORIZED" and result["execution_status"] == "EXECUTING" and result["risk"] == "L2"
        invalid = dict(action, risk="L1")
        try:
            authorize(invalid)
        except AssertionError as exc:
            assert "does not match derived risk" in str(exc)
        else:
            raise AssertionError("gateway accepted caller-supplied risk below derived risk")
        print("PASS — model/tool gateway authorization self-test GREEN")
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
