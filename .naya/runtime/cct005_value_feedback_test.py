#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cct005_value_feedback import make_outcome, verify_outcome, value_signal

BLOCK = "block-a"

def outcome(outcome_id="o1", classification="SUCCESS", evidence_type="VERIFIED", actor="naya-b", privacy="SCOPED", context=None):
    return make_outcome(
        outcome_id=outcome_id, block_id=BLOCK, actor=actor,
        intended_use="solve-task", action="used-block", result="task completed",
        classification=classification, evidence=[{"type": evidence_type, "ref": "e1"}],
        confidence=1.0, context={"domain": "test"} if context is None else context, privacy=privacy,
        provenance={"source_block": BLOCK},
    )

def test_valid_outcome():
    assert verify_outcome(outcome(), block_id=BLOCK).allowed

def test_wrong_block_denied():
    assert not verify_outcome(outcome(), block_id="other").allowed

def test_actor_mismatch_denied():
    assert not verify_outcome(outcome(), block_id=BLOCK, authorized_actor="naya-a").allowed

def test_missing_evidence_denied():
    x = outcome(); x["evidence"] = []
    assert not verify_outcome(x, block_id=BLOCK).allowed

def test_forged_outcome_integrity_denied():
    x = outcome(); x["result"] = "fabricated"
    assert not verify_outcome(x, block_id=BLOCK).allowed

def test_private_context_not_shareable_by_default():
    x = outcome(privacy="PRIVATE", context={"secret": "do-not-export"})
    assert verify_outcome(x, block_id=BLOCK).allowed
    assert x["privacy"] == "PRIVATE"

def test_duplicate_outcome_does_not_inflate_value():
    x = outcome()
    assert value_signal([x]) == value_signal([x, x])

def test_reuse_alone_does_not_create_value():
    assert value_signal([]) == 0.0

def test_failure_reduces_value():
    assert value_signal([outcome(classification="FAILURE")]) < value_signal([outcome(classification="SUCCESS")])

def test_contradiction_reduces_value():
    assert value_signal([outcome(classification="CONTRADICTED")]) < value_signal([outcome(classification="SUCCESS")])

def test_inferred_is_weaker_than_verified():
    assert value_signal([outcome(evidence_type="INFERRED")]) < value_signal([outcome(evidence_type="VERIFIED")])

def test_invalid_confidence_denied():
    x = outcome(); x["confidence"] = 2.0
    assert not verify_outcome(x, block_id=BLOCK).allowed

def test_oversized_context_denied():
    x = outcome(); x["context"] = {"payload": "x" * 5000}
    assert not verify_outcome(x, block_id=BLOCK).allowed

def test_provenance_mismatch_denied():
    x = outcome(); x["provenance"] = {"source_block": "other"}
    assert not verify_outcome(x, block_id=BLOCK).allowed

def test_unknown_classification_denied():
    x = outcome(); x["classification"] = "MAGIC"
    assert not verify_outcome(x, block_id=BLOCK).allowed

if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for test in tests:
        test(); print("PASS", test.__name__)
    print(f"PASS {len(tests)} CCT-005 tests")
