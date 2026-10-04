"""Tests for the Smart Note Promotion Writer.

The promotion writer implements the CANDIDATE -> VERIFIED state transition.
These tests use an isolated temp registry — they never touch the real index.
"""
import copy
import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _fresh_ts(days_ago=1):
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def make_registry(tmp_path):
    """Create a minimal registry with one CANDIDATE note."""
    reg = {
        "schema": "naya.smart-note-projection-index.v1",
        "version": "1.0",
        "entries": [
            {
                "smart_note_id": "SN-900",
                "intelligent_block_id": "IB-TEST-900",
                "title": "Test Note for Promotion",
                "truth_state": "CANDIDATE",
                "scope": "PRIVATE",
            }
        ],
    }
    p = tmp_path / "index.json"
    p.write_text(json.dumps(reg))
    return p


def make_evidence(gatherer_a="naya-2", gatherer_b="human-director"):
    """Two independent evidence items of different types."""
    return [
        {
            "type": "independent_verification",
            "source": "Naya 2 independent review of SN-900 claims",
            "content_hash": "a" * 64,
            "gatherer": gatherer_a,
            "gathered_at": _fresh_ts(1),
        },
        {
            "type": "behavioral_test",
            "source": "Held-out behavior test demonstrating the claim",
            "content_hash": "b" * 64,
            "gatherer": gatherer_b,
            "gathered_at": _fresh_ts(2),
        },
    ]


def test_valid_evidence_promotes_to_verified(tmp_path):
    reg_path = make_registry(tmp_path)
    # Point the module's record writer at tmp
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", make_evidence(), "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is True
    receipt = result["record"]
    assert receipt["old_state"] == "CANDIDATE"
    assert receipt["new_state"] == "VERIFIED"
    assert receipt["promoter"] == "naya-4"

    # Registry was updated
    reg = json.loads(reg_path.read_text())
    entry = reg["entries"][0]
    assert entry["truth_state"] == "VERIFIED"
    assert "promotion_receipt" in entry


def test_empty_evidence_stays_candidate(tmp_path):
    reg_path = make_registry(tmp_path)
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", [], "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    refusal = result["record"]
    assert refusal["reason_code"] == "EMPTY_EVIDENCE"

    reg = json.loads(reg_path.read_text())
    assert reg["entries"][0]["truth_state"] == "CANDIDATE"


def test_self_gathered_evidence_refused(tmp_path):
    """Promoter cannot be the evidence gatherer (anti-self-certification)."""
    reg_path = make_registry(tmp_path)
    evidence = make_evidence(gatherer_a="naya-4", gatherer_b="naya-4")
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    assert result["record"]["reason_code"] == "SELF_CERTIFICATION"

    reg = json.loads(reg_path.read_text())
    assert reg["entries"][0]["truth_state"] == "CANDIDATE"


def test_self_referential_evidence_refused(tmp_path):
    """A note cannot cite itself as evidence."""
    reg_path = make_registry(tmp_path)
    evidence = make_evidence()
    evidence[0]["note_ref"] = "SN-900"  # cites the note being promoted
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    assert result["record"]["reason_code"] == "SELF_REFERENTIAL"

    reg = json.loads(reg_path.read_text())
    assert reg["entries"][0]["truth_state"] == "CANDIDATE"


def test_receipt_has_all_required_fields(tmp_path):
    reg_path = make_registry(tmp_path)
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", make_evidence(), "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is True
    receipt = result["record"]
    required = [
        "schema", "note_id", "intelligent_block_id",
        "old_state", "new_state", "promoter", "promoted_at",
        "threshold_version", "evidence_hashes", "evidence_count",
        "gatherers", "receipt_hash",
    ]
    for field in required:
        assert field in receipt, f"Missing required field: {field}"
    assert receipt["schema"] == "naya.promotion-receipt.v1"
    assert len(receipt["evidence_hashes"]) == 2
    assert len(receipt["gatherers"]) == 2


def test_receipt_is_independently_reverifiable(tmp_path):
    """A second party can verify the promotion from receipt + evidence alone."""
    reg_path = make_registry(tmp_path)
    evidence = make_evidence()
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is True
    valid, detail = mod.verify_receipt(result["record"], evidence)
    assert valid is True, detail


def test_tampered_receipt_fails_verification(tmp_path):
    reg_path = make_registry(tmp_path)
    evidence = make_evidence()
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    tampered = copy.deepcopy(result["record"])
    tampered["gatherers"] = ["naya-4"]  # tamper without updating hash
    valid, detail = mod.verify_receipt(tampered, evidence)
    assert valid is False
    assert "hash mismatch" in detail.lower() or "tampered" in detail.lower()


def test_stale_evidence_refused(tmp_path):
    reg_path = make_registry(tmp_path)
    evidence = make_evidence()
    evidence[0]["gathered_at"] = _fresh_ts(100)  # older than 90-day max
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    assert result["record"]["reason_code"] == "STALE_EVIDENCE"


def test_single_gatherer_refused(tmp_path):
    """Two items from the same gatherer is not independence."""
    reg_path = make_registry(tmp_path)
    evidence = make_evidence(gatherer_a="naya-2", gatherer_b="naya-2")
    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", evidence, "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    failed = [f["check"] for f in result["record"]["failed_checks"]]
    assert "gatherer_independence" in failed


def test_already_verified_note_refused(tmp_path):
    reg_path = make_registry(tmp_path)
    reg = json.loads(reg_path.read_text())
    reg["entries"][0]["truth_state"] = "VERIFIED"
    reg_path.write_text(json.dumps(reg))

    orig_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        result = mod.promote_note("SN-900", make_evidence(), "naya-4", registry_path=reg_path)
    finally:
        mod.ROOT = orig_root

    assert result["promoted"] is False
    assert result["record"]["reason_code"] == "NOT_CANDIDATE"
