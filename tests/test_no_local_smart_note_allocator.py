from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TX = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"


def test_local_smart_note_transaction_cannot_allocate_or_create_canonical_ib():
    source = TX.read_text(encoding="utf-8")
    assert "def _allocate_ib_id" not in source
    assert "identity_cursor" not in source
    assert "next_number = max" not in source
    assert "note[\"intelligent_block_id\"] or _allocate_ib_id()" not in source


def test_local_transaction_is_explicitly_receiver_only_projection_compatibility():
    source = TX.read_text(encoding="utf-8")
    assert "LOCAL_SMART_NOTE_CREATION_DISABLED" in source
    assert "v7-smart-note-canonical" in source
