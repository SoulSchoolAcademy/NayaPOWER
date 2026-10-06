import copy
import json
import pytest
from tools.live_intelligence_reconcile import (
    DRIFT, assess, canonical_hash, supersede_request, validate_supersede, verify_supersession
)

LESSON = json.dumps({"essence":"current","machine_view":{"automatic_truth_ceiling":"CANDIDATE"}}, sort_keys=True, separators=(",",":"))
OLD = json.dumps({"essence":"old"}, sort_keys=True, separators=(",",":"))

def base_verify(lesson=LESSON):
    block={"block_id":"11111111-1111-1111-1111-111111111111","intelligent_block_id":"IB-000111","content":{"lesson":lesson},"status":"ACTIVE","owner_scope":"PRIVATE","block_type":"GOVERNED_INTELLIGENCE","superseded_by_block_id":None}
    event={"id":"e"}; lineage={"id":"l"}; relationship={"relationship_id":"r"}; index={"id":"i"}; checkpoint={"id":"c"}
    receipt={"id":"x","action":"intelligence_commit","evidence":{"event_row_id":"e","intelligent_block_id":"IB-000111","lineage_id":"l","relationship_id":"r","index_id":"i","checkpoint_id":"c"}}
    checks={"event_present":True,"block_present":True,"lineage_present":True,"relationship_present":True,"index_present":True,"checkpoint_present":True,"receipt_present":True,"event_to_block":True,"block_lineage":True,"block_relationship":True,"block_index":True,"checkpoint_links_lineage":False,"checkpoint_links_relationship":False,"checkpoint_links_index":False,"checkpoint_links_block":False,"checkpoint_links_receipt":False,"receipt_is_intelligence_commit":True}
    return {"independent_verification":True,"checks":checks,"persisted":{"event":event,"block":block,"lineage":lineage,"relationship":relationship,"index":index,"checkpoint":checkpoint,"receipt":receipt}}

def expected():
    return {"expected_content":LESSON,"content_hash":canonical_hash(LESSON),"resolved_connections":[]}

def test_registry_hit_with_exact_runtime_content_is_reusable():
    got=assess(expected(),base_verify(),False)
    assert got["status"]=="REUSE_VERIFIED"
    assert got["action"]=="REUSE"

def test_registry_hit_with_stale_runtime_content_fails_closed_in_verify_only():
    got=assess(expected(),base_verify(OLD),True)
    assert got["status"]==DRIFT
    assert got["action"]=="FAIL_CLOSED"

def test_registry_hit_with_stale_runtime_content_routes_to_supersession_on_write():
    old=base_verify(OLD)
    got=assess(expected(),old,False)
    assert got["action"]=="SUPERSEDE"
    capture={"title":"T","topic":"GOVERNANCE","category":"SYSTEM_INTELLIGENCE"}
    req=supersede_request(capture,expected(),old,"grant")
    assert req["mode"]=="supersede"
    assert req["p_superseded_block_id"]==old["persisted"]["block"]["block_id"]
    assert req["p_content"]==LESSON

def test_supersession_preserves_old_lineage_and_requires_exact_new_content():
    old=base_verify(OLD)
    response={"ok":True,"status":"SUPERSEDED","result":{"block_id":"22222222-2222-2222-2222-222222222222","intelligent_block_id":"IB-000222","supersedes_block_id":old["persisted"]["block"]["block_id"],"content":{"lesson":LESSON}}}
    marker=validate_supersede(expected(),old,response)
    assert marker["prior_lineage_preserved"] is True
    new=copy.deepcopy(response["result"]); new["status"]="ACTIVE"; new["superseded_by_block_id"]=None; new["owner_scope"]="PRIVATE"
    old["persisted"]["block"]["status"]="SUPERSEDED"; old["persisted"]["block"]["superseded_by_block_id"]=new["block_id"]
    envelope=verify_supersession(expected(),old,{"ok":True,"status":"BLOCK_VERIFIED","persisted":{"block":new}},marker)
    assert envelope["independent_verification"] is True
    assert envelope["persisted"]["block"]["intelligent_block_id"]=="IB-000222"
    assert envelope["supersession_proof"]["prior_lineage"]["receipt_id"]=="x"

def test_bad_supersession_content_is_rejected():
    old=base_verify(OLD)
    response={"ok":True,"status":"SUPERSEDED","result":{"block_id":"22222222-2222-2222-2222-222222222222","intelligent_block_id":"IB-000222","supersedes_block_id":old["persisted"]["block"]["block_id"],"content":{"lesson":OLD}}}
    with pytest.raises(ValueError, match="SUPERSESSION_CONTENT_MISMATCH"):
        validate_supersede(expected(),old,response)
