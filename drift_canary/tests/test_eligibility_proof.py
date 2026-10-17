"""Tests for drift_canary/eligibility_proof.py (D58 / AER-LIVE-3).

Negative controls throughout: every refusal path is exercised, and the
sabotage-sensitive invariants (UNDETERMINED never counts, tainted origins
never yield ELIGIBLE, busyness can never make ineligible) are pinned by
dedicated tests.
"""
import dataclasses

import pytest

from drift_canary.eligibility_proof import (
    APPLICABLE_OPPORTUNITY,
    AUTHORIZATION,
    CONSISTENT,
    CONSISTENT_ORDERING,
    DEFERRED,
    ELIGIBLE,
    FALSE_CLAIM,
    HIDDEN_OPPORTUNITY,
    INELIGIBLE,
    NOT_ASSESSED,
    OUTSTANDING_WORK,
    READY_DEPENDENCIES,
    SCHEDULABLE_CAPACITY,
    TAINTED_ORIGINS,
    UNDETERMINED,
    UNKNOWN,
    PROVEN,
    REFUTED,
    COMPONENTS,
    EligibilityBoundCounter,
    EligibilityProver,
    Evidence,
    TaintedOriginError,
    UnknownComponentError,
)


def ev(status, origin="law_registry", detail="checked"):
    return Evidence(status, detail, origin)


def full_proven(**overrides):
    """A complete six-component PROVEN evidence set. Overrides by component."""
    base = {
        AUTHORIZATION: ev(PROVEN, "law_registry", "LAW authorization held at round 7"),
        OUTSTANDING_WORK: ev(PROVEN, "work_queue_snapshot", "3 tasks uncompleted at round 7"),
        READY_DEPENDENCIES: ev(PROVEN, "dependency_graph", "all 2 deps satisfied at round 7"),
        SCHEDULABLE_CAPACITY: ev(PROVEN, "capacity_plan",
                                "worker class W: 8 slots provisioned, obligation routable"),
        APPLICABLE_OPPORTUNITY: ev(PROVEN, "scheduler_tick_log", "round 7 tick recorded"),
        CONSISTENT_ORDERING: ev(PROVEN, "ordering_log", "single authoritative ordering, no fork"),
    }
    base.update(overrides)
    return base


def prover_for(source):
    return EligibilityProver(source)


# ---------------------------------------------------------------------------
# Positive: the honest path.
# ---------------------------------------------------------------------------

def test_all_six_proven_yields_eligible_and_counts():
    p = prover_for(full_proven())
    r = p.prove("opp-1", "obl-A", 7)
    assert r.verdict == ELIGIBLE
    assert r.counts_toward_bound is True
    assert r.recovery_obligation == ()
    assert r.refuted == () and r.unknown == ()
    assert [c for c, _ in r.components] == list(COMPONENTS)


def test_counter_debt_accumulates_only_eligible():
    p = prover_for(full_proven())
    counter = EligibilityBoundCounter()
    assert counter.count(p.prove("opp-1", "obl-A", 7)) == 1
    assert counter.count(p.prove("opp-2", "obl-A", 8)) == 1
    assert counter.debt_for("obl-A") == 2


def test_e2a_hidden_opportunities_detected_and_counted():
    """E2-a: scheduler records eligible=false on three genuine opportunities
    and never serves the task. The verifier must find the breach the flags hid."""
    p = prover_for(full_proven())
    counter = EligibilityBoundCounter()
    for i in range(3):
        r = p.prove(f"opp-e2a-{i}", "obl-starved", 10 + i, scheduler_flag=False)
        assert r.verdict == ELIGIBLE, "genuine opportunity must be proven eligible"
        assert r.flag_assessment == HIDDEN_OPPORTUNITY
        assert counter.count(r) == 1
    assert counter.debt_for("obl-starved") == 3
    assert len(counter.hidden_opportunities()) == 3


def test_e2b_false_claim_refused_no_violation_manufactured():
    """E2-b: no LAW authorization while the worker asserts eligible=true.
    The verifier must refuse the false claim — and must not manufacture a
    fairness violation from the refusal."""
    source = full_proven(**{
        AUTHORIZATION: ev(REFUTED, "law_registry", "no authorization record for round 7"),
    })
    p = prover_for(source)
    r = p.prove("opp-e2b", "obl-X", 7, scheduler_flag=True)
    assert r.verdict == INELIGIBLE
    assert r.refuted == (AUTHORIZATION,)
    assert r.counts_toward_bound is False
    assert r.flag_assessment == FALSE_CLAIM
    # The receipt carries no violation attribution: refusing a false claim
    # is not accusing anyone of a fairness breach.
    assert not hasattr(r, "violation")


def test_each_refuted_component_yields_ineligible():
    """Every single component, refuted alone, sinks the verdict."""
    for component in COMPONENTS:
        source = full_proven(**{component: ev(REFUTED, "independent_source",
                                              f"{component} refuted")})
        r = prover_for(source).prove("opp", "obl", 1)
        assert r.verdict == INELIGIBLE, component
        assert r.refuted == (component,), component
        assert r.counts_toward_bound is False, component


# ---------------------------------------------------------------------------
# Three-valued verdicts: UNDETERMINED is not a soft INELIGIBLE.
# ---------------------------------------------------------------------------

def test_unknown_yields_undetermined_with_recovery_obligation():
    source = full_proven(**{
        READY_DEPENDENCIES: ev(UNKNOWN, "dependency_graph", "graph snapshot unavailable"),
    })
    r = prover_for(source).prove("opp-u", "obl-U", 3)
    assert r.verdict == UNDETERMINED
    assert r.unknown == (READY_DEPENDENCIES,)
    assert r.recovery_obligation == (READY_DEPENDENCIES,)
    assert r.counts_toward_bound is False
    assert r.refuted == ()


def test_undetermined_defers_flag_judgment_both_directions():
    """Unknown eligibility manufactures neither a violation nor a clearance."""
    source = full_proven(**{AUTHORIZATION: ev(UNKNOWN, "absent", "not supplied")})
    p = prover_for(source)
    assert p.prove("o1", "obl", 1, scheduler_flag=True).flag_assessment == DEFERRED
    assert p.prove("o2", "obl", 1, scheduler_flag=False).flag_assessment == DEFERRED


def test_undetermined_never_counts_even_across_many_rounds():
    p = prover_for({})  # nothing supplied: everything UNKNOWN
    counter = EligibilityBoundCounter()
    for i in range(5):
        r = p.prove(f"opp-{i}", "obl-G", i, scheduler_flag=True)
        assert r.verdict == UNDETERMINED
        assert counter.count(r) == 0
    assert counter.debt_for("obl-G") == 0
    assert len(counter.open_recoveries()) == 5


def test_missing_component_defaults_to_unknown_not_proven():
    """Absent evidence is UNKNOWN (fail closed), never silently PROVEN."""
    source = full_proven()
    del source[APPLICABLE_OPPORTUNITY]
    r = prover_for(source).prove("opp", "obl", 1)
    assert r.verdict == UNDETERMINED
    assert r.unknown == (APPLICABLE_OPPORTUNITY,)
    assert r.recovery_obligation == (APPLICABLE_OPPORTUNITY,)


# ---------------------------------------------------------------------------
# Origin discipline: worker/scheduler claims are not evidence.
# ---------------------------------------------------------------------------

def test_tainted_origin_rejected_even_when_all_proven():
    """A scheduler-flag-backed 'proof' must fail closed, not fail open."""
    for tainted in TAINTED_ORIGINS:
        source = full_proven(**{
            AUTHORIZATION: ev(PROVEN, tainted, "flag said eligible"),
        })
        with pytest.raises(TaintedOriginError):
            prover_for(source).prove("opp", "obl", 1)
    # The tainted origin can never yield ELIGIBLE — the raise happens first.
    assert len(TAINTED_ORIGINS) >= 5


def test_unknown_component_rejected_fail_closed():
    """A seventh component (e.g. smuggled busyness) is rejected outright."""
    source = full_proven()
    source["WORKERS_BUSY_AT_TICK"] = ev(REFUTED, "scheduler_trace", "all busy")
    with pytest.raises(UnknownComponentError):
        EligibilityProver(source)


def test_non_evidence_value_rejected():
    source = full_proven()
    source[AUTHORIZATION] = {"status": PROVEN}  # not an Evidence instance
    with pytest.raises(Exception):
        prover_for(source).prove("opp", "obl", 1)


# ---------------------------------------------------------------------------
# The busy-guard: contention never makes a task ineligible.
# ---------------------------------------------------------------------------

def test_busy_tick_still_eligible_when_capacity_structural():
    """All workers busy at the selection instant; capacity is structural
    (provisioned + routable), so the opportunity stays ELIGIBLE."""
    source = full_proven(**{
        SCHEDULABLE_CAPACITY: ev(
            PROVEN, "capacity_plan",
            "class W: 8 slots provisioned, obligation routable; "
            "tick 7: all 4 workers busy at selection instant — "
            "busyness is not an input to this component"),
    })
    r = prover_for(source).prove("opp-busy", "obl-B", 7)
    assert r.verdict == ELIGIBLE
    assert r.counts_toward_bound is True


def test_busyness_has_no_field_in_evidence_model():
    """The guard is structural: busyness cannot be expressed as evidence."""
    field_names = {f.name for f in dataclasses.fields(Evidence)}
    assert field_names == {"status", "detail", "origin"}
    assert not any("busy" in n for n in field_names)


def test_zero_provisioned_capacity_refutes_structurally():
    """REFUTED capacity is about provisioning, not busyness."""
    source = full_proven(**{
        SCHEDULABLE_CAPACITY: ev(REFUTED, "capacity_plan",
                                "class W: 0 slots provisioned — nothing to route to"),
    })
    r = prover_for(source).prove("opp", "obl", 1)
    assert r.verdict == INELIGIBLE
    assert r.refuted == (SCHEDULABLE_CAPACITY,)


# ---------------------------------------------------------------------------
# Flag assessment matrix.
# ---------------------------------------------------------------------------

def test_flag_assessment_matrix():
    p = prover_for(full_proven())
    assert p.prove("o", "b", 1, True).flag_assessment == CONSISTENT
    assert p.prove("o", "b", 1, False).flag_assessment == HIDDEN_OPPORTUNITY
    assert p.prove("o", "b", 1, None).flag_assessment == NOT_ASSESSED

    p2 = prover_for(full_proven(**{OUTSTANDING_WORK: ev(REFUTED, "work_queue_snapshot",
                                                            "already complete")}))
    assert p2.prove("o", "b", 1, False).flag_assessment == CONSISTENT
    assert p2.prove("o", "b", 1, True).flag_assessment == FALSE_CLAIM
    assert p2.prove("o", "b", 1, None).flag_assessment == NOT_ASSESSED


def test_ordering_conflict_refutes_ordering():
    """Two conflicting ordering records for one round: no consistent order."""
    source = full_proven(**{
        CONSISTENT_ORDERING: ev(REFUTED, "ordering_log",
                               "round 9 appears in two conflicting orderings"),
    })
    r = prover_for(source).prove("opp-ord", "obl-O", 9)
    assert r.verdict == INELIGIBLE
    assert r.refuted == (CONSISTENT_ORDERING,)


# ---------------------------------------------------------------------------
# Receipt integrity.
# ---------------------------------------------------------------------------

def test_receipt_is_frozen():
    r = prover_for(full_proven()).prove("opp", "obl", 1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.verdict = INELIGIBLE  # type: ignore[misc]


def test_receipt_invariants_enforced_at_construction():
    good = prover_for(full_proven()).prove("opp", "obl", 1)
    d = good.to_dict()
    assert d["verdict"] == ELIGIBLE and d["counts_toward_bound"] is True
    assert set(d["components"]) == set(COMPONENTS)
    # A hand-built ELIGIBLE receipt that does not count is rejected.
    with pytest.raises(AssertionError):
        from drift_canary.eligibility_proof import EligibilityReceipt
        EligibilityReceipt(
            opportunity_id="x", obligation_id="y", round_seq=1,
            verdict=ELIGIBLE, components=good.components,
            counts_toward_bound=False)
    # A hand-built UNDETERMINED receipt that accuses via flag is rejected.
    with pytest.raises(AssertionError):
        from drift_canary.eligibility_proof import EligibilityReceipt
        EligibilityReceipt(
            opportunity_id="x", obligation_id="y", round_seq=1,
            verdict=UNDETERMINED, components=good.components,
            unknown=(AUTHORIZATION,), recovery_obligation=(AUTHORIZATION,),
            flag_assessment=HIDDEN_OPPORTUNITY)


def test_counter_helpers_surface_e2_signals():
    p = prover_for(full_proven())
    counter = EligibilityBoundCounter()
    counter.count(p.prove("h1", "obl", 1, scheduler_flag=False))  # hidden
    p2 = prover_for(full_proven(**{AUTHORIZATION: ev(REFUTED, "law_registry", "no auth")}))
    counter.count(p2.prove("f1", "obl", 1, scheduler_flag=True))   # false claim
    assert [r.opportunity_id for r in counter.hidden_opportunities()] == ["h1"]
    assert [r.opportunity_id for r in counter.false_claims()] == ["f1"]
    assert counter.debt_for("obl") == 1  # only the hidden (genuine) one counts


def test_evidence_requires_status_detail_origin():
    with pytest.raises(AssertionError):
        Evidence("MAYBE", "x", "y")
    with pytest.raises(AssertionError):
        Evidence(PROVEN, "", "y")
    with pytest.raises(AssertionError):
        Evidence(PROVEN, "x", "")
