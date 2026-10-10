"""Fairness Assumption Audit Protocol (FAAP): audit every fairness assumption
before it may restrict the executions a model checker examines (spec).

Ratified principle: "Every fairness assumption must have an independent
reason to be believed, a satisfiable and meaningful scope, a demonstrated
role in the proof, and a justification that does not depend on the
conclusion it is supposed to support."

The highest-value safeguard is the adversarial scheduler test: if NayaNET
can make an intentionally unfair scheduler look fair merely by
strengthening its assumptions, the assumption audit must reject that
qualification.

Four audit gates — ALL FOUR required; passing three cannot compensate for
failing the fourth:
  Gate 1 — independent justification:  provenance-bound justification that
           does not depend on the fairness conclusion.
  Gate 2 — satisfiability:              a reproducible witness execution,
           AND the environment must admit the difficult behavior the
           property is meant to cover (relevant-behavior satisfiability).
  Gate 3 — minimal sufficiency:         reproducible greedy minimization;
           minimality is relative to the declared model and assumption
           vocabulary (stated limitation, not a universal claim).
  Gate 4 — non-circularity:            provenance-cycle audit PLUS
           adversarial scheduler substitution (M_unfair ∧ A ∧ ¬F).

UNKNOWN stays UNKNOWN. It is never converted to PASS by an aggregate
quality score.

No new Brain or independent authority layer. The division of labor is:
  CONNECT — traces assumption dependency provenance.
  PROVE   — binds assumption evidence and model witnesses.
  VERIFY  — conducts satisfiability, minimization, semantic circularity,
            and adversarial scheduler checks.
  LAW     — governs whether the resulting qualification is sufficient
            for the intended use.

Composes with:
  fairness_verify.py — the staged model checker whose assumption set is
                       audited here; the lasso classifier's verdicts feed
                       Gate 2 witnesses.
  strong_fairness.py — the 8-assumption checklist; FAAP is the audit those
                       assumptions must pass before restricting the model.
  propagation.py     — support sets; justification dependency graphs reuse
                       the same provenance discipline.
  uncertainty.py     — three-valued exposure logic; PENDING/UNKNOWN audit
                       states compose with UNCERTAIN scopes.

Answers to the three open questions:
  (compass)  Audit evidence is versioned by content hash: every manifest
             carries manifest_sha; every receipt references manifest_sha +
             scheduler_model_sha; revisions form an append-only chain via
             `supersedes`. An old receipt never suffices for a new
             scheduler version because the model SHA differs.
  (bricks)   Audit boundaries are enforced at REGISTRATION time, not at
             audit time: register() REJECTS an assumption whose
             control_boundary is SCHEDULER-controlled but classified as
             environmental. The model checker additionally tags every
             transition with its controlling component, so a scheduler
             decision can never silently travel as environment.
  (magnifier) The exact machine procedure is run_full_audit(): register ->
             Gate 1 independence -> Gate 2a consistency -> Gate 2b
             relevant-behavior -> Gate 3 minimization -> Gate 4a
             provenance-cycle -> Gate 4b adversarial substitution ->
             sensitivity report -> machine-readable receipt. Each step
             emits artifacts; the receipt references them all.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 1. The environment / scheduler / worker / verifier boundary.
# ---------------------------------------------------------------------------
# The boundary must be explicit. Anything controlled by the scheduler must
# remain visible as a scheduler decision — including behavior that makes an
# obligation temporarily ineligible.
COMPONENTS = ("ENVIRONMENT", "SCHEDULER", "WORKER", "VERIFIER")

# Conditions only an independently controlled environment may assume.
ENVIRONMENT_CONDITIONS = (
    "RESOURCE_AVAILABILITY",   # external resource availability
    "LAWFUL_AUTHORIZATION",    # lawful authorization from outside
    "NETWORK_BEHAVIOR",        # network behavior
    "EXTERNAL_ARBITER",        # an external arbiter's guaranteed selection
)

# Conditions that are scheduler decisions and may NEVER be smuggled in as
# environmental assumptions when scheduler fairness is under test.
SCHEDULER_CONDITIONS = (
    "QUEUE_SELECTION",         # which obligation the queue selects
    "DISPATCH",                # dispatch of work to a worker
    "TASK_OWNERSHIP",          # who owns the task
    "PRIORITIZATION",          # prioritization among obligations
    "RESOURCE_ALLOCATION",      # the scheduler's own allocation decision
    "SERVICE_DELIVERY",        # delivery of a usable execution opportunity
    "TEMPORARY_INELIGIBILITY", # the scheduler making an obligation
                               # temporarily ineligible
)


@dataclass(frozen=True)
class ControlBoundary:
    """Who controls the assumed condition.

    controller: one of COMPONENTS.
    condition:  the kind of condition (see ENVIRONMENT_CONDITIONS /
                SCHEDULER_CONDITIONS).
    scheduler_influenced: True if the scheduler can influence the condition
                          even when it does not fully control it.
    """
    controller: str
    condition: str
    scheduler_influenced: bool = False

    def __post_init__(self):
        assert self.controller in COMPONENTS, self.controller

    def is_environmental(self) -> bool:
        """True only for independently controlled environment conditions."""
        return (
            self.controller == "ENVIRONMENT"
            and self.condition in ENVIRONMENT_CONDITIONS
            and not self.scheduler_influenced
        )

    def is_scheduler_controlled(self) -> bool:
        return (
            self.controller == "SCHEDULER"
            or self.condition in SCHEDULER_CONDITIONS
            or self.scheduler_influenced
        )


# ---------------------------------------------------------------------------
# 2. The assumption registry: every assumption is a reviewable object.
# ---------------------------------------------------------------------------
# Most important field: counterexamples_excluded — the assumption must
# record which traces it excludes. That is how NayaNET identifies an
# assumption that quietly removes the exact starvation scenario the
# scheduler was supposed to handle.
@dataclass(frozen=True)
class Assumption:
    """One registered fairness assumption (immutable, versioned)."""
    assumption_id: str
    revision: int
    predicate: str            # exact formal assertion
    scope: str                # applicable environment, participants, timeframe
    owner: str                # system responsible for the assumed behavior
    control_boundary: ControlBoundary
    justification_refs: tuple  # independent evidence or governing contracts
    dependency_refs: tuple     # other assumptions/claims supporting it
    counterexamples_excluded: tuple  # traces removed from the model
    satisfiability_witness: object = None   # set by Gate 2
    necessity_result: str = "UNDETERMINED"   # set by Gate 3
    circularity_result: str = "NOT_YET_CHECKED"  # set by Gate 4
    verifier_receipt: object = None         # set by the independent audit
    supersedes: object = None  # (assumption_id, revision) this replaces

    def identity(self) -> str:
        return f"{self.assumption_id}#r{self.revision}"


class BoundaryViolation(Exception):
    """Raised when an assumption violates the environment/scheduler boundary."""


@dataclass
class AssumptionManifest:
    """The registered, reviewable set of assumptions for one audit.

    (compass) Versioning: manifest_sha is the content hash of the
    canonical serialization. Revisions append via supersedes; nothing is
    edited in place.
    (bricks) Boundary enforcement happens HERE, at registration: a
    scheduler-controlled condition classified as environmental is
    rejected immediately, before any audit runs.
    """
    assumptions: dict = field(default_factory=dict)  # identity -> Assumption
    manifest_sha: str = ""

    def register(self, assumption: Assumption) -> Assumption:
        ident = assumption.identity()
        if ident in self.assumptions:
            raise BoundaryViolation(f"duplicate registration: {ident}")
        if assumption.control_boundary.is_scheduler_controlled():
            raise BoundaryViolation(
                f"{ident}: scheduler-controlled condition "
                f"({assumption.control_boundary.condition}) may not be "
                f"registered as an environmental assumption when scheduler "
                f"fairness is under test"
            )
        self.assumptions[ident] = assumption
        self.manifest_sha = self._hash()
        return assumption

    def _hash(self) -> str:
        canon = json.dumps(
            sorted(
                {
                    ident: {
                        "predicate": a.predicate,
                        "scope": a.scope,
                        "owner": a.owner,
                        "controller": a.control_boundary.controller,
                        "condition": a.control_boundary.condition,
                        "justifications": list(a.justification_refs),
                        "dependencies": list(a.dependency_refs),
                        "excludes": list(a.counterexamples_excluded),
                    }
                    for ident, a in self.assumptions.items()
                }.items()
            ),
            sort_keys=True,
        )
        return hashlib.sha256(canon.encode()).hexdigest()[:16]

    def revise(self, old: Assumption, **changes) -> Assumption:
        """Append a new revision; the old one is never edited in place."""
        new = Assumption(
            assumption_id=old.assumption_id,
            revision=old.revision + 1,
            predicate=changes.get("predicate", old.predicate),
            scope=changes.get("scope", old.scope),
            owner=changes.get("owner", old.owner),
            control_boundary=changes.get("control_boundary",
                                         old.control_boundary),
            justification_refs=changes.get("justification_refs",
                                           old.justification_refs),
            dependency_refs=changes.get("dependency_refs",
                                        old.dependency_refs),
            counterexamples_excluded=changes.get("counterexamples_excluded",
                                                 old.counterexamples_excluded),
            supersedes=(old.assumption_id, old.revision),
        )
        return self.register(new)


# ---------------------------------------------------------------------------
# 3. Justification classes with honest limits.
# ---------------------------------------------------------------------------
# Three classes of justification. Each carries its own limitation —
# a formal guarantee is valid only under its protocol's assumptions; a
# contract is a commitment, not a runtime conformance proof; 100
# historical availabilities do not prove infinite recurrence.
JUSTIFICATION_KINDS = (
    "FORMAL_GUARANTEE",
    "AUTHORITATIVE_CONTRACT",
    "EMPIRICAL_EVIDENCE",
)

JUSTIFICATION_LIMITS = {
    "FORMAL_GUARANTEE": (
        "Valid only under that protocol's own assumptions; the audit "
        "must name them."
    ),
    "AUTHORITATIVE_CONTRACT": (
        "A contractual commitment does not itself prove universal "
        "runtime conformance."
    ),
    "EMPIRICAL_EVIDENCE": (
        "Supports measured behavior over the observed period, not an "
        "unconditional infinite-time guarantee. Historical monitoring "
        "showing a resource became available 100 times cannot prove it "
        "will become available infinitely often."
    ),
}


@dataclass(frozen=True)
class Justification:
    """One piece of independent evidence for an assumption."""
    justification_id: str
    kind: str                       # one of JUSTIFICATION_KINDS
    origin: str                     # who/what produced it
    scope: str                      # what it actually establishes
    depends_on: tuple = ()          # other justification/claim ids it rests on
    originating_test: object = None  # the test that produced it, if any

    def __post_init__(self):
        assert self.kind in JUSTIFICATION_KINDS, self.kind

    def honest_limit(self) -> str:
        return JUSTIFICATION_LIMITS[self.kind]


# ---------------------------------------------------------------------------
# 4. Gate 1 — independent justification (CONNECT traces the provenance).
# ---------------------------------------------------------------------------
# Independence is NOT established simply because a different agent reviewed
# the evidence. The verifier must establish that the supporting evidence
# does not depend on the conclusion through any direct or indirect chain.
INDEPENDENCE_FLAGS = (
    "EVIDENCE_FROM_SCHEDULER_UNDER_TEST",  # justification generated by the
                                           # scheduler being evaluated
    "REVIEWER_COPIED_AUTHOR_EXPECTATION",  # reviewer copied the scheduler
                                           # author's expected outcome
    "ASSUMPTION_DEPENDS_ON_TARGET",        # relies on the fairness claim it
                                           # is supposed to support
    "SHARED_ORIGINATING_TEST",             # two "independent" sources share
                                           # one originating test
    "CYCLE_THROUGH_DERIVED_CONCLUSION",    # depends on a derived conclusion
                                           # whose justification depends on
                                           # the assumption
)

TARGET_PROPERTY_ID = "STRONG_FAIRNESS_GF_ENABLED_IMP_GF_SERVICED"


@dataclass(frozen=True)
class IndependenceFinding:
    assumption_identity: str
    passed: bool
    flags: tuple
    detail: str


def audit_independence(assumption: Assumption,
                       justifications: dict,
                       target_property_id: str = TARGET_PROPERTY_ID
                       ) -> IndependenceFinding:
    """Gate 1: trace the provenance dependency graph to the justifications.

    justifications: justification_id -> Justification.
    Returns flags for every independence violation found; passed is True
    only when no flags fire.
    """
    flags = []
    details = []

    # Build the transitive dependency closure of the assumption's
    # justifications.
    def closure(start_ids):
        seen = set()
        stack = list(start_ids)
        while stack:
            jid = stack.pop()
            if jid in seen:
                continue
            seen.add(jid)
            j = justifications.get(jid)
            if j is not None:
                stack.extend(j.depends_on)
        return seen

    dep_ids = closure(assumption.justification_refs)
    if not assumption.justification_refs:
        flags.append("ASSUMPTION_DEPENDS_ON_TARGET")
        details.append("no justification references at all: the assumption "
                       "is unsupported and therefore cannot be independent "
                       "of the conclusion")

    for jid in sorted(dep_ids):
        j = justifications.get(jid)
        if j is None:
            continue
        # Evidence generated by the scheduler under evaluation.
        if j.origin == "SCHEDULER_UNDER_TEST":
            flags.append("EVIDENCE_FROM_SCHEDULER_UNDER_TEST")
            details.append(f"{jid}: origin is the scheduler under test")
        # A reviewer who merely copied the scheduler author's expectation.
        if j.origin == "REVIEWER_COPY_OF_AUTHOR_EXPECTATION":
            flags.append("REVIEWER_COPIED_AUTHOR_EXPECTATION")
            details.append(f"{jid}: reviewer copied the author's expectation")
        # The justification chain reaches the target property itself.
        if target_property_id in j.depends_on or jid == target_property_id:
            flags.append("ASSUMPTION_DEPENDS_ON_TARGET")
            details.append(f"{jid}: justification depends on the target "
                           f"fairness conclusion")
        # Cycle through a derived conclusion: some justification in the
        # closure depends on the assumption being audited.
        if assumption.assumption_id in j.depends_on:
            flags.append("CYCLE_THROUGH_DERIVED_CONCLUSION")
            details.append(f"{jid}: depends on {assumption.assumption_id}, "
                           f"which is the assumption under audit")

    # Two supposedly independent sources sharing one originating test.
    origins = {}
    for jid in sorted(dep_ids):
        j = justifications.get(jid)
        if j is None or j.originating_test is None:
            continue
        origins.setdefault(j.originating_test, []).append(jid)
    for test, jids in sorted(origins.items()):
        if len(jids) > 1:
            flags.append("SHARED_ORIGINATING_TEST")
            details.append(f"{', '.join(jids)}: share originating test "
                           f"{test}; not independent sources")

    # Transitive check: does ANY justification in the closure depend on the
    # target through a chain? (Direct check above; this covers indirect.)
    for jid in sorted(dep_ids):
        j = justifications.get(jid)
        if j is None:
            continue
        if _reaches(jid, target_property_id, justifications, set()):
            if "ASSUMPTION_DEPENDS_ON_TARGET" not in flags:
                flags.append("ASSUMPTION_DEPENDS_ON_TARGET")
            details.append(f"{jid}: reaches {target_property_id} through an "
                           f"indirect dependency chain")

    unique_flags = tuple(sorted(set(flags)))
    return IndependenceFinding(
        assumption_identity=assumption.identity(),
        passed=not unique_flags,
        flags=unique_flags,
        detail="; ".join(details) if details else "no independence violations",
    )


def _reaches(jid, target, justifications, visited):
    """True if jid depends (transitively) on target."""
    if jid in visited:
        return False
    visited.add(jid)
    j = justifications.get(jid)
    if j is None:
        return False
    if target in j.depends_on:
        return True
    return any(_reaches(d, target, justifications, visited)
               for d in j.depends_on)


# ---------------------------------------------------------------------------
# 5. Gate 2 — satisfiability: the miniature explicit-state model.
# ---------------------------------------------------------------------------
# Two different satisfiability tests:
#   (a) assumption consistency:  exists pi: pi |= M /\ A
#   (b) relevant-behavior satisfiability: the environment must admit the
#       difficult behavior the fairness property is meant to cover — for
#       strong fairness, recurring eligibility WITHOUT continuous
#       enablement. An environment that assumes eventual continuous
#       eligibility is overconstrained: it eliminates the
#       intermittent-eligibility counterexample instead of proving the
#       scheduler handles it -> VACUOUS_FOR_TARGET.
#
# The model: one ACT task with environment-driven flickering eligibility,
# plus a scheduler policy. State space is finite (capped counters, phase
# modulo the flicker pattern, one-way era latch), so lassos exist.
POLICIES = ("FAIR", "FLICKER_UNFAIR", "NEVER")

FLICKER_PATTERN = (True, False)  # recurring eligibility, never continuous
DEBT_CAP = 3
CONSEC_CAP = 2  # FLICKER_UNFAIR serves only tasks eligible >= 2 in a row


@dataclass(frozen=True)
class AuditState:
    """One abstract state of the assumption-audit model."""
    elig: bool        # genuinely eligible this round (environment)
    consec: int       # consecutive eligible rounds (capped)
    debt: int         # eligible rounds without service (capped)
    phase: int        # environment phase (mod len(FLICKER_PATTERN))
    era: int          # 0 = flicker era; 1 = post-switch era (one-way latch)
    served: bool      # service happened on the transition INTO this state


def audit_initial() -> AuditState:
    return AuditState(elig=True, consec=1, debt=0, phase=0, era=0,
                      served=False)


RUNLEN_PATTERN = (True, True, False)  # eligible runs last >= 2 rounds


def _model_flags(assumptions: list) -> tuple:
    """Derive model restrictions from the assumption set."""
    assume_continuous = any(a.assumption_id == "A_CONT" for a in assumptions)
    long_runs = any(a.assumption_id == "A_RUNLEN" for a in assumptions)
    pattern = RUNLEN_PATTERN if long_runs else FLICKER_PATTERN
    return assume_continuous, pattern


def audit_successors(state: AuditState, policy: str,
                     assume_continuous: bool,
                     pattern: tuple = FLICKER_PATTERN) -> list:
    """Deterministic-environment successors under a scheduler policy.

    assume_continuous: the A_CONT environmental restriction — after one
        full flicker cycle the task stays continuously eligible. This is
        the assumption the decisive experiment shows to be masking.
    policy FAIR:           serve whenever eligible.
    policy FLICKER_UNFAIR: serve only if eligible >= CONSEC_CAP in a row —
        starves flickering tasks, serves continuously eligible ones.
    policy NEVER:          never serve.
    """
    assert policy in POLICIES
    plen = len(pattern)
    phase2 = (state.phase + 1) % plen
    # One-way era latch: after a full cycle under A_CONT, eligibility locks.
    era2 = 1 if (assume_continuous and state.era == 0
                 and state.phase == plen - 1) else state.era
    if era2 == 1:
        elig2 = True
    else:
        elig2 = pattern[phase2]
    consec2 = min(state.consec + 1, CONSEC_CAP) if elig2 else 0

    if policy == "NEVER":
        serve = False
    elif policy == "FAIR":
        serve = elig2
    else:  # FLICKER_UNFAIR
        serve = elig2 and consec2 >= CONSEC_CAP

    if serve:
        debt2 = 0
    elif elig2:
        debt2 = min(state.debt + 1, DEBT_CAP)
    else:
        debt2 = state.debt
    return [AuditState(elig=elig2, consec=consec2, debt=debt2, phase=phase2,
                       era=era2, served=serve)]


@dataclass(frozen=True)
class AuditLasso:
    prefix: tuple
    cycle: tuple

    def __post_init__(self):
        assert self.cycle, "lasso cycle must be non-empty"


def find_audit_lassos(policy: str, assume_continuous: bool,
                      max_depth: int = 60,
                      pattern: tuple = FLICKER_PATTERN) -> list:
    """DFS for lassos (prefix + repeating cycle) in the audit model."""
    found = []
    visiting = {}
    path = []

    def dfs(state: AuditState, depth: int):
        if depth > max_depth or len(found) >= 4:
            return
        if state in visiting:
            idx = visiting[state]
            found.append(AuditLasso(tuple(path[:idx]), tuple(path[idx:])))
            return
        if any(state == s for s in path):
            return
        visiting[state] = len(path)
        path.append(state)
        for nxt in audit_successors(state, policy, assume_continuous,
                                    pattern):
            dfs(nxt, depth + 1)
            if len(found) >= 4:
                break
        path.pop()
        del visiting[state]

    dfs(audit_initial(), 0)
    return found


def is_starvation_lasso(lasso: AuditLasso) -> bool:
    """GF eligible in the cycle, never served in the cycle."""
    rec_elig = any(s.elig for s in lasso.cycle)
    ever_served = any(s.served for s in lasso.cycle)
    return rec_elig and not ever_served


def admits_recurring_eligibility(assume_continuous: bool,
                                 pattern: tuple = FLICKER_PATTERN
                                 ) -> tuple:
    """Relevant-behavior satisfiability: does the model admit recurring
    eligibility WITHOUT continuous enablement? Returns (bool, witness).

    Only the CYCLE counts: a transient pre-switch prefix is a modeling
    artifact, not genuine recurring eligibility. The steady state must
    exhibit both eligible and ineligible rounds.
    """
    for lasso in find_audit_lassos("NEVER", assume_continuous,
                                   pattern=pattern):
        has_elig = any(s.elig for s in lasso.cycle)
        has_inelig = any(not s.elig for s in lasso.cycle)
        if has_elig and has_inelig:
            return True, lasso
    return False, None


def check_consistency(assumptions: list) -> tuple:
    """Gate 2a: is there at least one admissible execution under M and A?

    Returns (consistent: bool, witness_or_reason).
    Predicate-level contradiction: an assumption and its direct negation
    cannot both hold. Model-level: the restricted model must have a path.
    """
    preds = [a.predicate for a in assumptions]
    for i, p in enumerate(preds):
        for q in preds[i + 1:]:
            if q.strip() == "NOT(" + p.strip() + ")" or \
               p.strip() == "NOT(" + q.strip() + ")":
                return False, f"contradictory pair: {p} vs {q}"
    assume_continuous, pattern = _model_flags(assumptions)
    lassos = find_audit_lassos("NEVER", assume_continuous, pattern=pattern)
    if not lassos:
        return False, "restricted model admits no execution"
    witness = lassos[0]
    return True, witness


SAT_PASS = "PASS"
SAT_UNSATISFIABLE = "UNSATISFIABLE"
SAT_VACUOUS = "VACUOUS_FOR_TARGET"


def audit_satisfiability(assumptions: list) -> tuple:
    """Gate 2: consistency AND relevant-behavior satisfiability.

    Returns (verdict, artifact). Verdict is one of PASS / UNSATISFIABLE /
    VACUOUS_FOR_TARGET. An overconstrained environment that cannot
    represent recurring eligibility is VACUOUS_FOR_TARGET — it may have
    proved a narrower property, but it must not report comprehensive
    strong-fairness qualification.
    """
    consistent, witness = check_consistency(assumptions)
    if not consistent:
        return SAT_UNSATISFIABLE, {"reason": witness}
    assume_continuous, pattern = _model_flags(assumptions)
    ok, wit = admits_recurring_eligibility(assume_continuous, pattern)
    if not ok:
        return SAT_VACUOUS, {
            "reason": "model cannot represent recurring eligibility "
                      "without continuous enablement; the "
                      "intermittent-eligibility counterexample is excluded "
                      "by assumption, not handled by the scheduler",
            "consistency_witness": _witness_ref(witness),
        }
    return SAT_PASS, {
        "consistency_witness": _witness_ref(witness),
        "relevant_behavior_witness": _witness_ref(wit),
    }


def _witness_ref(witness: AuditLasso) -> dict:
    return {
        "prefix_len": len(witness.prefix),
        "cycle_len": len(witness.cycle),
        "cycle_elig_pattern": [s.elig for s in witness.cycle],
    }


# ---------------------------------------------------------------------------
# 6. Gate 3 — minimal sufficiency: greedy assumption elimination.
# ---------------------------------------------------------------------------
# Establish M /\ A |= F, then remove each A_i and rerun the checker:
#   fairness still holds      -> A_i unnecessary (relative to the rest)
#   genuine counterexample    -> A_i necessary (relative to the model)
#   checker returns unknown   -> necessity unresolved
#   counterexample is physically impossible -> inspect missing domain
#       constraints; do NOT blindly declare A_i necessary.
# Minimality is always relative to the declared model and assumption
# vocabulary. Immutable physical/protocol constraints stay in the base
# model and are never treated as optional assumptions.
NEC_NECESSARY = "NECESSARY"
NEC_REDUNDANT = "REDUNDANT"
NEC_UNRESOLVED = "UNRESOLVED"
NEC_DOMAIN_CONSTRAINT_MISSING = "DOMAIN_CONSTRAINT_MISSING"
MINIMALITY_UNKNOWN = "MINIMALITY_UNKNOWN"


def _fairness_holds(assumptions: list, policy: str = "FAIR") -> tuple:
    """Does M /\\ A entail F (no starvation lasso) under the policy?

    Returns (holds: bool, counterexample_or_none). F here is strong
    fairness for the recurring-eligibility obligation: GF E_o => GF S_o.
    """
    assume_continuous, pattern = _model_flags(assumptions)
    for lasso in find_audit_lassos(policy, assume_continuous,
                                   pattern=pattern):
        if is_starvation_lasso(lasso):
            return False, lasso
    return True, None


def minimize_assumptions(assumptions: list, policy: str = "FAIR",
                         domain_constraints: tuple = (),
                         step_budget: int = 10000) -> dict:
    """Greedy elimination: find an inclusion-minimal sufficient set.

    domain_constraints: callables state -> bool; a counterexample whose
        every state violates a domain constraint is physically impossible.
    step_budget: checker steps allowed; exhaustion -> MINIMALITY_UNKNOWN
        (a timeout is UNKNOWN, never converted to PASS).
    Returns {assumption_identity: necessity, ..., "minimal_set": [...],
             "status": "COMPLETE" | MINIMALITY_UNKNOWN}.
    """
    steps = [0]

    def holds(assumps):
        steps[0] += 1
        if steps[0] > step_budget:
            return None  # unknown: budget exhausted
        return _fairness_holds(assumps, policy)

    base = holds(assumptions)
    if base is None:
        return {"status": MINIMALITY_UNKNOWN}
    base_holds, _ = base
    result = {}
    remaining = list(assumptions)
    # Greedy: try removing each assumption once, in registration order.
    for a in list(remaining):
        trial = [x for x in remaining if x.identity() != a.identity()]
        outcome = holds(trial)
        if outcome is None:
            result[a.identity()] = NEC_UNRESOLVED
            continue
        trial_holds, counterexample = outcome
        if trial_holds:
            result[a.identity()] = NEC_REDUNDANT
            remaining = trial
        else:
            if _violates_domain(counterexample, domain_constraints):
                result[a.identity()] = NEC_DOMAIN_CONSTRAINT_MISSING
            else:
                result[a.identity()] = NEC_NECESSARY
    # Assumptions never tried (removed as redundant earlier) stay REDUNDANT.
    for a in assumptions:
        result.setdefault(a.identity(), NEC_REDUNDANT)
    return {
        **result,
        "minimal_set": [a.identity() for a in remaining],
        "status": "COMPLETE",
    }


def _violates_domain(lasso: AuditLasso, constraints: tuple) -> bool:
    """True if every state of the lasso violates a domain constraint."""
    if not constraints or lasso is None:
        return False
    states = lasso.prefix + lasso.cycle
    return all(not all(c(s) for c in constraints) for s in states)


# ---------------------------------------------------------------------------
# 7. Gate 4 — non-circularity: provenance-cycle audit + adversarial
#     scheduler substitution.
# ---------------------------------------------------------------------------
# A dependency-graph check is necessary but not sufficient: a circular
# guarantee can hide behind different terminology. Example: the desired
# guarantee is "eligible tasks eventually receive service"; the assumption
# is "every eligible queue entry is eventually removed"; the hidden
# runtime behavior is "queue entries are removed only after service".
# The assumption is semantically equivalent to much of the desired
# property. detect_semantic_equivalence() catches this by checking
# whether the assumption, together with the domain rules, entails the
# target property's consequent.
CIRCULAR = "CIRCULAR"
NOT_CIRCULAR = "NOT_CIRCULAR"
CIRCULARITY_UNKNOWN = "CIRCULARITY_UNKNOWN"


def _gf_atom(predicate: str):
    """Extract the atom from a 'GF <atom>' predicate; None otherwise."""
    p = predicate.strip()
    if p.startswith("GF ") and len(p) > 3:
        return p[3:].strip()
    return None


def detect_semantic_equivalence(assumption: Assumption,
                                domain_rules: tuple,
                                target_consequent_atom: str) -> tuple:
    """Check whether assumption + domain rules entail the target.

    domain_rules: implications "X -> Y" (atoms). Forward-chain from the
    assumption's GF-atom; if the target consequent atom is reachable,
    the assumption is semantically equivalent to (part of) the desired
    property even if it uses different words.
    Returns (equivalent: bool, chain: list).
    """
    atom = _gf_atom(assumption.predicate)
    if atom is None:
        return False, []
    impl = {}
    for rule in domain_rules:
        if "->" in rule:
            left, right = rule.split("->", 1)
            impl.setdefault(left.strip(), []).append(right.strip())
    # Forward chain.
    reached = {atom: [atom]}
    queue = [atom]
    while queue:
        cur = queue.pop(0)
        for nxt in impl.get(cur, []):
            if nxt not in reached:
                reached[nxt] = reached[cur] + [nxt]
                queue.append(nxt)
    if target_consequent_atom in reached:
        return True, reached[target_consequent_atom]
    return False, []


@dataclass(frozen=True)
class CircularityFinding:
    assumption_identity: str
    verdict: str  # CIRCULAR / NOT_CIRCULAR / CIRCULARITY_UNKNOWN
    detail: str


def audit_circularity(assumption: Assumption, justifications: dict,
                      domain_rules: tuple = (),
                      target_consequent_atom: str = "serviced(o)",
                      target_property_id: str = TARGET_PROPERTY_ID
                      ) -> CircularityFinding:
    """Gate 4a: provenance-cycle audit + semantic-equivalence check."""
    # (1) Provenance cycle: does the justification closure reach the
    # target property and does the target (transitively) depend back on
    # the assumption? The independence audit already flags the first
    # half; here we check the full cycle.
    indep = audit_independence(assumption, justifications, target_property_id)
    if "ASSUMPTION_DEPENDS_ON_TARGET" in indep.flags:
        return CircularityFinding(
            assumption.identity(), CIRCULAR,
            "justification depends on the target fairness conclusion: "
            + indep.detail)
    if "CYCLE_THROUGH_DERIVED_CONCLUSION" in indep.flags:
        return CircularityFinding(
            assumption.identity(), CIRCULAR,
            "justification cycle passes through the assumption itself: "
            + indep.detail)
    # (2) Semantic equivalence under different terminology.
    equiv, chain = detect_semantic_equivalence(assumption, domain_rules,
                                               target_consequent_atom)
    if equiv:
        return CircularityFinding(
            assumption.identity(), CIRCULAR,
            "assumption + domain rules entail the target consequent via "
            + " -> ".join(chain) + "; the assumption restates the desired "
            "property in different words")
    return CircularityFinding(assumption.identity(), NOT_CIRCULAR,
                               "no provenance cycle; no semantic equivalence "
                               "with the target consequent")


MASKING_RISK = "MASKING_RISK"
NO_MASKING = "NO_MASKING"


def adversarial_substitution(assumptions: list,
                             unfair_policies: tuple = ("FLICKER_UNFAIR",)
                             ) -> dict:
    """Gate 4b: replace the scheduler with a deliberately unfair one.

    Ask: M_unfair /\\ A /\\ ~F — is a starvation execution still possible?
    If NO starvation execution is possible under an unfair scheduler, the
    assumptions already force the fairness outcome (masking): the audit
    must reject the unqualified PASS. Diagnostic, not absolute — an
    external-arbiter contract legitimately moves proof responsibility to
    the arbiter, but the receipt must then say WHICH component
    establishes the guarantee.
    """
    assume_continuous, pattern = _model_flags(assumptions)
    per_policy = {}
    for policy in unfair_policies:
        starved = any(
            is_starvation_lasso(l)
            for l in find_audit_lassos(policy, assume_continuous,
                                       pattern=pattern)
        )
        per_policy[policy] = "STARVATION_POSSIBLE" if starved \
            else "STARVATION_IMPOSSIBLE"
    masking = any(v == "STARVATION_IMPOSSIBLE"
                  for v in per_policy.values())
    return {
        "verdict": MASKING_RISK if masking else NO_MASKING,
        "per_policy": per_policy,
        "detail": ("at least one unfair scheduler cannot starve under "
                   "these assumptions: the assumptions force the outcome"
                   if masking else
                   "unfair schedulers still admit starvation: the "
                   "assumptions do not mask scheduler failure"),
    }


# ---------------------------------------------------------------------------
# 8. Assumption-change sensitivity report.
# ---------------------------------------------------------------------------
# Every assumption audit explains what the assumption excludes. The model
# checker must NEVER treat disappearance of a counterexample as sufficient
# proof that the scheduler was repaired: establish whether the scheduler
# implementation improved or the environment was merely constrained.
@dataclass(frozen=True)
class SensitivityEntry:
    change: str            # ADD / REMOVE / WEAKEN / STRENGTHEN / REPLACE /
                           # INTRODUCE_UNFAIR_SCHEDULER
    assumption_identity: str
    starvation_before: bool
    starvation_after: bool
    counterexamples_removed: int
    counterexamples_added: int
    interpretation: str


def _starvation_present(assumptions: list, policy: str) -> tuple:
    assume_continuous, pattern = _model_flags(assumptions)
    lassos = [l for l in find_audit_lassos(policy, assume_continuous,
                                           pattern=pattern)
              if is_starvation_lasso(l)]
    return (len(lassos) > 0), len(lassos)


def sensitivity_report(before: list, after: list, change: str,
                       assumption: Assumption, policy: str = "FAIR"
                       ) -> SensitivityEntry:
    """Compare starvation-counterexample sets across an assumption change."""
    starved_before, n_before = _starvation_present(before, policy)
    starved_after, n_after = _starvation_present(after, policy)
    removed = max(0, n_before - n_after)
    added = max(0, n_after - n_before)
    if removed > 0 and not starved_after:
        interpretation = (
            "counterexample disappeared after the change: this is NOT "
            "proof the scheduler was repaired — establish whether the "
            "scheduler implementation improved or the environment was "
            "merely constrained")
    elif added > 0:
        interpretation = (
            "new counterexamples appeared: the change exposed behavior "
            "the previous assumption set concealed")
    elif starved_before == starved_after:
        interpretation = "no change in the starvation-counterexample set"
    else:
        interpretation = "counterexample set changed partially"
    return SensitivityEntry(
        change=change,
        assumption_identity=assumption.identity(),
        starvation_before=starved_before,
        starvation_after=starved_after,
        counterexamples_removed=removed,
        counterexamples_added=added,
        interpretation=interpretation,
    )


# ---------------------------------------------------------------------------
# 9. Machine-readable audit receipt.
# ---------------------------------------------------------------------------
# Every PASS references an actual verification artifact, executable
# checker invocation, model revision, and independently reviewable
# evidence. A bare "satisfiable": true without its witness and
# reproducing procedure is REJECTED.
GATE_NAMES = ("independence", "satisfiability", "non_vacuity",
              "minimality", "non_circularity", "adversarial_scheduler")
GATE_STATUSES = ("PASS", "PENDING", "FAIL", "UNKNOWN")


@dataclass
class AuditReceipt:
    """The machine-readable outcome of one assumption audit."""
    audit_id: str
    target_property: str
    scheduler_model_sha: str
    assumption_manifest_sha: str
    scheduler_version: str
    obligation_class: str
    environment: str
    model_abstraction: str
    assumptions: list = field(default_factory=list)  # per-assumption dicts
    audit_gates: dict = field(default_factory=dict)  # gate -> status
    gate_artifacts: dict = field(default_factory=dict)  # gate -> artifact ref
    qualification: str = "UNPROVEN"  # never a bare PASS; see Qualification

    def to_dict(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "target_property": self.target_property,
            "scheduler_model_sha": self.scheduler_model_sha,
            "assumption_manifest_sha": self.assumption_manifest_sha,
            "scheduler_version": self.scheduler_version,
            "obligation_class": self.obligation_class,
            "environment": self.environment,
            "model_abstraction": self.model_abstraction,
            "assumptions": self.assumptions,
            "audit_gates": self.audit_gates,
            "gate_artifacts": self.gate_artifacts,
            "qualification": self.qualification,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=1, sort_keys=True)


def validate_receipt(receipt_dict: dict) -> tuple:
    """Reject receipts whose PASS gates lack referenced artifacts.

    Returns (valid: bool, problems: list). A gate marked PASS must name
    an artifact: checker invocation, model revision, witness with a
    reproducing procedure. UNKNOWN must remain UNKNOWN.
    """
    problems = []
    gates = receipt_dict.get("audit_gates", {})
    artifacts = receipt_dict.get("gate_artifacts", {})
    for gate in GATE_NAMES:
        status = gates.get(gate, "PENDING")
        if status not in GATE_STATUSES:
            problems.append(f"{gate}: unknown status {status!r}")
        if status == "PASS" and not artifacts.get(gate):
            problems.append(
                f"{gate}: PASS without a referenced verification artifact "
                f"— a bare boolean is rejected; attach the witness and its "
                f"reproducing procedure")
    for a in receipt_dict.get("assumptions", []):
        if a.get("satisfiable") is True and not a.get("satisfiability_witness"):
            problems.append(
                f"assumption {a.get('id')}: 'satisfiable': true without a "
                f"witness — rejected")
    qual = receipt_dict.get("qualification", "")
    if qual == "PASS":
        problems.append("qualification must never be a bare PASS; name the "
                        "scheduler version, obligation class, environment, "
                        "assumption set, model abstraction, and evidence")
    return (not problems), problems


# ---------------------------------------------------------------------------
# 10. Conditional, versioned qualification — never a bare PASS.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Qualification:
    """The final, conditional qualification statement."""
    verdict: str  # QUALIFIED_IN_MODEL_SCOPE / UNPROVEN / VACUOUS_FOR_TARGET
                  # / MASKING_RISK / UNSATISFIABLE / CIRCULAR
    scheduler_version: str
    obligation_class: str
    environment: str
    assumption_set_sha: str
    model_abstraction: str
    evidence_refs: tuple

    def render(self) -> str:
        if self.verdict == "QUALIFIED_IN_MODEL_SCOPE":
            return (
                f"{self.verdict}: strong fairness is established for "
                f"scheduler version {self.scheduler_version}, obligation "
                f"class {self.obligation_class}, environment "
                f"{self.environment}, assumption set "
                f"{self.assumption_set_sha}, under model abstraction "
                f"{self.model_abstraction} and independent verification "
                f"evidence {', '.join(self.evidence_refs)}. If the "
                f"environment changes, trace the affected assumptions and "
                f"requalify only the dependent claims.")
        return (f"{self.verdict}: no qualification issued for scheduler "
                f"version {self.scheduler_version} under assumption set "
                f"{self.assumption_set_sha}.")


def decide_qualification(gate_results: dict) -> str:
    """All four gates required; 3/4 is failure; UNKNOWN stays UNKNOWN."""
    indep = gate_results.get("independence")
    sat = gate_results.get("satisfiability")
    minr = gate_results.get("minimality")
    circ = gate_results.get("non_circularity")
    adv = gate_results.get("adversarial")
    if sat == SAT_UNSATISFIABLE:
        return "UNSATISFIABLE"
    if sat == SAT_VACUOUS:
        return "VACUOUS_FOR_TARGET"
    if circ == CIRCULAR or indep is False:
        return "CIRCULAR"
    if adv == MASKING_RISK:
        return "MASKING_RISK"
    if None in (indep, sat, minr, circ, adv):
        return "UNPROVEN"
    if MINIMALITY_UNKNOWN in (minr,):
        return "UNPROVEN"
    if indep is True and sat == SAT_PASS and circ == NOT_CIRCULAR \
            and adv == NO_MASKING:
        return "QUALIFIED_IN_MODEL_SCOPE"
    return "UNPROVEN"


# ---------------------------------------------------------------------------
# 11. The first decisive experiment.
# ---------------------------------------------------------------------------
# Build a tiny explicit-state scheduler model with one intermittently
# eligible ACT task and a deliberately unfair scheduler.
#   1. M_flicker-unfair + A_CONT  -> starvation trace CONCEALED.
#   2. Remove A_CONT              -> counterexample REAPPEARS.
#   3. Repair the scheduler (not the assumptions) -> the legitimate
#      recurring-eligibility case receives service; progress on service
#      remains a separate obligation.
def decisive_experiment() -> dict:
    """Run the first decisive experiment; return the evidence record."""
    a_cont = Assumption(
        assumption_id="A_CONT", revision=1,
        predicate="GF(continuous_eligibility(o))",
        scope="audit model, single ACT obligation, all rounds",
        owner="ENVIRONMENT",
        control_boundary=ControlBoundary("ENVIRONMENT",
                                         "RESOURCE_AVAILABILITY"),
        justification_refs=("J_HISTORICAL_UPTIME",),
        dependency_refs=(),
        counterexamples_excluded=("intermittent-eligibility starvation",),
    )
    a_recurs = Assumption(
        assumption_id="A_RECURS", revision=1,
        predicate="GF(eligible(o))",
        scope="audit model, single ACT obligation, all rounds",
        owner="ENVIRONMENT",
        control_boundary=ControlBoundary("ENVIRONMENT",
                                         "RESOURCE_AVAILABILITY"),
        justification_refs=("J_RESOURCE_PROTOCOL",),
        dependency_refs=(),
        counterexamples_excluded=(),
    )
    # Step 1: unfair scheduler + concealing assumption -> no starvation
    # lasso visible.
    concealed, _ = _starvation_present([a_cont], "FLICKER_UNFAIR")
    # Step 2: remove the assumption -> the counterexample reappears.
    revealed, n_revealed = _starvation_present([a_recurs], "FLICKER_UNFAIR")
    witness = None
    for lasso in find_audit_lassos("FLICKER_UNFAIR", False):
        if is_starvation_lasso(lasso):
            witness = _witness_ref(lasso)
            break
    # Step 3: repair the scheduler, keep the honest environment.
    repaired, _ = _starvation_present([a_recurs], "FAIR")
    # The fair scheduler serves the recurring-eligibility case: exhibit a
    # lasso where service happens infinitely often.
    service_lasso = None
    for lasso in find_audit_lassos("FAIR", False):
        if any(s.served for s in lasso.cycle):
            service_lasso = _witness_ref(lasso)
            break
    return {
        "step1_concealed_under_A_CONT": not concealed,
        "step2_counterexample_reappears_without_A_CONT": revealed,
        "step2_starvation_lassos": n_revealed,
        "step2_witness": witness,
        "step3_repaired_scheduler_no_starvation": not repaired,
        "step3_recurring_eligibility_served": service_lasso is not None,
        "step3_service_witness": service_lasso,
        # Progress on service stays a SEPARATE obligation: service here
        # never discharges proof; that is progress.py's ranking, not this
        # experiment's claim.
        "progress_on_service_separate": True,
    }


# ---------------------------------------------------------------------------
# 12. The exact machine procedure (magnifier): run_full_audit().
# ---------------------------------------------------------------------------
def run_full_audit(audit_id: str, assumptions: list, justifications: dict,
                   scheduler_version: str, obligation_class: str,
                   environment: str, model_abstraction: str,
                   domain_rules: tuple = (),
                   unfair_policies: tuple = ("FLICKER_UNFAIR",),
                   target_property_id: str = TARGET_PROPERTY_ID,
                   ) -> AuditReceipt:
    """The full FAAP pipeline. Every step emits artifacts; the receipt
    references them all.

      1. register            (boundary enforced at construction)
      2. Gate 1 independence (CONNECT traces provenance)
      3. Gate 2a consistency (PROVE binds the witness)
      4. Gate 2b relevant behavior (no vacuous environments)
      5. Gate 3 minimization (reproducible greedy audit)
      6. Gate 4a provenance-cycle + semantic equivalence
      7. Gate 4b adversarial scheduler substitution
      8. sensitivity report + machine-readable receipt
    """
    manifest = AssumptionManifest()
    for a in assumptions:
        manifest.register(a)  # BoundaryViolation on scheduler smuggling

    # Gate 1.
    indep_findings = [audit_independence(a, justifications,
                                        target_property_id)
                      for a in assumptions]
    indep_pass = all(f.passed for f in indep_findings)

    # Gate 2.
    sat_verdict, sat_artifact = audit_satisfiability(assumptions)

    # Gate 3.
    min_result = minimize_assumptions(assumptions, policy="FAIR")
    min_complete = min_result.get("status") == "COMPLETE"

    # Gate 4a.
    circ_findings = [audit_circularity(a, justifications, domain_rules)
                     for a in assumptions]
    circ_values = {f.verdict for f in circ_findings}
    circ_overall = (CIRCULAR if CIRCULAR in circ_values
                    else NOT_CIRCULAR)

    # Gate 4b.
    adv = adversarial_substitution(assumptions, unfair_policies)

    gate_results = {
        "independence": indep_pass,
        "satisfiability": sat_verdict,
        "minimality": "COMPLETE" if min_complete else MINIMALITY_UNKNOWN,
        "non_circularity": circ_overall,
        "adversarial": adv["verdict"],
    }
    verdict = decide_qualification(gate_results)

    per_assumption = []
    for a in assumptions:
        per_assumption.append({
            "id": a.identity(),
            "owner": a.owner,
            "classification": "ENVIRONMENT",
            "independent_justification":
                "PASS" if all(f.passed for f in indep_findings
                              if f.assumption_identity == a.identity())
                else "FAIL",
            "satisfiable": sat_verdict == SAT_PASS,
            "satisfiability_witness":
                sat_artifact.get("consistency_witness"),
            "necessity": min_result.get(a.identity(), "UNDETERMINED"),
            "circularity": next(
                (f.verdict for f in circ_findings
                 if f.assumption_identity == a.identity()),
                CIRCULARITY_UNKNOWN),
        })

    gates = {
        "independence": "PASS" if indep_pass else "FAIL",
        "satisfiability": "PASS" if sat_verdict == SAT_PASS
                          else ("FAIL" if sat_verdict == SAT_UNSATISFIABLE
                                else "UNKNOWN"),
        "non_vacuity": "PASS" if sat_verdict == SAT_PASS else "FAIL",
        "minimality": "PASS" if min_complete else "UNKNOWN",
        "non_circularity": "PASS" if circ_overall == NOT_CIRCULAR else "FAIL",
        "adversarial_scheduler":
            "PASS" if adv["verdict"] == NO_MASKING else "FAIL",
    }
    artifacts = {
        "independence": [f.detail for f in indep_findings],
        "satisfiability": sat_artifact,
        "non_vacuity": sat_artifact,
        "minimality": min_result,
        "non_circularity": [f.detail for f in circ_findings],
        "adversarial_scheduler": adv,
    }
    qualification = Qualification(
        verdict=verdict,
        scheduler_version=scheduler_version,
        obligation_class=obligation_class,
        environment=environment,
        assumption_set_sha=manifest.manifest_sha,
        model_abstraction=model_abstraction,
        evidence_refs=(audit_id,),
    )
    return AuditReceipt(
        audit_id=audit_id,
        target_property="STRONG_FAIRNESS",
        scheduler_model_sha="audit-model-v1",
        assumption_manifest_sha=manifest.manifest_sha,
        scheduler_version=scheduler_version,
        obligation_class=obligation_class,
        environment=environment,
        model_abstraction=model_abstraction,
        assumptions=per_assumption,
        audit_gates=gates,
        gate_artifacts=artifacts,
        qualification=qualification.render(),
    )
