"""Read-only source boundary for canonical Intelligent Blocks.

This module does not persist, mutate, or resolve project events. It only
validates and passes through the canonical Intelligent Block shape required by
Claim Currentness V1. The canonical `content.*` fields remain nested exactly
as persisted; no event-shaped translation is performed.
"""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Iterable

REQUIRED_TOP_LEVEL = {"block_id", "subject_id", "status", "understanding_state", "content"}


def normalize_intelligent_block(row: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_TOP_LEVEL - set(row)
    if missing:
        raise ValueError(f"INTELLIGENT_BLOCK_SOURCE_INVALID: missing={sorted(missing)}")
    if not isinstance(row.get("content"), dict):
        raise ValueError("INTELLIGENT_BLOCK_SOURCE_INVALID: content must be an object")

    content = row["content"]
    for key in ("truth", "time", "context", "evidence", "provenance"):
        if key in content and content[key] is not None and not isinstance(content[key], dict):
            raise ValueError(f"INTELLIGENT_BLOCK_SOURCE_INVALID: content.{key} must be an object or null")

    # Read-only: return a deep copy of the canonical shape. No persistence,
    # mutation, event conversion, or currentness decision occurs here.
    return deepcopy(row)


def load_intelligent_blocks(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a read-only canonical snapshot; never writes or mutates inputs."""
    return [normalize_intelligent_block(row) for row in rows]
