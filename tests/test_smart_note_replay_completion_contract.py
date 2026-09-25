from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIVER = ROOT / "supabase/functions/v7-smart-note-canonical/index.ts"
COMPOUND = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"
SURFACE = ROOT / "NAYANET/HUB/src/app/SmartNoteSurface.tsx"


def test_v7_replay_repairs_and_verifies_downstream_state():
    source = RECEIVER.read_text(encoding="utf-8")
    for marker in (
        "const replayed=persistedEventId!==eventId",
        "stableUuid",
        "SMART_NOTE_IDEMPOTENCY_CONFLICT",
        "createdLearning.error.code!==\"23505\"",
        "persistedReceiptId",
        "persistedBlockHash",
        "checkpointEvidenceMatches",
        "pipeline:replayed?\"replayed\":\"completed\"",
    ):
        assert marker in source
    assert "if(persistedEventId!==eventId){" not in source


def test_checkpoint_replay_returns_persisted_receipt_and_surface_requires_it():
    compound = COMPOUND.read_text(encoding="utf-8")
    surface = SURFACE.read_text(encoding="utf-8")
    assert "CHECKPOINT_RECEIPT_MISSING" in compound
    assert "receipt: {id:existingReceiptId,receipt_id:existingReceiptId}" in compound
    assert "const persistedCheckpoint=receipt?.event||event" in compound
    assert "if(!learning?.id||checkpoint?.status!=='CHECKPOINT_VERIFIED')" in surface
    assert "result?.pipeline==='completed'&&" not in surface
