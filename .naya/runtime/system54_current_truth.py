"""System 54 canonical current-truth boundary.

Canonical Intelligent Blocks are authoritative. The legacy repository-event
resolver is retained only as a compatibility shadow. A divergence is allowed
only when the caller supplies the explicit, versioned migration explanation;
otherwise the gate fails closed and canonical current[] is not emitted.
"""
from __future__ import annotations

from typing import Any, Callable, Iterable

from claim_currentness_v1 import resolve_currentness

MIGRATION_REASON = "SYSTEM54_CANONICAL_BLOCK_MIGRATION_V1"
CANONICAL_AUTHORITY = "CANONICAL_INTELLIGENT_BLOCK"
LEGACY_SHADOW = "LEGACY_REPOSITORY_EVENT_COMPATIBILITY"


def _ids(result: dict[str, Any]) -> list[str]:
    return [str(x.get("block_id") or x.get("event_id")) for x in result.get("current", [])]


def _canonical_current(result: dict[str, Any]) -> list[dict[str, Any]]:
    selected = result.get("selected_block_id")
    if not selected:
        return []
    return [result["blocks_by_id"][selected]]


def compare_with_legacy(
    canonical_result: dict[str, Any],
    legacy_result: dict[str, Any],
    *,
    migration_reason: str | None = None,
) -> dict[str, Any]:
    """Fail closed on unexplained authority divergence."""
    canonical_ids = [str(canonical_result["selected_block_id"])] if canonical_result.get("selected_block_id") else []
    legacy_ids = _ids(legacy_result)

    if canonical_ids == legacy_ids:
        return {
            "status": "PASS",
            "reason": "AUTHORITY_OUTPUTS_EQUAL",
            "canonical_ids": canonical_ids,
            "legacy_ids": legacy_ids,
        }

    if migration_reason != MIGRATION_REASON:
        return {
            "status": "BLOCKED",
            "reason": "UNEXPLAINED_AUTHORITY_DIVERGENCE",
            "canonical_ids": canonical_ids,
            "legacy_ids": legacy_ids,
        }

    return {
        "status": "PASS",
        "reason": MIGRATION_REASON,
        "canonical_ids": canonical_ids,
        "legacy_ids": legacy_ids,
        "legacy_role": LEGACY_SHADOW,
        "canonical_role": CANONICAL_AUTHORITY,
    }


def resolve_system54(
    blocks: Iterable[dict[str, Any]],
    legacy_builder: Callable[[], dict[str, Any]],
    *,
    now,
    requested_scope: str = "PRIVATE",
    migration_reason: str | None = None,
) -> dict[str, Any]:
    """Resolve System 54 from canonical Blocks, gated by legacy shadow."""
    block_rows = list(blocks)
    canonical = resolve_currentness(
        block_rows, now, requested_scope=requested_scope
    )
    by_id = {str(b["block_id"]): b for b in block_rows}

    legacy = legacy_builder()
    gate = compare_with_legacy(
        {
            **canonical,
            "blocks_by_id": by_id,
        },
        legacy,
        migration_reason=migration_reason,
    )

    if gate["status"] != "PASS":
        raise RuntimeError(
            "SYSTEM54_CANONICAL_SHADOW_BLOCKED:"
            + gate["reason"]
        )

    output = {
        "schema": "naya-power-project-intelligence/v1",
        "resolution": {
            "status": "RECONSTRUCTED",
            "authority": CANONICAL_AUTHORITY,
            "compatibility_shadow": LEGACY_SHADOW,
            "shadow_gate": gate,
        },
        "current": _canonical_current({**canonical, "blocks_by_id": by_id}),
        "currentness": canonical,
        "legacy_shadow": legacy,
        "counts": {
            "current": len(canonical_ids := (
                [canonical["selected_block_id"]]
                if canonical.get("selected_block_id")
                else []
            )),
            "legacy_current": len(legacy.get("current", [])),
        },
    }
    return output
