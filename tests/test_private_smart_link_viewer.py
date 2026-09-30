from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "supabase/functions/nayanet-smart-note-viewer/index.ts").read_text()

def test_private_smart_link_requires_real_user_before_data():
    assert "client.auth.getUser(token)" in SOURCE
    assert "block.owner_id !== user.id" in SOURCE
    assert "SMART_NOTE_FORBIDDEN" in SOURCE

def test_private_smart_link_has_no_token_in_url_contract():
    assert "access_token=" not in SOURCE
    assert "refresh_token=" not in SOURCE
    assert "Authorization:'Bearer '+s.access_token" in SOURCE

def test_private_smart_link_reads_canonical_block_and_registry():
    assert '.from("nayanet_intelligent_blocks")' in SOURCE
    assert ".naya/memory/smart-notes/index.json" in SOURCE
    assert "canonical_path" in SOURCE
    assert 'JSON.parse(block.content?.lesson' in SOURCE

def test_private_smart_link_preserves_truth_and_scope():
    assert "understanding_state" in SOURCE
    assert "owner_scope" in SOURCE
    assert "truth_state: block.understanding_state" in SOURCE
    assert "scope: block.owner_scope" in SOURCE

def test_private_smart_link_is_read_only():
    lowered = SOURCE.lower()
    assert ".insert(" not in lowered
    assert ".update(" not in lowered
    assert ".upsert(" not in lowered
    assert ".delete(" not in lowered
