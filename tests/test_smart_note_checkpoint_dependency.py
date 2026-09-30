from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIVER = ROOT / "supabase" / "functions" / "v7-smart-note-canonical" / "index.ts"


def _source() -> str:
    return RECEIVER.read_text(encoding="utf-8-sig")


def test_canonical_receiver_has_no_missing_compound_intelligence_edge_dependency():
    source = _source()
    assert '/functions/v1/nayanet-compound-intelligence' not in source
    assert '.rpc("nayanet_record_cognition_event"' in source


def test_checkpoint_preserves_source_identity_evidence_and_receipt_boundary():
    source = _source()
    assert 'const checkpointId="smart-note-checkpoint:"+eventId' in source
    assert 'CHECKPOINT_SOURCE_EVENT_NOT_FOUND' in source
    assert '{kind:"smart_note_receipt",receipt_id:persistedReceiptId}' in source
    assert '{kind:"source_event",event_id:eventId}' in source
    assert '{kind:"intelligent_block_hash",sha256:persistedBlockHash}' in source
    assert '{kind:"learning_evidence",evidence_id:learning.id}' in source
    assert 'status:"CHECKPOINT_VERIFIED"' in source
    assert 'checkpointRecord?.receipt?.id' in source


def test_checkpoint_does_not_claim_learning_proof():
    source = _source()
    assert "Checkpoint persistence does not by itself prove learning" in source
    assert "Future applicability, behavior change, and outcome verification remain open." in source
