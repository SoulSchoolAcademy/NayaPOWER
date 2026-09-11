#!/usr/bin/env python3
"""Adversarial proof that runtime ranking uses the canonical Decision Calculus."""
from __future__ import annotations

import naya_power_kernel as kernel


def base_request(candidates):
    return {
        "request_id": "CALCULUS-INTEGRATION-001",
        "mission": "Choose the highest responsible verified-value software action.",
        "context": {"project": "NayaPOWER", "mode": "decision-calculus-integration"},
        "authority": {"actor": "test-harness", "scope": "runtime-evaluation"},
        "constitution_version": "1.0.0",
        "candidates": candidates,
    }


def candidate(cid, benefit, cost, risk, evidence="VERIFIED", reversible=True, boundary=None):
    return {
        "id": cid,
        "description": cid,
        "expected_benefit": benefit,
        "necessary_cost": cost,
        "risk_loss": risk,
        "authorization": "approved",
        "boundary_violations": boundary or [],
        "evidence_state": evidence,
        "reversible": reversible,
        "governance_sensitive": False,
    }


def test_old_scalar_is_not_the_runtime_authority():
    risky = candidate("risky", 100, 0, 30, evidence="UNKNOWN", reversible=False)
    safe = candidate("safe", 80, 10, 5, evidence="VERIFIED", reversible=True)
    old_risky_value = risky["expected_benefit"] - risky["necessary_cost"] - risky["risk_loss"]
    old_safe_value = safe["expected_benefit"] - safe["necessary_cost"] - safe["risk_loss"]
    assert old_risky_value > old_safe_value

    result = kernel.evaluate(base_request([risky, safe]))
    assert result["decision"] == "SELECT", result
    assert result["selected_candidate"] == "safe", result
    assert result["ranking_authority"] == "SUPERBRAIN.naya_power_decision_calculus"


def test_protected_boundary_never_enters_value_ranking():
    forbidden = candidate("forbidden", 100, 0, 0, evidence="PRODUCTION-PROVEN", reversible=False, boundary=["HUMAN_LIFE_PROTECTED"])
    safe = candidate("safe", 1, 1, 1, evidence="VERIFIED")
    result = kernel.evaluate(base_request([forbidden, safe]))
    assert result["selected_candidate"] == "safe", result
    row = next(item for item in result["candidate_evaluations"] if item["candidate_id"] == "forbidden")
    assert row["status"] == "INELIGIBLE"
    assert row["value"] is None


def test_high_consequence_uncertainty_defers_before_execution():
    risky = candidate("high-consequence-unknown", 100, 0, 95, evidence="UNKNOWN", reversible=False)
    result = kernel.evaluate(base_request([risky]))
    assert result["decision"] == "ESCALATE", result
    assert result["selected_candidate"] is None
    assert "deferred" in result["reason"].lower()


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Decision Calculus runtime integration: PASS {len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
