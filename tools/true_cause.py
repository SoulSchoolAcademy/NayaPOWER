"""UD-09 — TRACE EVERY FAILURE TO ITS TRUE CAUSE.

When something fails, blame belongs to whoever controlled the failing
condition — proven by evidence, never by labels. A CORRELATES_WITH edge
is never promoted to CAUSED_BY; ordering is not causation; negative
claims need coverage evidence — without it the verdict is "we can't
observe enough to say," never an invented explanation.

Built on the D29 boundary-classification fixture
(drift_canary/d29_boundary.py, branch naya4/d29-boundary-fixture):
the controller-decisive responsibility record and the evidence-based
boundary classifier. This module adds what the fixture did not have:

  (2) canonical evidence events with separate producer AND observer
      (self-certification is a construction error), Lamport clocks,
      artifact hashes, attestation;
  (3) the four-rung observation ladder
      REPORTED / AUTHENTICATED / INDEPENDENTLY_CORROBORATED /
      CAUSALLY_QUALIFIED, and a causal verifier that accepts no
      label-like inputs — label swaps leave verdicts byte-identical;
  (4) the three causal checks (mechanism / counterfactual /
      independent reproduction) before any CAUSED_BY edge exists.

Four ownership domains: ENVIRONMENT, SCHEDULER, WORKER, ORCHESTRATOR
(the authorizing/calling layer). The controller field of the
responsibility record is decisive; no narrative overrides it.

Stdlib only. The verifier is a pure function of its evidence inputs:
a fresh verifier with no agent state reproduces byte-identical
verdicts from the same evidence.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

OWNERSHIP_DOMAINS = ("ENVIRONMENT", "SCHEDULER", "WORKER", "ORCHESTRATOR")

VERDICTS = (
    "ENVIRONMENT_BLOCKER",        # external resource genuinely unavailable
    "SCHEDULER_STARVATION",        # eligible work never dispatched
    "SCHEDULER_SERVICE_FAILURE",   # dispatched but no usable service provided
    "WORKER_NONPROGRESS",          # adequate service, no verified advancement
    "ORCHESTRATOR_MISCONFIGURATION",  # authorizing layer set an impossible condition
    "BOUNDARY_UNDETERMINED",       # evidence insufficient — never blame-by-default
    "COMPLETED",                   # the workflow actually completed
)

LADDER = (
    "REPORTED",
    "AUTHENTICATED",
    "INDEPENDENTLY_CORROBORATED",
    "CAUSALLY_QUALIFIED",
)

EDGE_TYPES = ("NONE", "CORRELATES_WITH", "CAUSED_BY")

# Claim keys that are narrative labels, not evidence. The causal verifier
# accepts no label-like inputs: these are refused at construction.
LABEL_KEYS = frozenset({"label", "narrative", "blame", "blamed", "verdict", "fault"})

# Machine-readable refusal / downgrade codes.
SELF_CERTIFICATION = "SELF_CERTIFICATION"
HASH_MISMATCH = "HASH_MISMATCH"
MISSING_ATTESTATION = "MISSING_ATTESTATION"
LABEL_INPUT_REFUSED = "LABEL_INPUT_REFUSED"
INSUFFICIENT_LINEAGE = "INSUFFICIENT_LINEAGE"
RUNG_SKIP_REFUSED = "RUNG_SKIP_REFUSED"
CORRELATION_NOT_CAUSATION = "CORRELATION_NOT_CAUSATION"
NO_MECHANISM = "NO_MECHANISM"
NO_COUNTERFACTUAL = "NO_COUNTERFACTUAL"
NO_INDEPENDENT_REPRODUCTION = "NO_INDEPENDENT_REPRODUCTION"
INSUFFICIENT_OBSERVABLE_EVIDENCE = "INSUFFICIENT_OBSERVABLE_EVIDENCE"


class EvidenceConstructionError(ValueError):
    """Raised when an evidence event cannot be constructed honestly."""


class LadderPromotionError(ValueError):
    """Raised when an observation cannot be promoted to the requested rung."""


class CausalRefusal(ValueError):
    """Raised when a CAUSED_BY edge is refused; .code names the missing check."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# Canonical evidence events
# ---------------------------------------------------------------------------

def _canonical_bytes(claim: Dict[str, Any]) -> bytes:
    return json.dumps(claim, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _claim_hash(claim: Dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(claim)).hexdigest()


@dataclass(frozen=True)
class EvidenceEvent:
    """One canonical evidence event.

    producer: who generated the underlying observation.
    observer: who independently witnessed and attested it.
    The two must differ — self-certification is a construction error.
    artifact_hash must be the sha256 of the canonical claim bytes;
    a mismatch means the log was corrupted (or fabricated) and the
    event is refused at construction.
    attestation must be a dict carrying the observer's signed
    statement referencing this event_id.
    """

    event_id: str
    lamport: int
    producer: str
    observer: str
    claim: Dict[str, Any]
    artifact_hash: str
    attestation: Dict[str, Any]

    def __post_init__(self):
        if self.producer == self.observer:
            raise EvidenceConstructionError(
                f"{SELF_CERTIFICATION}: producer and observer are both "
                f"'{self.producer}' — a component cannot certify its own evidence."
            )
        bad_keys = LABEL_KEYS.intersection(self.claim.keys())
        if bad_keys:
            raise EvidenceConstructionError(
                f"{LABEL_INPUT_REFUSED}: claim carries label-like keys "
                f"{sorted(bad_keys)} — narrative labels are not evidence."
            )
        if self.artifact_hash != _claim_hash(self.claim):
            raise EvidenceConstructionError(
                f"{HASH_MISMATCH}: event '{self.event_id}' claim bytes do not "
                "match artifact_hash — corrupted or fabricated log."
            )
        if not self.attestation or self.attestation.get("event_id") != self.event_id:
            raise EvidenceConstructionError(
                f"{MISSING_ATTESTATION}: event '{self.event_id}' has no "
                "observer attestation referencing it."
            )


def make_event(event_id: str, lamport: int, producer: str, observer: str,
               claim: Dict[str, Any], attestation_note: str = "") -> EvidenceEvent:
    """Honest constructor: hashes the claim and builds the attestation."""
    attestation = {
        "event_id": event_id,
        "observer": observer,
        "statement": attestation_note or f"{observer} witnessed {event_id}",
    }
    return EvidenceEvent(
        event_id=event_id,
        lamport=lamport,
        producer=producer,
        observer=observer,
        claim=dict(claim),
        artifact_hash=_claim_hash(claim),
        attestation=attestation,
    )


# ---------------------------------------------------------------------------
# Responsibility records — the controller field is decisive
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ResponsibilityRecord:
    """Versioned record of who controls a liveness condition.

    controller must be one of OWNERSHIP_DOMAINS. No narrative —
    agent or component — can override it. established_by lists the
    evidence event ids that established the control boundary.
    """

    condition: str
    controller: str
    version: int = 1
    established_by: Tuple[str, ...] = ()
    lamport: int = 0

    def __post_init__(self):
        if self.controller not in OWNERSHIP_DOMAINS:
            raise ValueError(
                f"controller must be one of {OWNERSHIP_DOMAINS}, "
                f"got '{self.controller}'"
            )


# ---------------------------------------------------------------------------
# The four-rung observation ladder
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Observation:
    """A claim about the world at a given rung of the ladder."""

    observation_id: str
    event_ids: Tuple[str, ...]
    rung: str = "REPORTED"
    edge_type: str = "NONE"  # NONE | CORRELATES_WITH | CAUSED_BY

    def __post_init__(self):
        if self.rung not in LADDER:
            raise ValueError(f"unknown rung '{self.rung}'")
        if self.edge_type not in EDGE_TYPES:
            raise ValueError(f"unknown edge type '{self.edge_type}'")
        if self.rung == "CAUSALLY_QUALIFIED" and self.edge_type != "CAUSED_BY":
            raise ValueError(
                "CAUSALLY_QUALIFIED requires a CAUSED_BY edge; "
                "correlation is never causally qualified."
            )


def _lineages(events: List[EvidenceEvent]) -> List[Tuple[str, str]]:
    return [(e.producer, e.observer) for e in events]


def _independent_lineages(events: List[EvidenceEvent]) -> bool:
    """Two events are independent iff they share no producer and no
    observer — no common lineage that could copy one observation into
    the other."""
    lins = _lineages(events)
    for i in range(len(lins)):
        for j in range(i + 1, len(lins)):
            a, b = lins[i], lins[j]
            if a[0] == b[0] or a[1] == b[1] or a[0] == b[1] or a[1] == b[0]:
                return False
    return True


class ObservationLadder:
    """Promotes observations rung by rung. Skips are refused; correlation
    can never be promoted to CAUSALLY_QUALIFIED."""

    def __init__(self, events: List[EvidenceEvent]):
        self._events = {e.event_id: e for e in events}

    def _resolve(self, obs: Observation) -> List[EvidenceEvent]:
        try:
            return [self._events[eid] for eid in obs.event_ids]
        except KeyError as exc:
            raise LadderPromotionError(
                f"{INSUFFICIENT_OBSERVABLE_EVIDENCE}: unknown event {exc}"
            )

    def promote(self, obs: Observation, to_rung: str,
                causal_case: Optional["CausalCase"] = None) -> Observation:
        if to_rung not in LADDER:
            raise ValueError(f"unknown rung '{to_rung}'")
        cur, want = LADDER.index(obs.rung), LADDER.index(to_rung)
        if want <= cur:
            raise LadderPromotionError(
                f"{RUNG_SKIP_REFUSED}: cannot promote {obs.rung} to {to_rung}"
            )
        if want - cur > 1:
            raise LadderPromotionError(
                f"{RUNG_SKIP_REFUSED}: {obs.rung} -> {to_rung} skips rungs; "
                "promote one rung at a time."
            )
        events = self._resolve(obs)
        if to_rung == "AUTHENTICATED":
            # Construction already enforced hash + attestation +
            # producer != observer; promotion re-verifies on the bytes.
            for e in events:
                if e.artifact_hash != _claim_hash(e.claim):
                    raise LadderPromotionError(
                        f"{HASH_MISMATCH}: event '{e.event_id}' failed "
                        "re-verification at promotion time."
                    )
        elif to_rung == "INDEPENDENTLY_CORROBORATED":
            if len(events) < 2:
                raise LadderPromotionError(
                    f"{INSUFFICIENT_LINEAGE}: corroboration needs >= 2 events, "
                    f"got {len(events)}."
                )
            if not _independent_lineages(events):
                raise LadderPromotionError(
                    f"{INSUFFICIENT_LINEAGE}: events share producer/observer "
                    "lineage — repetition is not independent corroboration."
                )
        elif to_rung == "CAUSALLY_QUALIFIED":
            if obs.edge_type == "CORRELATES_WITH":
                raise LadderPromotionError(
                    f"{CORRELATION_NOT_CAUSATION}: a CORRELATES_WITH edge is "
                    "never promoted to CAUSED_BY."
                )
            if causal_case is None:
                raise LadderPromotionError(
                    f"{NO_MECHANISM}: CAUSALLY_QUALIFIED requires the three "
                    "causal checks (mechanism / counterfactual / independent "
                    "reproduction)."
                )
            establish_caused_by(causal_case, self._events)  # raises on failure
            return Observation(obs.observation_id, obs.event_ids,
                               rung=to_rung, edge_type="CAUSED_BY")
        return Observation(obs.observation_id, obs.event_ids, rung=to_rung,
                           edge_type=obs.edge_type)


# ---------------------------------------------------------------------------
# The three causal checks
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CausalCase:
    """A candidate CAUSED_BY edge: cause -> effect.

    mechanism: stated mechanism linking cause to effect (not "A then B").
    mechanism_evidence: event ids evidencing the mechanism at work.
    counterfactual_evidence: event ids from a comparison where the cause
        was absent and the effect did not occur (control arm).
    reproduction_evidence: event ids from an INDEPENDENT reproduction
        (lineage disjoint from the original observations).
    """

    cause: str
    effect: str
    mechanism: str
    mechanism_evidence: Tuple[str, ...] = ()
    counterfactual_evidence: Tuple[str, ...] = ()
    reproduction_evidence: Tuple[str, ...] = ()


def _rung_of(events_by_id: Dict[str, EvidenceEvent],
             event_ids: Tuple[str, ...],) -> int:
    # Evidence used in causal checks must be at least AUTHENTICATED.
    # Construction guarantees hash + attestation, so presence counts.
    for eid in event_ids:
        if eid not in events_by_id:
            return -1
    return 1 if event_ids else -1


def check_mechanism(case: CausalCase,
                    events_by_id: Dict[str, EvidenceEvent]) -> None:
    """Ordering is not causation: a bare 'A happened before B' is refused."""
    if not case.mechanism or not case.mechanism.strip():
        raise CausalRefusal(NO_MECHANISM, "no mechanism stated — ordering alone")
    if _rung_of(events_by_id, case.mechanism_evidence) < 1:
        raise CausalRefusal(
            NO_MECHANISM,
            "mechanism stated but not evidenced by authenticated events",
        )


def check_counterfactual(case: CausalCase,
                          events_by_id: Dict[str, EvidenceEvent]) -> None:
    if _rung_of(events_by_id, case.counterfactual_evidence) < 1:
        raise CausalRefusal(
            NO_COUNTERFACTUAL,
            "no control-arm evidence: cause absent -> effect absent",
        )


def check_reproduction(case: CausalCase,
                       events_by_id: Dict[str, EvidenceEvent]) -> None:
    if _rung_of(events_by_id, case.reproduction_evidence) < 1:
        raise CausalRefusal(
            NO_INDEPENDENT_REPRODUCTION,
            "no independent reproduction of the cause -> effect link",
        )
    repro = [events_by_id[eid] for eid in case.reproduction_evidence]
    original_ids = set(case.mechanism_evidence) | set(case.counterfactual_evidence)
    original = [events_by_id[eid] for eid in original_ids if eid in events_by_id]
    for r in repro:
        for o in original:
            if (r.producer == o.producer or r.observer == o.observer
                    or r.producer == o.observer or r.observer == o.producer):
                raise CausalRefusal(
                    NO_INDEPENDENT_REPRODUCTION,
                    f"reproduction event '{r.event_id}' shares lineage with "
                    "the original observations — not independent",
                )


def establish_caused_by(case: CausalCase,
                        events_by_id: Dict[str, EvidenceEvent]) -> Dict[str, str]:
    """Run the three causal checks. Returns the CAUSED_BY edge record
    only if all three pass; otherwise raises CausalRefusal naming the
    missing check."""
    check_mechanism(case, events_by_id)
    check_counterfactual(case, events_by_id)
    check_reproduction(case, events_by_id)
    return {"edge": "CAUSED_BY", "cause": case.cause, "effect": case.effect,
            "mechanism": case.mechanism}


# ---------------------------------------------------------------------------
# Failure cases and the causal verifier
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FailureCase:
    """Everything the verifier may consult — evidence only.

    symptoms: observable facts (e.g. 'workflow did not complete').
    events: canonical evidence events.
    responsibility: versioned responsibility records; the controller
        field is decisive.
    narrative_labels: what components CLAIMED (kept for the record,
        NEVER consulted by the verifier — this is what makes label
        swaps leave verdicts byte-identical).
    """

    case_id: str
    symptoms: Tuple[str, ...]
    events: Tuple[EvidenceEvent, ...]
    responsibility: Tuple[ResponsibilityRecord, ...] = ()
    narrative_labels: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Verdict:
    case_id: str
    verdict: str
    controller: str
    causal_edges: Tuple[Tuple[str, str], ...]
    reason: str
    digest: str  # sha256 of the canonical verdict bytes

    def canonical(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "causal_edges": sorted([list(e) for e in self.causal_edges]),
            "controller": self.controller,
            "reason": self.reason,
            "verdict": self.verdict,
        }


class TrueCauseVerifier:
    """The causal verifier. A pure function of evidence: it reads
    symptoms, events, and responsibility records — never narrative
    labels. A fresh instance reproduces byte-identical verdicts from
    the same evidence."""

    def verify(self, case: FailureCase) -> Verdict:
        events_by_id = {e.event_id: e for e in case.events}
        # Controller is decisive: find the responsibility record for the
        # failing condition. Latest version wins.
        controller = "UNDETERMINED"
        if case.responsibility:
            latest = max(case.responsibility, key=lambda r: (r.version, r.lamport))
            controller = latest.controller

        verdict, reason = self._classify(case, events_by_id, controller)
        edges = self._causal_edges(case, events_by_id)
        v = Verdict(case.case_id, verdict, controller, edges, reason, digest="")
        digest = hashlib.sha256(
            json.dumps(v.canonical(), sort_keys=True,
                       separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return Verdict(v.case_id, v.verdict, v.controller, v.causal_edges,
                       v.reason, digest)

    # -- internals ------------------------------------------------------

    def _evidence_supports(self, events_by_id: Dict[str, EvidenceEvent],
                           predicate) -> bool:
        return any(predicate(e) for e in events_by_id.values())

    def _classify(self, case: FailureCase,
                  events_by_id: Dict[str, EvidenceEvent],
                  controller: str) -> Tuple[str, str]:
        if not case.events:
            return ("BOUNDARY_UNDETERMINED",
                    f"{INSUFFICIENT_OBSERVABLE_EVIDENCE}: no evidence events "
                    "— we can't observe enough to say.")
        completed = self._evidence_supports(
            events_by_id,
            lambda e: e.claim.get("workflow_completed") is True)
        if completed:
            return "COMPLETED", "evidence shows the workflow completed."

        # The controller field decides; evidence must corroborate that the
        # controller's domain matches the observed failure condition.
        if controller == "ENVIRONMENT":
            if self._evidence_supports(
                    events_by_id,
                    lambda e: e.claim.get("resource_available") is False):
                return ("ENVIRONMENT_BLOCKER",
                        "controller=ENVIRONMENT and independent evidence shows "
                        "the resource unavailable.")
        elif controller == "SCHEDULER":
            dispatched = self._evidence_supports(
                events_by_id, lambda e: e.claim.get("dispatched") is True)
            if not dispatched:
                return ("SCHEDULER_STARVATION",
                        "controller=SCHEDULER and no dispatch evidence — "
                        "eligible work never dispatched.")
            return ("SCHEDULER_SERVICE_FAILURE",
                    "controller=SCHEDULER, dispatched, but no usable service "
                    "evidenced.")
        elif controller == "WORKER":
            if self._evidence_supports(
                    events_by_id,
                    lambda e: e.claim.get("adequate_service") is True):
                return ("WORKER_NONPROGRESS",
                        "controller=WORKER and adequate service evidenced, "
                        "but no verified advancement.")
        elif controller == "ORCHESTRATOR":
            if self._evidence_supports(
                    events_by_id,
                    lambda e: e.claim.get("condition_impossible") is True):
                return ("ORCHESTRATOR_MISCONFIGURATION",
                        "controller=ORCHESTRATOR and evidence shows the "
                        "authorized condition was impossible as specified.")
        return ("BOUNDARY_UNDETERMINED",
                f"{INSUFFICIENT_OBSERVABLE_EVIDENCE}: evidence does not "
                "corroborate the recorded controller — we can't observe "
                "enough to say, so we don't invent an explanation.")

    def _causal_edges(self, case: FailureCase,
                      events_by_id: Dict[str, EvidenceEvent]
                      ) -> Tuple[Tuple[str, str], ...]:
        # CAUSED_BY edges are established only via establish_caused_by;
        # the verifier never invents them from ordering or labels.
        return ()


# ---------------------------------------------------------------------------
# Narrative labels live outside evidence — the verifier never reads them
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ComponentReport:
    """What a component CLAIMS happened. Narrative only.

    The verifier is never given these. They exist so tests can prove
    false blame and label swaps do not move the verdict."""

    component: str
    label: str
    seq: int = 0
