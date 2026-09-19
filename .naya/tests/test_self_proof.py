from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from self_proof import (
    FAIL, NOT_VERIFIED, OVERALL_LIMITED, OVERALL_NOT_VERIFIED,
    OVERALL_SELF_VERIFIED, PASS, REQUIRED_CHECKS,
    build_durable_self_proof_event, evaluate_self_proof,
)

def complete_evidence():
    return {name: {"status": PASS, "evidence": [f"evidence:{name}"]} for name in REQUIRED_CHECKS}

def test_complete_existing_evidence_self_verifies():
    proof = evaluate_self_proof(complete_evidence(), observed_at="2026-09-19T19:00:00+00:00")
    assert proof["overall"] == OVERALL_SELF_VERIFIED
    assert proof["failed_checks"] == []
    assert proof["unverified_checks"] == []
    assert all(check["status"] == PASS for check in proof["checks"])

def test_missing_evidence_cannot_become_pass():
    evidence = complete_evidence()
    evidence.pop("authority")
    proof = evaluate_self_proof(evidence)
    assert proof["overall"] == OVERALL_LIMITED
    assert proof["unverified_checks"] == ["authority"]
    assert proof["checks"][7]["status"] == NOT_VERIFIED

def test_failure_blocks_self_verified():
    evidence = complete_evidence()
    evidence["integrity"] = {"status": FAIL, "evidence": ["integrity-regression"]}
    proof = evaluate_self_proof(evidence)
    assert proof["overall"] == OVERALL_NOT_VERIFIED
    assert proof["failed_checks"] == ["integrity"]
    assert proof["unverified_checks"] == []

def test_durable_event_reuses_activity_shape_and_contains_proof():
    proof = evaluate_self_proof(complete_evidence(), observed_at="2026-09-19T19:00:00+00:00")
    event = build_durable_self_proof_event(
        proof, event_id="SE-20260919-190000-self-proof-v1-test",
        claim_id="SELF-PROOF-CLAIM", action_id="SELF-PROOF-ACTION",
        decision_id="SELF-PROOF-DECISION", authority_id="SELF-PROOF-AUTHORITY",
        actor_id="NAYA-SELF-PROOF", receipt_id="SELF-PROOF-RECEIPT",
        next_action="Continue from the recorded proof boundary.", successor="NAYA",
    )
    assert event["event_type"] == "activity"
    assert event["tags"] == ["activity", "self-proof", "nayanet-self-proof-v1"]
    assert event["self_proof"]["contract"] == "NAYANET_SELF_PROOF_V1"
    assert event["verification"]["status"] == "VERIFIED"
    json.dumps(event)
