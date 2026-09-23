#!/usr/bin/env python3
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    assert spec and spec.loader
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def test_universal_adapter_preserves_verified_causal_proof():
    cvo=load(ROOT/".naya/runtime/causal_verification.py","cvo")
    via=load(ROOT/".naya/runtime/verified_ai_action.py","via")
    receipt={
      "id":"RCP-VAA-001","user_id":"USER-001","action":"smart_mail_send",
      "expected_result":"Message is delivered.","observed_result":"Message delivered.",
      "status":"SUCCESS","authority_grant_id":"GRANT-001","authority_issuer_id":"USER-001",
      "authority_scope":{"target":"NayaNET"},"authority_actions":["SMART_MAIL_SEND"],
      "authority_status_at_execution":"AUTHORIZED","evidence":[{"cognition_event_id":"COG-001"}]
    }
    vr={"receipt_id":"VR-001","verification_state":"outcome_verified",
        "verification_method":"independent canonical receipt verification",
        "evidence_refs":["COG-001"]}
    result=via.build_verified_ai_action(receipt,verification_receipt=vr)
    assert result["schema"]=="NAYAPOWER_VERIFIED_AI_ACTION_V1"
    assert result["causal"]["causal_status"]=="VERIFIED"
    assert result["causal"]["receipt"]["execution_receipt_id"]=="RCP-VAA-001"

def test_universal_adapter_does_not_upgrade_partial_proof():
    via=load(ROOT/".naya/runtime/verified_ai_action.py","via")
    receipt={"id":"RCP-VAA-002","action":"smart_mail_send",
             "expected_result":"Message is delivered.","observed_result":"Message delivered.",
             "status":"SUCCESS","evidence":[{"cognition_event_id":"COG-002"}]}
    result=via.build_verified_ai_action(receipt)
    assert result["causal"]["causal_status"]=="PARTIAL"
    assert result["causal"]["result"]["success"] is False

if __name__=="__main__":
    test_universal_adapter_preserves_verified_causal_proof()
    test_universal_adapter_does_not_upgrade_partial_proof()
    print("PASS verified AI action")
