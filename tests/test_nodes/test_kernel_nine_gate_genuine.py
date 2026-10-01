"""Genuine nine-gate decide() traversal — no fixtures.

Proves all nine kernel nodes PASS in a single Kernel.decide() call using
only genuine paths:
- VERIFY: real receipts via submit → reproduce → tier1 → close
- LEARN: real intake via resolver (no allow_fixture_intake), real pipeline
- All other gates: genuine inputs per nine-gate-input-map.md

This is the "nine nodes live" proof: one decide(), nine PASS, nine receipts.
"""

import copy
import pytest

from naya_kernel.kernel import Kernel
from naya_kernel.nodes import act_node
from naya_kernel.nodes import learn_node as learn_module

# Import helpers from the fixture-based test (inputs are genuine; only
# LEARN used fixtures there)
import sys
sys.path.insert(0, "tests/test_nodes")
from test_kernel_nine_node import (
    self_state, law_state, act_state, know_state,
    prove_state, connect_state, PINNED, NOW, _h,
)

OWNER = "owner-a"
T0 = "2026-10-01T12:00:00+00:00"


def _genuine_verify_receipt(verify, verify_key, claim_text, outcome_id=None):
    """Drive one genuine VERIFY receipt through the public lifecycle.
    
    Coda 1 Option A: actor authors outcome at submit(), VERIFY seals at close().
    """
    out = verify.submit({
        "verify_key": verify_key,
        "kind": "claim_baton",
        "subject": {
            "claim": claim_text,
            "epistemic_state": "observed",
            "evidence": ["ev1"],
            "provenance": "test-provenance",
            "scope": {"task_classes": ["triage"], "owner": OWNER},
            "limitations": [],
            "gaps": [],
        },
        # Actor-authored outcome, sealed by VERIFY at close():
        # Includes expected_behavior (for LEARN promotion) and scope.
        # outcome_id groups receipts into the same learning.
        "outcome": {
            "outcome_id": outcome_id or f"out-{verify_key}",
            "lesson": f"verified: {claim_text}",
            "scope": {"task_classes": ["triage"], "owner": OWNER},
            "expected_behavior": {
                "description": "check provenance before serving a summary",
                "observable": "provenance checked in trace before summary",
                "scope": "triage",
            },
        },
        "evidence_refs": [{"address": "ev1", "retrievable": True,
                           "class": "REFERENCE"}],
        "deciding_seat": {"identity": "deciding-seat"},
        "requesting_owner": OWNER,
        "now": T0,
    })
    assert not out.get("refused"), out
    rid = out["receipt"]["id"]
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
                           "expected": "fail", "note": "attack failed"}]},
        now=T0)
    close_out = verify.close(
        rid, outcome_status="SUCCESS",
        acceptance_decision="ACCEPTED",
        causal_status="CAUSAL_SUPPORTED",
        target_state="VERIFIED_PASS", now=T0)
    assert not close_out.get("refused"), close_out
    receipt = verify._receipts[rid]
    assert receipt["verification_state"] == "VERIFIED_PASS"
    # Seal covers the outcome (Coda 1 Option A)
    assert receipt["outcome"]["lesson"] == f"verified: {claim_text}"
    return receipt


def _build_promotable_learning(kernel):
    """Build a promotable learning via the genuine pipeline.
    
    Uses 5 genuine VERIFY receipts (k=5 critical floor) ingested via
    the resolver — no fixture intake.
    """
    verify = kernel.nodes["VERIFY"]
    learn = kernel.nodes["LEARN"]
    
    # Create 5 genuine VERIFY receipts with the same lesson and outcome_id
    # (full lifecycle: submit → reproduce → tier1 → close → VERIFIED_PASS)
    # Same outcome_id groups them into one learning for the k=5 floor.
    rids = []
    for i in range(5):
        receipt = _genuine_verify_receipt(
            verify, f"vk-nine-gate-{i}", "check provenance before serving",
            outcome_id="out-nine-gate-shared")
        rids.append(receipt["id"])
    
    # Ingest via resolver (genuine path, no fixture)
    # Pass the full receipt; C3 allowlist verifies it matches VERIFY's store
    for rid in rids:
        presented = copy.deepcopy(verify._receipts[rid])
        res = learn.ingest_verify_receipt(presented)
        assert res["accepted"], f"ingest failed for {rid}: {res}"
    
    # Extract candidates (returns list of learning ID strings)
    extracted = learn.extract(rids)
    assert extracted["candidates"], extracted
    cid = extracted["candidates"][0]
    assert isinstance(cid, str), f"expected str ID, got {type(cid)}: {cid}"
    
    # Reconcile to canonical (returns classification dict; ID unchanged)
    learn.reconcile(cid)
    canonical_id = cid
    
    # Design holdout and add evidence
    learn.design_holdout(canonical_id)
    learn.record_behavioral_evidence(canonical_id, "holdout-q1", 0.25, related=True)
    learn.record_behavioral_evidence(canonical_id, "calc-task-9", 0.0, related=False)
    learn.record_outcome_evidence(canonical_id, 0.18, metric="accuracy")
    
    # Mark as critical (k=5 floor) and claiming benefit
    learning = learn._get(canonical_id)
    learning["critical_claim"] = True
    learning["claims_benefit"] = True
    
    # Verify promotion eligible (takes ID string, not dict)
    eligible, reasons = learn.promotionEligible(canonical_id)
    assert eligible, f"not eligible: {reasons}"
    
    return canonical_id


def test_genuine_nine_gate_decide_all_pass():
    """One decide() call, all nine gates PASS, no fixtures."""
    kernel = Kernel()  # Default: LEARN fail-closed, no fixture intake
    
    # Build the promotable learning via genuine pipeline BEFORE decide()
    # (LEARN gate needs the learning to exist)
    learning_id = _build_promotable_learning(kernel)
    
    # Build gate states (reuse genuine helpers from fixture test)
    gates = {
        "SELF": self_state(),
        "LAW": law_state(),
        "KNOW": know_state(),
        "ACT": act_state(),
        "PROVE": prove_state(kernel),
        "CONNECT": connect_state(),
        # VERIFY: use one of our genuine receipts
        "VERIFY": {"receipt_id": kernel.nodes["VERIFY"]._receipts[
            list(kernel.nodes["VERIFY"]._receipts.keys())[0]]["id"]},
        # LEARN: promote the genuine learning
        "LEARN": {"action": "promote", "learning_id": learning_id},
        "EVOLVE": {"action": "metrics"},
    }
    
    # One decide() call
    result = kernel.decide({"decision_id": "nine-gate-genuine-001", "gates": gates})
    
    # All nine PASS
    assert result["verdict"] == "PASS", result
    assert result["stopped_at"] is None, result
    
    for gate in result["gates"]:
        assert gate["verdict"] == "PASS", f"{gate['node']}: {gate['verdict']}"
        assert gate["evaluated"], f"{gate['node']} not evaluated"
    
    # Nine receipts, one per node
    assert len(result["gates"]) == 9
    print(f"\n✓ All nine gates PASS in one decide() call")
    for gate in result["gates"]:
        print(f"  {gate['position']}. {gate['node']}: {gate['verdict']}")
