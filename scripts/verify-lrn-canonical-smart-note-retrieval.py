#!/usr/bin/env python3
"""Focused proof for the existing LRN -> canonical Smart Note retrieval adapter."""
from __future__ import annotations
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMART_NOTE_ID = "SN-20260917T200000+0000-IH-03-CANONICAL-INTELLIGENCE-IDENTITY"

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load " + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> None:
    adapter = load(ROOT / "tools/retrieve_learning.py", "retrieve_learning_adapter")
    tx = load(ROOT / ".naya/runtime/smart_note_transaction.py", "smart_note_transaction")
    with tempfile.TemporaryDirectory(prefix="naya-lrn-retrieval-") as raw:
        temp = Path(raw)
        note_dir = temp / ".naya" / "memory" / "notes"
        timestamp = "2026-09-17T20:00:00+00:00"
        topic = "IH-03 Canonical Intelligence Identity"
        canonical_path = tx.canonical_smart_note_path(timestamp, topic, root=note_dir)
        canonical_path.parent.mkdir(parents=True, exist_ok=True)
        canonical_path.write_text(
            "# SMART NOTE — " + topic + "\n\n"
            + "**Timestamp:** " + timestamp + "\n"
            + "**Smart Note ID:** `" + SMART_NOTE_ID + "`\n"
            + "**Status:** CANONICAL / TRANSACTIONALLY PROJECTED\n\n"
            + "## Learning Lesson / Adaptive Learning\n\n"
            + "Projection must preserve lineage rather than manufacture a new intelligence identity.\n\n"
            + "## Evidence / Smart Links\n\n- IH-03 canonical identity proof\n",
            encoding="utf-8",
        )
        learning_dir = temp / "MASTER-NOTES" / "ADAPTIVE-LEARNING"
        learning_dir.mkdir(parents=True, exist_ok=True)
        learning_id = "LRN-IH03-CANONICAL-IDENTITY"
        learning = {
            "learning_event_id": learning_id,
            "timestamp": timestamp,
            "source_event_id": SMART_NOTE_ID,
            "smart_note_id": SMART_NOTE_ID,
            "lesson": "Projection must preserve lineage rather than manufacture a new intelligence identity.",
            "evidence_state": "VERIFIED",
            "learning_state": "CONFIRMED",
        }
        (learning_dir / (learning_id + ".json")).write_text(json.dumps(learning, indent=2) + "\n", encoding="utf-8")
        result = adapter.retrieve_learning_event(learning_id, learning_dir=learning_dir, note_dir=note_dir)
        receipt = result["receipt"]
        note = result["note"]
        assert receipt["status"] == "RETRIEVED"
        assert receipt["learning_event_id"] == learning_id
        assert receipt["source_event_id"] == SMART_NOTE_ID
        assert receipt["smart_note_id"] == SMART_NOTE_ID
        assert receipt["retrieved_note_event_id"] == SMART_NOTE_ID
        assert note["id"] == SMART_NOTE_ID
        assert note["canonical_path"].endswith(".naya/memory/notes/2026/09/17/SN-20260917-IH-03-CANONICAL-INTELLIGENCE-IDENTITY.md")
        assert canonical_path.exists()
        print("LRN_SMART_NOTE_BINDING=PASS")
        print("CANONICAL_RESOLVER=PASS")
        print("RETRIEVAL_RECEIPT=PASS")
        print("SMART_NOTE_ID=" + SMART_NOTE_ID)
        print("LRN_ID=" + learning_id)
        print("LRN_CANONICAL_RETRIEVAL=PASS")

if __name__ == "__main__":
    main()
