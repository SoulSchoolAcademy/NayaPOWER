import json
import os
import uuid
import urllib.error
import urllib.request


URL = os.environ.get("SUPABASE_URL", "https://dahisasgpfvziswqvmvm.supabase.co").rstrip("/")
TOKEN = os.environ.get("SUPABASE_USER_ACCESS_TOKEN", "")
KEY = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")
GRANT = os.environ.get("NAYANET_INTELLIGENCE_COMMIT_GRANT_ID", "")


def request(path, method="GET", payload=None, token=TOKEN):
    headers = {"apikey": KEY, "Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(URL + path, headers=headers, method=method,
                                 data=json.dumps(payload).encode() if payload is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def test_fresh_lesson_intelligence_commit_persists_connected_checkpoint():
    if not TOKEN or not KEY or not GRANT:
        import pytest
        pytest.skip("protected owner session and intelligence_commit grant are required")

    status, user = request("/auth/v1/user")
    assert status == 200 and user.get("id"), (status, user)

    lesson_key = "FRESH-LESSON-" + uuid.uuid4().hex
    payload = {
        "p_event_id": lesson_key,
        "p_title": "Fresh canonical lesson",
        "p_content": "A meaningful lesson for proving durable connected intelligence.",
        "p_category": "COLLECTIVE_INTELLIGENCE",
        "p_topic": "COMPOUNDING_INTELLIGENCE",
        "p_target_id": "NAYA-NODE-0001",
        "p_authority_grant_id": GRANT,
        "p_project_id": "NayaNET",
    }
    status, result = request("/rest/v1/rpc/nayanet_intelligence_commit", "POST", payload)
    assert status == 200 and result.get("ok") is True, (status, result)

    event_id = result["event_id"]
    block_id = result["intelligent_block_id"]
    lineage_id = result["lineage_id"]
    relationship_id = result["relationship_id"]
    checkpoint_id = result["checkpoint_id"]
    receipt_id = result["receipt_id"]

    status, events = request(f"/rest/v1/nayanet_cognition_events?id=eq.{event_id}&user_id=eq.{user['id']}&select=*")
    assert status == 200 and len(events) == 1
    status, blocks = request(f"/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq.{block_id}&owner_id=eq.{user['id']}&select=*")
    assert status == 200 and len(blocks) == 1
    status, lineage = request(f"/rest/v1/nayanet_intelligence_lineage?id=eq.{lineage_id}&user_id=eq.{user['id']}&select=*")
    assert status == 200 and len(lineage) == 1
    status, rels = request(f"/rest/v1/nayanet_brain_relationships?relationship_id=eq.{relationship_id}&owner_id=eq.{user['id']}&select=*")
    assert status == 200 and len(rels) == 1
    status, state = request(f"/rest/v1/nayanet_project_cognition_state?id=eq.{checkpoint_id}&user_id=eq.{user['id']}&select=*")
    assert status == 200 and len(state) == 1
    status, receipts = request(f"/rest/v1/nayanet_execution_receipts?id=eq.{receipt_id}&user_id=eq.{user['id']}&select=*")
    assert status == 200 and len(receipts) == 1

    assert blocks[0]["source_event_ids"] == [event_id]
    assert lineage[0]["source_event_id"] == event_id
    assert lineage[0]["target_event_id"] == blocks[0]["block_id"]
    assert rels[0]["target_id"] == block_id
    assert state[0]["state"]["intelligent_block_id"] == block_id
    assert state[0]["state"]["lineage_id"] == lineage_id
    assert state[0]["state"]["relationship_id"] == relationship_id
    assert state[0]["state"]["receipt_id"] == receipt_id
    assert receipts[0]["action"] == "intelligence_commit"
