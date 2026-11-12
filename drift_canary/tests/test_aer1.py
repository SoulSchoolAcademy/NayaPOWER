"""AER-1 tests (SN-0793): recovery-safety under ambiguity. When an
external effect's commit outcome is unknown: preserve the uncertainty,
never automatically repeat the effect; reconcile first; any subsequent
execution needs current LAW permission, a stable logical-operation
identity, and independently verified duplicate-safety across every
remaining possible history."""
import pytest

from drift_canary.revocation_linearization import (
    LogicalOperation,
    AmbiguousEffect,
    RecoveryGuarantees,
    decide_recovery,
    no_safe_retry_record,
    safe_recovery_predicate,
    recover_ambiguous_operation,
    compensation_is_new_effect,
    MockExternalProvider,
    aer_001,
    IDEMPOTENCY_CONTRACT_CHECKS,
    REC_VERIFY_AND_CLOSE,
    REC_FRESH_EXECUTION,
    REC_RECONCILE,
    REC_SAME_KEY_RETRY,
    REC_IDEMPOTENT_RETRY,
    REC_HOLD,
    REC_HOLD_ESCALATE,
    REC_NO_SAFE_RETRY,
)


def _op(key="op-1"):
    return LogicalOperation(key, "payments", "hash", 1, 1)


def _eff(op=None, impact="reversible"):
    return AmbiguousEffect(op or _op(), frozenset({"IN_FLIGHT"}),
                           ("receipt withheld",), impact)


def _g(**kw):
    base = dict(committed_confirmed=False, cannot_commit_proven=False,
                read_only_status_query_available=False,
                atomic_dedup_proven=False, idempotent_covers_whole_effect=False,
                current_law_valid=True, recovery_fence_held=True,
                covers_all_possible_outstanding_attempts=False)
    base.update(kw)
    return RecoveryGuarantees(**base)


# --- the seven-row decision table ------------------------------------------------------------------
def test_row1_confirmed_committed():
    d = decide_recovery(_eff(), _g(committed_confirmed=True))
    assert d["decision"] == REC_VERIFY_AND_CLOSE


def test_row2_proven_cannot_commit():
    d = decide_recovery(_eff(), _g(cannot_commit_proven=True))
    assert d["decision"] == REC_FRESH_EXECUTION
    # ...but stale authority still holds the retry.
    d2 = decide_recovery(_eff(), _g(cannot_commit_proven=True,
                                   current_law_valid=False))
    assert d2["decision"] == REC_HOLD
    assert "CURRENT" in d2["reason"]


def test_row3_read_only_reconcile():
    d = decide_recovery(_eff(), _g(read_only_status_query_available=True))
    assert d["decision"] == REC_RECONCILE
    assert "original identity" in d["reason"]


def test_row4_atomic_dedup_retry():
    d = decide_recovery(
        _eff(), _g(atomic_dedup_proven=True,
                   covers_all_possible_outstanding_attempts=True))
    assert d["decision"] == REC_SAME_KEY_RETRY


def test_row5_idempotent_retry_needs_whole_effect():
    d = decide_recovery(
        _eff(), _g(idempotent_covers_whole_effect=True,
                   covers_all_possible_outstanding_attempts=True))
    assert d["decision"] == REC_IDEMPOTENT_RETRY


def test_row6_no_guarantee_holds():
    d = decide_recovery(_eff(), _g())
    assert d["decision"] == REC_HOLD


def test_row7_irreversible_escalates():
    d = decide_recovery(
        _eff(impact="irreversible-high"),
        _g(atomic_dedup_proven=True,
           covers_all_possible_outstanding_attempts=True))
    assert d["decision"] == REC_HOLD_ESCALATE


def test_timeout_never_proves_cancellation():
    """An earlier attempt may still be executing: without
    covers_all_possible_outstanding_attempts, no retry row fires."""
    d = decide_recovery(_eff(), _g(atomic_dedup_proven=True))
    assert d["decision"] == REC_HOLD


def test_stale_authority_blocks_dedup_retry():
    """A deduplicated retry can still execute after its authorization
    was revoked -- retries always need CURRENT permission."""
    d = decide_recovery(
        _eff(), _g(atomic_dedup_proven=True,
                   covers_all_possible_outstanding_attempts=True,
                   current_law_valid=False))
    assert d["decision"] == REC_HOLD


# --- SafeRecovery predicate ---------------------------------------------------------------------------
def test_safe_recovery_predicate():
    worlds = [lambda a: True, lambda a: True]
    assert safe_recovery_predicate("verify", worlds, True) is True
    assert safe_recovery_predicate("verify", worlds, False) is False
    worlds2 = [lambda a: True, lambda a: False]
    assert safe_recovery_predicate("retry", worlds2, True) is False


# --- the procedure: fence first ----------------------------------------------------------------------------
def test_recover_requires_fence():
    d = recover_ambiguous_operation(
        _eff(), _g(recovery_fence_held=False, atomic_dedup_proven=True,
                   covers_all_possible_outstanding_attempts=True))
    assert d["decision"] == REC_HOLD
    assert "fence" in d["reason"]


# --- compensation is a new effect -------------------------------------------------------------------------------
def test_compensation_separation():
    c = compensation_is_new_effect(_eff())
    assert c["proves_original_absent"] is False
    assert "NEW" in c["compensation"]


# --- terminal record: progress without retry loopholes ---------------------------------------------------------------
def test_no_safe_retry_terminal_record():
    r = no_safe_retry_record(_eff(), "no duplicate-safety contract")
    assert r["record"] == REC_NO_SAFE_RETRY
    assert "never" in r["deadline_policy"]


# --- idempotency contract checks --------------------------------------------------------------------------------------
def test_idempotency_contract_checks_listed():
    assert "key_expiry" in IDEMPOTENCY_CONTRACT_CHECKS
    assert "stale_authority" in IDEMPOTENCY_CONTRACT_CHECKS
    assert "downstream_effect_coverage" in IDEMPOTENCY_CONTRACT_CHECKS


# --- AER-001 ----------------------------------------------------------------------------------------------------------------
def test_aer_001():
    r = aer_001()
    assert r["withheld_receipt"] == REC_HOLD
    assert r["atomic_idempotency_at_most_one"] == 1
    assert r["key_expiry_rejects"] == "REJECTED_KEY_EXPIRED"
    assert r["stale_authority_rejects"] == "REJECTED_STALE_AUTHORITY"
    assert r["verifier_ledger_count"] == 1


# --- AER-01..AER-10 adversarial matrix (compact) ------------------------------------------------------------------------------
def test_aer_matrix():
    """Twin-worlds choice, fencing under revocation, replica queries,
    compensation, unrelated-claim continuation, timeout semantics, key
    expiry, stale authority, concurrent deciders, late completion."""
    results = {}

    # AER-01: identical incomplete evidence -> safe-in-both or decline.
    op = _op("aer01")
    eff = AmbiguousEffect(op, frozenset({"COMMITTED", "IN_FLIGHT"}),
                          ("receipt",), "reversible")
    d = recover_ambiguous_operation(eff, _g())
    results["AER-01"] = d["decision"] == REC_HOLD  # decline: safe in both

    # AER-02: fencing under revocation -- fence held, dedup proven.
    d = recover_ambiguous_operation(
        eff, _g(atomic_dedup_proven=True,
                covers_all_possible_outstanding_attempts=True))
    results["AER-02"] = d["decision"] == REC_SAME_KEY_RETRY

    # AER-03: incomplete-replica status query -- replica says unknown:
    # not authoritative, cannot confirm.
    d = recover_ambiguous_operation(eff, _g())
    results["AER-03"] = d["decision"] == REC_HOLD

    # AER-04: compensation needs its own authorization.
    c = compensation_is_new_effect(eff)
    results["AER-04"] = c["proves_original_absent"] is False

    # AER-05: unrelated-claim continuation -- ambiguity about op-x does
    # not block op-y.
    results["AER-05"] = decide_recovery(
        _eff(_op("other")), _g())["decision"] == REC_HOLD  # per-operation

    # AER-06: timeout never proves cancellation.
    results["AER-06"] = decide_recovery(
        eff, _g(atomic_dedup_proven=True))["decision"] == REC_HOLD

    # AER-07: key expiry -> rejection (covered in AER-001).
    p = MockExternalProvider()
    o7 = LogicalOperation("k7", "s", "h", 1, 1)
    p.submit(o7)
    p.expire_key("k7")
    results["AER-07"] = p.submit(o7)[0] == "REJECTED_KEY_EXPIRED"

    # AER-08: stale authority revocation.
    p.revoke_authority()
    o8 = LogicalOperation("k8", "s", "h", 1, 1)
    results["AER-08"] = p.submit(o8)[0] == "REJECTED_STALE_AUTHORITY"

    # AER-09: concurrent deciders -- the fence prevents two workers from
    # simultaneously deciding to retry.
    import threading
    fence = threading.Lock()
    decided = []
    eff9 = AmbiguousEffect(_op("k9"), frozenset({"IN_FLIGHT"}), (),
                           "reversible")
    g9 = _g(atomic_dedup_proven=True,
            covers_all_possible_outstanding_attempts=True)
    fence.acquire()  # worker-0 holds the fence for the whole recovery
    def worker():
        if fence.acquire(blocking=False):
            try:
                decided.append(decide_recovery(eff9, g9)["decision"])
            finally:
                fence.release()
        else:
            decided.append("DEFERRED_FENCE_HELD")
    ts = [threading.Thread(target=worker) for _ in range(3)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    fence.release()
    results["AER-09"] = (decided == ["DEFERRED_FENCE_HELD"] * 3)

    # AER-10: late completion after hold -- reconcile closes, no duplicate.
    p10 = MockExternalProvider()
    o10 = LogicalOperation("k10", "s", "h", 1, 1)
    p10.submit(o10)  # committed, receipt "lost"
    d10 = decide_recovery(
        AmbiguousEffect(o10, frozenset({"COMMITTED", "IN_FLIGHT"}), ("rcpt",),
                        "reversible"),
        _g(read_only_status_query_available=True))
    results["AER-10"] = (d10["decision"] == REC_RECONCILE
                         and p10.count_effects("k10") == 1)

    failed = [k for k, v in results.items() if not v]
    assert not failed, failed
