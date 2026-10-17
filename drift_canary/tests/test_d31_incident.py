"""D31 — Causal Uncertainty Without False Blame: decisive fixture tests.

Every test here runs against drift_canary/d31_incident.py. Positive and
negative controls; no warm knowledge; the verifier never emits a single
failure_reason — tests assert that field does not exist.
"""
import sys

sys.path.insert(0, "/home/hatch/workspace/d31-build")

from drift_canary.d30_causal_trace import (
    LogicalClock,
    make_event,
    tamper,
)
from drift_canary.d31_incident import (
    OBSERVABILITY,
    Blocker,
    BlockerGraph,
    ClaimProposition,
    EvidenceState,
    Hypothesis,
    Incident,
    IncidentAnalyzer,
    ObservationScope,
    DiscriminatingTestResult,
    cold_successor_reproduces,
    recompute,
)

PASSED, FAILED = 0, 0


def check(name, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS {name}")
    else:
        FAILED += 1
        print(f"  FAIL {name} {detail}")


def _evt(eid, producer, observer, clock, condition=""):
    return make_event(event_id=eid, producer=producer, observer=observer,
                      trace_id="d31t", clock=clock, condition=condition,
                      state_before="before", state_after="after")


# ---------------------------------------------------------------------------
# Fixture: the sharpest case. Two independently established blockers
# (LAW authorization expired AND worker unavailable), one unobservable
# interval, two competing hypotheses.
# ---------------------------------------------------------------------------


def build_sharpest_case():
    clock = LogicalClock()
    ev = EvidenceState()

    auth_ev = _evt("ev-auth-expired", "law-engine", "auth-monitor",
                   clock, condition="AUTH_EXPIRED")
    heartbeat_ev = _evt("ev-no-heartbeat", "worker-pool", "pool-monitor",
                        clock, condition="WORKER_UNAVAILABLE")
    dispatch_ev = _evt("ev-dispatch-issued", "scheduler", "dispatch-log",
                       clock, condition="DISPATCH_ISSUED")
    repair_ev = _evt("ev-worker-repaired", "worker-pool", "pool-monitor",
                     clock, condition="WORKER_REPAIRED")
    for e in (auth_ev, heartbeat_ev, dispatch_ev, repair_ev):
        ev.add_event(e)

    # Conflicting claims decomposed into precise propositions.
    ev.add_proposition(ClaimProposition(
        proposition_id="lease-reached-worker",
        statement="the dispatch lease reached the worker process",
        supporting_evidence=("ev-dispatch-issued",),
        refuting_evidence=("ev-no-heartbeat",),
        origin_of={"ev-dispatch-issued": "scheduler-bus",
                   "ev-no-heartbeat": "pool-monitor"}))

    # Two independently established blockers: EACH one alone blocks the
    # workflow (OR across singleton sets). Repairing one leaves the
    # other — the workflow stays blocked. This is the sharpest case.
    graph = BlockerGraph(blocking_sets=(
        frozenset({"law-auth-expired"}),
        frozenset({"worker-unavailable"})))
    graph.add_blocker(Blocker(
        blocker_id="law-auth-expired",
        description="LAW authorization for the action expired",
        condition="AUTH_EXPIRED",
        established_by=("ev-auth-expired",)))
    graph.add_blocker(Blocker(
        blocker_id="worker-unavailable",
        description="no worker process available to take the lease",
        condition="WORKER_UNAVAILABLE",
        established_by=("ev-no-heartbeat",)))

    scopes = (
        ObservationScope(
            scope_id="auth-ledger-interval",
            source="auth-monitor", event_type="authorization",
            resource_id="action-lease-1",
            interval=(auth_ev.lamport, auth_ev.lamport),
            observability="COVERED_COMPLETE"),
        ObservationScope(
            scope_id="scheduler-window-gap",
            source="scheduler", event_type="dispatch",
            resource_id="action-lease-1",
            interval=(dispatch_ev.lamport, dispatch_ev.lamport + 5),
            observability="UNOBSERVED"),
    )

    hypotheses = (
        Hypothesis(
            hypothesis_id="h-auth-cause",
            mechanism="expired LAW authorization prevented dispatch "
                      "acceptance",
            contribution_type="prevents_progress",
            relates_to=("law-auth-expired",),
            competing_with=("h-worker-cause",),
            next_discriminating_test="t-renew-auth-retry"),
        Hypothesis(
            hypothesis_id="h-worker-cause",
            mechanism="no live worker existed to receive the lease",
            contribution_type="prevents_progress",
            relates_to=("worker-unavailable",),
            competing_with=("h-auth-cause",),
            next_discriminating_test="t-inject-probe-worker"),
    )

    incident = Incident(
        incident_id="sharpest-case",
        scopes=scopes,
        evidence=ev,
        blockers=graph,
        hypotheses=hypotheses)
    return incident, repair_ev


# ---------------------------------------------------------------------------
# Sharpest-case tests
# ---------------------------------------------------------------------------


def test_sharpest_case_initial():
    incident, _ = build_sharpest_case()
    v = IncidentAnalyzer().verdict(incident)
    check("sharpest: two blockers established",
          v.blockers_established == ("law-auth-expired",
                                     "worker-unavailable"),
          v.blockers_established)
    check("sharpest: blocked", v.is_blocked is True)
    check("sharpest: two minimal blocking sets (singletons)",
          v.minimal_blocking_sets == (("law-auth-expired",),
                                      ("worker-unavailable",)),
          v.minimal_blocking_sets)
    check("sharpest: one interval unobservable",
          v.unobservable_scopes == ("scheduler-window-gap",),
          v.unobservable_scopes)
    check("sharpest: two explanations unresolved",
          v.unresolved_hypotheses == ("h-auth-cause", "h-worker-cause"),
          v.unresolved_hypotheses)
    check("sharpest: no failure_reason field exists",
          not hasattr(v, "failure_reason"))
    check("sharpest: completion refused",
          v.completion_declared is False)
    rendered = v.render()
    check("sharpest: trustworthy verdict rendered",
          "2 blockers established" in rendered
          and "1 interval unobservable" in rendered
          and "2 explanations unresolved" in rendered,
          rendered)


def test_sharpest_case_repair_recognized_without_completion():
    incident, repair_ev = build_sharpest_case()
    recognized, still_blocked, note = incident.blockers.apply_intervention(
        "worker-unavailable", repair_ev)
    check("repair: valid repair recognized", recognized is True, note)
    check("repair: workflow still blocked", still_blocked is True)
    v = IncidentAnalyzer().verdict(incident)
    check("repair: verdict still blocked", v.is_blocked is True)
    check("repair: repair listed", v.blockers_repaired ==
          ("worker-unavailable",), v.blockers_repaired)
    check("repair: completion still refused",
          v.completion_declared is False)
    check("repair: no sole cause assigned",
          v.render().count("sole cause") == 1
          and "not enough to assign a sole cause" in v.render(),
          v.render())
    check("repair: unresolved hypotheses preserved",
          set(v.unresolved_hypotheses) == {"h-auth-cause",
                                           "h-worker-cause"},
          v.unresolved_hypotheses)
    check("repair: trustworthy sentence",
          "1 repair(s) recognized" in v.render()
          and "not enough to assign a sole cause or declare completion"
          in v.render(),
          v.render())


# ---------------------------------------------------------------------------
# Negative controls
# ---------------------------------------------------------------------------


def test_unresolved_hypothesis_never_promotes():
    h = Hypothesis(hypothesis_id="h-x", mechanism="m",
                   contribution_type="correlated_only")
    raised = False
    try:
        h.promote_to_verified_lesson()
    except PermissionError:
        raised = True
    check("negative: unresolved hypothesis cannot promote", raised)
    hs = Hypothesis(hypothesis_id="h-y", mechanism="m",
                    contribution_type="prevents_progress",
                    status="supported")
    raised = False
    try:
        hs.promote_to_verified_lesson()
    except PermissionError:
        raised = True
    check("negative: even supported hypothesis has no local promote",
          raised)


def test_blocker_without_evidence_rejected():
    graph = BlockerGraph()
    raised = False
    try:
        graph.add_blocker(Blocker(blocker_id="ghost",
                                  description="no evidence",
                                  condition="X"))
    except ValueError:
        raised = True
    check("negative: evidence-less blocker refused", raised)


def test_repair_without_witness_refused():
    incident, _ = build_sharpest_case()
    clock = LogicalClock()
    real = _evt("ev-real-repair", "worker-pool", "pool-monitor", clock)
    # Corrupt the witness the way a compromised producer's log would:
    # alter a sealed body field so authentication fails on hash
    # mismatch. D30's own invariant already makes a self-certified
    # event unconstructible; here the repair is refused because the
    # witness no longer authenticates.
    fake = tamper(real, condition="WORKER_REPAIRED_FORGED")
    recognized, _, note = incident.blockers.apply_intervention(
        "worker-unavailable", fake)
    check("negative: tampered/self-certified repair refused",
          recognized is False, note)
    check("negative: blocker still active",
          "worker-unavailable" in incident.blockers.established_blockers())


def test_tampered_evidence_degrades_claim():
    clock = LogicalClock()
    ev = EvidenceState()
    good = _evt("ev-good", "p", "o", clock)
    ev.add_event(good)
    ev.add_proposition(ClaimProposition(
        proposition_id="c1", statement="s",
        supporting_evidence=("ev-good", "ev-tampered"),
        origin_of={"ev-good": "bus-a", "ev-tampered": "bus-b"}))
    ev.add_event(tamper(good, condition="CHANGED"))
    # overwrite the good copy with the tampered one under the same id
    ev._event_pool["ev-tampered"] = tamper(good, condition="CHANGED")
    v, why = ev.verdict_of("c1")
    check("negative: tampered evidence -> UNDETERMINED",
          v == "UNDETERMINED", f"{v} ({why})")


def test_false_independence_collapses():
    clock = LogicalClock()
    ev = EvidenceState()
    e1 = _evt("ev-log-1", "event-bus", "log-collector", clock)
    e2 = _evt("ev-log-2", "event-bus", "log-collector", clock)
    for e in (e1, e2):
        ev.add_event(e)
    # Two logs, ONE event bus: not two witnesses.
    ev.add_proposition(ClaimProposition(
        proposition_id="c-bus", statement="dispatch issued",
        supporting_evidence=("ev-log-1", "ev-log-2"),
        origin_of={"ev-log-1": "event-bus", "ev-log-2": "event-bus"}))
    prop = ev.propositions["c-bus"]
    check("negative: one bus = one genuine path",
          prop.independent_witness_count() == 1,
          prop.independent_witness_count())
    check("negative: false-corroboration pair detected",
          len(prop.false_corroboration_pairs()) == 1,
          prop.false_corroboration_pairs())
    v, why = ev.verdict_of("c-bus")
    check("negative: single genuine witness -> UNDETERMINED",
          v == "UNDETERMINED", f"{v} ({why})")


def test_genuine_two_witnesses_supported():
    clock = LogicalClock()
    ev = EvidenceState()
    e1 = _evt("ev-a", "scheduler", "sched-auditor", clock)
    e2 = _evt("ev-b", "worker-pool", "pool-auditor", clock)
    for e in (e1, e2):
        ev.add_event(e)
    ev.add_proposition(ClaimProposition(
        proposition_id="c-2w", statement="dispatch issued",
        supporting_evidence=("ev-a", "ev-b"),
        origin_of={"ev-a": "scheduler-path",
                   "ev-b": "worker-path"}))
    v, why = ev.verdict_of("c-2w")
    check("positive: two independent witnesses -> SUPPORTED",
          v == "SUPPORTED", f"{v} ({why})")


def test_conflicting_genuine_paths():
    clock = LogicalClock()
    ev = EvidenceState()
    e1 = _evt("ev-s", "scheduler", "sched-auditor", clock)
    e2 = _evt("ev-r", "worker-pool", "pool-auditor", clock)
    for e in (e1, e2):
        ev.add_event(e)
    ev.add_proposition(ClaimProposition(
        proposition_id="c-conf", statement="lease reached worker",
        supporting_evidence=("ev-s",),
        refuting_evidence=("ev-r",),
        origin_of={"ev-s": "scheduler-path",
                   "ev-r": "worker-path"}))
    v, why = ev.verdict_of("c-conf")
    check("negative: genuine conflict -> CONFLICTED not averaged",
          v == "CONFLICTED", f"{v} ({why})")


def test_swapped_labels_do_not_move_verdict():
    incident, _ = build_sharpest_case()
    before = IncidentAnalyzer().verdict(incident)
    # Swap the narrative labels; evidence unchanged.
    b1 = incident.blockers.blockers["law-auth-expired"]
    b2 = incident.blockers.blockers["worker-unavailable"]
    b1.description, b2.description = b2.description, b1.description
    after = recompute(incident)
    check("negative: swapped labels -> identical verdict",
          (after.blockers_established == before.blockers_established
           and after.is_blocked == before.is_blocked
           and after.unresolved_hypotheses
           == before.unresolved_hypotheses))


def test_absence_semantics():
    complete = ObservationScope(
        scope_id="s1", source="a", event_type="e", resource_id="r",
        interval=(0, 10), observability="COVERED_COMPLETE")
    unobs = ObservationScope(
        scope_id="s2", source="a", event_type="e", resource_id="r",
        interval=(0, 10), observability="UNOBSERVED")
    check("absence: meaningful inside COVERED_COMPLETE",
          complete.absence_is_evidence() is True)
    check("absence: NOT evidence inside UNOBSERVED",
          unobs.absence_is_evidence() is False)
    partial = ObservationScope(
        scope_id="s3", source="a", event_type="e", resource_id="r",
        interval=(0, 10), observability="COVERED_PARTIAL")
    check("absence: NOT full evidence inside COVERED_PARTIAL",
          partial.absence_is_evidence() is False)


# ---------------------------------------------------------------------------
# Positive controls
# ---------------------------------------------------------------------------


def test_valid_completion_declared():
    clock = LogicalClock()
    ev = EvidenceState()
    done_ev = _evt("ev-done", "worker-pool", "pool-monitor", clock,
                   condition="WORKFLOW_COMPLETED")
    ev.add_event(done_ev)
    graph = BlockerGraph(
        blocking_sets=(frozenset({"only-blocker"}),))
    graph.add_blocker(Blocker(
        blocker_id="only-blocker", description="d", condition="C",
        established_by=("ev-done",)))
    fix = _evt("ev-fix", "worker-pool", "pool-monitor", clock,
               condition="REPAIRED")
    recognized, still_blocked, _ = graph.apply_intervention(
        "only-blocker", fix)
    check("completion: single blocker repaired", recognized is True)
    check("completion: not blocked afterwards",
          still_blocked is False)
    incident = Incident(incident_id="done-case", evidence=ev,
                        blockers=graph,
                        completion_evidence=("ev-done",))
    v = IncidentAnalyzer().verdict(incident)
    check("completion: declared on full evidence",
          v.completion_declared is True, v.reasons)


def test_minimal_blocking_sets():
    graph = BlockerGraph(blocking_sets=(
        frozenset({"a", "b"}),
        frozenset({"a", "b", "c"}),   # redundant superset
        frozenset({"d"}),))
    clock = LogicalClock()
    ev = _evt("ev-x", "p", "o", clock)
    for bid in ("a", "b", "c", "d"):
        graph.add_blocker(Blocker(blocker_id=bid, description=bid,
                                  condition="C",
                                  established_by=("ev-x",)))
    mbs = graph.minimal_blocking_sets()
    check("blockers: redundant superset dropped",
          set(mbs) == {frozenset({"d"}), frozenset({"a", "b"})}, mbs)


def test_cold_successor_reproduces():
    incident, repair_ev = build_sharpest_case()
    incident.blockers.apply_intervention("worker-unavailable",
                                         repair_ev)
    incident.interventions = (
        DiscriminatingTestResult(test_id="t-probe", distinguished=(),
                   uncertainty_reduced=1),)
    ok, detail = cold_successor_reproduces(incident)
    check("cold successor: reproduces verdict from bytes", ok, detail)


def test_conclusions_recomputed_not_stale():
    incident, _ = build_sharpest_case()
    v1 = IncidentAnalyzer().verdict(incident)
    # New evidence arrives: the auth ledger was actually fine.
    clock = LogicalClock()
    clear = _evt("ev-auth-ok", "law-engine", "auth-monitor", clock,
                 condition="AUTH_VALID")
    incident.evidence.add_event(clear)
    incident.evidence.add_proposition(ClaimProposition(
        proposition_id="auth-valid", statement="auth was valid",
        supporting_evidence=("ev-auth-expired", "ev-auth-ok"),
        origin_of={"ev-auth-expired": "auth-monitor",
                   "ev-auth-ok": "law-engine"}))
    v2 = recompute(incident)
    verdicts2 = dict(v2.claim_verdicts)
    check("recompute: new claim appears after evidence change",
          "auth-valid" in verdicts2, verdicts2)
    check("recompute: original verdict unchanged object",
          v1 is not v2)


def test_discriminating_tests_listed():
    incident, _ = build_sharpest_case()
    v = IncidentAnalyzer().verdict(incident)
    check("tests: discriminating tests named",
          set(v.discriminating_tests) == {"t-renew-auth-retry",
                                          "t-inject-probe-worker"},
          v.discriminating_tests)


def test_uncertainty_credit_without_repair():
    incident, _ = build_sharpest_case()
    incident.interventions = (
        DiscriminatingTestResult(test_id="t-probe-no-fix", distinguished=("h-x",),
                   uncertainty_reduced=2),)
    v = IncidentAnalyzer().verdict(incident)
    check("tests: uncertainty reduction credited without repair",
          v.uncertainty_reduced == 2)
    check("tests: still blocked after non-repairing test",
          v.is_blocked is True)


def test_or_blockers():
    # Either blocker alone blocks: repair one, still blocked.
    graph = BlockerGraph(blocking_sets=(
        frozenset({"x"}), frozenset({"y"})))
    clock = LogicalClock()
    ev = _evt("ev-x", "p", "o", clock)
    for bid in ("x", "y"):
        graph.add_blocker(Blocker(blocker_id=bid, description=bid,
                                  condition="C",
                                  established_by=("ev-x",)))
    fix = _evt("ev-fix", "p", "o", clock)
    recognized, still_blocked, _ = graph.apply_intervention("x", fix)
    check("or-blockers: repair recognized", recognized is True)
    check("or-blockers: still blocked via other set",
          still_blocked is True)
    mbs = graph.minimal_blocking_sets()
    check("or-blockers: one minimal set remains",
          set(mbs) == {frozenset({"y"})}, mbs)


if __name__ == "__main__":
    print("D31 decisive fixture tests")
    for name, fn in sorted(
            [(k, v) for k, v in globals().items()
             if k.startswith("test_")]):
        print(f"- {name}")
        fn()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
