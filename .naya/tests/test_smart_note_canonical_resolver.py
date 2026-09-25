#!/usr/bin/env python3
"""Regression proof for the canonical Smart Note / Intelligent Block boundary."""
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
spec = importlib.util.spec_from_file_location("smart_note_transaction", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_canonical_smart_note_path():
    path = module.canonical_smart_note_path("2026-09-19T20:30:00+00:00","Day Wisdom",category="system",ib_id="IB-000002")
    assert path == ROOT/".naya/memory/smart-notes/2026/09/19/system/day-wisdom/IB-000002/smart-note.md"

def test_resolver_has_one_physical_namespace():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert 'ROOT / ".naya" / "memory" / "smart-notes"' in source
    assert 'ROOT / "SUPERBRAIN" / "SMART-NOTES"' not in source

def test_calendar_writer_requires_receiver_receipt():
    source = (ROOT/".naya/runtime/smart_note_calendar.py").read_text(encoding="utf-8")
    assert "receiver_receipt" in source
    assert "v7-smart-note-canonical" in source
    assert "intelligent_block_id: str" not in source

def test_calendar_writer_rejects_missing_receiver_before_persistence():
    spec = importlib.util.spec_from_file_location("calendar", ROOT/".naya/runtime/smart_note_calendar.py")
    assert spec and spec.loader
    calendar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(calendar)
    body = "\n".join(f"## {h}" for h in calendar.REQUIRED_HEADINGS)
    with tempfile.TemporaryDirectory() as raw:
        try:
            calendar.persist_smart_note(timestamp="2026-09-25T18:00:00+00:00",topic="Enforcement",body=body,receiver_receipt={},root=Path(raw)/"smart-notes")
        except ValueError as exc:
            assert str(exc) == "CANONICAL_RECEIVER_RECEIPT_INVALID"
        else:
            raise AssertionError("projection bypassed canonical receiver")

def test_calendar_writer_accepts_only_receiver_issued_identity_and_lineage():
    spec = importlib.util.spec_from_file_location("calendar", ROOT/".naya/runtime/smart_note_calendar.py")
    assert spec and spec.loader
    calendar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(calendar)
    body = "\n".join(f"## {h}" for h in calendar.REQUIRED_HEADINGS)
    receipt = {"canonical_receiver":"v7-smart-note-canonical","status":"completed","intelligent_block_id":"IB-000123","event_id":"EV-123","transaction_id":"TX-123"}
    with tempfile.TemporaryDirectory() as raw:
        result = calendar.persist_smart_note(timestamp="2026-09-25T18:00:00+00:00",topic="Enforcement",body=body,receiver_receipt=receipt,root=Path(raw)/"smart-notes")
        assert result["intelligent_block_id"] == "IB-000123"
        assert result["source_event_id"] == "EV-123"
        assert Path(result["path"]).is_file()

if __name__ == "__main__":
    test_canonical_smart_note_path()
    test_resolver_has_one_physical_namespace()
    test_calendar_writer_requires_receiver_receipt()
    test_calendar_writer_rejects_missing_receiver_before_persistence()
    test_calendar_writer_accepts_only_receiver_issued_identity_and_lineage()
    print("PASS — Smart Note canonical enforcement")
