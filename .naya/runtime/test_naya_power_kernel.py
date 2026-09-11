#!/usr/bin/env python3
"""Real dependency-free self-test for Naya Power Runtime Kernel v1."""
from __future__ import annotations

import json

import naya_power_kernel as kernel


def test_contract_loads():
    contract = kernel.load_contract()
    assert contract["contract_id"] == "NAYA-POWER-RUNTIME"
    assert contract["version"] == "1.0.0"
    assert contract["principles"]["human_life_is_non_compensable"] is True


def test_safe_action_is_selected_by_value():
    result = kernel.self_test()
    row = next(item for item in result["tests"] if item["test"] == "safe-value-selection")
    assert row["passed"] is True, row
    assert row["actual"] == "SELECT"


def test_human_life_boundary_cannot_be_bought_back():
    result = kernel.evaluate(kernel.demo_requests()[1][1])
    assert result["decision"] == "SELECT"
    assert result["selected_candidate"] == "safe"
    harm = next(x for x in result["candidate_evaluations"] if x["candidate_id"] == "harm")
    assert harm["status"] == "INELIGIBLE"
    assert harm["decision"] == "REFUSE"
    assert harm["value"] is None


def test_unknown_authority_escalates():
    result = kernel.evaluate(kernel.demo_requests()[2][1])
    assert result["decision"] == "ESCALATE"
    assert result["selected_candidate"] is None


def test_governance_mutation_escalates():
    result = kernel.evaluate(kernel.demo_requests()[3][1])
    assert result["decision"] == "ESCALATE"


def test_fabricated_verification_is_rejected():
    name, request, expected = kernel.demo_requests()[4]
    try:
        kernel.evaluate(request)
    except ValueError as exc:
        assert "fabricated verification" in str(exc)
    else:
        raise AssertionError("fabricated verification was accepted")
    assert expected == "ERROR"


def test_receipt_does_not_claim_external_execution():
    result = kernel.evaluate(kernel.demo_requests()[0][1])
    assert result["evidence"]["kernel_evaluation"] == "RUNTIME-PROVEN"
    assert result["evidence"]["external_action"] == "NOT_EXECUTED_BY_KERNEL"
    assert result["verification"]["external_action_verified"] is False
    json.dumps(result)


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS {test.__name__}")
    print(f"Naya Power Runtime Kernel self-test: PASS {passed}/{len(tests)}")


if __name__ == "__main__":
    main()
