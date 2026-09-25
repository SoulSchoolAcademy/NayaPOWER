from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".naya" / "SMART-NOTE-CONTRACT-V1.md"
TX = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
CAL = ROOT / ".naya" / "runtime" / "smart_note_calendar.py"
RECEIVER = ROOT / "supabase" / "functions" / "v7-smart-note-canonical" / "index.ts"
RUNTIME = ROOT / "NAYANET" / "HUB" / "public" / "assistant-runtime.js"
SURFACE = ROOT / "NAYANET" / "HUB" / "src" / "app" / "SmartNoteSurface.tsx"

CANONICAL_HEADINGS = [
    "IN A NUTSHELL",
    "HUMAN NOTE",
    "CHILD NOTE",
    "GRANDMA NOTE",
    "NAYA NOTE",
    "MACHINE NOTE",
    "LEARNING LESSON",
    "WHAT IT MEANS",
    "HOW IT CONNECTS",
    "HOW TO APPLY IT",
    "WHAT'S IN IT FOR THEM / YOU / US",
    "EVIDENCE / SMART LINKS",
    "CURRENT STATE",
    "ONE NEXT ACTION",
]


def test_one_canonical_contract_declares_smart_note_equals_intelligent_block():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "SMART NOTE = INTELLIGENT BLOCK." in text
    assert "NAYANET_INTELLIGENT_BLOCK_V1" in text
    positions = [text.index("## " + heading) for heading in CANONICAL_HEADINGS]
    assert positions == sorted(positions)
    assert "NayaPOWER/SMART-NOTES/YYYY/MM/DD/" in text
    assert ".naya/memory/notes/YYYY/MM/DD/" in text


def test_runtime_writer_uses_only_canonical_perspectives_and_schema():
    text = TX.read_text(encoding="utf-8")
    assert '.naya" / "memory" / "notes"' in text
    assert "CANONICAL_SCHEMA = \"NAYANET_INTELLIGENT_BLOCK_V1\"" in text
    for heading in CANONICAL_HEADINGS:
        assert "## " + heading in text


def test_calendar_writer_matches_the_same_human_contract():
    text = CAL.read_text(encoding="utf-8")
    for heading in CANONICAL_HEADINGS:
        assert '\"' + heading + '\"' in text


def test_live_receiver_and_hub_surface_carry_canonical_block():
    receiver = RECEIVER.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")
    surface = SURFACE.read_text(encoding="utf-8")
    assert "NAYANET_INTELLIGENT_BLOCK_V1" in receiver
    assert "perspectives" in receiver
    for field in ("childText", "grandmaText", "learningText", "meaningText", "connectsText", "applyText", "valueText"):
        assert field in receiver
    assert "child_note" in runtime and "grandma_note" in runtime
    assert "how_to_apply" in runtime and "how_it_connects" in runtime
    assert "SMART_NOTE_CANONICAL_BLOCK_INCOMPLETE" in surface


def test_legacy_smart_notes_are_explicitly_not_current_write_targets():
    text = CONTRACT.read_text(encoding="utf-8")
    for path in (
        ".naya/SUPERBRAIN/SMART-NOTES/",
        ".naya/memory/smart-notes/",
        ".naya/project-intelligence/smart-notes/",
        "SUPERBRAIN/SMART-NOTES/",
    ):
        assert path in text
