#!/usr/bin/env python3
"""Failing-before/fixed-after proof for canonical Smart Note receiver enforcement."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

def load_module(name: str, source: str):
    path = ROOT / f".naya/runtime/{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_before_main_bypasses_receiver():
    old_source = subprocess.check_output(
        ["git", "show", "origin/main:.naya/runtime/smart_note_calendar.py"],
        text=True,
    )
    with tempfile.TemporaryDirectory() as raw:
        old_path = Path(raw) / "old_calendar.py"
        old_path.write_text(old_source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("old_calendar", old_path)
        assert spec and spec.loader
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        body = "\n".join(f"## {h}" for h in old.REQUIRED_HEADINGS)
        result = old.persist_smart_note(
            timestamp="2026-09-25T18:00:00+00:00",
            topic="Before Enforcement",
            body=body,
            intelligent_block_id="IB-000002",
            root=Path(raw) / "smart-notes",
        )
        assert Path(result["path"]).is_file()
        print("BEFORE_MAIN=FAIL (direct intelligent_block_id bypass persisted)")

def test_after_requires_receiver_receipt():
    current = load_module("smart_note_calendar", "")
    body = "\n".join(f"## {h}" for h in current.REQUIRED_HEADINGS)
    with tempfile.TemporaryDirectory() as raw:
        try:
            current.persist_smart_note(
                timestamp="2026-09-25T18:00:00+00:00",
                topic="After Enforcement",
                body=body,
                receiver_receipt={},
                root=Path(raw) / "smart-notes",
            )
        except ValueError as exc:
            assert str(exc) == "CANONICAL_RECEIVER_RECEIPT_INVALID"
        else:
            raise AssertionError("fixed writer accepted a missing receiver receipt")
        print("AFTER_BRANCH=PASS (missing receiver receipt rejected before persistence)")

def test_after_accepts_only_completed_receiver_receipt():
    current = load_module("smart_note_calendar", "")
    body = "\n".join(f"## {h}" for h in current.REQUIRED_HEADINGS)
    receipt = {
        "canonical_receiver": "v7-smart-note-canonical",
        "status": "completed",
        "intelligent_block_id": "IB-NEW001",
        "event_id": "EV-NEW001",
        "transaction_id": "TX-NEW001",
    }
    with tempfile.TemporaryDirectory() as raw:
        result = current.persist_smart_note(
            timestamp="2026-09-25T18:00:00+00:00",
            topic="After Enforcement",
            body=body,
            receiver_receipt=receipt,
            root=Path(raw) / "smart-notes",
        )
        assert result["intelligent_block_id"] == "IB-NEW001"
        assert result["source_event_id"] == "EV-NEW001"
        assert Path(result["path"]).is_file()
        print("AFTER_BRANCH=PASS (receiver-issued identity + lineage projected canonically)")

if __name__ == "__main__":
    test_before_main_bypasses_receiver()
    test_after_requires_receiver_receipt()
    test_after_accepts_only_completed_receiver_receipt()
    print("SMART_NOTE_RECEIVER_ENFORCEMENT=PASS")
