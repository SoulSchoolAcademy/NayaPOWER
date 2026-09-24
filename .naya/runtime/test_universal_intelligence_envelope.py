#!/usr/bin/env python3
"""Fail-first contract tests for Universal Intelligence Envelope V1."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from universal_intelligence_envelope import SCHEMA, UniversalIntelligenceEnvelope
from project_intelligence_bridge import accept_universal_envelope


def valid():
    return {
        "schema": SCHEMA,
        "envelope_id": "ENV-001",
        "source": {"type": "smart_note", "id": "SN-001"},
        "identity": {"actor_type": "naya", "actor_id": "test-naya"},
        "owner_scope": {"owner_id": "owner-001", "project_id": "NayaNET"},
        "occurred_at": "2026-09-24T16:00:00Z",
        "received_at": "2026-09-24T16:00:01Z",
        "output": {"title": "Verified useful output", "content": "A meaningful test result."},
        "meaningfulness": "MEANINGFUL",
        "provenance": {"source_id": "SN-001", "source_ref": "main"},
        "epistemic": {"status": "OBSERVED"},
        "privacy": {"visibility": "PRIVATE"},
        "authority": {"status": "CONTEXT_ONLY"},
        "context": {"project": "NayaNET"},
        "idempotency_key": "ENV-001",
    }


def test_valid_envelope_round_trips():
    envelope = UniversalIntelligenceEnvelope.from_mapping(valid())
    payload = envelope.receiver_payload()
    assert payload["schema"] == SCHEMA
    assert payload["envelope_id"] == "ENV-001"
    assert payload["provenance"]["source_id"] == "SN-001"



def test_existing_receiver_adapter_preserves_envelope_identity():
    envelope = valid()
    packet = {"protocol": "NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1", "intelligence": []}
    adapted = accept_universal_envelope(envelope, packet)
    assert adapted["intelligence"][-1]["object_id"] == "envelope:ENV-001"
    assert adapted["universal_envelope_ids"] == ["ENV-001"]
    assert adapted["protocol"] == packet["protocol"]
    assert "persistence" not in adapted

def test_unknown_is_preserved():
    raw = valid()
    raw["epistemic"] = {"status": "UNKNOWN"}
    envelope = UniversalIntelligenceEnvelope.from_mapping(raw)
    assert envelope.epistemic["status"] == "UNKNOWN"


def test_missing_provenance_is_red():
    raw = valid()
    raw["provenance"] = {}
    try:
        UniversalIntelligenceEnvelope.from_mapping(raw)
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("missing provenance must be rejected")


def test_non_private_default_is_red():
    raw = valid()
    raw["privacy"] = {"visibility": "SHARED_BY_CONSENT"}
    try:
        UniversalIntelligenceEnvelope.from_mapping(raw)
    except ValueError as exc:
        assert "PRIVATE" in str(exc)
    else:
        raise AssertionError("non-private envelope must be rejected")


if __name__ == "__main__":
    tests = [test_valid_envelope_round_trips, test_existing_receiver_adapter_preserves_envelope_identity, test_unknown_is_preserved, test_missing_provenance_is_red, test_non_private_default_is_red]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} universal envelope contract tests")