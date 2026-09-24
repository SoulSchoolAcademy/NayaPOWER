#!/usr/bin/env python3
"""Execution-facing contract for portable INTELLIGENCE_COMMIT authorization.

This module mirrors the minimum contract the deployed
nayanet-compound-intelligence function must enforce before it calls the
existing nayanet_record_cognition_event receipt path.

It is deliberately subordinate to UniversalExecutionGate:
- the gate remains the sole authority issuer;
- the portable artifact is proof of gate issuance, not new authority;
- artifact_hash identifies the exact serialized artifact;
- the existing receipt evidence JSON is the backwards-compatible persistence
  location, so no receipt-table migration is required for this seam.

This module performs no network or production mutation.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

from portable_authorization import portable_authorization_artifact_hash

REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
ACTION_TYPE = "INTELLIGENCE_COMMIT"
PERMISSION = "intelligence_commit"
TARGET = "NayaNET"

_REQUIRED_AUTH_FIELDS = (
    "authority_id",
    "decision_id",
    "action_id",
    "action_type",
    "target",
    "actor_id",
    "scope",
    "permission",
    "governance_state",
    "binding_hash",
)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _fail(code: str, detail: str) -> dict[str, Any]:
    return {"allowed": False, "code": code, "detail": detail}


def validate_execution_envelope(
    *,
    envelope: Mapping[str, Any],
    expected_actor_id: str,
    expected_commit_sha: str,
    expected_repository: str = REPOSITORY,
) -> dict[str, Any]:
    """Validate the exact request envelope before the existing commit path.

    The outer execution_authorization must match the signed portable
    authorization identity. The supplied artifact_hash must match the exact
    serialized artifact. This closes the two gaps without introducing another
    authority issuer.
    """
    if not isinstance(envelope, Mapping):
        return _fail("EXECUTION_ENVELOPE_REQUIRED", "request envelope must be an object")

    artifact = envelope.get("portable_authorization")
    supplied_hash = str(envelope.get("portable_authorization_artifact_hash", "")).strip()
    ordinary = envelope.get("execution_authorization")

    if not isinstance(artifact, Mapping):
        return _fail("PORTABLE_AUTHORIZATION_REQUIRED", "portable_authorization is required")
    if not supplied_hash:
        return _fail("PORTABLE_ARTIFACT_HASH_REQUIRED", "portable_authorization_artifact_hash is required")
    if not isinstance(ordinary, Mapping):
        return _fail("EXECUTION_AUTHORIZATION_REQUIRED", "execution_authorization is required")

    actual_hash = portable_authorization_artifact_hash(artifact)
    if actual_hash != supplied_hash:
        return _fail("PORTABLE_ARTIFACT_HASH_MISMATCH", "artifact hash does not identify the supplied artifact")

    signed = artifact.get("authorization")
    if not isinstance(signed, Mapping):
        return _fail("PORTABLE_AUTHORIZATION_MALFORMED", "artifact.authorization is required")

    missing = [key for key in _REQUIRED_AUTH_FIELDS if not str(signed.get(key, "")).strip()]
    if missing:
        return _fail("PORTABLE_AUTHORIZATION_INCOMPLETE", ",".join(missing))

    if signed.get("action_type") != ACTION_TYPE:
        return _fail("ACTION_TYPE_MISMATCH", "portable authorization is not INTELLIGENCE_COMMIT")
    if signed.get("permission") != PERMISSION:
        return _fail("PERMISSION_MISMATCH", "portable authorization is not intelligence_commit")
    if signed.get("target") != TARGET:
        return _fail("TARGET_MISMATCH", "portable authorization target is not NayaNET")
    if signed.get("actor_id") != expected_actor_id:
        return _fail("ACTOR_MISMATCH", "portable authorization actor does not match the authenticated user")
    if signed.get("repository") != expected_repository:
        return _fail("REPOSITORY_MISMATCH", "portable authorization repository does not match the execution repository")
    if signed.get("commit_sha") != expected_commit_sha:
        return _fail("SOURCE_COMMIT_MISMATCH", "portable authorization source commit does not match the execution source")

    # Bind the ordinary credential consumed by the existing RPC to the exact
    # credential that was signed and independently verified.
    for key in _REQUIRED_AUTH_FIELDS:
        if ordinary.get(key) != signed.get(key):
            return _fail("AUTHORIZATION_ARTIFACT_MISMATCH", f"{key} differs between authorization and portable artifact")

    return {
        "allowed": True,
        "code": "PORTABLE_AUTHORIZATION_BOUND",
        "artifact_hash": actual_hash,
        "authorization": copy.deepcopy(dict(signed)),
    }


def receipt_evidence(
    *,
    existing_evidence: Any,
    artifact: Mapping[str, Any],
    artifact_hash: str,
) -> dict[str, Any]:
    """Return backwards-compatible receipt evidence with exact artifact identity."""
    evidence: dict[str, Any]
    if isinstance(existing_evidence, Mapping):
        evidence = copy.deepcopy(dict(existing_evidence))
    else:
        evidence = {"legacy_evidence": existing_evidence}

    evidence["portable_authorization"] = copy.deepcopy(dict(artifact))
    evidence["portable_authorization_artifact_hash"] = str(artifact_hash)
    return evidence


def reconstruct_receipt_evidence(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Reconstruct the portable artifact identity from persisted receipt evidence."""
    evidence = receipt.get("evidence")
    if not isinstance(evidence, Mapping):
        return _fail("RECEIPT_EVIDENCE_MISSING", "receipt evidence is not an object")

    artifact = evidence.get("portable_authorization")
    stored_hash = str(evidence.get("portable_authorization_artifact_hash", "")).strip()
    if not isinstance(artifact, Mapping):
        return _fail("RECEIPT_PORTABLE_AUTHORIZATION_MISSING", "portable authorization is absent from receipt evidence")
    if not stored_hash:
        return _fail("RECEIPT_ARTIFACT_HASH_MISSING", "portable artifact hash is absent from receipt evidence")

    recomputed = portable_authorization_artifact_hash(artifact)
    if recomputed != stored_hash:
        return _fail("RECEIPT_ARTIFACT_HASH_MISMATCH", "persisted artifact hash does not match persisted artifact")

    return {
        "allowed": True,
        "code": "RECEIPT_PORTABLE_AUTHORIZATION_RECONSTRUCTED",
        "artifact_hash": recomputed,
        "artifact": copy.deepcopy(dict(artifact)),
    }


__all__ = [
    "REPOSITORY",
    "ACTION_TYPE",
    "PERMISSION",
    "TARGET",
    "validate_execution_envelope",
    "receipt_evidence",
    "reconstruct_receipt_evidence",
]
