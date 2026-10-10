"""Causal Uncertainty Without False Blame (Shawn, 2026-10-10 — SN-0781).

EXTENSION of the causal contracts in causal_trace.py — not a competing
evidence store. Same EvidenceEvent / CausalGraph / verifier seams; this
module adds the uncertainty machinery his framework requires.

Ratified rule: never trade an accurate set of partial truths for one
confident but unsupported explanation.

Four independent dimensions, never collapsed:
  observability  — was it watched? (not observed != did not happen)
  evidence state — what do the reports establish per proposition?
  blocker state  — what currently makes progress impossible?
  causal state   — what caused the outcome? (unresolved != false)
"""

from dataclasses import dataclass, field

from causal_trace import (
    CausalGraph, EvidenceEvent,
    L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED,
    V_UNDETERMINED,
)

# ---------------------------------------------------------------------------
# Dimension 1: scoped observability claims.
# ---------------------------------------------------------------------------
OBS_COVERED_COMPLETE = "COVERED_COMPLETE"      # absence meaningful in scope
OBS_COVERED_PARTIAL = "COVERED_PARTIAL"
OBS_UNOBSERVED = "UNOBSERVED"                  # not observed != did not happen
OBS_CONFLICTED_COVERAGE = "CONFLICTED_COVERAGE"
OBS_NOT_APPLICABLE = "NOT_APPLICABLE"

OBS_STATUSES = (
    OBS_COVERED_COMPLETE, OBS_COVERED_PARTIAL, OBS_UNOBSERVED,
    OBS_CONFLICTED_COVERAGE, OBS_NOT_APPLICABLE,
)


@dataclass(frozen=True)
class ObservabilityClaim:
    """Was this watched, where, and how completely?

    Absence of an event is meaningful ONLY under COVERED_COMPLETE for
    that source/type/resource/interval. UNOBSERVED never licenses a
    "did not happen" conclusion.
    """
    source: str
    event_type: str
    resource: str
    interval: tuple            # (start_clock, end_clock)
    status: str
    sequence_continuous: bool = False
    loss_counters: tuple = ()
    collection_boundaries: tuple = ()
    snapshots: tuple = ()

    def __post_init__(self):
        assert self.status in OBS_STATUSES, self.status

    def absence_meaningful(self) -> bool:
        return (self.status == OBS_COVERED_COMPLETE
                and self.sequence_continuous)


# ---------------------------------------------------------------------------
# Dimension 2: claim-level propositions.
# ---------------------------------------------------------------------------
PROP_SUPPORTED = "SUPPORTED"
PROP_REFUTED = "REFUTED"
PROP_CONFLICTED = "CONFLICTED"
PROP_UNDETERMINED = "UNDETERMINED"
PROP_NOT_APPLICABLE = "NOT_APPLICABLE"

PROP_VERDICTS = (
    PROP_SUPPORTED, PROP_REFUTED, PROP_CONFLICTED,
    PROP_UNDETERMINED, PROP_NOT_APPLICABLE,
)

# Canonical dispatch-dispute decomposition. Reports about different
# stages must never be manufactured into contradictions.
STAGE_ISSUED = "issued"      # P1: the scheduler issued the dispatch
STAGE_REACHED = "reached"    # P2: the lease reached the worker
STAGE_ACCEPTED = "accepted"  # P3: the worker accepted it
STAGE_ATTEMPTED = "attempted"  # P4: the worker attempted the transition


@dataclass(frozen=True)
class Proposition:
    prop_id: str
    statement: str
    stage: str
    verdict: str = PROP_UNDETERMINED
    evidence_refs: tuple = ()

    def __post_init__(self):
        assert self.verdict in PROP_VERDICTS, self.verdict


def decompose_dispatch_dispute(prop_id_prefix: str,
                               events: list) -> list:
    """Decompose conflicting dispatch reports into stage-precise
    propositions P1..P4. Two logs from one event bus count as ONE
    witness (same source binding) — they do not corroborate each other.
    """
    stages = [STAGE_ISSUED, STAGE_REACHED, STAGE_ACCEPTED, STAGE_ATTEMPTED]
    statements = {
        STAGE_ISSUED: "the scheduler issued a dispatch for the obligation",
        STAGE_REACHED: "a usable lease reached the worker",
        STAGE_ACCEPTED: "the worker accepted the lease",
        STAGE_ATTEMPTED: "the worker attempted the transition",
    }
    # Group evidence by source binding: same (producer, artifact set)
    # is one witness no matter how many log lines it emitted.
    witnesses = {}
    for e in events:
        key = (e.producer, tuple(sorted(e.artifact_hashes)) or (e.event_id,))
        witnesses.setdefault(key, []).append(e)
    props = []
    for i, stage in enumerate(stages, 1):
        relevant = [e for e in events
                    if _event_supports_stage(e, stage)]
        # Distinct witness groups behind the relevant evidence.
        groups = {k for k, evs in witnesses.items()
                  if any(e in relevant for e in evs)}
        if not relevant:
            verdict = PROP_UNDETERMINED
        elif len(groups) >= 2:
            verdict = PROP_SUPPORTED
        else:
            verdict = PROP_UNDETERMINED  # one witness is not corroboration
        props.append(Proposition(
            prop_id=f"{prop_id_prefix}-P{i}",
            statement=statements[stage],
            stage=stage,
            verdict=verdict,
            evidence_refs=tuple(e.event_id for e in relevant),
        ))
    return props


def _event_supports_stage(event: EvidenceEvent, stage: str) -> bool:
    from causal_trace import (
        EV_DISPATCH, EV_DISPATCH_ACCEPTED, EV_SERVICE_DELIVERED, EV_ATTEMPT,
    )
    mapping = {
        STAGE_ISSUED: (EV_DISPATCH,),
        STAGE_REACHED: (EV_SERVICE_DELIVERED,),
        STAGE_ACCEPTED: (EV_DISPATCH_ACCEPTED,),
        STAGE_ATTEMPTED: (EV_ATTEMPT,),
    }
    return (event.event_type in mapping[stage]
            and event.observation_status in
            (L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED))

# ---------------------------------------------------------------------------
# Dimension 3: blocker algebra.
# ---------------------------------------------------------------------------
BLOCKER_ACTIVE = "ACTIVE"
BLOCKER_CLEARED = "CLEARED"          # cleared only with evidence
BLOCKER_UNASSESSED = "UNASSESSED"

BLOCKER_STATUSES = (BLOCKER_ACTIVE, BLOCKER_CLEARED, BLOCKER_UNASSESSED)


@dataclass(frozen=True)
class Blocker:
    """One currently-established impediment to progress.

    A confirmed blocker explains current impossibility — it does NOT
    prove original causality. Status changes require evidence_refs;
    assertion alone never clears a blocker.
    """
    blocker_id: str
    obligation_id: str
    condition: str
    status: str = BLOCKER_UNASSESSED
    controller: str = ""             # who controls the condition
    valid_interval: tuple = ()       # (start_clock, end_clock)
    escape_conditions: tuple = ()
    evidence_refs: tuple = ()

    def __post_init__(self):
        assert self.status in BLOCKER_STATUSES, self.status

    def cleared_with_evidence(self, evidence_refs: tuple):
        if not evidence_refs:
            raise ValueError(
                f"blocker {self.blocker_id}: assertion alone cannot clear; "
                "evidence required")
        import dataclasses
        return dataclasses.replace(self, status=BLOCKER_CLEARED,
                                   evidence_refs=tuple(evidence_refs))


@dataclass
class BlockerSet:
    """AND/OR combinations of blockers with minimal blocking sets.

    - conjunction: every member must clear before progress is possible.
    - alternative: clearing one full alternative path suffices.
    minimal_blocking_sets() returns the inclusion-minimal sets of
    blockers whose combined presence explains the stall.
    """
    blockers: list = field(default_factory=list)
    # alternatives: list of frozensets of blocker_ids; the stall is
    # explained if ANY alternative's members are all ACTIVE.
    alternatives: list = field(default_factory=list)

    def active(self) -> list:
        return [b for b in self.blockers if b.status == BLOCKER_ACTIVE]

    def is_blocked(self) -> bool:
        act = {b.blocker_id for b in self.active()}
        if not act:
            return False
        if not self.alternatives:
            return True  # conjunction: any active blocker blocks
        return any(alt <= act for alt in self.alternatives)

    def minimal_blocking_sets(self) -> list:
        """Inclusion-minimal sets of active blockers explaining the stall."""
        act = {b.blocker_id for b in self.active()}
        if not act:
            return []
        if not self.alternatives:
            return [frozenset(act)]  # conjunction: the whole set is minimal
        candidates = [frozenset(alt & act) for alt in self.alternatives
                      if alt <= act]
        # Keep only inclusion-minimal candidates.
        minimal = []
        for c in sorted(candidates, key=len):
            if not any(m < c for m in minimal):
                minimal = [m for m in minimal if not c < m]
                minimal.append(c)
        return minimal

    def repair(self, blocker_id: str, evidence_refs: tuple) -> "BlockerSet":
        """Repair one blocker (evidence required). Returns the new set.

        Repair is recognized; completion is NEVER declared here — the
        caller must re-evaluate is_blocked() on the result.
        """
        import dataclasses
        new_blockers = [
            b.cleared_with_evidence(evidence_refs) if b.blocker_id == blocker_id
            else b for b in self.blockers
        ]
        return dataclasses.replace(self, blockers=new_blockers)


# ---------------------------------------------------------------------------
# Dimension 4: hypotheses as competing revisable claims.
# ---------------------------------------------------------------------------
CAUSE_CONTRIBUTING = "contributing"
CAUSE_NECESSARY = "necessary"
CAUSE_SUFFICIENT = "sufficient"
CAUSE_POSSIBLE = "possible"

CAUSE_TYPES = (CAUSE_CONTRIBUTING, CAUSE_NECESSARY,
               CAUSE_SUFFICIENT, CAUSE_POSSIBLE)

HYP_ACTIVE = "ACTIVE"
HYP_REFINED = "REFINED"
HYP_SUPERSEDED = "SUPERSEDED"
HYP_UNRESOLVED = "UNRESOLVED"

HYP_STATUSES = (HYP_ACTIVE, HYP_REFINED, HYP_SUPERSEDED, HYP_UNRESOLVED)

REL_COMPATIBLE = "compatible"
REL_COMPETING = "competing"
REL_DEPENDENT = "dependent"
REL_UNASSESSED = "unassessed"


@dataclass
class RevisableHypothesis:
    """A causal hypothesis that stays revisable until a discriminating
    test resolves it. Unresolved hypotheses are NEVER promoted to
    verified lessons.
    """
    hypothesis_id: str
    mechanism: str
    cause_type: str = CAUSE_POSSIBLE
    supporting: tuple = ()
    challenging: tuple = ()
    gaps: tuple = ()
    relationships: dict = field(default_factory=dict)  # id -> relation
    discriminating_test: str = ""
    status: str = HYP_UNRESOLVED

    def __post_init__(self):
        assert self.cause_type in CAUSE_TYPES, self.cause_type
        assert self.status in HYP_STATUSES, self.status
        for rel in self.relationships.values():
            assert rel in (REL_COMPATIBLE, REL_COMPETING, REL_DEPENDENT,
                           REL_UNASSESSED), rel

    def refine(self, **changes) -> "RevisableHypothesis":
        """Produce a refined successor; the original is superseded, not
        edited — history of the reasoning is preserved."""
        import dataclasses
        child = dataclasses.replace(self, status=HYP_REFINED, **changes)
        self.status = HYP_SUPERSEDED
        return child


class HypothesisSet:
    """Non-mutually-exclusive branches: conjunctions (must co-hold),
    alternatives (at least one holds), unknown relationships. The
    verifier never forces an unsupported choice between live hypotheses.
    """

    def __init__(self):
        self.hypotheses = {}     # id -> RevisableHypothesis
        self.branches = []       # (kind, frozenset(ids))

    def add(self, hyp: RevisableHypothesis, branch: tuple = None):
        self.hypotheses[hyp.hypothesis_id] = hyp
        if branch is not None:
            kind, ids = branch
            assert kind in ("conjunction", "alternative", "unknown")
            self.branches.append((kind, frozenset(ids)))

    def live(self) -> list:
        return [h for h in self.hypotheses.values()
                if h.status in (HYP_ACTIVE, HYP_UNRESOLVED, HYP_REFINED)]

    def check_no_forced_choice(self) -> list:
        """Violations: a verdict that selects exactly one hypothesis
        while a competing one is still live and unassessed."""
        violations = []
        for kind, ids in self.branches:
            if kind != "alternative":
                continue
            live = [i for i in ids
                    if self.hypotheses[i].status in
                    (HYP_ACTIVE, HYP_UNRESOLVED)]
            rels = [self.hypotheses[i].relationships for i in live]
            # If any live pair is still 'unassessed', choosing between
            # them now would force an unsupported choice.
            for i in live:
                for j in live:
                    if i != j and self.hypotheses[i].relationships.get(
                            j) == REL_UNASSESSED:
                        violations.append(
                            f"unsupported choice risk: {i} vs {j} "
                            "relationship unassessed")
        return violations

# ---------------------------------------------------------------------------
# Support-set recomputation: uncertainty follows dependencies.
# ---------------------------------------------------------------------------

def recompute_support(conclusion_id: str, support_sets: list,
                      unreliable: set, evidence_sources: dict) -> dict:
    """Recompute a conclusion's support after evidence becomes unreliable.

    support_sets: list of frozensets of evidence ids; the conclusion
        holds iff ANY set is fully admissible:  H <= (E1&E2) | (E3&E4).
    unreliable: evidence ids no longer admissible.
    evidence_sources: eid -> source id (for shared-source detection).

    Returns {conclusion_id, admissible_paths, verdict} where verdict is
    SUPPORTED (a fully admissible path remains), UNDERMINED (no
    admissible path remains), or NOT_INDEPENDENT (remaining paths share
    a contaminated source — apparent independence rejected).
    """
    admissible = [s for s in support_sets if not (set(s) & unreliable)]
    if not admissible:
        return {"conclusion_id": conclusion_id,
                "admissible_paths": [],
                "verdict": "UNDERMINED",
                "note": "no fully admissible support path remains"}
    # Shared contaminated source: paths are not independent.
    contaminated_sources = {evidence_sources[e] for e in unreliable
                            if e in evidence_sources}
    for path in admissible:
        path_sources = {evidence_sources.get(e) for e in path}
        if path_sources & contaminated_sources:
            return {"conclusion_id": conclusion_id,
                    "admissible_paths": [sorted(p) for p in admissible],
                    "verdict": "NOT_INDEPENDENT",
                    "note": "remaining paths share a contaminated source; "
                            "apparent independence rejected"}
    return {"conclusion_id": conclusion_id,
            "admissible_paths": [sorted(p) for p in admissible],
            "verdict": "SUPPORTED",
            "note": "at least one fully admissible path remains"}


# ---------------------------------------------------------------------------
# Next-test selection by distinguishing power.
# ---------------------------------------------------------------------------

def select_next_test(candidates: list, live_hypotheses: list) -> dict:
    """Choose the test with the greatest distinguishing power.

    candidates: [{test_id, outcomes: {outcome: [hyp_ids eliminated]}}].
    Distinguishing power of a test = the WORST-CASE number of hypotheses
    eliminated across its outcomes (a test that might eliminate nothing
    has no distinguishing power). Ties break toward fewer outcomes
    (simpler test). Returns {test_id, distinguishing_power, note}.

    Credit is for VERIFIED uncertainty reduction. A test's mere
    performance never counts as resolution: the caller must re-run the
    hypotheses against the actual outcome before any status changes.
    """
    live = set(live_hypotheses)
    best, best_power = None, -1
    for c in candidates:
        outcomes = c.get("outcomes", {})
        if not outcomes:
            continue
        power = min(len(set(elim) & live) for elim in outcomes.values())
        if (power > best_power or
                (power == best_power and best is not None
                 and len(outcomes) < len(best["outcomes"]))):
            best, best_power = c, power
    if best is None:
        return {"test_id": None, "distinguishing_power": 0,
                "note": "no candidate test eliminates any live hypothesis"}
    return {"test_id": best["test_id"],
            "distinguishing_power": best_power,
            "note": "credit requires re-running hypotheses against the "
                    "actual outcome; test performance alone resolves nothing"}


# ---------------------------------------------------------------------------
# Machine-readable causal uncertainty record.
# ---------------------------------------------------------------------------

@dataclass
class CausalUncertaintyRecord:
    """One versioned uncertainty assessment.

    The overall_causal_verdict NEVER substitutes for the individual
    assessments: readers must consult observability, propositions,
    blockers, and hypotheses, not the headline.
    """
    record_id: str
    trace_id: str
    version: int = 1
    observability: list = field(default_factory=list)   # ObservabilityClaim
    propositions: list = field(default_factory=list)    # Proposition
    blockers: list = field(default_factory=list)        # Blocker
    causal_hypotheses: list = field(default_factory=list)  # RevisableHypothesis
    overall_causal_verdict: str = V_UNDETERMINED

    def to_dict(self) -> dict:
        import dataclasses
        return {
            "record_id": self.record_id,
            "trace_id": self.trace_id,
            "version": self.version,
            "observability": [dataclasses.asdict(o)
                              for o in self.observability],
            "propositions": [dataclasses.asdict(p)
                             for p in self.propositions],
            "blockers": [dataclasses.asdict(b) for b in self.blockers],
            "causal_hypotheses": [
                {"hypothesis_id": h.hypothesis_id,
                 "mechanism": h.mechanism,
                 "cause_type": h.cause_type,
                 "supporting": list(h.supporting),
                 "challenging": list(h.challenging),
                 "gaps": list(h.gaps),
                 "relationships": dict(h.relationships),
                 "discriminating_test": h.discriminating_test,
                 "status": h.status}
                for h in self.causal_hypotheses],
            "overall_causal_verdict": self.overall_causal_verdict,
            "verdict_disclaimer": "the overall verdict never substitutes "
                                  "for the individual assessments above",
        }

    def supersede(self) -> "CausalUncertaintyRecord":
        """Version the record: the old version is preserved, never edited."""
        import dataclasses
        return dataclasses.replace(self, version=self.version + 1)
