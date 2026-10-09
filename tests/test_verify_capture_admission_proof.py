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
        "expected_content": "lesson essence",
        "content_hash": "a" * 64,
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
        "content_hash": "a" * 64,
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
