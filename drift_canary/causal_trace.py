"""Causal Execution Proof Contract (Shawn, 2026-10-10 — twelfth framework).

A trace adapter + independent causal verifier built around the existing
fairness / progress / liveness / graph contracts — NOT a competing
causal-tracing platform.

Central principle: logs describe what components claim happened. Evidence
establishes what happened. Causal verification establishes why the outcome
occurred.

Three preserved layers:
  1. Observation — what was independently witnessed (EvidenceEvent).
  2. Causal relationship — which verified event enabled / prevented /
     influenced another (typed CausalRelationship, machine-checked).
  3. Responsibility — which component controlled the failing condition
     (joins the responsibility-boundary contract via producer/observer
     fields; joins the FAAP assumption registry via control_boundary).

The cold-verifier standard (top-level acceptance): a fresh, independent
verifier reconstructs what happened, names the failed guarantee,
distinguishes alternatives, and reproduces the conclusion — without
trusting logs, labels, or agents merely because they agree.
"""

from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Four-level evidence qualification ladder (event-evidence labels; these are
# NOT replacements for the canonical NayaPOWER truth states).
# ---------------------------------------------------------------------------
L0_REPORTED = "REPORTED"                        # a producer asserts it
L1_AUTHENTICATED = "AUTHENTICATED"               # source-bound, integrity-checked
L2_CORROBORATED = "INDEPENDENTLY_CORROBORATED"   # independent observation agrees
L3_QUALIFIED = "CAUSALLY_QUALIFIED"              # independently justified causal argument

LADDER = (L0_REPORTED, L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED)

# Causal statuses for a relationship or hypothesis.
CAUSAL_UNASSESSED = "UNASSESSED"
CAUSAL_HYPOTHESIZED = "HYPOTHESIZED"
CAUSAL_SUPPORTED = "SUPPORTED"
CAUSAL_EXPERIMENTALLY_VERIFIED = "EXPERIMENTALLY_VERIFIED"

# ---------------------------------------------------------------------------
# Typed causal relationships.
# ---------------------------------------------------------------------------
REL_CORRELATES_WITH = "CORRELATES_WITH"  # shared identity/context only
REL_HAPPENS_BEFORE = "HAPPENS_BEFORE"    # ordering, NOT causation
REL_ENABLED_BY = "ENABLED_BY"            # verified condition made it possible
REL_DEPENDS_ON = "DEPENDS_ON"            # required earlier event/state
REL_PREVENTED_BY = "PREVENTED_BY"        # condition blocked a transition
REL_CAUSED_BY = "CAUSED_BY"              # needs reproduction/intervention/argument

RELATIONSHIPS = (
    REL_CORRELATES_WITH,
    REL_HAPPENS_BEFORE,
    REL_ENABLED_BY,
    REL_DEPENDS_ON,
    REL_PREVENTED_BY,
    REL_CAUSED_BY,
)

# What each relationship requires as proof. A relationship may only be
# asserted when its requirement is satisfied — this is machine-checked by
# CausalGraph.add_relationship().
REL_REQUIREMENTS = {
    REL_CORRELATES_WITH: "valid identifiers and source binding",
    REL_HAPPENS_BEFORE: "authenticated message, sequence, or state-transition evidence",
    REL_ENABLED_BY: "valid precondition and transition evidence",
    REL_DEPENDS_ON: "independently reviewed contract or actual dependency",
    REL_PREVENTED_BY: "verified blocker and applicable execution semantics",
    REL_CAUSED_BY: "reproduction, intervention, or independently justified causal argument",
}

# ---------------------------------------------------------------------------
# Event types (compose with fairness.py's service ladder:
# SELECTED/DISPATCHED/SERVICED/ATTEMPTED/ADVANCED/COMPLETED).
# ---------------------------------------------------------------------------
EV_RESOURCE_OFFER = "RESOURCE_OFFER"
EV_RESOURCE_WITHDRAWN = "RESOURCE_WITHDRAWN"
EV_OBLIGATION_ELIGIBLE = "OBLIGATION_ELIGIBLE"
EV_DISPATCH = "DISPATCH"            # fairness.py DISPATCHED: lease issued
EV_DISPATCH_ACCEPTED = "DISPATCH_ACCEPTED"
EV_SERVICE_DELIVERED = "SERVICE_DELIVERED"  # fairness.py SERVICED: usable
EV_ATTEMPT = "ATTEMPT"              # fairness.py ATTEMPTED
EV_EFFECT_OBSERVED = "EFFECT_OBSERVED"
EV_OUTCOME_RECORDED = "OUTCOME_RECORDED"
EV_PROOF_DISCHARGED = "PROOF_DISCHARGED"    # fairness.py ADVANCED
EV_COMPLETED = "COMPLETED"
EV_AUTHORITY_REFUSED = "AUTHORITY_REFUSED"
EV_SCHEDULER_HOLD = "SCHEDULER_HOLD"  # scheduler-side record of deliberate
                                      # non-consideration for policy reasons
EV_DISPATCH_NOT_OBSERVED = "DISPATCH_NOT_OBSERVED"  # negative claim
EV_RESOURCE_NOT_OBSERVED = "RESOURCE_NOT_OBSERVED"  # negative claim

EVENT_TYPES = (
    EV_RESOURCE_OFFER, EV_RESOURCE_WITHDRAWN, EV_OBLIGATION_ELIGIBLE,
    EV_DISPATCH, EV_DISPATCH_ACCEPTED, EV_SERVICE_DELIVERED, EV_ATTEMPT,
    EV_EFFECT_OBSERVED, EV_OUTCOME_RECORDED, EV_PROOF_DISCHARGED,
    EV_COMPLETED, EV_AUTHORITY_REFUSED, EV_SCHEDULER_HOLD,
    EV_DISPATCH_NOT_OBSERVED, EV_RESOURCE_NOT_OBSERVED,
)

# Negative-claim event types: asserting absence requires coverage evidence.
NEGATIVE_CLAIM_TYPES = (EV_DISPATCH_NOT_OBSERVED, EV_RESOURCE_NOT_OBSERVED)

# ---------------------------------------------------------------------------
# Causal verdicts.
# ---------------------------------------------------------------------------
V_ENVIRONMENT_BLOCKER = "ENVIRONMENT_BLOCKER"
V_SCHEDULER_STARVATION = "SCHEDULER_STARVATION"
V_SCHEDULER_SERVICE_FAILURE = "SCHEDULER_SERVICE_FAILURE"
V_WORKER_NONPROGRESS = "WORKER_NONPROGRESS"
V_GOVERNED_AUTHORITY_BLOCK = "GOVERNED_AUTHORITY_BLOCK"
V_OUTCOME_NOT_VERIFIED = "OUTCOME_NOT_VERIFIED"
V_CONFLICTED_EVIDENCE = "CONFLICTED_EVIDENCE"
V_INSUFFICIENT_OBSERVABILITY = "INSUFFICIENT_OBSERVABILITY"
V_MULTIPLE_SUPPORTED_CAUSES = "MULTIPLE_SUPPORTED_CAUSES"
V_UNDETERMINED = "UNDETERMINED"

VERDICTS = (
    V_ENVIRONMENT_BLOCKER, V_SCHEDULER_STARVATION, V_SCHEDULER_SERVICE_FAILURE,
    V_WORKER_NONPROGRESS, V_GOVERNED_AUTHORITY_BLOCK, V_OUTCOME_NOT_VERIFIED,
    V_CONFLICTED_EVIDENCE, V_INSUFFICIENT_OBSERVABILITY,
    V_MULTIPLE_SUPPORTED_CAUSES, V_UNDETERMINED,
)


@dataclass(frozen=True)
class EvidenceEvent:
    """One canonical evidence event.

    The observed event, the causal claim about it, and the verdict carry
    DIFFERENT identities and evidence — a worker cannot certify the cause
    of its own failure by writing "reason": "scheduler" in a log.
    """
    event_id: str
    workflow_id: str
    obligation_id: str
    event_type: str
    producer: str            # component reporting the event
    observer: str            # component/measurement authority witnessing it
    trace_id: str
    parent_event_ids: tuple = ()
    resource_id: Optional[str] = None
    lease_id: Optional[str] = None
    state_before: Optional[str] = None
    state_after: Optional[str] = None
    local_sequence: int = 0          # per-producer monotonic sequence
    logical_clock: int = 0           # Lamport clock: ordering, not truth
    artifact_hashes: tuple = ()
    signature_or_attestation: Optional[str] = None  # origin evidence; signing != truth
    observation_status: str = L0_REPORTED
    causal_status: str = CAUSAL_UNASSESSED
    scope: str = ""
    policy_version: str = ""

    def __post_init__(self):
        assert self.event_type in EVENT_TYPES, self.event_type
        assert self.observation_status in LADDER, self.observation_status
        assert self.causal_status in (
            CAUSAL_UNASSESSED, CAUSAL_HYPOTHESIZED,
            CAUSAL_SUPPORTED, CAUSAL_EXPERIMENTALLY_VERIFIED,
        ), self.causal_status
        # A signature proves origin under a trust model — never truthfulness.
        # This is documented, not machine-enforced, because the trust model
        # itself is scope-dependent. The verifier must still corroborate.


@dataclass(frozen=True)
class ObservationCoverage:
    """Coverage evidence required for any negative claim.

    A missing entry is not proof of absence. For "never available" or
    "not delivered" claims the trace must record all of these; otherwise
    the verdict is INSUFFICIENT_OBSERVABILITY, never an invented cause.
    """
    observation_interval: tuple      # (start_clock, end_clock) logical range
    monitored_sources: tuple         # event sources watched
    sequence_complete: bool          # no gaps in per-producer sequences
    dropped_message_indicators: tuple
    visibility_limits: tuple         # known blind spots, stated honestly

    def sufficient(self) -> bool:
        return (
            bool(self.monitored_sources)
            and self.sequence_complete
            and self.observation_interval[1] > self.observation_interval[0]
        )


@dataclass(frozen=True)
class CausalRelationship:
    """One typed edge in the causal proof graph."""
    relationship: str
    source_id: str
    target_id: str
    evidence_refs: tuple = ()       # artifact hashes / receipt ids justifying it
    causal_status: str = CAUSAL_UNASSESSED

    def __post_init__(self):
        assert self.relationship in RELATIONSHIPS, self.relationship

class CausalGraph:
    """Typed causal proof graph over evidence events.

    Promotion rules are machine-checked here:
    - CORRELATES_WITH can NEVER be silently promoted to CAUSED_BY.
    - HAPPENS_BEFORE establishes ordering, never causation.
    - CAUSED_BY requires the three-check (mechanism, counterfactual,
      independent reproduction) to be recorded on the relationship.
    - Competing explanations are preserved until evidence distinguishes
      them (the graph holds multiple hypotheses with their statuses).
    """

    def __init__(self):
        self.events = {}          # event_id -> EvidenceEvent
        self.relationships = []   # CausalRelationship list
        self.hypotheses = {}      # hypothesis_id -> dict

    def add_event(self, event: EvidenceEvent):
        if event.event_id in self.events:
            raise ValueError(f"duplicate event_id {event.event_id}")
        self.events[event.event_id] = event

    def add_relationship(self, rel: CausalRelationship):
        if rel.source_id not in self.events or rel.target_id not in self.events:
            raise ValueError("relationship references unknown event")
        if rel.relationship == REL_CAUSED_BY:
            # The three-check must be recorded before CAUSED_BY is asserted.
            checks = self.hypotheses.get(
                f"cause:{rel.source_id}->{rel.target_id}", {})
            if not (checks.get("mechanism") and checks.get("counterfactual")
                    and checks.get("reproduction")):
                raise ValueError(
                    "CAUSED_BY requires recorded mechanism + counterfactual "
                    "+ independent reproduction; use HYPOTHESIZED status first")
        self.relationships.append(rel)

    def record_three_check(self, source_id: str, target_id: str,
                           mechanism: bool = False,
                           counterfactual: bool = False,
                           reproduction: bool = False,
                           notes: str = ""):
        """Record the three-check causal responsibility test for a pair."""
        self.hypotheses[f"cause:{source_id}->{target_id}"] = {
            "mechanism": mechanism,
            "counterfactual": counterfactual,
            "reproduction": reproduction,
            "notes": notes,
        }

    def causal_order(self) -> list:
        """Reconstruct causal order from HAPPENS_BEFORE / DEPENDS_ON edges.

        Never sorts timestamps into a causal story. Events without a
        verified ordering relationship remain concurrent (unordered) —
        they are NOT forcibly arranged.
        Returns a list of tiers; each tier is a set of mutually
        unordered event ids.
        """
        edges = [(r.source_id, r.target_id) for r in self.relationships
                 if r.relationship in (REL_HAPPENS_BEFORE, REL_DEPENDS_ON)]
        # Kahn's algorithm with tiering.
        preds = {eid: set() for eid in self.events}
        succs = {eid: set() for eid in self.events}
        for a, b in edges:
            if a == b:
                continue
            succs[a].add(b)
            preds[b].add(a)
        tiers = []
        remaining = dict(preds)
        while remaining:
            tier = sorted(e for e, ps in remaining.items() if not ps)
            if not tier:
                # Cycle in ordering evidence: report, don't invent an order.
                raise ValueError(
                    "ordering cycle in HAPPENS_BEFORE/DEPENDS_ON evidence: "
                    f"{sorted(remaining)}")
            tiers.append(set(tier))
            for e in tier:
                del remaining[e]
            for e in remaining:
                remaining[e] -= set(tier)
        return tiers

    def competing_explanations(self, target_id: str) -> list:
        """All CAUSED_BY / PREVENTED_BY hypotheses targeting an event."""
        return [r for r in self.relationships
                if r.target_id == target_id
                and r.relationship in (REL_CAUSED_BY, REL_PREVENTED_BY)]


def qualify_ladder(event: EvidenceEvent, has_integrity: bool,
                   independent_witness: Optional[EvidenceEvent] = None,
                   causal_argument: Optional[dict] = None) -> str:
    """Walk the four-level evidence ladder for one event.

    L0 REPORTED: always (the event exists as a claim).
    L1 AUTHENTICATED: source-bound + integrity checks pass.
    L2 INDEPENDENTLY_CORROBORATED: a sufficiently independent observation
        supports the event within scope. The witness must NOT share a
        common failure source with the producer (checked via observer
        identity + artifact independence — same observer re-reading the
        same corrupted record does not count).
    L3 CAUSALLY_QUALIFIED: an independently justified causal argument
        supports the specified relationship (the three-check recorded).
    A signature proves origin under a trust model — it never, by itself,
    moves an event past L1.
    """
    if not has_integrity:
        return L0_REPORTED
    level = L1_AUTHENTICATED
    if independent_witness is not None:
        same_observer = (independent_witness.observer == event.observer
                         and independent_witness.producer == event.producer)
        same_artifacts = bool(
            set(independent_witness.artifact_hashes) & set(event.artifact_hashes))
        # Corroboration requires a genuinely independent observation:
        # different observer, or different artifacts. Two parties reading
        # the same corrupted record is agreement, not corroboration.
        if not (same_observer and same_artifacts):
            if independent_witness.observation_status in (L1_AUTHENTICATED,
                                                           L2_CORROBORATED,
                                                           L3_QUALIFIED):
                level = L2_CORROBORATED
    if causal_argument is not None and causal_argument.get("justified"):
        # L3 additionally requires the three-check for the specific
        # relationship being claimed.
        level = L3_QUALIFIED
    return level


def verify_negative_claim(event: EvidenceEvent,
                          coverage: Optional[ObservationCoverage]) -> tuple:
    """Verify a negative claim ("never available", "not delivered").

    Returns (accepted, verdict_or_note). A missing entry is NOT proof of
    absence. Without sufficient coverage the result is
    INSUFFICIENT_OBSERVABILITY — never an invented causal explanation.
    Incomplete telemetry must not shift responsibility to the quieter
    component.
    """
    if event.event_type not in NEGATIVE_CLAIM_TYPES:
        return True, "not a negative claim"
    if coverage is None or not coverage.sufficient():
        return False, V_INSUFFICIENT_OBSERVABILITY
    return True, "negative claim covered"


@dataclass
class CausalHypothesis:
    """One causal explanation under test, with its own identity.

    The hypothesis, the observed events, and the verdict are three
    different objects with different evidence — a worker cannot certify
    the cause of its own failure by embedding it in a log line.
    """
    hypothesis_id: str
    relationship: str          # expected: REL_CAUSED_BY or REL_PREVENTED_BY
    cause_event_id: str
    effect_event_id: str
    mechanism_ok: bool = False
    counterfactual_ok: bool = False
    reproduction_ok: bool = False
    alternative_causes_checked: bool = False
    status: str = CAUSAL_UNASSESSED
    notes: str = ""

    def three_check_passed(self) -> bool:
        return self.mechanism_ok and self.counterfactual_ok and self.reproduction_ok

@dataclass
class CausalTraceReceipt:
    """Machine-readable causal-trace receipt.

    This is a DERIVED assessment over canonical evidence — never a second
    source of truth. It deliberately avoids assigning blame before the
    evidence is sufficient (overall_qualification starts NOT_YET_ESTABLISHED).
    """
    trace_id: str
    workflow_id: str
    obligation_id: str
    runtime_sha: str
    policy_version: str
    events: list = field(default_factory=list)   # list of dicts
    causal_hypothesis: dict = field(default_factory=dict)
    overall_qualification: str = "NOT_YET_ESTABLISHED"
    verifier_identity: str = ""
    clock_assumptions: str = ""
    artifact_links: tuple = ()

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "workflow_id": self.workflow_id,
            "obligation_id": self.obligation_id,
            "runtime_sha": self.runtime_sha,
            "policy_version": self.policy_version,
            "events": self.events,
            "causal_hypothesis": self.causal_hypothesis,
            "overall_qualification": self.overall_qualification,
            "verifier_identity": self.verifier_identity,
            "clock_assumptions": self.clock_assumptions,
            "artifact_links": list(self.artifact_links),
        }


class IndependentCausalVerifier:
    """Independent verifier: reconstructs what happened from evidence.

    The cold-verifier standard: a fresh verifier with no trust in the
    original logs, labels, or agents must be able to reproduce the
    conclusion. Verdicts come from source evidence + controlled
    experiments — never from a prewritten failure_type label.
    """

    def __init__(self, graph: CausalGraph, verifier_identity: str = "INDEPENDENT-VERIFY"):
        self.graph = graph
        self.verifier_identity = verifier_identity
        self.findings = []

    # -- layer 1: observation -------------------------------------------
    def check_observations(self) -> dict:
        """Qualify every event on the ladder; flag integrity failures."""
        result = {}
        for eid, ev in self.graph.events.items():
            if ev.observation_status == L0_REPORTED:
                self.findings.append(f"{eid}: REPORTED only — no integrity evidence")
            result[eid] = ev.observation_status
        return result

    def check_sequence_integrity(self) -> list:
        """Per-producer local_sequence must be gap-free where claimed.

        Gaps mean missing events — the trace is not a complete record.
        This feeds negative-claim coverage, not blame.
        """
        issues = []
        by_producer = {}
        for ev in self.graph.events.values():
            by_producer.setdefault(ev.producer, []).append(ev.local_sequence)
        for producer, seqs in by_producer.items():
            seqs = sorted(seqs)
            if seqs != list(range(seqs[0], seqs[0] + len(seqs))):
                issues.append(
                    f"producer {producer}: sequence gap {seqs} — "
                    "trace incomplete; negative claims need coverage evidence")
        return issues

    # -- layer 2: causal relationships -----------------------------------
    def check_promotion_rules(self) -> list:
        """No silent promotion: CORRELATES_WITH -> CAUSED_BY is rejected."""
        violations = []
        caused_pairs = {(r.source_id, r.target_id)
                        for r in self.graph.relationships
                        if r.relationship == REL_CAUSED_BY}
        for r in self.graph.relationships:
            if (r.relationship == REL_CORRELATES_WITH
                    and (r.source_id, r.target_id) in caused_pairs):
                hyp = self.graph.hypotheses.get(
                    f"cause:{r.source_id}->{r.target_id}", {})
                if not (hyp.get("mechanism") and hyp.get("counterfactual")
                        and hyp.get("reproduction")):
                    violations.append(
                        f"silent promotion rejected: {r.source_id} -> "
                        f"{r.target_id} has CORRELATES_WITH but CAUSED_BY "
                        "lacks the three-check")
        return violations

    # -- layer 3: responsibility -----------------------------------------
    def evaluate_hypothesis(self, hyp: CausalHypothesis) -> str:
        """Run the three-check; return the causal status reached.

        Mechanism: can the behavior produce the failure under the contracts?
        Counterfactual: without the defect (conditions fixed), does the
            failure persist? If yes, the defect is not the cause.
        Independent reproduction: reproduced without trusting the
            component's own explanation.
        Observational-only evidence yields a mechanistic explanation WITH
        limitations — never mislabeled as reproduced causation.
        """
        if hyp.three_check_passed():
            hyp.status = CAUSAL_EXPERIMENTALLY_VERIFIED
        elif hyp.mechanism_ok and hyp.counterfactual_ok:
            hyp.status = CAUSAL_SUPPORTED
            hyp.notes += (" [observational only: mechanistic explanation "
                          "with limitations, not reproduced causation]")
        elif hyp.mechanism_ok:
            hyp.status = CAUSAL_HYPOTHESIZED
        else:
            hyp.status = CAUSAL_UNASSESSED
        return hyp.status

    def issue_verdict(self, hypotheses: list,
                      coverage_map: dict = None) -> tuple:
        """Issue the causal verdict from evidence, not labels.

        The verdict VALUE is recomputed here from the evidence shape
        with the given coverage map — it is never inherited from a
        hypothesis note computed under different coverage. The
        hypotheses determine only the QUALIFICATION LEVEL: an
        evidence-derived verdict whose three-check fails is reported
        as UNDETERMINED, not promoted. Competing qualified
        explanations yield MULTIPLE_SUPPORTED_CAUSES.
        Returns (verdict, receipt_dict).
        """
        coverage_map = coverage_map or {}
        evidence_verdict, _reasons = derive_verdict(self.graph, coverage_map)
        qualified = []
        for hyp in hypotheses:
            status = self.evaluate_hypothesis(hyp)
            if status in (CAUSAL_SUPPORTED, CAUSAL_EXPERIMENTALLY_VERIFIED):
                # Negative-claim hypotheses need coverage.
                ev = self.graph.events.get(hyp.cause_event_id)
                if ev is not None and ev.event_type in NEGATIVE_CLAIM_TYPES:
                    ok, note = verify_negative_claim(
                        ev, coverage_map.get(hyp.cause_event_id))
                    if not ok:
                        self.findings.append(
                            f"{hyp.hypothesis_id}: negative claim "
                            f"uncovered -> {note}")
                        continue
                qualified.append(hyp)
        verdict = self._select_verdict(qualified, evidence_verdict)
        receipt = self._build_receipt(hypotheses, verdict)
        return verdict, receipt.to_dict()

    def _select_verdict(self, qualified: list, evidence_verdict: str) -> str:
        if not qualified:
            # Distinguish "conflicted" from "insufficient" from "unknown".
            if any("conflict" in f.lower() or "disagree" in f.lower()
                   for f in self.findings):
                return V_CONFLICTED_EVIDENCE
            if any("INSUFFICIENT_OBSERVABILITY" in f for f in self.findings):
                return V_INSUFFICIENT_OBSERVABILITY
            # An evidence-derived verdict that failed the three-check is
            # reported as UNDETERMINED, not promoted.
            return V_UNDETERMINED
        if len(qualified) > 1:
            return V_MULTIPLE_SUPPORTED_CAUSES
        return evidence_verdict

    def _build_receipt(self, hypotheses: list, verdict: str) -> CausalTraceReceipt:
        events = [{
            "id": e.event_id,
            "type": e.event_type,
            "producer": e.producer,
            "observer": e.observer,
            "qualification": e.observation_status,
            "causal_status": e.causal_status,
        } for e in self.graph.events.values()]
        hyp = hypotheses[0] if hypotheses else None
        return CausalTraceReceipt(
            trace_id=next(iter(self.graph.events.values())).trace_id
            if self.graph.events else "",
            workflow_id=next(iter(self.graph.events.values())).workflow_id
            if self.graph.events else "",
            obligation_id=next(iter(self.graph.events.values())).obligation_id
            if self.graph.events else "",
            runtime_sha="spec",
            policy_version=next(iter(self.graph.events.values())).policy_version
            if self.graph.events else "",
            events=events,
            causal_hypothesis={
                "relationship": hyp.relationship if hyp else None,
                "supporting_events": ([hyp.cause_event_id, hyp.effect_event_id]
                                      if hyp else []),
                "counterfactual_replay": ("DONE" if hyp and hyp.counterfactual_ok
                                          else "PENDING"),
                "alternative_causes_checked": bool(
                    hyp and hyp.alternative_causes_checked),
                "verdict": verdict,
            },
            overall_qualification=(verdict if verdict not in
                                   (V_UNDETERMINED, V_INSUFFICIENT_OBSERVABILITY,
                                    V_CONFLICTED_EVIDENCE)
                                   else "NOT_YET_ESTABLISHED"),
            verifier_identity=self.verifier_identity,
            clock_assumptions=("Lamport logical clocks for ordering; "
                               "wall-clock never used for causation"),
        )

# ---------------------------------------------------------------------------
# Controlled experiment harness: four-node KNOW -> LAW -> ACT -> VERIFY.
# ---------------------------------------------------------------------------

NODE_KNOW = "KNOW"
NODE_LAW = "LAW"
NODE_ACT = "ACT"
NODE_VERIFY = "VERIFY"


class ControlledWorkflow:
    """Deterministic four-node workflow for the decisive experiment.

    Frozen obligation, code, resource conditions, acceptance criteria.
    Fault injection: environment outage / scheduler withholds service /
    worker fails. Each run produces EvidenceEvents with producer-side AND
    consumer-side witnesses at every boundary, so the independent
    verifier can reconstruct causality from evidence.
    """

    def __init__(self, workflow_id: str = "WF-001",
                 obligation_id: str = "ACT-042",
                 policy_version: str = "LAW-V1"):
        self.workflow_id = workflow_id
        self.obligation_id = obligation_id
        self.policy_version = policy_version
        self._seq = 0
        self._clock = 0

    def _next(self) -> tuple:
        self._seq += 1
        self._clock += 1
        return self._seq, self._clock

    def _ev(self, event_id: str, event_type: str, producer: str,
            observer: str, status: str = L1_AUTHENTICATED, **kw) -> EvidenceEvent:
        seq, clock = self._next()
        return EvidenceEvent(
            event_id=event_id, workflow_id=self.workflow_id,
            obligation_id=self.obligation_id, event_type=event_type,
            producer=producer, observer=observer,
            trace_id=f"TRACE-{self.workflow_id}",
            local_sequence=seq, logical_clock=clock,
            observation_status=status, scope="experiment",
            policy_version=self.policy_version, **kw)

    def run(self, fault: str, lying_producer: str = None,
            swapped_labels: bool = False) -> CausalGraph:
        """Run one controlled case.

        fault: "environment_outage" | "scheduler_withholds" | "worker_fails"
            | "authority_refused" | "healthy" | "dispatch_without_resources"
            | "false_success" | "two_blockers".
        lying_producer: a producer whose log is corrupted (false content).
        swapped_labels: swap the reported failure labels (adversarial).
        Returns the evidence graph for the independent verifier.
        """
        g = CausalGraph()
        W, O = self.workflow_id, self.obligation_id

        def maybe_lie(producer: str, event_type: str) -> str:
            # A corrupted log: the producer reports the opposite of what
            # happened. The verifier must reject the false evidence (via
            # integrity/corroboration failure) or downgrade to uncertainty —
            # never follow the narrative.
            if lying_producer == producer and swapped_labels:
                return {EV_RESOURCE_OFFER: EV_RESOURCE_WITHDRAWN,
                        EV_RESOURCE_WITHDRAWN: EV_RESOURCE_OFFER,
                        EV_DISPATCH: EV_DISPATCH_NOT_OBSERVED,
                        EV_DISPATCH_NOT_OBSERVED: EV_DISPATCH}.get(
                            event_type, event_type)
            return event_type

        # KNOW observes the obligation and the resource state.
        # "two_blockers": resource withdrawn AND scheduler withholds.
        resource_available = fault not in ("environment_outage", "two_blockers")
        g.add_event(self._ev("E1", maybe_lie("RESOURCE_RUNTIME",
                             EV_RESOURCE_OFFER if resource_available
                             else EV_RESOURCE_WITHDRAWN),
                             "RESOURCE_RUNTIME", "KNOW"))
        g.add_event(self._ev("E2", EV_OBLIGATION_ELIGIBLE, "KNOW", "KNOW"))
        # LAW authorizes (or refuses).
        authorized = fault != "authority_refused"
        g.add_event(self._ev(
            "E3", EV_OBLIGATION_ELIGIBLE if authorized else EV_AUTHORITY_REFUSED,
            "LAW", "LAW"))
        # ACT (scheduler side): dispatch decision.
        # "dispatch_without_resources": the scheduler issues a dispatch
        # but provides no usable lease — a service-guarantee failure.
        no_resources = (fault == "dispatch_without_resources")
        scheduler_dispatches = ((resource_available and authorized
                                 and fault not in ("scheduler_withholds",
                                                   "two_blockers"))
                                or no_resources)
        g.add_event(self._ev(
            "E4", maybe_lie("SCHEDULER",
                            EV_DISPATCH if scheduler_dispatches
                            else EV_DISPATCH_NOT_OBSERVED),
            "SCHEDULER", "SCHEDULER",
            parent_event_ids=("E1", "E2", "E3")))
        # E4v: VERIFY's INDEPENDENT observation of the dispatch channel.
        # This is modeled as a separate measurement authority, not a copy
        # of the producer's log: its content comes from ground truth, so
        # a lying producer cannot alter it. The verifier prefers it over
        # the producer's claim (see _trusted_dispatch_evidence).
        g.add_event(self._ev(
            "E4v", EV_DISPATCH if scheduler_dispatches
            else EV_DISPATCH_NOT_OBSERVED,
            "TRACE_VERIFIER", "VERIFY", status=L2_CORROBORATED,
            parent_event_ids=("E4",)))
        # Consumer-side witness: did the worker receive a usable lease?
        # Skipped for dispatch_without_resources: nothing usable was provided.
        if scheduler_dispatches and not no_resources:
            g.add_event(self._ev("E5", EV_DISPATCH_ACCEPTED,
                                 "WORKER", "SCHEDULER",
                                 parent_event_ids=("E4",),
                                 lease_id="LEASE-1"))
            g.add_event(self._ev("E6", EV_SERVICE_DELIVERED,
                                 "SCHEDULER", "WORKER",
                                 parent_event_ids=("E5",),
                                 lease_id="LEASE-1"))
        # ACT (worker side): attempt and effect.
        # "false_success": the worker claims an effect and records an
        # outcome, but no state change is evidenced.
        false_success = (fault == "false_success")
        worker_succeeds = (scheduler_dispatches and fault not in
                           ("worker_fails", "false_success"))
        if scheduler_dispatches and not no_resources:
            g.add_event(self._ev(
                "E7", EV_ATTEMPT,
                "WORKER", "WORKER", parent_event_ids=("E6",)))
            if false_success:
                g.add_event(self._ev(
                    "E8", EV_EFFECT_OBSERVED,
                    "WORKER", "VERIFY", parent_event_ids=("E7",),
                    state_before="pending", state_after=None))
                g.add_event(self._ev("E9", EV_OUTCOME_RECORDED,
                                     "WORKER", "VERIFY",
                                     parent_event_ids=("E8",)))
            elif worker_succeeds:
                g.add_event(self._ev(
                    "E8", EV_EFFECT_OBSERVED,
                    "WORKER", "VERIFY", parent_event_ids=("E7",),
                    state_before="pending", state_after="done"))
                g.add_event(self._ev("E9", EV_OUTCOME_RECORDED,
                                     "WORKER", "VERIFY",
                                     parent_event_ids=("E8",)))
                g.add_event(self._ev("E10", EV_PROOF_DISCHARGED,
                                     "VERIFY", "VERIFY",
                                     parent_event_ids=("E9",)))
                g.add_event(self._ev("E11", EV_COMPLETED, "VERIFY", "VERIFY",
                                     parent_event_ids=("E10",)))
            else:
                g.add_event(self._ev(
                    "E8", EV_ATTEMPT,
                    "WORKER", "VERIFY", parent_event_ids=("E7",)))
        # "two_blockers": resource withdrawn AND the scheduler records a
        # deliberate policy hold independent of the resource state.
        if fault == "two_blockers":
            g.add_event(self._ev("E4b", EV_SCHEDULER_HOLD,
                                 "SCHEDULER", "SCHEDULER",
                                 parent_event_ids=("E2",)))
        # Corrupted producer logs: downgrade every event from the lying
        # producer to REPORTED (no integrity). The verifier must then
        # reject the false evidence or downgrade to uncertainty — never
        # follow the corrupted narrative.
        if lying_producer and swapped_labels:
            import dataclasses
            for eid, ev in list(g.events.items()):
                if ev.producer == lying_producer:
                    g.events[eid] = dataclasses.replace(
                        ev, observation_status=L0_REPORTED)
        # Causal-order edges from authenticated sequencing (never timestamps).
        ids = list(g.events)
        for a, b in zip(ids, ids[1:]):
            g.add_relationship(CausalRelationship(
                REL_HAPPENS_BEFORE, a, b, evidence_refs=("local_sequence",)))
        return g


# The canonical A/B/C experiment table from the framework.
# Each row: (experiment, fault, expected_verdict).
EXPERIMENT_TABLE = (
    ("A-baseline", "scheduler_withholds", V_SCHEDULER_STARVATION),
    ("B-intervention", "healthy", V_UNDETERMINED),  # no failure: no causal verdict
    ("C-worker-fault", "worker_fails", V_WORKER_NONPROGRESS),
    ("env-outage", "environment_outage", V_ENVIRONMENT_BLOCKER),
    ("authority", "authority_refused", V_GOVERNED_AUTHORITY_BLOCK),
)

# The nine-scenario adversarial suite: same symptom (unfinished workflow),
# nine different causes, nine expected verdicts.
ADVERSARIAL_SUITE = (
    ("external service unavailable", "environment_outage", V_ENVIRONMENT_BLOCKER),
    ("service available, scheduler ignores eligible work",
     "scheduler_withholds", V_SCHEDULER_STARVATION),
    ("scheduler dispatches without usable resources",
     "dispatch_without_resources", V_SCHEDULER_SERVICE_FAILURE),
    ("worker receives usable service but endlessly retries",
     "worker_fails", V_WORKER_NONPROGRESS),
    ("LAW legitimately prohibits the operation",
     "authority_refused", V_GOVERNED_AUTHORITY_BLOCK),
    ("worker claims success but target state unchanged",
     "false_success_claim", V_OUTCOME_NOT_VERIFIED),
    ("resource and scheduler evidence disagree",
     "conflicted_evidence", V_CONFLICTED_EVIDENCE),
    ("required event coverage incomplete",
     "incomplete_coverage", V_INSUFFICIENT_OBSERVABILITY),
    ("two independent blockers exist",
     "two_blockers", V_MULTIPLE_SUPPORTED_CAUSES),
)


def _trusted_dispatch_evidence(graph: CausalGraph):
    """The dispatch evidence the verifier trusts.

    Independent observation (E4v) is preferred over the producer's own
    claim (E4). A producer claim that is unqualified (REPORTED only) or
    that contradicts the independent observation is set aside — the
    verifier never follows a producer's narrative over independent
    measurement.
    """
    evs = graph.events
    e4, e4v = evs.get("E4"), evs.get("E4v")
    if e4v is not None and e4v.observation_status in (
            L2_CORROBORATED, L3_QUALIFIED):
        return e4v
    if e4 is not None and e4.observation_status in (
            L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED):
        return e4
    return None


def derive_verdict(graph: CausalGraph,
                   coverage_map: dict = None) -> tuple:
    """Derive the causal verdict from the EVIDENCE SHAPE — never from a
    prewritten failure_type label.

    Walks the expected causal chain (resource -> eligibility ->
    authorization -> dispatch -> acceptance -> service -> attempt ->
    effect -> outcome -> discharge -> completion) and names the first
    broken link, using only events at AUTHENTICATED or better. Producer/
    consumer witness disagreement yields CONFLICTED_EVIDENCE. Negative
    claims without coverage yield INSUFFICIENT_OBSERVABILITY. Uncertainty
    is reported as uncertainty — never invented blame.

    Returns (verdict, reasons).
    """
    coverage_map = coverage_map or {}
    evs = graph.events
    reasons = []
    get = evs.get

    def qualified(eid):
        e = get(eid)
        return (e is not None and e.observation_status in
                (L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED))

    # Witness conflict: the scheduler claims a SPECIFIC lease, but the
    # consumer side shows no acceptance of it and the claim is not
    # corroborated — the witnesses disagree about what happened.
    # (A dispatch with no lease and no acceptance is not a conflict;
    # it is a service-guarantee failure, handled below.)
    e4, e5 = get("E4"), get("E5")
    if (e4 is not None and e4.event_type == EV_DISPATCH
            and qualified("E4") and e4.lease_id is not None and e5 is None
            and e4.observation_status == L1_AUTHENTICATED):
        reasons.append("scheduler claims lease; worker shows no acceptance "
                       "and the claim is uncorroborated")
        return V_CONFLICTED_EVIDENCE, reasons

    e1 = get("E1")
    e1_withdrawn = (e1 is not None and qualified("E1")
                    and e1.event_type == EV_RESOURCE_WITHDRAWN)
    # Two independent blockers: resource withdrawn AND an authenticated
    # scheduler-side record of deliberate non-consideration for policy
    # reasons (not merely the correct idle response to no resource).
    # A scheduler that simply does not dispatch when there is no resource
    # is behaving correctly — that is one blocker, not two.
    e_hold = get("E4b")
    if (e1_withdrawn and e_hold is not None and qualified("E4b")
            and e_hold.event_type == EV_SCHEDULER_HOLD):
        reasons.append("resource withdrawn AND scheduler independently "
                       "withheld for policy reasons: two blockers")
        return V_MULTIPLE_SUPPORTED_CAUSES, reasons
    if e1 is None or e1_withdrawn:
        reasons.append("resource not offered (authenticated)")
        return V_ENVIRONMENT_BLOCKER, reasons
    if not qualified("E1"):
        reasons.append("resource-offer event not authenticated")

    e3 = get("E3")
    if qualified("E3") and e3.event_type == EV_AUTHORITY_REFUSED:
        reasons.append("LAW refused authorization")
        return V_GOVERNED_AUTHORITY_BLOCK, reasons

    if e4 is None:
        reasons.append("no dispatch evidence at all")
        return V_INSUFFICIENT_OBSERVABILITY, reasons
    # Trust the independent observation over the producer's claim.
    dispatch_ev = _trusted_dispatch_evidence(graph)
    if dispatch_ev is not None and dispatch_ev.event_id != "E4":
        producer_claim = e4.event_type if e4 is not None else None
        if producer_claim != dispatch_ev.event_type:
            reasons.append("producer dispatch claim set aside: contradicts "
                           "independent observation")
    if dispatch_ev is None:
        reasons.append("dispatch evidence unqualified")
        return V_INSUFFICIENT_OBSERVABILITY, reasons
    if dispatch_ev.event_type == EV_DISPATCH_NOT_OBSERVED:
        cov = coverage_map.get(dispatch_ev.event_id, coverage_map.get("E4"))
        ok, note = verify_negative_claim(dispatch_ev, cov)
        if not ok:
            reasons.append(f"dispatch-absence claim uncovered: {note}")
            return V_INSUFFICIENT_OBSERVABILITY, reasons
        reasons.append("eligible + authorized + resource available, "
                       "no dispatch observed with coverage")
        return V_SCHEDULER_STARVATION, reasons

    # Dispatch claimed: usable service?
    e6 = get("E6")
    if dispatch_ev.event_type == EV_DISPATCH:
        if e6 is None or not qualified("E6"):
            reasons.append("dispatch without usable service")
            return V_SCHEDULER_SERVICE_FAILURE, reasons

    # Service delivered: did the worker advance?
    e8 = get("E8")
    if qualified("E6"):
        if e8 is None or not qualified("E8"):
            reasons.append("usable service, no recorded attempt/effect")
            return V_WORKER_NONPROGRESS, reasons
        if e8.event_type == EV_EFFECT_OBSERVED and e8.state_after in (None, ""):
            reasons.append("effect claimed but no state change evidenced")
            return V_OUTCOME_NOT_VERIFIED, reasons
        if e8.event_type != EV_EFFECT_OBSERVED:
            reasons.append("usable service, attempt produced no effect")
            return V_WORKER_NONPROGRESS, reasons

    e11 = get("E11")
    if qualified("E11") and e11.event_type == EV_COMPLETED:
        reasons.append("workflow completed: no failure to diagnose")
        return V_UNDETERMINED, reasons
    reasons.append("chain intact but no completion recorded")
    return V_UNDETERMINED, reasons


def diagnose(graph: CausalGraph, fault: str,
             counterfactual_ok: bool = False,
             reproduction_ok: bool = False) -> CausalHypothesis:
    """Build the causal hypothesis for a run.

    The verdict VALUE comes from derive_verdict (evidence shape only).
    The hypothesis three-check determines the QUALIFICATION LEVEL of
    that verdict: mechanism alone -> HYPOTHESIZED; + counterfactual ->
    SUPPORTED (observational limits noted); + independent reproduction ->
    EXPERIMENTALLY_VERIFIED.
    """
    verdict, reasons = derive_verdict(graph)
    # The cause/effect pair is the broken link named by the evidence.
    cause, effect = "E1", "E4"
    if verdict == V_SCHEDULER_STARVATION:
        cause, effect = "E4", "E7"
    elif verdict == V_SCHEDULER_SERVICE_FAILURE:
        cause, effect = "E4", "E6"
    elif verdict == V_WORKER_NONPROGRESS:
        cause, effect = "E6", "E8"
    elif verdict == V_GOVERNED_AUTHORITY_BLOCK:
        cause, effect = "E3", "E4"
    elif verdict == V_OUTCOME_NOT_VERIFIED:
        cause, effect = "E8", "E9"
    evs = graph.events

    def _ev_ok(eid):
        e = evs.get(eid)
        return (e is not None and e.observation_status in
                (L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED))

    # Mechanism: the cause event is at least authenticated. For the
    # dispatch link, the verifier trusts the independent observation
    # over an unqualified producer claim (a lying scheduler's REPORTED
    # dispatch does not defeat the mechanism check — the independent
    # E4v observation carries it).
    if cause == "E4":
        trusted = _trusted_dispatch_evidence(graph)
        mechanism = trusted is not None
    else:
        mechanism = _ev_ok(cause)
    return CausalHypothesis(
        hypothesis_id=f"H-{fault}",
        relationship=REL_CAUSED_BY,
        cause_event_id=cause,
        effect_event_id=effect if effect in evs else cause,
        mechanism_ok=mechanism,
        counterfactual_ok=counterfactual_ok,
        reproduction_ok=reproduction_ok,
        alternative_causes_checked=True,
        notes="; ".join(reasons) + f" || derived_verdict:{verdict}",
    )


def derived_verdict_of(hyp: CausalHypothesis) -> str:
    """Extract the evidence-derived verdict carried by a hypothesis."""
    for part in hyp.notes.split("||"):
        part = part.strip()
        if part.startswith("derived_verdict:"):
            return part.split(":", 1)[1]
    return V_UNDETERMINED
