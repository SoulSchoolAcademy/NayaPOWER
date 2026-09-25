#!/usr/bin/env python3
"""Compatibility-only canonical Smart Note projection resolver.

The live `v7-smart-note-canonical` receiver is the sole Smart Note creation and
IB identity-allocation authority. This module remains only because existing
repository contracts reference its canonical physical-path resolver.

It MUST NOT allocate IB identities, persist a Smart Note, create a Note Event,
or run a competing CIS/PIS/Hub lifecycle. Any local creation attempt fails
closed so future code cannot silently reintroduce a second creation system.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMART_NOTES_ROOT = ROOT / ".naya" / "memory" / "smart-notes"
IB_ID_RE = re.compile(r"^IB-d{6}$")


def slug(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").upper()
    return token[:100] or "SMART-NOTE"


def canonical_smart_note_path(
    timestamp: str,
    topic: str,
    category: str = "system",
    ib_id: str = "IB-000000",
    root: Path | None = None,
) -> Path:
    """Resolve the ratified Smart Note V1 logical→physical namespace.

    The IB ID must already have been returned by the canonical receiver.
    This function resolves placement only; it never allocates identity.
    """
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)
    category_slug = slug(category).lower()
    topic_slug = "-".join(slug(topic).lower().split("-")[:3]) or "smart-note"
    if not IB_ID_RE.fullmatch(ib_id):
        raise ValueError("canonical Smart Note requires receiver-issued immutable IB-XXXXXX identity")
    base = Path(root) if root is not None else SMART_NOTES_ROOT
    return base / f"{dt:%Y}" / f"{dt:%m}" / f"{dt:%d}" / category_slug / topic_slug / ib_id / "smart-note.md"


def execute(note: dict) -> None:
    """Fail closed: local Smart Note creation is no longer an allowed path."""
    raise RuntimeError(
        "LOCAL_SMART_NOTE_CREATION_DISABLED: use v7-smart-note-canonical; "
        "the live receiver allocates the canonical IB identity and owns creation."
    )


__all__ = ["canonical_smart_note_path", "execute", "SMART_NOTES_ROOT"]
