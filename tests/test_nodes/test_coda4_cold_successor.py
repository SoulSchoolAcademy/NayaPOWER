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
    - provenance is CITED BEFORE the block is treated as truth
      (PROV-BEFORE-APPLY-1). Citation only. See the correction below.
    - ATTRIBUTION DISCRIMINATION: the unrelated control resolves to a
      DIFFERENT block. This is NOT unrelated-task refusal.
    - stale evidence excluded, not served
    - retrieval grants no authority
    - unverified learning not promoted
    - missing evidence not concealed
    - candidate never reported as production
    - sealed handoff: successor_ready, no inherited authority, blocker omission
      INVALID, SELF refuses a package carrying authority
    - tampered receipts never trusted; AUDIT receipts never tallied as decisions
    - reconstruction is EVIDENCE-DERIVED: omitting an input artifact changes
      the reconstruction or reports UNKNOWN

  BLOCKED / NOT CLAIMED:
    - retrieval from a COLD-RECONSTRUCTED node            (CS-01, above)
    - an authorized APPLICATION of retrieved intelligence — no application
      seam is exercised here; only citation
    - behavioral reuse (behavior actually changed) — not claimed
    - unrelated-task refusal — belongs to CONNECT/PROVE, not demonstrated
    - causal improvement — no A/B, single run, no delta claimed
    - production proof — #1216 is an unmerged draft
    - cross-process durability in a separate OS process — not attempted

Isolation honesty: the helpers below take receipts and canonical contracts
only. That is OBJECT-LEVEL isolation in one process, NOT process-level
isolation, and NOT a fully independent cold agent. The harness is authored by
the same seat that writes these tests, so it is a known and biased harness.

PROOF-LANGUAGE CORRECTIONS (coordinator review, applied)
-------------------------------------------------------
1. NO TEST-AUTHORED BEHAVIOR. The trace helper used to set `applied=True`
   after a citation call and tests asserted on that flag. A flag the test
   itself wrote proves nothing about the runtime. The trace now reports
   `cited`, `citation_resolved_to`, and `application_attempted=False`, and no
   test asserts on a Boolean the helper set for its own benefit.
2. ATTRIBUTION IS NOT REFUSAL. Distinct block IDs show the control resolves
   separately. They do not show that an unrelated task is refused. This file
   does not invent a substring-based applicability engine; that decision
   belongs to CONNECT's owner.
3. DERIVED, NOT HARDCODED. Current revision, proof status, blockers and next
   action are read out of preserved artifacts. A kernel version string is not
   treated as an exact source SHA.

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


def _cite_before_trust(node, needle):
    """Observable trace: citation happens BEFORE the block is treated as truth.

    Correction (coordinator review): this helper previously returned
    `applied=True`, a Boolean it set itself immediately after a citation call.
    Asserting on that flag credits a test-authored value, not runtime behavior.

    What is honestly observable through public seams:
      - retrieval admitted / missed
      - which block actually carries the needle (attribution)
      - provenance resolved by the node's own `cite_provenance`
      - that no application occurred (`application_attempted` stays False —
        no authorized application seam exists in this lane, so nothing is
        applied and nothing is claimed to be applied)

    Applying retrieved intelligence would require an authorized operation seam.
    None is exercised here, so no application claim is made.
    """
    found = _retrieve(node, needle)
    if not found["admitted"]:
        return {"retrieved": False, "cited": False,
                "application_attempted": False, "reasons": found.get("reasons")}
    served = _matching(found, needle)
    if not served:
        # Nothing carries the needle. Report the miss; never invent a match.
        return {"retrieved": True, "cited": False,
                "application_attempted": False, "miss": True,
                "served_count": len(found.get("blocks", [])),
                "reasons": found.get("reasons"),
                "exclusions": found.get("exclusions", [])}
    block_id = served[0]["id"]
    provenance = node.cite_provenance(block_id)  # BEFORE treating as truth
    return {"retrieved": True,
            "cited": bool(provenance),
            "citation_resolved_to": block_id,
            "provenance": provenance,
            "application_attempted": False,
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


def test_cs01_defect_signature_is_exact(kernel, stages):
    """Pin CS-01 precisely, so an unrelated harness error cannot masquerade.

    Not xfail. This test PASSES today by asserting the reproduced signature
    with an exact-match guard on the failure text. An unrelated harness error
    (import failure, fixture break, wrong receipt shape) surfaces here as a
    HARD FAILURE instead of hiding inside an xfail.

    This and the xfail below are a pair: when the owner's repair lands, this
    test fails (the defect signature is gone) and the xfail XPASSes under
    strict mode. Both force a deliberate rewrite.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    successor = know_node.KnowNode()
    report = successor.cold_reconstruct(cycle1["receipts"])

    # The report is accurate about the REBUILT store...
    assert report["restored_block_count"] == 3, report
    assert report["store_hash"] == cycle1["store_hash"], (
        "the reported hash matches; that is exactly what makes CS-01 "
        "dangerous — the report is green while the node is empty")

    # ...and simultaneously silent about the NODE.
    assert successor.blocks == {}, (
        "CS-01 signature changed: self is no longer left empty. If this now "
        "fails, the owner has started installing state — reconcile this test "
        "with the acceptance test below before claiming anything.")
    assert successor._hash_index == {}, (
        "CS-01 signature changed: indexes were rebuilt onto self")

    # The guarded failure text must be the CS-01 one, nothing else.
    with pytest.raises(AssertionError, match="must hold the blocks"):
        assert successor.blocks, "the reconstructed node must hold the blocks"


CS02 = "CS-02: KnowNode.cold_reconstruct performs no receipt integrity " \
       "verification, so a forged receipt replays into state as genuine"


@pytest.mark.xfail(strict=True, reason=CS01)
def test_cold_successor_can_retrieve_from_reconstructed_state(kernel, stages):
    """THE acceptance requirement: a cold successor RETRIEVES from receipts.

    Deliberately a PLAIN assertion, so it genuinely fails today. Wrapping it in
    `pytest.raises` would make it pass and turn into an XPASS(strict) run
    failure, which is worse than an honest xfail.

    The constraint on an unrelated harness error lives in the paired
    non-xfail test `test_cs01_defect_signature_is_exact`. That test hard-fails
    if the fixture, the receipt shape, or the import path breaks, so a broken
    harness cannot hide inside this xfail: it breaks the paired test loudly
    first.
    """
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


def _derive_reconstruction(receipts, report):
    """Build the successor's answer set FROM the receipts actually supplied.

    Correction (coordinator review): the predecessor of this test hardcoded an
    `answers` dict and then asserted on its own literals. Hardcoded answers are
    fixture expectations, not evidence-derived reconstruction.

    `receipts` is the exact list handed to `cold_reconstruct` — not the
    predecessor's full set. That is what makes the derivation falsifiable: drop
    an artifact and the answer must change.

    Every value is read out of a preserved artifact or is the literal string
    "UNKNOWN" because the artifacts do not determine it. Notably
    `source_revision` is UNKNOWN: the decision receipt carries a kernel_version
    string, which is not an exact source SHA.
    """
    # Receipt shapes, measured: the decision receipt has `verdict` and
    # `decision_id` and no `operation`; ACT receipts carry `path`; KNOW
    # ingest receipts carry operation="INGEST" plus `blockId` and `seq`.
    decision = next((r for r in receipts if "verdict" in r), None)
    ingests = [r for r in receipts if r.get("operation") == "INGEST"]
    act_receipts = [r for r in receipts if r.get("path")]

    verify = verify_decision_receipt(decision) if decision else \
        {"result": "UNKNOWN"}

    return {
        "human_director": "Shawn Vibert (AGENTS.md > HUMAN AUTHORITY)",
        "bounded_identity": "Coda 4 — cold-successor verification seat",
        "source_revision": "UNKNOWN",  # version string is not a source SHA
        "kernel_version_string": (decision or {}).get(
            "kernel_version", "UNKNOWN"),
        "decision_verdict": (decision or {}).get("verdict", "UNKNOWN"),
        "act_path": (act_receipts[0]["path"]
                     if act_receipts else "UNKNOWN"),
        "ingest_count": len(ingests),
        "restored_block_count": report["restored_block_count"],
        "decision_receipt_verified": verify.get("result"),
        "candidate_banner": (decision or {}).get("candidate_banner",
                                                  "UNKNOWN"),
        "production_proven": False,
    }


def test_successor_reconstructs_from_artifacts_with_honest_unknowns(
        kernel, stages):
    """Reconstruction is derived, and unknowables are labeled UNKNOWN."""
    cycle1 = _predecessor_cycle(kernel, stages)
    report = know_node.KnowNode().cold_reconstruct(cycle1["receipts"])
    a = _derive_reconstruction(cycle1["receipts"], report)

    # Derived values must equal what the artifacts actually say.
    assert a["decision_receipt_verified"] == "MATCH", a
    assert a["decision_verdict"] == "PASS", a
    assert a["act_path"] == "EXECUTED", a
    assert a["ingest_count"] == 3, a
    assert a["restored_block_count"] == 3, a
    assert report["store_hash"] == cycle1["store_hash"]

    # Truth laws stay separate.
    assert a["production_proven"] is False
    assert "CANDIDATE" in a["candidate_banner"]
    assert "NOT RATIFIED" in a["candidate_banner"]
    assert "NOT MERGED" in a["candidate_banner"]

    # An exact source SHA is not derivable from the artifacts. Saying so
    # honestly is the point; guessing a version string as a SHA is the error.
    assert a["source_revision"] == "UNKNOWN"
    assert a["kernel_version_string"] != a["source_revision"], (
        "the kernel version string must not be passed off as a source revision")


def test_omitting_an_input_artifact_changes_the_reconstruction(
        kernel, stages):
    """Negative control for the claim above: reconstruction tracks artifacts.

    If reconstruction were hardcoded or fixture-driven, dropping an input
    receipt would leave the answer identical. Here it must change, so the
    reconstruction is genuinely evidence-derived.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    full = _derive_reconstruction(
        cycle1["receipts"],
        know_node.KnowNode().cold_reconstruct(cycle1["receipts"]))

    # Drop one KNOW ingest artifact, identified by its recorded blockId.
    ingests = [r for r in cycle1["receipts"] if r.get("operation") == "INGEST"]
    dropped_block = next(r["blockId"] for r in ingests
                         if LESSON_ID in json.dumps(r, sort_keys=True))
    reduced = [r for r in cycle1["receipts"]
               if r.get("blockId") != dropped_block]
    assert len(reduced) == len(cycle1["receipts"]) - 1

    report_reduced = know_node.KnowNode().cold_reconstruct(reduced)
    after = _derive_reconstruction(reduced, report_reduced)

    assert after["ingest_count"] == full["ingest_count"] - 1, (
        "removing a preserved ingest must change the reconstructed count")
    assert after["restored_block_count"] == \
        full["restored_block_count"] - 1, (
        "removing a preserved block must change the restored count")
    assert dropped_block not in [
        b.get("id") for b in (report_reduced.get("restored_blocks") or [])], (
        "the dropped block must not appear in the reconstruction")

    # Dropping the decision receipt: the verdict becomes genuinely unavailable
    # rather than silently inherited from the parent object.
    without_decision = [r for r in cycle1["receipts"] if "verdict" not in r]
    assert len(without_decision) == len(cycle1["receipts"]) - 1
    derived_without = _derive_reconstruction(
        without_decision,
        know_node.KnowNode().cold_reconstruct(without_decision))
    assert derived_without["decision_verdict"] == "UNKNOWN", (
        "with the PASS receipt removed, the verdict must read UNKNOWN; "
        "a hardcoded answer would still report PASS")
    assert derived_without["act_path"] == "EXECUTED", (
        "the ACT receipt is still present, so its path is still derivable")


# ---------------------------------------------------------------------------
# 3. Behavioral reuse + unrelated-task control (live cycle-1 store)


def test_predeclared_lesson_is_cited_before_it_is_treated_as_truth(
        kernel, stages):
    """PREV-RULE-1: provenance is cited BEFORE the block is treated as truth.

    Scope note: this exercises the governed retrieval seam on the cycle-1
    store. It is NOT a claim of cold-continuity — that is CS-01, xfail above.
    It is NOT a behavioral-reuse claim: no application seam exists here, so
    `application_attempted` stays False and no behavior is claimed to change.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    trace = _cite_before_trust(cycle1["know"], LESSON_ID)

    assert trace["retrieved"] is True
    assert trace["cited"] is True, "the node must resolve provenance"
    assert trace["citation_resolved_to"], (
        "citation must resolve to a concrete block id")
    assert trace["application_attempted"] is False, (
        "no authorized application seam exists in this lane; claiming an "
        "application here would be a false claim")
    assert trace["provenance"]["sources"][0]["ref"] == \
        "ext://coda4/predecessor/lesson", (
        "the citation must resolve to the SOURCE recorded at ingest, not to "
        "the block id — that is what makes it provenance rather than an echo")


def test_unrelated_control_resolves_to_a_different_block(kernel, stages):
    """ATTRIBUTION DISCRIMINATION only — this is NOT unrelated-task refusal.

    Correction (coordinator review): the predecessor of this test claimed to
    show a control lesson "is not credited as the applied lesson". Distinct
    block ids do not establish that an unrelated task is refused; refusal is
    an applicability/consumer decision owned by CONNECT's owner. No substring
    applicability engine is invented here.

    What IS proven: the control resolves to a different block than the
    predeclared lesson, with its own distinct provenance ref. Attribution is
    therefore real and separable, not an accident of a shared hit.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    control = _cite_before_trust(node, UNRELATED_LESSON_ID)
    applicable = _cite_before_trust(node, LESSON_ID)

    assert control["retrieved"] is True, "the control lesson is retrievable"
    assert control["citation_resolved_to"] != applicable["citation_resolved_to"], (
        "the unrelated control must resolve to a DIFFERENT block than the "
        "predeclared applicable lesson — otherwise attribution is meaningless")
    assert control["provenance"]["sources"][0]["ref"] != \
        applicable["provenance"]["sources"][0]["ref"], (
        "distinct provenance refs: the control is attributed to its own source")


# ---------------------------------------------------------------------------
# 4. Negative controls


def test_stale_evidence_is_excluded_not_served(kernel, stages):
    """A withdrawn block must never be served as current."""
    cycle1 = _predecessor_cycle(kernel, stages)
    node = cycle1["know"]

    victim = _cite_before_trust(node, LESSON_ID)["citation_resolved_to"]
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
    trace = _cite_before_trust(cycle1["know"], LESSON_ID)

    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    assert trace["cited"] is True, "retrieval and citation succeeded..."
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

    subject = _cite_before_trust(node, LESSON_ID)["citation_resolved_to"]
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

    trace = _cite_before_trust(node, MISSING_ID)
    assert trace["retrieved"] is True
    assert trace["cited"] is False, "a miss must not read as a citation"
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
        "blockers": [{"blocker_id": "CS-01",
                      "why": "KnowNode.cold_reconstruct does not populate self"}],
        "material_blockers_known": ["CS-01"],
        "active_work": ["cold-successor protocol"],
        "privacy_context": {"owner_scope": "public"},
        "constraints": ["no merges", "no production writes"],
        "next_action": "Naya 4 repairs CS-01 in KnowNode",
        "next_proof_requirement":
            "an agreed contract plus a re-run of this suite",
        "source_snapshot": {"main": "a726a837",
                            "pr1216_head": "4e87d4a5"},
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
                        material_blockers_known=["CS-01"]))
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
    """A SECOND fresh reader recovers the improved state from receipts alone.

    Plain assertion, so it genuinely fails today. Constraint on an unrelated
    harness error lives in the paired non-xfail tests
    `test_cs01_defect_signature_is_exact` and
    `test_omitting_an_input_artifact_changes_the_reconstruction`, which hard-fail
    if the fixtures or receipt shapes break.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    report2 = know_node.KnowNode().cold_reconstruct(cycle1["receipts"])

    package, ev_receipt = _sealed_package(evolve_node.EvolveNode())

    second = know_node.KnowNode()
    report3 = second.cold_reconstruct(cycle1["receipts"] + [ev_receipt])

    # The improved state must be USABLE, not merely hash-identical.
    found = _retrieve(second, LESSON_ID)
    assert _matching(found, LESSON_ID), (
        "the second cold successor must actually retrieve the lesson")

    assert package["blockers"][0]["blocker_id"] == "CS-01"
    assert report3["store_hash"] == report2["store_hash"] or \
        report3["restored_block_count"] >= report2["restored_block_count"]


def test_second_successor_sees_same_next_action_and_blocker():
    """The sealed handoff states exactly one next action and its blocker.

    The blocker named here is CS-01, which is the live blocker in this lane.
    The earlier draft named the receipt contract; Naya 2 withdrew that proposal
    (see #554 comment 5934656876) and answered Naya 4's seam question in
    5934779683, so it is no longer the open item.
    """
    package, _receipt = _sealed_package(evolve_node.EvolveNode())
    assert package["next_action"] == "Naya 4 repairs CS-01 in KnowNode"
    assert [b["blocker_id"] for b in package["blockers"]] == ["CS-01"]
    assert package["unknowns"] == ["agreed receipt contract shape"]


# ---------------------------------------------------------------------------
# 6. APPLICABILITY AND REFUSAL — through CONNECT's own seam, not substring
#    heuristics. This is the correction to the earlier
#    `test_unrelated_control_resolves_to_a_different_block`: distinct block ids
#    proved attribution, not refusal. Refusal is a CONNECT decision and it has a
#    real governed seam (`assess_applicability`), so this lane now exercises it
#    directly instead of standing in for it.
# --------------------------------------------------------------------------


def _active_connection():
    """A real ACTIVE CONNECT connection, via the real admission gate."""
    from naya_kernel.nodes import connect_node as _connect
    from test_nodes.test_kernel_nine_node import connect_state

    state = connect_state()
    node = _connect.ConnectNode()
    node.propose(state["connection_request"], state)
    return node, state["connection_request"]["id"]


def test_connect_admits_the_bound_purpose_and_refuses_three_others():
    """One fixed task. Applicable passes; unrelated / wrong-scope / wrong-owner
    are each refused, with a stated reason. No substring matching anywhere."""
    node, cid = _active_connection()

    # The applicable use: purpose AND scope both bound to the request.
    applicable = {"purpose": "research", "content_class": "reports",
                  "owner_scope": "shawn-scope"}
    assert node.assess_applicability(cid, applicable)["applicable"] is True

    # 1. Unrelated task: a genuinely different purpose.
    unrelated = {"purpose": "ship to production",
                 "content_class": "reports",
                 "owner_scope": "shawn-scope"}
    refused = node.assess_applicability(cid, unrelated)
    assert refused["applicable"] is False, (
        "an unrelated purpose must be refused, not merely down-ranked")
    assert "purpose" in refused["reason"], refused

    # 2. Right purpose, content class outside the scope allow-list.
    out_of_class = {"purpose": "research", "content_class": "CORE",
                    "owner_scope": "shawn-scope"}
    assert node.assess_applicability(
        cid, out_of_class)["applicable"] is False

    # 3. Right purpose and class, but a foreign owner scope. This is the
    #    cross-owner case: refusal must be structural, not incidental.
    foreign_owner = {"purpose": "research", "content_class": "reports",
                     "owner_scope": "someone-elses-scope"}
    foreign = node.assess_applicability(cid, foreign_owner)
    assert foreign["applicable"] is False
    assert "scope" in foreign["reason"], foreign

    # An unknown connection is refused rather than defaulted open.
    assert node.assess_applicability("no-such-connection", applicable)[
        "applicable"] is False


def test_connect_relevance_ranking_is_derived_not_a_substring_score():
    """ranking exists as a recorded, re-derivable decision, not a text match."""
    node, cid = _active_connection()
    ranked = node.rank_relevance({"purpose": "research",
                                  "content_classes": ["reports"]})
    assert ranked, "an active connection must be rankable"
    top = ranked[0]
    assert top["connection_id"] == cid
    assert top["factors"]["purpose_match"] == 1.0
    # Every factor is recorded, so a cold successor can re-derive the ordering.
    for factor in ("purpose_match", "scope_overlap", "ladder_rank"):
        assert factor in top["factors"], top

    # A purpose that matches nothing scores 0.0 on purpose_match — an explicit
    # factor, not an incidental string difference.
    unmatched = node.rank_relevance({"purpose": "unrelated-purpose",
                                     "content_classes": ["reports"]})
    assert unmatched[0]["factors"]["purpose_match"] == 0.0


# ---------------------------------------------------------------------------
# 7. AUTHORITY NON-INHERITANCE, measured at the successor boundary
# --------------------------------------------------------------------------


def test_no_authority_crosses_the_receipt_boundary(kernel, stages):
    """Memory, receipts, and a sealed package all grant nothing.

    Covers the specific smuggling shapes: an `authority` key inside a receipt,
    and an `authority_context` that claims inheritance.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    package, _receipt = _sealed_package(evolve_node.EvolveNode())

    # A receipt carrying an explicit authority claim changes nothing.
    smuggled = copy.deepcopy(cycle1["receipts"][2])
    smuggled["authority"] = {"approved": True, "scope": "production"}
    smuggled["authority_context"] = {"authority_inherited": True}
    node = know_node.KnowNode()
    node.cold_reconstruct(cycle1["receipts"] + [smuggled])

    found = _retrieve(node, LESSON_ID)
    assert found.get("authority") is None, (
        "retrieval must not surface an authority grant from a receipt")
    assert package["authority_context"]["authority_inherited"] is False
    assert package["authority_context"]["requires_reresolution"] is True

    # And SELF refuses a package that claims to carry authority, naming it.
    ev_receipt = _sealed_package(evolve_node.EvolveNode())[1]
    dirty_pkg = copy.deepcopy(package)
    dirty_pkg["carries_authority"] = True
    state = self_state()
    state["predecessor_receipt"] = copy.deepcopy(ev_receipt)
    state["successor_package"] = dirty_pkg
    refused = self_node.SelfNode().gate(state)
    assert refused.verdict.value != "PASS"
    assert any("authority" in r.lower() for r in refused.reasons)


CS03 = "CS-03: SELF did not re-verify the successor package seal; closed in " \
       "Naya 4 commit 9a21efda ('refuse tampered successor packages at the " \
       "SELF consuming boundary')"


@pytest.mark.xfail(strict=True, reason=CS03)
def test_successor_gate_refuses_a_tampered_package():
    """CS-03 acceptance: a package whose seal does not recompute must FAIL.

    Provenance of this finding, because I got the direction wrong first:

    1. I asserted SELF refuses a tampered package. It did not. I had assumed
       the consuming boundary re-verifies the seal.
    2. I pinned that as current behaviour with a passing test, which was the
       right call only if the gap were still open.
    3. Naya 4 then closed it in 9a21efda. I found this while re-verifying
       against the real candidate head instead of my older branch base, where
       9a21efda was not yet present.

    So this was a real defect that is now repaired, and it is xfail here
    because it was open at this branch's base. On the candidate head it
    xpasses, and strict mode fails loudly so the marker gets removed.

    Tampering `next_action`, dropping `blockers`, and claiming inherited
    authority all in one case: the seal covers the whole body, so any one
    mutation must be enough.
    """
    package, ev_receipt = _sealed_package(evolve_node.EvolveNode())

    def gate_with(pkg):
        state = self_state()
        state["predecessor_receipt"] = copy.deepcopy(ev_receipt)
        state["successor_package"] = copy.deepcopy(pkg)
        return self_node.SelfNode().gate(state)

    assert gate_with(package).verdict.value == "PASS", (
        "the untampered package is the control and must pass")

    tampered = copy.deepcopy(package)
    tampered["next_action"] = "merge #1216 to production"
    tampered["blockers"] = []
    tampered["authority_context"] = dict(package["authority_context"])
    tampered["authority_context"]["authority_inherited"] = True

    assert evolve_package_hash(tampered) != package["package_hash"], (
        "precondition: the seal detects this tampering")
    assert gate_with(tampered).verdict.value != "PASS", (
        "SELF recomputes the predecessor receipt hash but NOT the successor "
        "package seal, so a tampered next_action and dropped blockers both "
        "reach a PASS")


# ---------------------------------------------------------------------------
# 8. INTERRUPTED ACT — a fresh successor must not blindly repeat the effect
# --------------------------------------------------------------------------


def test_interrupted_act_is_not_blindly_repeated_by_a_fresh_node():
    """A preserved predecessor receipt alone does NOT stop re-execution.

    Measured, and it matters: `ActNode.execute` deduplicates against an
    execution LEDGER carried in node state or on the node instance. A successor
    that inherits only the predecessor RECEIPT has no ledger, so the executor is
    invoked again. The `execution_id` is stable, but the effect repeats.

    This is a finding about interruption recovery, not a request for a patch:
    ACT is Coda 2's failure-testing lane and Naya 4's runtime lane. The point is
    that "the id matches" must not be read as "the work did not run twice."
    """
    from naya_kernel.nodes import act_node
    from test_nodes.test_kernel_nine_node import act_state

    calls = []

    def counting_executor(tool_id, params):
        calls.append(params.get("text"))
        return {"status": "ok", "effects": "echoed", "error_class": None}

    predecessor = act_node.ActNode(executor=counting_executor)
    first = predecessor.execute(act_state())
    assert len(calls) == 1

    # A fresh node given ONLY the predecessor receipt.
    state = act_state()
    state["predecessor_receipt"] = copy.deepcopy(first["receipt"])
    successor = act_node.ActNode(executor=counting_executor)
    second = successor.execute(state)

    assert second["execution_id"] == first["execution_id"], (
        "the id is stable, which is exactly why this must be stated plainly")
    assert len(calls) == 2, (
        "a receipt alone does not prevent re-execution; the ledger does. "
        "If this ever becomes 1, the successor gained interruption recovery.")

    # Contrast: a fresh node that inherits the LEDGER does not re-execute.
    calls.clear()
    ledger_aware = act_node.ActNode(executor=counting_executor)
    ledger_aware.ledger = copy.deepcopy(predecessor.ledger)
    ledger_aware.execute(act_state())
    assert len(calls) == 0, (
        "with the execution ledger preserved, the effect is not repeated")


# ---------------------------------------------------------------------------
# 9. STALE HANDOFF AND STALE SOURCE — negative controls
# --------------------------------------------------------------------------


def test_superseded_checkpoint_is_treated_as_stale_not_current():
    """A valid-hash but superseded checkpoint must read UNKNOWN, not current.

    Located by inspection: SELF records the staleness in its emitted
    `last_boot_receipt.truth_boundary`, not on the GateResult (which carries
    only verdict and reasons). Asserting on where it actually lives, since a
    check against the wrong field would pass vacuously.
    """
    import naya_kernel.nodes.self_node as self_mod

    package, ev_receipt = _sealed_package(evolve_node.EvolveNode())
    payload = {"content": "current continuation state"}
    node = self_node.SelfNode()

    def boundary(superseded):
        state = self_state()
        state["predecessor_receipt"] = copy.deepcopy(ev_receipt)
        state["successor_package"] = copy.deepcopy(package)
        checkpoint = {"hash": self_mod._sha256(payload), "payload": payload}
        if superseded:
            checkpoint["superseded_by"] = "b" * 64
        state["checkpoint"] = checkpoint
        node.gate(state)
        return node.last_boot_receipt["truth_boundary"]

    current = boundary(False)
    stale = boundary(True)

    assert "checkpoint_content: superseded" not in current["unknown"], (
        "a current checkpoint must not be reported as superseded")
    assert any("superseded" in u for u in stale["unknown"]), (
        "a superseded checkpoint must surface as UNKNOWN, never as current "
        "state: %s" % stale)


def test_tampering_the_package_breaks_its_seal():
    """The seal must detect tampering. This is EVOLVE's own contract.

    Scope correction: I first asserted that SELF would also refuse the tampered
    package, having assumed the successor boundary re-verifies the seal. It does
    not — SELF checks `carries_authority` and the predecessor receipt hash, but
    never recomputes `package_hash`. So that assertion was wrong about the
    system, and I am not turning an unverified guess into a failing test.

    The real finding, verified below in
    `test_successor_gate_does_not_reverify_the_package_seal`, is that gap.
    """
    package, _receipt = _sealed_package(evolve_node.EvolveNode())

    tampered = copy.deepcopy(package)
    tampered["next_action"] = "merge #1216 to production"
    tampered["blockers"] = []

    assert evolve_package_hash(tampered) != package["package_hash"], (
        "the seal must detect tampering at the producing side")


# ---------------------------------------------------------------------------
# 10. CS-02 — KNOW replay trusts its inputs unconditionally
# --------------------------------------------------------------------------


@pytest.mark.xfail(strict=True, reason=CS02)
def test_know_cold_reconstruct_verifies_receipt_integrity(kernel, stages):
    """CS-02 acceptance: a forged KNOW receipt must NOT be replayed.

    `Kernel.cold_reconstruct` reports `hash_matched` / `hash_mismatched`.
    `KnowNode.cold_reconstruct` performs no integrity verification at all, so a
    forged receipt replays into state as if genuine. Pinned xfail(strict) until
    the owner repairs it; CS-01 blocks the restore path independently.
    """
    cycle1 = _predecessor_cycle(kernel, stages)
    ingests = [r for r in cycle1["receipts"] if r.get("operation") == "INGEST"]
    forged = copy.deepcopy(ingests[0])
    forged["block_snapshot"]["provenance"]["sources"][0]["ref"] = \
        "ext://coda4/FORGED"

    report = know_node.KnowNode().cold_reconstruct([forged])

    assert "hash_mismatched" in report, (
        "a forged receipt must be listed as mismatched; KNOW reports no "
        "integrity fields at all: %s" % sorted(report))
    assert "hash_matched" in report, (
        "the restore must report which receipts it actually verified")
    assert report.get("hash_matched") == [], (
        "a forged receipt must never appear as verified")


# ---------------------------------------------------------------------------
# 11. Protocol artifact present (human reproducibility)


def test_protocol_document_exists_and_names_its_scope():
    path = os.path.join(REPO_ROOT, "CODA-4",
                        "COLD-SUCCESSOR-PROTOCOL-V1.md")
    assert os.path.isfile(path), "the protocol must be a real repo artifact"
    text = open(path, encoding="utf-8").read()
    for required in ["PROV-BEFORE-APPLY-1", "NOT CLAIMED",
                     "naya-receipt-contract/1", "Cold-Successor", "CS-01"]:
        assert required in text, "the protocol must state %r" % required
