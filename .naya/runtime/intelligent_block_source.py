"""Read-only source boundary for canonical Intelligent Blocks.

This module does not persist, mutate, or resolve project events. It only
normalizes already-canonical Intelligent Block rows into the minimal input
shape required by the Claim Currentness V1 contract.
"""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Iterable


REQUIRED_TOP_LEVEL = {"block_id", "subject_id", "status", "understanding_state"}


def normalize_intelligent_block(row: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_TOP_LEVEL - set(row)
    if missing:
        raise ValueError(f"INTELLIGENT_BLOCK_SOURCE_INVALID: missing={sorted(missing)}")

    content = row.get("content") if isinstance(row.get("content"), dict) else {}
    truth = content.get("truth") if isinstance(content.get("truth"), dict) else {}
    time = content.get("time") if isinstance(content.get("time"), dict) else {}
    context = content.get("context") if isinstance(content.get("context"), dict) else {}
    evidence = content.get("evidence") if isinstance(content.get("evidence"), dict) else {}
    provenance = content.get("provenance") if isinstance(content.get("provenance"), dict) else {}

    # Deliberately preserve only fields named by Claim Currentness V1.
    return {
        "block_id": str(row["block_id"]),
        "subject_id": str(row["subject_id"]),
        "status": str(row["status"]),
        "understanding_state": str(row["understanding_state"]),
        "superseded_by_block_id": row.get("superseded_by_block_id"),
        "truth": deepcopy(truth),
        "time": deepcopy(time),
        "context": deepcopy(context),
        "evidence": deepcopy(evidence),
        "provenance": deepcopy(provenance),
        "meaning": deepcopy(content.get("meaning") if isinstance(content.get("meaning"), dict) else {}),
    }


def load_intelligent_blocks(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a read-only normalized snapshot; never writes or mutates inputs."""
    return [normalize_intelligent_block(row) for row in rows]
