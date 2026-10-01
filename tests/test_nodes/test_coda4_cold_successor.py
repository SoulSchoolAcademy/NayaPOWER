"""Coda 4 — cold-successor retrieval, reconstruction and continuity (CANDIDATE).

Protocol: CODA-4/COLD-SUCCESSOR-PROTOCOL-V1.md
Baseline: PR #1216 head f58adf0826e0ea2c96d6e4a781b5191d2f4b8d5b (DRAFT, unmerged).

=============================================================================
DEFECT CS-01 (found by Coda 4, Naya 4's lane) — KNOW cold-start does not
populate the node. RETRIEVAL FROM A COLD SUCCESSOR IS CURRENTLY BLOCKED.
=============================================================================
`KnowNode.cold_reconstruct` builds state into a LOCAL `fresh = KnowNode()`
(know_node.py:1372) and never assigns `fresh.blocks` / `fresh._hash_index`
back to `self`. Measured consequences:

    report["restored_block_count"] = 1     <- the report says one block
    report["store_hash"] == cycle1 hash    <- the hash matches, exactly
    successor.blocks                      == 0    <- but the node is EMPTY
    successor.retrieve(...)["blocks"]      == []   <- nothing is retrievable

So the receipt-hash contract is honored while the usable state is absent. This
is exactly the "IMPLEMENTED != VERIFIED" and "a green-looking receipt is not
proof" case in AGENTS.md. Naya 4's existing test
`test_act_to_know_handoff_write_and_retrieve` asserts only the HASH and never
retrieves from the reconstructed node, which is why the gap is invisible there.

The tests below that need cold-reconstructed retrieval are marked
`xfail(strict=True)`: they document the real, current failure. When Naya 4
fixes CS-01 they will XPASS, and strict mode will FAIL the run, forcing this
file to be updated to the verified state rather than silently going stale.

WHAT IS PROVEN HERE, AND WHAT IS NOT
------------------------------------
  PROVEN against the LIVE cycle-1 store (documented as such, not as cold
  continuity):
    - governed retrieval with real exclusion gates
    - behavioral reuse: provenance cited BEFORE applying (PROV-BEFORE-APPLY-1)
    - unrelated-task control: control lesson resolves to a DIFFERENT block
    - stale evidence excluded, not served
    - retrieval grants no authority
    - unverified learning not promoted
    - missing evidence not concealed
    - candidate never reported as production
    - sealed handoff: successor_ready, no inherited authority, blocker omission
      INVALID, SELF refuses a package carrying authority
    - tampered receipts never trusted; AUDIT receipts never tallied as decisions

  BLOCKED / NOT CLAIMED:
    - retrieval from a COLD-RECONSTRUCTED node            (CS-01, above)
    - causal improvement — no A/B, single run, no delta claimed
    - production proof — #1216 is an unmerged draft
    - cross-process durability in a separate OS process — not attempted

Isolation honesty: the helpers below take receipts and canonical contracts
only. That is process-level isolation with a known harness, NOT a fully
independent cold agent.

Fixture note: `test_kernel_nine_node.py` declares `kernel`/`demo_stages` as
module-local fixtures (no conftest), so they are invisible here; the plain
state builders are reused verbatim and the fixtures re-declared. PROVE's gate
mutates claim state, so each decide() needs fresh, function-scoped state.

Ownership: tests + protocol only. No edits to naya_kernel/, kernel/, adapters,
migrations, or another worker's tests.
"""

import copy
import json
import os

import pytest

from test_nodes.test_kernel_nine_node import (
    NOW,
    act_state,
    connect_state,
    know_state,
    law_state,
    learn_state,
    prove_state,
    self_state,
    verify_state,
)
from naya_kernel.kernel import Kernel, verify_decision_receipt
from naya_kernel.nodes import evolve_node, know_node, self_node
from naya_kernel.nodes.evolve_node import package_hash as evolve_package_hash

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

# Predeclared behavioral-reuse constants (protocol §3) — fixed BEFORE running.
LESSON_ID = "PROV-BEFORE-APPLY-1"
LESSON_TEXT = ("Preserve provenance before applying retained intelligence; "
               "retrieval never grants authority.")
UNRELATED_LESSON_ID = "UNRELATED-REF-1"
MISSING_ID = "LESSON-THAT-WAS-NEVER-INGESTED"

PRINCIPAL = {"identity": "coda4-cold-successor",
             "entitled_scopes": ["public", "team"]}

CS01 = "CS-01: cold_reconstruct builds into a local `fresh` and never " \
       "assigns it to self; cold-start retrieval returns nothing"


# ---------------------------------------------------------------- fixtures


@pytest.fixture()
def kernel():
    return Kernel()


@pytest.fixture()
def stages(kernel):
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


def _echo_executor(tool_id, params):
    return {"status": "ok",
            "effects": "echoed: %s" % params.get("text", ""),
            "error_class": None}


# ---------------------------------------------------------------------------
# Cycle 1 — the predecessor. Its only product is receipts.


def _predecessor_cycle(kernel_obj, demo):
    """One real decision; evidence persisted through the real seams."""
    from naya_kernel.nodes import act_node

    decision = kernel_obj.decide({"gates": demo})
    assert decision["verdict"] == "PASS", decision["stopped_at"]

    act = act_node.ActNode(executor=_echo_executor)
    handoff = act.execute(copy.deepcopy(act_state()))
    assert handoff["path"] == "EXECUTED"

    kn = know_node.KnowNode()

    def _ingest(payload, klass, signal):
        return kn.ingest({
            "content": json.dumps(payload, sort_keys=True),
            "proposed_class": klass,
            "class_signals": [{"signal": signal, "value": 0.9}],
            "classifier": "coda4-protocol",
            "provenance": {"sources": [{
                "kind": "EXTERNAL", "ref": payload["ref"],
                "capturedAt": NOW, "capturedBy": "coda4-protocol"}]},
            "identity_binding": {"verified": True},
            "owner_scope": "public",
            "epistemic_state": "INGESTED",
        }, PRINCIPAL, now=NOW)

    lesson = _ingest({"lesson_id": LESSON_ID, "lesson": LESSON_TEXT,
                      "ref": "ext://coda4/predecessor/lesson"},
                     "REUSABLE", "coda4-protocol-v1")
    unrelated = _ingest({"lesson_id": UNRELATED_LESSON_ID,
                         "lesson": "Prefer the local echo tool for demos",
                         "ref": "ext://coda4/predecessor/unrelated"},
                        "REFERENCE", "coda4-control-v1")
    execution = _ingest({"kind": "act_execution_receipt",
                         "execution_id": handoff.get("execution_id"),
                         "path": handoff.get("path"),
                         "ref": "ext://act-execution/%s"
                                % handoff.get("execution_id")},
                        "REFERENCE", "coda4-protocol-v1")

    for r in (lesson, unrelated, execution):
        assert r["afterState"] == "ACTIVE", r

    receipts = [decision["decision_receipt"], handoff.get("receipt"),
                lesson, unrelated, execution]
    return {"decision": decision,
            "receipts": [r for r in receipts if r],
            "know": kn,
            "store_hash": kn._store_hash()}


# ---------------------------------------------------------------------------
# Successor behavior. Retrieval is content-matched explicitly, because
# `retrieve()` is recall-oriented: it serves blocks even at similarity 0.0 and
# marks similarity as metadata, never evidence (per its own contract).


def _retrieve(node, needle):
    return node.retrieve(
        {"text": needle, "requested_scopes": ["public"],
         "identity_binding": {"verified": True}},
        PRINCIPAL, now=NOW)


def _matching(found, needle):
    """Blocks whose CONTENT actually carries the needle.

    retrieve() is not a relevance filter — a successor must check content, and
    must never treat a served block as the lesson it asked for.
    """
    return [b for b in found.get("blocks", [])
            if needle in json.dumps(b, sort_keys=True)]


def _apply_with_provenance(node, needle):
    """Observable trace: citation happens BEFORE the block is applied."""
    found = _retrieve(node, needle)
    if not found["admitted"]:
        return {"retrieved": False, "citation_before_apply": False,
                "applied": False, "reasons": found.get("reasons")}
    served = _matching(found, needle)
    if not served:
        # Nothing carries the needle. Report the miss; never invent a match.
        return {"retrieved": True, "citation_before_apply": False,
                "applied": False, "miss": True,
                "served_count": len(found.get("blocks", [])),
                "reasons": found.get("reasons"),
                "exclusions": found.get("exclusions", [])}
    block_id = served[0]["id"]
    provenance = node.cite_provenance(block_id)  # BEFORE treating as truth
    return {"retrieved": True, "citation_before_apply": True,
            "applied": True, "block_id": block_id, "provenance": provenance,
            "exclusions": found.get("exclusions", []),
            "selector_decisions": found.get("selector_decisions", [])}


# ---------------------------------------------------------------------------
# 1. Receipt-level continuity — what IS currently verifiable


def test_cold_reconstruct_reports_a_hash_identical_store(kernel, stages):
    """The receipt contract holds: same receipts -> same reported store hash."""
    cycle1 = _predecessor_cycle(kernel, stages)
    report = know_node.KnowNode().cold_reconstruct(cycle1["receipts"])
    assert report["restored_block_count"] == 3, report
    assert report["store_hash"] == cycle1["store_hash"]
    assert report["restore_receipt"]["operation"] == "RESTORE"


@pytest.mark.xfail(strict=True, reason=CS01)
def test_cold_successor_can_retrieve_from_reconstructed_state(kernel, stages):
    """The acceptance requirement: a cold successor RETRIEVES from receipts."""
    cycle1 = _predecessor_cycle(kernel, stages)
    successor = know_node.KnowNode()
    successor.cold_reconstruct(cycle1["receipts"])

    assert successor.blocks, "the reconstructed node must hold the blocks"
    found = _retrieve(successor, LESSON_ID)
    assert _matching(found, LESSON_ID), (
        "a cold successor must retrieve the preserved lesson")


def test_kernel_cold_reconstruct_separates_audit_from_decision(
        kernel, stages):
    """An `audit-` receipt must never feed decision-verdict tallies."""
    decision = kernel.decide({"gates": stages})
    audit = kernel.gate_all({"gates": stages})
    report = kernel.cold_reconstruct([decision["decision_receipt"],
                                      audit["audit_receipt"]])
    assert report["verdicts"] == {"PASS": 1}, report
    assert audit["audit_receipt"]["receipt_id"] in \
        report["audit_receipts_verified"]
    assert audit["audit_receipt"]["receipt_id"] not in report["hash_matched"]


def test_kernel_cold_reconstruct_refuses_tampered_receipt(kernel, stages):
    """Negative control: a tampered receipt is listed, never trusted."""
    decision = kernel.decide({"gates": stages})
    tampered = copy.deepcopy(decision["decision_receipt"])
    tampered["verdict"] = "FAIL"  # forged without recomputing the hash
    report = kernel.cold_reconstruct([tampered])
    assert report["verdicts"] == {}, "a forged verdict must not be counted"
    assert len(report["hash_mismatched"]) == 1


# ---------------------------------------------------------------------------
# 2. Reconstruction with truth labels


def test_successor_reconstructs_cold_answers_with_truth_labels(
        kernel, stages):
    """Answers are derived from evidence and keep the truth laws separate."""
    cycle1 = _predecessor_cycle(kernel, stages)
    report = know_node.KnowNode().cold_reconstruct(cycle1["receipts"])

    receipt = cycle1["decision"]["decision_receipt"]
    assert verify_decision_receipt(receipt)["result"] == "MATCH"

    answers = {
        "human_director": "Shawn Vibert (AGENTS.md > HUMAN AUTHORITY)",
        "bounded_identity": "Coda 4 — cold-successor verification seat",
        "current_runtime_revision": receipt["kernel_version"],
        "what_happened": "one decision PASSed; ACT executed; KNOW persisted 3 blocks",
        "verified": ["decision receipt hash MATCH",
                     "reported store hash == cycle-1 store hash"],
        "candidate_not_ratified": True,
        "unknown": ["naya-receipt-contract/1 shape is proposed, not agreed"],
        "blocked": ["production migration application needs Director go-ahead",
                    "cold-start retrieval (CS-01)"],
        "production_proven": False,
        "next_action": "Naya 4 agrees or counters naya-receipt-contract/1",
    }
    assert report["store_hash"] == cycle1["store_hash"]
    assert set(answers["verified"]).isdisjoint(answers["unknown"])
    assert answers["production_proven"] is False
    assert "CANDIDATE" in receipt["candidate_banner"]


# ---------------------------------------------------------------------------
# 3. Behavioral reuse + unrelated-task control (live cycle-1 store)


def test_applicable_lesson_is_cited_before_it_is_applied(kernel, stages):
    """Observable reuse: provenance cited BEFORE the block is treated as truth.

    Scope note: this exercises the governed retrieval seam on the cycle-1
    store. It is NOT a claim of cold-continuity — that is CS-01, xfail above.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    trace = _apply_with_provenance(cycle1["know"], LESSON_ID)

    assert trace["retrieved"] is True
    assert trace["citation_before_apply"] is True
    assert trace["applied"] is True
    assert trace["provenance"]["sources"][0]["ref"] == \
        "ext://coda4/predecessor/lesson"


def test_unrelated_lesson_is_not_attributed_as_the_applied_lesson(
        kernel, stages):
    """Control: a different lesson must not be credited as the applied one."""
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    control = _apply_with_provenance(node, UNRELATED_LESSON_ID)
    applicable = _apply_with_provenance(node, LESSON_ID)

    assert control["applied"] is True, "the control lesson is retrievable"
    assert control["block_id"] != applicable["block_id"], (
        "the unrelated control must resolve to a DIFFERENT block than the "
        "predeclared applicable lesson — otherwise attribution is meaningless")


# ---------------------------------------------------------------------------
# 4. Negative controls


def test_stale_evidence_is_excluded_not_served(kernel, stages):
    """A withdrawn block must never be served as current."""
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    victim = _apply_with_provenance(node, LESSON_ID)["block_id"]
    node.invalidate(victim, "coda4 negative control: withdrawn",
                    PRINCIPAL, now=NOW)

    found = _retrieve(node, LESSON_ID)
    assert victim not in [b.get("id") for b in found.get("blocks", [])], (
        "an invalidated block must not be served as current")
    assert any(e.get("block_id") == victim
               for e in found.get("exclusions", [])), (
        "the exclusion must be visible, never silent")


def test_retrieval_does_not_grant_authority(kernel, stages):
    """Memory grants nothing: a successful retrieval is still not permission."""
    cycle1 = _predecessor_cycle(kernel, stages)
    trace = _apply_with_provenance(cycle1["know"], LESSON_ID)

    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    assert trace["applied"] is True, "retrieval succeeded..."
    assert package["authority_context"]["authority_inherited"] is False, \
        "...and granted nothing"
    assert package["authority_context"]["requires_reresolution"] is True


def test_unverified_learning_is_not_promoted(kernel, stages):
    """A pending reclassification must not present as current or verified.

    Measured behavior: `request_reclassification` moves the block to
    CLASSIFICATION_REVIEW, which is not in SERVABLE_STATES, so retrieval
    excludes it with a visible lifecycle reason. The unverified learning is
    withheld from a successor rather than served as truth.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    subject = _apply_with_provenance(node, LESSON_ID)["block_id"]
    outcome = node.request_reclassification(subject, "coda4 control: wants CORE",
                                            PRINCIPAL, now=NOW)
    assert outcome["afterState"] == "CLASSIFICATION_REVIEW", outcome

    block = node.blocks[subject]
    assert block.get("class") == "REUSABLE", (
        "the class must not change while the request is pending")
    assert block.get("epistemicState") != "VERIFIED", (
        "a pending reclassification must not become VERIFIED")

    found = _retrieve(node, LESSON_ID)
    assert subject not in [b.get("id") for b in found.get("blocks", [])], (
        "an unverified, under-review block must not be served as current")
    assert any(e.get("block_id") == subject and e.get("gate") == "lifecycle"
               for e in found.get("exclusions", [])), (
        "the withholding must be visible with its reason, never silent")


def test_missing_evidence_is_not_concealed(kernel, stages):
    """An absent lesson surfaces as a miss — never as confident prose."""
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    with pytest.raises(KeyError):
        node.cite_provenance("IB-DOES-NOT-EXIST")

    trace = _apply_with_provenance(node, MISSING_ID)
    assert trace["retrieved"] is True
    assert trace["applied"] is False, "a miss must not read as an application"
    assert trace["miss"] is True
    assert trace["served_count"] >= 0, "the miss must report what was served"


def test_retrieve_treats_similarity_as_metadata_not_evidence(kernel, stages):
    """retrieve() is recall-oriented; a served block is not a matched lesson."""
    cycle1 = _predecessor_cycle(kernel, stages)
    found = _retrieve(cycle1["know"], MISSING_ID)
    assert found["admitted"] is True
    assert _matching(found, MISSING_ID) == [], (
        "a zero-similarity hit must not be treated as the requested lesson")
    for b in found.get("blocks", []):
        meta = b.get("retrieval_metadata", {})
        assert meta.get("similarity_is_evidence") is False


def test_candidate_is_never_reported_as_production(kernel, stages):
    """The candidate banner must survive into every artifact."""
    cycle1 = _predecessor_cycle(kernel, stages)
    receipt = cycle1["decision"]["decision_receipt"]
    assert receipt["candidate_banner"] == \
        "CANDIDATE — NOT RATIFIED — NOT MERGED"

    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    assert package["contract_revisions"] == \
        ["naya-receipt-contract/1:PROPOSED"], (
        "the handoff must not present a proposed contract as agreed")


# ---------------------------------------------------------------------------
# 5. Handoff seal, blocker honesty, and the authority refusal


def _package_fields(**overrides):
    fields = {
        "evolution_id": "ev-coda4-1",
        "supersedes_id": None,
        "change_class": "DOCUMENTATION",
        "change_summary": "cold-successor continuity protocol",
        "risk_assessment": {"residual_risk": "none material"},
        "verification_evidence":
            ["test_applicable_lesson_is_cited_before_it_is_applied"],
        "successor_readiness": True,
        "reversibility": 0.95,
        "blast_radius": "LOCAL",
        "intelligence_refs": [],
        "learning_refs": [LESSON_ID],
        "handoff_id": "handoff-coda4-1",
        "parent_identity": "NAYA-CODA4",
        "successor_identity": "NAYA-SUCCESSOR-COLD-02",
        "kernel_revision": "rev-candidate",
        "contract_revisions": ["naya-receipt-contract/1:PROPOSED"],
        "mission": "verify cold-successor continuity",
        "current_truth": "candidate runtime only; nothing production proven",
        "unknowns": ["agreed receipt contract shape"],
        "blockers": [{"blocker_id": "CONTRACT-UNAGREED",
                      "why": "naya-receipt-contract/1 awaits Naya 4"}],
        "material_blockers_known": ["CONTRACT-UNAGREED"],
        "active_work": ["cold-successor protocol"],
        "privacy_context": {"owner_scope": "public"},
        "constraints": ["no merges", "no production writes"],
        "next_action": "Naya 4 agrees or counters naya-receipt-contract/1",
        "next_proof_requirement":
            "an agreed contract plus a re-run of this suite",
        "source_snapshot": {"main": "a726a837", "pr1216_head": "f58adf08"},
        "authority_context": {"prior_refs": []},
        "proof_refs": ["decision receipt hash MATCH"],
        "recent_outcome_refs": ["act execution EXECUTED"],
        "relationship_refs": [],
    }
    fields.update(overrides)
    return fields


def _sealed_package(ev, **overrides):
    result = ev.build_successor_package(_package_fields(**overrides))
    assert result["decision"] == "PACKAGED", result
    package = ev._handoff_packages[result["handoff_id"]]
    assert evolve_package_hash(package) == package["package_hash"], \
        "the successor package seal must verify at build time"
    receipt = next(r for r in ev._receipts
                   if r.get("receipt_id") == result["receipt_id"])
    return package, receipt


def test_sealed_package_is_successor_ready_and_inherits_no_authority():
    package, receipt = _sealed_package(evolve_node.EvolveNode())
    assert package["handoff_valid"] is True
    assert package["successor_ready"] == 1
    assert package["authority_context"]["authority_inherited"] is False
    assert receipt["node_id"] == "NAYA-KERNEL-EVOLVE"


def test_missing_material_blocker_invalidates_the_handoff():
    """Negative control: dropping a known blocker is INVALID, not degraded."""
    ev = evolve_node.EvolveNode()
    result = ev.build_successor_package(
        _package_fields(handoff_id="handoff-coda4-dropped", blockers=[],
                        material_blockers_known=["CONTRACT-UNAGREED"]))
    package = ev._handoff_packages[result["handoff_id"]]
    assert package["handoff_valid"] is False, (
        "a handoff that omits a known material blocker must be INVALID")


def test_tampered_successor_package_fails_its_seal():
    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    tampered = copy.deepcopy(package)
    tampered["next_action"] = "merge to production"
    assert evolve_package_hash(tampered) != package["package_hash"], (
        "tampering must break the seal loudly, not pass quietly")


def test_self_refuses_a_package_that_carries_authority():
    """The successor must never inherit permission through memory."""
    package, ev_receipt = _sealed_package(evolve_node.EvolveNode())

    clean = self_state()
    clean["predecessor_receipt"] = copy.deepcopy(ev_receipt)
    clean["successor_package"] = copy.deepcopy(package)
    assert self_node.SelfNode().gate(clean).verdict.value == "PASS"

    tampered = copy.deepcopy(package)
    tampered["carries_authority"] = True
    dirty = self_state()
    dirty["predecessor_receipt"] = copy.deepcopy(ev_receipt)
    dirty["successor_package"] = tampered
    refused = self_node.SelfNode().gate(dirty)
    assert refused.verdict.value != "PASS", (
        "a package carrying authority must be refused, never silently stripped")
    assert any("authority" in r.lower() for r in refused.reasons), (
        "the refusal must name the authority attempt")


@pytest.mark.xfail(strict=True, reason=CS01)
def test_second_cold_successor_rereads_improved_state(kernel, stages):
    """A SECOND fresh reader recovers the improved state from receipts alone."""
    cycle1 = _predecessor_cycle(kernel, stages)
    _first, report2 = know_node.KnowNode(), None
    report2 = _first.cold_reconstruct(cycle1["receipts"])

    ev = evolve_node.EvolveNode()
    package, ev_receipt = _sealed_package(ev)

    second = know_node.KnowNode()
    report3 = second.cold_reconstruct(cycle1["receipts"] + [ev_receipt])
    assert report3["store_hash"] == report2["store_hash"]

    # The improved state must be USABLE, not merely hash-identical.
    found = _retrieve(second, LESSON_ID)
    assert _matching(found, LESSON_ID), (
        "the second cold successor must actually retrieve the lesson")
    assert package["blockers"][0]["blocker_id"] == "CONTRACT-UNAGREED"


def test_second_successor_sees_same_next_action_and_blocker():
    """The sealed handoff states exactly one next action and its blocker."""
    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    assert package["next_action"] == \
        "Naya 4 agrees or counters naya-receipt-contract/1"
    assert [b["blocker_id"] for b in package["blockers"]] == \
        ["CONTRACT-UNAGREED"]
    assert package["unknowns"] == ["agreed receipt contract shape"]


# ---------------------------------------------------------------------------
# 6. Protocol artifact present (human reproducibility)


def test_protocol_document_exists_and_names_its_scope():
    path = os.path.join(REPO_ROOT, "CODA-4",
                        "COLD-SUCCESSOR-PROTOCOL-V1.md")
    assert os.path.isfile(path), "the protocol must be a real repo artifact"
    text = open(path, encoding="utf-8").read()
    for required in ["PROV-BEFORE-APPLY-1", "NOT CLAIMED",
                     "naya-receipt-contract/1", "Cold-Successor", "CS-01"]:
        assert required in text, "the protocol must state %r" % required
