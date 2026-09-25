#!/usr/bin/env python3
"""Core Intelligence semantic reconciliation over existing Intelligent Blocks.

This is a pure decision boundary: it does not create a second store and does
not mutate persistence. Callers use the returned disposition to route through
the existing canonical intelligence substrate.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

class Disposition(str, Enum):
    DUPLICATE="DUPLICATE"
    CONFIRM="CONFIRM"
    EXTEND="EXTEND"
    CORRECT="CORRECT"
    CONFLICT="CONFLICT"
    SUPERSEDE="SUPERSEDE"
    UNCERTAIN="UNCERTAIN"
    LOW_VALUE="LOW_VALUE"

@dataclass(frozen=True)
class Reconciliation:
    disposition: Disposition
    reason: str
    preserve_history: bool = True
    current_update_allowed: bool = False

def reconcile(candidate: dict[str, Any], current: list[dict[str, Any]]) -> Reconciliation:
    if not candidate.get("meaning"):
        return Reconciliation(Disposition.LOW_VALUE, "candidate has no reusable meaning")
    verification = candidate.get("verification")
    if isinstance(verification, dict):
        verification_state = str(
            verification.get("status")
            or verification.get("state")
            or verification.get("verification_state")
            or verification.get("evidence_state")
            or "UNKNOWN"
        ).upper()
    else:
        verification_state = str(verification or "UNKNOWN").upper()
    if verification_state in {"UNKNOWN", "UNVERIFIED", "UNPROVEN", "PENDING", "OBSERVED"}:
        return Reconciliation(Disposition.UNCERTAIN, "candidate is not sufficiently verified")
    key = candidate.get("semantic_key")
    matches = [x for x in current if key and x.get("semantic_key") == key]
    if not matches:
        return Reconciliation(Disposition.EXTEND, "no existing canonical understanding matches the semantic key", current_update_allowed=True)
    incumbent = matches[0]
    if candidate.get("claim") == incumbent.get("claim"):
        return Reconciliation(Disposition.DUPLICATE, "candidate restates the current understanding")
    if candidate.get("corrects") == incumbent.get("block_id"):
        return Reconciliation(Disposition.CORRECT, "candidate explicitly corrects the current understanding", current_update_allowed=True)
    if candidate.get("supersedes") == incumbent.get("block_id"):
        return Reconciliation(Disposition.SUPERSEDE, "candidate explicitly supersedes the current understanding", current_update_allowed=True)
    if candidate.get("contradicts") == incumbent.get("block_id"):
        return Reconciliation(Disposition.CONFLICT, "candidate contradicts the current understanding")
    if candidate.get("extends") == incumbent.get("block_id"):
        return Reconciliation(Disposition.EXTEND, "candidate explicitly extends the current understanding", current_update_allowed=True)
    return Reconciliation(Disposition.UNCERTAIN, "same semantic area but relationship to current understanding is not established")
