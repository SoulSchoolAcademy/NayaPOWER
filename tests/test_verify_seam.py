"""Red-phase tests for the kernel VERIFY seam (consumer side of action receipts).

Module under test: kernel/verify_seam.py (does not exist yet — all fail).
Closes the ACT -> VERIFY loop: EXECUTION_COMPLETED receipts sit at
truth_state UNKNOWN until an independent verifier closes them via
apply_verify_verdict. The seam enforces the VERIFY node contract as
fail-closed machinery; the injected verifier judges outcomes.
"""
import pytest

from kernel import act_pipeline as ap
from kernel import verify_seam as vs
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="verify-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(**kw):
    base = dict(
        candidate_id="p1",
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


def _completed_receipt(observed="node state updated, previous state restorable",
                       expected="node state updated, previous state restorable"):
    plan, _ = ap.plan_action(_authority(), [_candidate(expected_outcome=expected)
                                            if expected else _candidate()],
                             _profile(), now=NOW)
    ledger = ap.ReceiptLedger()
    receipt = ap.execute_plan(plan, executor=lambda p: observed,
                              re_resolve=lambda: _authority(),
                              now=NOW, ledger=ledger)
    assert receipt.phase == "EXECUTION_COMPLETED"
    return receipt


def _accept(receipt):
    return vs.Verdict(verified=True, acceptance=vs.ACCEPTED,
                      evidence="observed state_diff matches expected outcome exactly")


def _reject(receipt):
    return vs.Verdict(verified=False, acceptance=vs.REJECTED,
                      evidence="observed outcome contradicts expected outcome")


# ---------------- happy path ----------------

def test_accepted_verdict_closes_receipt_verified():
    receipt = _completed_receipt()
    result = vs.close_receipts([receipt], verifier_id="naya-2",
                               verdict_fn=_accept, now=NOW)
    assert len(result.closed) == 1
    closed = result.closed[0]
    assert closed.receipt_id == receipt.receipt_id  # closed, not replaced
    assert closed.truth_state == "VERIFIED"
    assert closed.outcome_verified is True
    assert closed.executed is True
    assert any("VERIFY verdict" in e for e in closed.evidence)
    rec = result.records[0]
    assert rec.receipt_id == receipt.receipt_id
    assert rec.verifier_id == "naya-2"
    assert rec.acceptance == "ACCEPTED"
    assert rec.verdict_at == NOW


def test_rejected_verdict_closes_receipt_blocked():
    receipt = _completed_receipt(observed="node unchanged")
    result = vs.close_receipts([receipt], verifier_id="naya-2",
                               verdict_fn=_reject, now=NOW)
    closed = result.closed[0]
    assert closed.truth_state == "BLOCKED"
    assert closed.outcome_verified is False


def test_full_chain_plan_execute_verify_round_trip():
    """PLAN -> EXECUTE -> ledger -> VERIFY seam: the loop actually closes."""
    plan, plan_receipt = ap.plan_action(_authority(), [_candidate()],
                                        _profile(), now=NOW)
    ledger = ap.ReceiptLedger()
    ledger.append(plan_receipt)
    ap.execute_plan(plan, executor=lambda p: "node state updated, previous state restorable",
                    re_resolve=lambda: _authority(), now=NOW, ledger=ledger)
    log = vs.VerdictLog()
    completed = [r for r in ledger.entries() if r.phase == "EXECUTION_COMPLETED"]
    assert len(completed) == 1
    result = vs.close_receipts(completed, verifier_id="naya-2",
                               verdict_fn=_accept, now=NOW, log=log)
    assert result.closed[0].truth_state == "VERIFIED"
    assert log.closed_receipt_ids() == frozenset({completed[0].receipt_id})


# ---------------- fail-closed machinery ----------------

def test_verdict_without_evidence_is_refused():
    receipt = _completed_receipt()

    def no_evidence(r):
        return vs.Verdict(verified=True, acceptance=vs.ACCEPTED, evidence="")

    with pytest.raises(vs.VerdictRefused):
        vs.close_receipts([receipt], verifier_id="naya-2",
                          verdict_fn=no_evidence, now=NOW)
    assert receipt.truth_state == "UNKNOWN"  # untouched


def test_verifier_identity_is_required():
    receipt = _completed_receipt()
    with pytest.raises(vs.VerdictRefused):
        vs.close_receipts([receipt], verifier_id="",
                          verdict_fn=_accept, now=NOW)


def test_incoherent_verdict_pair_is_refused():
    receipt = _completed_receipt()

    def incoherent(r):
        return vs.Verdict(verified=True, acceptance=vs.REJECTED,
                          evidence="contradictory verdict")

    with pytest.raises(vs.VerdictRefused):
        vs.close_receipts([receipt], verifier_id="naya-2",
                          verdict_fn=incoherent, now=NOW)


def test_missing_observation_is_not_proven_without_verifier():
    calls = []
    receipt = _completed_receipt(observed=None)

    def spy(r):
        calls.append(r)
        return _accept(r)

    result = vs.close_receipts([receipt], verifier_id="naya-2",
                               verdict_fn=spy, now=NOW)
    assert calls == []  # verifier never consulted — nothing to judge
    closed = result.closed[0]
    assert closed.truth_state == "BLOCKED"
    assert vs.OBSERVATION_MISSING in closed.codes


def test_undefined_expected_outcome_is_not_proven():
    # Constructed directly: plan_action refuses empty expected outcomes,
    # so the seam must still handle a receipt that arrives without one.
    receipt = ap.ActionReceipt(
        receipt_id="r1", plan_id="p1", phase="EXECUTION_COMPLETED",
        executed=True, outcome_verified=False, truth_state="UNKNOWN",
        observed_outcome="something happened", expected_outcome=None)
    calls = []
    result = vs.close_receipts([receipt], verifier_id="naya-2",
                               verdict_fn=lambda r: calls.append(r) or _accept(r),
                               now=NOW)
    assert calls == []
    assert result.closed[0].truth_state == "BLOCKED"
    assert vs.EXPECTED_OUTCOME_UNDEFINED in result.closed[0].codes


def test_non_completed_receipts_are_skipped_not_closed():
    plan, plan_receipt = ap.plan_action(_authority(), [_candidate()],
                                        _profile(), now=NOW)
    assert plan_receipt.phase == "PLAN_ACCEPTED"
    result = vs.close_receipts([plan_receipt], verifier_id="naya-2",
                               verdict_fn=_accept, now=NOW)
    assert result.closed == ()
    assert len(result.skipped) == 1
    assert result.skipped[0][0] == plan_receipt.receipt_id


def test_pending_verdict_records_gap_without_closing():
    receipt = _completed_receipt()

    def pending(r):
        return vs.Verdict(verified=False, acceptance=vs.PENDING,
                          evidence="state_diff artifact not yet produced; cannot decide")

    result = vs.close_receipts([receipt], verifier_id="naya-2",
                               verdict_fn=pending, now=NOW)
    assert result.closed == ()  # inconclusive is neither success nor failure
    assert receipt.truth_state == "UNKNOWN"
    assert len(result.records) == 1
    assert result.records[0].acceptance == "PENDING"


def test_double_close_is_refused_loudly():
    receipt = _completed_receipt()
    log = vs.VerdictLog()
    vs.close_receipts([receipt], verifier_id="naya-2", verdict_fn=_accept,
                      now=NOW, log=log)
    with pytest.raises(vs.ReceiptAlreadyClosed):
        vs.close_receipts([receipt], verifier_id="naya-2", verdict_fn=_accept,
                          now=NOW, log=log)


def test_verifier_exception_leaves_receipt_unclosed():
    receipt = _completed_receipt()

    def boom(r):
        raise RuntimeError("verifier crashed")

    with pytest.raises(RuntimeError):
        vs.close_receipts([receipt], verifier_id="naya-2",
                          verdict_fn=boom, now=NOW)
    assert receipt.truth_state == "UNKNOWN"


def test_verdict_log_bound_fails_loud():
    receipt = _completed_receipt()
    log = vs.VerdictLog(max_entries=1)
    vs.close_receipts([receipt], verifier_id="naya-2", verdict_fn=_accept,
                      now=NOW, log=log)
    receipt2 = _completed_receipt()
    with pytest.raises(vs.LogFull):
        vs.close_receipts([receipt2], verifier_id="naya-2",
                          verdict_fn=_accept, now=NOW, log=log)
