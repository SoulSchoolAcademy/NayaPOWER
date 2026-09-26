#!/usr/bin/env python3
"""Regression gate for the Universal Agent Interface Smart Note capability."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / "NAYANET" / "UNIVERSAL-AGENT-INTERFACE" / "worker.js"
OPENAPI = ROOT / "NAYANET" / "UNIVERSAL-AGENT-INTERFACE" / "openapi.yaml"


def test_uai_exposes_canonical_smart_note_capture():
    worker = WORKER.read_text(encoding="utf-8")
    assert "nayanet_smart_note_capture" in worker
    assert "smart_note_capture" in worker
    assert "v7-smart-note-canonical" in worker


def test_uai_smart_note_capture_requires_the_completion_contract():
    worker = WORKER.read_text(encoding="utf-8")
    assert "human_note" in worker
    assert "naya_note" in worker
    assert "idempotency_key" in worker
    assert "smart_link" in worker
    assert "intelligent_block_id" in worker
    assert "PROJECTION_VERIFIED" in worker


def test_uai_openapi_documents_the_same_canonical_operation():
    spec = OPENAPI.read_text(encoding="utf-8")
    assert "captureCanonicalSmartNote" in spec
    assert "smart_note_capture" in spec
    assert "v7-smart-note-canonical" in spec


if __name__ == "__main__":
    tests = [
        test_uai_exposes_canonical_smart_note_capture,
        test_uai_smart_note_capture_requires_the_completion_contract,
        test_uai_openapi_documents_the_same_canonical_operation,
    ]
    for test in tests:
        test()
    print(f"PASS {len(tests)}/{len(tests)} UAI Smart Note capability tests")
