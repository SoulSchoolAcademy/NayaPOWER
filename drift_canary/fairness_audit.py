#!/usr/bin/env python3
"""Independent Fairness Assumption Audit Protocol — D28 (spec + machinery).

Directive D28 (directive-register wave 6, owner naya2): "the audit that
keeps fairness proofs honest: every assumption earns its place or gets
thrown out."

Four gates, all required:
  G1 INDEPENDENT_JUSTIFICATION — every assumption is JUSTIFIED by evidence
       that resolves in an independent ledger the prover does not control;
       the scheduler never assumes its own fairness; the verdict being
       audited never justifies the assumptions it rests on; a footprint
       that constrains scheduler behavior is circular by construction.
  G2 SATISFIABILITY — the assumption set, as model constraints, admits at
       least one execution of the bounded model. A set admitting nothing
       makes every qualification under it vacuously true: rejected.
  G3 MINIMAL_SUFFICIENCY — every in-scope assumption earns its place:
       removing it must change the prover's check or resurrect a starvation
       trace in the adversarial probe. Decorative assumptions are flagged
       REDUNDANT_ASSUMPTIONS (fail-closed), never silently carried.
  G4 NON_CIRCULARITY — the killer probe: two deliberately unfair schedulers
       (BROKEN_WF, BROKEN_SF) produce genuine starvation traces. If the
       assumption set deletes such a trace from the model, the deletion is
       legitimate only when the excluded behavior is NAMED in the claim's
       excluded_behaviors (explicitly outside the qualified environment)
       AND independently justified (G1). Otherwise: rejected.

Passing three gates never compensates for failing the fourth.

Relationship to existing machinery (no second mechanism):
  drift_canary/fairness_verify.py :: audit_assumption() is the PROVER's
  self-audit questionnaire — the prover answers the eight questions and
  the function reports findings. The answers are self-reported.
  THIS module is the INDEPENDENT AUDITOR: it re-runs the model checker
  itself (find_lassos), classifies with the canonical classifier
  (classify_lasso), consults an independent evidence ledger, and runs the
  killer probe. It consumes the existing machinery; it never re-implements
  it. D27 (assumption registration, PR #2295) registers assumptions; D28
  audits them. The from_d27() adapter binds the two without importing the
  unmerged D27 module (duck-typed on .id/.statement).

The killer test (from the directive): assume "the task eventually stays
continuously eligible" and the intermittent-starvation trace vanishes —
not because the scheduler was fixed, but because the test was rigged.
Remove the assumption and the counterexample comes back. The test suite
demonstrates all three movements: the rig rejected (G1), the deletion
caught even with ledgered evidence (G4), and the counterexample returning
when the assumption is removed.

Verdicts never collapse into one green PASS:
  AUDIT_PASSED | REJECTED | REDUNDANT_ASSUMPTIONS | CLAIM_NOT_ESTABLISHED.
Every verdict names its model depth: the audit's scope is explicit, and
absence of counterexamples within the bound is never a general proof.

Stdlib only. NOT wired into kernel/, KNOW, LAW, ACT, or any live path.
Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from drift_canary.fairness_verify import (
    Lasso,
    classify_lasso,
    find_lassos,
    run_broken_scheduler,
)

# ---------------------------------------------------------------------------
# Vocabulary.
# ---------------------------------------------------------------------------
AUDIT_OWNERS = ("ENVIRONMENT", "WORKER", "HUMAN_AUTHORITY")
# NOTE: "SCHEDULER" is deliberately absent. For a scheduler-fairness
# property the scheduler may not own an assumption: that is the
# circularity G1 rejects. The dataclass still accepts "SCHEDULER" so the
# audit can REJECT it with a named reason instead of crashing on input.
_INPUT_OWNERS = AUDIT_OWNERS + ("SCHEDULER",)
AUDIT_STATUSES = ("PROPOSED", "JUSTIFIED", "CHALLENGED", "REJECTED")

# Model footprints: what an assumption constrains in the abstract model,
# expressed as a filter over lasso cycles (the model's infinite
# executions in finite form). Unknown strings are fail-closed: the
# dataclass refuses them rather than silently treating them as NONE.
MODEL_CONSTRAINTS = (
    "NONE",                    # documentary; no model footprint
    "STABILIZED_ELIGIBILITY",  # keep lassos whose cycle is all-enabled
                               # ("the task eventually stays continuously
                               # eligible" — the directive's rig)
    "ELIGIBLE_IFF_SERVICED",   # keep lassos where enabled == serviced in
                               # every cycle state (constrains scheduler
                               # behavior: circular by construction)
    "CONTRADICTORY",           # keeps nothing (negative control for G2)
)

# Which footprint constrains whose behavior. An ENVIRONMENT-domain
# footprint may be owned by ENVIRONMENT/HUMAN_AUTHORITY. A SCHEDULER-
# domain footprint assumes scheduler behavior while the property being
# proved IS scheduler behavior: circular by construction, rejected at G1.
_CONSTRAINT_DOMAIN = {
    "NONE": "NONE",
    "STABILIZED_ELIGIBILITY": "ENVIRONMENT",
    "ELIGIBLE_IFF_SERVICED": "SCHEDULER",
    "CONTRADICTORY": "NONE",
}

PROPERTIES = ("WEAK_FAIRNESS", "STRONG_FAIRNESS", "CONDITIONAL_LIVENESS")
PROVER_POLICIES = ("UNCONSTRAINED", "WEAK", "STRONG")

# Starvation verdicts relevant per claimed property (from the canonical
# classifier's taxonomy; PROGRESS_ON_SERVICE_VIOLATION is a worker/
# execution defect, not scheduler starvation, and is out of D28's scope).
PROPERTY_STARVATION = {
    "WEAK_FAIRNESS": ("WF_VIOLATION",),
    "STRONG_FAIRNESS": ("WF_VIOLATION", "SF_ONLY_VIOLATION"),
    "CONDITIONAL_LIVENESS": ("WF_VIOLATION", "SF_ONLY_VIOLATION"),
}

GATES = (
    "G1_INDEPENDENT_JUSTIFICATION",
    "G2_SATISFIABILITY",
    "G3_MINIMAL_SUFFICIENCY",
    "G4_NON_CIRCULARITY",
)

AUDIT_VERDICTS = (
    "AUDIT_PASSED",
    "REJECTED",
    "REDUNDANT_ASSUMPTIONS",
    "CLAIM_NOT_ESTABLISHED",
)


class AuditInputError(Exception):
    """The audit was given malformed input. Fail-closed: no verdict."""


# ---------------------------------------------------------------------------
# Data model.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AuditAssumption:
    """One assumption under independent audit.

    assumption_id: stable id (a D27 id when registered there).
    statement: exact human-readable meaning.
    owner: who can guarantee it. SCHEDULER is accepted at input so the
        audit can reject it by name; it never passes G1.
    status: PROPOSED | JUSTIFIED | CHALLENGED | REJECTED. Only JUSTIFIED
        can carry a qualification.
    justification: human-readable why (non-empty).
    justification_evidence: artifact names that MUST resolve in the
        independent evidence ledger. A justification that points nowhere
        checkable is not a justification.
    model_constraint: footprint in the abstract model (MODEL_CONSTRAINTS).
    in_qualification_scope: False exempts a documentary assumption from
        G3's redundancy check (it is relied upon by other components, à
        la D27's relied_upon_by). It still faces G1/G2.
    """
    assumption_id: str
    statement: str
    owner: str
    status: str
    justification: str
    justification_evidence: tuple
    model_constraint: str = "NONE"
    in_qualification_scope: bool = True

    def __post_init__(self):
        assert self.assumption_id, "assumption needs an id"
        assert self.statement, "assumption needs a statement"
        assert self.owner in _INPUT_OWNERS, f"unknown owner {self.owner}"
        assert self.status in AUDIT_STATUSES, f"unknown status {self.status}"
        assert self.model_constraint in MODEL_CONSTRAINTS, (
            f"unknown model constraint {self.model_constraint}: refusing "
            f"to guess its footprint")


@dataclass(frozen=True)
class QualificationClaim:
    """The qualification being audited.

    claim_id: stable id for the claim.
    property_claimed: WEAK_FAIRNESS | STRONG_FAIRNESS | CONDITIONAL_LIVENESS.
    scheduler_id: which scheduler was qualified.
    qualification_artifact: the receipt/report naming the qualification.
        It may never appear in an assumption's justification_evidence:
        the verdict being audited cannot justify the assumptions it
        rests on.
    prover_policy: the model-check policy the prover ran
        (UNCONSTRAINED | WEAK | STRONG). G0 re-runs it on its own terms.
    excluded_behaviors: scheduler-failure patterns explicitly scoped OUT
        of the qualification, named as "<BROKEN_KIND>:<verdict>", e.g.
        "BROKEN_SF:SF_ONLY_VIOLATION". G4's killer probe consults this:
        a deleted failure that is not named here is rigging, not scoping.
    """
    claim_id: str
    property_claimed: str
    scheduler_id: str
    qualification_artifact: str
    prover_policy: str = "STRONG"
    excluded_behaviors: tuple = ()

    def __post_init__(self):
        assert self.claim_id, "claim needs an id"
        assert self.property_claimed in PROPERTIES, self.property_claimed
        assert self.scheduler_id, "claim needs a scheduler id"
        assert self.qualification_artifact, "claim needs its artifact name"
        assert self.prover_policy in PROVER_POLICIES, self.prover_policy


@dataclass(frozen=True)
class EvidenceRecord:
    """One independently-produced evidence artifact."""
    name: str
    produced_by: str      # independent producer, not the prover
    produced_at: str
    summary: str = ""


class EvidenceLedger:
    """The independent evidence ledger. The prover does not control it:
    justification evidence resolves here or the assumption is unjustified."""

    def __init__(self):
        self._records = {}

    def record(self, rec: EvidenceRecord) -> None:
        assert isinstance(rec, EvidenceRecord), rec
        if rec.name in self._records:
            raise AuditInputError(
                f"duplicate evidence record {rec.name}: the ledger is "
                f"append-only per name")
        self._records[rec.name] = rec

    def resolve(self, name: str):
        return self._records.get(name)

    def __contains__(self, name: str) -> bool:
        return name in self._records


@dataclass(frozen=True)
class AuditVerdict:
    """One audit verdict. The four kinds never collapse into a green PASS."""
    kind: str                     # one of AUDIT_VERDICTS
    claim_id: str
    failed_gate: str = ""         # the G-code that failed, if any
    reason: str = ""
    gate_results: tuple = ()      # ((gate, passed, detail), ...) in order
    model_depth: int = 12

    def __post_init__(self):
        assert self.kind in AUDIT_VERDICTS, self.kind
        if self.kind != "AUDIT_PASSED":
            assert self.failed_gate or self.kind in (
                "REDUNDANT_ASSUMPTIONS", "CLAIM_NOT_ESTABLISHED"), (
                "a non-pass verdict must name its gate or carry its "
                "kind's meaning")


# ---------------------------------------------------------------------------
# Model-check cache. find_lassos is deterministic; caching by
# (policy, depth) keeps multi-gate audits cheap. Tests share it.
# ---------------------------------------------------------------------------
_lasso_cache: dict = {}


def _cached_lassos(policy: str, depth: int) -> list:
    key = (policy, depth)
    if key not in _lasso_cache:
        _lasso_cache[key] = find_lassos(policy, max_depth=depth)
    return _lasso_cache[key]


def clear_lasso_cache() -> None:
    _lasso_cache.clear()


# ---------------------------------------------------------------------------
# Constraint filters over lasso cycles.
# ---------------------------------------------------------------------------
def _cycle_patterns(lasso: Lasso) -> tuple:
    enabled = tuple(o.enabled for o in lasso.cycle)
    serviced = tuple(o.serviced for o in lasso.cycle)
    return enabled, serviced


def _constraint_keeps(constraint: str, lasso: Lasso) -> bool:
    """Does this lasso survive the assumption's model footprint?"""
    enabled, serviced = _cycle_patterns(lasso)
    if constraint == "NONE":
        return True
    if constraint == "STABILIZED_ELIGIBILITY":
        return bool(enabled) and all(enabled)
    if constraint == "ELIGIBLE_IFF_SERVICED":
        return all(e == s for e, s in zip(enabled, serviced))
    if constraint == "CONTRADICTORY":
        return False
    raise AuditInputError(
        f"unknown model constraint {constraint}: refusing to guess")


def _combined_filter(assumptions: tuple):
    constraints = [a.model_constraint for a in assumptions]

    def keep(lasso: Lasso) -> bool:
        return all(_constraint_keeps(c, lasso) for c in constraints)

    return keep


def _filtered_starvation(property_claimed: str, assumptions: tuple,
                         policy: str, depth: int) -> list:
    """Starvation lassos for the claimed property surviving the assumption
    filters under the given model-check policy. The shared probe behind
    G0 (claim establishment) and G3 (minimal sufficiency)."""
    starve = PROPERTY_STARVATION[property_claimed]
    keep = _combined_filter(assumptions)
    out = []
    for oid, lasso in _cached_lassos(policy, depth):
        if not keep(lasso):
            continue
        verdict, _ = classify_lasso(lasso)
        if verdict in starve:
            out.append((oid, verdict))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# G4's killer probe: two deliberately unfair schedulers. Deterministic;
# the probe is armed only if both classify as their known verdicts.
# ---------------------------------------------------------------------------
_PROBE_KINDS = (
    ("BROKEN_WF", "WF_VIOLATION"),
    ("BROKEN_SF", "SF_ONLY_VIOLATION"),
)


def killer_probe_traces() -> list:
    """Build the killer probe traces. Returns
    [(kind, verdict, armed, lasso), ...]. Exported so tests can assert the
    probe is armed independently of any audit."""
    out = []
    for kind, expected in _PROBE_KINDS:
        obs = run_broken_scheduler(kind, rounds=12)
        lasso = Lasso(obligation_id="WF-B", prefix=(), cycle=tuple(obs))
        verdict, reason = classify_lasso(lasso)
        out.append((kind, verdict, verdict == expected, lasso, reason))
    return out


# ---------------------------------------------------------------------------
# The four gates.
# ---------------------------------------------------------------------------
def _gate_g1(assumptions: tuple, claim: QualificationClaim,
             ledger: EvidenceLedger) -> tuple:
    """Independent justification. Returns (passed, detail)."""
    for a in assumptions:
        if a.status != "JUSTIFIED":
            return False, (
                f"{a.assumption_id}: status is {a.status}, not JUSTIFIED — "
                f"a non-justified assumption cannot carry a qualification")
        if a.owner == "SCHEDULER":
            return False, (
                f"{a.assumption_id}: owned by SCHEDULER while the property "
                f"being proved ({claim.property_claimed}) is the "
                f"scheduler's own behavior — circular")
        if not a.justification.strip():
            return False, (
                f"{a.assumption_id}: empty justification")
        if not a.justification_evidence:
            return False, (
                f"{a.assumption_id}: no justification evidence named — a "
                f"justification that points nowhere checkable is not a "
                f"justification")
        missing = [n for n in a.justification_evidence if n not in ledger]
        if missing:
            return False, (
                f"{a.assumption_id}: justification evidence {missing} does "
                f"not resolve in the independent ledger — the exclusion "
                f"is not independently proven")
        if claim.qualification_artifact in a.justification_evidence:
            return False, (
                f"{a.assumption_id}: justification evidence names the "
                f"qualification artifact itself "
                f"({claim.qualification_artifact}) — the verdict being "
                f"audited cannot justify the assumptions it rests on")
        domain = _CONSTRAINT_DOMAIN[a.model_constraint]
        if domain == "SCHEDULER":
            return False, (
                f"{a.assumption_id}: model footprint "
                f"{a.model_constraint} constrains scheduler behavior while "
                f"the property being proved is scheduler behavior — "
                f"circular by construction (A_env /\\ I_sched |/= F_sched "
                f"when F_sched is assumed)")
        if domain == "ENVIRONMENT" and a.owner not in (
                "ENVIRONMENT", "HUMAN_AUTHORITY"):
            return False, (
                f"{a.assumption_id}: environment-constraining footprint "
                f"owned by {a.owner} — only the environment (or the human "
                f"authority) can guarantee it")
    return True, (
        f"{len(assumptions)} assumption(s): every one JUSTIFIED, "
        f"ledger-resolved, independently owned, no self-justification")


def _gate_g2(assumptions: tuple, depth: int) -> tuple:
    """Satisfiability: the constrained model admits >= 1 execution."""
    keep = _combined_filter(assumptions)
    survivors = [1 for _, lasso in _cached_lassos("UNCONSTRAINED", depth)
                 if keep(lasso)]
    if not survivors:
        return False, (
            "no execution of the bounded model satisfies the assumption "
            "set — every qualification under it would be vacuously true")
    return True, (
        f"{len(survivors)} model execution(s) satisfy the assumption set: "
        f"the qualification is not vacuous")


def _gate_g3(property_claimed: str, assumptions: tuple,
             prover_policy: str, depth: int) -> tuple:
    """Minimal sufficiency: every in-scope assumption earns its place."""
    redundant = []
    for a in assumptions:
        if not a.in_qualification_scope:
            continue
        rest = tuple(x for x in assumptions
                     if x.assumption_id != a.assumption_id)
        before_prover = _filtered_starvation(
            property_claimed, assumptions, prover_policy, depth)
        after_prover = _filtered_starvation(
            property_claimed, rest, prover_policy, depth)
        before_adv = _filtered_starvation(
            property_claimed, assumptions, "UNCONSTRAINED", depth)
        after_adv = _filtered_starvation(
            property_claimed, rest, "UNCONSTRAINED", depth)
        if before_prover == after_prover and before_adv == after_adv:
            redundant.append(a.assumption_id)
    if redundant:
        return False, (
            f"assumption(s) {redundant} change neither the prover's check "
            f"nor the adversarial probe when removed — they earn no place "
            f"in this qualification")
    return True, (
        "every in-scope assumption is load-bearing: removing any one "
        "changes the prover's check or resurrects an adversarial trace")


def _gate_g4(property_claimed: str, assumptions: tuple,
             claim: QualificationClaim) -> tuple:
    """Non-circularity via the killer probe."""
    starve = PROPERTY_STARVATION[property_claimed]
    keep = _combined_filter(assumptions)
    deletions = []
    notes = []
    for kind, verdict, armed, lasso, _ in killer_probe_traces():
        if not armed:
            return False, (
                f"killer probe disarmed: {kind} no longer classifies as "
                f"its known starvation verdict — the audit cannot verify "
                f"non-circularity and refuses to pass")
        if verdict not in starve:
            continue
        if keep(lasso):
            notes.append(f"{kind}:{verdict} survives the assumption set")
            continue
        key = f"{kind}:{verdict}"
        if key in claim.excluded_behaviors:
            notes.append(
                f"{key} deleted by the assumption set but explicitly "
                f"excluded in the claim — legitimate scoping")
        else:
            deletions.append(key)
    if deletions:
        return False, (
            f"the assumption set deletes genuine scheduler failure(s) "
            f"{deletions} from the model without naming them in the "
            f"claim's excluded_behaviors — the test was rigged, not the "
            f"scheduler fixed")
    detail = "; ".join(notes) if notes else (
        "no probe trace deleted: the assumptions hide no scheduler failure")
    return True, detail


# ---------------------------------------------------------------------------
# The audit.
# ---------------------------------------------------------------------------
def _check_inputs(assumptions: tuple, claim: QualificationClaim,
                  ledger: EvidenceLedger) -> None:
    if not isinstance(assumptions, tuple):
        raise AuditInputError("assumptions must be a tuple")
    ids = [a.assumption_id for a in assumptions]
    if len(set(ids)) != len(ids):
        raise AuditInputError(
            f"duplicate assumption ids: {sorted(ids)}")
    if not isinstance(claim, QualificationClaim):
        raise AuditInputError("claim must be a QualificationClaim")
    if not isinstance(ledger, EvidenceLedger):
        raise AuditInputError("ledger must be an EvidenceLedger")


def audit_assumption_set(assumptions: tuple, claim: QualificationClaim,
                         ledger: EvidenceLedger,
                         model_depth: int = 12) -> AuditVerdict:
    """Run the D28 independent audit. Four gates, all required, in order;
    the first failure ends the audit (fail-closed). Returns an AuditVerdict
    whose kind never collapses into a bare PASS."""
    _check_inputs(assumptions, claim, ledger)
    results = []

    # G1 — independent justification.
    passed, detail = _gate_g1(assumptions, claim, ledger)
    results.append((GATES[0], passed, detail))
    if not passed:
        return AuditVerdict(
            kind="REJECTED", claim_id=claim.claim_id,
            failed_gate=GATES[0], reason=detail,
            gate_results=tuple(results), model_depth=model_depth)

    # G2 — satisfiability.
    passed, detail = _gate_g2(assumptions, model_depth)
    results.append((GATES[1], passed, detail))
    if not passed:
        return AuditVerdict(
            kind="REJECTED", claim_id=claim.claim_id,
            failed_gate=GATES[1], reason=detail,
            gate_results=tuple(results), model_depth=model_depth)

    # G0 — claim establishment (pre-check: the audit audits an established
    # claim; a claim that fails on its own terms is not the audit's to fix).
    starvation = _filtered_starvation(
        claim.property_claimed, assumptions, claim.prover_policy,
        model_depth)
    if starvation:
        detail = (
            f"the claimed qualification fails under its own assumptions: "
            f"{starvation} survive the prover's {claim.prover_policy} check")
        results.append(("G0_CLAIM_ESTABLISHMENT", False, detail))
        return AuditVerdict(
            kind="CLAIM_NOT_ESTABLISHED", claim_id=claim.claim_id,
            reason=detail, gate_results=tuple(results),
            model_depth=model_depth)
    results.append(("G0_CLAIM_ESTABLISHMENT", True,
                    f"prover's {claim.prover_policy} check holds under the "
                    f"assumption set"))

    # G3 — minimal sufficiency.
    passed, detail = _gate_g3(
        claim.property_claimed, assumptions, claim.prover_policy,
        model_depth)
    results.append((GATES[2], passed, detail))
    if not passed:
        return AuditVerdict(
            kind="REDUNDANT_ASSUMPTIONS", claim_id=claim.claim_id,
            failed_gate=GATES[2], reason=detail,
            gate_results=tuple(results), model_depth=model_depth)

    # G4 — non-circularity (killer probe).
    passed, detail = _gate_g4(claim.property_claimed, assumptions, claim)
    results.append((GATES[3], passed, detail))
    if not passed:
        return AuditVerdict(
            kind="REJECTED", claim_id=claim.claim_id,
            failed_gate=GATES[3], reason=detail,
            gate_results=tuple(results), model_depth=model_depth)

    return AuditVerdict(
        kind="AUDIT_PASSED", claim_id=claim.claim_id,
        reason=("all four gates passed at model depth "
                f"{model_depth}: independently justified, satisfiable, "
                f"minimal, non-circular"),
        gate_results=tuple(results), model_depth=model_depth)


def summarize(verdict: AuditVerdict) -> str:
    """Human-readable one-block summary of an audit verdict."""
    lines = [f"D28 audit of {verdict.claim_id}: {verdict.kind} "
             f"(model depth {verdict.model_depth})"]
    if verdict.failed_gate:
        lines.append(f"  failed gate: {verdict.failed_gate}")
    if verdict.reason:
        lines.append(f"  reason: {verdict.reason}")
    for gate, passed, detail in verdict.gate_results:
        lines.append(f"  [{'PASS' if passed else 'FAIL'}] {gate}: {detail}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# D27 adapter. The D27 registry (PR #2295, unmerged at time of writing)
# registers assumptions with .id/.statement. This adapter binds a
# registered assumption into the audit WITHOUT importing the unmerged
# module and WITHOUT inventing justification fields: owner, status,
# justification, and evidence are REQUIRED — the adapter refuses to
# imagine them (phantom justification is exactly what D28 exists to kill).
# ---------------------------------------------------------------------------
def from_d27(assumption, *, owner: str, status: str, justification: str,
             justification_evidence: tuple, model_constraint: str = "NONE",
             in_qualification_scope: bool = True) -> AuditAssumption:
    if not owner or not status or not justification \
            or not justification_evidence:
        raise AuditInputError(
            "from_d27 refuses to invent justification fields: owner, "
            "status, justification, and justification_evidence are all "
            "required")
    return AuditAssumption(
        assumption_id=assumption.id,
        statement=assumption.statement,
        owner=owner,
        status=status,
        justification=justification,
        justification_evidence=tuple(justification_evidence),
        model_constraint=model_constraint,
        in_qualification_scope=in_qualification_scope,
    )
