#!/usr/bin/env python3
"""Canonical human Smart Note calendar writer.

Smart Notes remain a separate human-readable intelligence stream. The writer
owns only their calendar placement and day index; it does not change the
machine event store or NAYA-TEAM semantics.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import sys

RUNTIME_ROOT = Path(__file__).resolve().parent
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from calendar_projection import _utc_parts, safe_topic
from smart_note_transaction import canonical_smart_note_path

ROOT = Path(__file__).resolve().parents[2]
SMART_NOTES_ROOT = ROOT / ".naya" / "memory" / "smart-notes"

REQUIRED_HEADINGS = (
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
)


def validate_smart_note(body: str) -> list[str]:
    return [heading for heading in REQUIRED_HEADINGS if f"## {heading}" not in body]


def persist_smart_note(
    *,
    timestamp: str | None,
    topic: str,
    body: str,
    intelligent_block_id: str,
    category: str = "system",
    root: Path | None = None,
) -> dict[str, Any]:
    missing = validate_smart_note(body)
    if missing:
        raise ValueError("Smart Note contract missing headings: " + ", ".join(missing))
    stamp = timestamp or datetime.now(timezone.utc).isoformat()
    destination_root = Path(root) if root else SMART_NOTES_ROOT
    path = canonical_smart_note_path(
        stamp,
        topic,
        category=category,
        ib_id=intelligent_block_id,
        root=destination_root,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != body:
            raise ValueError(f"Smart Note projection conflict: {path}")
        status = "REPLAY"
    else:
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
        status = "CREATED"

    day_index = path.parent / "INDEX.md"
    link = path.name
    if day_index.exists():
        index = day_index.read_text(encoding="utf-8")
        if link not in index:
            day_index.write_text(index.rstrip() + f"\n- [{topic}](./{link})\n", encoding="utf-8")
    else:
        dt, _ = _utc_parts(stamp)
        day_index.write_text(f"# Smart Notes — {dt:%Y-%m-%d}\n\n## Records\n\n- [{topic}](./{link})\n", encoding="utf-8")

    return {"status": status, "path": str(path), "timestamp": stamp, "topic": safe_topic(topic)}


__all__ = ["persist_smart_note", "validate_smart_note", "SMART_NOTES_ROOT"]
