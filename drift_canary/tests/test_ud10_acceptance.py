"""UD-10 acceptance gate — SAY "WE DON'T KNOW" INSTEAD OF INVENTING ANSWERS.

ACCEPTANCE GATE: PASS only if
  (1) uncertainty is preserved in all four dimensions,
  (2) partial repairs are recognized without false completion claims,
  (3) twin-world fixtures stay ambiguous until evidence arrives, and
  (4) nothing unresolved ever promotes to verified.
One failure = FAIL.

Composes the real machinery: D31 (incident verdict, four dimensions,
hypotheses) + D42 (possible histories, twin worlds, staged narrowing).
"""

import dataclasses

import pytest

from drift_canary.d30_causal_trace import LogicalClock, make_event
from drift_canary.d31_incident import (
    Blocker,
    BlockerGraph,
    EvidenceState,
    Hypothesis,
    Incident,
    IncidentAnalyzer,
    IncidentVerdict,
    ObservationScope,
)
from drift_canary.d42_possible_histories import (
    AMBIGUOUS_BOTH_POSSIBLE,
    COMMITTED,
    SAFETY_ESTABLISHED_IN_SCOPE,
    VIOLATION_ESTABLISHED,
    Observation as HObservation,
    PossibleHistories,
    SafetyPolicy,
    diagnose,
)


# ---------------------------------------------------------------------------
# (1) uncertainty preserved in all four dimensions; NO failure_reason field
# ---------------------------------------------------------------------------

def _evt(eid, producer, observer, clock, condition=""):
    return make_event(event_id=eid, producer=producer, observer=observer,
                      trace_id="ud10", clock=clock, condition=condition,
                      state_before="before", state_after="after")


def build_ambiguous_incident():
    """RFD-AMB-001 as a D31 incident: request sent, revocation committed,
    effect receipt missing. Two competing hypotheses, both unresolved."""
    clock = LogicalClock()
    ev = EvidenceState()
    req = _evt("ev-request-sent", "dispatcher", "dispatch-log",
               clock, condition="REQUEST_SENT")
    rev = _evt("ev-revocation-committed", "governance", "governance-ledger",
               clock, condition="REVOCATION_COMMITTED")
    for e in (req, rev):
        ev.add_event(e)

    scopes = (
        ObservationScope(
            scope_id="dispatch-log-window", source="dispatch-log",
            event_type="request", resource_id="op-127",
            interval=(req.lamport, req.lamport),
            observability="COVERED_COMPLETE"),
        ObservationScope(
            scope_id="effect-receipt-window", source="effect-receipts",
            event_type="effect", resource_id="op-127",
            interval=(rev.lamport, rev.lamport + 10),
            observability="UNOBSERVED"),
    )
    hypotheses = (
        Hypothesis(
            hypothesis_id="h-effect-before-revoke",
            mechanism="the effect committed before the revocation landed",
            contribution_type="prevents_progress",
            relates_to=(),
            competing_with=("h-effect-after-revoke",),
            next_discriminating_test="t-fetch-effect-receipt-ts"),
        Hypothesis(
            hypothesis_id="h-effect-after-revoke",
            mechanism="the effect committed after the revocation, "
                      "against the established fence",
            contribution_type="prevents_progress",
            relates_to=(),
            competing_with=("h-effect-before-revoke",),
            next_discriminating_test="t-audit-fence-log"),
    )
    return Incident(incident_id="ud10-amb001", scopes=scopes, evidence=ev,
                    blockers=BlockerGraph(), hypotheses=hypotheses)


def test_no_failure_reason_field():
    fields = {f.name for f in dataclasses.fields(IncidentVerdict)}
    assert "failure_reason" not in fields
    v = IncidentAnalyzer().verdict(build_ambiguous_incident())
    assert not hasattr(v, "failure_reason")
    assert "failure_reason" not in v.render()


def test_four_dimensions_preserved_independently():
    v = IncidentAnalyzer().verdict(build_ambiguous_incident())
    # Dimension 1 — observability: the unobserved receipt window is named.
    assert v.unobservable_scopes == ("effect-receipt-window",)
    # Dimension 2 — evidence state: present (possibly empty verdicts tuple).
    assert isinstance(v.claim_verdicts, tuple)
    # Dimension 3 — blocker state: present as its own dimension.
    assert isinstance(v.blockers_established, tuple)
    assert isinstance(v.minimal_blocking_sets, tuple)
    # Dimension 4 — causal state: both hypotheses preserved, unresolved.
    assert set(v.unresolved_hypotheses) == {
        "h-effect-before-revoke", "h-effect-after-revoke"}
    # The discriminating tests name what would resolve the ambiguity.
    assert "t-fetch-effect-receipt-ts" in v.discriminating_tests
    assert "t-audit-fence-log" in v.discriminating_tests


# ---------------------------------------------------------------------------
# (2) partial repairs recognized without false completion claims
# ---------------------------------------------------------------------------

def build_two_blocker_incident():
    clock = LogicalClock()
    ev = EvidenceState()
    e1 = _evt("ev-b1", "law-engine", "auth-monitor", clock,
              condition="AUTH_EXPIRED")
    e2 = _evt("ev-b2", "worker-pool", "pool-monitor", clock,
              condition="WORKER_UNAVAILABLE")
    rep = _evt("ev-repair", "worker-pool", "pool-monitor", clock,
               condition="WORKER_REPAIRED")
    for e in (e1, e2, rep):
        ev.add_event(e)
    graph = BlockerGraph(blocking_sets=(
        frozenset({"b-auth"}), frozenset({"b-worker"})))
    graph.add_blocker(Blocker(blocker_id="b-auth",
                             description="auth expired",
                             condition="AUTH_EXPIRED",
                             established_by=("ev-b1",)))
    graph.add_blocker(Blocker(blocker_id="b-worker",
                             description="worker unavailable",
                             condition="WORKER_UNAVAILABLE",
                             established_by=("ev-b2",)))
    incident = Incident(incident_id="ud10-partial", scopes=(),
                        evidence=ev, blockers=graph, hypotheses=())
    return incident, rep


def test_partial_repair_recognized_without_false_completion():
    incident, repair_ev = build_two_blocker_incident()
    recognized, still_blocked, _ = incident.blockers.apply_intervention(
        "b-worker", repair_ev)
    assert recognized is True
    assert still_blocked is True
    v = IncidentAnalyzer().verdict(incident)
    assert v.blockers_repaired == ("b-worker",)
    assert v.is_blocked is True
    assert v.completion_declared is False
    rendered = v.render()
    assert "partial repair" in rendered
    assert "not completion" in rendered


# ---------------------------------------------------------------------------
# (3) twin-world fixtures stay ambiguous until evidence arrives
# ---------------------------------------------------------------------------

def _amb001():
    from drift_canary.d42_possible_histories import Scenario
    def coherent(f):
        out, tim = f["effect_outcome"], f["effect_timing"]
        if out in ("ABORTED", "NOT_EXECUTED"):
            return tim == "NEVER"
        if out == "COMMITTED":
            return tim in ("BEFORE_REVOKE", "AFTER_REVOKE")
        return True
    def violates(f):
        return (f["effect_outcome"] == "COMMITTED"
                and f["effect_timing"] == "AFTER_REVOKE")
    scenario = Scenario(
        scenario_id="RFD-AMB-001",
        fact_domains=(
            ("request_outcome", (COMMITTED,)),
            ("revocation_outcome", (COMMITTED,)),
            ("effect_outcome",
             (COMMITTED, "ABORTED", "NOT_EXECUTED", "UNRESOLVED")),
            ("effect_timing",
             ("BEFORE_REVOKE", "AFTER_REVOKE", "NEVER")),
        ),
        constraints=(coherent,), violates=violates)
    base = (
        HObservation("o-req", "request_outcome", (COMMITTED,),
                     source="dispatch-log", trusted=True),
        HObservation("o-rev", "revocation_outcome", (COMMITTED,),
                     source="governance-ledger", trusted=True),
    )
    return scenario, base


def test_twin_worlds_stay_ambiguous_until_evidence():
    scenario, base = _amb001()
    # Two sealed worlds, identical observations. The worker never sees
    # which world is real.
    d_world_l = diagnose(PossibleHistories(scenario, base))
    d_world_v = diagnose(PossibleHistories(scenario, base))
    assert d_world_l["verdict"] == AMBIGUOUS_BOTH_POSSIBLE
    assert d_world_v["verdict"] == AMBIGUOUS_BOTH_POSSIBLE
    assert d_world_l == d_world_v


def test_staged_evidence_narrows_both_directions():
    scenario, base = _amb001()
    ph = PossibleHistories(scenario, base)
    legal = ph.refine(HObservation(
        "o-ts", "effect_timing", ("BEFORE_REVOKE",),
        source="effect-receipt-ts", trusted=True))
    assert legal.verdict() == SAFETY_ESTABLISHED_IN_SCOPE

    ph2 = PossibleHistories(scenario, base)
    bad = ph2.refine(HObservation(
        "o-f", "effect_outcome", (COMMITTED,),
        source="fence-audit", trusted=True)).refine(HObservation(
            "o-ft", "effect_timing", ("AFTER_REVOKE",),
            source="fence-audit", trusted=True))
    assert bad.verdict() == VIOLATION_ESTABLISHED

    # Evidence removed -> ambiguity returns. Nothing was invented.
    assert bad.recompute(base).verdict() == AMBIGUOUS_BOTH_POSSIBLE


def test_histories_agree_with_hypotheses():
    """The D31 hypotheses and the D42 possible histories describe the same
    uncertainty: the discriminating facts name the tests the hypotheses
    are waiting for."""
    scenario, base = _amb001()
    ph = PossibleHistories(scenario, base)
    v = IncidentAnalyzer().verdict(build_ambiguous_incident())
    assert ph.verdict() == AMBIGUOUS_BOTH_POSSIBLE
    assert len(v.unresolved_hypotheses) == 2
    missing = set(ph.discriminating_facts())
    # The missing evidence (effect timing) is exactly what the
    # hypotheses' next discriminating tests would produce.
    assert "effect_timing" in missing
    assert "t-fetch-effect-receipt-ts" in v.discriminating_tests


# ---------------------------------------------------------------------------
# (4) nothing unresolved ever promotes to verified
# ---------------------------------------------------------------------------

def test_unresolved_hypothesis_promotion_raises_hard_error():
    incident = build_ambiguous_incident()
    for h in incident.hypotheses:
        with pytest.raises(PermissionError):
            h.promote_to_verified_lesson()


def test_unresolved_proof_withholds_consequential_use():
    scenario, base = _amb001()
    ph = PossibleHistories(scenario, base)
    policy = SafetyPolicy(ph.verdict())
    assert policy.may_certify_safety() is False
    assert policy.may_promote_to_learn() is False
    assert policy.may_blind_retry() is False
    # ...while inspection and reconciliation stay permitted.
    assert policy.may_inspect() is True
    assert policy.may_reconcile() is True
