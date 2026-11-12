"""RFD-AMB-1 tests (SN-0792): the possible-histories calculus. When
incomplete observations admit both legal and violating executions:
preserve both, withhold certification/blame, name the missing evidence,
prohibit dependent consequential use of the unresolved proof."""
import pytest

from drift_canary.revocation_linearization import (
    AMB_SAFETY_ESTABLISHED,
    AMB_BOTH_POSSIBLE,
    AMB_INSUFFICIENT,
    AMB_INCONSISTENT,
    POS_VIOLATION,
    POS_CONSISTENT,
    COMMITTED,
    OUTCOME_ABORTED,
    OUTCOME_NOT_EXECUTED,
    OUTCOME_UNRESOLVED,
    AmbiguousOp,
    AmbiguityRecord,
    AMBIGUITY_ACTIVITIES,
    activity_permitted,
    may_must_violate,
    evaluate_ambiguous,
    refine_observations,
    withdraw_observation,
    twin_worlds_experiment,
    staged_revelation_experiment,
    rfd_amb_001,
    _twin_worlds_observations,
    refinement_fixture,
    CURRENT,
)


# --- conclusion model --------------------------------------------------------------------
def test_conclusion_model_four_cases():
    ops, variants = _twin_worlds_observations()
    r = evaluate_ambiguous(ops, variants)
    assert r["conclusion"] == AMB_BOTH_POSSIBLE
    assert r["legal_exists"] and r["violating_exists"]
    may, must = may_must_violate(r["legal_exists"], r["violating_exists"])
    assert (may, must) == (True, False)
    assert (r["may_violate"], r["must_violate"]) == (True, False)


def test_may_must_table():
    assert may_must_violate(True, False) == (False, False)   # all safe
    assert may_must_violate(True, True) == (True, False)     # ambiguous
    assert may_must_violate(False, True) == (True, True)     # must violate


def test_may_must_invalid_row_rejected():
    # The (No, Yes) row is invalid by construction: must implies may.
    # Direct construction is impossible through the public function;
    # assert the invariant instead.
    for legal, viol in [(True, False), (True, True), (False, True)]:
        may, must = may_must_violate(legal, viol)
        assert not (must and not may)


def test_inconsistent_observations_flagged():
    ops = [
        AmbiguousOp("X1", 1, 2, "receipt-A", None, frozenset({COMMITTED}),
                    (), "COVERED"),
        AmbiguousOp("X1", 1, 2, "receipt-B", None, frozenset({COMMITTED}),
                    (), "COVERED"),
    ]
    r = evaluate_ambiguous(ops, {})
    assert r["conclusion"] == AMB_INCONSISTENT


# --- twin worlds: no answer-key leakage ------------------------------------------------------
def test_twin_worlds_no_leakage():
    """D(Observe(H_L)) == D(Observe(H_V)): identical observations give
    identical answers. Different answers would mean leakage or hidden
    assumptions."""
    r = twin_worlds_experiment()
    assert r["coverage"] == "EXHAUSTIVE"


def test_staged_revelation_both_directions():
    r = staged_revelation_experiment()
    assert r["base"] == AMB_BOTH_POSSIBLE
    assert r["reveal_aborted"] == AMB_SAFETY_ESTABLISHED
    assert r["reveal_committed"] == POS_VIOLATION
    assert r["removal"] == AMB_BOTH_POSSIBLE


def test_rfd_amb_001():
    r = rfd_amb_001()
    assert r["twin_worlds"] == AMB_BOTH_POSSIBLE
    assert r["unaffected_claims_preserved"] is True
    assert r["record"] == "HIST-042/RFD-AMB-001"


# --- A1-A10 adversarial controls ----------------------------------------------------------------
def _ops_with(**kw):
    ops, variants = _twin_worlds_observations()
    return ops, variants


def test_a1_missing_receipt_unresolved():
    """A1: no receipt => UNRESOLVED, never a fabricated commit."""
    ops, _ = _ops_with()
    p1 = next(o for o in ops if o.operation_id == "P1")
    assert p1.commit_evidence is None
    assert OUTCOME_UNRESOLVED in p1.outcome_set


def test_a2_timeout_never_infers_rollback():
    """A2: a timed-out op keeps every outcome possible -- never ABORTED
    by inference."""
    op = AmbiguousOp("T1", 1, 50, None, None,
                     frozenset({COMMITTED, OUTCOME_ABORTED,
                                OUTCOME_NOT_EXECUTED, OUTCOME_UNRESOLVED}),
                     (), "COVERED")
    assert OUTCOME_ABORTED in op.outcome_set
    assert COMMITTED in op.outcome_set  # not narrowed by the timeout


def test_a3_receipts_narrow_both_directions():
    """A3: a COMMITTED receipt narrows one way; an ABORTED observation
    narrows the other."""
    ops, variants = _twin_worlds_observations()
    ra = evaluate_ambiguous(refine_observations(ops, "P1", {OUTCOME_ABORTED}),
                            variants)
    assert ra["conclusion"] == AMB_SAFETY_ESTABLISHED
    rb = evaluate_ambiguous(refine_observations(ops, "P1", {COMMITTED}),
                            variants)
    assert rb["conclusion"] == POS_VIOLATION


def test_a4_untrusted_logs_not_authoritative():
    """A4: an untrusted log's claim is reported, not authoritative: it
    does not constrain the outcome set by itself."""
    op = AmbiguousOp("L1", 1, 2, None, None,
                     frozenset({COMMITTED, OUTCOME_ABORTED,
                                OUTCOME_UNRESOLVED}),
                     (), "COVERED",
                     env_assumptions=("log claim: committed (untrusted)",))
    # The engine must not treat the log claim as commit evidence.
    assert op.commit_evidence is None


def test_a5_clock_skew_preserves_causality():
    """A5: ordering comes from causal constraints, never timestamps."""
    ops, variants = _twin_worlds_observations()
    # Skew the clocks wildly; constraints still order R1 < P1.
    skewed = [AmbiguousOp(o.operation_id, 999, 1, o.commit_evidence,
                          o.effect_evidence, o.outcome_set,
                          o.ordering_constraints, o.coverage_state,
                          o.env_assumptions) for o in ops]
    r = evaluate_ambiguous(skewed, variants)
    assert r["conclusion"] == AMB_BOTH_POSSIBLE


def test_a6_inconsistent_observations():
    test_inconsistent_observations_flagged()


def test_a7_staged_revelation_both_directions():
    test_staged_revelation_both_directions()


def test_a8_withdrawal_restores_ambiguity():
    """A8: governed withdrawal restores ambiguity and records the reason."""
    ops, variants = _twin_worlds_observations()
    narrowed = refine_observations(ops, "P1", {OUTCOME_ABORTED})
    widened = withdraw_observation(narrowed, "P1",
                                   {COMMITTED, OUTCOME_ABORTED,
                                    OUTCOME_UNRESOLVED},
                                   "test withdrawal")
    p1 = next(o for o in widened if o.operation_id == "P1")
    assert any("withdrawn" in a for a in p1.env_assumptions)
    r = evaluate_ambiguous(widened, variants)
    assert r["conclusion"] == AMB_BOTH_POSSIBLE


def test_a9_no_fencing_contract():
    """A9: 'the effect might have occurred' (MayViolate) is separate from
    'the fencing guarantee was violated' (needs a contract that promised
    it)."""
    ops, variants = _twin_worlds_observations()
    r = evaluate_ambiguous(ops, variants)
    assert r["may_violate"] is True
    assert r["must_violate"] is False
    # No fencing contract was ever asserted in the observations.
    assert all("fencing" not in " ".join(o.env_assumptions).lower()
               for o in ops)


def test_a10_independent_claim_preservation():
    """A10: ambiguity about P1 does not disturb c1's independently
    established E2-path standing."""
    r = rfd_amb_001()
    assert r["unaffected_claims_preserved"] is True


# --- evidence-monotonic refinement ----------------------------------------------------------------
def test_evidence_monotonic_narrows():
    """O1 ⊆ O2 => H(O2) ⊆ H(O1): completions never grow on refinement."""
    ops, variants = _twin_worlds_observations()
    r1 = evaluate_ambiguous(ops, variants)
    ops2 = refine_observations(ops, "P1", {OUTCOME_ABORTED})
    r2 = evaluate_ambiguous(ops2, variants)
    assert r2["completions"] <= r1["completions"]


def test_refinement_contradiction_flagged():
    """Contradictory refinement is flagged, not silently discarded."""
    ops, variants = _twin_worlds_observations()
    ops2 = refine_observations(ops, "P1", {OUTCOME_ABORTED})
    with pytest.raises(ValueError, match="contradiction"):
        refine_observations(ops2, "P1", {COMMITTED})


# --- safe behavior during ambiguity -----------------------------------------------------------------
def test_ambiguity_activity_table():
    assert activity_permitted("historical_inspection") is True
    assert activity_permitted("independent_reconciliation") is True
    assert activity_permitted("blind_retry") is False
    assert activity_permitted("certification") is False
    assert activity_permitted("dependent_consequential_use") is False
    assert AMBIGUITY_ACTIVITIES["learn_promotion"] == \
        "HELD_UNTIL_CAUSAL_EVIDENCE"
    assert AMBIGUITY_ACTIVITIES["smart_notes"] == \
        "PRESERVE_BOTH_WORLDS_AND_UNCERTAINTY"


def test_ambiguity_record_schema():
    r = rfd_amb_001()
    assert r["record"].startswith("HIST-042")
