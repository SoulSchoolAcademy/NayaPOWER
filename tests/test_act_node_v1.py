import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_act_is_registered_without_parallel_authority_or_receipt_store():
    r=json.loads((ROOT/"BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text())
    a=r["node_runtime_bindings"]["ACT"]
    assert a["entrypoint"]=="supabase/functions/nayanet-verified-ai-action/index.ts"
    assert a["consumes"]=="nayanet_execution_receipts.action=law_authority_decision"
    assert a["writes"].startswith("nayanet_execution_receipts.")
    src=(ROOT/a["entrypoint"]).read_text()
    assert "nayanet_authority_grants" in src
    assert "nayanet_execution_receipts" in src
    assert "create table" not in src.lower()

def test_act_door_operation_is_exact_and_law_gated():
    j=json.loads((ROOT/"BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json").read_text())
    ai=next(d for d in j["doors"] if d["door_id"]=="DOOR-AI")
    op=next(o for o in ai["operations"] if o["operation"]=="apply_retained_intelligence")
    assert op["authority_action"]=="naya_node_apply"
    assert op["target"]=="NAYA-NODE-0001"
    assert op["verification_required"] is True

def test_act_hands_observation_to_verify_but_does_not_self_verify():
    r=json.loads((ROOT/"BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text())
    src=(ROOT/r["node_runtime_bindings"]["ACT"]["entrypoint"]).read_text()
    compact=src.replace(" ","").lower()
    assert 'verification_method:"pending_independent_runtime_verification"' in compact
    assert "verified:true" not in compact
    assert "learning_evidence" not in src
