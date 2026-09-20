#!/usr/bin/env python3
"""CCT-004 adversarial semantic guards.

Dependency-free, fail-closed checks for replay, identity, lineage, lifecycle,
contradiction, independence claims, authorization escalation, staleness, and
bounded portable payloads. This module does not provide network transport.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cct_intelligent_block import SCHEMA, content_hash, verify_block

MAX_BLOCK_BYTES = 64 * 1024
MAX_CONTENT_BYTES = 32 * 1024


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_block_semantics(block: Any, *, consumer: str, now: datetime | None = None,
                             known_ids: set[str] | None = None,
                             parent: dict[str, Any] | None = None) -> tuple[bool, str]:
    """Apply CCT-004 semantic guards after the base CCT verifier."""
    base = verify_block(block, consumer=consumer)
    if not base.allowed:
        return False, base.reason
    if known_ids is not None and block["block_id"] in known_ids:
        return False, "duplicate or replayed block identity"

    raw = __import__("json").dumps(block, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    content_raw = __import__("json").dumps(block["content"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if len(raw.encode("utf-8")) > MAX_BLOCK_BYTES:
        return False, "block exceeds payload limit"
    if len(content_raw.encode("utf-8")) > MAX_CONTENT_BYTES:
        return False, "content exceeds payload limit"

    lifecycle = block["lifecycle"]
    if lifecycle in {"REVOKED", "SUPERSEDED"}:
        return False, f"block lifecycle is {lifecycle.lower()}"

    provenance = block["provenance"]
    if provenance.get("parent") == block["block_id"]:
        return False, "circular self-lineage"
    if provenance.get("parent") and parent is None:
        return False, "parent artifact required for lineage verification"
    if parent is not None:
        if provenance.get("parent") != parent.get("block_id"):
            return False, "parent identity mismatch"
        if content_hash(parent) != parent.get("integrity", {}).get("content_hash"):
            return False, "parent integrity is invalid"
        if parent.get("lifecycle") in {"REVOKED", "SUPERSEDED"}:
            return False, "parent is no longer valid for derivation"
        if provenance.get("origin") == parent.get("provenance", {}).get("origin"):
            return False, "derived block falsely claims source-independent origin"

    derivation = provenance.get("derivation")
    if provenance.get("parent") and derivation != "independent-consumption":
        return False, "derived block lacks explicit derivation semantics"

    evidence = block["evidence"]
    for item in evidence:
        if isinstance(item, dict) and item.get("contradicts") is True and block["verification"] == "VERIFIED":
            return False, "contradictory evidence cannot support VERIFIED state"

    permissions = block["permissions"]
    if permissions.get("consumers") == ["*"] and parent is not None:
        parent_consumers = parent.get("permissions", {}).get("consumers")
        if parent_consumers != ["*"]:
            return False, "permission escalation"

    now = now or datetime.now(timezone.utc)
    valid_until = block.get("valid_until")
    if valid_until is not None:
        expiry = _parse_time(valid_until)
        if expiry is None:
            return False, "invalid validity timestamp"
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if now >= expiry:
            return False, "block is stale"

    return True, "accepted"
