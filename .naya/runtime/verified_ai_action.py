#!/usr/bin/env python3
"""Universal Verified AI Action adapter over the existing Causal Verification Object."""
from __future__ import annotations
from typing import Any
from pathlib import Path
import importlib.util

def _load_cvo():
    path = Path(__file__).with_name("causal_verification.py")
    spec = importlib.util.spec_from_file_location("naya_causal_verification", path)
    if not spec or not spec.loader:
        raise ImportError("CAUSAL_VERIFICATION_RUNTIME_REQUIRED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

SCHEMA = "NAYAPOWER_VERIFIED_AI_ACTION_V1"

def build_verified_ai_action(execution_receipt: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    cvo = _load_cvo().build_causal_verification_object(execution_receipt, **kwargs)
    return {
        "schema": SCHEMA,
        "action_id": cvo["causal_id"],
        "causal": cvo,
    }
