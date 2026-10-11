"""Tests for drift_canary/unresolved_evidence.py (D59 / AER-LIVE-4).

Negative controls throughout: every refusal path is exercised, and the
sabotage-sensitive invariants are pinned by dedicated tests:
  - no single debt number is ever manufactured from unresolved rounds
    (the range is the only public debt fact);
  - UNDETERMINED never counts, never clears, never breaches on its own;
  - breach needs EVERY compatible history over the bound (strict >);
  - reconstruction settles only via a re-run D58 receipt, never a bare
    boolean; tainted reconstruction evidence is refused;
  - budget exhaustion / repair starvation escalate with history preserved.
"""
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
    UnknownComponentError,
)
from drift_canary.fairness import FairnessContract
from drift_canary.unresolved_evidence import (
    BREACH,
    BUDGET_EXHAUSTED,
    CONTRADICTORY,
    MISSING,
    NO_BREACH,
    RECON_ESCALATED,
    RECON_OPEN,
    RECON_SETTLED,
    REPAIR_STARVED,
    STALE,
    UNRESOLVED,
    ComponentDefect,
    DuplicateRoundError,
    HistorySpaceTooLargeError,
    ReconstructionObligation,
    ReconstructionStateError,
    RoundRecord,
    UnboundedContractError,
    UnknownObligationError,
    UnresolvedEvidenceGovernor,
)


def ev(status, origin="law_registry", detail="checked"):
    return Evidence(status, detail, origin)


def full_proven(**overrides):
    base = {
        AUTHORIZATION: ev(PROVEN, "law_registry", "obligation authorized at round"),
        OUTSTANDING_WORK: ev(PROVEN, "work_queue_snapshot", "tasks uncompleted"),
        READY_DEPENDENCIES: ev(PROVEN, "dependency_graph", "all deps satisfied"),
        SCHEDULABLE_CAPACITY: ev(PROVEN, "capacity_plan", "slots provisioned, routable"),
        APPLICABLE_OPPORTUNITY: ev(PROVEN, "scheduler_tick_log", "round tick recorded"),
        CONSISTENT_ORDERING: ev(PROVEN, "ordering_log", "single authoritative ordering"),
    }
    base.update(overrides)
    return base


def proven_round(seq, oid, adequate, opp="opp"):
    receipt = EligibilityProver(full_proven()).prove(f"{opp}-{seq}", oid, seq)
    assert receipt.verdict == ELIGIBLE
    return RoundRecord(seq, oid, ELIGIBLE, adequate, receipt=receipt)


def undetermined_round(seq, oid, adequate, unknowns, kinds=None, opp="opp"):
    """unknowns: iterable of components left UNKNOWN. kinds: component->kind."""
    kinds = kinds or {}
    overrides = {c: ev(UNKNOWN, "absent", f"{c} not supplied") for c in unknowns}
    receipt = EligibilityProver(full_proven(**overrides)).prove(f"{opp}-{seq}", oid, seq)
    assert receipt.verdict == UNDETERMINED
    defects = tuple(
        ComponentDefect(c, kinds.get(c, MISSING), f"{c}: {kinds.get(c, MISSING).lower()}")
        for c in unknowns
    )
    return RoundRecord(seq, oid, UNDETERMINED, adequate, defects=defects, receipt=receipt)


def bounded_contract(oid, bound):
    return FairnessContract(
        obligation_id=oid,
        revision="r1",
        standard="BOUNDED",
        eligibility_predicate="D58 six-component proof",
        service_predicate="adequate service evidenced",
        service_bound_rounds=bound,
        capacity_basis="8 slots provisioned for worker class W",
    )


def governor_with(rounds):
    g = UnresolvedEvidenceGovernor()
    for r in rounds:
        g.register_round(r)
    return g


# ---------------------------------------------------------------------------
# Positive: the honest path.
# ---------------------------------------------------------------------------

def test_all_proven_adequate_service_no_breach():
    g = governor_with([proven_round(1, "obl-A", True),
                       proven_round(2, "obl-A", True),
                       proven_round(3, "obl-A", True)])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert a.verdict == NO_BREACH
    assert (a.debt_min, a.debt_max) == (0, 0)
    assert a.histories_examined == 1
    assert a.unresolved_rounds == ()


def test_all_proven_repeated_inadequate_service_breach():
    g = governor_with([proven_round(s, "obl-A", False) for s in (1, 2, 3, 4)])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert a.verdict == BREACH
    assert (a.debt_min, a.debt_max) == (4, 4)


def test_aer_live_004_stays_unresolved():
    """Two proven rounds, one missing record, complete service history."""
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
    ])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert a.verdict == UNRESOLVED
    assert (a.debt_min, a.debt_max) == (2, 3)
    assert a.histories_examined == 2
    assert a.unresolved_rounds == (2,)
    # Neither witness manufactures a conclusion: both completions are live.
    assert a.breach_witness is not None and a.clearance_witness is not None


def test_fourth_proven_round_settles_without_recovery():
    """Stronger surrounding evidence settles the breach; round 2 is never
    recovered, never guessed."""
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
        proven_round(4, "obl-A", False),
    ])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    # min-debt history (round 2 ineligible): 1,1,2,3 -> 3 > 2. Settled.
    assert a.verdict == BREACH
    assert a.debt_min == 3
    assert a.unresolved_rounds == (2,)  # still unresolved — and still reported


def test_reconstruction_settling_eligible_establishes_breach():
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
    ])
    recon = g.open_reconstruction("obl-A", 2)
    assert recon.status == RECON_OPEN
    receipt = recon.attempt({AUTHORIZATION: ev(PROVEN, "law_registry", "auth recovered")})
    assert receipt.verdict == ELIGIBLE
    assert recon.status == RECON_SETTLED
    settled = g.apply_settlement(recon.repair_obligation_id)
    assert settled.verdict == ELIGIBLE and settled.defects == ()
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert a.verdict == BREACH
    assert (a.debt_min, a.debt_max) == (3, 3)


def test_reconstruction_settling_ineligible_clears():
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
    ])
    recon = g.open_reconstruction("obl-A", 2)
    receipt = recon.attempt({AUTHORIZATION: ev(REFUTED, "law_registry", "no authorization on file")})
    assert receipt.verdict == INELIGIBLE
    g.apply_settlement(recon.repair_obligation_id)
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert a.verdict == NO_BREACH
    assert (a.debt_min, a.debt_max) == (2, 2)


def test_defect_kinds_preserved_per_component():
    r = undetermined_round(2, "obl-A", False,
                           (AUTHORIZATION, CONSISTENT_ORDERING),
                           kinds={AUTHORIZATION: CONTRADICTORY,
                                  CONSISTENT_ORDERING: STALE})
    kinds = {d.component: d.kind for d in r.defects}
    assert kinds == {AUTHORIZATION: CONTRADICTORY, CONSISTENT_ORDERING: STALE}
    g = governor_with([proven_round(1, "obl-A", False), r])
    a = g.assess("obl-A", bounded_contract("obl-A", 5))
    assert a.verdict == NO_BREACH  # kinds don't change the arithmetic


def test_witnesses_attain_the_extremes():
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
    ])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    # breach witness: round 2 completed eligible -> debt 3
    assert dict(a.breach_witness)[2] is True
    # clearance witness: round 2 completed ineligible -> debt 2
    assert dict(a.clearance_witness)[2] is False


def test_adequate_service_resets_debt_inside_histories():
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", True),
    ])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    # both histories end at 0: (1,2,0) and (1,1,0)
    assert a.verdict == NO_BREACH
    assert (a.debt_min, a.debt_max) == (0, 0)


def test_reconstruction_merges_over_original_components():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2)
    receipt = recon.attempt({AUTHORIZATION: ev(PROVEN, "law_registry", "auth recovered")})
    comps = dict(receipt.components)
    assert comps[AUTHORIZATION].detail == "auth recovered"
    # untouched components keep their ORIGINAL evidence, not blanks
    assert comps[OUTSTANDING_WORK].detail == "tasks uncompleted"
    assert comps[OUTSTANDING_WORK].origin == "work_queue_snapshot"


def test_empty_attempt_consumes_budget_without_settling():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2, budget_attempts=3, repair_bound=5)
    receipt = recon.attempt({})
    assert receipt.verdict == UNDETERMINED
    assert recon.attempts_used == 1
    assert recon.status == RECON_OPEN


# ---------------------------------------------------------------------------
# Negative controls: every refusal path.
# ---------------------------------------------------------------------------

def test_duplicate_round_refused():
    g = governor_with([proven_round(1, "obl-A", True)])
    with pytest.raises(DuplicateRoundError):
        g.register_round(proven_round(1, "obl-A", True))


def test_assess_unknown_obligation_refused():
    g = UnresolvedEvidenceGovernor()
    with pytest.raises(UnknownObligationError):
        g.assess("obl-ghost", bounded_contract("obl-ghost", 2))


def test_assess_non_bounded_contract_refused():
    g = governor_with([proven_round(1, "obl-A", False)])
    weak = FairnessContract(
        obligation_id="obl-A", revision="r1", standard="WEAK",
        eligibility_predicate="p", service_predicate="q")
    with pytest.raises(UnboundedContractError):
        g.assess("obl-A", weak)


def test_history_space_cap_refused():
    rounds = [undetermined_round(s, "obl-A", False, (AUTHORIZATION,))
              for s in range(1, 14)]  # 13 > cap 12
    g = governor_with(rounds)
    with pytest.raises(HistorySpaceTooLargeError):
        g.assess("obl-A", bounded_contract("obl-A", 2))


def test_non_bool_service_outcome_refused():
    with pytest.raises(AssertionError):
        RoundRecord(1, "obl-A", ELIGIBLE, "yes")


def test_undetermined_without_defects_refused():
    with pytest.raises(AssertionError):
        RoundRecord(1, "obl-A", UNDETERMINED, False)


def test_defect_component_mismatch_refused():
    receipt = EligibilityProver(
        full_proven(**{AUTHORIZATION: ev(UNKNOWN, "absent", "missing")})
    ).prove("opp-1", "obl-A", 1)
    bad_defect = (ComponentDefect(CONSISTENT_ORDERING, MISSING, "wrong component"),)
    with pytest.raises(AssertionError):
        RoundRecord(1, "obl-A", UNDETERMINED, False,
                    defects=bad_defect, receipt=receipt)


def test_attempt_on_settled_reconstruction_refused():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2)
    recon.attempt({AUTHORIZATION: ev(PROVEN, "law_registry", "recovered")})
    assert recon.status == RECON_SETTLED
    with pytest.raises(ReconstructionStateError):
        recon.attempt({AUTHORIZATION: ev(PROVEN, "law_registry", "again")})


def test_tainted_reconstruction_evidence_caught():
    """The false-ineligibility mutation: settling via the scheduler's own
    flag is refused, not laundered into a verdict."""
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2)
    with pytest.raises(TaintedOriginError):
        recon.attempt({AUTHORIZATION: ev(REFUTED, "scheduler_flag", "scheduler says no")})
    assert recon.status == RECON_OPEN
    assert recon.attempts_used == 0  # refused attempts consume nothing


def test_unknown_component_in_reconstruction_refused():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2)
    with pytest.raises(UnknownComponentError):
        recon.attempt({"BUSYNESS": ev(PROVEN, "x", "not a component")})


def test_open_reconstruction_on_settled_round_refused():
    g = governor_with([proven_round(1, "obl-A", True)])
    with pytest.raises(ReconstructionStateError):
        g.open_reconstruction("obl-A", 1)


def test_double_open_reconstruction_refused():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    g.open_reconstruction("obl-A", 2)
    with pytest.raises(ReconstructionStateError):
        g.open_reconstruction("obl-A", 2)


def test_settled_round_record_before_settlement_refused():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2)
    with pytest.raises(ReconstructionStateError):
        recon.settled_round_record()
    with pytest.raises(ReconstructionStateError):
        g.apply_settlement(recon.repair_obligation_id)


def test_budget_exhaustion_escalates_history_preserved():
    g = governor_with([
        proven_round(1, "obl-A", False),
        undetermined_round(2, "obl-A", False, (AUTHORIZATION,)),
        proven_round(3, "obl-A", False),
    ])
    before = g.assess("obl-A", bounded_contract("obl-A", 2))
    recon = g.open_reconstruction("obl-A", 2, budget_attempts=2, repair_bound=5)
    recon.attempt({})
    recon.attempt({})
    assert recon.status == RECON_ESCALATED
    assert recon.escalation_reason == BUDGET_EXHAUSTED
    # History preserved: the assessment is unchanged — neither innocence
    # nor guilt was invented by the escalation.
    after = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert after.verdict == UNRESOLVED
    assert (after.debt_min, after.debt_max) == (before.debt_min, before.debt_max)


def test_repair_starvation_escalates_visibly():
    """The repair's own fairness contract fires: starving the repair is
    visible escalation, never a silent excuse."""
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2, budget_attempts=10, repair_bound=1)
    recon.attempt({})   # repair debt 1, still within bound
    assert recon.status == RECON_OPEN
    recon.attempt({})   # repair debt 2 > bound 1
    assert recon.status == RECON_ESCALATED
    assert recon.escalation_reason == REPAIR_STARVED


def test_attempt_on_escalated_reconstruction_refused():
    g = governor_with([undetermined_round(2, "obl-A", False, (AUTHORIZATION,))])
    recon = g.open_reconstruction("obl-A", 2, budget_attempts=1, repair_bound=5)
    recon.attempt({})
    assert recon.status == RECON_ESCALATED
    with pytest.raises(ReconstructionStateError):
        recon.attempt({AUTHORIZATION: ev(PROVEN, "law_registry", "too late")})


def test_breach_boundary_debt_equals_bound_is_not_breach():
    """Breach is strict: debt == bound has not exceeded the bound."""
    g = governor_with([proven_round(1, "obl-A", False),
                       proven_round(2, "obl-A", False)])
    a = g.assess("obl-A", bounded_contract("obl-A", 2))
    assert (a.debt_min, a.debt_max) == (2, 2)
    assert a.verdict == NO_BREACH


def test_no_bare_completion_is_ever_asserted():
    """The governor exposes no method that asserts a single completion as
    fact — completions exist only inside enumerated histories."""
    g = UnresolvedEvidenceGovernor()
    suspicious = [n for n in dir(g)
                  if any(k in n.lower() for k in ("was_eligible", "is_eligible",
                                                  "completed_as", "actual_",
                                                  "true_verdict", "resolve_round"))]
    assert suspicious == [], f"manufacture surface: {suspicious}"
    assert isinstance(g, UnresolvedEvidenceGovernor)
    assert ReconstructionObligation.__doc__ is not None
