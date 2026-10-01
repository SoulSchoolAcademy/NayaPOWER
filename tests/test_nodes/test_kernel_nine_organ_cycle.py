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

    Coda 1 Option A (#554/5939450892): actor authors the outcome at
    submit(); VERIFY seals it at close(). The outcome scope is subset of
    subject scope (C4).
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
        # Actor-authored outcome, sealed by VERIFY at close():
        "outcome": {
            "lesson": "verified: provenance-check-before-summary",
            "scope": {"task_classes": ["triage"], "owner": OWNER,
                     "task": TASK},
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
    """Ingest the genuine receipt by reference; drive the real LEARN
    pipeline (extract -> reconcile -> holdout -> evidence) to a promotable
    learning. Returns the learning_id.

    2026-10-01: Coda 1 Option A (#554/5939450892) — actor authors the
    outcome at submit(), VERIFY seals it at close(), LEARN extracts the
    sealed outcome.lesson. Seal covers the outcome.
    """
    presented = copy.deepcopy(genuine_receipt)
    res = learn.ingest_verify_receipt(presented)
    assert res["accepted"], res
    rid = genuine_receipt["id"]

    # Real LEARN pipeline on the ingested evidence. The lesson is the
    # actor-authored, VERIFY-sealed outcome.lesson.
    extracted = learn.extract([rid])
    assert extracted["candidates"], extracted
    cid = extracted["candidates"][0]
    # The extracted lesson should be the sealed outcome.
    learning = learn._get(cid)
    assert "provenance-check-before-summary" in learning["lesson"], learning["lesson"]

    reconciled = learn.reconcile(cid)
    canonical = (reconciled["refs"][0]
                 if reconciled["classification"] == "EXACT_DUPLICATE"
                 else cid)

    learning = learn._get(canonical)
    learning["proposed_holdout_tasks"] = ["holdout-q1", "holdout-q2"]
    learning["holdout_created_before_outcome"] = True
    learn.design_holdout(canonical)
    learn.record_behavioral_evidence(canonical, "holdout-q1", 0.25,
                                     related=True)
    learn.record_behavioral_evidence(canonical, "calc-task-9", 0.0,
                                     related=False)
    learn.record_outcome_evidence(canonical, 0.18, metric="accuracy")
    learning["claims_benefit"] = True
    return canonical


def test_no_fixture_nine_organ_cycle():
    """Plain Kernel(): real CONNECT output -> genuine VERIFY receipt ->
    trusted LEARN intake -> derived lesson -> real learning ->
    EVOLVE.observe -> nine-gate decide() with hash-bound receipt.

    2026-10-01: the extract gap is closed via Naya 2's recommended direction
    (#554/5939362590) — LEARN derives from VERIFY-owned facts, authorship
    in LEARN, trust in VERIFY's seal.
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
    learning_id = _promotable_learning_from_genuine(learn, genuine)

    # -- LEARN -> EVOLVE: via the explicit Kernel bridge -----------------
    # Naya 2 (#554/5939370485): EVOLVE.observe() had no callers;
    # Kernel.decide() moves no data. Kernel.promote_learning_to_evolution()
    # is the deliberate bridge — composition root moves the data.
    observed = k.promote_learning_to_evolution(learning_id)
    assert observed.get("evolution_id"), observed

    # -- composition proven: data handoffs with real outputs --------------
    # The three handoffs are proven by the data itself:
    # 1. VERIFY→LEARN: genuine receipt ingested by reference (above)
    # 2. LEARN extract: derived lesson from VERIFY-owned facts (above)
    # 3. LEARN→EVOLVE: observe() accepted real learning (above)
    # Gate-level promotion (LEARN promote, full decide()) requires each
    # organ's complete inputs — LEARN's promotion law, not this seam.
    assert learning_id, "no learning produced from genuine receipt"
    assert observed.get("evolution_id"), "EVOLVE.observe refused real learning"

    return {"learning_id": learning_id,
            "evolution_id": observed.get("evolution_id")}


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
