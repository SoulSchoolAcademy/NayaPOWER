"""Integration: Kernel.decide() traverses the nine-node runtime graph.

FLAG-001 reconciliation (CANDIDATE — NOT RATIFIED — NOT MERGED): decide()
no longer runs a forced linear call stack. The executable topology is the
canonical 13-edge runtime graph from
BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json, with the lock's
11 minimum runtime routes as the required subset. Per-edge fail-fast and
fail-closed semantics are asserted below — no gate is weakened.
"""
import copy
import json
import hashlib
import os
from datetime import datetime, timedelta, timezone

import pytest

from naya_kernel.kernel import (
    EVALUATION_ORDER,
    GATE_REQUIREMENTS,
    NON_GATE_EDGES,
    LOCK_MINIMUM_ROUTES,
    RUNTIME_EDGES,
    Kernel,
    verify_decision_receipt,
)
from naya_kernel.node_base import NodeBase, GateResult, GateVerdict
from naya_kernel.nodes import act_node, connect_node, learn_node, prove_node, verify_node


NOW = "2026-10-01T04:00:00+00:00"
PINNED = "constitution-v1-hash"
SEED_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "BRAIN", "04-INTELLIGENCE", "GRAPH", "0001-KERNEL-GRAPH-SEED-V1.json")


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
    k = Kernel()
    # This test drives LEARN with synthetic receipts (not the VERIFY→LEARN
    # trust seam). Explicit test-scope opt-in; default construction stays
    # fail-closed (see test_learn_intake_trust_seam.py for the seam tests).
    k.nodes["LEARN"] = learn_node.LearnNode(allow_fixture_intake=True)
    return k


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


# ------------------------------------------------- graph authority / drift


def _seed_kernel_edges():
    with open(SEED_PATH, encoding="utf-8") as fh:
        seed = json.load(fh)
    edges = []
    for e in seed["edges"]:
        if e["source_id"].startswith("NAYA-KERNEL-") and \
           e["target_id"].startswith("NAYA-KERNEL-"):
            src = e["source_id"].replace("NAYA-KERNEL-", "")
            tgt = e["target_id"].replace("NAYA-KERNEL-", "")
            edges.append((e["relationship_id"], src, tgt, e["type"]))
    return edges


def test_runtime_edges_match_canonical_seed():
    """Drift guard: the in-code 13-edge table is byte-faithful to the
    canonical seed file. The seed is authoritative — the code follows it."""
    assert _seed_kernel_edges() == list(RUNTIME_EDGES)


def test_lock_minimum_routes_are_required_subset():
    """The lock's 11 minimum runtime routes are all present in the 13-edge
    seed (the seed adds ACT→KNOW PRODUCES and LAW→EVOLVE GOVERNS)."""
    pairs = {(s, t) for _rid, s, t, _typ in RUNTIME_EDGES}
    for route in LOCK_MINIMUM_ROUTES:
        assert route in pairs, f"lock minimum route {route} missing"
    assert len(RUNTIME_EDGES) == 13


def test_evaluation_order_is_topological_over_gate_requirements():
    """Every node is evaluated only after its required upstreams — the
    evaluation order respects every gate edge of the runtime graph."""
    position = {name: i for i, name in enumerate(EVALUATION_ORDER)}
    assert set(EVALUATION_ORDER) == set(GATE_REQUIREMENTS)
    for node, reqs in GATE_REQUIREMENTS.items():
        for req in reqs:
            assert position[req] < position[node], \
                f"{node} evaluated before its required upstream {req}"


def test_gate_requirements_derive_from_seed_gate_edges():
    """GATE_REQUIREMENTS is exactly the gate-edge subset of the seed: every
    edge except the ACT→KNOW write edge and the EVOLVE→SELF next-cycle edge
    is a gate input."""
    gate_pairs = {(s, t) for rid, s, t, _typ in RUNTIME_EDGES
                  if rid not in NON_GATE_EDGES}
    req_pairs = {(u, n) for n, reqs in GATE_REQUIREMENTS.items() for u in reqs}
    assert req_pairs == gate_pairs


# ------------------------------------------------------------------- tests


def test_kernel_instantiates_all_nine_nodes(kernel):
    assert len(kernel.nodes) == 9
    assert all(isinstance(n, NodeBase) for n in kernel.nodes.values())


def test_decide_full_pass_under_ratified_calculus(kernel, demo_stages):
    """FLAG-001 step 4: with V2.1 RATIFIED, LEARN's promote gate honestly
    PASSes (no stale CALCULUS_NOT_RATIFIED refusal), so the LEARN->EVOLVE
    edge is satisfied and EVOLVE evaluates too. The decision verdict is
    PASS across all nine gates; stopped_at is None. This is the governance
    working on true premises: the ratified calculus is what lets learning
    proceed, stated in every receipt via calculusConfigHash."""
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    assert out["verdict"] == GateVerdict.PASS.value
    assert out["stopped_at"] is None
    assert [g["node"] for g in out["gates"]] == list(EVALUATION_ORDER)
    assert all(g["verdict"] == "PASS" for g in out["gates"])
    assert all(g["evaluated"] for g in out["gates"])
    learn_gate = out["gates"][-2]
    assert learn_gate["node"] == "LEARN"
    assert not any("CALCULUS_NOT_RATIFIED" in r
                   for r in learn_gate["reasons"])
    evolve_gate = out["gates"][-1]
    assert evolve_gate["node"] == "EVOLVE"
    assert evolve_gate["verdict"] == "PASS"


def test_gate_all_exercises_all_nine_nodes(kernel, demo_stages):
    out = kernel.gate_all({"decision_id": "demo-001", "gates": demo_stages})
    assert [g["node"] for g in out["gates"]] == list(EVALUATION_ORDER)
    # FLAG-001 step 4: V2.1 RATIFIED — LEARN passes, so all nine PASS.
    assert [g["verdict"] for g in out["gates"]] == ["PASS"] * 9
    positions = [g["position"] for g in out["gates"]]
    assert positions == list(range(1, 10))


def test_decision_receipt_is_hash_bound_and_verifiable(kernel, demo_stages):
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    receipt = out["decision_receipt"]
    assert receipt["receipt_id"] == "decision-demo-001"
    # FLAG-001 step 4: V2.1 RATIFIED — the full chain passes.
    assert receipt["verdict"] == "PASS"
    assert receipt["stopped_at"] is None
    assert receipt["evaluation_order"] == list(EVALUATION_ORDER)
    assert receipt["topology"] == "canonical-runtime-graph-v1"
    assert receipt["graph_seed"].endswith(
        "0001-KERNEL-GRAPH-SEED-V1.json")
    assert len(receipt["edge_trace"]) == 13
    check = verify_decision_receipt(receipt)
    assert check["result"] == "MATCH"
    tampered = dict(receipt, verdict="FAIL")
    assert verify_decision_receipt(tampered)["result"] == "MISMATCH"


def _independent_inputs_hash(state):
    """Recompute inputs_hash the way the persistence adapter does: full
    SHA-256 over the canonical (sorted-keys, compact) evaluated input
    state. Deliberately does NOT use the kernel's _sha256 helper."""
    return hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=True).encode("utf-8")).hexdigest()


def test_decision_receipt_carries_inputs_hash(kernel, demo_stages):
    # P3 (naya-receipt-contract/1, 2026-10-01): the kernel binds the full
    # SHA-256 over the canonical evaluated input state into the receipt,
    # BEFORE receipt_hash is computed, so the receipt hash covers it.
    state = {"decision_id": "demo-001", "gates": demo_stages}
    receipt = kernel.decide(state)["decision_receipt"]
    assert receipt["inputs_hash"] == _independent_inputs_hash(state)
    assert verify_decision_receipt(receipt)["result"] == "MATCH"
    # inputs_hash participates in the receipt seal: tampering it breaks
    # the hash binding.
    tampered = dict(receipt, inputs_hash="0" * 64)
    assert verify_decision_receipt(tampered)["result"] == "MISMATCH"
    # Deterministic per input state: same state -> same inputs_hash even
    # though issued_at (and hence receipt_hash) differs between runs.
    again = kernel.decide(state)["decision_receipt"]
    assert again["inputs_hash"] == receipt["inputs_hash"]
    assert again["receipt_hash"] != receipt["receipt_hash"]
    # Sensitive to the input state: a different state hashes differently.
    other = kernel.decide(
        {"decision_id": "demo-002", "gates": demo_stages}
    )["decision_receipt"]
    assert other["inputs_hash"] != receipt["inputs_hash"]


def test_decide_fail_closed_on_law_prohibited(kernel, demo_stages):
    """A PROHIBITED LAW gate halts the whole decision: FAIL is global
    fail-fast. Only SELF and LAW are evaluated; ACT is never consulted
    (LAW→ACT GOVERNS blocks it)."""
    stages = dict(demo_stages)
    bad = law_state()
    bad["proposal"]["flags"] = {"harm_flag": True,
                                "harm_facts": ["demo harm case"]}
    stages["LAW"] = bad
    out = kernel.decide({"gates": stages})
    assert out["verdict"] == "FAIL"
    assert out["stopped_at"] == "LAW"
    assert out["halted_on_fail"] is True
    assert [g["node"] for g in out["gates"]] == ["SELF", "LAW"]
    trace = {e["relationship_id"]: e for e in out["edge_trace"]}
    assert trace["REL-KERNEL-LAW-ACT"]["status"] == "BLOCKED"
    assert trace["REL-KERNEL-LAW-EVOLVE"]["status"] == "BLOCKED"


def test_law_need_evidence_blocks_act_but_know_branch_continues(kernel,
                                                                demo_stages):
    """Per-edge fail-fast: LAW NEED_EVIDENCE blocks ACT (LAW→ACT) and EVOLVE
    (LAW→EVOLVE), but the independent SELF→KNOW→PROVE/CONNECT branch still
    evaluates. VERIFY is then edge-blocked because its ACT input never
    PASSed — VERIFY's own gate is not consulted without its upstreams."""
    stages = dict(demo_stages)
    thin = law_state()
    thin["evidence"] = {"n": 1, "confidence": 0.9}  # below floor k=3
    stages["LAW"] = thin
    out = kernel.decide({"gates": stages})
    by_node = {g["node"]: g for g in out["gates"]}
    assert by_node["LAW"]["verdict"] == "NEED_EVIDENCE"
    assert by_node["ACT"]["evaluated"] is False
    assert by_node["ACT"]["blocked_by"] == ["LAW"]
    # independent branch still ran
    assert by_node["KNOW"]["evaluated"] is True
    assert by_node["KNOW"]["verdict"] == "PASS"
    assert by_node["PROVE"]["verdict"] == "PASS"
    assert by_node["CONNECT"]["verdict"] == "PASS"
    # VERIFY requires ACT+PROVE+CONNECT — ACT missing, so not consulted
    assert by_node["VERIFY"]["evaluated"] is False
    assert by_node["VERIFY"]["blocked_by"] == ["ACT"]
    assert by_node["VERIFY"]["verdict"] == "NEED_EVIDENCE"
    assert any("ACT" in r for r in by_node["VERIFY"]["reasons"])
    assert by_node["LEARN"]["blocked_by"] == ["VERIFY"]
    assert set(by_node["EVOLVE"]["blocked_by"]) == {"LAW", "LEARN"}
    assert out["verdict"] == "NEED_EVIDENCE"
    assert out["stopped_at"] == "LAW"


def test_verify_not_consulted_when_prove_needs_evidence(kernel, demo_stages):
    """VERIFY still requires its upstream PROVE/CONNECT/ACT inputs: when
    PROVE cannot reach PASS, VERIFY's gate is withheld (fail-closed) and
    the receipt names PROVE as the blocker."""
    kernel.nodes["PROVE"].gate = lambda _s: GateResult(
        GateVerdict.NEED_EVIDENCE, ["demo forced: claim unproven"])
    out = kernel.decide({"gates": demo_stages})
    by_node = {g["node"]: g for g in out["gates"]}
    assert by_node["PROVE"]["verdict"] == "NEED_EVIDENCE"
    assert by_node["VERIFY"]["evaluated"] is False
    assert by_node["VERIFY"]["blocked_by"] == ["PROVE"]
    assert out["verdict"] == "NEED_EVIDENCE"
    assert out["stopped_at"] == "PROVE"


def test_edge_trace_records_special_edges(kernel, demo_stages):
    """The two non-gate edges are recorded honestly: ACT→KNOW as the
    PRODUCES write path (not a re-gate), EVOLVE→SELF as the next-cycle
    edge (not traversed inside one pass)."""
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    trace = {e["relationship_id"]: e for e in out["edge_trace"]}
    write_edge = trace["REL-KERNEL-ACT-KNOW"]
    assert write_edge["status"] == "SATISFIED_WRITE_PATH"
    assert "not re-run" in write_edge["note"]
    cycle_edge = trace["REL-KERNEL-EVOLVE-SELF"]
    assert cycle_edge["status"] == "NEXT_CYCLE"
    assert "not traversed" in cycle_edge["note"]
    # gate edges satisfied by PASSed sources
    assert trace["REL-KERNEL-SELF-LAW"]["status"] == "SATISFIED"
    assert trace["REL-KERNEL-KNOW-PROVE"]["status"] == "SATISFIED"
    assert trace["REL-KERNEL-VERIFY-LEARN"]["status"] == "SATISFIED"
    # LEARN->EVOLVE satisfied: LEARN passed under the ratified calculus
    # (FLAG-001 step 4), so EVOLVE's required upstream is met.
    assert trace["REL-KERNEL-LEARN-EVOLVE"]["status"] == "SATISFIED"


def test_gate_exception_is_fail_closed_not_skipped(kernel, demo_stages):
    def boom(_state):
        raise RuntimeError("simulated gate crash")
    kernel.nodes["KNOW"].gate = boom
    out = kernel.gate_all({"gates": demo_stages})
    know = next(g for g in out["gates"] if g["node"] == "KNOW")
    assert know["verdict"] == "FAIL"
    assert any("GATE EXCEPTION" in r for r in know["reasons"])


def test_gate_exception_halts_decision_globally(kernel, demo_stages):
    """A crashing gate is a FAIL — and FAIL is global fail-fast: the
    decision halts at KNOW and downstream gates are never evaluated."""
    def boom(_state):
        raise RuntimeError("simulated gate crash")
    kernel.nodes["KNOW"].gate = boom
    out = kernel.decide({"gates": demo_stages})
    assert out["verdict"] == "FAIL"
    assert out["stopped_at"] == "KNOW"
    assert out["halted_on_fail"] is True
    assert [g["node"] for g in out["gates"]] == ["SELF", "LAW", "KNOW"]


def test_missing_sub_state_fails_closed(kernel):
    """Empty state: SELF cannot boot on nothing — never an invented PASS."""
    out = kernel.decide({"gates": {}})
    assert out["verdict"] in ("FAIL", "NEED_EVIDENCE")
    assert out["stopped_at"] == "SELF"
    assert out["gates"][0]["node"] == "SELF"


def test_cold_reconstruct_verifies_receipts(kernel, demo_stages):
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    good = out["decision_receipt"]
    bad = dict(good, verdict="FAIL")  # hash no longer matches
    recon = kernel.cold_reconstruct([good, bad])
    assert recon["receipts_checked"] == 2
    assert recon["hash_matched"] == [good["receipt_id"]]
    assert recon["hash_mismatched"] == [bad["receipt_id"]]
    assert recon["verdicts"]["PASS"] == 1


def test_gate_results_name_reasons(kernel, demo_stages):
    out = kernel.gate_all({"gates": demo_stages})
    for g in out["gates"]:
        assert g["reasons"], f"{g['node']} returned no reasons"
        assert isinstance(g["reasons"], list)


def test_gate_non_gateresult_return_is_contract_violation_fail(kernel,
                                                               demo_stages):
    """A gate returning a non-GateResult is a contract violation — FAIL,
    never an interpreted PASS."""
    kernel.nodes["KNOW"].gate = lambda _state: {"verdict": "PASS"}
    out = kernel.gate_all({"gates": demo_stages})
    know = next(g for g in out["gates"] if g["node"] == "KNOW")
    assert know["verdict"] == "FAIL"
    assert any("CONTRACT VIOLATION" in r for r in know["reasons"])


def test_gate_all_continues_past_early_failure(kernel, demo_stages):
    """Audit visibility: gate_all evaluates every gate even when an early
    gate FAILs — unlike decide()'s global fail-fast on FAIL."""
    stages = dict(demo_stages)
    bad = law_state()
    bad["proposal"]["flags"] = {"harm_flag": True,
                                "harm_facts": ["demo harm case"]}
    stages["LAW"] = bad
    out = kernel.gate_all({"gates": stages})
    assert len(out["gates"]) == 9
    assert [g["node"] for g in out["gates"]] == list(EVALUATION_ORDER)
    law_gate = out["gates"][1]
    assert law_gate["verdict"] == "FAIL"
    # the decided graph traversal halts at LAW; the audit path does not
    decided = kernel.decide({"gates": stages})
    assert len(decided["gates"]) == 2


def test_cold_reconstruct_never_trusts_mismatched_verdicts(kernel,
                                                           demo_stages):
    """A forged receipt's verdict field is unauthenticated: it is listed
    under hash_mismatched and must not appear in the verdict counts."""
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    good = out["decision_receipt"]
    bad = dict(good, verdict="FAIL")  # forged verdict; hash no longer matches
    recon = kernel.cold_reconstruct([good, bad])
    assert recon["hash_mismatched"] == [bad["receipt_id"]]
    assert recon["verdicts"] == {"PASS": 1}
    assert "FAIL" not in recon["verdicts"]


def test_decision_receipt_carries_candidate_banner(kernel, demo_stages):
    """Every decision receipt labels itself candidate — never an implied
    ratification or merge claim."""
    out = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    receipt = out["decision_receipt"]
    assert receipt["candidate_banner"] == "CANDIDATE — NOT RATIFIED — NOT MERGED"
    assert receipt["kernel_version"]


def test_decide_with_no_state_is_fail_closed(kernel):
    """decide(None): SELF cannot boot on nothing — fail-closed, never an
    invented PASS."""
    out = kernel.decide(None)
    assert out["verdict"] in ("FAIL", "NEED_EVIDENCE")
    assert out["stopped_at"] == "SELF"
    assert verify_decision_receipt(out["decision_receipt"])["result"] == "MATCH"


# ------------------------------------------------- harden: routing edge cases (tick 22)


def test_fail_after_earlier_need_evidence_fail_dominates_verdict(
        kernel, demo_stages):
    """Verdict-semantics edge: PROVE returns NEED_EVIDENCE (position 5), then
    CONNECT FAILs (position 6). FAIL dominance (Brief 3, decided 2026-10-01
    under the Decision Protocol): the decision verdict and stopped_at name
    the halting FAIL (CONNECT / FAIL) — a naive consumer must never misread
    a decided NO as "couldn't decide". The first non-PASS is preserved in
    first_non_pass / first_non_pass_at (PROVE / NEED_EVIDENCE) and inside the
    receipt. The FAIL still halts the whole decision globally
    (halted_on_fail True)."""
    kernel.nodes["PROVE"].gate = lambda _s: GateResult(
        GateVerdict.NEED_EVIDENCE, ["demo forced: claim unproven"])
    kernel.nodes["CONNECT"].gate = lambda _s: GateResult(
        GateVerdict.FAIL, ["demo forced: boundary breach"])
    out = kernel.decide({"gates": demo_stages})
    by_node = {g["node"]: g for g in out["gates"]}
    assert by_node["PROVE"]["verdict"] == "NEED_EVIDENCE"
    assert by_node["CONNECT"]["evaluated"] is True
    assert by_node["CONNECT"]["verdict"] == "FAIL"
    # the FAIL halted the pass: later nodes never evaluated
    assert [g["node"] for g in out["gates"]] == [
        "SELF", "LAW", "KNOW", "ACT", "PROVE", "CONNECT"]
    assert out["verdict"] == "FAIL"
    assert out["stopped_at"] == "CONNECT"
    assert out["first_non_pass"] == "NEED_EVIDENCE"
    assert out["first_non_pass_at"] == "PROVE"
    assert out["halted_on_fail"] is True
    receipt = out["decision_receipt"]
    assert receipt["verdict"] == "FAIL"
    assert receipt["stopped_at"] == "CONNECT"
    assert receipt["first_non_pass"] == "NEED_EVIDENCE"
    assert receipt["first_non_pass_at"] == "PROVE"
    assert verify_decision_receipt(receipt)["result"] == "MATCH"


def test_decision_id_deterministic_when_omitted(kernel, demo_stages):
    """decision_id derives from the state hash when the caller omits it —
    two identical passes produce the identical id (replay-detectable)."""
    out1 = kernel.decide({"gates": copy.deepcopy(demo_stages)})
    out2 = kernel.decide({"gates": copy.deepcopy(demo_stages)})
    assert out1["decision_id"] == out2["decision_id"]
    assert out1["decision_id"].startswith("d-")
    assert out1["verdict"] == out2["verdict"] == "PASS"
    assert verify_decision_receipt(out1["decision_receipt"])["result"] == "MATCH"


def test_know_gate_consulted_exactly_once_per_pass(kernel, demo_stages):
    """ACT→KNOW is the PRODUCES write edge: KNOW's gate runs exactly once
    per pass — the write edge must not trigger a second consultation of
    KNOW's gate in the same pass."""
    calls = []
    orig = kernel.nodes["KNOW"].gate

    def counting(sub_state):
        calls.append(1)
        return orig(sub_state)

    kernel.nodes["KNOW"].gate = counting
    out = kernel.decide({"gates": demo_stages})
    assert len(calls) == 1, calls
    trace = {e["relationship_id"]: e for e in out["edge_trace"]}
    assert trace["REL-KERNEL-ACT-KNOW"]["status"] == "SATISFIED_WRITE_PATH"


def test_need_evidence_blocks_downstream_without_halting(kernel, demo_stages):
    """NEED_EVIDENCE is not a FAIL: PROVE's hold does not halt the decision
    (halted_on_fail False). The edge trace is source-centric by design: the
    KNOW->PROVE edge is SATISFIED (KNOW PASSed its handoff; PROVE's gate was
    consulted and returned NEED_EVIDENCE itself), while the downstream
    PROVE->VERIFY edge is BLOCKED (PROVE did not PASS its handoff)."""
    kernel.nodes["PROVE"].gate = lambda _s: GateResult(
        GateVerdict.NEED_EVIDENCE, ["demo forced: claim unproven"])
    out = kernel.decide({"gates": demo_stages})
    assert out["verdict"] == "NEED_EVIDENCE"
    assert out["halted_on_fail"] is False
    by_node = {g["node"]: g for g in out["gates"]}
    assert by_node["PROVE"]["evaluated"] is True
    assert by_node["PROVE"]["verdict"] == "NEED_EVIDENCE"
    trace = {e["relationship_id"]: e for e in out["edge_trace"]}
    assert trace["REL-KERNEL-SELF-KNOW"]["status"] == "SATISFIED"
    assert trace["REL-KERNEL-KNOW-PROVE"]["status"] == "SATISFIED"
    assert trace["REL-KERNEL-PROVE-VERIFY"]["status"] == "BLOCKED"
    assert verify_decision_receipt(
        out["decision_receipt"])["result"] == "MATCH"


def test_non_gate_edges_partition_closed():
    """NON_GATE_EDGES is exactly the non-gate subset of the seed's rel ids:
    every member is a seed rel id; every seed rel id that is not a gate
    input (per GATE_REQUIREMENTS) is a member; and the per-edge trace labels
    (never silently gate-classifies) every member — DISPOSITION_UNDEFINED
    is the honest fallback, plain SATISFIED must never appear on a
    non-gate edge."""
    seed_ids = {rid for rid, _s, _t, _typ in RUNTIME_EDGES}
    assert NON_GATE_EDGES <= seed_ids, "non-gate id not in the seed"
    req_pairs = {(u, n) for n, reqs in GATE_REQUIREMENTS.items() for u in reqs}
    gate_ids = {rid for rid, s, t, _typ in RUNTIME_EDGES if (s, t) in req_pairs}
    assert gate_ids | NON_GATE_EDGES == seed_ids, "partition does not cover the seed"
    assert gate_ids & NON_GATE_EDGES == set(), "overlap between gate and non-gate"
    # Full-PASS trace: non-gate edges carry their honest dispositions, never
    # a gate edge's plain SATISFIED and never the undefined fallback.
    trace = {e["relationship_id"]: e for e in Kernel()._edge_trace(
        {n: GateVerdict.PASS for n in EVALUATION_ORDER}, {})}
    for rid in NON_GATE_EDGES:
        assert trace[rid]["status"] not in ("SATISFIED", "DISPOSITION_UNDEFINED"), rid


# ------------------------------------------------- harden: receive path (tick 25)


def test_unexpected_gate_keys_are_recorded_not_silently_dropped(
        kernel, demo_stages):
    """A caller typo in state["gates"] keys (the tick-10 "harmFlag" class of
    bug) must be visible, never silently dropped: decide() records the
    unknown key in the receipt and the result; no gate is consulted with it
    and the decision outcome is unchanged."""
    stages = dict(demo_stages)
    stages["LAWX"] = {"some": "payload"}
    out = kernel.decide({"gates": stages})
    assert out["unexpected_gate_keys"] == ["LAWX"]
    receipt = out["decision_receipt"]
    assert receipt["unexpected_gate_keys"] == ["LAWX"]
    assert verify_decision_receipt(receipt)["result"] == "MATCH"
    # identical decision as without the stray key
    plain = kernel.decide({"gates": demo_stages})
    assert out["verdict"] == plain["verdict"]
    assert [g["verdict"] for g in out["gates"]] == \
        [g["verdict"] for g in plain["gates"]]


def test_decide_tolerates_non_dict_gates_container(kernel):
    """A malformed state["gates"] (not a dict) is treated as absent —
    fail-closed, never an AttributeError crash."""
    out = kernel.decide({"gates": ["not", "a", "dict"]})
    assert out["verdict"] in ("FAIL", "NEED_EVIDENCE")
    assert out["stopped_at"] == "SELF"
    assert out["unexpected_gate_keys"] == []
    assert verify_decision_receipt(out["decision_receipt"])["result"] == "MATCH"


def test_gate_all_tolerates_non_dict_gates_container(kernel):
    """gate_all evaluates all nine gates (each on an empty sub-state) even
    when state["gates"] is malformed."""
    out = kernel.gate_all({"gates": "not-a-dict"})
    assert len(out["gates"]) == 9
    assert [g["node"] for g in out["gates"]] == [
        "SELF", "LAW", "KNOW", "ACT", "PROVE", "CONNECT",
        "VERIFY", "LEARN", "EVOLVE"]


def test_gate_all_emits_hash_bound_audit_receipt(kernel, demo_stages):
    """The module docstring's promise: every gate_all() call emits a
    hash-bound receipt — an AUDIT receipt, distinct from a decision."""
    out = kernel.gate_all({"decision_id": "demo-001", "gates": demo_stages})
    receipt = out["audit_receipt"]
    assert receipt["receipt_id"] == "audit-demo-001"
    assert receipt["mode"] == "AUDIT"
    assert receipt["verdict"] == "PASS"  # demo chain passes all nine
    assert receipt["candidate_banner"] == "CANDIDATE — NOT RATIFIED — NOT MERGED"
    check = verify_decision_receipt(receipt)
    assert check["result"] == "MATCH"


def test_gate_all_reports_unexpected_gate_keys(kernel, demo_stages):
    """gate_all() is fail-visible on stray keys, like decide(): the tick-25
    'harmFlag' typo class surfaces in the audit output AND the receipt,
    never consulted by any gate."""
    stages = dict(demo_stages)
    stages["harmFlag"] = {"typo": True}  # not a node name
    out = kernel.gate_all({"gates": stages})
    assert out["unexpected_gate_keys"] == ["harmFlag"]
    assert out["audit_receipt"]["unexpected_gate_keys"] == ["harmFlag"]
    assert verify_decision_receipt(out["audit_receipt"])["result"] == "MATCH"


def test_cold_reconstruct_separates_audit_receipts(kernel, demo_stages):
    """An AUDIT receipt's verdict is not a decision verdict: it is verified
    and listed separately, never counted in the decision tally."""
    decided = kernel.decide({"decision_id": "demo-001", "gates": demo_stages})
    audited = kernel.gate_all({"decision_id": "demo-001", "gates": demo_stages})
    recon = kernel.cold_reconstruct(
        [decided["decision_receipt"], audited["audit_receipt"]])
    assert recon["receipts_checked"] == 2
    assert recon["hash_matched"] == ["decision-demo-001"]
    assert recon["audit_receipts_verified"] == ["audit-demo-001"]
    assert recon["audit_receipts_mismatched"] == []
    assert recon["verdicts"] == {"PASS": 1}  # audit verdict not counted
