#!/usr/bin/env python3
"""Dependency-free CCT Intelligent Block contract and fail-closed verifier.

This is the first executable CCT boundary. It intentionally implements the
smallest portable artifact needed to prove: producer -> verifier -> derivation
with integrity, provenance, authorization, and explicit lineage.

It does not perform network transport or LLM inference. Those are later layers.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

SCHEMA = "naya/cct/intelligent-block/v1"
ALLOWED_VERIFICATION = {"UNVERIFIED", "SUPPORTED", "VERIFIED"}
ALLOWED_LIFECYCLE = {"ACTIVE", "SUPERSEDED", "REVOKED"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(block: dict[str, Any]) -> str:
    payload = dict(block)
    payload.pop("integrity", None)
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def make_block(*, block_id: str, producer: str, content: dict[str, Any],
               evidence: list[dict[str, Any]], permissions: dict[str, Any],
               verification: str = "SUPPORTED", parent: str | None = None,
               derivation: str | None = None, lifecycle: str = "ACTIVE") -> dict[str, Any]:
    block: dict[str, Any] = {
        "schema": SCHEMA,
        "block_id": block_id,
        "producer": producer,
        "content": content,
        "provenance": {"origin": producer, "parent": parent, "derivation": derivation},
        "evidence": evidence,
        "verification": verification,
        "permissions": permissions,
        "lifecycle": lifecycle,
    }
    block["integrity"] = {"algorithm": "sha256", "content_hash": content_hash(block)}
    return block


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def verify_block(block: Any, *, consumer: str, purpose: str = "consume") -> Decision:
    """Fail-closed structural, integrity, provenance and permission verification."""
    if not isinstance(block, dict):
        return Decision(False, "block must be an object")
    required = {"schema", "block_id", "producer", "content", "provenance", "evidence",
                "verification", "permissions", "lifecycle", "integrity"}
    missing = sorted(required - set(block))
    if missing:
        return Decision(False, "missing required fields: " + ", ".join(missing))
    if block["schema"] != SCHEMA:
        return Decision(False, "unsupported schema")
    if not isinstance(block["block_id"], str) or not block["block_id"]:
        return Decision(False, "invalid block_id")
    if not isinstance(block["producer"], str) or not block["producer"]:
        return Decision(False, "invalid producer")
    if block["verification"] not in ALLOWED_VERIFICATION:
        return Decision(False, "invalid verification state")
    if block["lifecycle"] not in ALLOWED_LIFECYCLE:
        return Decision(False, "invalid lifecycle state")
    if block["lifecycle"] == "REVOKED":
        return Decision(False, "revoked block")
    provenance = block["provenance"]
    if not isinstance(provenance, dict) or provenance.get("origin") != block["producer"]:
        return Decision(False, "provenance origin does not match producer")
    evidence = block["evidence"]
    if not isinstance(evidence, list) or not evidence:
        return Decision(False, "evidence is required")
    integrity = block["integrity"]
    if not isinstance(integrity, dict) or integrity.get("algorithm") != "sha256":
        return Decision(False, "unsupported integrity declaration")
    expected = content_hash(block)
    if integrity.get("content_hash") != expected:
        return Decision(False, "integrity hash mismatch")
    permissions = block["permissions"]
    if not isinstance(permissions, dict):
        return Decision(False, "invalid permissions")
    consumers = permissions.get("consumers")
    if consumers != ["*"] and (not isinstance(consumers, list) or consumer not in consumers):
        return Decision(False, "consumer is not authorized")
    purposes = permissions.get("purposes")
    if purposes is not None and (not isinstance(purposes, list) or purpose not in purposes):
        return Decision(False, "purpose is not authorized")
    if block["verification"] == "UNVERIFIED":
        return Decision(False, "unverified block cannot cross the CCT consume boundary")
    return Decision(True, "accepted")


def derive_block(parent: dict[str, Any], *, consumer: str, block_id: str,
                 content: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    decision = verify_block(parent, consumer=consumer)
    if not decision.allowed:
        raise ValueError("parent rejected: " + decision.reason)
    return make_block(
        block_id=block_id,
        producer=consumer,
        content=content,
        evidence=evidence,
        permissions=parent["permissions"],
        verification="SUPPORTED",
        parent=parent["block_id"],
        derivation="independent-consumption",
    )
