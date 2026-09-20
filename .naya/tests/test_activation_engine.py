#!/usr/bin/env python3
"""Positive and deliberate-failure tests for zero-setup activation."""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from activation_contract import validate_manifest
from activation_engine import activate, inspect_package, stable_document_identity


def doc(i: int, content: str | None = None) -> dict:
    return {
        "document_id": f"ACT-{i:02d}",
        "version": "1.0",
        "package_id": "NAYA-ACTIVATION-TEST",
        "order": i,
        "purpose": f"Activation document {i}",
        "content": content or (f"Document {i} canonical knowledge. " * 30),
    }


def manifest(n: int = 1) -> dict:
    return {
        "schema_version": 1,
        "package_id": "NAYA-ACTIVATION-TEST",
        "package_version": "1.0",
        "north_star": "activate verified memory",
        "project": "Naya Power Superbrain",
        "documents": [doc(i) for i in range(1, n + 1)],
    }


def main() -> int:
    assert not validate_manifest(manifest(1))
    one = inspect_package(manifest(1))
    ten = inspect_package(manifest(10))
    twenty = inspect_package(manifest(20))
    assert one["status"] == "READY" and one["document_count"] == 1
    assert ten["status"] == "READY" and ten["document_count"] == 10
    assert twenty["status"] == "READY" and twenty["document_count"] == 20

    # Duplicate identity is deterministic and content-sensitive.
    a = stable_document_identity("P", "D", "1", "same")
    b = stable_document_identity("P", "D", "1", "same")
    c = stable_document_identity("P", "D", "1", "changed")
    assert a == b and a != c

    # Out-of-order / missing document is visible, never silently accepted.
    bad = manifest(3)
    bad["documents"] = [bad["documents"][0], bad["documents"][2]]
    bad["documents"][1]["order"] = 3
    assert inspect_package(bad)["status"] == "PARTIAL"

    # Empty content is a deliberate failure.
    empty = manifest(1)
    empty["documents"][0]["content"] = ""
    assert inspect_package(empty)["status"] == "FAILED"

    # Malformed package fails closed.
    malformed = manifest(1)
    malformed["documents"][0].pop("document_id")
    assert inspect_package(malformed)["status"] == "FAILED"

    # Derived activation state/receipt is idempotent.
    with tempfile.TemporaryDirectory() as td:
        import activation_engine as ae
        old_root, old_state, old_receipt = ae.ACTIVATION_ROOT, ae.STATE_FILE, ae.RECEIPT_FILE
        ae.ACTIVATION_ROOT = Path(td) / "activations"
        ae.STATE_FILE = ae.ACTIVATION_ROOT / "ACTIVATION-STATE.json"
        ae.RECEIPT_FILE = ae.ACTIVATION_ROOT / "ACTIVATION-RECEIPT.json"
        try:
            first = activate(manifest(10))
            state1 = ae.STATE_FILE.read_text(encoding="utf-8")
            second = activate(manifest(10))
            state2 = ae.STATE_FILE.read_text(encoding="utf-8")
            assert first == second and state1 == state2
            receipt = json.loads(ae.RECEIPT_FILE.read_text(encoding="utf-8"))
            assert receipt["verified"] is True and receipt["document_count"] == 10
        finally:
            ae.ACTIVATION_ROOT, ae.STATE_FILE, ae.RECEIPT_FILE = old_root, old_state, old_receipt

    # Canonical promotion uses the existing event writer, and replay is idempotent.
    with tempfile.TemporaryDirectory() as td:
        import activation_engine as ae
        old_events, old_index = ae.EVENTS, ae.INDEX
        ae.EVENTS = Path(td) / "events"
        ae.INDEX = ae.EVENTS / "INDEX.json"
        try:
            result = activate(manifest(1), effective_at="2026-08-26T01:20:00-07:00", promote=True)
            assert result["status"] == "READY"
            outcome = result["promotion"][0]
            assert outcome["status"] == "CREATED"
            event_path = ae.EVENTS / "2026/08/26/01/SE-20260826-012000-activation-act-01.json"
            assert event_path.exists()
            event = json.loads(event_path.read_text(encoding="utf-8"))
            assert event["verification"]["status"] == "VERIFIED"
            assert event["representations"]["naya"]["canonical_event_id"] == event["event_id"]
            assert event["representations"]["shawn"]["canonical_event_id"] == event["event_id"]
            replay = activate(manifest(1), effective_at="2026-08-26T01:20:00-07:00", promote=True)
            assert replay["promotion"][0]["status"] == "REPLAY"
            assert len(list(ae.EVENTS.rglob("SE-*.json"))) == 1
        finally:
            ae.EVENTS, ae.INDEX = old_events, old_index

    print("PASS — activation 1/10/20, duplicate, idempotency, ordering, deliberate-failure, and canonical-promotion tests GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
