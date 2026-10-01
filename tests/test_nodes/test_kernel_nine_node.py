"""Integration: Kernel.decide() exercises all nine nodes (GAP-A closure).

CANDIDATE — NOT RATIFIED — NOT MERGED. This file replaces the scaffold
smoke test (test_kernel.py): decide()/gate_all() are real now.
"""
import copy
import json
import hashlib
from datetime import datetime, timedelta, timezone

import pytest

from naya_kernel.kernel import GATE_ORDER, Kernel, verify_decision_receipt
from naya_kernel.node_base import NodeBase, GateVerdict
from naya_kernel.nodes import act_node, connect_node, learn_node, prove_node, verify_node


NOW = "2026-10-01T04:00:00+00:00"
PINNED = "constitution-v1-hash"


def _h(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# ---------------------------------------------------------------- fixtures


def self_state():
    payload = {"boot_count": 7, "owner_scope": "shawn-personal"}
    checkpoint_hash = _h(payload)
    pred = {"predecessor_hash": None, "checkpoint_hash": checkpoint_hash,
            "config_hash": "config-rev-9", "identity_binding": "bind-1"}
    pred["receipt_hash"] = _h({k: v for k, v in pred.items()
                               if k != "receipt_hash"})
    return {
        "execution_id": "exec-demo-001", "seen_execution_ids": [],
        "identity_claim": {"type": "NAYA"},
        "identity_binding": {"binding_ref": "bind-1", "verified": True,
                             "actor_type": "NAYA"},
        "mission_ref": "mission:ratified-v1", "scope_ref": "scope:ratified-v1",
        "ratified_sources": {
            "mission:ratified-v1": {"text": "serve Shawn as Naya"},
            "scope:ratified-v1": {"actions": ["read", "summarize"]}},
        "owner_scope": "shawn-personal", "kernel_revision": "rev-9",
        "checkpoint": {"hash": checkpoint_hash, "payload": payload,
                       "owner_scope": "shawn-personal"},
        "predecessor_receipt": pred, "known": ["mission text"],
        "unknown": [], "blocked": ["production database"],
    }


def law_state():
    prop = {
        "proposalId": "p-demo-1", "intent": "demo decision",
        "action": {"type": "send_email", "scope_tag": "send_email",
                   "action_class": "routine", "targets": ["a@example.com"],
                   "bounds": {"max": 1}},
        "proposedBy": "ACT",
        "authorityClaim": {"grant_ref": "g1", "grantor": "DIRECTOR"},
        "evidenceRefs": ["e1"], "stakes": "low", "reversibility": 8,
        "identityContext": {}, "constitutionHash": PINNED, "flags": {},
        "material_facts_version": 1,
    }
    return {
        "proposal": prop,
        "constitution_store": {"pinned_hash": PINNED,
                               "corpus": {PINNED: "ratified text"},
                               "reachable": True},
        "grants": [{"grant_ref": "g1", "grantor": "DIRECTOR",
                    "grantee": "ACT", "scope": ["send_email"], "bounds": {},
                    "expiry": None, "revoked": False, "chain": [],
                    "tampered": False}],
        "evidence": {"n": 5, "confidence": 0.9}, "evidence_floor_k": 3,
        "seen_proposal_hashes": {},
    }


def act_state():
    return {
        "decision_receipt": act_node.make_decision_receipt(
            receipt_id="dec-demo-001",
            issued_at="2026-10-01T02:00:00+00:00",
            valid_until="2026-10-02T00:00:00+00:00"),
        "tool_registry": act_node.make_tool_registry(),
        "execution_ledger": {}, "now": NOW,
    }


def know_state():
    return {
        "candidate": {
            "content": "The quick brown fox", "proposed_class": "CONTEXT",
            "class_signals": [{"signal": "auto-classifier-v0", "value": 0.82}],
            "classifier": "auto",
            "provenance": {"sources": [{
                "kind": "EXTERNAL", "ref": "ext://example/demo",
                "capturedAt": NOW, "capturedBy": "naya-demo"}]},
            "identity_binding": {"verified": True},
            "owner_scope": "public", "epistemic_state": "INGESTED"},
        "principal": {"identity": "naya-demo",
                      "entitled_scopes": ["public", "team"]},
        "now": NOW,
    }


def prove_state(kernel):
    pnow = datetime.now(timezone.utc)
    evidence = []
    for i in range(5):
        evidence.append({
            "address": f"ev-sensor-{i}", "source": f"sensor-{i}",
            "acquisition_method": f"direct-read-{i}",
            "acquired_at": (pnow - timedelta(days=i)).isoformat(),
            "qualified_oracle": True, "failure_mode": f"mode-{i}",
            "independent_of_claim": True, "restates_claim": False,
            "provisional_until": None})
    claim = {
        "id": "claim-demo-1", "class": "EMPIRICAL",
        "assertion": "the suite passed",
        "assertions": [{"text": "the suite passed",
                        "evidence": ["ev-sensor-0"]}],
        "evidence": evidence, "stakes": "low",
        "overturn_conditions": ["a failing run under the same conditions"],
        "observation_recorded_with_method": True, "raw_data_retained": True,
        "freshness_seconds": 7 * 24 * 3600, "as_of": pnow.isoformat()}
    node = kernel.nodes["PROVE"]
    node.submit(copy.deepcopy(claim))
    for _ in range(4):
        node.advance("claim-demo-1")
    return {"claim": claim, "operation": "intake"}


def connect_state():
    bindings = {"naya": {"authenticated": True,
                         "owner_scope": "shawn-scope",
                         "binding_ref": "b-naya"}}
    body = {"consent_id": "consent-naya", "party": "naya",
            "purpose": "research", "scope": ["reports", "facts"],
            "expires_at": "2999-01-01T00:00:00+00:00",
            "revoked": False, "revocable": True}
    body["consent_hash"] = connect_node._sha256(
        {k: v for k, v in body.items() if k != "consent_hash"})
    req = {"id": "conn-demo-1", "kind": "GRAPH_EDGE",
           "parties": [{"identity": "naya", "owner_scope": "shawn-scope",
                        "role": "peer"}],
           "purpose": "research",
           "scope": [{"owner_scope": "shawn-scope",
                      "content_classes": ["reports"]}],
           "consentRefs": ["consent-naya"], "evidenceRefs": ["ev-1"],
           "boundaryPolicy": {"version": "v1", "forbidden_classes": [],
                              "strictness": 1},
           "expiresAt": None, "reversibility": 8.0, "consentLadder": "SHARED"}
    return {
        "connection_request": req,
        "consent_registry": {"consent-naya": body},
        "identity_bindings": copy.deepcopy(bindings),
        "evidence_registry": {"ev-1": {"content_hash": "abc123",
                                      "valid": True}},
        "boundary_policy": {"version": "v1", "forbidden_classes": [],
                            "strictness": 1},
        "now": NOW,
    }


def verify_state(kernel):
    t0 = "2026-10-01T03:00:00+00:00"
    node = kernel.nodes["VERIFY"]
    req = {
        "verify_key": "vk-demo-1", "kind": "claim_baton",
        "subject": {"claim": "the widget works",
                    "epistemic_state": "SUPPORTED", "evidence": ["ev1"],
                    "provenance": {"source": "lab"}, "scope": "widget v2",
                    "limitations": ["lab-only"], "gaps": []},
        "expected_outcome": {"declared": True, "success": "widget passes"},
        "acceptance_criteria": [{"id": "c1", "critical": True, "met": True}],
        "evidence_refs": [{"address": "ev1", "class": "REUSABLE",
                           "retrievable": True, "owner": "owner-a"}],
        "reproducer_seat": {"identity": "seat-B"},
        "deciding_seat": {"identity": "seat-A"},
        "requesting_owner": "owner-a", "now": t0}
    out = node.submit(req)
    assert not out.get("refused"), out
    rid = out["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity", "no_shared_unlogged_context",
         "own_authenticated_issued_by"], "MATCH", now=t0)
    node.run_tier1(
        rid, {"recompute_match": True, "evidence_ref_integrity": True,
              "gate_conformance": True,
              "negation_probes": [{"probe": "try-to-fail", "passed": False,
                                   "expected": "fail",
                                   "note": "attack failed"}]},
        now=t0)
    node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
               "VERIFIED_PASS", now=t0)
    return {"receipt_id": rid}


def learn_state(kernel):
    node = kernel.nodes["LEARN"]
    behavior = {"description": "check provenance before serving",
                "observable": "provenance checked in trace",
                "scope": "triage"}
    canonical = None
    for i in range(20):
        rid = f"vr-demo-{i}"
        receipt = {
            "receipt_id": rid, "node_id": "NAYA-KERNEL-VERIFY",
            "verification_state": "VERIFIED_PASS", "owner_id": "owner-1",
            "source_id": "vsrc-1",
            "outcome": {"outcome_id": f"out-{rid}",
                        "lesson": "check provenance first",
                        "scope": {"task_classes": ["triage"]},
                        "learning_type": "BEHAVIOR_RULE",
                        "expected_behavior": dict(behavior),
                        "critical_claim": False}}
        r = node.ingest_verify_receipt(receipt)
        assert r["accepted"], r
        cid = node.extract([rid])["candidates"][0]
        res = node.reconcile(cid)
        if res["classification"] == "EXACT_DUPLICATE":
            canonical = res["refs"][0]
        elif canonical is None:
            canonical = cid
    learning = node._get(canonical)
    learning["proposed_holdout_tasks"] = ["holdout-q1", "holdout-q2"]
    learning["holdout_created_before_outcome"] = True
    node.design_holdout(canonical)
    node.record_behavioral_evidence(canonical, "holdout-q1", 0.25,
                                    related=True)
    node.record_behavioral_evidence(canonical, "calc-task-9", 0.0,
                                    related=False)
    node.record_outcome_evidence(canonical, 0.18, metric="accuracy")
    learning["claims_benefit"] = True
    return {"action": "promote", "learning_id": canonical}


@pytest.fixture()
def kernel():
    return Kernel()


@pytest.fixture()
def demo_stages(kernel):
    return {
        "SELF": self_state(),
        "LAW": law_state(),
        "ACT": act_state(),
        "KNOW": know_state(),
        "PROVE": prove_state(kernel),
        "CONNECT": connect_state(),
        "VERIFY": verify_state(kernel),
        "LEARN": learn_state(kernel),
        "EVOLVE": {"action": "metrics"},
    }


# ------------------------------------------------------------------ tests


def test_gate_order_covers_all_nine_nodes():
    names = [name for name, _ in GATE_ORDER]
    assert names == ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT",
                     "VERIFY", "LEARN", "EVOLVE"]


def test_kernel_instantiates_all_nine_nodes(kernel):
    assert len(kernel.nodes) == 9
    assert all(isinstance(n, NodeBase) for n in kernel.nodes.values())


def test_decide_short_circuits_at_learn_by_design(kernel, demo_stages):
    """With V2.1 unratified, LEARN honestly refuses autonomous promotion.

    8 gates PASS; LEARN returns NEED_EVIDENCE with CALCULUS_NOT_RATIFIED
    and the learning is routed to BRIEF. decide() stops there by design —
    the kernel will not autonomously learn on unratified math.
    """
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    assert out["verdict"] == GateVerdict.NEED_EVIDENCE.value
    assert out["stopped_at"] == "LEARN"
    assert [g["node"] for g in out["gates"]] == [
        "SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN"]
    assert all(g["verdict"] == "PASS" for g in out["gates"][:-1])
    learn_gate = out["gates"][-1]
    assert learn_gate["verdict"] == "NEED_EVIDENCE"
    assert any("CALCULUS_NOT_RATIFIED" in r for r in learn_gate["reasons"])
    # EVOLVE not reached in decide() — the pipeline stopped by design.


def test_gate_all_exercises_all_nine_nodes(kernel, demo_stages):
    out = kernel.gate_all({"decision_id": "demo-001", "gates": demo_stages})
    assert [g["node"] for g in out] == [
        "SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY",
        "LEARN", "EVOLVE"]
    assert [g["verdict"] for g in out] == [
        "PASS", "PASS", "PASS", "PASS", "PASS", "PASS", "PASS",
        "NEED_EVIDENCE", "PASS"]
    positions = [g["position"] for g in out]
    assert positions == list(range(1, 10))


def test_decision_receipt_is_hash_bound_and_verifiable(kernel, demo_stages):
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    receipt = out["decision_receipt"]
    assert receipt["receipt_id"] == "decision-demo-001"
    assert receipt["verdict"] == "NEED_EVIDENCE"
    assert receipt["stopped_at"] == "LEARN"
    assert receipt["gate_order"] == [n for n, _ in GATE_ORDER]
    check = verify_decision_receipt(receipt)
    assert check["result"] == "MATCH"
    tampered = dict(receipt, verdict="PASS")
    assert verify_decision_receipt(tampered)["result"] == "MISMATCH"


def test_decide_fail_closed_on_law_prohibited(kernel, demo_stages):
    """A PROHIBITED LAW gate stops the pipeline before ACT/KNOW run."""
    stages = dict(demo_stages)
    bad = law_state()
    bad["proposal"]["flags"] = {"harm_flag": True,
                                "harm_facts": ["demo harm case"]}
    stages["LAW"] = bad
    out = kernel.decide({"gates": stages})
    assert out["verdict"] == "FAIL"
    assert out["stopped_at"] == "LAW"
    assert [g["node"] for g in out["gates"]] == ["SELF", "LAW"]


def test_gate_exception_is_fail_closed_not_skipped(kernel, demo_stages):
    def boom(_state):
        raise RuntimeError("simulated gate crash")
    kernel.nodes["KNOW"].gate = boom
    out = kernel.gate_all({"gates": demo_stages})
    know = next(g for g in out if g["node"] == "KNOW")
    assert know["verdict"] == "FAIL"
    assert any("GATE EXCEPTION" in r for r in know["reasons"])


def test_missing_sub_state_fails_closed(kernel):
    """Empty state: SELF cannot boot on nothing — never an invented PASS."""
    out = kernel.decide({"gates": {}})
    assert out["verdict"] in ("FAIL", "NEED_EVIDENCE")
    assert out["stopped_at"] == "SELF"
    assert out["gates"][0]["node"] == "SELF"


def test_cold_reconstruct_verifies_receipts(kernel, demo_stages):
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    good = out["decision_receipt"]
    bad = dict(good, verdict="PASS")  # hash no longer matches
    recon = kernel.cold_reconstruct([good, bad])
    assert recon["receipts_checked"] == 2
    assert recon["hash_matched"] == [good["receipt_id"]]
    assert recon["hash_mismatched"] == [bad["receipt_id"]]
    assert recon["verdicts"]["NEED_EVIDENCE"] == 1


def test_gate_results_name_reasons(kernel, demo_stages):
    out = kernel.gate_all({"gates": demo_stages})
    for g in out:
        assert g["reasons"], f"{g['node']} returned no reasons"
        assert isinstance(g["reasons"], list)
