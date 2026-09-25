from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".naya" / "codex" / "CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md"
TX = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
CAL = ROOT / ".naya" / "runtime" / "smart_note_calendar.py"
RECEIVER = ROOT / "supabase" / "functions" / "v7-smart-note-canonical" / "index.ts"
RUNTIME = ROOT / "NAYANET" / "HUB" / "public" / "assistant-runtime.js"
SURFACE = ROOT / "NAYANET" / "HUB" / "src" / "app" / "SmartNoteSurface.tsx"

CANONICAL_HEADINGS = [
    "IN A NUTSHELL", "DATE / TIME", "WHAT", "WHY IT MATTERS", "HUMAN",
    "CHILD", "GRANDMA", "NAYA", "MACHINE", "WHAT WE LEARNED", "CONNECTIONS",
    "HOW TO APPLY", "WHAT IT ULTIMATELY MEANS", "WHAT'S IN IT FOR YOU / US", "NEXT ACTION",
]


def test_one_canonical_contract_declares_one_smart_note_ib_object():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Smart Note" in text and "Intelligent Block (IB)" in text
    assert "Intelligent Block" in text and "V1" in text
    assert "## 4. CANONICAL HUMAN STRUCTURE" in text
    positions = [text.index(f"{i}. {heading}") for i, heading in enumerate(CANONICAL_HEADINGS, start=1)]
    assert positions == sorted(positions)
    assert ".naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md" in text


def test_local_runtime_is_projection_compatibility_only():
    text = TX.read_text(encoding="utf-8")
    assert "LOCAL_SMART_NOTE_CREATION_DISABLED" in text
    assert "v7-smart-note-canonical" in text
    assert "def _allocate_ib_id" not in text
    assert "identity_cursor" not in text


def test_calendar_writer_uses_receiver_issued_identity_resolver():
    text = CAL.read_text(encoding="utf-8")
    assert "canonical_smart_note_path" in text
    assert "intelligent_block_id" in text


def test_live_receiver_and_hub_surface_carry_canonical_block():
    receiver = RECEIVER.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")
    surface = SURFACE.read_text(encoding="utf-8")
    assert "NAYANET_INTELLIGENT_BLOCK_V1" in receiver
    assert "v7_create_smart_note" in receiver
    assert "intelligent_block_id" in receiver
    assert "child_note" in runtime and "grandma_note" in runtime
    assert "how_to_apply" in runtime and "how_it_connects" in runtime
    assert "SMART_NOTE_CANONICAL_BLOCK_INCOMPLETE" in surface
