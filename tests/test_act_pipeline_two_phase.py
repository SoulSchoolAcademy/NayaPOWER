"""Red-phase tests for the kernel ACT pipeline (two-phase governed execution).

Module under test: kernel/act_pipeline.py (does not exist yet — all fail).
Covers the ACT node contract's execution seam:
  PLAN -> re-resolve LAW -> EXECUTE, receipts at every phase transition.
"""
import re
import uuid

import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="act-test", version="1", objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence to NAYA-NODE-0001",
        quality={"objective_fit": 8.0, "evidence_sufficiency": 7.0,
                 "applicability": 8.0, "robustness": 7.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.8,
                    "applicability": 0.9, "robustness": 0.8},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated, previous state restorable",
        proof_requirements=("execution_receipt", "state_diff"),
        stakes="low",
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _plan(now=NOW):
    authority = _authority(decided_at=now - 60)
    plan, receipt = ap.plan_action(authority, [_candidate()], _profile(), now=now)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"
    return plan


def _fresh(authority):
    return lambda: authority


# ---------------- PLAN phase ----------------

def test_plan_selects_minimum_sufficient_through_value_calculus():
    authority = _authority()
    weak = _candidate("p-weak",
                      quality={"objective_fit": 4.0, "evidence_sufficiency": 4.0,
                               "applicability": 4.0, "robustness": 4.0},
                      confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                                  "applicability": 0.9, "robustness": 0.9})
    strong = _candidate("p-strong")
    plan, receipt = ap.plan_action(authority, [weak, strong], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-strong"
    assert receipt.phase == "PLAN_ACCEPTED"
    assert any("p-strong" in e for e in receipt.evidence)
    # both candidate scores recorded — the math is visible, not hidden
    assert len(plan.candidate_scores) == 2


def test_plan_rejects_scope_mismatch():
    authority = _authority(scope="some_other_scope")
    plan, receipt = ap.plan_action(authority, [_candidate()], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert "PLAN_UNAUTHORIZED_SCOPE" in receipt.codes


def test_plan_rejects_missing_expected_outcome():
    plan, receipt = ap.plan_action(_authority(), [_candidate(expected_outcome="")],
                                   _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert "PLAN_OUTCOME_UNDEFINED" in receipt.codes


def test_plan_rejects_missing_proof_requirements():
    plan, receipt = ap.plan_action(_authority(), [_candidate(proof_requirements=())],
                                   _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert "PLAN_PROOF_UNDEFINED" in receipt.codes


def test_plan_binding_carries_authority_trace():
    plan = _plan()
    assert plan.authority.grant_id == "grant-1"
    assert plan.authority.decided_at == NOW - 60
    assert plan.plan_id and re.fullmatch(r"[0-9a-f]{32}", plan.plan_id)


# ---------------- EXECUTE phase: fail-closed LAW checks ----------------

def test_execute_refuses_when_law_receipt_time_missing():
    plan = _plan()
    stale = _authority(decided_at=None)
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(stale), now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert "LAW_RECEIPT_TIME_INVALID" in receipt.codes


def test_execute_refuses_when_law_receipt_time_in_future():
    plan = _plan()
    future = _authority(decided_at=NOW + 3600)
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(future), now=NOW, profile=_profile())
    assert receipt.executed is False
    assert "LAW_RECEIPT_TIME_INVALID" in receipt.codes


def test_execute_refuses_when_authority_expired():
    plan = _plan()
    expired = _authority(expires_at=NOW - 1)  # expiry at/before clock = expired
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(expired), now=NOW, profile=_profile())
    assert receipt.executed is False
    assert "LAW_AUTHORITY_EXPIRED" in receipt.codes


def test_execute_allows_unbounded_expiry():
    plan = _plan()
    unbounded = _authority(expires_at=None)
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(unbounded), now=NOW, profile=_profile())
    assert receipt.executed is True


def test_execute_refuses_when_law_older_than_max_age():
    plan = _plan()
    old = _authority(decided_at=NOW - 901)  # DOOR-AI max is 900s
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(old), now=NOW, profile=_profile(),
                              max_law_age_seconds=900)
    assert receipt.executed is False
    assert "LAW_AUTHORITY_STALE" in receipt.codes


def test_execute_refuses_when_re_resolution_unavailable():
    plan = _plan()
    calls = []
    def executor(p):
        calls.append(p)
        return "ok"
    receipt = ap.execute_plan(plan, executor=executor,
                              re_resolve=lambda: None, now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert "LAW_RE_RESOLUTION_UNAVAILABLE" in receipt.codes
    assert calls == [], "nothing may execute without re-resolved authority"


def test_execute_rereads_live_authority_even_when_receipt_fresh():
    plan = _plan(now=NOW)
    seen = []
    def re_resolve():
        seen.append(True)
        return _authority(decided_at=NOW - 10)  # fresh live grant
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=re_resolve, now=NOW, profile=_profile())
    assert seen == [True], "live authority must be re-read before every execution"
    assert receipt.executed is True


# ---------------- EXECUTE phase: receipts ----------------

def test_execute_produces_completed_receipt_on_success():
    plan = _plan()
    receipt = ap.execute_plan(plan, executor=lambda p: "node state updated, previous state restorable",
                              re_resolve=_fresh(_authority()), now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert receipt.observed_outcome == "node state updated, previous state restorable"
    assert receipt.expected_outcome == plan.chosen.expected_outcome
    # executor claim is never trusted as verification
    assert receipt.outcome_verified is False
    assert receipt.truth_state == "UNKNOWN"


def test_execute_records_failure_receipt_without_retry():
    plan = _plan()
    calls = []
    def flaky(p):
        calls.append(p)
        raise RuntimeError("downstream timeout")
    receipt = ap.execute_plan(plan, executor=flaky,
                              re_resolve=_fresh(_authority()), now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_FAILED"
    assert receipt.executed is False
    assert len(calls) == 1, "no blind retry after failure"
    assert any("downstream timeout" in e for e in receipt.evidence)


def test_executor_claim_never_trusted_as_verification():
    plan = _plan()
    receipt = ap.execute_plan(plan, executor=lambda p: plan.chosen.expected_outcome,
                              re_resolve=_fresh(_authority()), now=NOW, profile=_profile())
    assert receipt.observed_outcome == receipt.expected_outcome
    assert receipt.outcome_verified is False
    assert receipt.truth_state == "UNKNOWN"


def test_verify_verdict_can_close_the_receipt():
    plan = _plan()
    receipt = ap.execute_plan(plan, executor=lambda p: "observed x",
                              re_resolve=_fresh(_authority()), now=NOW, profile=_profile())
    closed = ap.apply_verify_verdict(receipt, verified=True,
                                     evidence="verify-seam observed x matches expected",
                                     verifier_id="verify-seam/run-1")
    assert closed.outcome_verified is True
    assert closed.truth_state == "VERIFIED"
    assert closed.receipt_id == receipt.receipt_id  # same receipt, closed — not a new one


def test_receipt_ledger_records_every_phase_transition():
    plan = _plan()
    ledger = ap.ReceiptLedger()
    receipt = ap.execute_plan(plan, executor=lambda p: "ok",
                              re_resolve=_fresh(_authority()), now=NOW, profile=_profile(),
                              ledger=ledger)
    phases = [r.phase for r in ledger.entries()]
    assert phases == ["EXECUTION_STARTED", "EXECUTION_COMPLETED"]
    assert ledger.entries()[-1].receipt_id == receipt.receipt_id
    # append-only: entries() returns a snapshot, not the live list
    assert not isinstance(ledger.entries(), list)


def test_ledger_is_bounded_and_fail_loud():
    ledger = ap.ReceiptLedger(max_entries=2)
    r = ap.ActionReceipt(receipt_id="a", plan_id="p", phase="X", executed=False,
                         outcome_verified=False, truth_state="UNKNOWN",
                         evidence=(), codes=(), observed_outcome=None,
                         expected_outcome=None)
    ledger.append(r)
    ledger.append(r)
    with pytest.raises(ap.LedgerFull):
        ledger.append(r)
