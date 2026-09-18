#!/usr/bin/env python3
"""Contract tests for the single NAYA_SUPERBRAIN_READY gate."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / ".naya/control-plane/naya_superbrain_ready.py"


def load():
    spec = importlib.util.spec_from_file_location("naya_superbrain_ready", GATE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_current_repository_is_blocked_by_unproven_boundaries():
    gate = load()
    payload = gate.evaluate()
    assert payload["gate"] == "NAYA_SUPERBRAIN_READY"
    assert payload["fail_closed"] is True
    assert payload["status"] == "BLOCKED"
    names = {c["name"]: c["status"] for c in payload["checks"]}
    assert names["golden_journey"] == "UNKNOWN"
    assert names["learning_adaptation"] == "UNKNOWN"
    assert names["privacy_access"] == "UNKNOWN"
    assert names["concurrency_idempotency"] == "UNKNOWN"
    assert names["runtime_parity"] == "PRODUCTION_PROVEN"
    assert names["authenticated_lifecycle"] == "BLOCKED"
    assert names["external_cold_naya"] == "BLOCKED"


def test_unknown_can_never_be_ready():
    gate = load()
    checks = [
        {"name": "known", "status": "VERIFIED", "evidence": [], "reason": ""},
        {"name": "unknown", "status": "UNKNOWN", "evidence": [], "reason": ""},
    ]
    payload = gate._finalize(checks, "fixture")
    assert payload["status"] == "BLOCKED"


def test_failed_can_never_be_ready():
    gate = load()
    checks = [
        {"name": "failed", "status": "FAILED", "evidence": [], "reason": ""},
    ]
    payload = gate._finalize(checks, "fixture")
    assert payload["status"] == "BLOCKED"


if __name__ == "__main__":
    test_current_repository_is_blocked_by_unproven_boundaries()
    test_unknown_can_never_be_ready()
    test_failed_can_never_be_ready()
    print("NAYA_SUPERBRAIN_READY_CONTRACT=PASS")
