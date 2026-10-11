"""Tests for drift_canary/fairness_debt_bounds.py (D60 / AER-LIVE-5).

Negative controls throughout: every refusal path is exercised, and the
equivalence property test is proven to be a real control by a dedicated
mutation test (a sabotaged propagation MUST break it — verified red):
  - no enumeration: scattered unresolved rounds beyond D59's 2^12 cap are
    bounded exactly, in O(N) time;
  - missing intervals longer than the cap refuse (D61 territory), never
    approximated;
  - UNDETERMINED never counts, never clears, never breaches on its own;
  - breach needs EVERY defensible history over the bound (strict >);
  - witnesses attain exactly the reported extremes (replayed, not trusted);
  - the engine manufactures no completion: no public API returns a single
    history as fact.
"""
import random
import time

import pytest

from drift_canary.eligibility_proof import (
    APPLICABLE_OPPORTUNITY,
    AUTHORIZATION,
    CONSISTENT_ORDERING,
    ELIGIBLE,
    INELIGIBLE,
    OUTSTANDING_WORK,
    PROVEN,
    READY_DEPENDENCIES,
    REFUTED,
    SCHEDULABLE_CAPACITY,
    UNDETERMINED,
    UNKNOWN,
    EligibilityProver,
    Evidence,
    TaintedOriginError,
)
from drift_canary.fairness import FairnessContract
from drift_canary.unresolved_evidence import (
    BREACH,
    MISSING,
    NO_BREACH,
    RECON_OPEN,
    STALE,
    UNRESOLVED,
    ComponentDefect,
    RoundRecord,
    UnresolvedEvidenceGovernor,
)
from drift_canary import fairness_debt_bounds as d60
from drift_canary.fairness_debt_bounds import (
    ContractObligationMismatchError,
    DebtBoundEngine,
    DebtBoundError,
    DuplicateRoundError,
    MissingInterval,
    MissingIntervalTooLongError,
    UnboundedContractError,
    UnknownObligationError,
)


def ev(status, origin="law_registry", detail="checked"):
    return Evidence(status, detail, origin)


def full_proven(**overrides):
    base = {
        AUTHORIZATION: ev(PROVEN, "law_registry", "authorized"),
        OUTSTANDING_WORK: ev(PROVEN, "work_queue_snapshot", "tasks uncompleted"),
        READY_DEPENDENCIES: ev(PROVEN, "dependency_graph", "all deps satisfied"),
        SCHEDULABLE_CAPACITY: ev(PROVEN, "capacity_plan", "slots provisioned, routable"),
        APPLICABLE_OPPORTUNITY: ev(PROVEN, "scheduler_tick_log", "round tick recorded"),
        CONSISTENT_ORDERING: ev(PROVEN, "ordering_log", "single authoritative ordering"),
    }
    base.update(overrides)
    return base


def proven_round(seq, oid, adequate, eligible=True, opp="opp"):
    overrides = {} if eligible else {
        AUTHORIZATION: ev(REFUTED, "law_registry", "not authorized")}
    receipt = EligibilityProver(full_proven(**overrides)).prove(f"{opp}-{seq}", oid, seq)
    assert receipt.verdict == (ELIGIBLE if eligible else INELIGIBLE)
    return RoundRecord(seq, oid, receipt.verdict, adequate, receipt=receipt)


def undetermined_round(seq, oid, adequate, unknowns, kinds=None, opp="opp"):
    kinds = kinds or {}
    overrides = {c: ev(UNKNOWN, "absent", f"{c} not supplied") for c in unknowns}
    receipt = EligibilityProver(full_proven(**overrides)).prove(f"{opp}-{seq}", oid, seq)
    assert receipt.verdict == UNDETERMINED
    defects = tuple(
        ComponentDefect(c, kinds.get(c, MISSING), f"{c}: {kinds.get(c, MISSING).lower()}")
        for c in unknowns
    )
    return RoundRecord(seq, oid, UNDETERMINED, adequate, defects=defects, receipt=receipt)


def bare_undetermined(seq, oid, adequate):
    """UNDETERMINED without a receipt (defects still required)."""
    return RoundRecord(
        seq, oid, UNDETERMINED, adequate,
        defects=(ComponentDefect(AUTHORIZATION, MISSING, "authorization: missing"),))


def bounded_contract(oid, bound, standard="BOUNDED"):
    return FairnessContract(
        obligation_id=oid,
        revision="r1",
        standard=standard,
        eligibility_predicate="D58 six-component proof",
        service_predicate="adequate service evidenced",
        service_bound_rounds=bound,
        capacity_basis="8 slots provisioned for worker class W",
    )


def replay_debt(rounds, witness):
    """Final debt for one witness completion. Independent of the engine."""
    by_seq = {r.round_seq: r for r in rounds}
    debt = 0
    for seq, eligible in witness:
        rec = by_seq[seq]
        if not eligible:
            continue
        debt = 0 if rec.adequate_service else debt + 1
    return debt


# ---------------------------------------------------------------------------
# Positive: the honest path.
# ---------------------------------------------------------------------------

def test_all_settled_adequate_no_breach():
    rounds = [proven_round(s, "obl-A", True) for s in (1, 2, 3)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))
    assert r.verdict == NO_BREACH
    assert (r.debt_min, r.debt_max) == (0, 0)
    assert r.histories_admitted == 1
    assert r.missing_intervals == ()
    assert r.unresolved_rounds == ()
    assert r.breach_witness is None  # NO_BREACH names no breach
    assert r.clearance_witness is not None


def test_all_settled_inadequate_breach():
    rounds = [proven_round(s, "obl-A", False) for s in (1, 2, 3, 4)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))
    assert r.verdict == BREACH
    assert (r.debt_min, r.debt_max) == (4, 4)
    assert replay_debt(rounds, r.breach_witness) == 4
    assert r.clearance_witness is None  # BREACH names no clearance


def test_single_undetermined_inadequate_unresolved():
    rounds = [
        proven_round(1, "obl-A", False),
        bare_undetermined(2, "obl-A", False),
        proven_round(3, "obl-A", False),
    ]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))
    assert r.verdict == UNRESOLVED
    assert (r.debt_min, r.debt_max) == (2, 3)
    assert r.histories_admitted == 2
    assert r.unresolved_rounds == (2,)
    assert len(r.missing_intervals) == 1
    iv = r.missing_intervals[0]
    assert isinstance(iv, MissingInterval)
    assert (iv.start_seq, iv.end_seq, iv.length) == (2, 2, 1)
    assert (iv.width_before, iv.width_after, iv.added_width) == (0, 1, 1)
    # Neither witness manufactures a conclusion: both extremes are live.
    assert replay_debt(rounds, r.breach_witness) == 3
    assert replay_debt(rounds, r.clearance_witness) == 2


def test_single_undetermined_adequate_unresolved():
    rounds = [
        proven_round(1, "obl-A", False),
        bare_undetermined(2, "obl-A", True),
        proven_round(3, "obl-A", False),
    ]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 1))
    assert r.verdict == UNRESOLVED
    assert (r.debt_min, r.debt_max) == (1, 2)
    iv = r.missing_intervals[0]
    assert (iv.width_before, iv.width_after, iv.added_width) == (0, 1, 1)


def test_aer_live_005_continuations():
    """The D59 acceptance pair, one level up: continuation A settles
    ELIGIBLE and breaches; continuation B settles INELIGIBLE and clears.
    Settled replacements bind — no bare booleans."""
    base = [proven_round(1, "obl-A", False),
            bare_undetermined(2, "obl-A", False),
            proven_round(3, "obl-A", False)]
    cont_a = [base[0], proven_round(2, "obl-A", False), base[2]]
    cont_b = [base[0], proven_round(2, "obl-A", False, eligible=False), base[2]]
    ra = DebtBoundEngine.compute(cont_a, bounded_contract("obl-A", 2))
    rb = DebtBoundEngine.compute(cont_b, bounded_contract("obl-A", 2))
    assert (ra.debt_min, ra.debt_max, ra.verdict) == (3, 3, BREACH)
    assert (rb.debt_min, rb.debt_max, rb.verdict) == (2, 2, NO_BREACH)


def test_equivalence_with_d59_brute_force():
    """Property: interval propagation == D59's enumeration, exactly.
    Seeded; every (debt_min, debt_max, verdict) must match."""
    rng = random.Random(20261011)
    for trial in range(60):
        n = rng.randint(1, 9)
        rounds, gov_rounds = [], []
        for s in range(1, n + 1):
            adequate = rng.random() < 0.5
            pick = rng.random()
            if pick < 0.35:
                r = bare_undetermined(s, "obl-P", adequate)
            elif pick < 0.55:
                r = proven_round(s, "obl-P", adequate, eligible=False)
            else:
                r = proven_round(s, "obl-P", adequate)
            rounds.append(r)
            gov_rounds.append(r)
        gov = UnresolvedEvidenceGovernor()
        for r in gov_rounds:
            gov.register_round(r)
        bound = rng.randint(0, n)
        contract = bounded_contract("obl-P", bound if bound > 0 else 1)
        a = gov.assess("obl-P", contract)
        r = DebtBoundEngine.compute(rounds, contract)
        assert (r.debt_min, r.debt_max) == (a.debt_min, a.debt_max), \
            f"trial {trial}: interval != enumeration"
        assert r.verdict == a.verdict, f"trial {trial}: verdict mismatch"
        assert r.histories_admitted == a.histories_examined
        assert r.unresolved_rounds == a.unresolved_rounds


def test_scattered_intervals_beyond_d59_cap():
    """19 unresolved rounds in four short intervals: D59 fails closed at
    2^19 > 2^12, D60 bounds exactly in O(N)."""
    rounds = ([bare_undetermined(s, "obl-A", True) for s in range(1, 6)]
              + [proven_round(6, "obl-A", False)]
              + [bare_undetermined(s, "obl-A", False) for s in range(7, 12)]
              + [proven_round(12, "obl-A", False)]
              + [bare_undetermined(s, "obl-A", True) for s in range(13, 18)]
              + [proven_round(18, "obl-A", False)]
              + [bare_undetermined(s, "obl-A", False) for s in range(19, 23)])
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 3))
    assert (r.debt_min, r.debt_max) == (1, 12)
    assert r.verdict == UNRESOLVED
    assert r.histories_admitted == 2 ** 19
    widths = [(iv.start_seq, iv.end_seq, iv.added_width) for iv in r.missing_intervals]
    assert widths == [(7, 11, 5), (19, 22, 4), (13, 17, 2), (1, 5, 0)]  # priority order
    assert replay_debt(rounds, r.breach_witness) == 12
    assert replay_debt(rounds, r.clearance_witness) == 1


def test_large_window_fast_no_enumeration():
    """10k rounds, 5k unresolved in scattered intervals: must finish fast,
    proving no enumeration hides inside."""
    rounds = []
    seq = 1
    for block in range(1000):
        rounds.append(proven_round(seq, "obl-A", block % 2 == 0))
        seq += 1
        for _ in range(5):
            rounds.append(bare_undetermined(seq, "obl-A", block % 3 == 0))
            seq += 1
    t0 = time.monotonic()
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 7))
    dt = time.monotonic() - t0
    assert dt < 2.0, f"too slow for O(N): {dt:.2f}s"
    assert r.histories_admitted == 2 ** 5000
    assert r.debt_min >= 0 and r.debt_max >= r.debt_min


def test_ineligible_rounds_hold_debt():
    rounds = [proven_round(1, "obl-A", False),
              proven_round(2, "obl-A", False, eligible=False),
              proven_round(3, "obl-A", False)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))
    assert (r.debt_min, r.debt_max) == (2, 2)
    assert r.verdict == NO_BREACH


def test_witnesses_attain_extremes_on_mixed_window():
    rounds = [proven_round(1, "obl-A", True),
              bare_undetermined(2, "obl-A", False),
              bare_undetermined(3, "obl-A", False),
              proven_round(4, "obl-A", False, eligible=False),
              bare_undetermined(5, "obl-A", True)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 1))
    assert replay_debt(rounds, r.breach_witness) == r.debt_max
    assert replay_debt(rounds, r.clearance_witness) == r.debt_min
    # Witnesses cover every round exactly once, in order.
    assert [s for s, _ in r.breach_witness] == [1, 2, 3, 4, 5]
    assert [s for s, _ in r.clearance_witness] == [1, 2, 3, 4, 5]


def test_gap_in_round_seq_is_not_a_missing_interval():
    """Unregistered seqs are absent opportunities, not missing evidence."""
    rounds = [proven_round(1, "obl-A", False), proven_round(5, "obl-A", False)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 3))
    assert (r.debt_min, r.debt_max) == (2, 2)
    assert r.missing_intervals == ()


# ---------------------------------------------------------------------------
# Negative controls: every refusal path.
# ---------------------------------------------------------------------------

def test_empty_rounds_refused():
    with pytest.raises(UnknownObligationError):
        DebtBoundEngine.compute([], bounded_contract("obl-A", 2))


def test_unbounded_contract_refused():
    rounds = [proven_round(1, "obl-A", False)]
    with pytest.raises(UnboundedContractError):
        DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2, standard="WEAK"))


def test_contract_obligation_mismatch_refused():
    rounds = [proven_round(1, "obl-A", False)]
    with pytest.raises(ContractObligationMismatchError):
        DebtBoundEngine.compute(rounds, bounded_contract("obl-B", 2))


def test_mixed_obligation_rounds_refused():
    rounds = [proven_round(1, "obl-A", False), proven_round(2, "obl-B", False)]
    with pytest.raises(DebtBoundError):
        DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))


def test_duplicate_round_seq_refused():
    rounds = [proven_round(1, "obl-A", False), proven_round(1, "obl-A", True)]
    with pytest.raises(DuplicateRoundError):
        DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))


def test_missing_interval_beyond_cap_refused():
    """65 consecutive UNDETERMINED rounds: D61 territory — refused, never
    approximated, never sampled."""
    rounds = [bare_undetermined(s, "obl-A", False)
              for s in range(1, d60.MAX_MISSING_INTERVAL_ROUNDS + 2)]
    with pytest.raises(MissingIntervalTooLongError):
        DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 10))


def test_interval_at_cap_allowed():
    rounds = [bare_undetermined(s, "obl-A", False)
              for s in range(1, d60.MAX_MISSING_INTERVAL_ROUNDS + 1)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 1000))
    assert (r.debt_min, r.debt_max) == (0, d60.MAX_MISSING_INTERVAL_ROUNDS)
    assert r.verdict == NO_BREACH


def test_strict_breach_boundary():
    """debt_min == bound is NOT a breach: breach needs EVERY history
    strictly over the bound."""
    rounds = [proven_round(s, "obl-A", False) for s in (1, 2)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 2))
    assert (r.debt_min, r.debt_max) == (2, 2)
    assert r.verdict == NO_BREACH  # not BREACH


def test_mutation_breaks_equivalence():
    """The equivalence property test is a real control: sabotage the
    admissibility predicate (UNDETERMINED completes eligible-only —
    manufacturing) and the comparison against D59's enumeration MUST go
    red. Then the real engine passes. Deterministic, no randomness."""
    rounds = [bare_undetermined(1, "obl-A", False),
              proven_round(2, "obl-A", False)]
    contract = bounded_contract("obl-A", 5)
    gov = UnresolvedEvidenceGovernor()
    for r in rounds:
        gov.register_round(r)
    a = gov.assess("obl-A", contract)
    assert (a.debt_min, a.debt_max) == (1, 2)  # both completions live
    good = DebtBoundEngine.compute(rounds, contract)
    assert (good.debt_min, good.debt_max) == (1, 2)

    orig = d60._defensible_completions

    def eligible_only(record):
        comps = orig(record)
        elig = [c for c in comps if c[0]]
        return elig if elig else comps

    d60._defensible_completions = eligible_only
    try:
        bad = DebtBoundEngine.compute(rounds, contract)
        assert (bad.debt_min, bad.debt_max) != (a.debt_min, a.debt_max), \
            "sabotage did not change the bounds — the control is blind"
    finally:
        d60._defensible_completions = orig
    # And the restored engine matches D59 exactly.
    restored = DebtBoundEngine.compute(rounds, contract)
    assert (restored.debt_min, restored.debt_max) == (a.debt_min, a.debt_max)


def test_no_completion_api():
    """Structural anti-manufacturing: the engine exposes no method that
    returns a single completion as fact."""
    public = {n for n in dir(DebtBoundEngine) if not n.startswith("_")}
    assert public == {"compute"}, f"unexpected public surface: {public}"
    rounds = [bare_undetermined(1, "obl-A", False),
              bare_undetermined(2, "obl-A", False)]
    r = DebtBoundEngine.compute(rounds, bounded_contract("obl-A", 1))
    # The only completions in the receipt are witnesses bound to extremes.
    assert r.verdict == UNRESOLVED
    assert replay_debt(rounds, r.breach_witness) == 2
    assert replay_debt(rounds, r.clearance_witness) == 0


def test_receipt_verdict_mismatch_still_refused():
    """D59's invariant pinned: a verdict that disagrees with its D58
    receipt cannot enter the bound computation."""
    receipt = EligibilityProver(
        full_proven(**{AUTHORIZATION: ev(REFUTED, "law_registry", "no")})
    ).prove("opp-1", "obl-A", 1)
    assert receipt.verdict == INELIGIBLE
    with pytest.raises(AssertionError):
        RoundRecord(1, "obl-A", ELIGIBLE, True, receipt=receipt)


def test_tainted_round_cannot_enter():
    """A round whose settlement came from a tainted origin never exists:
    D59's reconstruction refuses scheduler_flag-originated evidence, so
    the engine never sees the manufactured round."""
    gov = UnresolvedEvidenceGovernor()
    rec = undetermined_round(2, "obl-A", False, (AUTHORIZATION,))
    gov.register_round(rec)
    recon = gov.open_reconstruction("obl-A", 2)
    with pytest.raises(TaintedOriginError):
        recon.attempt({AUTHORIZATION: ev(REFUTED, "scheduler_flag", "scheduler says no")})
    assert recon.status == RECON_OPEN
    # The round is still UNDETERMINED: the engine bounds it, never settles it.
    r = DebtBoundEngine.compute([rec], bounded_contract("obl-A", 5))
    assert r.unresolved_rounds == (2,)
