"""Boundary validation for kernel/persistence_seam.py.

Covers the 10 directive cases:
 1. valid canonical payload
 2. missing required metadata
 3. invalid types / lifecycle state
 4. hash mismatch (tamper)
 5. source/configuration mismatch
 6. wrong ownership / scope
 7. claimed VERIFIED outcome without evidence (insert is always UNVERIFIED)
 8. unsupported successor authority
 9. supersession / lineage consistency
10. duplicate request -> deterministic idempotency key

Run: python3 tests/persistence_seam.test.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kernel"))

from persistence_seam import (
    project_kernel_receipt,
    validate_contract_record,
    verify_kernel_receipt,
    idempotency_key,
    _canon,
    _sha256,
)

OWNER = "12345678-1234-1234-1234-123456789abc"
KERNEL_SHA = "f58adf0826e0ea2c96d6e4a781b5191d2f4b8d5b"
PARENT = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def make_receipt(decision_id="dec-001", verdict="PASS", tamper=False,
                 with_inputs=False, inputs_state=None):
    body = {
        "receipt_id": f"decision-{decision_id}",
        "node_id": "naya-node-0001",
        "kernel_version": "nine-node-kernel-v1",
        "topology": "canonical-runtime-graph-v1",
        "decision_id": decision_id,
        "evaluation_order": ["SELF", "LAW"],
        "verdict": verdict,
        "stopped_at": None,
        "gates": [],
        "edge_trace": [],
        "issued_at": "2026-10-01T15:30:00+00:00",
        "candidate_banner": "CANDIDATE — NOT RATIFIED — NOT MERGED",
    }
    if with_inputs:
        state = inputs_state if inputs_state is not None else {"gates": {"SELF": {}}}
        body["inputs_hash"] = _sha256(state)
    body["receipt_hash"] = _sha256({k: v for k, v in body.items()})
    if tamper:
        body["verdict"] = "FAIL"  # mutate after hashing
    return body


def expect_value_error(fn, label):
    try:
        fn()
    except ValueError as e:
        print(f"  ok [{label}]: {str(e)[:90]}")
        return
    raise AssertionError(f"expected ValueError for {label}")


def test_1_valid_payload():
    r = make_receipt()
    p = project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA)
    assert p["p_owner_id"] == OWNER
    assert p["p_source_table"] == "naya_kernel_decision"
    assert p["p_source_id"] == "dec-001"
    assert p["p_event_at"] == "2026-10-01T15:30:00+00:00"  # kernel's own issued_at
    assert p["p_verification"]["state"] == "UNVERIFIED"
    assert p["p_outcome"] == {}
    assert p["p_metadata"]["kernel_sha"] == KERNEL_SHA
    assert p["p_metadata"]["node_id"] == "naya-node-0001"
    assert "received_at" in p["p_metadata"]
    assert p["p_value"]["receipt_hash"] == r["receipt_hash"]  # verbatim evidence
    print("  ok [valid payload projected]")


def test_2_missing_metadata():
    r = make_receipt()
    del r["receipt_hash"]
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA),
                       "missing receipt_hash")
    r2 = make_receipt()
    del r2["decision_id"]
    expect_value_error(lambda: project_kernel_receipt(r2, owner_id=OWNER, kernel_sha=KERNEL_SHA),
                       "missing decision_id")


def test_3_invalid_types():
    r = make_receipt()
    expect_value_error(lambda: project_kernel_receipt(r, owner_id="not-a-uuid", kernel_sha=KERNEL_SHA),
                       "owner_id not uuid")
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA,
                                                      owner_scope="EVERYONE"),
                       "owner_scope invalid")


def test_4_hash_mismatch():
    r = make_receipt(tamper=True)
    assert verify_kernel_receipt(r)["result"] == "MISMATCH"
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA),
                       "tampered receipt")


def test_5_source_config_mismatch():
    r = make_receipt()
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha="xyz"),
                       "kernel_sha not 40-hex")


def test_6_wrong_ownership():
    r = make_receipt()
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=None, kernel_sha=KERNEL_SHA),
                       "owner_id null")
    expect_value_error(lambda: project_kernel_receipt(r, owner_id="", kernel_sha=KERNEL_SHA),
                       "owner_id empty")


def test_7_no_verified_at_insert():
    # Even if the receipt body claims something strong, the seam inserts UNVERIFIED.
    r = make_receipt(verdict="PASS")
    r["verification"] = {"state": "VERIFIED_PASS"}  # kernel-side claim, if ever present
    r["receipt_hash"] = _sha256({k: v for k, v in r.items() if k != "receipt_hash"})
    p = project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA)
    assert p["p_verification"]["state"] == "UNVERIFIED", "insert must never claim verified"
    assert p["p_outcome"] == {}, "no outcome invented at insert"
    print("  ok [insert forced UNVERIFIED, no invented outcome]")


def test_8_bad_successor_authority():
    r = make_receipt()
    expect_value_error(lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA,
                                                      parent_ledger_event_id="nope"),
                       "parent not uuid")


def test_9_lineage_consistency():
    r = make_receipt()
    p = project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA,
                               parent_ledger_event_id=PARENT)
    assert p["p_parent_ledger_event_id"] == PARENT
    p2 = project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA)
    assert p2["p_parent_ledger_event_id"] is None
    print("  ok [lineage parent threaded / null]")


def test_10_duplicate_idempotency():
    k1 = idempotency_key(OWNER, "dec-001")
    k2 = idempotency_key(OWNER, "dec-001")
    k3 = idempotency_key(OWNER, "dec-002")
    assert k1 == k2 and k1 != k3
    assert k1 == f"{OWNER}|naya_kernel_decision|dec-001"
    print("  ok [idempotency key deterministic]")


def test_contract_record_validation():
    good = {
        "object_id": PARENT, "owner_id": OWNER, "owner_scope": "PRIVATE",
        "created_at": "2026-10-01T15:30:00+00:00", "updated_at": "2026-10-01T15:30:00+00:00",
        "schema_version": "1.0.0", "provenance": {"node_id": "x"},
        "truth_state": "CANDIDATE", "status": "RECORDED", "superseded_by": None,
        "lineage": {"parent": None}, "content_hash": "a" * 64,
    }
    assert validate_contract_record(good) == []
    bad = dict(good)
    del bad["owner_id"]
    assert any("owner_id" in x for x in validate_contract_record(bad))
    bad2 = dict(good, content_hash="zzz")
    assert any("content_hash" in x for x in validate_contract_record(bad2))
    print("  ok [contract record validation]")


def test_inputs_hash_verified():
    # Kernel binds inputs_hash; adapter recomputes over the submitted state.
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    p = project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA,
                               inputs_state=state)
    assert p["p_value"]["inputs_hash"] == _sha256(state)
    print("  ok [inputs_hash recomputed MATCH]")


def test_inputs_hash_mismatch_rejected():
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    expect_value_error(
        lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA,
                                       inputs_state={"gates": {"SELF": {"input": 2}}}),
        "inputs_hash mismatch")
    expect_value_error(
        lambda: project_kernel_receipt(r, owner_id=OWNER, kernel_sha=KERNEL_SHA),
        "inputs_hash without submitted state")


def main():
    tests = [test_1_valid_payload, test_2_missing_metadata, test_3_invalid_types,
             test_4_hash_mismatch, test_5_source_config_mismatch, test_6_wrong_ownership,
             test_7_no_verified_at_insert, test_8_bad_successor_authority,
             test_9_lineage_consistency, test_10_duplicate_idempotency,
             test_contract_record_validation, test_inputs_hash_verified,
             test_inputs_hash_mismatch_rejected]
    for t in tests:
        print(f"case: {t.__name__}")
        t()
    print(f"\nALL {len(tests)} boundary cases pass.")


if __name__ == "__main__":
    main()
