"""VERIFY→LEARN trust seam — adversarial qualification (Coda 1 verdict #554/5937954809).

Failure-first tests for the fail-closed intake boundary (C1–C6). Every test
here PROVES a refusal; the positive path proves genuine VERIFY receipts
traverse with no fixture privilege.

Test map (Coda 1's required list):
  unknown ID · fabricated object · genuine ID + altered payload ·
  valid receipt for another task · valid receipt for another owner/scope ·
  non-VERIFIED result · self-certified · missing resolver ·
  caller supplying its own resolver · fixture mode off by default ·
  superseded/reopened receipt · C6 direct-write case · positive path.

SECURITY INVARIANT under test: LEARN can consume verification. It can never
create, infer, or manufacture it — including when the caller asserts the
object came from VERIFY.
"""
import copy
import inspect

import pytest

from naya_kernel.nodes.learn_node import LearnNode
from naya_kernel.nodes.verify_node import VerifyNode


# ---------------------------------------------------------------------------
# Helpers: genuine VERIFY receipts (no fixtures — the real VerifyNode)
# ---------------------------------------------------------------------------

def _submit(v, verify_key, task="triage-task", owner="owner-1"):
    return v.submit({
        "verify_key": verify_key,
        "kind": "claim_baton",
        "subject": {
            "claim": "provenance-check-before-summary",
            "epistemic_state": "observed",
            "evidence": ["ev1"],
            "provenance": "test-provenance",
            "scope": {"task_classes": ["triage"], "owner": owner, "task": task},
            "limitations": [],
            "gaps": [],
        },
        "evidence_refs": [{"address": "ev1", "retrievable": True,
                           "class": "REFERENCE"}],
        "deciding_seat": {"identity": "deciding-seat"},
        "requesting_owner": owner,
    })["receipt"]


def _drive_to_pass(v, receipt):
    rid = receipt["id"]
    v.record_reproduction(
        rid, mode="RECOMPUTE",
        reproducer_seat={"identity": "repro-seat"},
        achieved_dims=["different_seat_identity"],
        result="MATCH")
    v.run_tier1(rid, battery={
        "recompute_match": True,
        "evidence_ref_integrity": True,
        "gate_conformance": True,
        "negation_probes": [{"probe": "neg1", "passed": False,
                             "expected": "fail"}],
    })
    return v.close(rid, outcome_status="SUCCESS",
                   acceptance_decision="ACCEPTED",
                   causal_status="NOT_CLAIMED",
                   target_state="VERIFIED_PASS")


def _genuine_pass(v, verify_key, task="triage-task", owner="owner-1"):
    return _drive_to_pass(v, _submit(v, verify_key, task=task, owner=owner))


@pytest.fixture
def verify():
    return VerifyNode()


@pytest.fixture
def wired():
    """A (VerifyNode, LearnNode) pair wired through the reference resolver,
    with NO fixture privilege — the production-shaped configuration."""
    v = VerifyNode()
    n = LearnNode(verify_resolver=LearnNode.reference_resolver(v))
    return v, n


# ---------------------------------------------------------------------------
# 1. Unknown ID
# ---------------------------------------------------------------------------

def test_unknown_id_refused(wired):
    v, n = wired
    result = n.ingest_verify_receipt({
        "id": "vr-0000000000000000",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_UNKNOWN"


# ---------------------------------------------------------------------------
# 2. Fabricated object (the original Coda 1 finding)
# ---------------------------------------------------------------------------

def test_fabricated_object_refused():
    node = LearnNode()  # fail-closed default: no resolver, no fixture
    result = node.ingest_verify_receipt({
        "receipt_id": "forged-1",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED"


# ---------------------------------------------------------------------------
# 3. Genuine ID + altered payload (C3 tamper detection)
# ---------------------------------------------------------------------------

def test_genuine_id_altered_payload_refused(wired):
    v, n = wired
    genuine = _genuine_pass(v, "tamper-001")
    presented = copy.deepcopy(genuine)
    presented["acceptance_decision"] = "PENDING"  # alter one allowlisted field
    result = n.ingest_verify_receipt(presented)
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_TAMPERED"
    # Zero candidate extraction after refusal.
    assert genuine["id"] not in n._verify_receipts


# ---------------------------------------------------------------------------
# 4 & 5. Genuine receipt redirected to another task / owner (C4 via C3)
# ---------------------------------------------------------------------------

def test_genuine_receipt_for_another_task_refused(wired):
    """A genuine receipt for task-A cannot be redirected to task-B by
    presenting an altered copy: subject_ref is allowlisted (C3), so the
    mismatch is tampering; the stored receipt (C1) keeps the true binding."""
    v, n = wired
    genuine = _genuine_pass(v, "task-redirect-001", task="task-A", owner="owner-1")
    presented = copy.deepcopy(genuine)
    presented["subject_ref"] = copy.deepcopy(genuine["subject_ref"])
    presented["subject_ref"]["scope"]["task"] = "task-B"  # redirect!
    result = n.ingest_verify_receipt(presented)
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_TAMPERED"


def test_genuine_receipt_for_another_owner_refused(wired):
    v, n = wired
    genuine = _genuine_pass(v, "owner-redirect-001", task="task-A", owner="owner-1")
    presented = copy.deepcopy(genuine)
    presented["subject_ref"] = copy.deepcopy(genuine["subject_ref"])
    presented["subject_ref"]["scope"]["owner"] = "owner-2"  # redirect!
    result = n.ingest_verify_receipt(presented)
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_TAMPERED"


# ---------------------------------------------------------------------------
# 6. Non-VERIFIED result
# ---------------------------------------------------------------------------

def test_non_verified_result_refused(wired):
    v, n = wired
    receipt = _submit(v, "fail-001")
    rid = receipt["id"]
    v.classify_failure(rid, "EVIDENCE_GAP", evidence={"note": "test"})
    failed = v.close(rid, outcome_status="FAILURE",
                     acceptance_decision="REJECTED",
                     causal_status="NOT_CLAIMED", target_state="FAIL")
    assert failed["verification_state"] != "VERIFIED_PASS"
    result = n.ingest_verify_receipt(copy.deepcopy(failed))
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RESULT_REQUIRED"


# ---------------------------------------------------------------------------
# 7. Self-certified (LEARN's own receipt presented as VERIFY's)
# ---------------------------------------------------------------------------

def test_self_certified_refused(wired):
    """A receipt LEARN emitted itself cannot be laundered through intake:
    the VERIFY store has no such id."""
    v, n = wired
    own = n._emit("INTAKE_ACCEPTED", receipt_id_ref="x", reason="test")
    result = n.ingest_verify_receipt({
        "id": own["receipt_id"],
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_UNKNOWN"


# ---------------------------------------------------------------------------
# 8. Missing resolver
# ---------------------------------------------------------------------------

def test_missing_resolver_refused():
    node = LearnNode()  # no resolver, no fixture privilege
    result = node.ingest_verify_receipt({
        "receipt_id": "vr-aaaaaaaaaaaaaaaa",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED"
    assert node._verify_resolver is None


# ---------------------------------------------------------------------------
# 9. Caller supplying its own resolver (C2)
# ---------------------------------------------------------------------------

def test_caller_supplied_resolver_ignored(wired):
    """The resolver is construction-owned. A 'resolver' key smuggled in the
    event payload is ignored; ingest_verify_receipt takes no resolver
    parameter at all."""
    v, n = wired
    genuine = _genuine_pass(v, "smuggle-001")

    evil_calls = []

    def evil_resolver(rid):
        evil_calls.append(rid)
        return {"id": rid, "node_id": "NAYA-KERNEL-VERIFY",
                "verification_state": "VERIFIED_PASS"}

    presented = copy.deepcopy(genuine)
    presented["resolver"] = evil_resolver
    presented["verify_resolver"] = evil_resolver

    # Signature check: no resolver parameter exists to smuggle through.
    sig = inspect.signature(n.ingest_verify_receipt)
    assert list(sig.parameters) == ["receipt"], (
        f"C2 violated: ingest_verify_receipt takes {list(sig.parameters)}")

    result = n.ingest_verify_receipt(presented)
    assert result["accepted"] is True  # genuine receipt, real resolver used
    assert evil_calls == [], "smuggled resolver was invoked — C2 violated"


# ---------------------------------------------------------------------------
# 10. Fixture mode off by default, not flippable after construction (C5)
# ---------------------------------------------------------------------------

def test_fixture_mode_off_by_default():
    node = LearnNode()
    assert node._allow_fixture_intake is False
    assert node._verify_resolver is None
    # A fully qualifying synthetic receipt is still refused.
    result = node.ingest_verify_receipt({
        "receipt_id": "fixture-default-001",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED"


def test_fixture_mode_not_flippable_after_construction():
    node = LearnNode()
    # No public API exists to enable fixture intake or install a resolver
    # after construction.
    for name in ("enable_fixture_intake", "set_fixture_intake",
                 "set_verify_resolver", "install_resolver"):
        assert not hasattr(node, name), f"C5 violated: {name} exists"
    # The explicit constructor opt-in is the only path.
    fixture_node = LearnNode(allow_fixture_intake=True)
    result = fixture_node.ingest_verify_receipt({
        "receipt_id": "fixture-explicit-001",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    })
    assert result["accepted"] is True
    assert result.get("fixture") is True


def test_register_verify_receipt_gated():
    """The public fixture seam refuses without explicit opt-in."""
    node = LearnNode()
    with pytest.raises(ValueError, match="VERIFY_ORIGIN_UNESTABLISHED"):
        node.register_verify_receipt({"receipt_id": "x"})
    fixture_node = LearnNode(allow_fixture_intake=True)
    out = fixture_node.register_verify_receipt({
        "receipt_id": "y", "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS"})
    assert out["registered"] == "y"


# ---------------------------------------------------------------------------
# 11. Superseded / reopened receipts (C4)
# ---------------------------------------------------------------------------

def test_superseded_receipt_refused(wired):
    v, n = wired
    genuine = _genuine_pass(v, "supersede-001")
    rid = genuine["id"]
    # A correction creates a newer receipt; the old one is no longer current.
    v.correct(rid, {"note": "test correction"})
    result = n.ingest_verify_receipt(copy.deepcopy(genuine))
    assert result["accepted"] is False
    # The reference resolver filters superseded ids → unknown to LEARN.
    assert result["reason_code"] == "VERIFY_RECEIPT_UNKNOWN"


def test_reopened_receipt_refused(wired):
    v, n = wired
    genuine = _genuine_pass(v, "reopen-001")
    rid = genuine["id"]
    v.reopen(rid, "test re-examination")
    assert v._receipts[rid]["verification_state"] == "REOPENED"
    result = n.ingest_verify_receipt(copy.deepcopy(v._receipts[rid]))
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_REOPENED"


# ---------------------------------------------------------------------------
# 12. C6 direct-write case (Coda 1's proven counterexample)
# ---------------------------------------------------------------------------

def test_direct_write_forgery_refused(wired):
    """delete_receipt raises but v._receipts['attacker-1'] = {...} SUCCEEDS.
    The resolver returns what the store holds; C6's ownership proof refuses
    it with VERIFY_ORIGIN_UNESTABLISHED — the counterexample becomes a
    refusal, not an exploit."""
    v, n = wired
    forged = {"id": "attacker-1",
              "node_id": "NAYA-KERNEL-VERIFY",
              "verification_state": "VERIFIED_PASS",
              "outcome_status": "SUCCESS",
              "acceptance_decision": "ACCEPTED"}
    v._receipts["attacker-1"] = forged
    try:
        result = n.ingest_verify_receipt(dict(forged))
        assert result["accepted"] is False
        assert result["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED"
        assert "attacker-1" not in n._verify_receipts
    finally:
        del v._receipts["attacker-1"]


def test_valid_format_forgery_missing_structure_refused(wired):
    """A forgery with a valid-format id but incomplete VERIFY structure
    is still refused by the C6 ownership proof."""
    v, n = wired
    forged = {"id": "vr-abcdef0123456789",
              "node_id": "NAYA-KERNEL-VERIFY",
              "verification_state": "VERIFIED_PASS"}
    v._receipts["vr-abcdef0123456789"] = forged
    try:
        result = n.ingest_verify_receipt(dict(forged))
        assert result["accepted"] is False
        assert result["reason_code"] == "VERIFY_ORIGIN_UNESTABLISHED"
    finally:
        del v._receipts["vr-abcdef0123456789"]


# ---------------------------------------------------------------------------
# 13. Positive path: genuine receipt, no fixture privilege (C1)
# ---------------------------------------------------------------------------

def test_positive_path_genuine_receipt_accepted(wired):
    v, n = wired
    assert n._allow_fixture_intake is False  # no fixture privilege
    genuine = _genuine_pass(v, "positive-001")
    rid = genuine["id"]
    result = n.ingest_verify_receipt(copy.deepcopy(genuine))
    assert result["accepted"] is True
    assert result.get("fixture") is not True
    # C1: LEARN stored the RESOLVED receipt — the store's object, not the
    # caller's presented copy.
    assert n._verify_receipts[rid] is v._receipts[rid]


def test_c1_caller_object_never_consumed(wired):
    """Extra caller-supplied fields outside the allowlist are ignored, and
    the stored receipt is byte-identical to VERIFY's — the caller's object
    is compared only to detect tampering, never read for the decision."""
    v, n = wired
    genuine = _genuine_pass(v, "c1-001")
    rid = genuine["id"]
    presented = copy.deepcopy(genuine)
    presented["caller_note"] = "not part of VERIFY emission"
    presented["owner_id"] = "spoofed-owner"  # outside the allowlist
    result = n.ingest_verify_receipt(presented)
    assert result["accepted"] is True
    stored = n._verify_receipts[rid]
    assert stored is v._receipts[rid]
    assert "caller_note" not in stored
    assert stored.get("subject_ref") == genuine["subject_ref"]


def test_duplicate_intake_still_idempotent(wired):
    v, n = wired
    genuine = _genuine_pass(v, "dup-001")
    rid = genuine["id"]
    first = n.ingest_verify_receipt(copy.deepcopy(genuine))
    assert first["accepted"] is True
    second = n.ingest_verify_receipt(copy.deepcopy(genuine))
    assert second["accepted"] is False
    assert second["duplicate"] is True
