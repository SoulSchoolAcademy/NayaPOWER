#!/usr/bin/env python3
"""Derived Causal Verification Object over existing NayaPOWER truth stores.

This module creates no persistence layer. It composes an execution receipt,
its authority/permission lineage, existing evidence, and an existing
verification receipt into one causal object that can be independently
checked.
"""
from __future__ import annotations
from typing import Any

SCHEMA = "NAYAPOWER_CAUSAL_VERIFICATION_OBJECT_V1"

def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""

def build_causal_verification_object(
    execution_receipt: dict[str, Any],
    *,
    verification_receipt: dict[str, Any] | None = None,
    verification_status: str | None = None,
    evidence_refs: list[str] | None = None,
    learning_refs: list[Any] | None = None,
    causal_id: str | None = None,
) -> dict[str, Any]:
    """Compose the causal chain; never upgrade an unverified execution."""
    if not isinstance(execution_receipt, dict):
        raise ValueError("EXECUTION_RECEIPT_REQUIRED")
    receipt_id = _text(str(execution_receipt.get("id", "")))
    if not receipt_id:
        raise ValueError("EXECUTION_RECEIPT_ID_REQUIRED")
    action = _text(execution_receipt.get("action"))
    expected = _text(execution_receipt.get("expected_result"))
    observed = _text(execution_receipt.get("observed_result"))
    status = _text(execution_receipt.get("status")).upper()
    if not action or not expected:
        raise ValueError("EXECUTION_RECEIPT_INTENT_INCOMPLETE")

    authority_status = _text(execution_receipt.get("authority_status_at_execution") or
                             execution_receipt.get("authority_status")).upper()
    authority = {
        "status": authority_status or "UNKNOWN",
        "grant_id": execution_receipt.get("authority_grant_id"),
        "issuer_id": execution_receipt.get("authority_issuer_id"),
        "subject_id": execution_receipt.get("user_id"),
        "source_event_id": execution_receipt.get("authority_source_event_id"),
    }
    permission = {
        "basis": "execution_receipt.authority_scope",
        "scope": execution_receipt.get("authority_scope"),
        "actions": execution_receipt.get("authority_actions"),
        "constraints": execution_receipt.get("authority_constraints"),
    }

    refs = list(evidence_refs or [])
    raw_evidence = execution_receipt.get("evidence")
    if isinstance(raw_evidence, list):
        for item in raw_evidence:
            if isinstance(item, dict):
                for key in ("evidence_id","id","cognition_event_id"):
                    value = _text(item.get(key))
                    if value and value not in refs:
                        refs.append(value)

    vr_status = _text(verification_status).upper() if verification_status else ""
    vr_id = None
    vr_method = None
    if isinstance(verification_receipt, dict):
        vr_id = _text(verification_receipt.get("receipt_id")) or None
        vr_method = _text(verification_receipt.get("verification_method")) or None
        vr_status = _text(verification_receipt.get("verification_state")).upper() or vr_status
        for ref in verification_receipt.get("evidence_refs", []) or []:
            value = _text(ref)
            if value and value not in refs:
                refs.append(value)

    gaps: list[str] = []
    if authority.get("status") != "AUTHORIZED":
        gaps.append("AUTHORITY_NOT_VERIFIED")
    if not execution_receipt.get("authority_grant_id"):
        gaps.append("AUTHORITY_GRANT_MISSING")
    if not execution_receipt.get("authority_scope"):
        gaps.append("PERMISSION_SCOPE_MISSING")
    if not observed:
        gaps.append("OBSERVED_RESULT_MISSING")
    if not refs:
        gaps.append("EVIDENCE_REFS_MISSING")
    if status != "SUCCESS":
        gaps.append(f"EXECUTION_STATUS_{status or 'UNKNOWN'}")
    if vr_status != "OUTCOME_VERIFIED":
        gaps.append("INDEPENDENT_VERIFICATION_NOT_PROVEN")

    causal_status = "VERIFIED" if not gaps else ("BLOCKED" if status == "BLOCKED" else "PARTIAL")
    return {
        "schema": SCHEMA,
        "causal_id": causal_id or f"CVO-{receipt_id}",
        "intent": {"action": action, "expected_result": expected},
        "authority": authority,
        "permission": permission,
        "action": {"name": action},
        "observation": {"result": observed or "UNKNOWN", "status": status or "UNKNOWN"},
        "evidence": {"refs": refs},
        "verification": {"status": vr_status or "UNKNOWN", "receipt_id": vr_id, "method": vr_method},
        "result": {"status": status or "UNKNOWN", "success": status == "SUCCESS" and not gaps},
        "receipt": {
            "execution_receipt_id": receipt_id,
            "cognition_event_id": execution_receipt.get("cognition_event_id"),
        },
        "learning": {"refs": list(learning_refs if learning_refs is not None else execution_receipt.get("learning", []) or [])},
        "causal_status": causal_status,
        "causal_gaps": gaps,
    }
