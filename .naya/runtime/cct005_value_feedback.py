#!/usr/bin/env python3
"""Dependency-free CCT-005 outcome/value feedback primitive.

Records usage/outcome evidence without mutating the source intelligence block.
Value is a bounded, deterministic signal derived from outcome records; reuse
alone cannot increase value.  This is a local primitive, not a production
analytics or identity system.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

SCHEMA = "naya/cct/outcome/v1"
ALLOWED_OUTCOMES = {"SUCCESS", "FAILURE", "MIXED", "NO_EFFECT", "CONTRADICTED"}
ALLOWED_EVIDENCE = {"OBSERVED", "REPORTED", "INFERRED", "VERIFIED"}
ALLOWED_PRIVACY = {"PRIVATE", "SCOPED", "SHAREABLE"}
MAX_CONTEXT_BYTES = 4096


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def outcome_hash(record: dict[str, Any]) -> str:
    payload = dict(record)
    payload.pop("integrity", None)
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def make_outcome(*, outcome_id: str, block_id: str, actor: str, intended_use: str,
                 action: str, result: str, classification: str, evidence: list[dict[str, Any]],
                 confidence: float, context: dict[str, Any], privacy: str,
                 provenance: dict[str, Any]) -> dict[str, Any]:
    record = {
        "schema": SCHEMA,
        "outcome_id": outcome_id,
        "block_id": block_id,
        "actor": actor,
        "intended_use": intended_use,
        "action": action,
        "result": result,
        "classification": classification,
        "evidence": evidence,
        "confidence": confidence,
        "context": context,
        "privacy": privacy,
        "provenance": provenance,
    }
    record["integrity"] = {"algorithm": "sha256", "content_hash": outcome_hash(record)}
    return record


def verify_outcome(record: Any, *, block_id: str, authorized_actor: str | None = None) -> Decision:
    if not isinstance(record, dict):
        return Decision(False, "outcome must be an object")
    required = {"schema", "outcome_id", "block_id", "actor", "intended_use", "action",
                "result", "classification", "evidence", "confidence", "context", "privacy",
                "provenance", "integrity"}
    missing = sorted(required - set(record))
    if missing:
        return Decision(False, "missing required fields: " + ", ".join(missing))
    if record["schema"] != SCHEMA or not isinstance(record["outcome_id"], str) or not record["outcome_id"]:
        return Decision(False, "invalid schema or outcome_id")
    if record["block_id"] != block_id:
        return Decision(False, "outcome is not bound to the supplied intelligence block")
    if authorized_actor is not None and record["actor"] != authorized_actor:
        return Decision(False, "actor is not authorized")
    if record["classification"] not in ALLOWED_OUTCOMES:
        return Decision(False, "invalid outcome classification")
    if record["privacy"] not in ALLOWED_PRIVACY:
        return Decision(False, "invalid privacy scope")
    if not isinstance(record["evidence"], list) or not record["evidence"]:
        return Decision(False, "outcome evidence is required")
    if any(not isinstance(e, dict) or e.get("type") not in ALLOWED_EVIDENCE for e in record["evidence"]):
        return Decision(False, "invalid evidence classification")
    if not isinstance(record["confidence"], (int, float)) or not 0 <= record["confidence"] <= 1:
        return Decision(False, "confidence must be between 0 and 1")
    if not isinstance(record["context"], dict) or len(canonical_json(record["context"]).encode("utf-8")) > MAX_CONTEXT_BYTES:
        return Decision(False, "context exceeds bounded payload")
    provenance = record["provenance"]
    if not isinstance(provenance, dict) or provenance.get("source_block") != block_id:
        return Decision(False, "outcome provenance does not bind to source block")
    integrity = record["integrity"]
    if not isinstance(integrity, dict) or integrity.get("algorithm") != "sha256" or integrity.get("content_hash") != outcome_hash(record):
        return Decision(False, "integrity hash mismatch")
    return Decision(True, "accepted")


def value_signal(outcomes: list[dict[str, Any]]) -> float:
    """Return a bounded 0..100 signal; evidence strength must affect value."""
    valid: dict[str, dict[str, Any]] = {}
    for record in outcomes:
        outcome_id = record.get("outcome_id")
        if isinstance(outcome_id, str) and outcome_id not in valid:
            valid[outcome_id] = record
    if not valid:
        return 0.0
    weights = {"SUCCESS": 1.0, "FAILURE": -1.0, "MIXED": 0.0, "NO_EFFECT": 0.0, "CONTRADICTED": -0.75}
    evidence_weight = {"OBSERVED": 0.6, "REPORTED": 0.5, "INFERRED": 0.25, "VERIFIED": 1.0}
    total = 0.0
    maximum = 0.0
    for record in valid.values():
        cls = record.get("classification")
        confidence = float(record.get("confidence", 0)) if isinstance(record.get("confidence", 0), (int, float)) else 0.0
        evidence = record.get("evidence", [])
        strength = max((evidence_weight.get(e.get("type"), 0.0) for e in evidence if isinstance(e, dict)), default=0.0)
        contribution = weights.get(cls, 0.0) * confidence * strength
        total += contribution
        # Confidence measures how strongly the outcome is asserted; evidence
        # strength modulates the value contribution and must not be normalized
        # away by the denominator.
        maximum += confidence
    if maximum <= 0:
        return 0.0
    return round(max(0.0, min(100.0, 50.0 + 50.0 * total / maximum)), 4)
