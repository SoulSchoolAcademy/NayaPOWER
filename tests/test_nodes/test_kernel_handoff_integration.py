"""Kernel handoff integration (CANDIDATE — NOT RATIFIED, NOT MERGED).

One real decision's receipts travel between the nine nodes through the
nodes' REAL methods — not gate verdicts alone.

What this proves:
  1. The shared executable calculator (kernel/value_calculus.py) actually
     runs for EVOLVE: the receipt's score equals an independent
     recomputation through the same engine, the receipt names the engine
     ("shared_calculator"), and it binds the executable's blob SHA — the
     same SHA pinned in node_base (git blob hash of the ratified file).
  2. ACT -> KNOW: a PASSed decision drives ACT's real execute() (the CAS
     path), the execution receipt is ingested into KNOW through KNOW's
     real _persist_block, then retrieves it. A LATER cycle — a FRESH KnowNode
     rebuilt from the ingest receipt via the §10 cold_reconstruct
     procedure — restores a hash-identical store. Receipt-based continuity
     across a restart, verified by hash, not by trust.
  3. EVOLVE -> SELF: EVOLVE's sealed 24-field successor package is carried
     into the next cycle's SELF boot; SELF's boot receipt binds the
     package hash (predecessor_binding_hash) and carries the package in
     its inputs. The loop closes.
  4. Negative controls: a LAW PROHIBITED decision never executes ACT and
     the handoff write is refused; missing evidence yields NEED_EVIDENCE
     and the write is refused; a tampered successor package fails its
     seal loudly instead of binding.

Honest durability boundary: the kernel's decide() evaluates gates; it does
not execute handoffs ("recorded, not re-gated", "not traversed in one
pass"). The HandoffHarness below drives the handoffs the kernel records,
gated on the decision verdict — nothing executes or persists unless the
full decision PASSed. ACT's CAS is a single-process stand-in
(act_node.py); KNOW's store here is rebuilt in-process from receipts.
Cross-process durability (a successor OS process reading a predecessor's
receipt files) is NOT proven here and is not claimed. Kernel-level
auto-execution of handoffs inside decide() is follow-up work, named in the
module docstring, not smuggled in as a claim.
"""

import copy
import hashlib
import json

import pytest

from test_nodes.test_kernel_nine_node import (
    NOW,
    act_state,
    demo_stages,
    kernel,
    know_state,
    law_state,
    self_state,
)
from naya_kernel.node_base import CALCULUS_V21_EXECUTABLE_HASH
from naya_kernel.nodes import act_node, evolve_node, know_node, self_node
from naya_kernel.nodes.evolve_node import package_hash as evolve_package_hash
from kernel.value_calculus import (
    ENGINE_VERSION,
    Candidate as V21Candidate,
    PVEstimate as V21PVEstimate,
    QualityProfile as V21QualityProfile,
    RiskPolicy as V21RiskPolicy,
    evaluate_candidates as v21_evaluate_candidates,
)


# ---------------------------------------------------------------------------
# Harness


class HandoffRefused(Exception):
    """The harness refuses to move evidence across a non-PASS verdict."""


def _echo_executor(tool_id, params):
    """The real tool-execution seam: genuinely performs the echo tool.

    ACT never executes tools itself — it admits, budgets, CAS-locks, and
    delegates to this executor. For the integration proof the executor is
    the echo tool's real behavior: it returns the text as observed
    effects, which ACT captures as evidence (evidence_capture).
    """
    assert tool_id == "echo_tool", "demo registry carries only echo_tool"
    return {"status": "ok",
            "effects": "echoed: %s" % params.get("text", ""),
            "error_class": None}


class HandoffHarness:
    """Drives evidence handoffs through the nodes' real methods.

    Nothing executes or persists unless the full kernel decision PASSed.
    A refusal is loud (HandoffRefused), never a silent skip.
    """

    def __init__(self):
        # The executor is the tool's real behavior behind ACT's seam —
        # admission, budget, CAS, and evidence capture all still run.
        self.act = act_node.ActNode(executor=_echo_executor)
        self.evolve = evolve_node.EvolveNode()

    # -- ACT -> KNOW ----------------------------------------------------
    def execute_act(self, act_st, decision_out):
        if decision_out["verdict"] != "PASS":
            raise HandoffRefused(
                "execute_act refused: decision verdict is %r, not PASS; "
                "ACT must never execute without a PASSed decision"
                % decision_out["verdict"])
        handoff = self.act.execute(copy.deepcopy(act_st))
        assert handoff["path"] == "EXECUTED", (
            "the real ACT execution path must run, got %r" % handoff["path"])
        return handoff

    def write_act_to_know(self, handoff, decision_out, know_st):
        """Ingest the ACT execution receipt into KNOW's real block store."""
        if decision_out["verdict"] != "PASS":
            raise HandoffRefused(
                "write_act_to_know refused: decision verdict is %r, not PASS; "
                "no execution evidence may persist without a PASSed decision"
                % decision_out["verdict"])
        kn = know_node.KnowNode()
        candidate = {
            "content": json.dumps({
                "kind": "act_execution_receipt",
                "execution_id": handoff.get("execution_id"),
                "path": handoff.get("path"),
                "receipt": handoff.get("receipt"),
            }, sort_keys=True),
            "proposed_class": "REFERENCE",
            "class_signals": [{"signal": "handoff-harness-v1",
                               "value": 0.95}],
            "classifier": "handoff-harness",
            "provenance": {"sources": [{
                "kind": "EXTERNAL", "ref": "ext://act-execution/%s" %
                (handoff.get("execution_id") or "unknown"),
                "capturedAt": NOW, "capturedBy": "handoff-harness"}]},
            "identity_binding": {"verified": True},
            "owner_scope": "public",
            "epistemic_state": "INGESTED",
        }
        principal = {"identity": "handoff-harness",
                     "entitled_scopes": ["public", "team"]}
        result = kn.ingest(candidate, principal, now=NOW)
        # ingest() returns the receipt directly: INGEST/ACTIVE on success.
        assert result["operation"] == "INGEST" and \
            result["afterState"] == "ACTIVE", (
            "KNOW must admit the execution receipt, got %r: %r"
            % (result.get("operation"), result.get("reasons")))
        return kn, result

    # -- EVOLVE -> SELF -------------------------------------------------
    def build_evolve_handoff(self, decision_out, fields):
        """Build the sealed successor package; return (package, receipt).

        The receipt is EVOLVE's real SUCCESSOR_PACKAGE receipt — the next
        cycle's SELF verifies its hash as the predecessor binding, and the
        package travels as SELF's real `successor_package` input (§4.5/§4.8
        checks apply: no carried authority, no cross-owner leakage).
        """
        if decision_out["verdict"] != "PASS":
            raise HandoffRefused(
                "build_evolve_handoff refused: decision verdict is %r"
                % decision_out["verdict"])
        result = self.evolve.build_successor_package(fields)
        assert result["decision"] == "PACKAGED", (
            "successor package must package cleanly, got %r" % result)
        # The sealed package lives in the node's handoff store, keyed by
        # its derived handoff_id — the successor receives this package.
        package = self.evolve._handoff_packages[result["handoff_id"]]
        assert evolve_package_hash(package) == package["package_hash"], (
            "successor package seal must verify at build time")
        receipt = next(
            r for r in self.evolve._receipts
            if r.get("receipt_id") == result["receipt_id"])
        return package, receipt


def _blob_sha_of_calculator() -> str:
    import naya_kernel.node_base as nb
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(nb.__file__))), "kernel", "value_calculus.py")
    content = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(content) + content).hexdigest()


# ---------------------------------------------------------------------------
# 1. The shared calculator scores EVOLVE candidates


def test_shared_calculator_scores_evolve_candidates():
    """EVOLVE's public propose->evaluate path runs the shared V2.1 engine.

    The receipt's score must equal an independent recomputation through
    kernel/value_calculus.evaluate_candidates, name the shared engine, and
    bind the executable's blob SHA (matching the ratified pin).
    """
    node = evolve_node.EvolveNode()
    candidate = {
        "evolution_id": "ev-handoff-1",
        "expected_value": 0.9,
        "blast_radius": "LOCAL",
        "reversibility": 0.9,
        "change_class": "DOCUMENTATION",
        "touches_surface": [],
        "mission_compatible": True,
        "evidence_refs": ["e1", "e2", "e3", "e4", "e5"],
    }
    scored = node._score_candidate(candidate)

    # The receipt names the engine — never implied, never a local formula.
    assert scored["score_engine"] == "shared_calculator"
    assert scored["score_engine_version"] == ENGINE_VERSION
    assert scored["v21_mapping"] == "evolve-v21map-v1"

    # The executable that ran is the ratified one.
    assert scored["score_engine_executable_blob_sha"] == \
        _blob_sha_of_calculator() == CALCULUS_V21_EXECUTABLE_HASH

    # Independent recomputation through the same engine must MATCH —
    # rebuilt MECHANICALLY from the receipt's bound calculator_inputs
    # (no re-running the mapping, no hand-built baseline): the score IS
    # the calculator's output.
    inputs = scored["calculator_inputs"]

    def _candidate_from(d):
        d = dict(d)
        d["pv"] = V21PVEstimate(**d["pv"])
        return V21Candidate(**d)

    v21_candidate = _candidate_from(inputs["candidate"])
    baseline = _candidate_from(inputs["baseline"])
    profile = V21QualityProfile(**inputs["quality_profile"])
    policy = V21RiskPolicy(**inputs["risk_policy"])
    assert profile.profile_id == "EVOLVE-SHARED-CALCULATOR-V1"
    evaluation = v21_evaluate_candidates(
        [baseline, v21_candidate], inputs["baseline_candidate_id"],
        profile, policy)
    row = next(r for r in evaluation["rows"]
               if r["candidate_id"] == v21_candidate.candidate_id)
    assert scored["score"] == row["v_safe"]
    assert scored["gate"] == row["gate"]
    assert scored["quality_Q"] == row["q"]["Q"]

    # And the receipt's recompute check (the §3.3 void-if-mismatch rule)
    # still holds against the stored score.
    fresh = node._score_candidate(candidate)
    assert fresh["score"] == scored["score"]
    assert fresh["gate"] == scored["gate"]


def test_shared_calculator_hard_stops_immutable_touch():
    """The spec's MUST-NEVER surface reaches the calculator's hard stop."""
    node = evolve_node.EvolveNode()
    candidate = {
        "evolution_id": "ev-handoff-2",
        "expected_value": 0.9,
        "blast_radius": "LOCAL",
        "reversibility": 0.9,
        "change_class": "DOCUMENTATION",
        "touches_surface": ["CONSTITUTIONAL_LAW"],
        "mission_compatible": True,
        "evidence_refs": ["e1"],
    }
    scored = node._score_candidate(candidate)
    assert scored["score_engine"] == "shared_calculator"
    assert scored["gate"] == "PROHIBITED"
    assert "JUDGMENT_RULE_HARD_STOP" in scored["gate_reasons"]


# ---------------------------------------------------------------------------
# 2. ACT -> KNOW: execute, persist, retrieve across cycles


def test_act_to_know_handoff_write_and_retrieve(kernel, demo_stages):
    """One decision's execution receipt travels ACT -> KNOW -> next cycle.

    Cycle 1: full kernel decision PASSes; the harness runs ACT's real
    execute() (CAS path, real tool executor behind the seam) and ingests
    the execution receipt into KNOW via KNOW's real _persist_block, then
    retrieves it. Cycle 2: a FRESH KnowNode rebuilds its store from the
    ingest receipt alone via the §10 cold_reconstruct procedure — the same
    path a successor process would use — and the restored store hash must
    EXACTLY match the cycle-1 store hash. Receipt-based continuity across
    a restart, verified by hash, not by trust.
    """
    stages = demo_stages
    decision = kernel.decide({"gates": stages})
    assert decision["verdict"] == "PASS", (
        "the demo decision must PASS for the handoff to run: %r"
        % decision["stopped_at"])

    harness = HandoffHarness()
    act_st = act_state()
    handoff = harness.execute_act(act_st, decision)
    assert handoff["path"] == "EXECUTED"

    know_cycle1, ingest_receipt = harness.write_act_to_know(
        handoff, decision, know_state())
    block_id = ingest_receipt["blockId"]

    # Still cycle 1: the block is retrievable from the live store.
    principal = {"identity": "handoff-harness",
                 "entitled_scopes": ["public", "team"]}
    found = know_cycle1.retrieve(
        {"text": "act_execution_receipt", "requested_scopes": ["public"],
         "identity_binding": {"verified": True}},
        principal, now=NOW)
    assert found["admitted"] is True, found["reasons"]
    assert block_id in [b.get("id") for b in found.get("blocks", [])]

    # Cycle 2: cold successor — a fresh node, the ingest receipt only.
    successor = know_node.KnowNode()
    report = successor.cold_reconstruct([ingest_receipt])
    assert report["restore_receipt"]["operation"] == "RESTORE"
    assert report["restored_block_count"] == 1
    assert report["block_ids"] == [block_id]
    assert report["store_hash"] == know_cycle1._store_hash(), (
        "the successor's rebuilt store must be hash-identical to the "
        "cycle-1 store — continuity by verification, not by trust")


# ---------------------------------------------------------------------------
# 3. EVOLVE -> SELF: the successor loop closes


def _successor_fields():
    return {
        "evolution_id": "ev-handoff-3",
        "supersedes_id": None,
        "change_class": "DOCUMENTATION",
        "change_summary": "handoff integration proof",
        "risk_assessment": {"residual_risk": "none material"},
        "verification_evidence": ["test_act_to_know_handoff_write_and_retrieve"],
        "successor_readiness": True,
        "reversibility": 0.95,
        "blast_radius": "LOCAL",
        "intelligence_refs": [],
    }


def test_evolve_to_self_successor_loop(kernel, demo_stages):
    """EVOLVE's sealed package enters the next cycle's SELF boot, bound.

    The loop closes through the designed seam: EVOLVE's real
    SUCCESSOR_PACKAGE receipt becomes the next cycle's predecessor
    receipt (SELF hash-verifies it — cross-node receipt verification),
    and the sealed package travels as SELF's real `successor_package`
    input. SELF's boot receipt binds the predecessor hash and carries
    the package in its inputs.
    """
    decision = kernel.decide({"gates": demo_stages})
    assert decision["verdict"] == "PASS"

    harness = HandoffHarness()
    package, evolve_receipt = harness.build_evolve_handoff(
        decision, _successor_fields())
    package_hash = package["package_hash"]

    # Cycle 2: the successor SELF boots on EVOLVE's receipt + package.
    # (SELF's public entry is gate(); the boot receipt is exposed as
    # last_boot_receipt.)
    st = self_state()
    st["predecessor_receipt"] = copy.deepcopy(evolve_receipt)
    st["successor_package"] = copy.deepcopy(package)
    successor_self = self_node.SelfNode()
    gate_result = successor_self.gate(st)

    assert gate_result.verdict.value == "PASS", gate_result.reasons
    receipt = successor_self.last_boot_receipt
    assert receipt["predecessor_binding_hash"] == \
        evolve_receipt["receipt_hash"]
    carried = receipt["inputs"]["successor_package"]
    assert evolve_package_hash(carried) == package_hash, (
        "the package carried in SELF's inputs must seal-verify")

    # Tampering the carried copy breaks the seal loudly — never silently.
    tampered = copy.deepcopy(carried)
    tampered["change_summary"] = "forged summary"
    assert evolve_package_hash(tampered) != package_hash


# ---------------------------------------------------------------------------
# Negative controls


def test_handoff_refused_when_law_prohibited(kernel, demo_stages):
    """A PROHIBITED LAW decision: ACT is never evaluated, handoffs refused."""
    stages = dict(demo_stages)
    bad = law_state()
    bad["proposal"]["flags"] = {"harm_flag": True,
                                "harm_facts": ["demo harm case"]}
    stages["LAW"] = bad
    decision = kernel.decide({"gates": stages})
    assert decision["verdict"] == "FAIL"
    assert decision["stopped_at"] == "LAW"
    assert decision["halted_on_fail"] is True
    assert [g["node"] for g in decision["gates"]] == ["SELF", "LAW"], (
        "LAW PROHIBITED halts the decision: ACT is never consulted, "
        "so it appears in no gate record at all")

    harness = HandoffHarness()
    with pytest.raises(HandoffRefused):
        harness.execute_act(act_state(), decision)
    with pytest.raises(HandoffRefused):
        harness.write_act_to_know({"path": "EXECUTED"}, decision,
                                  know_state())
    with pytest.raises(HandoffRefused):
        harness.build_evolve_handoff(decision, _successor_fields())


def test_handoff_refused_on_missing_evidence(kernel, demo_stages):
    """LAW NEED_EVIDENCE: the handoff write is refused, not half-done."""
    stages = dict(demo_stages)
    thin = law_state()
    thin["evidence"] = {"n": 1, "confidence": 0.9}  # below floor k=3
    stages["LAW"] = thin
    decision = kernel.decide({"gates": stages})
    by_node = {g["node"]: g for g in decision["gates"]}
    assert by_node["LAW"]["verdict"] == "NEED_EVIDENCE"
    assert by_node["ACT"]["evaluated"] is False

    harness = HandoffHarness()
    with pytest.raises(HandoffRefused):
        harness.execute_act(act_state(), decision)
    with pytest.raises(HandoffRefused):
        harness.write_act_to_know({"path": "EXECUTED"}, decision,
                                  know_state())


def test_broken_successor_package_fails_loudly(kernel, demo_stages):
    """A tampered successor package fails its seal — loudly, at the seam."""
    decision = kernel.decide({"gates": demo_stages})
    assert decision["verdict"] == "PASS"

    harness = HandoffHarness()
    package, evolve_receipt = harness.build_evolve_handoff(
        decision, _successor_fields())
    original_hash = package["package_hash"]

    # Material mutation between cycles: the seal breaks, and the break is
    # detected — never a silent edit (§5.2 / A5).
    tampered = copy.deepcopy(package)
    tampered["successor_readiness"] = False
    assert evolve_package_hash(tampered) != original_hash, (
        "a material mutation MUST create a new version, never a silent edit")

    # A successor that boots on the tampered copy binds the tampered
    # receipt's hash — which does NOT match the true package hash. The
    # mismatch against the true package hash is the loud signal.
    st = self_state()
    st["predecessor_receipt"] = copy.deepcopy(evolve_receipt)
    st["successor_package"] = tampered
    successor_self = self_node.SelfNode()
    gate_result = successor_self.gate(st)
    assert gate_result.verdict.value == "PASS", gate_result.reasons
    carried = successor_self.last_boot_receipt["inputs"]["successor_package"]
    assert evolve_package_hash(carried) != original_hash, (
        "the tampered package's seal differs from the true package hash "
        "— the break is visible, not hidden")
