"""Decision-discipline execution-gate wiring: the gate is LIVE on the path.

decision_discipline.py was the top MERGED-NOT-ENFORCED register entry: merged
bytes, zero call sites. These tests prove the wire in execute_plan is
load-bearing, not decorative:

GREEN  clean plan -> the gate adjudicates ADMISSIBLE, executor fires once,
       receipt evidence records the gate verdict.
RED    (a) the gate itself sabotaged to refuse -> EXECUTION_REFUSED, the
       executor NEVER fires (bypassing the gate cannot execute).
       (b) COMPROMISED EARLIER CHECK: the Law-11 door check is replaced
       with one reporting a fabricated ADMISSIBLE verdict on a genuinely
       prohibited typed action -> the gate re-runs law11_gate on the LIVE
       action object (not the captured door verdict) and still refuses.
       The executor never fires.

Revert restores GREEN. If the wire can be bypassed, it is not wired.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.protocol import decision_discipline as dd
from kernel.protocol.typed_action import Law11Verdict
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="execgate-wiring-test", version="1",
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


def _hand_plan(candidate, grant_id="grant-1"):
    # Hand-crafted plan bypassing plan_action (adversarial surface).
    authority = _authority(grant_id=grant_id)
    return ap.ActionPlan(
        plan_id="hand-dd-1", action=authority.action, chosen=candidate,
        authority=authority, candidate_scores=(), planned_at=NOW - 10,
    )


def _execute(plan, calls):
    return ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: _authority(),
        now=NOW,
        profile=_profile(),
    )


# --- GREEN: the wire is live on the clean path ---

def test_gate_adjudicates_admissible_on_clean_path():
    calls = []
    receipt = _execute(_hand_plan(_candidate("p-good")), calls)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == ["hand-dd-1"], "executor must fire exactly once"
    joined = " ".join(receipt.evidence)
    assert "decision-discipline execution gate: verdict ADMISSIBLE" in joined


# --- RED (a): the gate itself refuses -> nothing executes ---

def test_sabotaged_gate_blocks_execution(monkeypatch):
    # Adversary: the decision-discipline gate flips to NEEDS_EVIDENCE.
    # The wire is load-bearing only if this blocks the executor.
    def _hostile(**kwargs):
        return dd.RequirementAssessment(
            state=dd.NEEDS_EVIDENCE,
            evidence_status=dd.EVIDENCE_PENDING,
            authority_status=dd.AUTHORITY_GRANTED,
            reasons=("MISSING_EVIDENCE",),
        )
    monkeypatch.setattr(dd, "execution_gate", _hostile)
    calls = []
    receipt = _execute(_hand_plan(_candidate("p-good")), calls)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert calls == [], "executor must never fire when the gate refuses"
    assert "decision-discipline execution gate" in " ".join(receipt.evidence)


# --- RED (b): compromised earlier check — gate re-derives from the live action ---

def test_gate_rederives_from_live_action_not_captured_door_verdict(monkeypatch):
    # Threat model: the Law-11 door check is compromised (or the action
    # object mutated) to report a fabricated ADMISSIBLE verdict on a
    # genuinely prohibited action. The gate must NOT trust the captured
    # verdict: it re-runs law11_gate on the live typed action and still
    # refuses.
    def _fabricated_admissible(action, **kwargs):
        return Law11Verdict(verdict=ap.LAW11_ADMISSIBLE, reasons=(),
                            affected_interests=(), policy_version="test")
    monkeypatch.setattr(ap, "execution_door_check", _fabricated_admissible)
    # Inherently prohibited operation with CLEAN safety flags: the
    # calculus do-no-harm gate admits it (see test_law11_pipeline_wiring),
    # so only the re-derived Law 11 verdict in the decision-discipline
    # gate stands between this action and the executor.
    evil = _candidate("p-evil", action="fabricate_evidence")
    calls = []
    receipt = _execute(_hand_plan(evil), calls)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert calls == [], "executor must never fire on a prohibited action"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert "decision-discipline execution gate" in " ".join(receipt.evidence)


# --- REVERT: unpatching restores the clean path (battery invariant) ---

def test_clean_path_still_green_after_battery():
    calls = []
    receipt = _execute(_hand_plan(_candidate("p-good")), calls)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == ["hand-dd-1"]
