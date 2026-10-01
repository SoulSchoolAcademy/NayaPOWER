"""No-fixture nine-organ cycle: plain Kernel() through real public seams.

FAILURE-FIRST composition proof for the current-head directive
(2026-10-01). Every organ output that feeds a downstream organ is produced
by that organ's own public methods — no hand-constructed VERIFY receipts,
no caller-supplied LEARN evidence, no invented CONNECT output.

Chain under proof:
  plain Kernel()
    -> CONNECT.propose()           (real public output)
    -> VERIFY.submit/record/run_tier1/close  (genuine receipt, public lifecycle)
    -> LEARN.ingest_verify_receipt (by reference, kernel-wired resolver)
    -> LEARN promotion pipeline    (real learning from the genuine receipt)
    -> EVOLVE.observe()            (real learning state, public seam)
    -> Kernel.decide()             (all nine gates; VERIFY/LEARN gates
                                    resolve the real receipt/learning from
                                    their own stores)
    -> decision receipt with full edge trace

Stop condition: the first exact failing handoff is reported, not patched
around. A fixture substitution anywhere in the chain voids the proof.
"""
import copy

import pytest

from naya_kernel.kernel import Kernel, verify_decision_receipt
from naya_kernel.node_base import GateVerdict


T0 = "2026-10-01T12:00:00+00:00"
OWNER = "owner-1"
TASK = "triage-task"


def _genuine_verify_receipt(verify, verify_key, connect_proposal_id):
    """Drive one genuine VERIFY receipt through the public lifecycle.

    The claim under verification references CONNECT's real proposal output,
    so CONNECT's public output is contextual input to the VERIFY chain.
    """
    out = verify.submit({
        "verify_key": verify_key,
        "kind": "claim_baton",
        "subject": {
            "claim": "provenance-check-before-summary",
            "epistemic_state": "observed",
            "evidence": ["ev1"],
            "provenance": "test-provenance",
            "scope": {"task_classes": ["triage"], "owner": OWNER,
                      "task": TASK},
            "limitations": [],
            "gaps": [],
            # CONNECT's real output as downstream context:
            "connection_context": {"proposal_id": connect_proposal_id},
        },
        "evidence_refs": [{"address": "ev1", "retrievable": True,
                           "class": "REFERENCE"}],
        "deciding_seat": {"identity": "deciding-seat"},
        "requesting_owner": OWNER,
        "now": T0,
    })
    assert not out.get("refused"), out
    receipt = out["receipt"]
    rid = receipt["id"]
    verify.record_reproduction(
        rid, mode="RECOMPUTE",
        reproducer_seat={"identity": "repro-seat"},
        achieved_dims=["different_seat_identity"],
        result="MATCH", now=T0)
    verify.run_tier1(rid, battery={
        "recompute_match": True,
        "evidence_ref_integrity": True,
        "gate_conformance": True,
        "negation_probes": [{"probe": "neg1", "passed": False,
                             "expected": "fail"}],
    }, now=T0)
    verify.close(rid, outcome_status="SUCCESS",
                 acceptance_decision="ACCEPTED",
                 causal_status="NOT_CLAIMED",
                 target_state="VERIFIED_PASS", now=T0)
    genuine = verify._receipts[rid]
    assert genuine["verification_state"] == "VERIFIED_PASS"
    assert genuine["sealed"] is True
    return genuine


def _promotable_learning_from_genuine(learn, genuine_receipt):
    """Ingest the genuine receipt by reference; attempt the real LEARN
    pipeline (extract -> reconcile -> holdout -> evidence).

    CURRENT-HEAD FINDING (2026-10-01): this STOPS at extract(). A genuine
    VERIFY receipt from the public lifecycle carries no `outcome.lesson`
    or `claimed_lesson` — VERIFY's submit/record/run_tier1/close never
    produces one. LEARN.extract() requires one. Only hand-constructed
    fixture receipts satisfy extract(). This is the first exact failing
    handoff in the no-fixture chain; per the directive, the cycle stops
    here rather than inventing lesson-derivation semantics.
    """
    presented = copy.deepcopy(genuine_receipt)
    res = learn.ingest_verify_receipt(presented)
    assert res["accepted"], res
    rid = genuine_receipt["id"]

    # The intake (VERIFY->LEARN trust seam) works with genuine receipts.
    # Extraction is the failing handoff — documented, not patched.
    with pytest.raises(ValueError, match="no lesson extractable"):
        learn.extract([rid])
    return None


def test_no_fixture_chain_to_first_failing_handoff():
    """Plain Kernel(): real CONNECT output -> genuine VERIFY receipt ->
    trusted LEARN intake (by reference). Documents the exact stopping
    point: LEARN.extract() refuses genuine receipts (no lesson field).

    What this PROVES:
    - plain Kernel() wires VERIFY->LEARN via the construction-owned
      resolver (no fixture, no caller-supplied resolver)
    - CONNECT.propose() produces real output used as VERIFY context
    - VERIFY's public lifecycle produces a genuine sealed VERIFIED_PASS
      receipt
    - LEARN.ingest_verify_receipt consumes it by reference (C1-C6 intact)

    Where it STOPS (first exact failing handoff):
    - LEARN.extract() on the genuine receipt -> ValueError: no lesson
      extractable. VERIFY's lifecycle never emits outcome.lesson.
    """
    k = Kernel()

    # -- CONNECT: real public output ------------------------------------
    connect = k.nodes["CONNECT"]
    bindings = {"seat-A": {"authenticated": True,
                           "owner_scope": "owner-1-scope",
                           "binding_ref": "b-seat-A"}}
    consent_body = {"consent_id": "consent-cycle", "party": "seat-A",
                    "purpose": "research", "scope": ["reports", "facts"],
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "revoked": False, "revocable": True}
    from naya_kernel.nodes import connect_node as _cn
    consent_body["consent_hash"] = _cn._sha256(
        {kk: vv for kk, vv in consent_body.items()
         if kk != "consent_hash"})
    conn_request = {
        "id": "conn-cycle-001", "kind": "GRAPH_EDGE",
        "parties": [{"identity": "seat-A", "owner_scope": "owner-1-scope",
                     "role": "peer"}],
        "purpose": "research",
        "scope": [{"owner_scope": "owner-1-scope",
                   "content_classes": ["reports"]}],
        "consentRefs": ["consent-cycle"], "evidenceRefs": ["ev-conn-1"],
        "boundaryPolicy": {"version": "v1", "forbidden_classes": [],
                           "strictness": 1},
        "expiresAt": None, "reversibility": 8.0, "consentLadder": "SHARED"}
    proposal = connect.propose(
        conn_request,
        context={"consent_registry": {"consent-cycle": consent_body},
                 "identity_bindings": copy.deepcopy(bindings),
                 "evidence_registry": {"ev-conn-1": {"content_hash": "abc123",
                                                    "valid": True}},
                 "boundary_policy": {"version": "v1",
                                      "forbidden_classes": [],
                                      "strictness": 1},
                 "now": T0})
    assert proposal.get("verdict") == "ACTIVE", proposal
    connect_proposal_id = "conn-cycle-001"

    # -- VERIFY: genuine receipt through the public lifecycle ------------
    verify = k.nodes["VERIFY"]
    genuine = _genuine_verify_receipt(verify, "vk-cycle-001",
                                      connect_proposal_id)

    # -- LEARN: consume by reference (kernel-wired resolver) ------------
    learn = k.nodes["LEARN"]
    assert learn._verify_resolver is not None
    assert learn._allow_fixture_intake is False
    # Proves intake works; documents the extract stop. Returns None.
    assert _promotable_learning_from_genuine(learn, genuine) is None

    # -- STOP: first exact failing handoff -------------------------------
    # LEARN.extract() cannot produce learning state from a genuine VERIFY
    # receipt (no outcome.lesson). Therefore there is no learning state to
    # feed EVOLVE, and no nine-gate decide() with real LEARN/EVOLVE outputs.
    # The chain up to LEARN intake is PROVEN; LEARN->EVOLVE is BLOCKED on
    # the extract gap. This test documents the boundary honestly.


def test_cycle_negative_forged_receipt_still_refused():
    """The no-fixture chain preserves the adversarial boundary: a forged
    receipt presented to the kernel-wired LEARN is refused."""
    k = Kernel()
    learn = k.nodes["LEARN"]
    forged = {
        "receipt_id": "forged-cycle-001",
        "id": "forged-cycle-001",
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
    }
    result = learn.ingest_verify_receipt(forged)
    assert result["accepted"] is False
    assert result["reason_code"] == "VERIFY_RECEIPT_UNKNOWN"


def test_cycle_negative_unknown_receipt_id_gate():
    """VERIFY's gate fails closed on an unknown receipt id."""
    k = Kernel()
    out = k.nodes["VERIFY"].gate({"receipt_id": "vr-does-not-exist"})
    assert out.verdict == GateVerdict.NEED_EVIDENCE
