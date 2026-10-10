"""D31 — Causal Uncertainty Without False Blame.

THE JOB: represent an incident as an evidence-bound set of observations,
uncertainties, blockers, and competing causal hypotheses — NEVER as a
single failure_reason field.

CORE RULE (D31): record what was observed, what could not be observed, what
the evidence supports, what remains possible, and what would distinguish
the remaining explanations. Assign responsibility only to the scope the
evidence actually establishes. Never trade an accurate set of partial
truths for one confident but unsupported explanation.

Four independent dimensions, never collapsed:
  Observability — what could we inspect, per source/event-type/resource/
                 interval. Absence is only meaningful inside covered scope.
                 Not observed != did not happen.
  Evidence state — supports / contradicts / fails-to-resolve. Conflicting
                 claims decomposed into precise propositions with
                 claim-level verdicts. Two logs from one event bus are NOT
                 two independent witnesses.
  Blocker state — what prevents progress, independently established.
                 Blockers as AND/OR combinations with minimal blocking
                 sets. Confirmed blocker != sole cause. Repairing one
                 blocker while another remains: the workflow stays blocked,
                 and the system must say so.
  Causal state — hypotheses as competing revisable claims (mechanism,
                 contribution type, relationships, next discriminating
                 test). Unresolved hypothesis != false. Unresolved
                 hypotheses never promote to verified lessons. Reported
                 fault != verified responsibility.

Composes (extends, never duplicates):
  d30_causal_trace.py — EvidenceEvent, authenticate, tamper, make_event,
      serialize_trace/deserialize_trace. D31 consumes D30's canonical
      evidence events as its evidence pool; D30 verifies causality, D31
      refuses to collapse it into blame.
  propagation.py — SupportSet, detect_false_corroboration, genuine_paths.
      Apparent independence is rejected when witness paths share one
      contaminated source.

SPEC + deterministic fixture machinery. NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field

from drift_canary.d30_causal_trace import (
    CausalTrace,
    EvidenceEvent,
    authenticate,
    deserialize_trace,
    make_event,
    serialize_trace,
    tamper,
)
from drift_canary.propagation import (
    SupportSet,
    detect_false_corroboration,
    genuine_paths,
)

# ---------------------------------------------------------------------------
# Vocabularies. The analyzer may ONLY emit these values. The one thing it
# may never emit anywhere is a single failure_reason — there is no such
# field on any verdict this module produces, and tests assert its absence.
# ---------------------------------------------------------------------------

OBSERVABILITY = (
    "COVERED_COMPLETE",     # every event in scope was inspected
    "COVERED_PARTIAL",      # scope inspected, gaps remain inside it
    "UNOBSERVED",           # nothing inspected in this scope
    "CONFLICTED_COVERAGE",  # coverage records disagree about the scope
    "NOT_APPLICABLE",       # scope does not apply to this incident
)

# Absence inside one of these scopes means "did not happen". Absence
# anywhere else means only "not seen".
ABSENCE_IS_EVIDENCE_IN = frozenset({"COVERED_COMPLETE"})

CLAIM_VERDICTS = (
    "SUPPORTED",      # >=2 genuinely independent witness paths
    "REFUTED",        # independently established counter-evidence
    "CONFLICTED",     # genuine paths on both sides — decompose, don't tie
    "UNDETERMINED",   # not enough independent evidence either way
)

CONTRIBUTION_TYPES = (
    "prevents_progress",   # holds the workflow stopped
    "enables_progress",    # its removal lets the workflow move
    "masks_cause",         # hides or rewrites the evidence trail
    "correlated_only",     # co-occurs; mechanism not established
)

HYPOTHESIS_STATUSES = (
    "supported",
    "refuted",
    "unresolved",          # may be revised, never deleted, never promoted
)

# ---------------------------------------------------------------------------
# Dimension 1 — Observability. Per source / event-type / resource / interval.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ObservationScope:
    """One inspected (or uninspected) slice of the world.

    interval is (start_lamport, end_lamport) on the logical clock; the
    wall clock is never trusted alone (D30).
    """
    scope_id: str
    source: str
    event_type: str
    resource_id: str
    interval: tuple            # (start_lamport, end_lamport)
    observability: str

    def __post_init__(self):
        assert self.observability in OBSERVABILITY, self.observability
        assert len(self.interval) == 2, self.interval

    def absence_is_evidence(self) -> bool:
        """True only when the scope is completely covered: a missing
        event inside COVERED_COMPLETE means it did not happen. Anywhere
        else, absence means only that nothing was observed."""
        return self.observability in ABSENCE_IS_EVIDENCE_IN


# ---------------------------------------------------------------------------
# Dimension 2 — Evidence state. Supports / contradicts / fails-to-resolve.
# Conflicting claims are decomposed into precise propositions; apparent
# independence is rejected when witness paths share one source.
# ---------------------------------------------------------------------------


@dataclass
class ClaimProposition:
    """One precise proposition, e.g. 'lease-reached-worker' instead of a
    mushy 'dispatch failed'.

    supporting_evidence: D30 event ids arguing FOR the proposition.
    refuting_evidence:   D30 event ids arguing AGAINST it.
    origin_of: event_id -> originating source. Two logs from one event
               bus map to ONE origin — they are not two witnesses.
    """
    proposition_id: str
    statement: str
    supporting_evidence: tuple = ()
    refuting_evidence: tuple = ()
    origin_of: dict = field(default_factory=dict)

    def _support_sets(self) -> tuple:
        return tuple(
            SupportSet(
                set_id=f"{self.proposition_id}-s{i}",
                evidence_refs=(ev,),
                covers=("scope",),
            )
            for i, ev in enumerate(self.supporting_evidence)
        )

    def _refute_sets(self) -> tuple:
        return tuple(
            SupportSet(
                set_id=f"{self.proposition_id}-r{i}",
                evidence_refs=(ev,),
                covers=("scope",),
                polarity="contradicts",
            )
            for i, ev in enumerate(self.refuting_evidence)
        )

    def independent_witness_count(self) -> int:
        """Genuine independent witness paths for the proposition. Support
        sets that share one originating source collapse into ONE path —
        internal repetition is not corroboration (D32's anti-citogenesis
        rule, applied here via propagation.genuine_paths)."""
        groups = genuine_paths(self._support_sets(), self.origin_of)
        return len(groups)

    def false_corroboration_pairs(self) -> tuple:
        """Pairs of support sets whose 'independent corroboration' is
        false because they share a hidden origin."""
        return detect_false_corroboration(
            self._support_sets(), "scope", self.origin_of)


class EvidenceState:
    """The evidence dimension of one incident: propositions, decomposed
    claims, independence-checked verdicts."""

    def __init__(self) -> None:
        self.propositions: dict[str, ClaimProposition] = {}
        self._event_pool: dict[str, EvidenceEvent] = {}

    # -- evidence pool (D30 events) -------------------------------------
    def add_event(self, event: EvidenceEvent) -> None:
        self._event_pool[event.event_id] = event

    def authenticated(self, event_id: str) -> bool:
        event = self._event_pool.get(event_id)
        if event is None:
            return False
        ok, _ = authenticate(event)
        return ok

    # -- propositions ----------------------------------------------------
    def add_proposition(self, prop: ClaimProposition) -> None:
        self.propositions[prop.proposition_id] = prop

    def verdict_of(self, proposition_id: str) -> tuple:
        """(claim_verdict, reason). Fails-to-resolve is explicit: a
        proposition with conflicting or thin evidence is UNDETERMINED or
        CONFLICTED, never quietly promoted to SUPPORTED."""
        prop = self.propositions[proposition_id]
        # Authentication first: compromised or missing evidence cannot
        # carry a claim.
        bad = [e for e in prop.supporting_evidence
               if not self.authenticated(e)]
        bad += [e for e in prop.refuting_evidence
                if not self.authenticated(e)]
        if bad:
            return ("UNDETERMINED",
                    f"evidence not authenticated or missing: {bad}")

        witnesses = prop.independent_witness_count()
        false_pairs = prop.false_corroboration_pairs()
        refute_witnesses = len(genuine_paths(
            prop._refute_sets(), prop.origin_of))

        if witnesses >= 1 and refute_witnesses >= 1:
            return ("CONFLICTED",
                    "genuine paths on both sides: decompose further, "
                    "do not average into a tie")
        if refute_witnesses >= 1:
            return ("REFUTED",
                    f"{refute_witnesses} independent path(s) refute it")
        if witnesses >= 2:
            reason = f"{witnesses} genuinely independent witness paths"
            if false_pairs:
                reason += (f"; {len(false_pairs)} false-corroboration "
                           f"pair(s) collapsed")
            return ("SUPPORTED", reason)
        if witnesses == 1:
            return ("UNDETERMINED",
                    "single independent witness: insufficient "
                    "corroboration for SUPPORTED")
        return ("UNDETERMINED", "no authenticated independent evidence")

# ---------------------------------------------------------------------------
# Dimension 3 — Blocker state. What prevents progress, independently
# established. Blockers as AND/OR combinations with minimal blocking sets.
# Confirmed blocker != sole cause. Repairing one blocker while another
# remains means the workflow stays blocked, and the system must say so.
# ---------------------------------------------------------------------------


@dataclass
class Blocker:
    """One independently established impediment.

    established_by: D30 event ids that independently establish the
        blocker. A blocker with no evidence is a hypothesis, not a
        blocker — BlockerGraph enforces this.
    repaired: becomes True only through apply_intervention with a
        witness event; a bare flag flip is refused.
    """
    blocker_id: str
    description: str
    condition: str
    established_by: tuple = ()
    repaired: bool = False
    repair_witness: str = ""


class BlockerGraph:
    """AND/OR combinations of blockers. The workflow is blocked iff at
    least one minimal blocking set is fully established and unrepaired.

    blocking_sets: tuple of frozensets of blocker ids. Each frozenset is
        one combination that keeps the workflow stopped (AND inside the
        set; OR across sets). Minimal blocking sets are derived by
        dropping any set that strictly contains another.
    """

    def __init__(self, blocking_sets: tuple = ()) -> None:
        self.blockers: dict[str, Blocker] = {}
        self.blocking_sets: tuple = tuple(
            frozenset(s) for s in blocking_sets)
        self._intervention_log: list = []

    def add_blocker(self, blocker: Blocker) -> None:
        if not blocker.established_by:
            raise ValueError(
                f"blocker {blocker.blocker_id} has no establishing "
                f"evidence: it is a hypothesis, not a blocker")
        self.blockers[blocker.blocker_id] = blocker

    def _active(self) -> dict:
        return {bid: b for bid, b in self.blockers.items()
                if not b.repaired}

    def minimal_blocking_sets(self) -> tuple:
        """Minimal blocking sets among the ACTIVE blockers: any set that
        strictly contains another is not minimal."""
        active = self._active()
        live = [s for s in self.blocking_sets
                if s and all(bid in active for bid in s)]
        minimal = []
        for s in live:
            if not any(t < s for t in live if t != s):
                minimal.append(s)
        return tuple(sorted(minimal, key=lambda s: (len(s), sorted(s))))

    def is_blocked(self) -> bool:
        return len(self.minimal_blocking_sets()) > 0

    def established_blockers(self) -> tuple:
        return tuple(sorted(self._active()))

    def apply_intervention(self, blocker_id: str,
                           witness: EvidenceEvent) -> tuple:
        """Attempt to repair one blocker. Returns
        (repair_recognized, still_blocked, note).

        The repair is recognized ONLY when a witness event is supplied
        and authenticates; a flag flip without evidence is refused. The
        workflow staying blocked afterwards is reported plainly — a
        valid repair is never mislabeled as completion.
        """
        blocker = self.blockers.get(blocker_id)
        if blocker is None:
            return (False, self.is_blocked(),
                    f"unknown blocker {blocker_id}: no repair recorded")
        if blocker.repaired:
            return (False, self.is_blocked(),
                    f"{blocker_id} already repaired: no duplicate credit")
        ok, reason = authenticate(witness)
        if not ok:
            return (False, self.is_blocked(),
                    f"repair of {blocker_id} refused: witness "
                    f"{witness.event_id} failed authentication ({reason})")
        blocker.repaired = True
        blocker.repair_witness = witness.event_id
        self._intervention_log.append(
            (blocker_id, witness.event_id))
        still_blocked = self.is_blocked()
        if still_blocked:
            remaining = [sorted(s) for s in
                         self.minimal_blocking_sets()]
            note = (f"valid repair of {blocker_id} recognized; workflow "
                    f"remains blocked by {remaining}: this is a partial "
                    f"repair, not completion")
        else:
            note = (f"valid repair of {blocker_id} recognized; no "
                    f"blocking set remains active")
        return (True, still_blocked, note)

    def intervention_log(self) -> tuple:
        return tuple(self._intervention_log)


# ---------------------------------------------------------------------------
# Dimension 4 — Causal state. Hypotheses as competing revisable claims:
# mechanism, contribution type, relationships, next discriminating test.
# Unresolved hypothesis != false. Unresolved hypotheses never promote to
# verified lessons. Reported fault != verified responsibility.
# ---------------------------------------------------------------------------


@dataclass
class Hypothesis:
    """One competing causal hypothesis.

    status: supported / refuted / unresolved. Unresolved hypotheses are
        preserved (never deleted, never silently dropped) and can never
        be promoted to verified lessons.
    next_discriminating_test: the test that would distinguish this
        hypothesis from its competitors.
    """
    hypothesis_id: str
    mechanism: str
    contribution_type: str
    relates_to: tuple = ()          # blocker/proposition ids
    competing_with: tuple = ()
    next_discriminating_test: str = ""
    status: str = "unresolved"

    def __post_init__(self):
        assert self.contribution_type in CONTRIBUTION_TYPES, \
            self.contribution_type
        assert self.status in HYPOTHESIS_STATUSES, self.status

    def promote_to_verified_lesson(self) -> None:
        """FORBIDDEN for unresolved hypotheses. The module refuses the
        promotion mechanically — a test asserts this raises."""
        if self.status != "supported":
            raise PermissionError(
                f"hypothesis {self.hypothesis_id} is {self.status}: "
                f"unresolved hypotheses never promote to verified lessons")
        # Even supported hypotheses promote through a separate governed
        # path, not here. This method exists to make the refusal loud.
        raise PermissionError(
            f"hypothesis {self.hypothesis_id}: promotion to verified "
            f"lesson is not available from the incident fixture")


@dataclass
class DiscriminatingTestResult:
    """One discriminating test run. A test earns credit for verified
    uncertainty reduction even when it repairs nothing."""
    test_id: str
    distinguished: tuple = ()       # hypothesis ids this test resolves
    uncertainty_reduced: int = 0    # count of claims moved off UNDETERMINED
    repaired_blocker: str = ""      # "" when the test repaired nothing


# ---------------------------------------------------------------------------
# The incident verdict: four dimensions, never collapsed into a single
# failure_reason. Note the deliberate absence: there is NO failure_reason
# field. The one who wants a single confident explanation must compute it
# from evidence — and this module refuses to do it for them.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncidentVerdict:
    """Everything the independent analyzer used and produced.

    completion_declared is True ONLY when no blocking set remains AND
    completion evidence is supplied. Partial repair never yields True.
    """
    incident_id: str
    blockers_established: tuple
    blockers_repaired: tuple
    is_blocked: bool
    minimal_blocking_sets: tuple
    unobservable_scopes: tuple
    claim_verdicts: tuple            # (proposition_id, verdict) pairs
    unresolved_hypotheses: tuple
    completion_declared: bool
    discriminating_tests: tuple      # next tests that would distinguish
    uncertainty_reduced: int
    reasons: tuple

    def render(self) -> str:
        parts = []
        n = len(self.blockers_established)
        parts.append(f"{n} blocker{'s' if n != 1 else ''} established")
        if self.blockers_repaired:
            parts.append(
                f"{len(self.blockers_repaired)} repair(s) recognized: "
                f"{', '.join(self.blockers_repaired)}")
        m = len(self.unobservable_scopes)
        parts.append(f"{m} interval{'s' if m != 1 else ''} unobservable")
        k = len(self.unresolved_hypotheses)
        parts.append(
            f"{k} explanation{'s' if k != 1 else ''} unresolved")
        if self.is_blocked:
            parts.append(
                "workflow remains blocked: this is a partial repair, "
                "not completion")
        elif self.completion_declared:
            parts.append("completion declared on full evidence")
        else:
            parts.append(
                "not enough evidence to declare completion")
        if self.blockers_established and not self.completion_declared:
            parts.append(
                "enough evidence to repair established problems; not "
                "enough to assign a sole cause or declare completion")
        return ". ".join(parts) + "."


@dataclass
class Incident:
    """One incident: four independent dimensions bound to one evidence
    pool. Conclusions are recomputed from the evidence every time —
    never stored, never stale."""
    incident_id: str
    scopes: tuple = ()
    evidence: EvidenceState = field(default_factory=EvidenceState)
    blockers: BlockerGraph = field(default_factory=BlockerGraph)
    hypotheses: tuple = ()
    interventions: tuple = ()       # DiscriminatingTestResult records
    completion_evidence: tuple = ()  # D30 event ids of completion proof

    def unresolved(self) -> tuple:
        return tuple(h for h in self.hypotheses
                     if h.status == "unresolved")


class IncidentAnalyzer:
    """The independent analyzer. Construct it fresh, hand it an incident,
    and it recomputes the verdict from the evidence alone. It never
    emits a failure_reason — that field does not exist."""

    def verdict(self, incident: Incident) -> IncidentVerdict:
        reasons = []
        active = incident.blockers.established_blockers()
        repaired = tuple(sorted(
            b.blocker_id for b in incident.blockers.blockers.values()
            if b.repaired))
        mbs = incident.blockers.minimal_blocking_sets()
        reasons.append(
            f"blocker dimension: {len(active)} established "
            f"({', '.join(active) if active else 'none'}), "
            f"{len(mbs)} minimal blocking set(s)")

        unobs = tuple(s.scope_id for s in incident.scopes
                      if s.observability == "UNOBSERVED")
        conflicted = tuple(s.scope_id for s in incident.scopes
                           if s.observability == "CONFLICTED_COVERAGE")
        reasons.append(
            f"observability dimension: {len(unobs)} unobserved, "
            f"{len(conflicted)} conflicted-coverage")

        claim_verdicts = []
        for pid in incident.evidence.propositions:
            v, why = incident.evidence.verdict_of(pid)
            claim_verdicts.append((pid, v))
            reasons.append(f"evidence dimension: {pid} -> {v} ({why})")

        unresolved = incident.unresolved()
        reasons.append(
            f"causal dimension: {len(unresolved)} unresolved "
            f"hypothesis/hypotheses "
            f"({', '.join(h.hypothesis_id for h in unresolved)
                         if unresolved else 'none'}) — preserved, "
            f"never promoted")

        # Completion: only when nothing blocks AND completion evidence
        # authenticates. Partial repair never completes.
        blocked = incident.blockers.is_blocked()
        completion_ok = (not blocked and incident.completion_evidence
                         and all(incident.evidence.authenticated(e)
                                 for e in incident.completion_evidence))
        completion_declared = bool(completion_ok)
        if blocked:
            reasons.append(
                "completion refused: blocking sets remain active")
        elif incident.completion_evidence and not completion_ok:
            reasons.append(
                "completion refused: completion evidence missing or "
                "unauthenticated")
        elif completion_declared:
            reasons.append(
                "completion declared: no blocking set active and "
                "completion evidence authenticated")

        tests = tuple(h.next_discriminating_test for h in unresolved
                      if h.next_discriminating_test)
        # De-duplicate while preserving order.
        seen, discriminating = set(), []
        for t in tests:
            if t not in seen:
                seen.add(t)
                discriminating.append(t)
        uncertainty_reduced = sum(
            t.uncertainty_reduced for t in incident.interventions)

        return IncidentVerdict(
            incident_id=incident.incident_id,
            blockers_established=active,
            blockers_repaired=repaired,
            is_blocked=blocked,
            minimal_blocking_sets=tuple(tuple(sorted(s)) for s in mbs),
            unobservable_scopes=unobs + conflicted,
            claim_verdicts=tuple(claim_verdicts),
            unresolved_hypotheses=tuple(h.hypothesis_id
                                        for h in unresolved),
            completion_declared=completion_declared,
            discriminating_tests=tuple(discriminating),
            uncertainty_reduced=uncertainty_reduced,
            reasons=tuple(reasons))


def recompute(incident: Incident) -> IncidentVerdict:
    """Conclusions recomputed through the evidence-support sets. Call
    this after any evidence change; never reuse a stale verdict."""
    return IncidentAnalyzer().verdict(incident)


# ---------------------------------------------------------------------------
# Serialization: the cold-successor path. A fresh analyzer rebuilds the
# incident from versioned bytes alone and must reproduce the verdict.
# ---------------------------------------------------------------------------

_FORMAT_VERSION = "d31-incident-v1"


def serialize_incident(incident: Incident) -> bytes:
    # The evidence pool travels with the incident as versioned bytes:
    # a cold successor must reproduce the verdict FROM the evidence,
    # so the evidence itself is part of the artifact. D30's canonical
    # trace serialization is reused — no second event format.
    pool_blob = serialize_trace(CausalTrace(
        trace_id=incident.incident_id,
        events=tuple(incident.evidence._event_pool.values()),
        edges=())).hex()
    payload = {
        "format": _FORMAT_VERSION,
        "incident_id": incident.incident_id,
        "evidence_pool": pool_blob,
        "scopes": [dataclasses.asdict(s) for s in incident.scopes],
        "propositions": [
            {"proposition_id": p.proposition_id,
             "statement": p.statement,
             "supporting_evidence": list(p.supporting_evidence),
             "refuting_evidence": list(p.refuting_evidence),
             "origin_of": dict(p.origin_of)}
            for p in incident.evidence.propositions.values()
        ],
        "blockers": [
            {"blocker_id": b.blocker_id,
             "description": b.description,
             "condition": b.condition,
             "established_by": list(b.established_by),
             "repaired": b.repaired,
             "repair_witness": b.repair_witness}
            for b in incident.blockers.blockers.values()
        ],
        "blocking_sets": [sorted(s)
                           for s in incident.blockers.blocking_sets],
        "hypotheses": [dataclasses.asdict(h)
                       for h in incident.hypotheses],
        "interventions": [dataclasses.asdict(t)
                          for t in incident.interventions],
        "completion_evidence": list(incident.completion_evidence),
    }
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def deserialize_incident(blob: bytes) -> Incident:
    payload = json.loads(blob.decode("utf-8"))
    assert payload["format"] == _FORMAT_VERSION, payload.get("format")
    evidence = EvidenceState()
    for e in deserialize_trace(
            bytes.fromhex(payload["evidence_pool"])).events:
        evidence.add_event(e)
    for p in payload["propositions"]:
        evidence.add_proposition(ClaimProposition(
            proposition_id=p["proposition_id"],
            statement=p["statement"],
            supporting_evidence=tuple(p["supporting_evidence"]),
            refuting_evidence=tuple(p["refuting_evidence"]),
            origin_of=dict(p["origin_of"])))
    graph = BlockerGraph(
        blocking_sets=tuple(payload["blocking_sets"]))
    for b in payload["blockers"]:
        graph.add_blocker(Blocker(
            blocker_id=b["blocker_id"],
            description=b["description"],
            condition=b["condition"],
            established_by=tuple(b["established_by"]),
            repaired=b["repaired"],
            repair_witness=b["repair_witness"]))
    return Incident(
        incident_id=payload["incident_id"],
        scopes=tuple(ObservationScope(**s)
                     for s in payload["scopes"]),
        evidence=evidence,
        blockers=graph,
        hypotheses=tuple(Hypothesis(**h)
                         for h in payload["hypotheses"]),
        interventions=tuple(DiscriminatingTestResult(**t)
                            for t in payload["interventions"]),
        completion_evidence=tuple(payload["completion_evidence"]))


def cold_successor_reproduces(incident: Incident) -> tuple:
    """A cold successor — fresh analyzer, versioned bytes only, no warm
    objects — must reproduce the original verdict exactly."""
    original = IncidentAnalyzer().verdict(incident)
    rebuilt = IncidentAnalyzer().verdict(
        deserialize_incident(serialize_incident(incident)))
    same = (
        rebuilt.blockers_established == original.blockers_established
        and rebuilt.is_blocked == original.is_blocked
        and rebuilt.unresolved_hypotheses
        == original.unresolved_hypotheses
        and rebuilt.completion_declared == original.completion_declared
        and rebuilt.claim_verdicts == original.claim_verdicts)
    return same, (
        f"original blocked={original.is_blocked} "
        f"completion={original.completion_declared} "
        f"unresolved={original.unresolved_hypotheses} | "
        f"rebuilt blocked={rebuilt.is_blocked} "
        f"completion={rebuilt.completion_declared} "
        f"unresolved={rebuilt.unresolved_hypotheses}")
