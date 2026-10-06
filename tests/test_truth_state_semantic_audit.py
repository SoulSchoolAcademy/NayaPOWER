import json
from pathlib import Path

from tools import smart_note_v2 as mod


def _root(tmp_path, entries):
    (tmp_path / ".naya" / "memory" / "smart-notes").mkdir(parents=True)
    (tmp_path / ".naya" / "capture").mkdir(parents=True)
    (tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES").mkdir(parents=True)
    (tmp_path / ".naya" / "memory" / "smart-notes" / "index.json").write_text(
        json.dumps({"entries": entries}), encoding="utf-8"
    )
    return tmp_path


def _semantic(report):
    return report["defects"]["truth_state_semantic_poison"]


def test_candidate_to_ratified_direct_edit_is_detected(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-TEST",
        "truth_state": "RATIFIED",
        "content_hash": "deadbeef",
    }])
    report = mod.audit_registry(root=root)
    assert {
        "smart_note_id": "SN-TEST",
        "reason": "ELEVATED_WITHOUT_PROMOTION_EVIDENCE",
        "truth_state": "RATIFIED",
    } in _semantic(report)


def test_verified_with_canonical_promotion_receipt_is_not_semantic_poison(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-TEST",
        "truth_state": "VERIFIED",
        "content_hash": "deadbeef",
        "promotion_receipt": {"promoter": "independent-verifier", "receipt_hash": "abc"},
    }])
    report = mod.audit_registry(root=root)
    assert _semantic(report) == []


def test_learned_requires_behavioral_evidence(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-TEST",
        "truth_state": "LEARNED",
        "content_hash": "deadbeef",
        "promotion_receipt": {"promoter": "independent-verifier", "receipt_hash": "abc"},
    }])
    report = mod.audit_registry(root=root)
    reasons = {x["reason"] for x in _semantic(report)}
    assert "LEARNED_WITHOUT_BEHAVIORAL_EVIDENCE" in reasons


def test_learned_with_behavioral_evidence_passes_semantic_audit(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-TEST",
        "truth_state": "LEARNED",
        "content_hash": "deadbeef",
        "promotion_receipt": {"promoter": "independent-verifier", "receipt_hash": "abc"},
        "behavioral_evidence": [{"task_id": "heldout-1", "delta": 1}],
    }])
    report = mod.audit_registry(root=root)
    assert _semantic(report) == []


def test_closed_legacy_ratified_allowlist_preserves_existing_two_only(tmp_path):
    entries = [
        {
            "smart_note_id": "SN-016",
            "truth_state": "RATIFIED",
            "content_hash": "h1",
            "provenance": {"receipt_id": "historical"},
        },
        {
            "smart_note_id": "SN-NET-POWER-MAGIC-001",
            "truth_state": "RATIFIED",
            "content_hash": "h2",
            "provenance": {"note": "Human Director direct ratification"},
        },
    ]
    report = mod.audit_registry(root=_root(tmp_path, entries))
    assert _semantic(report) == []


def test_legacy_allowlist_is_not_open_ended(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-OTHER",
        "truth_state": "RATIFIED",
        "content_hash": "deadbeef",
        "provenance": {"note": "self-asserted provenance is not enough"},
    }])
    report = mod.audit_registry(root=root)
    assert any(x["reason"] == "ELEVATED_WITHOUT_PROMOTION_EVIDENCE" for x in _semantic(report))


def test_unknown_truth_state_fails_closed(tmp_path):
    root = _root(tmp_path, [{
        "smart_note_id": "SN-TEST",
        "truth_state": "MAGIC",
        "content_hash": "deadbeef",
    }])
    report = mod.audit_registry(root=root)
    assert any(x["reason"] == "UNKNOWN_TRUTH_STATE" for x in _semantic(report))
