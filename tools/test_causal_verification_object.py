#!/usr/bin/env python3
"""Narrow proof for the derived Causal Verification Object."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_verified_chain_reuses_existing_receipt_and_verification():
    cvo = load(ROOT / ".naya/runtime/causal_verification.py")
    receipt = {
        "id":"RCP-CVO-001",
        "user_id":"USER-001",
        "action":"smart_mail_send",
        "expected_result":"Message is delivered and retrievable.",
        "observed_result":"Message delivered; receiver retrieval confirmed.",
        "status":"SUCCESS",
        "authority_grant_id":"GRANT-001",
        "authority_issuer_id":"USER-001",
        "authority_scope":{"target":"NayaNET"},
        "authority_actions":["SMART_MAIL_SEND"],
        "authority_constraints":{"recipient_scope":"authorized"},
        "authority_status_at_execution":"AUTHORIZED",
        "authority_source_event_id":"AUTH-EVENT-001",
        "cognition_event_id":"COG-001",
        "evidence":[{"cognition_event_id":"COG-001"}],
        "learning":[{"status":"captured","statement":"Persist the causal chain."}],
    }
    vr = {
        "receipt_id":"VR-001",
        "verification_state":"outcome_verified",
        "verification_method":"independent canonical receipt verification",
        "evidence_refs":["COG-001"],
    }
    result = cvo.build_causal_verification_object(receipt, verification_receipt=vr)
    assert result["causal_status"]=="VERIFIED", result
    assert result["intent"]["action"]=="smart_mail_send"
    assert result["authority"]["status"]=="AUTHORIZED"
    assert result["permission"]["scope"]["target"]=="NayaNET"
    assert result["evidence"]["refs"]==["COG-001"]
    assert result["receipt"]["execution_receipt_id"]=="RCP-CVO-001"

def test_unverified_chain_never_upgrades():
    cvo = load(ROOT / ".naya/runtime/causal_verification.py")
    receipt = {
        "id":"RCP-CVO-002",
        "action":"smart_mail_send",
        "expected_result":"Message is delivered.",
        "observed_result":"Message delivered.",
        "status":"SUCCESS",
        "evidence":[{"cognition_event_id":"COG-002"}],
    }
    vr = {"receipt_id":"VR-002","verification_state":"recorded","evidence_refs":["COG-002"]}
    result = cvo.build_causal_verification_object(receipt, verification_receipt=vr)
    assert result["causal_status"]=="PARTIAL", result
    assert "AUTHORITY_NOT_VERIFIED" in result["causal_gaps"]
    assert "INDEPENDENT_VERIFICATION_NOT_PROVEN" in result["causal_gaps"]

if __name__=="__main__":
    test_verified_chain_reuses_existing_receipt_and_verification()
    test_unverified_chain_never_upgrades()
    print("PASS causal verification object")
