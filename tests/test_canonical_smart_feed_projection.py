import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("smart_feed_projection", ROOT / "scripts/build-smart-feed-projection.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_feed_projection_reads_only_registry_bound_canonical_smart_note():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        note = root / ".naya/memory/smart-notes/2026/09/25/system/example/IB-001025/smart-note.md"
        note.parent.mkdir(parents=True)
        note.write_text(
            "# SMART NOTE — Example\n\n"
            "**Timestamp:** 2026-09-25T22:00:00+00:00\n"
            "## IN A NUTSHELL\n\nA canonical lesson.\n"
            "## NAYA NOTE\n\nPreserve it.\n"
            "## LEARNING LESSON / ADAPTIVE LEARNING\n\nUse it later.\n"
            "## WHY IT MATTERS\n\nContinuity.\n"
            "## ONE NEXT ACTION\n\nRetrieve it.\n",
            encoding="utf-8",
        )
        registry = note.parents[4] / "REGISTRY.json"
        registry.write_text(json.dumps({
            "$schema": "naya/smart-note-registry/v1",
            "status": "CANONICAL",
            "entries": [{
                "intelligent_block_id": "IB-001025",
                "path": ".naya/memory/smart-notes/2026/09/25/system/example/IB-001025/smart-note.md",
                "source_event_id": "EV-001025"
            }]
        }), encoding="utf-8")
        events = MODULE.canonical_note_events(root / ".naya/memory/smart-notes", root)
        assert len(events) == 1
        assert events[0]["event_id"] == "EV-001025"
        assert events[0]["context"]["intelligent_block_id"] == "IB-001025"
        assert events[0]["lesson"]["text"] == "Use it later."
