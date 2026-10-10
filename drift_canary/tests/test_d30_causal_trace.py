"""Tests for drift_canary/d30_causal_trace.py — D30 decisive experiment.

Rule under test: "Logs describe what components claim happened. Evidence
establishes what happened. Causal verification establishes why the
outcome occurred. A CORRELATES_WITH edge must never be silently promoted
to CAUSED_BY; HAPPENS_BEFORE establishes ordering, not causation."

The experiment: the same D29 controlled workflow (three injected
failures, same observable symptom — an uncompleted workflow) is
projected into canonical causal traces. An INDEPENDENT verifier,
reading ONLY the trace, must produce different verdicts from the
evidence; swapping narrative labels with the evidence unchanged must
not move the verdict; corrupting one producer's logs must downgrade to
uncertainty rather than follow the narrative.
"""
import dataclasses
import inspect

import pytest

from drift_canary.d29_boundary import (
    OBLIGATION_ID,
    ComponentReport,
    run_case,
)
from drift_canary.d30_causal_trace import (
    ENV_WITNESS,
    L0_REPORTED,
    L1_AUTHENTICATED,
    L2_CORROBORATED,
    L3_CAUSALLY_QUALIFIED,
    TRACE_MONITOR,
    VERDICTS,
    CausalTrace,
    CausalVerifier,
    EvidenceEvent,
    LogicalClock,
    adapt_d29_result,
    authenticate,
    build_correlation_edges,
    build_ordering_edges,
    deserialize_trace,
    event_body_hash,
    fresh_verifier_reproduces,
    make_event,
    observation_level,
    serialize_trace,
    tamper,
)

EXPECTED = {
    "A": "ENVIRONMENT_BLOCKER",
    "B": "SCHEDULER_STARVATION",
    "C": "WORKER_NONPROGRESS",
}


def traces():
    """The three canonical traces, adapted from D29's evidence layer."""
    return {c: adapt_d29_result(run_case(c)) for c in ("A", "B", "C")}


def corpus(exclude=None):
    ts = traces()
    return tuple(t for c, t in ts.items() if c != exclude)


# ---------------------------------------------------------------------------
# Canonical event integrity.
# ---------------------------------------------------------------------------
def test_producer_and_observer_are_separate():
    t = traces()["A"]
    assert t.events, "trace must carry events"
    for e in t.events:
        assert e.producer != e.observer, (
            f"{e.event_id}: self-certification must be impossible")


def test_self_certification_rejected_at_construction():
    with pytest.raises(AssertionError):
        EvidenceEvent(event_id="X", producer="P", observer="P",
                      trace_id="T")


def test_authentication_passes_on_intact_trace():
    t = traces()["B"]
    for e in t.events:
        ok, reason = authenticate(e)
        assert ok, f"{e.event_id}: {reason}"


def test_logical_clocks_order_parent_before_child():
    t = traces()["A"]
    by_id = {e.event_id: e for e in t.events}
    for e in t.events:
        for p in e.parent_ids:
            assert by_id[p].lamport < e.lamport, (
                f"parent {p} must happen-before child {e.event_id}")


def test_observation_starts_at_reported():
    t = traces()["A"]
    assert all(e.observation_status == "reported" for e in t.events)


# ---------------------------------------------------------------------------
# Sharpest case, part 1: same symptom, different verdicts — from the
# trace alone, with all three causal checks passing.
# ---------------------------------------------------------------------------
def test_same_symptom_different_verdicts():
    ts = traces()
    verdicts = {}
    for c, t in ts.items():
        v = CausalVerifier().verify(t, corpus=corpus(exclude=c))
        verdicts[c] = v
        assert v.verdict == EXPECTED[c], (
            f"case {c}: {v.verdict}; reasons: {v.reasons}")
        assert v.level >= L3_CAUSALLY_QUALIFIED, (
            f"case {c}: cause assigned but path never reached L3")
    assert {v.verdict for v in verdicts.values()} == set(EXPECTED.values())


def test_caused_by_edge_carries_all_three_checks():
    t = traces()["A"]
    v = CausalVerifier().verify(t, corpus=corpus(exclude="A"))
    caused = [e for e in v.edges if e.kind == "CAUSED_BY"]
    assert len(caused) == 1, (
        f"expected exactly one CAUSED_BY edge, got {len(caused)}")
    edge = caused[0]
    assert edge.checks == frozenset({"mechanism", "counterfactual",
                                     "independent_reproduction"}), edge.checks
    assert edge.basis, "CAUSED_BY edge must record its basis"


def test_caused_by_requires_all_three_checks_structurally():
    from drift_canary.d30_causal_trace import CausalEdge
    with pytest.raises(AssertionError):
        CausalEdge(kind="CAUSED_BY", source_id="s", target_id="t",
                   checks=frozenset({"mechanism"}))


def test_happens_before_never_claims_causation():
    t = traces()["C"]
    ordering = build_ordering_edges(t)
    assert ordering, "ordering edges must be derivable"
    assert all(e.kind == "HAPPENS_BEFORE" for e in ordering)
    assert all(not e.checks for e in ordering), (
        "ordering edges carry no causal checks")


def test_correlates_with_never_silently_promoted():
    # Case A: RESOURCE_UNAVAILABLE and SERVICE_INADEQUATE co-occur every
    # round. The co-occurrence is emitted as CORRELATES_WITH — and the
    # trace carries no path by which it could become CAUSED_BY without
    # the three checks.
    t = traces()["A"]
    corrs = build_correlation_edges(t)
    assert corrs, "expected co-occurrence edges in case A"
    assert all(e.kind == "CORRELATES_WITH" for e in corrs)
    assert all(not e.checks for e in corrs)
    v = CausalVerifier().verify(t, corpus=corpus(exclude="A"))
    kinds = {e.kind for e in v.edges}
    assert "CAUSED_BY" in kinds  # the verified path exists too
    # ...but every CAUSED_BY edge names its checks; none was promoted.
    for e in v.edges:
        if e.kind == "CAUSED_BY":
            assert len(e.checks) == 3


# ---------------------------------------------------------------------------
# Sharpest case, part 2: label swap with evidence unchanged.
# ---------------------------------------------------------------------------
def test_trace_carries_no_narrative_labels():
    labels = ("DATABASE_UNAVAILABLE", "SCHEDULER_STARVATION",
              "ENVIRONMENT_BLOCKER", "WORKER_FAILURE")
    for c, t in traces().items():
        blob = serialize_trace(t).decode("utf-8")
        for label in labels:
            assert label not in blob, (
                f"case {c}: narrative label {label} leaked into the trace")


def test_label_swap_verdict_stable():
    swapped = {
        "A": (ComponentReport("SCHEDULER", "SCHEDULER_STARVATION", 1),
              ComponentReport("ENVIRONMENT", "ENVIRONMENT_BLOCKER", 1)),
        "B": (ComponentReport("SCHEDULER", "ENVIRONMENT_BLOCKER", 1),
              ComponentReport("ENVIRONMENT", "SCHEDULER_STARVATION", 1)),
        "C": (ComponentReport("WORKER", "ENVIRONMENT_BLOCKER", 1),
              ComponentReport("SCHEDULER", "SCHEDULER_STARVATION", 1)),
    }
    for c in ("A", "B", "C"):
        clean = adapt_d29_result(run_case(c))
        blamed = adapt_d29_result(run_case(c, false_blame=swapped[c]))
        # Evidence unchanged: the adapted traces are byte-identical.
        assert serialize_trace(clean) == serialize_trace(blamed), (
            f"case {c}: labels altered the trace bytes")
        v1 = CausalVerifier().verify(clean, corpus=corpus(exclude=c))
        v2 = CausalVerifier().verify(blamed, corpus=corpus(exclude=c))
        assert v1.verdict == v2.verdict == EXPECTED[c], (
            f"case {c}: label swap moved the verdict")


def test_verifier_has_no_label_input():
    params = inspect.signature(CausalVerifier.verify).parameters
    forbidden = {"label", "labels", "report", "reports", "narrative",
                 "component_report", "component_reports", "result"}
    assert not (set(params) & forbidden), (
        f"verify accepts label-like inputs: {set(params) & forbidden}")


# ---------------------------------------------------------------------------
# Sharpest case, part 3: corrupt one producer's logs.
# ---------------------------------------------------------------------------
def test_corrupted_producer_logs_downgrade_to_uncertainty():
    t = traces()["B"]
    corrupted_events = []
    for e in t.events:
        if e.producer == "SCHEDULER":
            # Compromised log: rewrite the observed state without
            # resealing — the attestation no longer binds.
            corrupted_events.append(tamper(e, state_after="debt=0",
                                           condition="SERVICE_ADEQUATE"))
        else:
            corrupted_events.append(e)
    corrupted = CausalTrace(trace_id=t.trace_id,
                            events=tuple(corrupted_events), edges=())
    v = CausalVerifier().verify(corrupted, corpus=corpus(exclude="B"))
    assert v.verdict == "INSUFFICIENT_OBSERVABILITY", (
        f"tampered trace must yield uncertainty, got {v.verdict}")
    assert v.controller == "UNDETERMINED"
    assert "WORKER_NONPROGRESS" != v.verdict
    assert any("failed authentication" in r for r in v.reasons)


def test_corrupted_env_witness_cannot_fabricate_blocker():
    # Flip case B's environment observations to claim an outage, without
    # resealing: the verifier must reject the false evidence, not follow
    # the fabricated narrative.
    t = traces()["B"]
    corrupted_events = []
    for e in t.events:
        if e.producer == ENV_WITNESS:
            corrupted_events.append(tamper(
                e, condition="RESOURCE_UNAVAILABLE",
                state_before="DB-CONN:UNAVAILABLE",
                state_after="DB-CONN:UNAVAILABLE"))
        else:
            corrupted_events.append(e)
    corrupted = CausalTrace(trace_id=t.trace_id,
                            events=tuple(corrupted_events), edges=())
    v = CausalVerifier().verify(corrupted, corpus=corpus(exclude="B"))
    assert v.verdict != "ENVIRONMENT_BLOCKER", (
        "verifier followed fabricated environment evidence")
    assert v.verdict == "INSUFFICIENT_OBSERVABILITY"


def test_tamper_cannot_reseal():
    t = traces()["A"]
    e = t.events[0]
    with pytest.raises(AssertionError):
        tamper(e, artifact_hash="00" * 32)


# ---------------------------------------------------------------------------
# Negative claims need coverage evidence.
# ---------------------------------------------------------------------------
def test_env_coverage_gap_blocks_negative_claim():
    # Remove half the environment observations from case A: the claim
    # "the resource was NEVER available" is no longer coverable.
    t = traces()["A"]
    kept = [e for i, e in enumerate(t.events)
            if not (e.producer == ENV_WITNESS and i % 2 == 0)]
    gapped = CausalTrace(trace_id=t.trace_id, events=tuple(kept), edges=())
    v = CausalVerifier().verify(gapped, corpus=corpus(exclude="A"))
    assert v.verdict == "INSUFFICIENT_OBSERVABILITY", (
        f"coverage gap must yield uncertainty, got {v.verdict}")
    assert any("coverage gap" in r for r in v.reasons)


def test_no_environment_observations_is_uncertainty_not_blame():
    # Case B without the environment witness: the scheduler's debt is
    # evidenced, but the environment explanation can no longer be ruled
    # out — the verdict must preserve the competing explanations rather
    # than blame the scheduler by default.
    t = traces()["B"]
    kept = [e for e in t.events if e.producer != ENV_WITNESS]
    blind = CausalTrace(trace_id=t.trace_id, events=tuple(kept), edges=())
    v = CausalVerifier().verify(blind, corpus=corpus(exclude="B"))
    assert v.verdict == "BOUNDARY_UNDETERMINED", v.verdict
    assert v.controller == "UNDETERMINED"
    assert "SCHEDULER_STARVATION" in v.explanations_preserved
    assert "ENVIRONMENT_BLOCKER" in v.explanations_preserved


def test_worker_verdict_needs_no_env_witness():
    # Case C's worker claim is POSITIVE — adequate service corroborated
    # by worker acks — so it survives the loss of the environment
    # witness. Positive claims do not need the environment's coverage.
    t = traces()["C"]
    kept = [e for e in t.events if e.producer != ENV_WITNESS]
    blind = CausalTrace(trace_id=t.trace_id, events=tuple(kept), edges=())
    v = CausalVerifier().verify(blind, corpus=corpus(exclude="C"))
    assert v.verdict == "WORKER_NONPROGRESS", v.verdict


# ---------------------------------------------------------------------------
# Competing explanations are preserved until evidence distinguishes them.
# ---------------------------------------------------------------------------
def test_competing_explanations_preserved_on_uncertainty():
    t = traces()["A"]
    kept = [e for i, e in enumerate(t.events)
            if not (e.producer == ENV_WITNESS and i % 2 == 0)]
    gapped = CausalTrace(trace_id=t.trace_id, events=tuple(kept), edges=())
    v = CausalVerifier().verify(gapped, corpus=corpus(exclude="A"))
    assert v.verdict == "INSUFFICIENT_OBSERVABILITY"
    assert set(v.explanations_preserved) >= {
        "ENVIRONMENT_BLOCKER", "SCHEDULER_STARVATION", "WORKER_NONPROGRESS"}, (
        "competing explanations must be preserved, not discarded")


def test_decided_verdict_preserves_nothing():
    t = traces()["C"]
    v = CausalVerifier().verify(t, corpus=corpus(exclude="C"))
    assert v.verdict == "WORKER_NONPROGRESS"
    assert v.explanations_preserved == ()


# ---------------------------------------------------------------------------
# Evidence of done: a fresh independent verifier reproduces the
# conclusion without trusting original logs/labels/agents.
# ---------------------------------------------------------------------------
def test_fresh_verifier_reproduces_all_cases():
    for c, expected in EXPECTED.items():
        t = adapt_d29_result(run_case(c))
        ok, detail = fresh_verifier_reproduces(t, corpus=corpus(exclude=c))
        assert ok, f"case {c}: {detail}"


def test_reproduction_uses_bytes_only():
    t = traces()["A"]
    blob = serialize_trace(t)
    rebuilt = deserialize_trace(blob)
    assert rebuilt is not t
    assert rebuilt.events[0] is not t.events[0]
    assert serialize_trace(rebuilt) == blob, "round-trip must be stable"
    v1 = CausalVerifier().verify(t, corpus=corpus(exclude="A"))
    v2 = CausalVerifier().verify(rebuilt, corpus=corpus(exclude="A"))
    assert (v1.verdict, v1.controller) == (v2.verdict, v2.controller)


def test_verdict_vocabulary_closed():
    for c in ("A", "B", "C"):
        v = CausalVerifier().verify(traces()[c], corpus=corpus(exclude=c))
        assert v.verdict in VERDICTS, v.verdict


# ---------------------------------------------------------------------------
# The ladder: L0 -> L1 -> L2 -> L3 is earned, never assumed.
# ---------------------------------------------------------------------------
def test_ladder_levels_earned_in_order():
    t = traces()["B"]
    # Unauthenticated (tampered) event: stuck at L0.
    bad = tamper(t.events[0], condition="RESOURCE_UNAVAILABLE")
    assert observation_level(bad, t) == L0_REPORTED
    # Intact event: at least L1.
    assert observation_level(t.events[0], t) >= L1_AUTHENTICATED
    # Independently corroborated: L2 for events with a consistent
    # second-producer observation in the window.
    levels = [observation_level(e, t) for e in t.events]
    assert max(levels) >= L2_CORROBORATED, levels
    # Causally qualified: L3 only on the verified path.
    v = CausalVerifier().verify(t, corpus=corpus(exclude="B"))
    assert v.level >= L3_CAUSALLY_QUALIFIED


def test_single_producer_cannot_corroborate_itself():
    # A trace where every event comes from one producer: no event can
    # reach L2, because corroboration requires an INDEPENDENT producer.
    clock = LogicalClock()
    solo = tuple(
        make_event(f"SOLO-{i}", producer="SCHEDULER",
                   observer=TRACE_MONITOR, trace_id="SOLO", clock=clock,
                   condition="SERVICE_INADEQUATE")
        for i in range(3))
    t = CausalTrace(trace_id="SOLO", events=solo, edges=())
    assert all(observation_level(e, t) == L1_AUTHENTICATED for e in solo)


def test_observer_attestation_binds_observer():
    t = traces()["A"]
    e = t.events[0]
    forged = dataclasses.replace(e, observer="SCHEDULER")
    ok, _ = authenticate(forged)
    assert not ok, "swapping the observer must break the attestation"
