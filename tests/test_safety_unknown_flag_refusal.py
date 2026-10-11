"""Fail-closed falsifiers for unresolved critical safety flags in the ACT pipeline.

The proven defect: a candidate with safety_safe=None reached the executor.
_root cause_: kernel/act_pipeline._candidate_to_calculus never passed
`authorized`, so it defaulted False and the calculus's NEEDS_EVIDENCE
[HARD_GATE_UNKNOWN, UNKNOWN_SAFETY] verdict was masked as NEEDS_AUTHORITY
[AUTHORITY_MISSING] — which the pipeline intentionally lets through as
LAW-governed.

The fix: plan_action threads authorized=True from the LAW scope-match, so
NEEDS_EVIDENCE becomes reachable; plan_action's filter AND execute_plan's
re-gate refuse any verdict carrying HARD_GATE_UNKNOWN / UNKNOWN_* with
PLAN_SAFETY_UNKNOWN. Pure NEEDS_AUTHORITY [AUTHORITY_MISSING] still
executes (LAW-governed) — that behavior is preserved, not weakened.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import NEEDS_EVIDENCE, QualityProfile, RiskPolicy

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="unknown-flag-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="u1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.9, "evidence_sufficiency": 9.9,
                 "applicability": 9.9, "robustness": 9.9},
        confidence={"objective_fit": 0.99, "evidence_sufficiency": 0.99,
                    "applicability": 0.99, "robustness": 0.99},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated",
        proof_requirements=("execution_receipt",),
        stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


# ---------------- the proven defect, now refused ----------------

def test_plan_refuses_unknown_safety_flag():
    # THE falsifier: safety_safe=None (others proven safe) must be refused
    # at plan — it previously sailed through masked as NEEDS_AUTHORITY.
    plan, receipt = ap.plan_action(
        _authority(), [_candidate(safety_safe=None)], _profile(), now=NOW)
    assert plan is None, "unknown safety flag must never produce a plan"
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes
    assert any("UNKNOWN_SAFETY" in e for e in receipt.evidence)


def test_plan_refuses_all_unknown_hard_gate_flags():
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate(lawful=None, rights_safe=None,
                    privacy_safe=None, safety_safe=None)],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes
    joined = " ".join(receipt.evidence)
    for reason in ("HARD_GATE_UNKNOWN", "UNKNOWN_LAW", "UNKNOWN_RIGHTS",
                   "UNKNOWN_PRIVACY", "UNKNOWN_SAFETY"):
        assert reason in joined


def test_plan_refuses_mixed_unknown_and_prohibited():
    # Unknown takes the distinct code even when a prohibited candidate
    # is also present: the refusal names the knowledge gap, not just harm.
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("p-bad", safety_safe=False),
         _candidate("p-unknown", safety_safe=None)],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes
    joined = " ".join(receipt.evidence)
    assert "p-bad" in joined and "p-unknown" in joined


def test_plan_still_refuses_explicit_unsafe_flag_as_prohibited():
    # safety_safe=False keeps the PROHIBITED code (not the unknown code).
    plan, receipt = ap.plan_action(
        _authority(), [_candidate(safety_safe=False)], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert ap.PLAN_SAFETY_UNKNOWN not in receipt.codes


# ---------------- positive controls: what must still pass ----------------

def test_explicitly_safe_candidate_still_plans():
    plan, receipt = ap.plan_action(
        _authority(), [_candidate()], _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"


def test_pure_needs_authority_with_known_safe_flags_still_executes():
    # LAW-governed path preserved: explicit safe flags, but the hand-crafted
    # plan bypasses plan_action so the calculus sees authorized=False.
    # NEEDS_AUTHORITY [AUTHORITY_MISSING] must still execute.
    authority = _authority()
    plan = ap.ActionPlan(plan_id="hand-1", action=authority.action,
                         chosen=_candidate(), authority=authority,
                         candidate_scores=(), planned_at=NOW)
    calls = []
    receipt = ap.execute_plan(
        plan, executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1
    assert any("NEEDS_AUTHORITY" in e for e in receipt.evidence)


# ---------------- execute-time re-gate wiring ----------------

def test_execute_regate_refuses_unknown_flag_verdict(monkeypatch):
    # Drive the re-gate's unknown-flag branch directly: even if a verdict
    # carrying UNKNOWN_SAFETY ever reaches the re-gate, the executor fires
    # never and the refusal code is PLAN_SAFETY_UNKNOWN.
    def fake_gate(_candidate, _profile, _risk):
        return NEEDS_EVIDENCE, ["HARD_GATE_UNKNOWN", "UNKNOWN_SAFETY"], {}
    monkeypatch.setattr(ap, "gate_candidate", fake_gate)
    authority = _authority()
    plan = ap.ActionPlan(plan_id="hand-1", action=authority.action,
                         chosen=_candidate(), authority=authority,
                         candidate_scores=(), planned_at=NOW)
    calls = []
    receipt = ap.execute_plan(
        plan, executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes
    assert calls == [], "executor must never fire on unresolved safety flags"
    assert any("re-gate" in e for e in receipt.evidence)


# ---------------- unit: the unknown-flag detector ----------------

@pytest.mark.parametrize("reasons,expected", [
    (["HARD_GATE_UNKNOWN", "UNKNOWN_SAFETY"], True),
    (["UNKNOWN_LAW"], True),
    (["UNKNOWN_RIGHTS"], True),
    (["UNKNOWN_PRIVACY"], True),
    (["AUTHORITY_MISSING"], False),
    (["EVIDENCE_FLOOR"], False),
    (["TAIL_RISK:x"], False),
    ([], False),
])
def test_has_unknown_hard_gate_detector(reasons, expected):
    assert ap._has_unknown_hard_gate(reasons) is expected


def test_authority_threading_unmasks_needs_evidence():
    # Direct seam proof: the same candidate gates NEEDS_AUTHORITY when
    # authority is not threaded (masked) and NEEDS_EVIDENCE with the unknown
    # flag reasons when it is (unmasked).
    from kernel.value_calculus import gate_candidate, NEEDS_AUTHORITY
    profile, risk = _profile(), RiskPolicy()
    masked = gate_candidate(
        ap._candidate_to_calculus(_candidate(safety_safe=None)),
        profile, risk)
    assert masked[0] == NEEDS_AUTHORITY
    assert masked[1] == ["AUTHORITY_MISSING"]
    unmasked = gate_candidate(
        ap._candidate_to_calculus(_candidate(safety_safe=None), authorized=True),
        profile, risk)
    assert unmasked[0] == NEEDS_EVIDENCE
    assert "HARD_GATE_UNKNOWN" in unmasked[1]
    assert "UNKNOWN_SAFETY" in unmasked[1]
