"""Law 11 pipeline wiring: the gate is USED by the pipeline, not just present.

These tests prove the validator's check: a prohibited action actually gets
blocked when flowing through plan_action -> execute_plan. The Law 11 gate
library existing is not enough; the pipeline must walk through the door.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="law11-wiring-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0,
                 "reversibility": 9.0, "blast_containment": 9.0,
                 "simplicity": 9.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                    "applicability": 0.9, "robustness": 0.9,
                    "reversibility": 0.9, "blast_containment": 0.9,
                    "simplicity": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _execute(plan, authority=None, calls=None):
    """Run execute_plan with a recording executor."""
    calls = calls if calls is not None else []
    auth = authority or _authority()
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: auth,
        now=NOW,
        profile=_profile(),
    )
    return receipt, calls


# --- plan_action: Law 11 filter ---

def test_inherently_prohibited_operation_blocked_at_plan():
    # "fabricate_evidence" has CLEAN safety flags — the calculus gate alone
    # would admit it. Law 11 must catch it by the typed operation.
    authority = _authority(action="fabricate_evidence", scope="fabricate_evidence")
    plan, receipt = ap.plan_action(
        authority, [_candidate("p-evil", action="fabricate_evidence")],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    joined = " ".join(receipt.evidence)
    assert "Law 11" in joined
    assert "p-evil" in joined


def test_prohibited_candidate_removed_but_clean_candidate_proceeds():
    # p-evil has an explicit unsafe flag -> Law 11 PROHIBITED -> removed.
    # p-good is clean -> proceeds to selection and wins.
    evil = _candidate("p-evil", safety_safe=False)
    good = _candidate("p-good")
    plan, receipt = ap.plan_action(_authority(), [evil, good],
                                   _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-good"
    assert receipt.phase == "PLAN_ACCEPTED"
    joined = " ".join(receipt.evidence)
    assert "p-evil" in joined and "Law 11" in joined


def test_unknown_safety_dimensions_flagged_not_scored():
    # rights_safe=None -> Law 11 NEEDS_EVIDENCE -> excluded from scoring.
    plan, receipt = ap.plan_action(
        _authority(), [_candidate("p-unknown", rights_safe=None)],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_NEEDS_EVIDENCE in receipt.codes
    assert "Law 11" in " ".join(receipt.evidence)


def test_explicit_unsafe_flag_prohibited_by_law11():
    plan, receipt = ap.plan_action(
        _authority(), [_candidate("p-unsafe", safety_safe=False)],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert "Law 11" in " ".join(receipt.evidence)


def test_clean_candidate_flows_through_plan():
    plan, receipt = ap.plan_action(_authority(), [_candidate("p-good")],
                                   _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"


# --- execute_plan: Law 11 door check ---

def _hand_plan(candidate, grant_id="grant-1"):
    # Hand-crafted plan bypassing plan_action (adversarial: the plan was
    # NOT filtered by the Law 11 plan gate).
    authority = _authority(grant_id=grant_id)
    return ap.ActionPlan(
        plan_id="hand-1", action=authority.action, chosen=candidate,
        authority=authority, candidate_scores=(), planned_at=NOW - 10,
    )


def test_door_blocks_handcrafted_prohibited_action():
    # A prohibited action smuggled past plan_action is caught at the door.
    evil = _candidate("p-evil", action="fabricate_evidence")
    plan = _hand_plan(evil)
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert calls == [], "executor must never fire"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert "Law 11" in " ".join(receipt.evidence)


def test_door_blocks_changed_authority():
    # Grant changed between planning and execution -> NEEDS_AUTHORITY.
    plan = _hand_plan(_candidate("p-good"), grant_id="grant-1")
    receipt, calls = _execute(plan, authority=_authority(grant_id="grant-2"))
    assert receipt.phase == "EXECUTION_REFUSED"
    assert calls == []
    assert ap.PLAN_LAW11_NEEDS_AUTHORITY in receipt.codes


def test_door_blocks_changed_target():
    # Scope changed between planning and execution -> door PROHIBITED.
    # Crafted so the pre-existing scope check PASSES (fresh.action/scope
    # match plan.action) but the door's planned-vs-current resource
    # comparison still catches the change: defense in depth.
    authority = ap.LawAuthority(action="naya_node_apply", scope="original_scope",
                                decided_at=NOW - 60, expires_at=None,
                                grant_id="grant-1")
    plan = ap.ActionPlan(
        plan_id="hand-1", action="naya_node_apply", chosen=_candidate("p-good"),
        authority=authority, candidate_scores=(), planned_at=NOW - 10,
    )
    # Fresh authority: action AND scope match plan.action so the legacy scope
    # check passes, but scope differs from the PLANNED scope -> door must
    # still stop it via TARGET_CHANGED.
    fresh = ap.LawAuthority(action="naya_node_apply", scope="naya_node_apply",
                            decided_at=NOW - 30, expires_at=None,
                            grant_id="grant-1")
    receipt, calls = _execute(plan, authority=fresh)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert calls == [], "executor must never fire"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert "TARGET_CHANGED" in " ".join(receipt.evidence)


def test_door_allows_clean_execution():
    plan = _hand_plan(_candidate("p-good"))
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == ["hand-1"]


def test_full_flow_clean_candidate_plan_to_execute():
    plan, receipt = ap.plan_action(_authority(), [_candidate("p-good")],
                                   _profile(), now=NOW)
    assert plan is not None
    exec_receipt, calls = _execute(plan)
    assert exec_receipt.phase == "EXECUTION_COMPLETED"
    assert calls == [plan.plan_id]


# --- operation inference ---

def test_infer_operation_prohibited_first():
    assert ap._infer_operation("fabricate_evidence") == "fabricate_evidence"
    assert ap._infer_operation("do_harm_now") == "harm"


def test_infer_operation_prohibited_respelling_resistant():
    # Naya 2 adversarial battery (2026-10-11): these respellings bypassed
    # the exact-substring check and gated ADMISSIBLE. A respelling is not
    # a different action — all must map to the prohibited operation.
    # Separator variations
    assert ap._infer_operation("fabricate-evidence") == "fabricate_evidence"
    assert ap._infer_operation("destroy evidence") == "destroy_evidence"
    assert ap._infer_operation("weaken test") == "weaken_test"
    assert ap._infer_operation("break.trust") == "break_trust"
    # Leet-speak / character substitutions
    assert ap._infer_operation("fabricate_ev1dence") == "fabricate_evidence"
    assert ap._infer_operation("f4bricate_evidence") == "fabricate_evidence"
    assert ap._infer_operation("weaken_te$t") == "weaken_test"
    # Morphological variants
    assert ap._infer_operation("evidence_fabrication") == "fabricate_evidence"
    assert ap._infer_operation("fabricated_evidence_report") == "fabricate_evidence"
    # Case variations
    assert ap._infer_operation("FABRICATE_EVIDENCE") == "fabricate_evidence"
    # Legitimate actions must NOT be caught by the hardening
    assert ap._infer_operation("deploy_model") == "deploy"
    assert ap._infer_operation("read_user_profile") == "read"
    assert ap._infer_operation("something_unknown") == "execute"


def test_infer_operation_keywords():
    assert ap._infer_operation("deploy_model") == "deploy"
    assert ap._infer_operation("delete_record") == "delete"
    assert ap._infer_operation("merge_branch") == "merge"


def test_infer_operation_defaults_to_execute():
    assert ap._infer_operation("naya_node_apply") == "write"  # "apply" keyword
    assert ap._infer_operation("something_unknown") == "execute"


def test_description_never_influences_verdict():
    # Same typed fields, different descriptions -> same verdict.
    c1 = _candidate("p1", action="do_something",
                    description="please deploy the update")
    c2 = _candidate("p2", action="do_something",
                    description="totally harmless routine task")
    t1 = ap._candidate_to_typed_action(c1, _authority())
    t2 = ap._candidate_to_typed_action(c2, _authority())
    from kernel.protocol.typed_action import law11_gate
    assert law11_gate(t1).verdict == law11_gate(t2).verdict
