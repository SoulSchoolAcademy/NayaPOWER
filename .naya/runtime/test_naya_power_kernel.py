#!/usr/bin/env python3
"""Current-contract tests for Naya Power Runtime Kernel v1."""
from __future__ import annotations

import json

import naya_power_kernel as kernel


AUTHORITY = {
    "authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE",
    "actor_id": "SoulSchoolAcademy",
    "purpose": "governed maintenance and verification of NayaPOWER",
    "scope": "repo:SoulSchoolAcademy/NayaPOWER",
}


def candidate(cid, *, permission="repo_write", boundary=None, evidence="VERIFIED", reversible=True, verification_claim=None, evidence_rows=None):
    value = {
        "id": cid,
        "description": f"governed action {cid}",
        "expected_benefit": 90,
        "necessary_cost": 20,
        "risk_loss": 5,
        "authorization": "approved",
        "required_permission": permission,
        "boundary_violations": boundary or [],
        "evidence_state": evidence,
        "reversible": reversible,
        "governance_sensitive": False,
    }
    if verification_claim is not None:
        value["verification_claim"] = verification_claim
    if evidence_rows is not None:
        value["evidence"] = evidence_rows
    return value


def request(candidates, *, authority=None):
    return {
        "request_id": "RUNTIME-KERNEL-TEST",
        "mission": "Test governed runtime selection.",
        "context": {"test": True},
        "authority": authority or AUTHORITY,
        "constitution_version": "1.0.0",
        "candidates": candidates,
    }


def test_contract_loads():
    contract = kernel.load_contract()
    assert contract["contract_id"] == "NAYA-POWER-RUNTIME"
    assert contract["version"] == "1.0.0"
    assert contract["principles"]["human_life_is_non_compensable"] is True


def test_safe_action_is_selected_by_value():
    result = kernel.self_test()
    row = next(item for item in result["tests"] if item["test"] == "valid registry authority selects")
    assert row["passed"] is True, row
    assert row["actual"] == "SELECT"


def test_human_life_boundary_cannot_be_bought_back():
    forbidden = candidate("harm", boundary=["HUMAN_LIFE_PROTECTED"], evidence="PRODUCTION-PROVEN", reversible=False)
    safe = candidate("safe")
    result = kernel.evaluate(request([forbidden, safe]))
    assert result["decision"] == "SELECT", result
    assert result["selected_candidate"] == "safe", result
    harm = next(x for x in result["candidate_evaluations"] if x["candidate_id"] == "harm")
    assert harm["status"] == "INELIGIBLE"
    assert harm["decision"] == "REFUSE"
    assert harm["value"] is None


def test_unknown_authority_escalates():
    result = kernel.evaluate(request([candidate("safe")], authority={**AUTHORITY, "authority_id": "FABRICATED"}))
    assert result["decision"] == "ESCALATE"
    assert result["selected_candidate"] is None


def test_governance_mutation_escalates():
    result = kernel.evaluate(request([candidate("deploy", permission="deploy_public_runtime")]))
    assert result["decision"] == "ESCALATE"
    assert result["selected_candidate"] is None


def test_fabricated_verification_is_rejected():
    forged = candidate("forged", verification_claim=True)
    try:
        kernel.evaluate(request([forged]))
    except ValueError as exc:
        assert "fabricated verification" in str(exc)
    else:
        raise AssertionError("fabricated verification was accepted")


def test_receipt_does_not_claim_external_execution():
    result = kernel.evaluate(request([candidate("safe")]))
    assert result["evidence"]["kernel_evaluation"] == "RUNTIME-PROVEN"
    assert result["evidence"]["external_action"] == "NOT_EXECUTED_BY_KERNEL"
    assert result["verification"]["external_action_verified"] is False
    json.dumps(result)


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Naya Power Runtime Kernel self-test: PASS {len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
