#!/usr/bin/env python3
"""Thin LRN -> existing Smart Notes retrieval adapter.

This does not create a second memory store. Learning Events remain durable
learning records; the existing Smart Notes memory runtime remains the retrieval
authority. The adapter resolves LRN -> SN and emits an explicit retrieval receipt.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEARNING_DIR = ROOT / "MASTER-NOTES" / "ADAPTIVE-LEARNING"
RECEIPT_DIR = LEARNING_DIR / "RETRIEVAL-RECEIPTS"
MEMORY_DIR = ROOT / ".naya" / "memory"

sys.path.insert(0, str(MEMORY_DIR))
import memory_runtime as memory  # noqa: E402


def retrieve_learning_event(
    learning_event_id: str,
    *,
    learning_dir: Path = LEARNING_DIR,
    note_dir: Path = MEMORY_DIR / "notes",
    limit: int = 10,
) -> dict[str, Any]:
    """Resolve one LRN record through the existing Smart Notes retrieval runtime."""
    if not learning_event_id.startswith("LRN-"):
        raise ValueError("learning_event_id must start with LRN-")
    learning_path = learning_dir / f"{learning_event_id}.json"
    if not learning_path.exists():
        raise FileNotFoundError(learning_path)

    learning = json.loads(learning_path.read_text(encoding="utf-8"))
    source_event_id = str(learning.get("source_event_id", ""))
    smart_note_id = str(learning.get("smart_note_id", ""))
    lesson = str(learning.get("lesson", "")).strip()
    if not source_event_id.startswith("SE-"):
        raise ValueError("learning event is missing canonical source_event_id")
    if not smart_note_id.startswith("SN-"):
        raise ValueError("learning event is missing Smart Note identity")
    if not lesson:
        raise ValueError("learning event is missing lesson")

    previous_note_dir = memory.NOTE_DIR
    try:
        memory.NOTE_DIR = note_dir
        candidates = memory.retrieve(lesson, limit)
    finally:
        memory.NOTE_DIR = previous_note_dir

    retrieved = next(
        (note for _, note in candidates if note.get("id") == smart_note_id),
        None,
    )
    if retrieved is None:
        raise LookupError(
            f"learning event {learning_event_id} resolved to {smart_note_id}, "
            "but the existing Smart Notes runtime did not retrieve that note"
        )

    receipt = {
        "retrieval_receipt_id": f"RTR-{learning_event_id[4:]}",
        "status": "RETRIEVED",
        "learning_event_id": learning_event_id,
        "source_event_id": source_event_id,
        "smart_note_id": smart_note_id,
        "retrieved_note_event_id": retrieved.get("event_id", ""),
        "lesson": retrieved.get("what_we_learned", [lesson])[0] if retrieved.get("what_we_learned") else lesson,
        "runtime": ".naya/memory/memory_runtime.py",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "cold_context": True,
    }
    return {"receipt": receipt, "learning": learning, "note": retrieved}


def write_retrieval_receipt(result: dict[str, Any], *, receipt_dir: Path = RECEIPT_DIR) -> Path:
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = result["receipt"]
    path = receipt_dir / f"{receipt['retrieval_receipt_id']}.json"
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: retrieve_learning.py LRN-...")
    result = retrieve_learning_event(sys.argv[1])
    print(json.dumps(result["receipt"], indent=2, ensure_ascii=False))
