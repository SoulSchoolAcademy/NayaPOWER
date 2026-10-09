import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.verify_capture_admission_proof import verify_capture_admission


def fixture():
    capture = {
        "capture_id": "capture-1",
        "title": "Test lesson",
        "lifecycle_state": "CANDIDATE",
        "intelligence": {"machine_view": {"automatic_truth_ceiling": "CANDIDATE"}},
    }
    expected = {
        "capture_path": ".naya/capture/capture-1.json",
        "capture_id": "capture-1",
        "expected_content": json.dumps(capture["intelligence"], sort_keys=True, separators=(",", ":"), ensure_ascii=False),
        "content_hash": hashlib.sha256(json.dumps(capture["intelligence"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(),
    }
    lineage = {
        "intelligent_block_id": "IB-1", "event_id": "event-1", "receipt_id": "receipt-1",
        "lineage_id": "lineage-1", "relationship_id": "relationship-1",
        "index_id": "index-1", "checkpoint_id": "checkpoint-1",
    }
    proof = {
        "schema": "NAYA_SMART_NOTE_CAPTURE_PROOF_V2",
        "intelligent_block_id": "IB-1",
        "event_id": "event-1", "receipt_id": "receipt-1", "lineage_id": "lineage-1",
        "relationship_id": "relationship-1", "index_id": "index-1", "checkpoint_id": "checkpoint-1",
        "understanding_state": "CANDIDATE",
        "exact_distilled_payload_match": True,
        "independent_lineage_verification": True,
        "content_hash": expected["content_hash"],
    }
    return capture, expected, lineage, proof


def check(c, e, l, p):
    return verify_capture_admission(c, e, l, p, capture_path=".naya/capture/capture-1.json")


def test_admits_exact_independently_verified_candidate():
    c, e, l, p = fixture()
    assert check(c, e, l, p).reason == "ADMIT"


def test_missing_lifecycle_state_fails_closed():
    c, e, l, p = fixture()
    del c["lifecycle_state"]
    assert check(c, e, l, p).reason == "LIFECYCLE_STATE_REQUIRED"


def test_non_candidate_lifecycle_is_not_promoted():
    c, e, l, p = fixture()
    c["lifecycle_state"] = "ACTIVE"
    assert check(c, e, l, p).reason == "LIFECYCLE_STATE_NOT_CANDIDATE"


def test_missing_independent_verification_is_rejected():
    c, e, l, p = fixture()
    p["independent_lineage_verification"] = False
    assert check(c, e, l, p).reason == "INDEPENDENT_LINEAGE_VERIFICATION_REQUIRED"


def test_wrong_content_hash_is_rejected():
    c, e, l, p = fixture()
    p["content_hash"] = "b" * 64
    assert check(c, e, l, p).reason == "CONTENT_HASH_MISMATCH"


def test_wrong_intelligent_block_is_rejected():
    c, e, l, p = fixture()
    p["intelligent_block_id"] = "IB-WRONG"
    assert check(c, e, l, p).reason == "INTELLIGENT_BLOCK_MISMATCH"


def test_truth_ceiling_cannot_be_promoted_by_capture_lifecycle():
    c, e, l, p = fixture()
    c["intelligence"]["machine_view"]["automatic_truth_ceiling"] = "ACTIVE"
    assert check(c, e, l, p).reason == "AUTOMATIC_TRUTH_CEILING_MUST_REMAIN_CANDIDATE"


def test_capture_identity_mismatch_is_rejected():
    c, e, l, p = fixture()
    e["capture_id"] = "other"
    assert check(c, e, l, p).reason == "CAPTURE_ID_MISMATCH"


def test_wrong_proof_schema_is_rejected():
    c, e, l, p = fixture()
    p["schema"] = "WRONG"
    assert check(c, e, l, p).reason == "PROOF_SCHEMA_MISMATCH"


def test_lineage_receipt_mismatch_is_rejected():
    c, e, l, p = fixture()
    p["receipt_id"] = "other-receipt"
    assert check(c, e, l, p).reason == "LINEAGE_RECEIPT_ID_MISMATCH"


def test_capture_path_mismatch_is_rejected():
    c, e, l, p = fixture()
    e["capture_path"] = ".naya/capture/other.json"
    assert check(c, e, l, p).reason == "CAPTURE_PATH_MISMATCH"


def test_modified_capture_is_not_admitted_against_old_receipt():
    c, e, l, p = fixture()
    c["intelligence"]["machine_view"]["lesson"] = "INJECTED_UNVERIFIED_POLICY"
    assert check(c, e, l, p).reason == "CAPTURE_DISTILLATION_MISMATCH"


def test_modified_expected_content_is_not_admitted_against_old_hash():
    c, e, l, p = fixture()
    e["expected_content"] = "UNBOUND_TAMPERED_CONTENT"
    assert check(c, e, l, p).reason == "CAPTURE_DISTILLATION_MISMATCH"


def test_colluding_capture_and_expected_with_old_proof_are_rejected():
    c, e, l, p = fixture()
    c["intelligence"]["machine_view"]["lesson"] = "INJECTED_UNVERIFIED_POLICY"
    e["expected_content"] = json.dumps(c["intelligence"], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert check(c, e, l, p).reason == "CAPTURE_CONTENT_HASH_MISMATCH"


def test_valid_unicode_payload_uses_receiver_canonical_serialization():
    c, e, l, p = fixture()
    c["intelligence"]["human_view"] = "Résumé — 学习 💜"
    e["expected_content"] = json.dumps(c["intelligence"], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    h = hashlib.sha256(e["expected_content"].encode("utf-8")).hexdigest()
    e["content_hash"] = h
    p["content_hash"] = h
    assert check(c, e, l, p).reason == "ADMIT"
