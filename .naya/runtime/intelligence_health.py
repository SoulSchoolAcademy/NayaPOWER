#!/usr/bin/env python3
"""Derived NayaPOWER intelligence-health report.

Measures system usefulness boundaries without turning document counts into
"intelligence quality". No persistence is created.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya/memory"))
from smart_notes_v3 import load_canonical_ibs  # noqa: E402


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def report() -> dict[str, Any]:
    state = _read_json(ROOT / ".naya/control-plane/STATE.json")
    registry = _read_json(ROOT / ".naya/memory/smart-notes/REGISTRY.json")
    blocks = load_canonical_ibs(root=ROOT)

    ids = [x["intelligent_block_id"] for x in blocks]
    unique_ids = len(ids) == len(set(ids))
    authorized_retrieval_surface = all(
        x.get("canonical") is True
        and x.get("source", {}).get("registry")
        == ".naya/memory/smart-notes/REGISTRY.json"
        for x in blocks
    )

    unknown = list(state.get("unknown") or [])
    blocked = list(state.get("failures") or [])
    if state.get("next_action", {}).get("status") == "BLOCKED":
        blocked.append(state["next_action"])

    metrics = {
        "canonical_repository_ib_count": len(blocks),
        "canonical_repository_ib_ids_unique": unique_ids,
        "canonical_repository_retrieval_surface_valid": authorized_retrieval_surface,
        "registry_status": registry.get("status"),
        "cold_naya_unknown_count": len(unknown),
        "blocked_boundary_count": len(blocked),
        "current_block_status": state.get("current_block_status"),
        "recorded_head_is_authoritative": state.get("current_head", {}).get(
            "recorded_head_is_not_authoritative"
        ) is False,
    }

    green = [
        metrics["canonical_repository_ib_ids_unique"],
        metrics["canonical_repository_retrieval_surface_valid"],
        metrics["registry_status"] == "CANONICAL",
        metrics["recorded_head_is_authoritative"] is False,
    ]

    return {
        "schema": "NAYAPOWER_INTELLIGENCE_HEALTH_V1",
        "status": "GREEN" if all(green) else "ATTENTION",
        "metrics": metrics,
        "unknown": unknown,
        "blocked": blocked,
        "interpretation": {
            "quality_is_not_document_count": True,
            "repository_projection_is_not_the_full_live_runtime_population": True,
            "production_proof_is_separate_from_repository_health": True,
        },
        "highest_value_open_boundary": state.get("current_next_action"),
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, ensure_ascii=False))
