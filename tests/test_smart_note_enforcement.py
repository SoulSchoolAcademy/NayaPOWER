from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "memory"))
from smart_note_enforcement import (  # noqa: E402
    SmartNoteEnforcementError,
    detect_smart_note_request,
    enforce_smart_note_claim,
    validate_smart_note_operation,
)

EVENT_ID = "SE-20990101-120000-test-smart-note"
EFFECTIVE_AT = "2099-01-01T12:00:00-08:00"
COMMIT = "a" * 40


def governance_fixture() -> dict:
    return {
        "decision": {
            "decision_id": "DEC-20990101-SMART-NOTE",
            "mission": "preserve durable Smart Note intelligence",
            "actor": "naya",
            "request": "capture Smart Note event",
            "purpose": "smart-note-capture",
            "authority": {"authority_id": "AUTH-SMART-NOTE-001"},
            "scope": ["SoulSchoolAcademy/NayaPOWER/.naya/memory"],
            "boundaries": ["privacy-by-choice", "constitutional"],
            "evidence": ["event-payload", "receipt"],
            "uncertainty": 1,
            "consequence": 1,
            "reversibility": 1,
            "risk": {"prohibited": False},
            "alternatives": ["do-not-capture"],
            "value": {"responsible": True},
            "required_permission": "memory.write",
            "decision": "PROCEED",
            "execution_plan": ["persist event", "register index", "link feed"],
            "verification_plan": ["read back event", "verify receipt"],
            "stop_conditions": ["authority invalid", "evidence incomplete"],
            "receipt_requirements": ["canonical event", "index", "feed", "receipt"],
            "learning_output": ["record durable intelligence"],
        },
        "authority": {
            "authority_id": "AUTH-SMART-NOTE-001",
            "issuer": "human",
            "holder": "naya",
            "actor": "naya",
            "purpose": "smart-note-capture",
            "permissions": ["memory.write"],
            "scope": ["SoulSchoolAcademy/NayaPOWER/.naya/memory"],
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            "revoked_at": None,
            "status": "ACTIVE",
        },
    }


def fixture(tmp_path: Path) -> dict:
    event_dir = tmp_path / ".naya" / "memory" / "events" / "2099" / "01" / "01" / "12"
    event_dir.mkdir(parents=True)
    event = {
        "event_id": EVENT_ID,
        "effective_at": EFFECTIVE_AT,
        "representations": {
            "shawn": {"id": "SN-20990101-120000-shawn", "canonical_event_id": EVENT_ID, "content": "Human decision", "smart_link": "https://example.test/shawn"},
            "naya": {"id": "SN-20990101-120000-naya", "canonical_event_id": EVENT_ID, "content": "AI synthesis", "smart_link": "https://example.test/naya"},
            "machine": {"id": "SN-20990101-120000-machine", "canonical_event_id": EVENT_ID, "content": "Operational state", "smart_link": "https://example.test/machine"},
        },
    }
    (event_dir / f"{EVENT_ID}.json").write_text(json.dumps(event), encoding="utf-8")
    index = {"version": "3.0.0", "events": [{"event_id": EVENT_ID, "path": f"2099/01/01/12/{EVENT_ID}.json"}]}
    idx = tmp_path / ".naya" / "memory" / "events" / "INDEX.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps(index), encoding="utf-8")
    feed = tmp_path / ".naya" / "INTELLIGENT-FEED.md"
    feed.parent.mkdir(parents=True, exist_ok=True)
    feed.write_text(f"# Feed\n\n{EVENT_ID}\n", encoding="utf-8")
    return {
        "request_detected": True,
        "event_id": EVENT_ID,
        "event": event,
        "governance": governance_fixture(),
        "receipt": {
            "status": "VERIFIED",
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "branch": "main",
            "commit_sha": COMMIT,
            "canonical_event_url": f"https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/events/2099/01/01/12/{EVENT_ID}.json",
            "index_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/events/INDEX.json",
            "feed_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/INTELLIGENT-FEED.md",
        },
    }


def assert_reject(op, tmp_path, needle):
    errors = validate_smart_note_operation(op, root=tmp_path)
    assert any(needle in error for error in errors), errors
    try:
        enforce_smart_note_claim(op, root=tmp_path)
    except SmartNoteEnforcementError as exc:
        assert needle in str(exc)
    else:
        raise AssertionError("incomplete Smart Note claim was admitted")


def test_request_detection_positive_and_negative():
    assert detect_smart_note_request("Smart Note this")
    assert detect_smart_note_request("Naya, note this decision")
    assert detect_smart_note_request("lock this in")
    assert not detect_smart_note_request("tell me what a Smart Note is")
    assert not detect_smart_note_request("remember the general concept")


def test_complete_operation_is_admitted():
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as d:
        op = fixture(Path(d))
        result = enforce_smart_note_claim(op, root=Path(d))
        assert result["status"] == "VERIFIED"
        assert result["pis_propagation"] == "SEPARATE_EVIDENCE_REQUIRED"


def test_missing_governance_gate_is_rejected(tmp_path):
    op = fixture(tmp_path)
    del op["governance"]
    assert_reject(op, tmp_path, "canonical governance decision/authority is missing")


def test_expired_governance_authority_is_rejected(tmp_path):
    op = fixture(tmp_path)
    op["governance"]["authority"]["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    assert_reject(op, tmp_path, "expired")


def test_wrong_governance_permission_is_rejected(tmp_path):
    op = fixture(tmp_path)
    op["governance"]["authority"]["permissions"] = ["memory.read"]
    assert_reject(op, tmp_path, "required permission is not granted")


def test_missing_shawn_representation_is_rejected(tmp_path):
    op = fixture(tmp_path)
    del op["event"]["representations"]["shawn"]
    assert_reject(op, tmp_path, "missing or empty shawn representation")


def test_missing_naya_representation_is_rejected(tmp_path):
    op = fixture(tmp_path)
    del op["event"]["representations"]["naya"]
    assert_reject(op, tmp_path, "missing or empty naya representation")


def test_missing_machine_representation_is_rejected(tmp_path):
    op = fixture(tmp_path)
    del op["event"]["representations"]["machine"]
    assert_reject(op, tmp_path, "missing or empty machine representation")


def test_canonical_persistence_is_required(tmp_path):
    op = fixture(tmp_path)
    (tmp_path / ".naya" / "memory" / "events" / "2099" / "01" / "01" / "12" / f"{EVENT_ID}.json").unlink()
    assert_reject(op, tmp_path, "not persisted at the required path")


def test_index_registration_is_required(tmp_path):
    op = fixture(tmp_path)
    (tmp_path / ".naya" / "memory" / "events" / "INDEX.json").write_text('{"events": []}', encoding="utf-8")
    assert_reject(op, tmp_path, "not registered in events/INDEX.json")


def test_feed_linkage_is_required(tmp_path):
    op = fixture(tmp_path)
    (tmp_path / ".naya" / "INTELLIGENT-FEED.md").write_text("# Feed\n", encoding="utf-8")
    assert_reject(op, tmp_path, "not linked from the Intelligent Feed")


def test_receipt_and_smart_links_are_required(tmp_path):
    op = fixture(tmp_path)
    op["receipt"]["commit_sha"] = "bad"
    del op["receipt"]["feed_url"]
    del op["event"]["representations"]["naya"]["smart_link"]
    errors = validate_smart_note_operation(op, root=tmp_path)
    assert any("valid 40-character commit SHA" in e for e in errors), errors
    assert any("receipt missing feed_url" in e for e in errors), errors
    assert any("naya representation missing Smart Link" in e for e in errors), errors
    try:
        enforce_smart_note_claim(op, root=tmp_path)
    except SmartNoteEnforcementError:
        pass
    else:
        raise AssertionError("incomplete receipt/Smart Link claim was admitted")


def test_pis_propagation_is_separate(tmp_path):
    op = fixture(tmp_path)
    op["pis_propagated"] = True
    assert_reject(op, tmp_path, "PIS propagation claim is invalid")


def test_verified_pis_requires_separate_evidence_and_receipt(tmp_path):
    op = fixture(tmp_path)
    op["pis_propagation"] = {"status": "VERIFIED"}
    assert_reject(op, tmp_path, "PIS propagation marked VERIFIED")


def test_incomplete_claim_is_rejected_even_when_event_exists(tmp_path):
    op = fixture(tmp_path)
    op["request_detected"] = False
    assert_reject(op, tmp_path, "request was not detected")


def test_event_binding_and_distinct_ids_are_adversarially_checked(tmp_path):
    op = fixture(tmp_path)
    op["event"]["representations"]["naya"]["canonical_event_id"] = "SE-20990101-120000-other"
    assert_reject(op, tmp_path, "naya representation is not bound")
    op = fixture(tmp_path)
    op["event"]["representations"]["machine"]["id"] = op["event"]["representations"]["shawn"]["id"]
    assert_reject(op, tmp_path, "IDs must be distinct")
