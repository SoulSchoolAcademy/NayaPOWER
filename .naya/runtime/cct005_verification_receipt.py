#!/usr/bin/env python3
"""CCT-005 Outcome -> independent Verification Receipt boundary.

The authoritative verification operation remains evidence_runtime.verify_claim().
This module only records a receipt after that operation returns VERIFIED. It
cannot elevate an outcome, create authority, or turn unverified evidence into
verification.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

VERIFICATION_SCHEMA_VERSION = "1.0"
VERIFIED_STATE = "outcome_verified"


class VerificationReceiptRejected(ValueError):
    """Raised when an outcome cannot produce a verified receipt."""


def build_outcome_verification_receipt(
    outcome: dict[str, Any],
    *,
    activity_receipt_id: str,
    claim: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    verify_claim_fn: Callable[..., dict[str, Any]],
    receipt_id: str,
    verifier_type: str = "external_evidence",
    verification_method: str = "independent claim verification backed by canonical Activity receipt",
    verified_at: str | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    """Verify the claim through the existing authority, then emit one receipt."""
    if not isinstance(outcome, dict):
        raise VerificationReceiptRejected("outcome must be an object")
    outcome_id = outcome.get("outcome_id")
    if not isinstance(outcome_id, str) or not outcome_id:
        raise VerificationReceiptRejected("outcome_id is required")
    provenance = outcome.get("provenance")
    if not isinstance(provenance, dict):
        raise VerificationReceiptRejected("outcome provenance is required")
    if provenance.get("activity_receipt_id") != activity_receipt_id:
        raise VerificationReceiptRejected("activity_receipt_id must match outcome provenance")
    if not isinstance(activity_receipt_id, str) or not activity_receipt_id:
        raise VerificationReceiptRejected("activity_receipt_id is required")
    if not isinstance(receipt_id, str) or not receipt_id:
        raise VerificationReceiptRejected("receipt_id is required")
    if verifier_type not in {"system", "rule", "human", "external_evidence", "mixed"}:
        raise VerificationReceiptRejected("invalid verifier_type")
    if not isinstance(verification_method, str) or not verification_method.strip():
        raise VerificationReceiptRejected("verification_method is required")

    result = verify_claim_fn(claim, evidence_by_id, expected_commit=expected_commit)
    if not isinstance(result, dict) or result.get("status") != "VERIFIED":
        raise VerificationReceiptRejected(
            "authoritative claim verification did not return VERIFIED"
        )
    if claim.get("claim_id") != outcome_id:
        raise VerificationReceiptRejected(
            "claim_id must equal the CCT-005 outcome_id for subject binding"
        )

    stamp = verified_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "receipt_id": receipt_id,
        "schema_version": VERIFICATION_SCHEMA_VERSION,
        "subject_ref": outcome_id,
        "verification_state": VERIFIED_STATE,
        "verified_at": stamp,
        "verifier_type": verifier_type,
        "evidence_refs": [activity_receipt_id],
        "verification_method": verification_method,
    }
