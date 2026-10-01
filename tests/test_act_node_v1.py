import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_act_is_registered_without_parallel_authority_or_receipt_store():
    r=json.loads((ROOT/"BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text(encoding="utf-8"))
    a=r["node_runtime_bindings"]["ACT"]
    assert a["entrypoint"]=="supabase/functions/nayanet-act-runtime/index.ts"
    assert a["consumes"]=="nayanet_execution_receipts.action=law_authority_decision"
    assert a["writes"].startswith("nayanet_execution_receipts.")
    src=(ROOT/"supabase/functions/nayanet-act-runtime/index.ts").read_text(encoding="utf-8")
    assert "nayanet_authority_grants" in src
    assert "nayanet_execution_receipts" in src
    assert "create table" not in src.lower()

def test_act_door_operation_is_exact_and_law_gated():
    j=json.loads((ROOT/"BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json").read_text(encoding="utf-8"))
    ai=next(d for d in j["doors"] if d["door_id"]=="DOOR-AI")
    op=next(o for o in ai["operations"] if o["operation"]=="apply_retained_intelligence")
    assert op["authority_action"]=="naya_node_apply"
    assert op["target"]=="NAYA-NODE-0001"
    assert op["verification_required"] is True

def test_act_hands_observation_to_verify_but_does_not_self_verify():
    src=(ROOT/"supabase/functions/nayanet-act-runtime/index.ts").read_text(encoding="utf-8")
    assert 'handoff_to:"NAYA-KERNEL-VERIFY"' in src
    assert "verified:true" not in src.replace(" ","").lower()
    assert "learning_evidence" not in src
