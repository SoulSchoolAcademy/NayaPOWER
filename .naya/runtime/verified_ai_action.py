#!/usr/bin/env python3
"""Universal Verified AI Action adapter over the existing Causal Verification Object."""
from __future__ import annotations
from typing import Any
from causal_verification import build_causal_verification_object

SCHEMA = "NAYAPOWER_VERIFIED_AI_ACTION_V1"

def build_verified_ai_action(execution_receipt: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    cvo = build_causal_verification_object(execution_receipt, **kwargs)
    return {
        "schema": SCHEMA,
        "action_id": cvo["causal_id"],
        "causal": cvo,
    }
