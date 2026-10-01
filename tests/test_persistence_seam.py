"""Boundary validation for kernel/persistence_seam.py.

Pytest-discoverable (tests/test_*.py). Covers the directive cases:
 1. valid canonical payload
 2. missing required metadata
 3. invalid types / lifecycle state
 4. hash mismatch (tamper)
 5. source/configuration shape (labels, not provenance)
 6. ownership / scope shape (uuid format, not isolation proof)
 7. claimed VERIFIED outcome without evidence (insert is always UNVERIFIED)
 8. successor parent shape (uuid format, not lineage authorization)
 9. lineage threading
10. duplicate request -> deterministic idempotency key shape
11. seal validation: numeric/null/malformed receipt_hash rejected (RED-1)
12. receipt vocabulary: bogus verdict, bad timestamp, wrong types rejected
13. input commitment: inputs_hash verified; legacy receipts labeled absent
14. interop: real kernel-produced receipt verifies against the producer

What these tests do NOT prove (stated, not hidden):
- "ownership" tests uuid SHAPE; owner isolation is a database property
  (LEDGER_OWNER_MISMATCH / RLS), proven only by DB evidence.
- "idempotency" tests key determinism; safe replay is a database property.
- "successor authority" tests parent uuid SHAPE; lineage authorization is
  a database/governance property.
- kernel_sha/config_hash are caller-supplied LABELS; provenance must be
  established by the execution context, not by this adapter.

Run: python -m pytest tests/test_persistence_seam.py -q
"""
import json
from pathlib import Path

from kernel.persistence_seam import (
    project_kernel_receipt,
    validate_contract_record,
    verify_kernel_receipt,
    idempotency_key,
    _canon,
    _sha256,
)

OWNER = "12345678-1234-1234-1234-123456789abc"
KERNEL_SHA = "123fc98ed86daccf8364a419bece89566b6d6ecc"
PARENT = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def make_receipt(decision_id="dec-001", verdict="PASS", tamper=False,
                 with_inputs=False, inputs_state=None, **overrides):
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
        "candidate_banner": "CANDIDATE",
    }
    if with_inputs:
        state = inputs_state if inputs_state is not None else {"gates": {"SELF": {}}}
        body["inputs_hash"] = _sha256(state)
    body.update(overrides)
    # Seal LAST so overrides are covered — models a resealed receipt.
    # An explicit receipt_hash override is respected (models a presented
    # seal, valid or not); otherwise the body is sealed here.
    if "receipt_hash" not in overrides:
        body["receipt_hash"] = _sha256({k: v for k, v in body.items()
                                        if k != "receipt_hash"})
    if tamper:
        body["verdict"] = "FAIL"  # mutate after hashing
    return body


def expect_value_error(fn, label):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(f"expected ValueError for {label}")


def proj(r, **kw):
    kw.setdefault("owner_id", OWNER)
    kw.setdefault("kernel_sha", KERNEL_SHA)
    return project_kernel_receipt(r, **kw)


def test_1_valid_payload():
    r = make_receipt()
    p = proj(r)
    assert p["p_owner_id"] == OWNER
    assert p["p_source_table"] == "naya_kernel_decision"
    assert p["p_source_id"] == "dec-001"
    assert p["p_event_at"] == "2026-10-01T15:30:00+00:00"  # kernel's own issued_at
    assert p["p_verification"]["state"] == "UNVERIFIED"
    assert p["p_outcome"] == {}
    assert p["p_metadata"]["kernel_sha"] == KERNEL_SHA
    assert p["p_metadata"]["node_id"] == "naya-node-0001"
    assert p["p_metadata"]["input_commitment"] == "absent-legacy"
    assert "received_at" in p["p_metadata"]
    assert p["p_value"]["receipt_hash"] == r["receipt_hash"]  # verbatim evidence


def test_2_missing_metadata():
    r = make_receipt()
    del r["receipt_hash"]
    expect_value_error(lambda: proj(r), "missing receipt_hash")
    r2 = make_receipt()
    del r2["decision_id"]
    expect_value_error(lambda: proj(r2), "missing decision_id")


def test_3_invalid_types():
    r = make_receipt()
    expect_value_error(lambda: proj(r, owner_id="not-a-uuid"), "owner_id not uuid")
    expect_value_error(lambda: proj(r, owner_scope="EVERYONE"), "owner_scope invalid")


def test_4_hash_mismatch():
    r = make_receipt(tamper=True)
    assert verify_kernel_receipt(r)["result"] == "MISMATCH"
    expect_value_error(lambda: proj(r), "tampered receipt")


def test_5_source_config_shape():
    r = make_receipt()
    expect_value_error(lambda: proj(r, kernel_sha="xyz"), "kernel_sha not 40-hex")
    # A well-formed but arbitrary SHA is ACCEPTED as a label — the adapter
    # cannot establish provenance from JSON. Callers must bind real context.
    p = proj(r, kernel_sha="a" * 40)
    assert p["p_metadata"]["kernel_sha"] == "a" * 40
    expect_value_error(lambda: proj(r, config_hash="  "), "config_hash blank")


def test_6_ownership_shape():
    # Shape only — isolation is a database property, not proven here.
    r = make_receipt()
    expect_value_error(lambda: proj(r, owner_id=None), "owner_id null")
    expect_value_error(lambda: proj(r, owner_id=""), "owner_id empty")


def test_7_no_verified_at_insert():
    r = make_receipt(verdict="PASS")
    r["verification"] = {"state": "VERIFIED_PASS"}
    r["receipt_hash"] = _sha256({k: v for k, v in r.items() if k != "receipt_hash"})
    p = proj(r)
    assert p["p_verification"]["state"] == "UNVERIFIED"
    assert p["p_outcome"] == {}


def test_8_parent_shape():
    r = make_receipt()
    expect_value_error(lambda: proj(r, parent_ledger_event_id="nope"),
                       "parent not uuid")


def test_9_lineage_threading():
    r = make_receipt()
    p = proj(r, parent_ledger_event_id=PARENT)
    assert p["p_parent_ledger_event_id"] == PARENT
    p2 = proj(r)
    assert p2["p_parent_ledger_event_id"] is None


def test_10_idempotency_key_shape():
    k1 = idempotency_key(OWNER, "dec-001")
    k2 = idempotency_key(OWNER, "dec-001")
    k3 = idempotency_key(OWNER, "dec-002")
    assert k1 == k2 and k1 != k3
    assert k1 == f"{OWNER}|naya_kernel_decision|dec-001"


def test_11_seal_validation():
    # RED-1: numeric receipt_hash was accepted because the verifier only ran
    # for strings. Now every unverified hash is rejected.
    expect_value_error(lambda: proj(make_receipt(receipt_hash=123)),
                       "numeric receipt_hash")
    expect_value_error(lambda: proj(make_receipt(receipt_hash=None)),
                       "null receipt_hash")
    expect_value_error(lambda: proj(make_receipt(receipt_hash="not-hex")),
                       "malformed receipt_hash")
    expect_value_error(lambda: proj(make_receipt(receipt_hash="ab" * 32)),
                       "wrong-length receipt_hash")
    # Valid shape but wrong value: rejected by recomputation.
    r = make_receipt()
    r["receipt_hash"] = "00" * 32
    expect_value_error(lambda: proj(r), "mismatched receipt_hash")


def test_12_receipt_vocabulary():
    # RED-2/3/4: resealed but meaningless receipts were accepted.
    expect_value_error(lambda: proj(make_receipt(verdict="BOGUS")),
                       "bogus verdict")
    expect_value_error(lambda: proj(make_receipt(verdict=123)),
                       "numeric verdict")
    expect_value_error(lambda: proj(make_receipt(issued_at="banana")),
                       "banana timestamp")
    expect_value_error(lambda: proj(make_receipt(issued_at="2026-13-99")),
                       "impossible timestamp")
    expect_value_error(lambda: proj(make_receipt(decision_id=123)),
                       "numeric decision_id")
    expect_value_error(lambda: proj(make_receipt(receipt_id="")),
                       "empty receipt_id")
    # Canonical vocabulary still passes, including NEED_EVIDENCE.
    for v in ("PASS", "FAIL", "NEED_EVIDENCE"):
        p = proj(make_receipt(verdict=v))
        assert p["p_value"]["verdict"] == v


def test_13_input_commitment():
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    p = proj(r, inputs_state=state)
    assert p["p_value"]["inputs_hash"] == _sha256(state)
    assert p["p_metadata"]["input_commitment"] == "recomputed-match"
    expect_value_error(
        lambda: proj(r, inputs_state={"gates": {"SELF": {"input": 2}}}),
        "inputs_hash mismatch")
    expect_value_error(lambda: proj(r), "inputs_hash without submitted state")
    # Malformed inputs_hash is rejected, not silently treated as legacy.
    r2 = make_receipt(with_inputs=True, inputs_state=state)
    r2["inputs_hash"] = "zzz"
    r2["receipt_hash"] = _sha256({k: v for k, v in r2.items()
                                  if k != "receipt_hash"})
    expect_value_error(lambda: proj(r2, inputs_state=state),
                       "malformed inputs_hash")


def test_14_interop_real_kernel_receipt():
    # Naya 4's seam-verify-001, produced by Kernel.decide() at 4e87d4a,
    # posted on #554 (5934951319). The adapter's independent verification
    # must MATCH the producer's seal — same canonicalization, no shared code.
    r = json.loads((FIXTURES / "seam-verify-001.json").read_text())
    assert verify_kernel_receipt(r)["result"] == "MATCH"
    # Full projection still refuses without the input state (by design).
    expect_value_error(lambda: proj(r), "inputs_hash without state")


def test_15_inputs_state_preserved_for_cold_recompute():
    # Cold-successor closure: the exact evaluated input state must survive
    # in the projection so a fresh consumer can independently recompute
    # inputs_hash from the retrieved row alone.
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    p = proj(r, inputs_state=state)
    assert p["p_metadata"]["inputs_state"] == state
    # The cold consumer's recomputation path, from the row only:
    cold_state = p["p_metadata"]["inputs_state"]
    assert _sha256(cold_state) == p["p_value"]["inputs_hash"]
    assert verify_kernel_receipt(p["p_value"])["result"] == "MATCH"
    # Legacy receipts (no inputs_hash) carry no state key at all.
    p2 = proj(make_receipt())
    assert "inputs_state" not in p2["p_metadata"]


def test_contract_record_validation():
    good = {
        "object_id": PARENT, "owner_id": OWNER, "owner_scope": "PRIVATE",
        "created_at": "2026-10-01T15:30:00+00:00", "updated_at": "2026-10-01T15:30:00+00:00",
        "schema_version": "1.0.0",
        "provenance": {"source_table": "naya_kernel_decision",
                       "source_id": "dec-001"},
        "truth_state": "UNASSESSED", "status": "RECORDED", "superseded_by": None,
        "lineage": {"parent_ledger_event_id": None, "chain_seq": 1}, "content_hash": "a" * 64,
    }
    assert validate_contract_record(good) == []
    bad = dict(good)
    del bad["owner_id"]
    assert any("owner_id" in x for x in validate_contract_record(bad))
    bad2 = dict(good, content_hash="zzz")
    assert any("content_hash" in x for x in validate_contract_record(bad2))


# ---------------------------------------------------------------------------
# RED-2: snapshot aliasing (coordinator-reproduced, 2026-10-01).
# The projection must preserve DETACHED snapshots: caller mutation after
# projection must not alter already-validated projected evidence.
# ---------------------------------------------------------------------------

def test_projection_detaches_inputs_state():
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    p = proj(r, inputs_state=state)
    # Caller mutates the input state AFTER projection.
    state["gates"]["SELF"]["input"] = 999
    state["new_key"] = "injected"
    snap = p["p_metadata"]["inputs_state"]
    assert snap == {"gates": {"SELF": {"input": 1}}}, \
        f"projected inputs_state aliased caller mutation: {snap}"
    # The preserved snapshot still reproduces the kernel's claimed hash.
    assert _sha256(snap) == p["p_value"]["inputs_hash"]


def test_projection_detaches_receipt_nested():
    r = make_receipt(with_inputs=True, inputs_state={"a": 1})
    p = proj(r, inputs_state={"a": 1})
    # Caller mutates NESTED receipt content AFTER projection.
    r["gates"].append({"forged": True})
    r["evaluation_order"].append("FORGED")
    assert verify_kernel_receipt(p["p_value"])["result"] == "MATCH", \
        "projected p_value aliased caller mutation (seal broken)"
    assert p["p_value"]["gates"] == []
    assert p["p_value"]["evaluation_order"] == ["SELF", "LAW"]


def test_projection_mutation_does_not_alter_producer_evidence():
    state = {"gates": {"SELF": {"input": 1}}}
    r = make_receipt(with_inputs=True, inputs_state=state)
    before_receipt = _canon(r)
    before_state = _canon(state)
    p = proj(r, inputs_state=state)
    # Mutating the RETURNED projection must not reach back into the
    # caller's objects.
    p["p_value"]["gates"].append({"x": 1})
    p["p_metadata"]["inputs_state"]["gates"]["SELF"]["input"] = 2
    assert _canon(r) == before_receipt
    assert _canon(state) == before_state


def test_projection_rejects_non_json_inputs_state():
    r = make_receipt(with_inputs=True, inputs_state={"a": 1})
    # NaN is not valid JSON; a set is not JSON-native at all.
    for bad in ({"v": float("nan")}, {"v": {1, 2}}):
        try:
            proj(r, inputs_state=bad)
        except ValueError as e:
            assert "JSON" in str(e) or "snapshot" in str(e), str(e)
        else:
            raise AssertionError(f"non-JSON inputs_state accepted: {bad!r}")


# ---------------------------------------------------------------------------
# RED-3: substantive contract-record validation (coordinator-reproduced).
# validate_contract_record() must check field MEANINGS, not just presence.
# ---------------------------------------------------------------------------

def _good_record(**overrides):
    rec = {
        "object_id": PARENT, "owner_id": OWNER, "owner_scope": "PRIVATE",
        "created_at": "2026-10-01T15:30:00+00:00",
        "updated_at": "2026-10-01T15:30:00+00:00",
        "schema_version": "1.0.0",
        "provenance": {"source_table": "naya_kernel_decision",
                       "source_id": "dec-001"},
        "truth_state": "UNASSESSED", "status": "RECORDED",
        "superseded_by": None,
        "lineage": {"parent_ledger_event_id": None, "chain_seq": 1},
        "content_hash": "a" * 64,
    }
    rec.update(overrides)
    return rec


def test_contract_record_rejects_coordinator_repro():
    # The exact record the coordinator supplied: every bad field must be
    # flagged. Previously this returned [].
    bad = _good_record(
        created_at="banana",
        updated_at=[],
        schema_version=123,
        truth_state="MADE_UP",
        status="MADE_UP",
        superseded_by="not-a-uuid",
    )
    vs = validate_contract_record(bad)
    for field in ("created_at", "updated_at", "schema_version",
                  "truth_state", "status", "superseded_by"):
        assert any(field in x for x in vs), \
            f"no violation for {field}: {vs}"
    assert validate_contract_record(_good_record()) == []


def test_contract_record_timestamp_boundary():
    # Date-only is not a timestamp; naive (tz-less) is not the producer's
    # contract (kernel emits tz-aware; ledger stores timestamptz).
    for bad_ts in ("2026-10-01", "2026-10-01T15:30:00", "", None, 12345):
        vs = validate_contract_record(_good_record(created_at=bad_ts))
        assert any("created_at" in x for x in vs), \
            f"created_at={bad_ts!r} accepted: {vs}"
    # issued_at boundary: the adapter's own timestamp parser must agree.
    r = make_receipt()
    r["issued_at"] = "2026-10-01"  # date-only
    r["receipt_hash"] = _sha256({k: v for k, v in r.items()
                                 if k != "receipt_hash"})
    try:
        proj(r)
    except ValueError as e:
        assert "issued_at" in str(e)
    else:
        raise AssertionError("date-only issued_at accepted by adapter")


def test_contract_record_vocabularies():
    # status: the V1 migration's check-constraint vocabulary.
    for bad in ("MADE_UP", "PENDING", "", None):
        vs = validate_contract_record(_good_record(status=bad))
        assert any("status" in x for x in vs), f"status={bad!r}: {vs}"
    for good_status in ("RECORDED", "VERIFIED", "QUALIFIED",
                        "SUPERSEDED", "BLOCKED", "FAILED"):
        assert validate_contract_record(
            _good_record(status=good_status)) == [], good_status
    # truth_state: the V2.1 assessment vocabulary (the ledger's native
    # truth/assessment states).
    for bad in ("MADE_UP", "CANDIDATE", "", None):
        vs = validate_contract_record(_good_record(truth_state=bad))
        assert any("truth_state" in x for x in vs), \
            f"truth_state={bad!r}: {vs}"
    for good_ts in ("UNASSESSED", "ASSESSED", "VERIFIED_VALUE", "REJECTED"):
        assert validate_contract_record(
            _good_record(truth_state=good_ts)) == [], good_ts


def test_contract_record_lineage_and_provenance():
    vs = validate_contract_record(_good_record(
        lineage={"parent_ledger_event_id": "not-a-uuid", "chain_seq": "x"}))
    assert any("lineage" in x for x in vs), vs
    vs = validate_contract_record(_good_record(provenance={"node_id": "x"}))
    assert any("provenance" in x for x in vs), vs
    # Valid parent linkage passes.
    ok = _good_record(lineage={"parent_ledger_event_id": PARENT,
                               "chain_seq": 7})
    assert validate_contract_record(ok) == []
