#!/usr/bin/env python3
"""Fail-closed gateway contract for consequential Naya model/tool actions.

The gateway is the adapter boundary between an external model/tool caller and
NayaPOWER execution state. A caller must present an active execution context
and explicit action metadata before the action is authorized.

This module intentionally does not execute the requested tool. It authorizes
an action request and advances the canonical execution controller to EXECUTING.
A future hosted adapter must call this gateway before performing the real side
effect, then record observation/evidence through the controller afterward.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
STATE = RUNTIME / "EXECUTION-STATE.json"
ALLOWED_RISK = {"L1", "L2", "L3"}
REQUIRED_ACTION = (
    "action_id",
    "action_type",
    "target",
    "purpose",
    "risk",
    "protected_baseline",
    "observation_target",
    "evidence_requirement",
    "verification_requirement",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def load_state() -> dict[str, Any]:
    if not STATE.exists():
        fail("no active execution context")
    return json.loads(STATE.read_text(encoding="utf-8"))


def authorize(action: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_ACTION if action.get(key) in (None, "", [], {})]
    if missing:
        fail("action request missing required fields: " + ", ".join(missing))
    supplied_risk = str(action["risk"]).upper()
    if supplied_risk not in ALLOWED_RISK:
        fail("action risk must be L1, L2, or L3")

    from risk_engine import classify
    derived_risk = classify(action)
    if supplied_risk != derived_risk:
        fail(f"declared risk {supplied_risk} does not match derived risk {derived_risk}")

    state = load_state()
    if state.get("status") != "CLAIMED":
        fail(f"action gateway requires CLAIMED execution state, got {state.get('status')}")
    for key in ("claim_id", "block_id", "owner", "scope", "start_head"):
        if state.get(key) in (None, "", [], {}):
            fail("execution context missing " + key)

    from execution_controller import transition
    updated = transition("EXECUTING", action=action, derived_risk=derived_risk)
    return {
        "status": "AUTHORIZED",
        "action_id": action["action_id"],
        "execution_status": updated["status"],
        "claim_id": updated["claim_id"],
        "block_id": updated["block_id"],
        "risk": derived_risk,
        "side_effect_allowed": True,
        "proof_required_after_action": True,
    }


def self_test() -> int:
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    try:
        from execution_controller import transition
        if STATE.exists(): STATE.unlink()
        transition(
            "CLAIMED",
            claim_id="CL-TEST",
            block_id="B-TEST",
            owner="Naya-Test",
            scope=["test/block"],
            start_head="test-head",
        )
        action = {
            "action_id": "ACT-TEST-001",
            "action_type": "repository_write",
            "target": "test/block",
            "purpose": "prove gateway authorization",
            "risk": "L2",
            "protected_baseline": "test-head",
            "observation_target": "changed file state",
            "evidence_requirement": ["commit_sha"],
            "verification_requirement": ["runtime_or_ci"],
        }
        result = authorize(action)
        assert result["status"] == "AUTHORIZED"
        assert result["execution_status"] == "EXECUTING"
        assert result["risk"] == "L2"

        invalid = json.loads(json.dumps(action))
        invalid["risk"] = "L1"
        try:
            authorize(invalid)
        except AssertionError as exc:
            assert "does not match derived risk" in str(exc)
        else:
            raise AssertionError("gateway accepted a caller-supplied risk below the derived risk")

        print("PASS — model/tool gateway authorization self-test GREEN")
        return 0
    finally:
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            return self_test()
        fail("only self-test is available in this repository-native contract")
    except (AssertionError, json.JSONDecodeError, ValueError) as exc:
        print(f"GATEWAY=RED\nFIRST_DIVERGENCE={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
