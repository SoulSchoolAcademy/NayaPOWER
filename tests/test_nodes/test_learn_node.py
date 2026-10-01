"""LEARN node acceptance battery (CANDIDATE — mirrors spec §9 P1–P40 + golden tests)."""
import json

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes.learn_node import (
    LearnNode, DEFAULT_CONFIG, NO_AUTHORITY_GRANT,
    LEGAL_TRANSITIONS, PROMOTION_GATES,
)


RATIFIED_CONFIG = json.loads(json.dumps(DEFAULT_CONFIG))
# DEFAULT_CONFIG is the ratified V2.1 config (FLAG-001 step 4), so the
# fixture is just a deep copy with an explicit name for readability.

BEHAVIOR = {"description": "prefer provenance-check before summarising",
            "metric": "accuracy"}


_MISSING = object()


def verify_receipt(rid, lesson="check provenance first",
                   task_classes=("triage",), owner="owner-1", source="vsrc-1",
                   learning_type="BEHAVIOR_RULE", expected_behavior=_MISSING,
                   critical=False, claimed_scope=None):
    outcome = {
        "outcome_id": f"out-{rid}",
        "lesson": lesson,
        "scope": {"task_classes": list(task_classes)},
        "learning_type": learning_type,
        "expected_behavior": (dict(BEHAVIOR) if expected_behavior is _MISSING
                              else expected_behavior),
        "critical_claim": critical,
    }
    if claimed_scope is not None:
        outcome["claimed_lesson_scope"] = claimed_scope
    return {
        "receipt_id": rid,
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
        "owner_id": owner,
        "source_id": source,
        "outcome": outcome,
    }


def make_node(config=None):
    # Explicit test-scope opt-in: these tests exercise LEARN's pipeline with
    # synthetic receipts, not the VERIFY→LEARN trust seam (covered by
    # test_learn_intake_trust_seam.py). The fixture flag is the documented
    # test seam; default construction stays fail-closed.
    return LearnNode(config=config, allow_fixture_intake=True)


def ingest_and_extract(node, n, lesson="check provenance first",
                       task_classes=("triage",), owner="owner-1",
                       source="vsrc-1", **kw):
    """The intake pipeline: ingest -> extract -> reconcile. Extraction yields
    one candidate per verified receipt (the LearningKey binds the source
    outcome, §5); reconciliation applies the duplicate law so same-lesson
    candidates merge into one canonical candidate that accumulates receipts
    toward the evidence floor (§3.3, §6.3). Returns the canonical id."""
    canonical = None
    rids = []
    for i in range(n):
        rid = f"vr-{lesson[:3]}-{task_classes[0]}-{i}"
        r = node.ingest_verify_receipt(verify_receipt(
            rid, lesson=lesson, task_classes=task_classes, owner=owner,
            source=source, **kw))
        assert r["accepted"], r
        rids.append(rid)
        # Event-driven pipeline (§1.5): extract then reconcile per receipt, so
        # the first candidate becomes canonical and later identical receipts
        # merge into it via the duplicate law (no reconcile cascade).
        cid = node.extract([rid])["candidates"][0]
        res = node.reconcile(cid)
        if res["classification"] == "EXACT_DUPLICATE":
            canonical = res["refs"][0]
        elif canonical is None:
            canonical = cid
    return canonical, rids


def make_promotable(node, n=20, lesson="check provenance first",
                    task_classes=("triage",)):
    """Drive a learning to the point where every promotion conjunct is met."""
    lid, rids = ingest_and_extract(node, n, lesson=lesson,
                                   task_classes=task_classes)
    learning = node._get(lid)
    node.reconcile(lid)
    learning["proposed_holdout_tasks"] = ["holdout-q1", "holdout-q2"]
    learning["holdout_created_before_outcome"] = True
    node.design_holdout(lid)
    node.record_behavioral_evidence(lid, "holdout-q1", 0.25, related=True)
    node.record_behavioral_evidence(lid, "calc-task-9", 0.0, related=False)
    node.record_outcome_evidence(lid, 0.18, metric="accuracy")
    learning["claims_benefit"] = True
    return lid


# ---------------------------------------------------------------- NodeBase

def test_nodebase_conformance():
    node = make_node()
    assert issubclass(LearnNode, NodeBase)
    entry = node.manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-LEARN"
    assert "V1-CANDIDATE" in entry.version
    assert len(node.persisted_transitions()) > 0
    assert "verify_receipt_registry" in node.evidence_hooks()
    checks = node.authority_checks()
    assert checks[0] == NO_AUTHORITY_GRANT
    assert "no_authority_granted_by_learn" in checks[0]
    assert node.cold_reconstruct([])["determinism"]["checked"] == 0


def test_gate_unknown_action_fails():
    result = make_node().gate({"action": "teleport"})
    assert result.verdict == GateVerdict.FAIL


def test_gate_propose_candidate_without_delta_behavior_fails():
    result = make_node().gate({"action": "propose_candidate", "proposal": {}})
    assert result.verdict == GateVerdict.FAIL
    assert "NO_FUTURE_BEHAVIOR_NAMED" in result.reasons


def test_gate_propose_candidate_needs_evidence():
    result = make_node().gate({
        "action": "propose_candidate",
        "proposal": {"expected_behavior": dict(BEHAVIOR)},
    })
    assert result.verdict == GateVerdict.NEED_EVIDENCE
    assert "VERIFY_RESULT_REQUIRED" in result.reasons


# ------------------------------------------------- §1 baton: verified only

def test_intake_refuses_non_verified_receipt():
    node = make_node()
    r = node.ingest_verify_receipt({
        "receipt_id": "raw-1", "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "IN_VERIFICATION",
        "outcome": {"outcome_id": "o", "lesson": "x",
                    "scope": {"task_classes": ["triage"]}},
    })
    assert not r["accepted"]
    assert r["reason_code"] == "VERIFY_RESULT_REQUIRED"


def test_intake_refuses_wrong_node_receipt():
    node = make_node()
    r = node.ingest_verify_receipt({
        "receipt_id": "raw-2", "node_id": "NAYA-KERNEL-KNOW",
        "verification_state": "VERIFIED_PASS",
        "outcome": {"outcome_id": "o", "lesson": "x",
                    "scope": {"task_classes": ["triage"]}},
    })
    assert not r["accepted"]
    assert r["reason_code"] == "VERIFY_RESULT_REQUIRED"


def test_intake_idempotent_on_duplicate():
    node = make_node()
    r1 = node.ingest_verify_receipt(verify_receipt("vr-dup"))
    r2 = node.ingest_verify_receipt(verify_receipt("vr-dup"))
    assert r1["accepted"] and r2["duplicate"]


def test_intake_backpressure_when_pool_full():
    node = make_node(config={**json.loads(json.dumps(DEFAULT_CONFIG)),
                             "pool": {"maxSize": 1,
                                      "evidenceStalenessDays": 90}})
    node.ingest_verify_receipt(verify_receipt("vr-a"))
    node.extract(["vr-a"])
    r = node.ingest_verify_receipt(verify_receipt("vr-b"))
    assert r["backpressure"] is True
    assert any(rc["receipt_type"] == "LEARN_INTAKE_BACKPRESSURE"
               for rc in node._receipts)


def test_extract_refuses_non_verified_receipt():
    node = make_node()
    node._verify_receipts["bad"] = {"receipt_id": "bad",
                                    "node_id": "NAYA-KERNEL-VERIFY",
                                    "verification_state": "FAIL"}
    with pytest.raises(ValueError):
        node.extract(["bad"])


def test_extract_deterministic_same_receipts_same_candidates():
    node = make_node()
    node.ingest_verify_receipt(verify_receipt("vr-x1"))
    node.ingest_verify_receipt(verify_receipt("vr-x2"))
    first = node.extract(["vr-x2", "vr-x1"])["candidates"]
    second = node.extract(["vr-x1", "vr-x2"])["candidates"]
    assert first == second
    assert len(first) == 2


def test_extract_duplicate_reuses_canonical():
    # Same receipt extracted twice -> identical input -> same key, one canonical.
    node = make_node()
    node.ingest_verify_receipt(verify_receipt("vr-r1"))
    first = node.extract(["vr-r1"])["candidates"][0]
    second = node.extract(["vr-r1"])["candidates"][0]
    assert first == second


def test_duplicate_law_reuses_via_reconciliation():
    # Different outcomes, same lesson/owner/scope: the LearningKey differs
    # (sourceOutcome is part of the key, §5), so extraction yields two
    # candidates; reconciliation then applies the duplicate law — REUSE / ADD
    # EVIDENCE, never a second canonical learning (§6.3, A3).
    node = make_node()
    lid1, _ = ingest_and_extract(node, 20, lesson="same lesson")
    node.ingest_verify_receipt(verify_receipt("vr-rX", lesson="same lesson"))
    lid2 = node.extract(["vr-rX"])["candidates"][0]
    assert lid2 != lid1
    res = node.reconcile(lid2)
    assert res["classification"] == "EXACT_DUPLICATE"
    assert node._get(lid2)["state"] == "REJECTED"
    # Evidence from the duplicate joined the canonical learning:
    assert "vr-rX" in node._get(lid1)["verification_receipt_refs"]


# --------------------------------------- A12 investigation placeholders

def test_investigation_placeholder_is_inert():
    node = make_node()
    res = node.note_investigation({"lesson": "maybe the cache helps",
                                   "owner_id": "owner-1"})
    lid = res["learning_id"]
    assert res["inert"]
    with pytest.raises(ValueError):
        node.promote(lid)
    serve = node.serve(lid, "triage")
    assert serve["reason_code"] == "INVESTIGATION_PLACEHOLDER_INERT"
    eligible, codes = node.promotionEligible(lid)
    assert not eligible and "INVESTIGATION_PLACEHOLDER_INERT" in codes
    gate = node.gate({"action": "promote", "learning_id": lid})
    assert gate.verdict == GateVerdict.NEED_EVIDENCE


# --------------------------------------- P5: one success != general rule

def test_single_verified_receipt_stays_below_floor():
    node = make_node()
    lid, _ = ingest_and_extract(node, 1)
    eligible, codes = node.promotionEligible(lid)
    assert not eligible
    assert "EVIDENCE_FLOOR_NOT_MET" in codes
    learning = node._get(lid)
    # Visible, inspectable, inert: reconciled but held below the floor.
    assert learning["state"] in ("CANDIDATE", "RECONCILING")


def test_judgmental_extraction_needs_extra_independent_receipt():
    node = make_node()
    rids = []
    for i in range(20):
        rid = f"vr-j-{i}"
        node.ingest_verify_receipt(verify_receipt(rid, source="same-src"))
        rids.append(rid)
    lid = node.extract(rids, judgmental=True)["candidates"][0]
    eligible, codes = node.promotionEligible(lid)
    assert "INSUFFICIENT_INDEPENDENT_EVIDENCE" in codes


# --------------------------------------- §4 seven hard refusals

def test_no_effect_refusal():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5, expected_behavior=None)
    eligible, codes = node.promotionEligible(lid)
    assert "NO_FUTURE_BEHAVIOR_NAMED" in codes


def test_authority_smuggling_refusal():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    node._get(lid)["would_create_authority"] = True
    eligible, codes = node.promotionEligible(lid)
    assert "AUTHORITY_SMUGGLING" in codes
    result = node.promote(lid)
    assert result["refused"]


def test_constitutional_touch_refusal():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    node._get(lid)["touches_constitutional"] = True
    eligible, codes = node.promotionEligible(lid)
    assert "CONSTITUTIONAL_TOUCH" in codes


def test_recursive_self_modification_refusal():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    node._get(lid)["recursive_self_modification"] = True
    eligible, codes = node.promotionEligible(lid)
    assert "RECURSIVE_SELF_MODIFICATION" in codes


def test_open_harm_window_blocks_promotion_and_serving():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    node.report_harm_window(lid, severity=9,
                            description="delayed effect under observation")
    eligible, codes = node.promotionEligible(lid)
    assert "OPEN_HARM_WINDOW" in codes
    node._transition(node._get(lid), "TEST_REQUIRED", "test")
    node._transition(node._get(lid), "TESTING", "test")
    serve = node.serve(lid, "triage")
    assert serve["reason_code"] == "OPEN_HARM_WINDOW"
    gate = node.gate({"action": "serve", "learning_id": lid,
                      "task_class": "triage"})
    assert gate.verdict == GateVerdict.FAIL


def test_self_dealing_uncertainty_refused():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5, learning_type="CALIBRATION_UPDATE")
    learning = node._get(lid)
    learning["reduces_own_lineage_uncertainty"] = True
    learning["disjoint_verification"] = False
    eligible, codes = node.promotionEligible(lid)
    assert "SELF_DEALING_UNCERTAINTY" in codes


# --------------------------------------- P10/P11/P12/P13/P14 provenance

def test_unresolvable_evidence_ref_blocks():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    learning = node._get(lid)
    learning["evidence_refs"] = ["ev-ghost"]
    eligible, codes = node.promotionEligible(lid)
    assert "EVIDENCE_REFERENCE_UNRESOLVED" in codes


def test_forged_evidence_is_provenance_failure():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node.register_evidence("ev-fake", {"forged": True, "owner_id": "owner-1"})
    node._get(lid)["evidence_refs"] = ["ev-fake"]
    eligible, codes = node.promotionEligible(lid)
    assert "PROVENANCE_FAILURE" in codes


def test_wrong_owner_evidence_blocked():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node.register_evidence("ev-other", {"owner_id": "owner-2"})
    node._get(lid)["evidence_refs"] = ["ev-other"]
    eligible, codes = node.promotionEligible(lid)
    assert "PROVENANCE_FAILURE" in codes


def test_wrong_scope_cvo_blocked():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node.register_cvo({"cvo_id": "cvo-1", "task_classes": ["surgery"]})
    node._get(lid)["cvo_refs"] = ["cvo-1"]
    eligible, codes = node.promotionEligible(lid)
    assert "SCOPE_MISMATCH" in codes


# --------------------------------------- §6.3 reconciliation

def test_exact_duplicate_reuses_no_second_canonical():
    node = make_node()
    lid1, _ = ingest_and_extract(node, 20, lesson="same lesson")
    # A second, distinct candidate with identical lesson/owner/scope:
    other = node._new_learning(
        lesson="same lesson", learning_type="BEHAVIOR_RULE", owner_id="owner-1",
        scope={"task_classes": ["triage"]},
        applicability={"state": "APPLICABLE", "task_classes": ["triage"],
                       "limitations": []},
        source_outcome_refs=["out-other"], expected_behavior=dict(BEHAVIOR),
        verification="VERIFIED")
    res = node.reconcile(other["id"])
    assert res["classification"] == "EXACT_DUPLICATE"
    assert node._get(other["id"])["state"] == "REJECTED"


def test_contradiction_surfaces_and_preserves_both():
    node = make_node()
    lid1, _ = ingest_and_extract(node, 5, lesson="lesson alpha")
    lid2 = node._new_learning(
        lesson="lesson beta", learning_type="BEHAVIOR_RULE", owner_id="owner-1",
        scope={"task_classes": ["triage"]},
        applicability={"state": "APPLICABLE", "task_classes": ["triage"],
                       "limitations": []},
        source_outcome_refs=["out-b"], expected_behavior=dict(BEHAVIOR),
        verification="VERIFIED")["id"]
    node._get(lid2)["contradicts"] = {lid1: True}
    res = node.reconcile(lid2)
    assert res["classification"] == "CONTRADICTION"
    assert node._get(lid2)["state"] == "CONTRADICTED"
    # Both sides preserved, nothing overwritten:
    assert any(c["learning_id"] == lid1
               for c in node._get(lid2)["contradictions"])
    assert any(c["learning_id"] == lid2
               for c in node._get(lid1)["contradictions"])
    eligible, codes = node.promotionEligible(lid2)
    assert "CONTRADICTS_ACTIVE_LEARNING" in codes


def test_supersession_preserves_history():
    node = make_node(config=RATIFIED_CONFIG)
    lid1 = make_promotable(node, lesson="old lesson")
    node.promote(lid1)
    lid2 = make_promotable(node, lesson="new lesson")
    node.promote(lid2)
    res = node.supersede(lid1, lid2)
    assert res["superseded"] == lid1
    assert node._get(lid1)["state"] == "SUPERSEDED"
    assert node._get(lid2)["supersedes_learning_id"] == lid1
    # History intact: the old learning's receipts still verify.
    assert node.recompute(lid1)["result"] == "MATCH"


# --------------------------------------- P18/A2 generalization ceiling

def test_scope_expansion_without_transfer_evidence_blocked():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node._get(lid)["scope"] = {"task_classes": ["triage", "surgery"]}
    eligible, codes = node.promotionEligible(lid)
    assert "SCOPE_MISMATCH" in codes


def test_extraction_clamps_claimed_scope_to_source_scope():
    node = make_node()
    node.ingest_verify_receipt(verify_receipt(
        "vr-wide", claimed_scope={"task_classes": ["triage", "surgery"]}))
    lid = node.extract(["vr-wide"])["candidates"][0]
    learning = node._get(lid)
    assert learning["scope"]["task_classes"] == ["triage"]
    assert "SCOPE_MISMATCH" in learning["reconciliation"].get(
        "classification_note", "")


# --------------------------------------- §3.7 held-out law

def test_contaminated_holdout_is_invalid():
    node = make_node()
    lid, rids = ingest_and_extract(node, 5)
    learning = node._get(lid)
    learning["proposed_holdout_tasks"] = [f"out-{rids[0]}"]  # = source task
    plan = node.design_holdout(lid)["plan"]
    assert plan["contaminated"] is True
    assert node._get(lid)["state"] == "BLOCKED"


def test_related_heldout_supports_bounded_transfer():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    res = node.record_behavioral_evidence(lid, "holdout-q1", 0.3, related=True)
    assert not res["overgeneralization"]
    assert node._get(lid)["transfer_maturity"] == "HELD_OUT_RELATED_SUPPORTED"


def test_unrelated_effect_is_overgeneralization():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    res = node.record_behavioral_evidence(lid, "arithmetic-q", 0.4,
                                          related=False)
    assert res["overgeneralization"]
    assert any(rc["receipt_type"] == "OVERGENERALIZATION_DETECTED"
               for rc in node._receipts)
    eligible, codes = node.promotionEligible(lid)
    assert "NEGATIVE_TRANSFER_FAILED" in codes


def test_negative_transfer_boundary_required_for_promotion():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node.record_behavioral_evidence(lid, "holdout-q1", 0.2, related=True)
    eligible, codes = node.promotionEligible(lid)
    # Held-out ran, but the unrelated-refusal check never did:
    assert "NEGATIVE_TRANSFER_FAILED" in codes


def test_behavioral_claim_needs_behavioral_delta():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    node.record_behavioral_evidence(lid, "calc", 0.0, related=False)
    eligible, codes = node.promotionEligible(lid)
    assert "NO_BEHAVIORAL_DELTA" in codes or "HELDOUT_REQUIRED" in codes


def test_beneficial_claim_needs_outcome_evidence():
    node = make_node()
    lid, _ = ingest_and_extract(node, 20)
    learning = node._get(lid)
    learning["claims_benefit"] = True
    learning["proposed_holdout_tasks"] = ["hq"]
    node.design_holdout(lid)
    node.record_behavioral_evidence(lid, "hq", 0.2, related=True)
    node.record_behavioral_evidence(lid, "un", 0.0, related=False)
    eligible, codes = node.promotionEligible(lid)
    assert "NO_OUTCOME_DELTA" in codes


# --------------------------------------- golden promotion (condition 0 met)

def test_golden_promotion_to_active():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    result = node.promote(lid)
    assert result["promoted"] is True
    learning = node._get(lid)
    assert learning["state"] == "ACTIVE"
    assert learning["adoption_state"] == "ACTIVE"
    # Promotion receipt names its gates (§5) and creates no authority.
    promo = node._receipt_index[result["receipt_id"]]
    assert promo["authority_created"] is False
    assert set(PROMOTION_GATES) <= set(promo["gates_passed"])
    assert promo["handoff_to"] == "EVOLVE"
    # Promotion package validates (§7.1 trust-on-receipt).
    valid, codes = node.validate_promotion_package(
        node.promotion_package(lid))
    assert valid, codes
    # Recompute MATCH (§11.3).
    assert node.recompute(lid)["result"] == "MATCH"
    # Idempotent: second promotion returns the same receipt (P32).
    again = node.promote(lid)
    assert again["already"] is True
    assert again["receipt_id"] == result["receipt_id"]


def test_golden_serve_in_scope_only():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    in_scope = node.serve(lid, "triage")
    assert in_scope["served"] is True
    assert in_scope["applicability"] == "APPLICABLE"
    out = node.serve(lid, "arithmetic")
    assert out["served"] is False
    assert out["applicability"] == "NOT_APPLICABLE"  # never broad APPLICABLE


def test_unknown_applicability_is_not_broad_applicable():
    node = make_node()
    lid, _ = ingest_and_extract(node, 5)
    node._get(lid)["scope"] = {}
    node._transition(node._get(lid), "TEST_REQUIRED", "t")
    node._transition(node._get(lid), "TESTING", "t")
    result = node.serve(lid, "triage")
    assert result["applicability"] == "UNKNOWN"
    assert result["served"] is False


def test_stale_learning_cannot_silently_steer():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    node._get(lid)["validity_envelope"]["Environment"] = "lab-v1"
    res = node.detect_stale(lid, {"environment": "field-v2"})
    assert res["stale"] is True
    assert node._get(lid)["state"] == "REGRESSED"
    serve = node.serve(lid, "triage")
    assert serve["reason_code"] == "REGRESSION_DETECTED"
    eligible, codes = node.promotionEligible(lid)
    assert "REGRESSION_DETECTED" in codes


def test_regression_can_demote_and_retire():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    node.regress(lid, "field outcome contradicts the lesson")
    assert node._get(lid)["state"] == "REGRESSED"
    node.retire(lid, authority_ref="director:morning-brief")
    assert node._get(lid)["state"] == "RETIRED"
    assert node._get(lid)["adoption_state"] == "RETIRED"


# --------------------------------------- condition 0 satisfied (V2.1 RATIFIED)

def test_ratified_calculus_promotion_eligible_and_promotes():
    # FLAG-001 step 4: V2.1 is RATIFIED, so the default config no longer
    # raises CALCULUS_NOT_RATIFIED -- a fully-eligible learning promotes
    # autonomously instead of routing to BRIEF.
    node = make_node()  # default config: calculus V2.1 RATIFIED
    lid = make_promotable(node)
    eligible, codes = node.promotionEligible(lid)
    assert "CALCULUS_NOT_RATIFIED" not in codes
    assert eligible, codes
    result = node.promote(lid)
    assert result["promoted"] is True
    assert node._get(lid)["state"] == "ACTIVE"


def test_core_class_learning_never_autonomously_promotes():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node._get(lid)["learning_class"] = "CORE"
    result = node.promote(lid)
    assert result["routed_to_brief"] is True
    assert "CORE_CLASS_REQUIRES_DIRECTOR" in result["reason_codes"]


def test_verify_source_distrust_holds_promotions_to_brief():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.flag_verify_source_distrust("vsrc-1", "persistent measurement bias")
    eligible, codes = node.promotionEligible(lid)
    assert "VERIFY_SOURCE_DISTRUST" in codes
    result = node.promote(lid)
    assert result["routed_to_brief"] is True


# --------------------------------------- §3.5 calibration

def test_calibration_error_creates_candidate_not_mutation():
    node = make_node()
    before = json.loads(json.dumps(node._config))
    last = None
    for i in range(12):
        last = node.record_calibration("vsrc-9", 0.5, 0.9)  # bias +0.4
    assert last["candidate_created"] is not None
    cand = node._get(last["candidate_created"])
    assert cand["learning_type"] == "RECALIBRATION"
    # The active profile was never mutated:
    assert node._config == before
    assert any(rc["receipt_type"] == "VALUE_RECALIBRATION_CANDIDATE"
               for rc in node._receipts)


def test_calibration_within_tolerance_creates_nothing():
    node = make_node()
    last = None
    for _ in range(12):
        last = node.record_calibration("vsrc-ok", 0.5, 0.51)
    assert last["candidate_created"] is None


def test_gate_recalibrate_needs_authority():
    # FLAG-001 step 4: V2.1 RATIFIED -- no CALCULUS_NOT_RATIFIED code.
    # Recalibration still proposes only; authority must apply (§3.5).
    node = make_node()
    lid, _ = ingest_and_extract(node, 1, learning_type="RECALIBRATION",
                                expected_behavior=dict(BEHAVIOR))
    gate = node.gate({"action": "recalibrate", "learning_id": lid})
    assert gate.verdict == GateVerdict.NEED_EVIDENCE
    assert "CALCULUS_NOT_RATIFIED" not in gate.reasons
    assert "AUTHORITY_BOUNDARY_VIOLATION" in gate.reasons


# --------------------------------------- §4.3 / §10 Q7 routing

def test_governance_proposal_routes_to_brief_never_applies():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node, lesson="policy X caused recurring friction")
    node._get(lid)["learning_type"] = "GOVERNANCE_PROPOSAL"
    proposal = node.design_governance_proposal(lid)
    assert proposal["proposal_id"]
    out = [p for p in node._brief_outbox
           if p.get("proposal_id") == proposal["proposal_id"]]
    assert out and out[0]["status"] == "PROPOSED"
    assert out[0]["ratified_by"] is None  # lessons never silently rewrite governance
    result = node.promote(lid)
    assert result["routed_to_brief"] is True


def test_identity_learning_routes_to_brief():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node, lesson="adopt a warmer greeting style")
    node._get(lid)["touches_identity_or_personality"] = True
    result = node.promote(lid)
    assert result["routed_to_brief"] is True
    assert "IDENTITY_LEARNING_ROUTED_TO_BRIEF" in result["reason_codes"]


def test_caller_asserted_promotion_refused():
    node = make_node()
    res = node.refuse_caller_promotion({"learning_id": "ln-x",
                                        "promoted": True})
    assert not res["accepted"]
    assert res["reason_code"] == "CALLER_ASSERTED_PROMOTION"
    node2 = make_node()
    lid, _ = ingest_and_extract(node2, 20)
    node2._get(lid)["caller_asserted_verified"] = True
    eligible, codes = node2.promotionEligible(lid)
    assert "CALLER_ASSERTED_PROMOTION" in codes


# --------------------------------------- A8 compounding

def test_compounding_requires_measured_later_behavior():
    node = make_node(config=RATIFIED_CONFIG)
    earlier = make_promotable(node, lesson="earlier lesson")
    later = make_promotable(node, lesson="later lesson")
    node.promote(earlier)
    node.promote(later)
    refused = node.record_compounding(earlier, later, {"what_changed": "x"})
    assert not refused["accepted"]
    accepted = node.record_compounding(earlier, later, {
        "which_earlier_used": earlier, "which_later_depended": later,
        "what_changed": "holdout metric +0.2",
        "outcome_improved": {"metric": "accuracy", "delta": 0.2},
        "attribution_amount": 0.15, "unrelated_stable": True,
        "successor_retained": True,
    })
    assert accepted["accepted"]
    assert node._get(later)["transfer_maturity"] == "COMPOUNDING_SUPPORTED"


# --------------------------------------- lifecycle transitions

def test_illegal_transition_fails_closed():
    node = make_node()
    lid, _ = ingest_and_extract(node, 1)
    with pytest.raises(ValueError):
        node._transition(node._get(lid), "ACTIVE", "skipping the machine")


def test_persisted_transitions_cover_the_machine():
    node = make_node()
    transitions = node.persisted_transitions()
    assert "CANDIDATE->RECONCILING" in transitions
    assert "PROMOTION_READY->ACTIVE" in transitions
    assert "ACTIVE->SUPERSEDED" in transitions
    assert "ACTIVE->X" not in transitions


def test_promotion_package_defect_returned_not_applied():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    pkg = node.promotion_package(lid)
    pkg["authority_created"] = True  # defective
    valid, codes = node.validate_promotion_package(pkg)
    assert not valid
    assert "AUTHORITY_BOUNDARY_VIOLATION" in codes
    pkg2 = dict(pkg)
    pkg2.pop("package_id")
    valid2, codes2 = node.validate_promotion_package(pkg2)
    assert not valid2


# --------------------------------------- §11.3 recompute + cold successor

def test_recompute_mismatch_on_tampered_promotion():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    assert node.recompute(lid)["result"] == "MATCH"
    node._get(lid)["lesson"] = "tampered lesson"  # silent replacement attempt
    assert node.recompute(lid)["result"] == "MISMATCH"


def test_cold_reconstruct_answers_successor_questions():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    fresh = make_node(config=RATIFIED_CONFIG)
    state = fresh.cold_reconstruct(list(node._receipts))
    assert lid in state["successor_answers"]["retrieve_by_id"]
    assert state["successor_answers"]["refuse_unrelated"] is True
    assert state["successor_answers"]["fresh_authority_required"] is True
    assert state["successor_answers"]["intelligence_inherited_not_authority"] is True
    assert state["determinism"]["mismatched"] == []


def test_cold_reconstruct_flags_tampered_receipt():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    receipts = [dict(r) for r in node._receipts]
    receipts[3]["reason"] = "tampered"
    fresh = make_node(config=RATIFIED_CONFIG)
    state = fresh.cold_reconstruct(receipts)
    assert receipts[3]["receipt_id"] in state["determinism"]["mismatched"]


def test_promotion_receipt_never_creates_authority():
    node = make_node(config=RATIFIED_CONFIG)
    lid = make_promotable(node)
    node.promote(lid)
    for receipt in node._receipts:
        if receipt["receipt_type"] in ("PROMOTION", "PROMOTION_ROUTED_TO_BRIEF"):
            assert receipt["authority_created"] is False
