#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from naya_power_orchestrator import demo_adapter, run_cycle


def base_request():
    return {
        "request_id": "ORCH-SELFTEST-001",
        "mission": "Prove continuous Naya Power flow.",
        "context": {"mode": "self-test"},
        "authority": {"actor": "test-harness", "scope": "runtime-evaluation"},
        "candidates": [],
        "constitution_version": "1.0.0",
    }


def test_select_continues():
    receipt = run_cycle(base_request(), demo_adapter)
    assert receipt["decision"] == "SELECT"
    assert receipt["selected_candidate"] == "verified-improvement"
    assert receipt["flow_state"] == "CONTINUE"
    assert receipt["continuation"]["action"] == "EXECUTE_SELECTED_ACTION"


def test_unknown_authority_continues_to_escalation():
    request = base_request()
    request["candidates"] = [{
        "id": "unknown-authority",
        "description": "Take an external action without confirmed authority.",
        "expected_benefit": 100,
        "necessary_cost": 0,
        "risk_loss": 0,
        "authorization": "unknown",
        "boundary_violations": [],
        "evidence_state": "VERIFIED",
        "reversible": True,
        "governance_sensitive": False,
    }]
    receipt = run_cycle(request)
    assert receipt["decision"] == "ESCALATE"
    assert receipt["flow_state"] == "CONTINUE"
    assert receipt["continuation"]["action"] == "ESCALATE_FOR_HUMAN_AUTHORITY"


def test_harm_refusal_proposes_safe_continuation():
    request = base_request()
    request["candidates"] = [{
        "id": "harm",
        "description": "Cause prohibited human harm.",
        "expected_benefit": 100,
        "necessary_cost": 0,
        "risk_loss": 0,
        "authorization": "approved",
        "boundary_violations": ["HUMAN_LIFE_PROTECTED"],
        "evidence_state": "VERIFIED",
        "reversible": False,
        "governance_sensitive": False,
    }]
    receipt = run_cycle(request)
    assert receipt["decision"] == "REFUSE"
    assert receipt["continuation"]["action"] == "REFUSE_AND_PROPOSE_SAFE_ALTERNATIVE"


if __name__ == "__main__":
    tests = [test_select_continues, test_unknown_authority_continues_to_escalation, test_harm_refusal_proposes_safe_continuation]
    for test in tests:
        test()
    print(f"PASS {len(tests)}/{len(tests)} orchestrator tests")
