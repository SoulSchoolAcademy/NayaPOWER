"""Fail-closed falsifiers for the ACT execution seam's post-execution hook.

The hole: execute_plan calls the on_executed observer hook AFTER the
EXECUTION_COMPLETED receipt is emitted to the ledger — but with no
exception isolation. If the hook raises (e.g. record_experience's store
write fails), the exception propagates to the caller, who never receives
the completed receipt. Ledger truth = COMPLETED, caller signal =
exception. Any retry-on-exception caller re-executes an already-completed
action — a truth/signal divergence that can double-execute stateful or
harmful actions.

The fix: the hook is an observer, never a decider. Its exception is
isolated — recorded as EXECUTION_HOOK_FAILED ledger evidence — and the
caller always receives the true completed outcome. No exception after
completion, no blind retry.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-hook-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="h1", **kw):
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
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _plan(now=NOW):
    authority = _authority(decided_at=now - 60)
    return ap.ActionPlan(plan_id="hook-1", action=authority.action,
                         chosen=_candidate(), authority=authority,
                         candidate_scores=(), planned_at=now)


def _run(plan, hook):
    """Execute with a ledger; return (receipt, ledger entries)."""
    ledger = ap.ReceiptLedger()
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile(),
        ledger=ledger, on_executed=hook,
    )
    return receipt, ledger.entries()


def _boom(plan, receipt):
    raise RuntimeError("observer store write failed")


# --- Falsifiers (RED pre-fix: the exception escapes; no isolation) ---

def test_hook_exception_does_not_rewrite_completed_outcome():
    """The caller must receive the true completed outcome, never an
    exception-after-completion that invites a blind retry."""
    receipt, _ = _run(_plan(), _boom)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True


def test_hook_failure_is_recorded_as_ledger_evidence():
    """A failed observer must leave visible evidence — never silent, and
    never by rewriting the action's outcome."""
    _, entries = _run(_plan(), _boom)
    phases = [e.phase for e in entries]
    assert "EXECUTION_COMPLETED" in phases
    hook_failures = [e for e in entries if e.phase == "EXECUTION_HOOK_FAILED"]
    assert len(hook_failures) == 1
    assert hook_failures[0].executed is True  # action still completed
    assert "EXECUTION_HOOK_FAILED" in hook_failures[0].codes
    assert "no blind retry" in hook_failures[0].evidence[0]


def test_truth_and_signal_agree_no_double_execution_invite():
    """Ledger truth and caller signal must agree the action completed, so
    no caller can mistake it for a failure and re-execute."""
    receipt, entries = _run(_plan(), _boom)
    completed = [e for e in entries if e.phase == "EXECUTION_COMPLETED"]
    assert len(completed) == 1
    assert receipt.receipt_id == completed[0].receipt_id
    assert receipt.executed == completed[0].executed is True


# --- Regression guards (GREEN before and after) ---

def test_healthy_hook_still_fires_exactly_once():
    seen = []

    def _ok(plan, receipt):
        seen.append((plan, receipt))

    receipt, entries = _run(_plan(), _ok)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert len(seen) == 1
    assert seen[0][1].phase == "EXECUTION_COMPLETED"


def test_failed_executor_never_reaches_hook():
    seen = []
    ledger = ap.ReceiptLedger()
    receipt = ap.execute_plan(
        _plan(),
        executor=lambda p: (_ for _ in ()).throw(RuntimeError("executor down")),
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile(),
        ledger=ledger, on_executed=lambda p, r: seen.append(r),
    )
    assert receipt.phase == "EXECUTION_FAILED"
    assert seen == []
    assert [e.phase for e in ledger.entries()] == [
        "EXECUTION_STARTED", "EXECUTION_FAILED"]
