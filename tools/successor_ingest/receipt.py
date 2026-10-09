"""Successor-reuse receipt — tamper-evident, schema'd, evidence-only.

The receipt reconstructs one reuse event end-to-end: which verified
lesson, retrieved how, applied by whom, observed how, verified by what,
and whether reuse is claimed. A receipt is evidence, never authority
(the #1712 lesson): it carries no grant and satisfies no gate by itself.

Tamper-evidence: receipt_sha = sha256 over the canonical JSON of every
other field. Changing any field changes the sha — a forged receipt does
not verify.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict

from .models import Applicability, Lesson
from .verify import VerifyResult

SCHEMA = "naya.successor.reuse_receipt.v1"


def emit_reuse_receipt(
    *,
    lesson: Lesson,
    task_family: str,
    task_brief: str,
    cold_agent: str,
    applicability: Applicability,
    application_artifact: str,
    verify_result: VerifyResult,
    reused: bool,
    reuse_reason: str,
) -> dict:
    body = {
        "schema": SCHEMA,
        "lesson": {
            "id": lesson.id,
            "target_id": lesson.target_id,
            "level": lesson.level,
            "status": lesson.status,
            "provenance": lesson.provenance,
            "verification_method": lesson.verification_method,
            "claim_text": lesson.claim_text,
            "retrieved_at": lesson.retrieved_at,
            "retrieval_query": lesson.query,
        },
        "task": {
            "family": task_family,
            "brief_sha256": hashlib.sha256(task_brief.encode()).hexdigest(),
        },
        "cold_agent": cold_agent,
        "comprehend": {
            "verdict": applicability.verdict,
            "reason": applicability.reason,
        },
        "apply": {
            "artifact_sha256": hashlib.sha256(
                application_artifact.encode()).hexdigest(),
        },
        "observe": {
            "evidence": verify_result.evidence,
            "detail": verify_result.detail,
        },
        "independently_verify": {
            "verdict": verify_result.verdict,
            "mechanism": "deterministic AST verifier (tools/successor_ingest/verify.py), "
                         "separate from the applier",
        },
        "successor_reuse": {
            "reused": reused,
            "reason": reuse_reason,
        },
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    body["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return body


def verify_receipt_sha(receipt: dict) -> bool:
    """Recompute the sha over every field except receipt_sha256 itself."""
    sha = receipt.get("receipt_sha256")
    if not sha:
        return False
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest() == sha
