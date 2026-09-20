#!/usr/bin/env python3
"""Machine-readable preflight gate for the execution boundary (STEP 2).

The preflight/handoff contract (SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-
CONTRACT-V1.md) is documentation. This gate is the machine-enforced 10-question
execution object required at `transition("EXECUTING")`. It is distinct from
.naya/runtime/naya_preflight_gate.py (the structural repository governance
guard); this module gates consequential runtime execution itself:

    what, why, where, authority, protected, current_state, current_gap,
    next_action, proof, handoff

Each field must carry a truth classification:
    VERIFIED / INFERRED / UNKNOWN / CONFLICTED / REQUIRES_HUMAN_AUTHORITY

The gate refuses consequential execution when:
  - the preflight is missing, empty, or a field is unanswered;
  - a field has an invalid classification;
  - authority is not VERIFIED (unknown authority must never permit execution);
  - any field is CONFLICTED (reconcile before consequential execution);
  - any field REQUIRES_HUMAN_AUTHORITY (stop at the human boundary);
  - current_state or protected is UNKNOWN (cannot establish current truth or
    the protected baseline for consequential work).

Fields left as plain strings default to INFERRED, which may support planning
but is never proof.
"""
from __future__ import annotations

from typing import Any

PREFLIGHT_FIELDS: tuple[str, ...] = (
    "what",
    "why",
    "where",
    "authority",
    "protected",
    "current_state",
    "current_gap",
    "next_action",
    "proof",
    "handoff",
)

CLASSIFICATIONS: frozenset[str] = frozenset(
    {"VERIFIED", "INFERRED", "UNKNOWN", "CONFLICTED", "REQUIRES_HUMAN_AUTHORITY"}
)

UNKNOWN_BLOCKED_FIELDS: frozenset[str] = frozenset({"current_state", "protected"})


def _parse_field(payload: dict[str, Any], name: str) -> tuple[str, str]:
    raw = payload.get(name)
    if isinstance(raw, dict):
        value = raw.get("value")
        classification = str(raw.get("classification") or "INFERRED").upper()
    else:
        value = raw
        classification = "INFERRED"
    return value, classification


def gate_preflight(preflight: Any, *, context: str = "consequential execution") -> dict[str, Any]:
    reasons: list[str] = []
    warnings: list[str] = []

    if not isinstance(preflight, dict) or not preflight:
        return {
            "status": "REFUSED",
            "reasons": ["preflight is required for " + context],
            "warnings": warnings,
        }

    for name in PREFLIGHT_FIELDS:
        value, classification = _parse_field(preflight, name)
        if value in (None, ""):
            reasons.append(f"preflight missing field: {name}")
            continue
        if classification not in CLASSIFICATIONS:
            reasons.append(f"preflight field {name} has invalid classification {classification!r}")
            continue
        if classification == "REQUIRES_HUMAN_AUTHORITY":
            reasons.append(f"preflight {name} REQUIRES_HUMAN_AUTHORITY — stop at the human authority boundary")
            continue
        if classification == "CONFLICTED":
            reasons.append(f"preflight {name} is CONFLICTED — reconcile before {context}")
            continue
        if name == "authority" and classification != "VERIFIED":
            reasons.append(f"preflight authority is not VERIFIED (unknown authority blocks {context}): {classification}")
            continue
        if name in UNKNOWN_BLOCKED_FIELDS and classification == "UNKNOWN":
            reasons.append(f"preflight {name} is UNKNOWN — cannot establish the baseline required for {context}")
            continue
        if classification == "UNKNOWN":
            warnings.append(f"preflight {name} is UNKNOWN")

    if reasons:
        return {"status": "REFUSED", "reasons": reasons, "warnings": warnings}
    return {"status": "APPROVED", "reasons": [], "warnings": warnings}


def classified(value: Any, classification: str) -> dict[str, Any]:
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"invalid preflight classification: {classification!r}")
    return {"value": value, "classification": classification}


def approved_preflight(**overrides: Any) -> dict[str, Any]:
    preflight = {
        "what": classified("governed repository execution", "VERIFIED"),
        "why": classified("authorized governed maintenance", "VERIFIED"),
        "where": classified("repository working tree", "VERIFIED"),
        "authority": classified("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", "VERIFIED"),
        "protected": classified("fail-closed semantics and canonical stores", "VERIFIED"),
        "current_state": classified("current truth inspected", "VERIFIED"),
        "current_gap": classified("complete the governed work", "VERIFIED"),
        "next_action": classified("execute and record the governed work", "VERIFIED"),
        "proof": classified("governed test suite GREEN", "VERIFIED"),
        "handoff": classified("record canonical Activity event + successor torch", "VERIFIED"),
    }
    preflight.update(overrides)
    return preflight


__all__ = [
    "PREFLIGHT_FIELDS",
    "CLASSIFICATIONS",
    "UNKNOWN_BLOCKED_FIELDS",
    "gate_preflight",
    "classified",
    "approved_preflight",
]