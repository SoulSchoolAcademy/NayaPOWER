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
    path = module.canonical_smart_note_path(timestamp, "Day Wisdom")
    assert path == (
        ROOT
        / ".naya"
        / "memory"
        / "notes"
        / "2026"
        / "09"
        / "19"
        / "SN-20260919-DAY-WISDOM.md"
    )


def test_resolver_has_one_physical_namespace():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert 'ROOT / ".naya" / "memory" / "notes"' in source
    assert 'ROOT / "SUPERBRAIN" / "SMART-NOTES"' not in source


def test_calendar_writer_uses_same_resolver():
    calendar_path = ROOT / ".naya" / "runtime" / "smart_note_calendar.py"
    calendar_spec = importlib.util.spec_from_file_location("smart_note_calendar", calendar_path)
    assert calendar_spec is not None and calendar_spec.loader is not None
    calendar = importlib.util.module_from_spec(calendar_spec)
    calendar_spec.loader.exec_module(calendar)

    body = "\n".join(
        [
            "## Parent / predecessor",
            "## Human",
            "## Naya",
            "## Machine",
            "## Child / derived",
            "## What happened",
            "## What learned",
            "## Why this matters",
            "## How to use",
            "## What's in it for us",
            "## Evidence / Smart Links",
            "## Current state",
            "## ONE NEXT ACTION",
        ]
    )
    with tempfile.TemporaryDirectory() as raw:
        result = calendar.persist_smart_note(
            timestamp="2026-09-19T20:30:00+00:00",
            topic="Day Wisdom",
            body=body,
            root=Path(raw) / "notes",
        )
        assert result["path"] == str(
            Path(raw) / "notes" / "2026" / "09" / "19" / "SN-20260919-DAY-WISDOM.md"
        )


if __name__ == "__main__":
    test_canonical_smart_note_path()
    test_resolver_has_one_physical_namespace()
    print("PASS — Smart Note canonical resolver")
