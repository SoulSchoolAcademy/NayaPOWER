"""Law 12 pipeline wiring: the plan-time proof is USED by execute_plan,
not just issued. A stale proof refuses execution even when the Law 11
door passes — and the negative control proves the Law 12 check is the
enforcement (bypass it and the stale proof executes).
"""
import pytest

from kernel import act_pipeline as ap
from kernel.protocol.proof_receipt import UNBOUND, check_proof_validity
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="law12-wiring-test", version="1",
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


def _plan(**kw):
    plan, receipt = ap.plan_action(
        _authority(), [_candidate()], _profile(), now=NOW,
        source_sha="sha-aaa", resource_state_digest="rs-1", **kw)
    assert plan is not None, f"plan refused: {receipt.evidence}"
    return plan


def _execute(plan, now=NOW, source_sha="sha-aaa",
             resource_state_digest="rs-1", calls=None, authority=None):
    calls = calls if calls is not None else []
    auth = authority or _authority(decided_at=now - 60)
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: auth,
        now=now,
        profile=_profile(),
        source_sha=source_sha,
        resource_state_digest=resource_state_digest,
    )
    return receipt, calls


# --- plan issues the Law 12 proof ---

def test_plan_issues_bound_law12_proof():
    plan = _plan()
    proof = plan.law12_proof
    assert proof is not None
    assert proof.integrity_ok()
    assert proof.law_verdict == "ADMISSIBLE"
    assert proof.source_sha == "sha-aaa"
    assert proof.resource_state_digest == "rs-1"
    assert proof.valid_until == NOW + ap.MAX_LAW_AGE_SECONDS


def test_plan_records_unbound_fields_openly():
    plan, _ = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    assert plan is not None
    assert plan.law12_proof.source_sha == UNBOUND


# --- execute revalidates ---

def test_execute_succeeds_when_world_unchanged():
    receipt, calls = _execute(_plan(), now=NOW + 5)
    assert receipt.phase == "EXECUTION_COMPLETED" and calls


def test_execute_refuses_on_moved_sha():
    receipt, calls = _execute(_plan(), now=NOW + 5, source_sha="sha-moved")
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_PROOF_STALE in receipt.codes
    assert calls == []


def test_execute_refuses_on_changed_resource_state():
    receipt, calls = _execute(_plan(), now=NOW + 5,
                              resource_state_digest="rs-changed")
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_PROOF_STALE in receipt.codes
    assert calls == []


def test_execute_refuses_on_expired_proof_window():
    # Proof window (900s) passed but the LAW authority itself is fresh:
    # the refusal must be Law 12 staleness, not LAW staleness.
    plan = _plan()
    receipt, calls = _execute(plan, now=NOW + 901)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_PROOF_STALE in receipt.codes
    assert calls == []


def test_execute_refuses_on_unbound_sha_when_execute_binds():
    # T-19 Evidence Binding Law: plan never bound a SHA, but "write"
    # requires source_sha as a mandatory binding. The proof cannot be
    # honored — UNBOUND on a mandatory field is MISSING_BINDING, even
    # when the execute-time context binds a SHA. The plan must pin what
    # the operation requires; execute cannot backfill it.
    plan, _ = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    receipt, calls = _execute(plan, now=NOW + 5, source_sha="sha-aaa")
    assert receipt.phase == "EXECUTION_REFUSED" and not calls


# --- negative control: the Law 12 check is the enforcement ---

def test_negative_control_bypassed_check_executes_stale_proof(monkeypatch):
    """If the Law 12 validity check is bypassed (always-valid), a stale
    proof EXECUTES. This proves the check — not some other gate — is what
    refuses stale proofs in the tests above."""
    monkeypatch.setattr(ap, "check_proof_validity", lambda r, c: (True, None))
    receipt, calls = _execute(_plan(), now=NOW + 5, source_sha="sha-moved")
    assert receipt.phase == "EXECUTION_COMPLETED" and calls
