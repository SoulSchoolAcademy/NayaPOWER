import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "project_canonical_smart_note.py"
TARGET = ROOT / ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"

spec = importlib.util.spec_from_file_location("projection", SCRIPT)
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)


def receiver_transaction():
    block = {
        "identity": {
            "intelligent_block_id": "IB-009999",
            "event_id": "evt-009999",
            "schema_version": "NAYANET_INTELLIGENT_BLOCK_V1",
        },
        "meaning": {
            "title": "Projection Fidelity Test",
            "subject": "Projection Fidelity Test",
            "in_a_nutshell": "A score of 9/10 is material intelligence.",
            "content": "Preserve this exact source meaning. Do not summarize it away.",
        },
        "perspectives": {
            "human": "Preserve this exact source meaning. Do not summarize it away.",
            "child": "Keep the important meaning.",
            "grandma": "Keep the important meaning intact.",
            "naya": "The exact source meaning must survive projection.",
            "learning": "A supplied score is intelligence and must not be approximated.",
            "connections": "Source → receiver → IB → projection.",
            "application": "Retrieve and apply the exact lesson.",
            "meaning": "Canonicalization preserves meaning.",
            "value": "The next Naya inherits the same intelligence.",
        },
        "intent": {
            "why": "A successor must be able to recover the exact material meaning.",
            "desired_outcome": "The same intelligence remains attributable and reusable.",
        },
        "context": {"scope": "PRIVATE", "visibility": "PRIVATE"},
        "provenance": {"source": "test-source"},
        "evidence": {"evidence_state": "OBSERVED", "receipt_id": "receipt-009999"},
        "truth": {"state": "SUPPORTED"},
        "authority": {"state": "AUTHORIZED"},
        "learning": {"applicability": "Candidate — outcome verification pending.", "lesson": "A supplied score is intelligence and must not be approximated."},
        "action": {"action": "Retrieve and apply the exact lesson."},
        "outcome": {"state": "UNKNOWN"},
        "lifecycle": {"stage": "DISTILLED"},
        "metadata": {"projection_category": "system", "projection_topic": "fidelity-test"},
        "integrity": {},
    }
    block["integrity"]["content_hash"] = hashlib.sha256(
        projection.canonical_json(block).encode("utf-8")
    ).hexdigest()
    return {
        "id": "tx-009999",
        "event_id": "evt-009999",
        "created_at": "2026-09-25T20:00:00+00:00",
        "intelligent_block_id": "IB-009999",
        "intelligent_block": block,
        "evidence": {"receipt_id": "receipt-009999"},
    }


def test_receiver_is_sole_identity_authority_and_projection_is_deterministic(tmp_path):
    tx = receiver_transaction()
    first = projection.render(tx)
    second = projection.render(copy.deepcopy(tx))
    assert first == second
    assert "IB-009999" in first
    assert "9/10" in first
    assert "Preserve this exact source meaning. Do not summarize it away." in first
    assert "Smart Link" in first
    assert "/IB-009999/smart-note.md" in first
    assert "/hub?ib=IB-009999" in first
    assert "Smart Note = Intelligent Block" in first


def test_projection_rejects_meaning_or_score_drift():
    tx = receiver_transaction()
    expected = projection.render(tx)
    altered = tx["intelligent_block"]["meaning"]["in_a_nutshell"]
    tx["intelligent_block"]["meaning"]["in_a_nutshell"] = altered.replace("9/10", "7/10")
    try:
        projection.verify_projection(tx, expected)
    except ValueError as exc:
        assert "SMART_NOTE_PROJECTION_DRIFT" in str(exc)
    else:
        raise AssertionError("projection drift was not rejected")


def test_projection_rejects_identity_drift():
    tx = receiver_transaction()
    expected = projection.render(tx)
    tx["intelligent_block"]["identity"]["intelligent_block_id"] = "IB-000998"
    try:
        projection.verify_projection(tx, expected)
    except ValueError as exc:
        assert "SMART_NOTE_PROJECTION_DRIFT" in str(exc)
    else:
        raise AssertionError("identity drift was not rejected")


def test_existing_daily_scorecard_contains_material_score_and_canonical_identity():
    text = TARGET.read_text(encoding="utf-8")
    assert "**Intelligent Block ID:** `IB-001061`" in text
    assert "approximately 7/10" in text
    assert "Smart Link is the direct GitHub link to the canonical smart-note.md projection." in text
    assert "A Hub URL such as /hub?ib=IB-XXXXXX is a Hub Deep Link, not a Smart Link." in text
