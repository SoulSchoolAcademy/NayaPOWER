"""VERIFY acceptance battery: 40+ property tests mirroring
VERIFY-NODE-SPEC-CANDIDATE.md §9 (reconciled candidate; CANDIDATE — NOT RATIFIED)."""
import hashlib
import json

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import verify_node
from naya_kernel.nodes.verify_node import VerifyNode

T0 = "2026-10-01T03:00:00+00:00"

_counter = {"n": 0}


def _request(**over):
    _counter["n"] += 1
    req = {
        "verify_key": f"vk-{_counter['n']}",
        "kind": "claim_baton",
        "subject": {
            "claim": "the widget works",
            "epistemic_state": "SUPPORTED",
            "evidence": ["ev1"],
            "provenance": {"source": "lab"},
            "scope": "widget v2",
            "limitations": ["lab-only"],
            "gaps": [],
        },
        "expected_outcome": {"declared": True, "success": "widget passes"},
        "acceptance_criteria": [{"id": "c1", "critical": True, "met": True}],
        "evidence_refs": [
            {"address": "ev1", "class": "REUSABLE", "retrievable": True,
             "owner": "owner-a"},
        ],
        "reproducer_seat": {"identity": "seat-B"},
        "deciding_seat": {"identity": "seat-A"},
        "requesting_owner": "owner-a",
        "now": T0,
    }
    req.update(over)
    return req


def _clean_tier1():
    return {
        "recompute_match": True,
        "evidence_ref_integrity": True,
        "gate_conformance": True,
        "negation_probes": [
            {"probe": "try-to-fail-the-claim", "passed": False,
             "expected": "fail", "note": "attack failed as designed"},
        ],
    }


def _pass_flow(node, **over):
    """Drive a request all the way to a sealed VERIFIED_PASS receipt."""
    out = node.submit(_request(**over))
    assert not out.get("refused"), out
    rid = out["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity", "no_shared_unlogged_context",
         "own_authenticated_issued_by"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    receipt = node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                         "VERIFIED_PASS", now=T0)
    return rid, receipt


# -- NodeBase conformance -------------------------------------------------

def test_module_exposes_node_class():
    assert issubclass(verify_node.VerifyNode, NodeBase)


def test_manifest_entry():
    entry = VerifyNode().manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-VERIFY"
    assert len(entry.responsibilities) >= 5


def test_persisted_transitions_cover_state_machine():
    names = VerifyNode().persisted_transitions()
    for t in ("intake_accepted", "verification_pass", "window_hold",
              "window_closed_clean", "window_reopened", "postpass_reopened",
              "reexamination_started", "verification_fail", "cannot_verify",
              "lineage_correction", "battery_broken_reopen",
              "classification_superseded"):
        assert t in names


def test_evidence_hooks_named():
    hooks = VerifyNode().evidence_hooks()
    assert "verified_receipts" in hooks and "adversarial_results" in hooks


def test_authority_checks_declare_but_never_grant():
    checks = VerifyNode().authority_checks()
    grant_negations = [c for c in checks if "no_authority_grant" in c.lower()
                       or "no authority" in c.lower()]
    assert grant_negations, "must carry the no-authority-grant convention"
    grant_claims = [c for c in checks
                    if "grant" in c.lower() and "no_authority" not in c.lower()
                    and "never grants" not in c.lower()]
    assert not grant_claims, f"VERIFY must never claim to grant: {grant_claims}"


# -- intake (§2, §4 refusals) ---------------------------------------------

def test_submit_accepts_into_in_verification():
    node = VerifyNode()
    out = node.submit(_request())
    assert not out.get("refused")
    receipt = out["receipt"]
    assert receipt["verification_state"] == "IN_VERIFICATION"
    assert receipt["outcome_status"] == "NOT_PROVEN"
    assert receipt["acceptance_decision"] == "PENDING"
    assert receipt["causal_status"] == "NOT_CLAIMED"


def test_submit_without_verify_key_refused():
    req = _request()
    del req["verify_key"]
    out = VerifyNode().submit(req)
    assert out["refused"] and out["code"] == "R_EVIDENCE_INACCESSIBLE"


def test_submit_without_evidence_refs_refused():
    out = VerifyNode().submit(_request(evidence_refs=[]))
    assert out["refused"] and out["code"] == "R_EVIDENCE_INACCESSIBLE"


def test_submit_with_unretrievable_evidence_refused():
    out = VerifyNode().submit(_request(evidence_refs=[
        {"address": "ev1", "retrievable": False, "owner": "owner-a"}]))
    assert out["refused"] and out["code"] == "R_EVIDENCE_INACCESSIBLE"


def test_self_verification_refused_as_independence_violation():
    out = VerifyNode().submit(
        _request(reproducer_seat={"identity": "seat-A"},
                 deciding_seat={"identity": "seat-A"}))
    assert out["refused"] and out["code"] == "R_INDEPENDENCE_VIOLATION"


def test_cross_owner_evidence_without_consent_refused():
    out = VerifyNode().submit(_request(requesting_owner="owner-b"))
    assert out["refused"] and out["code"] == "R_CROSS_OWNER_LEAKAGE"


def test_cross_owner_evidence_with_consent_accepted():
    refs = [{"address": "ev1", "class": "REUSABLE", "retrievable": True,
             "owner": "owner-a", "consent_ref": "consent-7"}]
    out = VerifyNode().submit(
        _request(requesting_owner="owner-b", evidence_refs=refs))
    assert not out.get("refused")


def test_battery_truncation_refused():
    out = VerifyNode().submit(_request(truncate_battery=True))
    assert out["refused"] and out["code"] == "R_BATTERY_TRUNCATION"


def test_window_skipping_refused():
    out = VerifyNode().submit(_request(skip_window=True))
    assert out["refused"] and out["code"] == "R_WINDOW_SKIPPING"


def test_downgrade_instruction_in_request_refused_with_judgment_rule():
    out = VerifyNode().submit(_request(downgrade_instruction={
        "type": "convert_fail_to_pass", "source": "director"}))
    assert out["refused"] and out["code"] == "R_DOWNGRADE_PRESSURE"
    assert "Judgment Rule" in out["refusal"]["law_cited"]
    assert "director" in out["refusal"]["reason"]


def test_refusal_receipts_are_hash_bound():
    node = VerifyNode()
    out = node.submit(_request(evidence_refs=[]))
    body = out["refusal"]
    recomputed = hashlib.sha256(
        json.dumps({k: v for k, v in body.items() if k != "receipt_hash"},
                   sort_keys=True, separators=(",", ":"),
                   default=str).encode()).hexdigest()
    assert body["receipt_hash"] == recomputed


def test_submit_is_idempotent_on_verify_key():
    node = VerifyNode()
    req = _request()
    first = node.submit(req)
    second = node.submit(req)
    assert second["replay"] is True
    assert second["receipt_id"] == first["receipt_id"]
    # The original evidence/time boundary is preserved.
    assert second["receipt"]["issued_at"] == first["receipt"]["issued_at"]


def test_baton_missing_fields_rejected():
    node = VerifyNode()
    req = _request(kind="action_baton",
                   subject={"action_contract": "x"})  # missing 4 fields
    with pytest.raises(ValueError, match="missing baton fields"):
        node.submit(req)


def test_unknown_baton_kind_rejected():
    node = VerifyNode()
    with pytest.raises(ValueError, match="baton kind"):
        node.submit(_request(kind="oracle_baton"))


# -- independent reproduction (§2) -----------------------------------------

def test_record_reproduction_happy_path():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    rec = node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity", "no_shared_unlogged_context"], "MATCH",
        now=T0)
    assert rec["mode"] == "RECOMPUTE" and rec["result"] == "MATCH"


def test_reproduction_same_seat_rejected():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="INDEPENDENCE_VIOLATION"):
        node.record_reproduction(rid, "REPLICATE", {"identity": "seat-A"},
                                 ["different_seat_identity"], "MATCH")


def test_reproduction_without_named_dims_rejected():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="explicitly"):
        node.record_reproduction(rid, "RECOMPUTE", {"identity": "seat-B"},
                                 [], "MATCH")


def test_reproduction_unknown_mode_rejected():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="unknown reproduction mode"):
        node.record_reproduction(rid, "TELEPATHY", {"identity": "seat-B"},
                                 ["different_seat_identity"], "MATCH")


# -- adversarial battery (§2) ----------------------------------------------

def test_tier1_clean_with_negation_probe():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    rec = node.run_tier1(rid, _clean_tier1(), now=T0)
    assert rec["clean"] is True
    # Failed attacks are recorded, not hidden.
    probes = [v for v in rec["verdicts"] if v["probe"] == "try-to-fail-the-claim"]
    assert probes and probes[0]["passed"] is False


def test_tier1_without_negation_probe_is_malformed():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    battery = _clean_tier1()
    del battery["negation_probes"]
    rec = node.run_tier1(rid, battery, now=T0)
    assert rec["clean"] is False
    assert any("MALFORMED" in v.get("note", "") for v in rec["verdicts"])


def test_tier1_failing_gate_conformance_not_clean():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    battery = _clean_tier1()
    battery["gate_conformance"] = False
    assert node.run_tier1(rid, battery, now=T0)["clean"] is False


def test_tier2_negative_control_passing_declares_battery_broken():
    node = VerifyNode()
    rid, _ = _pass_flow(node)  # VERIFIED_PASS under the battery
    rid2 = node.submit(_request())["receipt_id"]
    rec = node.run_tier2(rid2, {"negative_controls": [
        {"control": "forged-evidence-must-not-verify", "passed": True,
         "note": "unexpectedly passed"}]}, now=T0)
    assert rec["battery_broken"] is True
    assert verify_node.BATTERY_ID in node._battery_broken
    # §9 item 10: everything under the battery is REOPENED; original persists.
    assert node._receipts[rid]["verification_state"] == "REOPENED"
    assert node._receipts[rid]["sealed"] is True


def test_tier2_held_when_controls_fail_as_designed():
    node = VerifyNode()
    rid2 = node.submit(_request())["receipt_id"]
    rec = node.run_tier2(rid2, {"negative_controls": [
        {"control": "forged-evidence-must-not-verify", "passed": False}]},
        now=T0)
    assert rec["battery_broken"] is False
    assert verify_node.BATTERY_ID not in node._battery_broken


# -- failure classification before any code change (§2, N4 §4.2) -------------

def test_classify_failure_happy_path():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    fc = node.classify_failure(rid, "LOGIC_DEFECT",
                               {"note": "off-by-one in gate"}, now=T0)
    assert fc["class"] == "LOGIC_DEFECT" and fc["supersedes"] is None


def test_classify_failure_unknown_class_rejected():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="not in the taxonomy"):
        node.classify_failure(rid, "VIBES_OFF")


def test_classification_superseded_with_lineage_never_edited():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    first = node.classify_failure(rid, "EVIDENCE_GAP", now=T0)
    second = node.classify_failure(rid, "LOGIC_DEFECT", now=T0)
    assert second["supersedes"] == first["id"]
    assert second["id"] != first["id"]


def test_fail_requires_classification_first():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="classified failure first"):
        node.close(rid, "FAILURE", "REJECTED", "CAUSAL_CONTRADICTED",
                   "FAIL", now=T0)
    node.classify_failure(rid, "ADVERSARIAL_COMPROMISE", now=T0)
    receipt = node.close(rid, "FAILURE", "REJECTED", "CAUSAL_CONTRADICTED",
                         "FAIL", now=T0)
    assert receipt["verification_state"] == "FAIL"
    assert receipt["sealed"] is True


def test_attempt_repair_refused():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    out = node.attempt_repair(rid)
    assert out["refused"] and out["code"] == "R_REPAIR_BY_VERIFIER"


# -- closing the four axes (§1, §3) ------------------------------------------

def test_full_pass_flow_seals_hash_bound_receipt():
    node = VerifyNode()
    rid, receipt = _pass_flow(node)
    assert receipt["verification_state"] == "VERIFIED_PASS"
    assert receipt["sealed"] is True
    recomputed = hashlib.sha256(
        json.dumps({k: v for k, v in receipt.items() if k != "receipt_hash"},
                   sort_keys=True, separators=(",", ":"),
                   default=str).encode()).hexdigest()
    assert receipt["receipt_hash"] == recomputed


def test_pass_requires_recompute_match():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.run_tier1(rid, _clean_tier1(), now=T0)
    with pytest.raises(ValueError, match="RECOMPUTE MATCH"):
        node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                   "VERIFIED_PASS", now=T0)


def test_pass_requires_clean_tier1():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    with pytest.raises(ValueError, match="tier-1 battery"):
        node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                   "VERIFIED_PASS", now=T0)


def test_critical_criteria_never_averaged_away():
    node = VerifyNode()
    req = _request(acceptance_criteria=[
        {"id": "c1", "critical": True, "met": False},
        {"id": "c2", "critical": False, "met": True}])
    rid = node.submit(req)["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    with pytest.raises(ValueError, match="never be averaged away"):
        node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                   "VERIFIED_PASS", now=T0)


def test_acceptance_neq_verification_verified_outcome_may_be_rejected():
    node = VerifyNode()
    rid, receipt = _pass_flow(node)
    # A factually verified outcome can still be REJECTED (spec §1, PDF §39).
    # Drive a second flow closed as REJECTED-but-verified.
    node2 = VerifyNode()
    rid2, _ = _pass_flow(node2)
    rec2 = node2._receipts[rid2]
    assert rec2["verification_state"] == "VERIFIED_PASS"
    # now a REJECTED acceptance on a fresh verified flow
    out = node2.submit(_request())
    rid3 = out["receipt_id"]
    node2.record_reproduction(
        rid3, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node2.run_tier1(rid3, _clean_tier1(), now=T0)
    closed = node2.close(rid3, "SUCCESS", "REJECTED", "CAUSAL_SUPPORTED",
                         "VERIFIED_PASS", now=T0)
    assert closed["verification_state"] == "VERIFIED_PASS"
    assert closed["acceptance_decision"] == "REJECTED"


def test_failure_not_proven_inconclusive_are_distinct():
    for outcome in ("FAILURE", "NOT_PROVEN", "INCONCLUSIVE"):
        node = VerifyNode()
        rid = node.submit(_request())["receipt_id"]
        node.classify_failure(rid, "UNKNOWN", now=T0)
        receipt = node.close(rid, outcome, "REJECTED", "UNVERIFIED",
                             "FAIL", now=T0)
        assert receipt["outcome_status"] == outcome
        assert receipt["verification_state"] == "FAIL"


def test_partial_success_lives_in_outcome_details():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    receipt = node.close(rid, "PARTIAL", "ACCEPTED", "CAUSAL_SUPPORTED",
                         "VERIFIED_PASS", now=T0)
    assert receipt["outcome_status"] == "PARTIAL"


def test_cannot_verify_terminal():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    receipt = node.close(rid, "NOT_PROVEN", "PENDING", "UNVERIFIED",
                         "CANNOT_VERIFY", now=T0)
    assert receipt["verification_state"] == "CANNOT_VERIFY"


def test_terminal_receipt_cannot_be_mutated():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    with pytest.raises(ValueError, match="terminal"):
        node.record_reproduction(rid, "RECOMPUTE", {"identity": "seat-B"},
                                 ["different_seat_identity"], "MATCH")
    with pytest.raises(ValueError, match="terminal"):
        node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                   "VERIFIED_PASS")


def test_escalate_for_shawn_reserved_judgment():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    receipt = node.close(rid, "SUCCESS", "PENDING_HUMAN", "CAUSAL_SUPPORTED",
                         "ESCALATE", now=T0)
    assert receipt["verification_state"] == "ESCALATE"
    assert receipt["acceptance_decision"] == "PENDING_HUMAN"


# -- observation windows (§2, §3) ---------------------------------------------

def test_delayed_harm_opens_window_and_blocks_promotion():
    node = VerifyNode()
    rid = node.submit(_request(delayed_harm_horizon="7d"))["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    receipt = node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
                         "VERIFIED_PASS", now=T0)
    assert receipt["verification_state"] == "PASS_PENDING_WINDOW"
    assert node.promotion_eligible(rid) is False


def test_window_closes_clean_to_verified_pass():
    node = VerifyNode()
    rid = node.submit(_request(delayed_harm_horizon="24h"))["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
               "VERIFIED_PASS", now=T0)
    receipt = node.close_window(rid, "clean", now=T0)
    assert receipt["verification_state"] == "VERIFIED_PASS"
    assert node.promotion_eligible(rid) is True


def test_window_contradiction_reopens_with_new_receipt():
    node = VerifyNode()
    rid = node.submit(_request(delayed_harm_horizon="24h"))["receipt_id"]
    node.record_reproduction(
        rid, "RECOMPUTE", {"identity": "seat-B"},
        ["different_seat_identity"], "MATCH", now=T0)
    node.run_tier1(rid, _clean_tier1(), now=T0)
    node.close(rid, "SUCCESS", "ACCEPTED", "CAUSAL_SUPPORTED",
               "VERIFIED_PASS", now=T0)
    new = node.close_window(rid, "contradictory",
                            {"harm": "delayed effect observed"}, now=T0)
    assert new["id"] != rid
    assert new["reopened_by"] == rid
    assert new["verification_state"] == "IN_VERIFICATION"
    # The original persists — re-examination is never an edit.
    assert node._receipts[rid]["verification_state"] == "REOPENED"


def test_close_window_only_applies_to_window_hold():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    with pytest.raises(ValueError, match="PASS_PENDING_WINDOW"):
        node.close_window(rid, "clean")


def test_reopen_of_non_eligible_state_rejected():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="REOPEN applies"):
        node.reopen(rid, "no grounds")


# -- versioning / lineage (§2) -------------------------------------------------

def test_correction_creates_new_lineage_original_persists():
    node = VerifyNode()
    rid, old = _pass_flow(node)
    new = node.correct(rid, {"note": "evidence ref re-pointed"}, now=T0)
    assert new["id"] != rid
    assert new["supersedes"] == rid
    assert new["verify_version"] == 2
    assert node._receipts[rid]["verification_state"] == "VERIFIED_PASS"


# -- recomputation law (§2, PDF §50) --------------------------------------------

def test_recompute_match_on_sealed_pass():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    assert node.recompute(rid) == "MATCH"


def test_recompute_mismatch_on_tampered_receipt():
    node = VerifyNode()
    rid, receipt = _pass_flow(node)
    receipt["outcome_status"] = "FAILURE"  # tamper after seal
    assert node.recompute(rid) == "MISMATCH"


def test_recompute_unknown_receipt():
    assert VerifyNode().recompute("vr-nope") == "UNKNOWN_RECEIPT"


def test_recompute_unsealed_is_mismatch():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    assert node.recompute(rid) == "MISMATCH"


# -- cold reconstruction (§3) ---------------------------------------------------

def test_cold_reconstruct_replays_with_determinism_report():
    node = VerifyNode()
    rid, receipt = _pass_flow(node)
    fresh = VerifyNode()
    state = fresh.cold_reconstruct([receipt])
    assert state["receipts"][rid]["verification_state"] == "VERIFIED_PASS"
    assert state["verify_keys"][receipt["verify_key"]] == rid
    assert state["determinism"]["checked"] == 1
    assert state["determinism"]["matched"] == 1


def test_cold_reconstruct_flags_tampered_receipt_for_reopen():
    node = VerifyNode()
    rid, receipt = _pass_flow(node)
    tampered = dict(receipt)
    tampered["outcome_status"] = "FAILURE"
    fresh = VerifyNode()
    state = fresh.cold_reconstruct([tampered])
    assert state["determinism"]["mismatched"] == [rid]
    assert state["reopened_on_mismatch"] == [rid]


# -- §6: VERIFY→LEARN baton + failure propagation ---------------------------------

def test_learn_baton_pass_is_may_use():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    baton = node.learn_baton(rid)
    assert baton["may_use"], "aliveness gate: VERIFY must change LEARN eligibility"
    assert not baton["must_not_generalize"]


def test_learn_baton_fail_is_must_not_generalize():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.classify_failure(rid, "LOGIC_DEFECT", now=T0)
    node.close(rid, "FAILURE", "REJECTED", "CAUSAL_CONTRADICTED",
               "FAIL", now=T0)
    baton = node.learn_baton(rid)
    assert baton["must_not_generalize"], "aliveness gate (PDF §82)"
    assert not baton["may_use"]


def test_learn_baton_requires_sealed_receipt():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="sealed"):
        node.learn_baton(rid)


def test_failure_propagation_routes_and_pattern_only():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.classify_failure(rid, "AUTHORITY_VIOLATION",
                          {"note": "seat overstep"}, now=T0)
    node.close(rid, "FAILURE", "REJECTED", "UNVERIFIED", "FAIL", now=T0)
    routes = node.failure_propagation(rid)
    assert routes["learn"]["pattern_only"] is True
    assert routes["learn"]["learning_input"] is False
    assert routes["evolve"]["failed_verifications"] == [rid]
    assert routes["self"]["known_failures"]
    assert routes["law"]["integrity_events"][0]["class"] == "AUTHORITY_VIOLATION"
    assert routes["deciding_seat"]["feedback"]


def test_failure_propagation_non_integrity_class_no_law_event():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.classify_failure(rid, "TRANSIENT_INFRA", now=T0)
    node.close(rid, "FAILURE", "REJECTED", "UNVERIFIED", "FAIL", now=T0)
    assert node.failure_propagation(rid)["law"]["integrity_events"] == []


# -- §5 CVO ----------------------------------------------------------------------

def test_build_cvo_requires_all_slots():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    with pytest.raises(ValueError, match="missing slots"):
        node.build_cvo(rid, {"known": "x"})
    cvo = node.build_cvo(rid, {s: f"{s}-value" for s in
                               verify_node.CVO_SLOTS}, now=T0)
    assert set(cvo) >= set(verify_node.CVO_SLOTS)


# -- §7 value calculus (aspirational) ---------------------------------------------

def test_record_value_computes_calibration_error_and_marks_aspirational():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    value = node.record_value(rid, 5.0, 3.0, now=T0)
    assert value["calibration_error"] == 2.0
    assert value["aspirational"] is True


# -- §8 intelligence-class preservation -------------------------------------------

def test_evidence_classes_preserved_core_never_auto_assigned():
    node = VerifyNode()
    refs = [{"address": "ev1", "class": "CORE", "retrievable": True,
             "owner": "owner-a", "consent_ref": "c-1"}]
    out = node.submit(_request(evidence_refs=refs,
                               requesting_owner="owner-b"))
    assert not out.get("refused")
    receipt = out["receipt"]
    assert receipt["evidence_classes"] == ["CORE"]
    # VERIFY preserves the class; it never auto-assigns or upgrades it.
    assert receipt["evidence_classes"][0] == refs[0]["class"]


# -- no delete, ever (§3, N4 §5.2) ---------------------------------------------------

def test_delete_receipt_always_refused():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    with pytest.raises(RuntimeError, match="no delete operation"):
        node.delete_receipt(rid)


# -- gate() surface ---------------------------------------------------------------

def test_gate_pass_on_verified_pass_receipt():
    node = VerifyNode()
    rid, _ = _pass_flow(node)
    result = node.gate({"receipt_id": rid})
    assert result.verdict == GateVerdict.PASS
    assert "A=SUCCESS" in result.reasons[0]


def test_gate_fail_on_fail_receipt():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    node.classify_failure(rid, "UNKNOWN", now=T0)
    node.close(rid, "FAILURE", "REJECTED", "UNVERIFIED", "FAIL", now=T0)
    result = node.gate({"receipt_id": rid})
    assert result.verdict == GateVerdict.FAIL


def test_gate_need_evidence_on_live_receipt():
    node = VerifyNode()
    rid = node.submit(_request())["receipt_id"]
    result = node.gate({"receipt_id": rid})
    assert result.verdict == GateVerdict.NEED_EVIDENCE


def test_gate_fail_on_downgrade_instruction_even_from_director():
    node = VerifyNode()
    result = node.gate({"downgrade_instruction": {
        "type": "skip_classification", "source": "director"}})
    assert result.verdict == GateVerdict.FAIL
    assert "Judgment Rule" in result.reasons[0]


def test_gate_need_evidence_on_request_precheck():
    node = VerifyNode()
    result = node.gate({"request": _request()})
    assert result.verdict == GateVerdict.NEED_EVIDENCE


def test_gate_fail_on_refused_request():
    node = VerifyNode()
    result = node.gate({"request": _request(evidence_refs=[])})
    assert result.verdict == GateVerdict.FAIL


def test_gate_need_evidence_on_unknown_receipt():
    assert VerifyNode().gate({"receipt_id": "vr-nope"}).verdict == GateVerdict.NEED_EVIDENCE


def test_gate_need_evidence_on_empty_state():
    assert VerifyNode().gate({}).verdict == GateVerdict.NEED_EVIDENCE


# -- downgrade pressure (§4, N4 §7.4) -----------------------------------------------

def test_downgrade_pressure_refused_and_receipted():
    node = VerifyNode()
    out = node.downgrade_pressure(
        {"type": "convert_fail_to_pass", "source": "director",
         "target_receipt": "vr-x"})
    assert out["refused"] is True
    assert out["code"] == "R_DOWNGRADE_PRESSURE"
    assert "Judgment Rule" in out["refusal"]["law_cited"]
    assert out["refusal"]["receipt_hash"]


def test_downgrade_pressure_suppress_finding_refused():
    out = VerifyNode().downgrade_pressure(
        {"type": "suppress_adversarial_finding", "source": "seat-B"})
    assert out["refused"] is True and out["code"] == "R_DOWNGRADE_PRESSURE"


def test_non_downgrade_instruction_not_refused():
    out = VerifyNode().downgrade_pressure({"type": "please_hurry"})
    assert out["refused"] is False
