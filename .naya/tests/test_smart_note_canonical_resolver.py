#!/usr/bin/env python3
"""Regression proof for the canonical Smart Note logical→physical resolver."""

from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import tempfile


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"

spec = importlib.util.spec_from_file_location("smart_note_transaction", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_canonical_smart_note_path():
    timestamp = "2026-09-19T20:30:00+00:00"
    path = module.canonical_smart_note_path(timestamp, "Day Wisdom", category="system", ib_id="IB-000002")
    assert path == (
        ROOT
        / ".naya"
        / "memory"
        / "smart-notes"
        / "2026"
        / "09"
        / "19"
        / "system"
        / "day-wisdom"
        / "IB-000002"
        / "smart-note.md"
    )


def test_resolver_has_one_physical_namespace():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert 'ROOT / ".naya" / "memory" / "smart-notes"' in source
    assert 'ROOT / "SUPERBRAIN" / "SMART-NOTES"' not in source


def test_calendar_writer_uses_same_resolver():
    calendar_path = ROOT / ".naya" / "runtime" / "smart_note_calendar.py"
    calendar_spec = importlib.util.spec_from_file_location("smart_note_calendar", calendar_path)
    assert calendar_spec is not None and calendar_spec.loader is not None
    calendar = importlib.util.module_from_spec(calendar_spec)
    calendar_spec.loader.exec_module(calendar)

    body = "\n".join(
        [
            "## IN A NUTSHELL",
            "## DATE / TIME",
            "## WHAT",
            "## WHY IT MATTERS",
            "## HUMAN",
            "## CHILD",
            "## GRANDMA",
            "## NAYA",
            "## MACHINE",
            "## WHAT WE LEARNED",
            "## CONNECTIONS",
            "## HOW TO APPLY",
            "## WHAT IT ULTIMATELY MEANS",
            "## WHAT'S IN IT FOR YOU / US",
            "## NEXT ACTION",
        ]
    )
    with tempfile.TemporaryDirectory() as raw:
        result = calendar.persist_smart_note(
            timestamp="2026-09-19T20:30:00+00:00",
            topic="Day Wisdom",
            body=body,
            intelligent_block_id="IB-000002",
            category="system",
            root=Path(raw) / "smart-notes",
        )
        assert result["path"] == str(
            Path(raw) / "smart-notes" / "2026" / "09" / "19" / "system" / "day-wisdom" / "IB-000002" / "smart-note.md"
        )



def test_transaction_rejects_missing_receiver_assigned_ib_before_persistence():
    note = {
        "topic": "Receiver Identity Boundary",
        "timestamp": "2026-09-25T18:00:00+00:00",
        "in_a_nutshell": "test",
        "human": "test",
        "child": "test",
        "grandma": "test",
        "naya": "test",
        "machine": "test",
        "learning": "test",
        "why_it_matters": "test",
        "how_it_connects": "test",
        "how_to_use": "test",
        "value": "test",
        "evidence": ["test"],
        "current_state": "test",
        "next_action": "test",
    }
    try:
        module.execute(note)
    except ValueError as exc:
        assert str(exc) == "live canonical receiver must supply intelligent_block_id"
    else:
        raise AssertionError("transaction accepted missing receiver-assigned IB identity")


def test_transaction_cannot_allocate_ib_identity_locally():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "_allocate_ib_id" not in source
    assert "live canonical receiver" in source.lower()

if __name__ == "__main__":
    test_canonical_smart_note_path()
    test_resolver_has_one_physical_namespace()
    print("PASS — Smart Note canonical resolver")
