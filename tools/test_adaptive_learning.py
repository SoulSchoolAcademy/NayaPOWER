#!/usr/bin/env python3
"""Acceptance tests for NayaPOWER Adaptive Learning Engine v1."""
from __future__ import annotations

import tempfile
from pathlib import Path

import adaptive_learning as al


def base_event():
    return {
        "event_id": "INT-ADAPTIVE-001",
        "timestamp": "2026-09-06T07:00:00-07:00",
        "project": "Naya Power",
        "lesson": "Source intent is not runtime truth; verify the exact public runtime independently.",
        "source": ["architecture-discussion"],
        "evidence_state": "VERIFIED",
        "promotion_status": "CANONICAL",
        "what_happened": "A source-level result was previously treated as release truth.",
        "actual_outcome": "The runtime must be independently observed.",
        "evidence": ["independent-runtime-observation"],
    }


def test_build_event():
    event = al.build_learning_event(base_event(), {
        "intent": "Release the application",
        "action": "Inspect source and deployment",
        "expected_outcome": "Exact public runtime matches source",
        "actual_outcome": "Independent runtime verification required",
        "lesson": "Source intent is not runtime truth.",
        "root_cause": "Source and runtime were treated as equivalent evidence.",
        "recommendation": "Require source to build to deployment to exact URL to independent runtime observation.",
        "evidence_state": "VERIFIED",
        "learning_state": "OPERATIONAL",
        "preflight": "Before declaring release complete, independently observe the exact public runtime.",
        "evidence": ["runtime-test"],
    })
    assert event["learning_state"] == "OPERATIONAL"
    assert event["verification_required"] is True
    assert al.validate_learning_event(event) == []


def test_unverified_cannot_be_operational():
    event = al.build_learning_event(base_event(), {
        "lesson": "Do not repeat a known mistake.",
        "evidence_state": "IMPLEMENTED",
        "learning_state": "OPERATIONAL",
    })
    assert event["learning_state"] == "CONFIRMED"


def test_rule_is_evidence_gated():
    event = al.build_learning_event(base_event(), {
        "lesson": "Verify before claiming completion.",
        "recommendation": "Run independent verification.",
        "evidence_state": "TESTED",
    })
    rule = al.propose_rule(event)
    assert rule["state"] == "PROPOSED"

    event["evidence_state"] = "VERIFIED"
    rule = al.propose_rule(event)
    assert rule["state"] == "OPERATIONAL"


def test_preflight_matches_operational_rule():
    rules = [{
        "rule_id": "RULE-001",
        "lesson": "Source intent is not runtime truth",
        "rule": "Independently verify the exact public runtime before declaring release complete",
        "preflight": "Observe the exact public URL independently",
        "state": "OPERATIONAL",
    }]
    result = al.preflight("Deploy the source and verify the exact public runtime", rules)
    assert result["matched_rules"]
    assert result["required_checks"]


def test_outcome_does_not_self_certify():
    event = al.build_learning_event(base_event(), {"lesson": "Test learning"})
    with tempfile.TemporaryDirectory() as tmp:
        original = al.RECEIPT_DIR
        try:
            al.RECEIPT_DIR = Path(tmp)
            result = al.record_outcome(event, {
                "verified": False,
                "independent_observation": "",
                "evidence": [],
            })
            assert result["verified"] is False
            assert result["rule_promotion_allowed"] is False
        finally:
            al.RECEIPT_DIR = original


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Adaptive Learning Engine v1 tests passed: {len(tests)}")


if __name__ == "__main__":
    main()
