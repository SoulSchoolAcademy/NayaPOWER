"""Tests for drift_canary/unbounded_debt_bounds.py (D61 / AER-LIVE-6).

Negative controls throughout: every refusal path is exercised, the
attainability theorem is proven to be a real control by a dedicated
mutation test (a sabotaged step rule MUST break the replay — verified
red), and the AER-LIVE-006 mutation (final-debt-only compliance) is
rejected by the independent verifier:

  - unknown length, unbounded debt, and proven violation are never
    interchanged (three receipts, three distinct statuses/verdicts);
  - a later service reset never erases a possible earlier breach:
    final debt 0 with an unbounded peak is UNRESOLVED, never NO_BREACH;
  - NO_BREACH is establishable only through a finite limit, never through
    the unbounded interval itself (property test);
  - the SLA under test can never serve as its own enforcement evidence
    (circular limit refused; unnamed tested SLA fails closed);
  - peak one-to-infinity: every integer >= entry debt is the peak of a
    constructed, replayed witness history (property test);
  - the engine manufactures no completion: no public API returns a single
    history as fact — witnesses are hypotheses for bound computation.
"""
import random

import pytest

from drift_canary.fairness import FairnessContract
from drift_canary import unbounded_debt_bounds as d61
from drift_canary.unbounded_debt_bounds import (
    BREACH,
    ENFORCED_RESET,
    FINITE_LIMIT_ESTABLISHED,
    LAW_WITHDRAWAL,
    NO_BREACH,
    NO_FINITE_BOUND_ESTABLISHED,
    PROVEN_UNBOUNDED,
    TRUSTED_SEQUENCE_NUMBERS,
    UNRESOLVED,
    CircularEvidenceError,
    ClaimMismatchError,
    ContractObligationMismatchError,
    FinalDebtOnlyClaimError,
    FiniteLimit,
    PeakUnboundedClaimError,
    UnboundedContractError,
    UnboundedDebtEngine,
    UnboundedDebtError,
    UnboundedInterval,
    UnknownLimitSourceError,
    replay_history,
    verify_compliance_claim,
    witness_history,
)


def contract(oid="obligation-1", bound=5):
    return FairnessContract(
        obligation_id=oid,
        revision="r1",
        standard="BOUNDED",
        eligibility_predicate="eligible when queued",
        service_predicate="adequate service when served",
        service_bound_rounds=bound,
        capacity_basis="capacity plan v3: 5 slots per round",
    )


def interval(oid="obligation-1", lo=0, hi=0, exit=True):
    return UnboundedInterval(
        obligation_id=oid, entry_debt_lo=lo, entry_debt_hi=hi,
        must_end_with_service=exit)


# ---------------------------------------------------------------------------
# AER-LIVE-006 canonical case: unbounded peak, zero final debt.
# The checker must prove final debt zero and peak one-to-infinity,
# holding the verdict undetermined.
# ---------------------------------------------------------------------------

def test_aer_live_006_canonical():
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    assert r.final_debt == 0
    assert "clears the counter" in r.final_debt_basis
    assert r.peak_status == PROVEN_UNBOUNDED
    assert r.peak_lower_bound == 0
    assert r.peak_upper_bound is None
    assert r.verdict == UNRESOLVED
    assert r.witness is not None
    assert r.finite_limit is None
    assert r.model_assumptions  # unbounded uppers rest on stated assumptions


def test_reset_never_erases_possible_breach():
    # Final debt is exactly 0 — and the verdict is STILL not NO_BREACH.
    # The service clears the counter, not the history.
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    assert r.final_debt == 0
    assert r.verdict != NO_BREACH
    assert "never the final" in r.verdict_basis or "peak" in r.verdict_basis


def test_peak_one_to_infinity_property():
    # Every integer >= entry debt is the peak of a constructed witness
    # history — replayed, not trusted.
    rng = random.Random(6102429215)  # D61's register comment id: deterministic
    for _ in range(60):
        lo = rng.randint(0, 20)
        k = rng.randint(0, 5000)
        hist = witness_history(lo, k)
        peak, final = replay_history(lo, hist)
        assert peak == lo + k, f"peak must be one-to-infinity above entry {lo}"
        assert final == 0, "U*S always ends at final debt 0"


def test_witness_histories_are_hypotheses_not_facts():
    # The engine manufactures no completion: the public witness API returns
    # histories explicitly as bound-computation hypotheses.
    h = witness_history(3, 4)
    assert h == ("U", "U", "U", "U", "S")
    peak, final = replay_history(3, h)
    assert (peak, final) == (7, 0)


def test_mutation_sabotaged_step_breaks_replay(monkeypatch):
    # The attainability property is a real control: sabotage the step rule
    # (+2 per unserved round instead of +1) and the replay MUST go red.
    monkeypatch.setattr(d61, "_apply_step", lambda debt, step: debt + 2 if step == "U" else 0)
    peak, final = replay_history(0, witness_history(0, 3))
    assert (peak, final) != (3, 0), "sabotaged step rule must break the replay"
    # Restored engine goes green.
    monkeypatch.undo()
    peak, final = replay_history(0, witness_history(0, 3))
    assert (peak, final) == (3, 0)


# ---------------------------------------------------------------------------
# The three things never interchanged.
# ---------------------------------------------------------------------------

def test_unknown_length_unbounded_debt_proven_violation_distinct():
    # Same entry, same bound — three different situations, three different
    # (status, verdict) pairs.
    c = contract(bound=5)
    unbounded = UnboundedDebtEngine.assess(interval(lo=0, hi=0), c)
    assert (unbounded.peak_status, unbounded.verdict) == (PROVEN_UNBOUNDED, UNRESOLVED)

    limited = UnboundedDebtEngine.assess(
        interval(lo=0, hi=0), contract(bound=3),
        finite_limit=FiniteLimit(TRUSTED_SEQUENCE_NUMBERS, 4, "seq-ledger:trusted"),
        tested_sla_ref="sla:bounded-3:capacity-v3")
    assert (limited.peak_status, limited.verdict) == (FINITE_LIMIT_ESTABLISHED, UNRESOLVED)
    assert limited.defers_to == "D60"

    breached = UnboundedDebtEngine.assess(interval(lo=7, hi=9), c)
    assert (breached.peak_status, breached.verdict) == (PROVEN_UNBOUNDED, BREACH)


def test_breach_proven_on_peak_not_final():
    r = UnboundedDebtEngine.assess(interval(lo=7, hi=9), contract(bound=5))
    assert r.verdict == BREACH
    assert r.final_debt == 0  # the final is still zero — the breach is on the peak
    assert "peak" in r.verdict_basis


def test_no_breach_impossible_without_finite_limit_property():
    # Theorem pinned: without a finite limit, the verdict is never NO_BREACH.
    rng = random.Random(20261011)
    for _ in range(80):
        lo = rng.randint(0, 30)
        hi = lo + rng.randint(0, 10)
        bound = rng.randint(1, 40)
        exit = rng.random() < 0.5
        r = UnboundedDebtEngine.assess(interval(lo=lo, hi=hi, exit=exit), contract(bound=bound))
        assert r.verdict != NO_BREACH, (
            f"NO_BREACH without a finite limit at entry [{lo},{hi}] bound {bound}")
        assert r.verdict in (BREACH, UNRESOLVED)
        if lo > bound:
            assert r.verdict == BREACH
        else:
            assert r.verdict == UNRESOLVED


# ---------------------------------------------------------------------------
# U* without a demonstrated exit: NO_FINITE_BOUND_ESTABLISHED, not proven.
# ---------------------------------------------------------------------------

def test_no_exit_no_constructive_witness():
    r = UnboundedDebtEngine.assess(interval(lo=2, hi=4, exit=False), contract(bound=5))
    assert r.peak_status == NO_FINITE_BOUND_ESTABLISHED
    assert r.witness is None  # the witness requires a valid exit
    assert r.final_debt is None  # the final is itself unbounded
    assert r.peak_upper_bound is None
    assert r.verdict == UNRESOLVED


def test_no_exit_breach_still_proven_on_peak():
    r = UnboundedDebtEngine.assess(interval(lo=6, hi=6, exit=False), contract(bound=5))
    assert r.verdict == BREACH
    assert r.peak_status == NO_FINITE_BOUND_ESTABLISHED


# ---------------------------------------------------------------------------
# Finite limits: the hunt's result, validated.
# ---------------------------------------------------------------------------

def _limit(source, cap, ref="evidence:ok"):
    return FiniteLimit(source, cap, ref)


def test_finite_limit_trusted_sequence_numbers_closes_compliance():
    r = UnboundedDebtEngine.assess(
        interval(lo=2, hi=3), contract(bound=10),
        finite_limit=_limit(TRUSTED_SEQUENCE_NUMBERS, 4),
        tested_sla_ref="sla:bounded-10:capacity-v3")
    assert r.peak_status == FINITE_LIMIT_ESTABLISHED
    assert r.peak_upper_bound == 3 + 4
    assert r.verdict == NO_BREACH  # 7 <= 10: closed through the limit
    assert r.defers_to is None


def test_finite_limit_straddling_defers_to_finite_engine():
    r = UnboundedDebtEngine.assess(
        interval(lo=2, hi=3), contract(bound=5),
        finite_limit=_limit(ENFORCED_RESET, 4, "reset-policy:R-7"),
        tested_sla_ref="sla:bounded-5:capacity-v3")
    assert r.peak_status == FINITE_LIMIT_ESTABLISHED
    assert r.peak_upper_bound == 7  # peak in [2,7] straddles bound 5
    assert r.verdict == UNRESOLVED
    assert r.defers_to == "D60"  # bounded territory again: the finite engine judges


def test_finite_limit_law_withdrawal():
    r = UnboundedDebtEngine.assess(
        interval(lo=0, hi=1), contract(bound=4),
        finite_limit=_limit(LAW_WITHDRAWAL, 2, "law-registry:withdrawal-0042"),
        tested_sla_ref="sla:bounded-4:capacity-v3")
    assert r.peak_status == FINITE_LIMIT_ESTABLISHED
    assert r.peak_upper_bound == 3
    assert r.verdict == NO_BREACH


def test_finite_limit_breach_when_entry_over_bound():
    r = UnboundedDebtEngine.assess(
        interval(lo=8, hi=9), contract(bound=5),
        finite_limit=_limit(TRUSTED_SEQUENCE_NUMBERS, 1),
        tested_sla_ref="sla:bounded-5:capacity-v3")
    assert r.verdict == BREACH


def test_circular_evidence_refused():
    # The SLA under test can never serve as its own enforcement evidence.
    with pytest.raises(CircularEvidenceError):
        UnboundedDebtEngine.assess(
            interval(), contract(bound=5),
            finite_limit=_limit(TRUSTED_SEQUENCE_NUMBERS, 4, "sla:bounded-5:capacity-v3"),
            tested_sla_ref="sla:bounded-5:capacity-v3")


def test_unnamed_tested_sla_fails_closed():
    # Without naming the tested SLA, circularity cannot be excluded — refuse.
    with pytest.raises(CircularEvidenceError):
        UnboundedDebtEngine.assess(
            interval(), contract(bound=5),
            finite_limit=_limit(TRUSTED_SEQUENCE_NUMBERS, 4))


def test_unknown_limit_source_refused():
    with pytest.raises(UnknownLimitSourceError):
        FiniteLimit("SLA_UNDER_TEST", 4, "sla:bounded-5")
    with pytest.raises(UnknownLimitSourceError):
        FiniteLimit("TRUST_ME", 4, "whatever")


def test_negative_cap_refused():
    with pytest.raises(UnboundedDebtError):
        FiniteLimit(TRUSTED_SEQUENCE_NUMBERS, -1, "seq-ledger:trusted")


# ---------------------------------------------------------------------------
# Fail-closed inputs.
# ---------------------------------------------------------------------------

def test_non_bounded_contract_refused():
    weak = FairnessContract(
        obligation_id="obligation-1", revision="r1", standard="WEAK",
        eligibility_predicate="e", service_predicate="s")
    with pytest.raises(UnboundedContractError):
        UnboundedDebtEngine.assess(interval(), weak)


def test_obligation_mismatch_refused():
    with pytest.raises(ContractObligationMismatchError):
        UnboundedDebtEngine.assess(interval(oid="obligation-9"), contract(oid="obligation-1"))


def test_bad_entry_intervals_refused():
    with pytest.raises(UnboundedDebtError):
        UnboundedInterval("o", -1, 3)
    with pytest.raises(UnboundedDebtError):
        UnboundedInterval("o", 5, 3)  # inverted
    with pytest.raises(UnboundedDebtError):
        UnboundedInterval("", 0, 0)  # no obligation id
    with pytest.raises(UnboundedDebtError):
        witness_history(0, -2)


def test_witness_triple_integrity():
    with pytest.raises(UnboundedDebtError):
        from drift_canary.unbounded_debt_bounds import UnboundednessWitness
        UnboundednessWitness(demonstrated=((3, 99, 0),))  # not a U*S replay


# ---------------------------------------------------------------------------
# The independent verifier: AER-LIVE-006's mutation must be rejected.
# ---------------------------------------------------------------------------

class NaiveFinalDebtChecker:
    """The mutation: examines only the final debt and declares compliance.
    This is exactly the error D61 exists to prevent."""

    @staticmethod
    def check(receipt, contract):
        if receipt.final_debt is not None and receipt.final_debt <= contract.service_bound_rounds:
            return NO_BREACH
        return UNRESOLVED


def test_verifier_rejects_final_debt_only_compliance():
    # AER-LIVE-006's mutation: final debt 0 -> "compliant". Rejected.
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    claim = NaiveFinalDebtChecker.check(r, contract(bound=5))
    assert claim == NO_BREACH  # the naive checker really makes the error
    with pytest.raises(FinalDebtOnlyClaimError):
        verify_compliance_claim(r, claim, {"final_debt": 0})


def test_verifier_rejects_fabricated_peak_max():
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    with pytest.raises(PeakUnboundedClaimError):
        verify_compliance_claim(r, NO_BREACH, {"peak_upper_bound": 12})


def test_verifier_accepts_honest_undetermined():
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    assert verify_compliance_claim(r, UNRESOLVED, {"note": "holding undetermined"}) == "ACCEPTED"


def test_verifier_accepts_peak_witness_breach():
    r = UnboundedDebtEngine.assess(interval(lo=7, hi=9), contract(bound=5))
    assert r.verdict == BREACH
    assert verify_compliance_claim(
        r, BREACH, {"peak_witness": {"entry_debt": 7, "unserved_rounds": 0}}) == "ACCEPTED"


def test_verifier_rejects_breach_claim_on_undetermined_receipt():
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    with pytest.raises(ClaimMismatchError):
        verify_compliance_claim(
            r, BREACH, {"peak_witness": {"entry_debt": 0, "unserved_rounds": 0}})


def test_verifier_accepts_finite_limit_compliance_only_via_the_limit():
    r = UnboundedDebtEngine.assess(
        interval(lo=2, hi=3), contract(bound=10),
        finite_limit=_limit(TRUSTED_SEQUENCE_NUMBERS, 4, "seq-ledger:trusted"),
        tested_sla_ref="sla:bounded-10:capacity-v3")
    assert r.verdict == NO_BREACH
    # Citing the establishing limit: accepted.
    assert verify_compliance_claim(r, NO_BREACH, {
        "finite_limit_source": TRUSTED_SEQUENCE_NUMBERS,
        "max_unserved_rounds": 4,
        "evidence_ref": "seq-ledger:trusted",
    }) == "ACCEPTED"
    # Citing anything else (even the true peak upper): rejected.
    with pytest.raises(ClaimMismatchError):
        verify_compliance_claim(r, NO_BREACH, {"peak_upper_bound": 7})


def test_verifier_rejects_unknown_verdict():
    r = UnboundedDebtEngine.assess(interval(lo=0, hi=0), contract(bound=5))
    with pytest.raises(ClaimMismatchError):
        verify_compliance_claim(r, "MAYBE", {})


# ---------------------------------------------------------------------------
# Determinism and receipt integrity.
# ---------------------------------------------------------------------------

def test_assess_is_deterministic():
    iv = interval(lo=1, hi=4)
    c = contract(bound=6)
    assert UnboundedDebtEngine.assess(iv, c) == UnboundedDebtEngine.assess(iv, c)


def test_receipt_invariants_hold_on_random_inputs():
    rng = random.Random(987654321)
    for _ in range(50):
        lo = rng.randint(0, 25)
        hi = lo + rng.randint(0, 8)
        bound = rng.randint(1, 30)
        r = UnboundedDebtEngine.assess(interval(lo=lo, hi=hi), contract(bound=bound))
        assert r.peak_lower_bound == lo
        assert r.model_assumptions
        assert "peak" in r.verdict_basis.lower()
