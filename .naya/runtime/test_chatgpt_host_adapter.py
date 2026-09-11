#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chatgpt_host_adapter import build_request, normalize_candidates


def candidate(**overrides):
    value = {
        "id": "candidate",
        "description": "Do the useful next action.",
        "expected_benefit": 90,
        "necessary_cost": 10,
        "risk_loss": 5,
        "authorization": "approved",
        "boundary_violations": [],
        "evidence_state": "VERIFIED",
        "reversible": True,
        "governance_sensitive": False,
    }
    value.update(overrides)
    return value


def test_normalization_preserves_contract():
    result = normalize_candidates([candidate()])
    assert result[0]["id"] == "candidate"


def test_model_verification_claim_cannot_create_evidence():
    result = normalize_candidates([candidate(model_claimed_verified=True)])
    assert result[0]["evidence_state"] == "IMPLEMENTED"


def test_request_is_built_from_host_candidates():
    result = build_request({"request_id": "HOST-1", "constitution_version": "1.0.0"}, [candidate()])
    assert result["candidates"][0]["id"] == "candidate"


def test_invalid_authority_rejected():
    try:
        normalize_candidates([candidate(authorization="self-authorized")])
    except ValueError:
        return
    raise AssertionError("invalid authority was accepted")


if __name__ == "__main__":
    tests = [
        test_normalization_preserves_contract,
        test_model_verification_claim_cannot_create_evidence,
        test_request_is_built_from_host_candidates,
        test_invalid_authority_rejected,
    ]
    for test in tests:
        test()
    print(f"PASS {len(tests)}/{len(tests)} ChatGPT host adapter tests")
