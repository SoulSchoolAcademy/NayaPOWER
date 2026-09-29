import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def test_know_runtime_binds_law_receipt_input_and_source_is_syntactically_clean():
    src=(ROOT/"supabase/functions/nayanet-know-runtime/index.ts").read_text(encoding="utf-8")
    model=(ROOT/"supabase/functions/nayanet-know-runtime/know.ts").read_text(encoding="utf-8")
    assert "law_receipt_id:body.law_receipt_id" in src
    assert "law_receipt_id?: string;" in model
    assert "request.law_receipt_id" in src
    assert "},\\n          authorization," not in src


def test_know_registry_stays_source_only_until_live_proof():
    registry=json.loads((ROOT/"BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text(encoding="utf-8"))
    know=registry["node_runtime_bindings"]["KNOW"]
    assert know["status"]=="IMPLEMENTED_SOURCE_PENDING_LIVE_PROOF"
    assert know["proof"]=="PENDING_LIVE_PROOF"
    assert know["authority_law"]=="retrieval_grants_authority=false"
    assert know["handoff_to"]=="NAYA-KERNEL-PROVE"


def test_know_object_does_not_overclaim_runtime_or_production():
    obj=json.loads((ROOT/"BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-KNOW.json").read_text(encoding="utf-8"))
    assert obj["canonical_status"]=="CANDIDATE"
    assert obj["proof"]["implementation_status"]=="EXECUTABLE_SOURCE"
    assert obj["proof"]["production_status"]=="NOT_PROVEN"
    assert "PENDING" in obj["proof"]["behavioral_status"]
