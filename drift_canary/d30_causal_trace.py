"""D30 — Verifiable Causal Trace Across Environment, Scheduler and Worker.

Implements the decisive D30 experiment: compose environment, scheduler,
and worker evidence into ONE independently verifiable causal trace —
without treating logs or labels as proof.

Core rule (D30): logs describe what components claim happened. Evidence
establishes what happened. Causal verification establishes why the
outcome occurred. A CORRELATES_WITH edge must never be silently promoted
to CAUSED_BY; HAPPENS_BEFORE establishes ordering, not causation.

Three layers kept strictly distinct:
  Observation        — independently witnessed events (producer AND
                       observer are separate identities).
  Causal relationship — verified enabling/prevention links, emitted only
                       after mechanism + counterfactual + independent
                       reproduction checks pass.
  Responsibility     — the controller of the failing condition (D29's
                       responsibility record, reused — never re-derived).

Composes (extends, never duplicates):
  d29_boundary.py — ResponsibilityRecord, classify_boundary,
                    run_case, verify_against_ledger (the responsibility
                    and evidence layer D30 builds on).
  fairness.py     — SchedulingEvent, event_adequate_service, ladder_rank.
  progress.py     — obligation state vocabulary.

The D30 layer added here: the canonical evidence event (identity,
producer+observer, trace/parent IDs, resource/lease IDs, state
before/after, logical clocks, artifact hashes, attestation), the
four-level observation ladder (L0 REPORTED / L1 AUTHENTICATED /
L2 INDEPENDENTLY_CORROBORATED / L3 CAUSALLY_QUALIFIED), the causal
verifier with the three pre-cause checks, and the trace adapter that
projects D29's evidence into canonical form. None of those exist in the
three contracts — that is the gap this fixture fills, as specified.

SPEC + deterministic fixture machinery. NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field

from drift_canary.d29_boundary import (
    OBLIGATION_ID,
    RESOURCE_ID,
    WORKFLOW_ID,
    BoundaryCaseResult,
    ResponsibilityRecord,
    classify_boundary,
)
from drift_canary.fairness import (
    SchedulingEvent,
    event_adequate_service,
)

# ---------------------------------------------------------------------------
# Vocabularies. The verifier may ONLY emit these verdicts; it may never
# emit a component's narrative label as a verdict.
# ---------------------------------------------------------------------------
VERDICTS = (
    "ENVIRONMENT_BLOCKER",       # external resource genuinely unavailable
    "SCHEDULER_STARVATION",       # eligible work never dispatched
    "SCHEDULER_SERVICE_FAILURE",  # dispatched but no usable service provided
    "WORKER_NONPROGRESS",         # adequate service, no verified advancement
    "BOUNDARY_UNDETERMINED",      # evidence intact but cause not established
    "INSUFFICIENT_OBSERVABILITY",  # missing/compromised evidence — never blame
    "COMPLETED",                  # the workflow actually completed
)

OBSERVATION_STATUSES = (
    "reported",        # L0: present, producer != observer asserted
    "authenticated",   # L1: artifact hash + observer attestation verify
    "corroborated",    # L2: independently corroborated (see below)
    "verified",        # L3: on a causally qualified path (see below)
)

CAUSAL_STATUSES = (
    "unassessed",
    "hypothesized",
    "supported",
    "experimentally_verified",
)

EDGE_KINDS = (
    "HAPPENS_BEFORE",   # ordering from logical clocks — never causation
    "CORRELATES_WITH",  # co-occurrence — must never be promoted silently
    "CAUSED_BY",        # only after the three checks pass
)

# Four-level observation ladder.
L0_REPORTED = 0
L1_AUTHENTICATED = 1
L2_CORROBORATED = 2
L3_CAUSALLY_QUALIFIED = 3

# Canonical producers and the independent observers that witness them.
# The observer is NEVER the producer: a component cannot certify itself.
ENV_WITNESS = "ENV_WITNESS"
TRACE_MONITOR = "TRACE_MONITOR"
SCHEDULER_PRODUCER = "SCHEDULER"
WORKER_PRODUCER = "WORKER"
WORKER_ACK_MONITOR = "WORKER_ACK_MONITOR"

# Observed conditions. These are evidence — measured states — not the
# narrative labels components assign to each other.
CONDITIONS = (
    "RESOURCE_UNAVAILABLE",
    "RESOURCE_AVAILABLE",
    "SERVICE_INADEQUATE",
    "SERVICE_ADEQUATE",
    "NO_ADVANCEMENT",
    "WORKFLOW_UNFINISHED",
)

# Mechanism registry: (enabling condition, outcome) -> mechanism note.
# A CAUSED_BY edge requires a mechanism entry; without one the claim is
# at most CORRELATES_WITH.
MECHANISMS = {
    ("RESOURCE_UNAVAILABLE", "WORKFLOW_UNFINISHED"):
        "enabling: no usable execution opportunity can be evidenced while "
        "the required resource is unavailable; scheduler debt accrued in "
        "that window is explained, not blame",
    ("SERVICE_INADEQUATE", "WORKFLOW_UNFINISHED"):
        "enabling: eligible work that is never adequately serviced cannot "
        "advance; dispatch-without-service is not service (fairness.py)",
    ("SERVICE_ADEQUATE", "WORKFLOW_UNFINISHED"):
        "enabling: adequate service delivered with no verified advancement "
        "localizes the failure to the worker's progress-on-service "
        "(progress.py)",
}


# ---------------------------------------------------------------------------
# Logical clocks. Wall-clock is never trusted alone: ordering comes from
# Lamport stamps with a per-actor vector for causal comparison.
# ---------------------------------------------------------------------------
class LogicalClock:
    """Per-trace logical clock: Lamport counter plus per-actor vector."""

    def __init__(self) -> None:
        self.lamport = 0
        self.vector: dict = {}

    def stamp(self, actor: str) -> tuple:
        self.lamport += 1
        self.vector[actor] = self.vector.get(actor, 0) + 1
        return self.lamport, tuple(sorted(self.vector.items()))

    def receive(self, actor: str, other_lamport: int,
                other_vector: tuple) -> tuple:
        self.lamport = max(self.lamport, other_lamport) + 1
        merged = dict(self.vector)
        for a, c in other_vector:
            merged[a] = max(merged.get(a, 0), c)
        merged[actor] = merged.get(actor, 0) + 1
        self.vector = merged
        return self.lamport, tuple(sorted(self.vector.items()))


# ---------------------------------------------------------------------------
# Canonical evidence event.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class EvidenceEvent:
    """One canonical evidence event.

    identity: event_id. producer AND observer are separate identities —
    a component cannot witness itself. trace_id/parent_ids link the
    causal chain. resource_id/lease_id scope the failing condition.
    state_before/state_after record the observed transition. lamport/
    vector are logical clocks (wall-clock never trusted alone).
    artifact_hash binds the event body; attestation binds the observer.
    observation_status / causal_status walk the ladders above.
    """
    event_id: str
    producer: str
    observer: str
    trace_id: str
    parent_ids: tuple = ()
    resource_id: str = ""
    lease_id: str = ""
    condition: str = ""
    state_before: str = ""
    state_after: str = ""
    lamport: int = 0
    vector: tuple = ()
    artifact_hash: str = ""
    attestation: str = ""
    observation_status: str = "reported"
    causal_status: str = "unassessed"

    def __post_init__(self):
        assert self.producer != self.observer, (
            f"producer and observer must be separate identities, got "
            f"{self.producer}")
        assert self.observation_status in OBSERVATION_STATUSES, \
            self.observation_status
        assert self.causal_status in CAUSAL_STATUSES, self.causal_status


def _canonical_body(event: EvidenceEvent) -> str:
    """Canonical serialization of the event body — everything the hash
    and attestation bind. Excludes the hash, the attestation, and the
    ladder statuses themselves (they are assessments, not evidence)."""
    return json.dumps({
        "event_id": event.event_id,
        "producer": event.producer,
        "observer": event.observer,
        "trace_id": event.trace_id,
        "parent_ids": list(event.parent_ids),
        "resource_id": event.resource_id,
        "lease_id": event.lease_id,
        "condition": event.condition,
        "state_before": event.state_before,
        "state_after": event.state_after,
        "lamport": event.lamport,
        "vector": [list(p) for p in event.vector],
    }, sort_keys=True, separators=(",", ":"))


def event_body_hash(event: EvidenceEvent) -> str:
    return hashlib.sha256(_canonical_body(event).encode("utf-8")).hexdigest()


def observer_attestation(body_hash: str, observer: str) -> str:
    """The observer's attestation token: binds observer identity to the
    exact bytes it witnessed. Forging a state change without the
    observer's cooperation breaks this token."""
    return hashlib.sha256(
        f"{body_hash}|{observer}".encode("utf-8")).hexdigest()


def make_event(event_id: str, producer: str, observer: str, trace_id: str,
               clock: LogicalClock, parent_ids: tuple = (),
               resource_id: str = "", lease_id: str = "",
               condition: str = "", state_before: str = "",
               state_after: str = "") -> EvidenceEvent:
    """Construct a fully attested evidence event: stamp the logical
    clock, hash the body, bind the observer's attestation."""
    lamport, vector = clock.stamp(producer)
    bare = EvidenceEvent(
        event_id=event_id, producer=producer, observer=observer,
        trace_id=trace_id, parent_ids=tuple(parent_ids),
        resource_id=resource_id, lease_id=lease_id, condition=condition,
        state_before=state_before, state_after=state_after,
        lamport=lamport, vector=vector,
        observation_status="reported", causal_status="unassessed")
    body_hash = event_body_hash(bare)
    return dataclasses.replace(
        bare, artifact_hash=body_hash,
        attestation=observer_attestation(body_hash, observer))


def tamper(event: EvidenceEvent, **changes) -> EvidenceEvent:
    """Corrupt an event the way a compromised producer's log would: change
    a field WITHOUT recomputing the hash/attestation. Authentication
    must fail on the result."""
    if "artifact_hash" in changes or "attestation" in changes:
        raise AssertionError(
            "tamper() must not recompute the seal: pass only body fields")
    return dataclasses.replace(event, **changes)


def authenticate(event: EvidenceEvent) -> tuple:
    """L0 -> L1 gate. Returns (ok, reason). Fails when the body was
    altered after attestation, when the attestation does not bind the
    observer, or when producer == observer (self-certification)."""
    if event.producer == event.observer:
        return False, "self-certification: producer == observer"
    expected_hash = event_body_hash(event)
    if expected_hash != event.artifact_hash:
        return False, "artifact hash mismatch: body altered after sealing"
    expected_att = observer_attestation(event.artifact_hash, event.observer)
    if expected_att != event.attestation:
        return False, "attestation does not bind the observer"
    return True, "authenticated"


# ---------------------------------------------------------------------------
# Causal edges and the trace.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CausalEdge:
    """One edge in the causal trace. HAPPENS_BEFORE is derived from
    logical clocks; CORRELATES_WITH from co-occurrence; CAUSED_BY only
    after the three checks pass — its checks record names them."""
    kind: str
    source_id: str
    target_id: str
    basis: tuple = ()
    checks: frozenset = frozenset()

    def __post_init__(self):
        assert self.kind in EDGE_KINDS, self.kind
        if self.kind == "CAUSED_BY":
            assert {"mechanism", "counterfactual",
                    "independent_reproduction"} <= set(self.checks), (
                "CAUSED_BY requires all three checks recorded; "
                f"got {sorted(self.checks)}")


@dataclass
class CausalTrace:
    """The composed trace: canonical events plus edges. Emitted edges
    are append-only; promotion of CORRELATES_WITH to CAUSED_BY is only
    possible through verify(), which records the checks."""
    trace_id: str
    events: tuple = ()
    edges: tuple = ()

    def by_id(self, event_id: str) -> EvidenceEvent:
        for e in self.events:
            if e.event_id == event_id:
                return e
        raise KeyError(event_id)

    def edges_of_kind(self, kind: str) -> tuple:
        return tuple(e for e in self.edges if e.kind == kind)


def happens_before(a: EvidenceEvent, b: EvidenceEvent) -> bool:
    """Ordering from logical clocks only. Never causation."""
    if a.lamport >= b.lamport:
        return False
    va, vb = dict(a.vector), dict(b.vector)
    return all(vb.get(k, 0) >= v for k, v in va.items())


def build_ordering_edges(trace: CausalTrace) -> tuple:
    """Derive HAPPENS_BEFORE edges from logical clocks. These carry no
    causal claim — they are the substrate the causal checks reason over."""
    edges = []
    for a in trace.events:
        for b in trace.events:
            if a.event_id != b.event_id and happens_before(a, b):
                edges.append(CausalEdge(
                    kind="HAPPENS_BEFORE", source_id=a.event_id,
                    target_id=b.event_id,
                    basis=("logical-clock ordering",)))
    return tuple(edges)


def build_correlation_edges(trace: CausalTrace) -> tuple:
    """CORRELATES_WITH edges for co-occurring conditions in the same
    window. Emitted explicitly so the verifier — and any reader — can
    see they were considered and NOT promoted."""
    edges = []
    conds = {}
    for e in trace.events:
        conds.setdefault(e.condition, []).append(e.event_id)
    pairs = [("RESOURCE_UNAVAILABLE", "SERVICE_INADEQUATE"),
             ("SERVICE_INADEQUATE", "NO_ADVANCEMENT"),
             ("RESOURCE_UNAVAILABLE", "NO_ADVANCEMENT")]
    for c1, c2 in pairs:
        for i1 in conds.get(c1, []):
            for i2 in conds.get(c2, []):
                edges.append(CausalEdge(
                    kind="CORRELATES_WITH", source_id=i1, target_id=i2,
                    basis=("temporal co-occurrence in the same trace "
                           "window",)))
    return tuple(edges)


# ---------------------------------------------------------------------------
# Observation ladder: L0 REPORTED / L1 AUTHENTICATED /
# L2 INDEPENDENTLY_CORROBORATED / L3 CAUSALLY_QUALIFIED.
# ---------------------------------------------------------------------------
_CONDITION_CONSISTENT = {
    # conditions that mutually corroborate when observed in the same
    # window by different producers
    "RESOURCE_UNAVAILABLE": {"RESOURCE_UNAVAILABLE", "SERVICE_INADEQUATE"},
    "RESOURCE_AVAILABLE": {"RESOURCE_AVAILABLE", "SERVICE_ADEQUATE",
                           "SERVICE_INADEQUATE"},
    "SERVICE_INADEQUATE": {"RESOURCE_UNAVAILABLE", "RESOURCE_AVAILABLE",
                           "SERVICE_INADEQUATE"},
    "SERVICE_ADEQUATE": {"RESOURCE_AVAILABLE", "SERVICE_ADEQUATE",
                         "NO_ADVANCEMENT"},
    "NO_ADVANCEMENT": {"SERVICE_ADEQUATE", "SERVICE_INADEQUATE",
                       "NO_ADVANCEMENT", "WORKFLOW_UNFINISHED"},
    "WORKFLOW_UNFINISHED": {"NO_ADVANCEMENT", "WORKFLOW_UNFINISHED"},
}


def observation_level(event: EvidenceEvent, trace: CausalTrace,
                      caused_by_sources: frozenset = frozenset()) -> int:
    """Compute the event's ladder level from the trace evidence.

    L1 requires authentication. L2 requires an INDEPENDENT second
    producer observing a consistent condition in the same window —
    one producer's word never corroborates itself. L3 requires the
    event to sit on a verified CAUSED_BY path.
    """
    ok, _ = authenticate(event)
    if not ok:
        return L0_REPORTED
    level = L1_AUTHENTICATED
    for other in trace.events:
        if other.event_id == event.event_id:
            continue
        ok2, _ = authenticate(other)
        if not ok2 or other.producer == event.producer:
            continue
        if other.condition in _CONDITION_CONSISTENT.get(event.condition,
                                                        set()):
            level = L2_CORROBORATED
            break
    if event.event_id in caused_by_sources:
        level = L3_CAUSALLY_QUALIFIED
    return level


# ---------------------------------------------------------------------------
# Trace adapter: project D29's evidence layer into canonical form.
#
# Deliberate design decision: ComponentReport narrative labels are NOT
# adapted. The canonical trace carries evidence only — there is no field
# for a label to enter through, so a verifier reading only the trace
# cannot be swayed by what components claimed about each other.
# ---------------------------------------------------------------------------
def adapt_d29_result(result: BoundaryCaseResult,
                     trace_id: str = None) -> CausalTrace:
    """Adapt one D29 case result into a canonical causal trace.

    Environment observations -> ENV_WITNESS events observed by
    TRACE_MONITOR. Ledger rounds -> SCHEDULER events observed by
    TRACE_MONITOR (WORKER_ACK_MONITOR when a worker ack is present).
    The obligation's terminal state -> a WORKER outcome event.
    Parent links chain env -> scheduler -> worker within each round.
    """
    trace_id = trace_id or f"TRACE-{result.case}"
    clock = LogicalClock()
    events = []

    debt = 0
    sched_parents = {}
    for i, obs in enumerate(result.env_observations, start=1):
        condition = ("RESOURCE_UNAVAILABLE" if not obs.available
                     else "RESOURCE_AVAILABLE")
        state = f"{obs.resource_id}:{'UNAVAILABLE' if not obs.available else 'AVAILABLE'}"
        ev = make_event(
            event_id=f"{trace_id}-ENV-{i:02d}",
            producer=ENV_WITNESS, observer=TRACE_MONITOR,
            trace_id=trace_id, clock=clock,
            resource_id=obs.resource_id,
            condition=condition,
            state_before=state, state_after=state)
        events.append(ev)
        sched_parents[i] = (ev.event_id,)

    sched_events = [e for e in result.ledger.history
                    if e.obligation_id == OBLIGATION_ID and e.eligible]
    for e in sorted(sched_events, key=lambda x: x.seq):
        adequate, _ = event_adequate_service(e)
        debt_before = debt
        debt = 0 if adequate else debt + 1
        ev_dict = dict(e.evidence)
        observer = (WORKER_ACK_MONITOR if ev_dict.get("worker_ack")
                    else TRACE_MONITOR)
        events.append(make_event(
            event_id=f"{trace_id}-SCHED-{e.seq:02d}",
            producer=SCHEDULER_PRODUCER, observer=observer,
            trace_id=trace_id, clock=clock,
            parent_ids=sched_parents.get(e.seq, ()),
            resource_id=RESOURCE_ID, lease_id=ev_dict.get("lease_id", ""),
            condition="SERVICE_ADEQUATE" if adequate else "SERVICE_INADEQUATE",
            state_before=f"debt={debt_before}", state_after=f"debt={debt}"))

    events.append(make_event(
        event_id=f"{trace_id}-WORKER-OUTCOME",
        producer=WORKER_PRODUCER, observer=TRACE_MONITOR,
        trace_id=trace_id, clock=clock,
        parent_ids=tuple(ev.event_id for ev in events
                         if ev.producer == SCHEDULER_PRODUCER),
        resource_id=RESOURCE_ID,
        condition=("WORKFLOW_UNFINISHED"
                   if result.obligation.state == "OUTSTANDING"
                   else "NO_ADVANCEMENT"),
        state_before=f"obligation:{result.obligation.state}",
        state_after=f"obligation:{result.obligation.state}"))

    return CausalTrace(trace_id=trace_id, events=tuple(events), edges=())


# ---------------------------------------------------------------------------
# The independent causal verifier.
#
# Reads ONLY the canonical trace. It has no parameter for narrative
# labels and no access to the original D29 result objects: verdicts are
# recomputed from authenticated evidence, and cause is assigned only
# after the three checks (mechanism / counterfactual /
# independent reproduction) pass. Missing or compromised evidence
# yields INSUFFICIENT_OBSERVABILITY — never invented blame.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CausalVerdict:
    """Everything the independent verifier used and produced."""
    verdict: str
    controller: str
    level: int                        # max ladder level on the causal path
    edges: tuple                      # ordering + correlation + causal edges
    explanations_preserved: tuple     # competing explanations still live
    reasons: tuple                    # human-readable audit trail
    trace_id: str = ""


_HYPOTHESES = (
    "ENVIRONMENT_BLOCKER",
    "SCHEDULER_STARVATION",
    "SCHEDULER_SERVICE_FAILURE",
    "WORKER_NONPROGRESS",
)


class CausalVerifier:
    """Independent causal verifier. Construct it fresh — even in a fresh
    process — hand it a canonical trace, and it reproduces the verdict
    from evidence alone."""

    def _authenticated(self, trace: CausalTrace) -> tuple:
        good, bad = [], []
        for e in trace.events:
            ok, reason = authenticate(e)
            (good if ok else bad).append((e, reason))
        return tuple(good), tuple(bad)

    def _env_coverage(self, env_events: tuple) -> tuple:
        """Negative claims about the environment need coverage evidence:
        the witness must have observed every round in the window."""
        seqs = sorted(
            int(e.event_id.rsplit("-", 1)[1]) for e in env_events)
        if not seqs:
            return False, "no environment observations at all"
        expected = list(range(1, seqs[-1] + 1))
        if seqs != expected:
            missing = sorted(set(expected) - set(seqs))
            return False, (f"environment witness coverage gap at "
                           f"rounds {missing}: negative claims about the "
                           f"environment are inadmissible")
        return True, f"environment witness covered rounds 1..{seqs[-1]}"

    def _recompute_classification(self, trace: CausalTrace,
                                  good: tuple) -> tuple:
        """Recompute the D29-style classification from authenticated
        canonical events — never from labels (there are none to read)."""
        by_producer = {}
        for e, _ in good:
            by_producer.setdefault(e.producer, []).append(e)

        env_events = sorted(by_producer.get(ENV_WITNESS, []),
                            key=lambda e: e.lamport)
        sched_events = sorted(by_producer.get(SCHEDULER_PRODUCER, []),
                              key=lambda e: e.lamport)
        outcome = [e for e, _ in good
                   if e.producer == WORKER_PRODUCER]
        unfinished = any(e.condition == "WORKFLOW_UNFINISHED"
                         for e in outcome)

        coverage_ok, coverage_reason = self._env_coverage(env_events)

        # Scheduler debt recomputed from canonical scheduler events.
        debt, max_rung_inadequate = 0, True
        saw_adequate, saw_inadequate = False, False
        for e in sched_events:
            adequate = e.condition == "SERVICE_ADEQUATE"
            saw_adequate |= adequate
            saw_inadequate |= (not adequate)
            debt = 0 if adequate else debt + 1
        threshold = 3

        env_all_unavailable = (
            coverage_ok and env_events
            and all(e.condition == "RESOURCE_UNAVAILABLE"
                    for e in env_events))

        if env_all_unavailable:
            return ("ENVIRONMENT_BLOCKER", "ENVIRONMENT",
                    "RESOURCE_UNAVAILABLE", coverage_reason,
                    coverage_ok, debt)
        if not coverage_ok and env_events and all(
                e.condition == "RESOURCE_UNAVAILABLE" for e in env_events):
            # The evidence POINTS at the environment but coverage is
            # gapped: the negative claim ("never available") is
            # inadmissible. Uncertainty, not blame.
            return ("INSUFFICIENT_OBSERVABILITY", "UNDETERMINED",
                    None, coverage_reason, coverage_ok, debt)
        if debt >= threshold and unfinished:
            if not coverage_ok:
                # Without environment coverage the scheduler's debt
                # cannot be distinguished from an environment-explained
                # stall: competing explanations preserved, no blame.
                return ("BOUNDARY_UNDETERMINED", "UNDETERMINED", None,
                        "scheduler debt evidenced but environment "
                        "coverage missing: cannot rule out an "
                        "environment-explained stall; " + coverage_reason,
                        coverage_ok, debt)
            if saw_adequate:
                # mixed service history with terminal debt: dispatched
                # but never usable
                verdict = "SCHEDULER_SERVICE_FAILURE"
            elif saw_inadequate and not saw_adequate:
                verdict = "SCHEDULER_STARVATION"
            else:
                verdict = "SCHEDULER_SERVICE_FAILURE"
            return (verdict, "SCHEDULER", "SERVICE_INADEQUATE",
                    f"recomputed scheduler debt={debt} >= {threshold} "
                    f"with workflow unfinished", coverage_ok, debt)
        if saw_adequate and debt == 0 and unfinished:
            return ("WORKER_NONPROGRESS", "WORKER", "SERVICE_ADEQUATE",
                    "adequate service evidenced with no verified "
                    "advancement", coverage_ok, debt)
        return ("BOUNDARY_UNDETERMINED", "UNDETERMINED", None,
                "evidence insufficient to distinguish the competing "
                "explanations", coverage_ok, debt)

    def _mechanism_check(self, condition: str) -> tuple:
        key = (condition, "WORKFLOW_UNFINISHED")
        if key in MECHANISMS:
            return True, f"mechanism: {MECHANISMS[key]}"
        return False, (f"no documented mechanism links {condition} to an "
                       f"unfinished workflow: co-occurrence only")

    def _counterfactual_check(self, verdict: str, condition: str,
                              corpus: tuple) -> tuple:
        """Counterfactual: some other trace in the corpus shows the same
        symptom (unfinished workflow) with this condition ABSENT and a
        different verdict — the outcome does not follow the condition
        trivially, and the condition is not blamed where it is absent."""
        for other in corpus:
            if other.trace_id == getattr(self, "_current_trace_id", None):
                continue
            conds = {e.condition for e, _ in self._authenticated(other)[0]}
            if condition not in conds:
                ov, _, _, _, _, _ = self._recompute_classification(
                    other, self._authenticated(other)[0])
                if ov != verdict and ov in _HYPOTHESES:
                    return True, (
                        f"counterfactual: trace {other.trace_id} lacks "
                        f"{condition}, same symptom, verdict {ov}")
        return False, ("no counterfactual in corpus: no comparable trace "
                       "with the condition absent")

    def _reproduction_check(self, trace: CausalTrace, verdict: str,
                            controller: str, corpus: tuple) -> tuple:
        """Independent reproduction: serialize the trace, rebuild it in a
        FRESH verifier with no shared objects, and require the same
        verdict. The original logs/labels/agents are not consulted.
        Runs in _repro_mode so the fresh verifier does not recurse."""
        blob = serialize_trace(trace)
        fresh = CausalVerifier()
        rebuilt = deserialize_trace(blob)
        rep = fresh.verify(rebuilt, corpus=corpus, _repro_mode=True)
        if rep.verdict == verdict and rep.controller == controller:
            return True, ("independent reproduction: fresh verifier on "
                          "serialized trace reproduces the verdict")
        return False, (f"reproduction failed: fresh verifier concluded "
                       f"{rep.verdict}/{rep.controller}")

    def verify(self, trace: CausalTrace, corpus: tuple = (),
               _repro_mode: bool = False) -> CausalVerdict:
        """Verify one trace against an optional corpus of peer traces.

        Returns a CausalVerdict. Competing explanations are preserved
        (listed, not discarded) whenever the evidence does not
        distinguish them; compromised or missing evidence yields
        INSUFFICIENT_OBSERVABILITY, never invented blame.
        """
        self._current_trace_id = trace.trace_id
        reasons = []
        good, bad = self._authenticated(trace)
        if bad:
            reasons.append(
                f"{len(bad)} event(s) failed authentication and are "
                f"excluded from evidence: "
                + "; ".join(f"{e.event_id} ({r})" for e, r in bad))

        verdict, controller, condition, why, coverage_ok, debt = \
            self._recompute_classification(trace, good)
        reasons.append(f"classification from authenticated evidence: {why}")

        if bad:
            # Compromised evidence: the remaining authenticated events
            # cannot carry a causal claim. Uncertainty — never blame
            # reconstructed from a partial, tampered trace.
            reasons.append(
                "compromised evidence excluded: downgrading to "
                "INSUFFICIENT_OBSERVABILITY rather than reasoning from "
                "a tampered trace")
            verdict, controller = "INSUFFICIENT_OBSERVABILITY", "UNDETERMINED"

        edges = list(build_ordering_edges(trace))
        edges.extend(build_correlation_edges(trace))

        if verdict in ("INSUFFICIENT_OBSERVABILITY",
                       "BOUNDARY_UNDETERMINED"):
            preserved = tuple(h for h in _HYPOTHESES if h != verdict)
            return CausalVerdict(
                verdict=verdict, controller=controller, level=L1_AUTHENTICATED,
                edges=tuple(edges),
                explanations_preserved=preserved,
                reasons=tuple(reasons + [
                    "cause not assigned: competing explanations preserved "
                    "until evidence distinguishes them"]),
                trace_id=trace.trace_id)

        # The three checks before assigning cause.
        mech_ok, mech_reason = self._mechanism_check(condition)
        reasons.append(mech_reason)
        cf_ok, cf_reason = self._counterfactual_check(verdict, condition,
                                                      corpus)
        reasons.append(cf_reason)
        if _repro_mode:
            # The fresh reproduction verifier does not recurse: its own
            # verdict is the classification plus mechanism/counterfactual.
            rep_ok, rep_reason = True, "reproduction-mode: check vacuous"
        else:
            rep_ok, rep_reason = self._reproduction_check(
                trace, verdict, controller, corpus)
        reasons.append(rep_reason)

        if mech_ok and cf_ok and rep_ok:
            # Emit the CAUSED_BY edge with the checks recorded. The
            # source is the first authenticated event carrying the
            # enabling condition; the target is the outcome event.
            source = next(e for e, _ in good if e.condition == condition)
            target = next(e for e, _ in good
                          if e.condition == "WORKFLOW_UNFINISHED")
            edges.append(CausalEdge(
                kind="CAUSED_BY", source_id=source.event_id,
                target_id=target.event_id,
                basis=(mech_reason, cf_reason, rep_reason),
                checks=frozenset({"mechanism", "counterfactual",
                                  "independent_reproduction"})))
            caused = frozenset({source.event_id, target.event_id})
            level = max(
                (observation_level(e, trace, caused) for e, _ in good),
                default=L1_AUTHENTICATED)
            # Mark the path events causally qualified.
            return CausalVerdict(
                verdict=verdict, controller=controller, level=level,
                edges=tuple(edges),
                explanations_preserved=(),
                reasons=tuple(reasons + [
                    "all three causal checks passed: cause assigned"]),
                trace_id=trace.trace_id)

        preserved = tuple(h for h in _HYPOTHESES if h != verdict)
        return CausalVerdict(
            verdict="BOUNDARY_UNDETERMINED", controller="UNDETERMINED",
            level=L1_AUTHENTICATED, edges=tuple(edges),
            explanations_preserved=preserved,
            reasons=tuple(reasons + [
                "causal checks incomplete: withholding cause assignment; "
                "competing explanations preserved"]),
            trace_id=trace.trace_id)


# ---------------------------------------------------------------------------
# Serialization: the reproduction path. A fresh verifier rebuilds the
# trace from bytes alone — never from the original objects, logs, or
# labels.
# ---------------------------------------------------------------------------
def serialize_trace(trace: CausalTrace) -> bytes:
    payload = {
        "trace_id": trace.trace_id,
        "events": [
            {
                "event_id": e.event_id, "producer": e.producer,
                "observer": e.observer, "trace_id": e.trace_id,
                "parent_ids": list(e.parent_ids),
                "resource_id": e.resource_id, "lease_id": e.lease_id,
                "condition": e.condition,
                "state_before": e.state_before,
                "state_after": e.state_after,
                "lamport": e.lamport,
                "vector": [list(p) for p in e.vector],
                "artifact_hash": e.artifact_hash,
                "attestation": e.attestation,
                "observation_status": e.observation_status,
                "causal_status": e.causal_status,
            }
            for e in trace.events
        ],
    }
    return json.dumps(payload, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def deserialize_trace(blob: bytes) -> CausalTrace:
    payload = json.loads(blob.decode("utf-8"))
    events = tuple(
        EvidenceEvent(
            event_id=d["event_id"], producer=d["producer"],
            observer=d["observer"], trace_id=d["trace_id"],
            parent_ids=tuple(d["parent_ids"]),
            resource_id=d["resource_id"], lease_id=d["lease_id"],
            condition=d["condition"],
            state_before=d["state_before"],
            state_after=d["state_after"],
            lamport=d["lamport"],
            vector=tuple(tuple(p) for p in d["vector"]),
            artifact_hash=d["artifact_hash"],
            attestation=d["attestation"],
            observation_status=d["observation_status"],
            causal_status=d["causal_status"],
        )
        for d in payload["events"]
    )
    return CausalTrace(trace_id=payload["trace_id"], events=events,
                       edges=())


def fresh_verifier_reproduces(trace: CausalTrace,
                              corpus: tuple = ()) -> tuple:
    """Evidence-of-done helper: a brand-new verifier, given only the
    serialized bytes, must reproduce the original conclusion without
    trusting the original logs, labels, or agent objects."""
    original = CausalVerifier().verify(trace, corpus=corpus)
    rebuilt = CausalVerifier().verify(deserialize_trace(serialize_trace(trace)),
                                      corpus=corpus)
    ok = (rebuilt.verdict == original.verdict
          and rebuilt.controller == original.controller)
    return ok, (f"original={original.verdict}/{original.controller} "
                f"rebuilt={rebuilt.verdict}/{rebuilt.controller}")
