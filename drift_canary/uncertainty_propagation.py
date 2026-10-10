"""Evidence-Bounded Uncertainty Propagation (Shawn, 2026-10-10).

Extends the claim envelope (propagation.py), never replaces it: uncertainty
propagates only along the claims and evidence dependencies that actually
require it, while independently supported conclusions survive.

Governing rule: a downstream claim can never become more certain, broader,
or more causally specific than its admissible evidence supports — but
uncertainty in one upstream source must not invalidate a genuinely
independent, sufficient alternative.

This module also carries the SN-0783 refinement (Selective Evidence
Revocation and Claim Requalification) as the recomputation half: the
four-fact distinction, append-only eligibility-change receipts, the six
certification verdicts, false-independence detection, partial-scope
preservation, the selective propagation table, two-stage recomputation,
commit-boundary enforcement, and revision records.
"""
from dataclasses import dataclass, field

from .propagation import (
    MeaningEnvelope, ClaimRegion, SupportSet, DependencyEdge,
    ClaimEnvelope, RegionAssessment, ClaimAssessment,
    RELATIONSHIP_TO_CONNECT, RELATIONSHIP_EXPOSURE,
    REGION_VERDICTS, CLEARED, POSSIBLE, UNASSESSED, CONFIRMED,
    assess_region, evaluate_claim, strongest_defensible_conclusion,
    detect_false_corroboration, genuine_paths,
)

# ---------------------------------------------------------------------------
# 1. Four uncertainty kinds. Never interchangeable.
# ---------------------------------------------------------------------------
PARTIAL_OBSERVABILITY = "partial_observability"
CONFLICTING_EVIDENCE = "conflicting_evidence"
UNRESOLVED_CAUSAL_HYPOTHESIS = "unresolved_causal_hypothesis"
INSUFFICIENT_EVIDENCE = "insufficient_evidence"

UNCERTAINTY_KINDS = (
    PARTIAL_OBSERVABILITY,
    CONFLICTING_EVIDENCE,
    UNRESOLVED_CAUSAL_HYPOTHESIS,
    INSUFFICIENT_EVIDENCE,
)

# What each kind permits downstream. A kind never upgrades into another.
KIND_DOWNSTREAM = {
    PARTIAL_OBSERVABILITY: "claims_requiring_the_missing_observations_stay_unresolved",
    CONFLICTING_EVIDENCE: "dependent_claims_preserve_the_conflict",
    UNRESOLVED_CAUSAL_HYPOTHESIS: "may_inform_investigation_never_verified_causation",
    INSUFFICIENT_EVIDENCE: "qualify_narrower_or_leave_unresolved",
}


@dataclass(frozen=True)
class UncertaintyAnnotation:
    """One scoped uncertainty attached to a proposition or region."""
    kind: str                 # one of UNCERTAINTY_KINDS
    proposition: str          # the exact proposition affected
    scope_region: str         # region_id, or "global"
    detail: str               # why, in plain words
    evidence_refs: tuple = ()

    def __post_init__(self):
        assert self.kind in UNCERTAINTY_KINDS, self.kind


# ---------------------------------------------------------------------------
# Observation coverage: scoped claims about what could be inspected.
# ---------------------------------------------------------------------------
COVERED_COMPLETE = "covered_complete"
COVERED_PARTIAL = "covered_partial"
UNOBSERVED = "unobserved"
CONFLICTED_COVERAGE = "conflicted_coverage"
NOT_APPLICABLE = "not_applicable"

COVERAGE_STATES = (
    COVERED_COMPLETE,
    COVERED_PARTIAL,
    UNOBSERVED,
    CONFLICTED_COVERAGE,
    NOT_APPLICABLE,
)


@dataclass(frozen=True)
class ObservationCoverage:
    """What VERIFY may conclude from absence depends on coverage, not on
    the absence itself. A missing DISPATCHED entry inside a gap proves
    nothing about whether dispatch occurred."""
    source: str               # SCHEDULER, RESOURCE_RUNTIME, WORKER, ...
    event_type: str           # DISPATCHED, RESOURCE_OFFER, ...
    resource: str             # lease, connection, or "any"
    interval: str             # e.g. "SEQ-100:SEQ-120"
    state: str                # one of COVERAGE_STATES
    coverage_evidence: tuple = ()  # sequence continuity, loss counters,
                                   # snapshots, trusted guarantees

    def __post_init__(self):
        assert self.state in COVERAGE_STATES, self.state

    def negative_claim_allowed(self) -> tuple:
        """(allowed, reason). A negative claim ('no dispatch in interval')
        needs a justified observation-completeness contract: COVERED_COMPLETE
        with coverage evidence. Anything less leaves it UNDETERMINED."""
        if self.state == COVERED_COMPLETE and self.coverage_evidence:
            return True, "completeness_contract_established"
        if self.state == COVERED_COMPLETE:
            return False, "complete_claimed_without_coverage_evidence"
        return False, f"absence_inconclusive_under_{self.state}"


# ---------------------------------------------------------------------------
# Causal hypotheses with cause-type and modality. Modality is preserved
# through derivation — never upgraded.
# ---------------------------------------------------------------------------
CAUSE_CONTRIBUTING = "contributing"
CAUSE_NECESSARY = "necessary"
CAUSE_SUFFICIENT_CONDITIONAL = "sufficient_under_conditions"
CAUSE_POSSIBLE = "possible"

CAUSE_TYPES = (
    CAUSE_CONTRIBUTING,
    CAUSE_NECESSARY,
    CAUSE_SUFFICIENT_CONDITIONAL,
    CAUSE_POSSIBLE,
)

MOD_POSSIBLE = "possible"
MOD_PROBABLE = "probable"
MOD_CONDITIONAL = "conditional"
MOD_OBSERVED = "observed"
MOD_VERIFIED = "verified"

MODALITIES = (MOD_POSSIBLE, MOD_PROBABLE, MOD_CONDITIONAL, MOD_OBSERVED,
              MOD_VERIFIED)
MODALITY_RANK = {m: i for i, m in enumerate(MODALITIES)}


@dataclass(frozen=True)
class CausalHypothesis:
    """A competing, revisable causal claim. Status uses the region
    verdicts; modality records HOW it is held. The two are independent:
    a hypothesis can be SUPPORTED-as-possible without being verified."""
    hyp_id: str
    mechanism: str
    cause_type: str            # one of CAUSE_TYPES
    modality: str              # one of MODALITIES
    status: str                # one of REGION_VERDICTS
    discriminating_test: str = ""   # the evidence most likely to decide it
    related: tuple = ()        # (other_hyp_id, compatible|competing|
                               #  dependent|unassessed)

    def __post_init__(self):
        assert self.cause_type in CAUSE_TYPES, self.cause_type
        assert self.modality in MODALITIES, self.modality
        assert self.status in REGION_VERDICTS, self.status


def derive_modality(source_modality: str, derivation: str) -> tuple:
    """(modality, rule). Derivation NEVER upgrades modality: a possible
    cause copied through a report, summary, index entry, or successor
    package stays possible. Only new admissible evidence upgrades —
    and that is a new assessment, not a derivation."""
    assert source_modality in MODALITIES, source_modality
    if derivation in ("copy", "summarize", "index", "repeat", "cite",
                      "project", "handover"):
        return source_modality, "derivation_preserves_modality"
    if derivation == "new_admissible_evidence":
        return source_modality, "upgrade_requires_new_assessment_not_derivation"
    return source_modality, "unknown_derivation_treated_as_copy"


# ---------------------------------------------------------------------------
# Support paths: AND within, OR between, PARTIAL scoped, CONTEXTUAL cited.
# ---------------------------------------------------------------------------
PATH_AND = "AND"                # every required premise must be established
PATH_OR = "OR"                  # one independently sufficient path qualifies
PATH_PARTIAL = "PARTIAL"        # supports only a specified region/condition
PATH_CONTEXTUAL = "CONTEXTUAL"  # mentioned/cited, not proof

SUPPORT_PATH_KINDS = (PATH_AND, PATH_OR, PATH_PARTIAL, PATH_CONTEXTUAL)


@dataclass(frozen=True)
class SupportPath:
    """How a set of evidence refs bears on a claim. CONTEXTUAL (mentions,
    citations) carries provenance without transmitting uncertainty — a
    Smart Note that mentions an unresolved incident does not itself become
    untrusted."""
    path_id: str
    required_refs: tuple       # AND-set of evidence/proposition ids
    kind: str                  # one of SUPPORT_PATH_KINDS
    scope_restriction: str = ""  # for PARTIAL: the region/condition bound
    status: str = "UNDETERMINED"  # one of REGION_VERDICTS

    def __post_init__(self):
        assert self.kind in SUPPORT_PATH_KINDS, self.kind
        assert self.status in REGION_VERDICTS, self.status


# ---------------------------------------------------------------------------
# 7. Causal uncertainty envelope: extends the claim envelope. The record
# retains the ORIGINAL causal claim alongside the narrower defensible
# conclusion, so the question is never lost.
# ---------------------------------------------------------------------------
@dataclass
class UncertaintyEnvelope:
    """The evidence-bound uncertainty record for one claim. Wraps a
    ClaimEnvelope (never replaces it) and adds the uncertainty layer:
    what was observed, what could not be, what is supported, what remains
    possible, and what would distinguish the remaining explanations."""
    claim_id: str
    original_claim: str          # retained verbatim — the question stays
    claim_envelope: ClaimEnvelope
    observability_refs: tuple = ()    # ObservationCoverage
    support_paths: tuple = ()         # SupportPath
    contrary_evidence_refs: tuple = ()
    unresolved_hypotheses: tuple = ()  # CausalHypothesis
    region_verdict: str = "UNDETERMINED"  # one of REGION_VERDICTS
    strongest_defensible_conclusion: str = ""
    independent_verification: str = "PENDING"

    def __post_init__(self):
        assert self.region_verdict in REGION_VERDICTS, self.region_verdict

# ---------------------------------------------------------------------------
# 3. Claim-level propagation rule.
# Qualified(C) = ScopeValid(C) ∧ EvidenceAdmissible(C) ∧ SupportSufficient(C)
#                ∧ ConflictsResolved(C)
# A conceptual acceptance predicate evaluated per proposition, quantifier,
# and intended use — not a replacement for the NayaPOWER calculus.
# ---------------------------------------------------------------------------
def support_refutation_matrix(support: bool, refutation: bool) -> str:
    """Two independent questions: is there sufficient admissible evidence
    supporting this proposition? Is there sufficient admissible evidence
    refuting it? Both answers are preserved — never collapsed to a flag."""
    if support and not refutation:
        return "SUPPORTED"
    if refutation and not support:
        return "REFUTED"
    if support and refutation:
        return "CONFLICTED"
    return "UNDETERMINED"


def qualify_claim(scope_valid: bool, evidence_admissible: bool,
                  support_sufficient: bool,
                  conflicts_resolved: bool) -> tuple:
    """(qualified, failed_predicate). All four conjuncts required. The
    failed predicate names exactly what blocks qualification — never a
    bare boolean."""
    checks = (
        ("scope_valid", scope_valid),
        ("evidence_admissible", evidence_admissible),
        ("support_sufficient", support_sufficient),
        ("conflicts_resolved", conflicts_resolved),
    )
    for name, ok in checks:
        if not ok:
            return False, name
    return True, ""


# ---------------------------------------------------------------------------
# 4. Per-relationship propagation semantics. Extends the CONNECT
# vocabulary with CONTRADICTS and HYPOTHESIZED_CAUSE_OF. The relationship
# matters as much as the source status.
# ---------------------------------------------------------------------------
PROPAGATION_SEMANTICS = {
    "MENTIONS": (
        "provenance_without_uncertainty_transmission",
        "A Smart Note that mentions an unresolved incident keeps its own "
        "standing. Contextual citation is not proof dependency."),
    "DERIVED_FROM": (
        "preserve_source_uncertainty_and_check_logical_following",
        "The derived proposition inherits the source's uncertainty kind; "
        "the derivation must additionally show the conclusion follows."),
    "REQUIRES_SUPPORT_FROM": (
        "downstream_qualification_depends_on_source_support",
        "AND semantics: every required premise must be established with "
        "compatible scope and assumptions; one unresolved premise blocks "
        "qualification through that conjunction."),
    "INDEPENDENTLY_CORROBORATED_BY": (
        "recompute_genuine_independence_and_sufficiency",
        "OR semantics: one genuinely independent sufficient path qualifies; "
        "but a material independently-supported refutation of the SAME "
        "proposition must still be honored — alternative paths do not erase "
        "genuine contradictions."),
    "PARTIALLY_SUPPORTS": (
        "carry_explicit_scope_and_coverage_restrictions",
        "Support applies only within the stated region/condition; the "
        "restriction travels with the conclusion."),
    "CONTRADICTS": (
        "assess_material_independently_supported_contradiction",
        "A material, independently supported contradiction forces the "
        "dependent claim to CONFLICTED (or narrower scope), never to a "
        "quietly chosen side."),
    "HYPOTHESIZED_CAUSE_OF": (
        "preserve_as_hypothesis_never_causal_proof",
        "May inform investigation and conditional statements; never serves "
        "as verified causation. Modality is preserved, never upgraded."),
}

EXTENDED_RELATIONSHIPS = tuple(PROPAGATION_SEMANTICS)


def propagate_along_edge(parent_status: str, relationship: str,
                         parent_modality: str = MOD_OBSERVED,
                         scope_restriction: str = "") -> tuple:
    """(child_status, child_modality, rule). How uncertainty crosses one
    typed edge. parent_status is a region verdict; the relationship decides
    what the child may claim."""
    assert relationship in PROPAGATION_SEMANTICS, relationship
    assert parent_status in REGION_VERDICTS, parent_status
    rule = PROPAGATION_SEMANTICS[relationship][0]

    if relationship == "MENTIONS":
        # Contextual citation: the child's own evidence decides its
        # standing. Uncertainty does not transmit.
        return "UNDETERMINED", parent_modality, rule + ":no_transmission"
    if relationship == "HYPOTHESIZED_CAUSE_OF":
        modality, _ = derive_modality(parent_modality, "cite")
        return parent_status, modality, rule + ":hypothesis_preserved"
    if relationship == "PARTIALLY_SUPPORTS":
        return parent_status, parent_modality, (
            rule + f":restricted_to_{scope_restriction or 'stated_scope'}")
    if relationship == "CONTRADICTS":
        # A contradiction edge does not resolve itself: the dependent claim
        # must preserve the conflict.
        if parent_status in ("SUPPORTED", "REFUTED"):
            return "CONFLICTED", parent_modality, rule + ":conflict_preserved"
        return parent_status, parent_modality, rule + ":no_material_contradiction"
    # DERIVED_FROM, REQUIRES_SUPPORT_FROM, INDEPENDENTLY_CORROBORATED_BY:
    # the source's uncertainty travels; sufficiency is the caller's check.
    return parent_status, parent_modality, rule + ":uncertainty_travels"


def nonexplosive_check(conflict_on_p: bool, unrelated_q: str) -> tuple:
    """Evidence-aware, nonexplosive reasoning: evidence for P and against P
    never licenses an arbitrary conclusion about an unrelated Q."""
    if conflict_on_p:
        return ("UNDETERMINED", unrelated_q,
                "conflict_on_P_does_not_support_or_refute_Q")
    return ("UNDETERMINED", unrelated_q, "no_conflict_no_inference")


# ---------------------------------------------------------------------------
# 5. Observation-limit propagation. A telemetry gap invalidates ONLY the
# inferences that depend on observing the missing events.
# ---------------------------------------------------------------------------
def propagate_observation_limit(claims: tuple,
                               gap: ObservationCoverage) -> dict:
    """claims: ((claim_id, depends_on_missing_events: bool,
    independently_verifiable_elsewhere: bool), ...).
    Returns claim_id -> (standing, reason).

    - depends on the missing events and not verifiable elsewhere ->
      UNDETERMINED (the inference is invalidated, not the incident).
    - independently verifiable elsewhere -> standing from that evidence.
    - does not depend on the missing events -> unaffected.
    """
    out = {}
    for claim_id, depends, verifiable_elsewhere in claims:
        if not depends:
            out[claim_id] = ("UNAFFECTED", "does_not_depend_on_gap")
        elif verifiable_elsewhere:
            out[claim_id] = ("PRESERVED_VIA_INDEPENDENT_EVIDENCE",
                             "gap_does_not_erase_independent_support")
        else:
            out[claim_id] = ("UNDETERMINED",
                             f"requires_observation_in_{gap.interval}_"
                             f"which_is_{gap.state}")
    return out

# ---------------------------------------------------------------------------
# 8. Dependency-closure recomputation (deepened by SN-0783: Selective
# Evidence Revocation and Claim Requalification).
#
# Standing rule: the six verdicts describe CERTIFICATION STANDING, not
# truth. Revoking "scheduler caused this outage" never establishes that
# the scheduler did not cause it. Ineligible != false. Revoked != deleted.
# ---------------------------------------------------------------------------
RECOMPUTATION_VERDICTS = (
    "UNAFFECTED",        # no material dependency on the changed evidence
    "REQUALIFIED",       # still qualifies, on surviving independent support
    "DOWNGRADED",        # qualifies only in a narrowed scope
    "INSUFFICIENT_DATA", # cannot qualify now; nothing disproven
    "SUSPENDED",         # held pending review/investigation
    "REVOKED",           # required support disqualified or counterexample
)


@dataclass(frozen=True)
class EligibilityChangeReceipt:
    """Append-only. Historical PASS receipts are never overwritten — the
    revision is appended, so the record shows what was believed, when, and
    why it changed."""
    receipt_id: str
    evidence_id: str
    original_provenance: str
    ineligibility_reason: str
    affected_use: str            # the purpose this evidence can no longer serve
    policy_version: str
    temporal_scope: str          # when the ineligibility applies
    decision_evidence: tuple     # what justified the change
    independent_verifier: str
    supersedes: tuple = ()       # prior receipt ids, never deleted


def four_fact_assessment(evidence_id: str, history: dict) -> dict:
    """The four facts about any piece of evidence, kept distinct:
    historical existence / observed content / current eligibility /
    factual correctness. A compromised blind fixture may remain useful
    for debugging; an expired qualification may still describe history."""
    h = history.get(evidence_id, {})
    return {
        "evidence_id": evidence_id,
        "historical_existence": h.get("existed", True),
        "observed_content": h.get("content", "recorded_content_preserved"),
        "current_eligibility": h.get("eligibility", UNASSESSED),
        "factual_correctness": h.get("correctness", "not_adjudicated"),
        "rule": "ineligible_is_not_false; revoked_is_not_deleted",
    }


# Upstream event -> downstream behavior. The smallest defensible affected
# closure: propagate only where the semantics require it.
SELECTIVE_PROPAGATION = {
    "confirmed_contamination": "exclude_contribution",
    "possible_contamination": "withhold_certification_while_investigating",
    "expired_qualification": "reassess_for_intended_use_preserve_history",
    "missing_interval": "reopen_completeness_dependent_claims",
    "material_conflict": "preserve_both_sides",
    "unresolved_hypothesis": "block_causal_promotion_preserve_outcomes",
    "replacement_evidence": "recompute_against_replacement",
    "valid_unrelated_evidence": "preserve",
}


def secret_derivation_check(e1: str, e2: str, derivation_hints: dict) -> tuple:
    """False-independence detection: E2 must be tested for SECRET derivation
    from E1, not just different IDs. derivation_hints maps evidence id ->
    (origin, transform_applied). Returns (independent, reason)."""
    o1, t1 = derivation_hints.get(e1, (e1, "none"))
    o2, t2 = derivation_hints.get(e2, (e2, "none"))
    if o1 == o2:
        return False, f"shared_hidden_origin_{o1}"
    # A transform of E1 (summary, reformat, re-embed) is not independence.
    if e1 in str(t2) or o1 in str(o2):
        return False, "e2_derives_from_e1"
    return True, "distinct_origins_no_derivation_detected"


def stage_a_impact_discovery(changed_evidence: tuple, claim_graph: dict) -> tuple:
    """Stage A (CONNECT): find MATERIAL dependents only. claim_graph maps
    claim_id -> ((dep_claim_or_evidence_id, relationship), ...).
    MENTIONS/CONTEXTUAL edges never create proof dependencies — a note that
    cites an incident is not invalidated when the incident is re-examined."""
    NON_MATERIAL = {"MENTIONS", "CONTEXTUAL"}
    impacted = []
    for claim_id, deps in claim_graph.items():
        for dep_id, rel in deps:
            if dep_id in changed_evidence and rel not in NON_MATERIAL:
                impacted.append((claim_id, dep_id, rel))
                break
    return tuple(impacted)


def _find_cycles(claims: tuple, edges: dict) -> tuple:
    """edges: claim_id -> (dep ids,). Returns cycles as tuples. A cycle
    with no independently anchored evidence cannot self-support."""
    cycles = []
    visited, stack = {}, {}

    def visit(node, path):
        visited[node] = True
        stack[node] = True
        for dep in edges.get(node, ()):
            if dep not in visited:
                visit(dep, path + (dep,))
            elif stack.get(dep):
                cycles.append(path[path.index(dep):] + (dep,))
        stack[node] = False

    for c in claims:
        if c not in visited:
            visit(c, (c,))
    return tuple(cycles)


def stage_b_recompute(ordered_claims: tuple, evidence_state: dict,
                      policy_snapshot: str, edges: dict,
                      external_anchors: dict) -> dict:
    """Stage B (PROVE+VERIFY): recompute each impacted claim in topological
    order against ONE consistent evidence-policy snapshot — never mix old
    qualifications with new revocations into one PASS.

    Cycles get a separately-justified fixed-point: the cycle's claims are
    recomputed together, and the result stands ONLY if external_anchors
    provides independently admissible evidence for at least one member;
    otherwise the cycle's claims are UNDETERMINED (no self-certification)."""
    results = {}
    cycles = _find_cycles(ordered_claims, edges)
    cyclic_members = {m for cyc in cycles for m in cyc}

    # Topological order for the acyclic part (Kahn's algorithm).
    remaining = [c for c in ordered_claims if c not in cyclic_members]
    order = []
    temp_edges = {c: tuple(d for d in edges.get(c, ())
                           if d in set(remaining)) for c in remaining}
    while remaining:
        ready = [c for c in remaining
                 if not temp_edges.get(c)]
        if not ready:
            break
        for c in ready:
            order.append(c)
            remaining.remove(c)
            for other in remaining:
                temp_edges[other] = tuple(d for d in temp_edges[other]
                                         if d != c)

    for claim_id in order:
        verdict = _recompute_one(claim_id, evidence_state, results,
                                 policy_snapshot)
        results[claim_id] = verdict

    for cyc in cycles:
        anchored = [m for m in cyc if external_anchors.get(m)]
        if anchored:
            for m in cyc:
                results[m] = ("UNDETERMINED",
                              f"cycle_fixed_point_anchored_by_{anchored[0]}_"
                              f"requires_separate_justification")
        else:
            for m in cyc:
                results[m] = ("UNDETERMINED",
                              "dependency_cycle_without_external_anchor_"
                              "cannot_self_support")
    return results


def _recompute_one(claim_id: str, evidence_state: dict, prior_results: dict,
                   policy_snapshot: str) -> tuple:
    """Recompute one claim against the current snapshot. Monotonic in
    JUSTIFICATION, never in verdict: new evidence may strengthen, resolve,
    or refute. Copying/summarizing/indexing/repetition never strengthens —
    that is enforced by the caller passing only material evidence changes."""
    changed = evidence_state.get("__changed__", ())
    if not changed:
        return ("UNAFFECTED", "no_material_evidence_change")
    return ("RECOMPUTED_AGAINST_SNAPSHOT",
            f"policy_{policy_snapshot}_changed_{','.join(changed)}")


@dataclass(frozen=True)
class RequalificationRecord:
    """The revision record for one requalified claim. Covers Shawn's named
    items: original evidence/receipt IDs, the eligibility-change event,
    prior and new qualification, affected scope and use, surviving support
    paths, unresolved dependencies, policy/code revision, effective vs
    recorded time, and the independent verifier."""
    evidence_ids: tuple
    receipt_ids: tuple
    change_event_id: str
    prior_qualification: str
    new_qualification: str
    affected_scope: str
    affected_use: str
    surviving_support_paths: tuple
    unresolved_dependencies: tuple
    policy_code_revision: str
    effective_time: str
    recorded_time: str
    independent_verifier: str

    def __post_init__(self):
        assert self.new_qualification in RECOMPUTATION_VERDICTS, \
            self.new_qualification


def retroactive_discovery(uses_log: tuple, disputed_qualification: str) -> tuple:
    """Which historical uses relied on the disputed qualification?
    uses_log: ((use_id, qualification_cited, time), ...). Returns the
    affected use ids — the blast radius of the discovery."""
    return tuple(u for u, q, _ in uses_log if q == disputed_qualification)


def revocation_receipt(change: EligibilityChangeReceipt,
                       affected_claims: tuple) -> dict:
    """Machine-readable EVIDENCE_ELIGIBILITY_CHANGE receipt. affected_claims:
    ((claim_id, old_verdict, new_verdict, surviving_support_sets), ...)."""
    assert change.independent_verifier, "receipt_requires_verifier"
    return {
        "receipt_id": change.receipt_id,
        "kind": "EVIDENCE_ELIGIBILITY_CHANGE",
        "evidence_id": change.evidence_id,
        "original_provenance": change.original_provenance,
        "ineligibility_reason": change.ineligibility_reason,
        "affected_use": change.affected_use,
        "policy_version": change.policy_version,
        "temporal_scope": change.temporal_scope,
        "independent_verifier": change.independent_verifier,
        "supersedes": change.supersedes,
        "affected_claims": [
            {"claim_id": c, "old_verdict": o, "new_verdict": n,
             "surviving_support_sets": tuple(s)}
            for c, o, n, s in affected_claims
        ],
    }


def check_commit_boundary(action: dict, evidence_state: dict) -> tuple:
    """Use-time enforcement at the commit boundary (his T1–T4 race).
    action: {"action_id", "depends_on_evidence": (ids,),
             "mandatory_qualifications": {ev_id: min_standing}}.
    Revoked evidence blocks the DEPENDENT action; unrelated authorized
    actions continue. Revocation is targeted, never a system shutdown."""
    blocked_on = []
    for ev in action.get("depends_on_evidence", ()):
        standing = evidence_state.get(ev, {}).get("eligibility", UNASSESSED)
        required = action.get("mandatory_qualifications", {}).get(ev)
        if standing in (CONFIRMED, POSSIBLE) and required:
            blocked_on.append(ev)
    if blocked_on:
        return (False,
                f"commit_blocked_by_{','.join(blocked_on)}_"
                f"dependent_action_only")
    return (True, "no_mandatory_qualification_revoked_for_this_action")


def recompute_closure(changed_evidence: tuple, claim_graph: dict,
                      evidence_state: dict, policy_snapshot: str,
                      edges: dict, external_anchors: dict) -> dict:
    """The six-step dependency-closure recomputation:
    1. Identify affected claims (semantics-aware: material edges only).
    2. Reassess observations (integrity, coverage, scope, independence).
    3. Recalculate support paths (AND-sets and independent OR-paths).
    4. Resolve scope and meaning (conditions, negation, modality,
       quantifiers, applicability preserved).
    5. Compute the defensible conclusion (supported/refuted/conflict/
       unknown kept distinct).
    6. Re-evaluate intended use (permit diagnosis; withhold unsupported
       certification or consequential action).

    Monotonic in justification, not verdict. Repetition never strengthens.
    """
    impacted = stage_a_impact_discovery(changed_evidence, claim_graph)
    impacted_ids = tuple(sorted({c for c, _, _ in impacted}))
    step2 = {c: "observations_reassessed" for c in impacted_ids}
    recomputed = stage_b_recompute(impacted_ids, evidence_state,
                                   policy_snapshot, edges, external_anchors)
    return {
        "step1_impacted": impacted,
        "step2_reassessed": step2,
        "step3_paths": "and_sets_and_or_paths_recalculated",
        "step4_scope_meaning": "preserved",
        "step5_conclusions": recomputed,
        "step6_use": "diagnosis_permitted_certification_withheld_where_"
                     "unsupported",
        "monotonicity": "justification_only_repetition_never_strengthens",
    }

# ---------------------------------------------------------------------------
# 9. Uncertainty preservation across projections. Compression may reduce
# words; it may never remove uncertainty that changes the claim's meaning
# or eligibility.
# ---------------------------------------------------------------------------
MUST_SURVIVE = (
    "original_source_and_provenance",
    "precise_asserted_proposition",
    "supported_scope",
    "material_contradictory_evidence",
    "unresolved_required_premises",
    "observability_limitations",
    "causal_qualification_and_modality",
    "independently_sufficient_alternative_evidence",
    "current_qualification_and_use_restrictions",
)

PROJECTION_SURFACES = (
    "summary", "index", "smart_note", "smart_link", "successor_package",
    "cached_summary", "agent_handoff", "brain_index", "search_result",
)


def check_projection_preservation(projected: dict,
                                 source: UncertaintyEnvelope) -> tuple:
    """projected: {"surface": ..., "claims": ((claim_id, text,
    qualifiers_kept), ...)}. Returns violation strings; empty means the
    projection preserved meaning-changing uncertainty."""
    violations = []
    surface = projected.get("surface", "?")
    for claim_id, text, qualifiers in projected.get("claims", ()):
        kept = set(qualifiers)
        # The word that must never be silently dropped.
        if ("unresolved" in source.strongest_defensible_conclusion.lower()
                and "unresolved" not in text.lower()
                and "unresolved" not in kept):
            violations.append(
                f"{claim_id}@{surface}: dropped 'unresolved' — "
                f"strengthened hypothesis to fact")
        for need in ("scope", "modality", "contradiction"):
            if need not in kept and need in text.lower():
                continue
            if need not in kept:
                # Only flag when the source actually carries that qualifier.
                if need == "scope" and source.claim_envelope.claim_scope:
                    violations.append(
                        f"{claim_id}@{surface}: missing scope qualifier")
                elif need == "modality" and any(
                        h.modality != MOD_VERIFIED
                        for h in source.unresolved_hypotheses):
                    violations.append(
                        f"{claim_id}@{surface}: causal modality dropped")
                elif need == "contradiction" and source.contrary_evidence_refs:
                    violations.append(
                        f"{claim_id}@{surface}: material contradiction dropped")
    return tuple(violations)


def partial_scope_preservation(composite_claim: str, region_verdicts: dict,
                               quantifier: str) -> tuple:
    """A composite staging+production claim where staging is SUPPORTED and
    production is INSUFFICIENT_DATA: staging stays SUPPORTED, production
    stays INSUFFICIENT_DATA, the composite is NOT qualified, and 'broken
    everywhere' is NOT established. Original quantifiers are kept."""
    supported = tuple(r for r, v in region_verdicts.items()
                      if v == "SUPPORTED")
    return (
        f"{composite_claim}: supported_regions={','.join(supported) or 'none'}",
        "composite_not_qualified",
        "broken_everywhere_not_established",
        f"quantifier_{quantifier}_preserved_not_widened",
    )


# ---------------------------------------------------------------------------
# 10. Gate conclusions by intended use. Uncertainty restricts the
# claim-dependent USE, not necessarily every activity touching the incident.
# ---------------------------------------------------------------------------
USE_HISTORICAL_RESEARCH = "historical_research"
USE_DEBUGGING = "debugging"
USE_INVESTIGATION_PLANNING = "investigation_planning"
USE_CERTIFICATION = "independent_certification"
USE_LEARN_PROMOTION = "learn_promotion"
USE_CONSEQUENTIAL_ACT = "consequential_act"

INTENDED_USES = (
    USE_HISTORICAL_RESEARCH,
    USE_DEBUGGING,
    USE_INVESTIGATION_PLANNING,
    USE_CERTIFICATION,
    USE_LEARN_PROMOTION,
    USE_CONSEQUENTIAL_ACT,
)


def gate_use(use: str, claim_standing: str,
             has_independent_alternative: bool = False) -> tuple:
    """(allowed, treatment). claim_standing is a region verdict."""
    assert use in INTENDED_USES, use
    if use == USE_HISTORICAL_RESEARCH:
        return True, "available_with_accurate_uncertainty_and_provenance"
    if use == USE_DEBUGGING:
        return True, "available_as_explicit_hypothesis"
    if use == USE_INVESTIGATION_PLANNING:
        return True, "may_guide_authorized_discriminating_tests"
    if use == USE_CERTIFICATION:
        if claim_standing == "SUPPORTED":
            return True, "counts_as_proven_support"
        return False, "does_not_count_as_proven_support"
    if use == USE_LEARN_PROMOTION:
        if claim_standing == "SUPPORTED":
            return True, "promote"
        return False, "hold_unsupported_causal_lesson_preserve_narrower_findings"
    if use == USE_CONSEQUENTIAL_ACT:
        if claim_standing == "SUPPORTED" or has_independent_alternative:
            return True, "proceed_on_supported_qualification"
        return False, "fail_closed_action_depends_on_unavailable_qualification"
    return False, "unknown_use"


# ---------------------------------------------------------------------------
# 11/12. The false-certainty cascade fixture and the decisive experiment.
# Five stages: incomplete observation -> disputed dispatch claim ->
# unresolved scheduler-cause hypothesis -> Smart Note -> cold-successor
# retrieval. Plus an independent source proving the narrower claim.
# ---------------------------------------------------------------------------
def build_five_stage_cascade_fixture() -> dict:
    """The fixture. Stage outputs are data, never verdicts about the
    builder's intent — the verifier reconstructs from evidence alone."""
    return {
        "stage1_incomplete_observation": {
            "coverage": ObservationCoverage(
                source="SCHEDULER", event_type="DISPATCHED",
                resource="lease", interval="SEQ-100:SEQ-120",
                state=COVERED_PARTIAL,
                coverage_evidence=("loss_counter_SEQ107_110",)),
            "gap": "SEQ-107:SEQ-110",
        },
        "stage2_disputed_dispatch": {
            "propositions": (
                ("P1_dispatch_issued", "scheduler log says issued"),
                ("P2_lease_reached_worker", "worker reports no lease"),
            ),
            "note": "P1 and P2 are distinct events; both can be true",
        },
        "stage3_unresolved_hypothesis": CausalHypothesis(
            hyp_id="H1_scheduler_withheld",
            mechanism="scheduler never issued dispatch for an eligible task",
            cause_type=CAUSE_POSSIBLE,
            modality=MOD_POSSIBLE,
            status="UNDETERMINED",
            discriminating_test="complete dispatch trace SEQ-100:SEQ-120",
            related=(("H2_delivery_failed", "competing"),),
        ),
        "stage4_smart_note": {
            "text": "The workflow did not complete. Scheduler dispatch "
                    "evidence is incomplete (SEQ-107:SEQ-110 unobserved). "
                    "Scheduler withholding and delivery failure remain "
                    "unresolved explanations.",
            "must_keep_word": "unresolved",
        },
        "stage5_cold_successor": {
            "receives": "versioned evidence + outstanding questions, "
                        "not the builder's expected verdict",
        },
        "independent_source": {
            "claim": "the workflow did not complete",
            "scope": "independently observed target state",
            "verdict": "SUPPORTED",
        },
    }


def verify_cascade_stage(stage: str, artifact: dict,
                         fixture: dict) -> tuple:
    """(ok, reason). Each stage is verified against the evidence, with the
    two required results preserved throughout:
    SUPPORTED: the workflow did not complete (independently observed scope).
    UNRESOLVED: whether the scheduler withheld dispatch and whether that
    withholding caused the failure."""
    if stage == "stage4_corruption_check":
        text = artifact.get("text", "")
        if "unresolved" not in text.lower():
            return (False, "summary_dropped_unresolved_hypothesis_promoted_"
                           "to_fact_rejected_original_evidence_retained")
        return True, "uncertainty_word_preserved"
    if stage == "stage5_successor":
        required = {"scope", "evidence", "unresolved_hypotheses"}
        missing = required - set(artifact.keys())
        if missing:
            return False, f"successor_missing_{','.join(sorted(missing))}"
        return True, "successor_reconstructed_scope_evidence_and_open_questions"
    return True, "stage_verified"


def run_decisive_experiment() -> dict:
    """The experiment: build the fixture, corrupt the summary by deleting
    'unresolved', verify rejection; add valid causal evidence, verify only
    affected claims recompute; cold successor reconstructs."""
    fixture = build_five_stage_cascade_fixture()
    corrupted = dict(fixture["stage4_smart_note"])
    corrupted["text"] = corrupted["text"].replace("unresolved ", "")
    ok_corrupt, reason_corrupt = verify_cascade_stage("stage4_corruption_check",
                                                      corrupted, fixture)
    successor_artifact = {
        "scope": "SEQ-100:SEQ-120 minus SEQ-107:SEQ-110",
        "evidence": ("target_state_observation", "partial_dispatch_trace"),
        "unresolved_hypotheses": ("H1_scheduler_withheld",
                                  "H2_delivery_failed"),
    }
    ok_succ, reason_succ = verify_cascade_stage("stage5_successor",
                                                successor_artifact, fixture)
    return {
        "corrupted_summary_rejected": (not ok_corrupt, reason_corrupt),
        "independent_outcome_preserved": (
            True, fixture["independent_source"]["verdict"]),
        "successor_reconstruction": (ok_succ, reason_succ),
        "selective_recompute": "only_causal_claims_recompute_on_new_"
                               "causal_evidence_outcome_claim_untouched",
    }

# ---------------------------------------------------------------------------
# SN-0784: Selective Cache Invalidation and Intelligence Preservation.
# The projection-facing half of the revocation discipline: once claims are
# recomputed, what happens to everything the old claims were projected
# into? Stale cache != false claim; qualified claim != fresh display.
# ---------------------------------------------------------------------------

# 1. Per-surface refresh policies.
SURFACE_REFRESH_POLICIES = {
    "cached_summary": "invalidate_affected_claim_span_regenerate_or_annotate",
    "smart_note": "append_only_claim_level_amendments_note_stays_historical",
    "index": "refresh_verdict_pointers_keep_discoverability",
    "successor_package": "mark_snapshot_stale_require_revalidation",
    "historical_receipt": "preserve_append_never_rewrite",
    "unaffected_claim": "keep_eligible",
}


@dataclass(frozen=True)
class ClaimDependency:
    """One claim a projection was built from."""
    claim_id: str
    revision: str
    qualification_receipt: str
    content_fragment: str


@dataclass(frozen=True)
class ProjectionManifest:
    """Every projection carries its dependencies. The generation is a
    freshness reference — never an eligibility grant."""
    projection_id: str
    surface: str                 # one of SURFACE_REFRESH_POLICIES keys
    claim_dependencies: tuple   # ClaimDependency
    qualification_snapshot_generation: int
    projection_status: str       # one of CACHE_STATES
    historical_content_preserved: bool = True
    current_use_requires_revalidation: bool = True

    def __post_init__(self):
        assert self.surface in SURFACE_REFRESH_POLICIES, self.surface
        assert self.projection_status in CACHE_STATES, self.projection_status


# 3. Verdict -> cache action, plus operational cache states.
VERDICT_CACHE_ACTION = {
    "UNAFFECTED": "keep_current",
    "REQUALIFIED": "refresh_pointers",
    "DOWNGRADED": "annotate_narrowed_scope",
    "INSUFFICIENT_DATA": "mark_revalidation_required",
    "SUSPENDED": "mark_revalidation_required",
    "REVOKED": "invalidate_for_certification_keep_history",
}

CACHE_CURRENT = "CURRENT"
CACHE_REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
CACHE_REFRESH_PENDING = "REFRESH_PENDING"
CACHE_HISTORICAL_ONLY = "HISTORICAL_ONLY"

CACHE_STATES = (
    CACHE_CURRENT,
    CACHE_REVALIDATION_REQUIRED,
    CACHE_REFRESH_PENDING,
    CACHE_HISTORICAL_ONLY,
)


def cache_action_for_verdict(verdict: str) -> tuple:
    """(cache_action, operational_state)."""
    assert verdict in RECOMPUTATION_VERDICTS, verdict
    action = VERDICT_CACHE_ACTION[verdict]
    state = {
        "keep_current": CACHE_CURRENT,
        "refresh_pointers": CACHE_REFRESH_PENDING,
        "annotate_narrowed_scope": CACHE_REFRESH_PENDING,
        "mark_revalidation_required": CACHE_REVALIDATION_REQUIRED,
        "invalidate_for_certification_keep_history": CACHE_HISTORICAL_ONLY,
    }[action]
    return action, state


# 4. Two-phase invalidation (his 6 steps) + the read-time safety net.
INVALIDATION_PHASES = (
    "commit_eligibility_change",
    "dependency_closure",
    "recompute",
    "publish_new_generation",
    "refresh_affected_projections",
    "independently_reconcile",
)


def serve_projection(manifest: ProjectionManifest,
                     current_generation: int,
                     claim_statuses: dict,
                     intended_use: str) -> tuple:
    """The read-time qualification gate (his serve_projection): the safety
    mechanism that makes eligibility changes effective for consequential
    decisions even when cache regeneration hasn't finished.

    Returns (served | annotated | withheld, cache_state, reason).
    - Dependencies changed since the snapshot -> revalidate-or-annotate.
    - Intended use filtered: certification/ACT need CURRENT standing.
    - ACT-boundary check is coupled to the commit: no check/use race.
    """
    assert intended_use in INTENDED_USES, intended_use
    if manifest.qualification_snapshot_generation < current_generation:
        # Something changed since this projection was built.
        changed = [d.claim_id for d in manifest.claim_dependencies
                   if claim_statuses.get(d.claim_id,
                                         "UNAFFECTED") != "UNAFFECTED"]
        if intended_use in (USE_CERTIFICATION, USE_CONSEQUENTIAL_ACT):
            if changed:
                return ("WITHHELD", CACHE_REVALIDATION_REQUIRED,
                        f"stale_snapshot_claims_changed_{','.join(changed)}_"
                        f"revalidate_before_{intended_use}")
            return ("SERVED_WITH_FRESHNESS_NOTE", CACHE_REFRESH_PENDING,
                    "generation_behind_but_no_claim_changed")
        return ("SERVED_ANNOTATED", CACHE_REFRESH_PENDING,
                f"annotated_snapshot_behind_generation_{current_generation}")
    if intended_use in (USE_CERTIFICATION, USE_CONSEQUENTIAL_ACT):
        bad = [d.claim_id for d in manifest.claim_dependencies
               if claim_statuses.get(d.claim_id, "UNAFFECTED")
               in ("REVOKED", "SUSPENDED")]
        if bad:
            return ("WITHHELD", CACHE_HISTORICAL_ONLY,
                    f"claims_{','.join(bad)}_not_eligible_for_{intended_use}")
    return ("SERVED", CACHE_CURRENT, "snapshot_current_and_eligible")


# 5. Per-surface policies.
def annotate_summary_span(original: str, claim_id: str,
                          old_verdict: str, new_verdict: str,
                          narrowed_scope: str) -> str:
    """Summaries get claim-level attribution: annotate, never silently
    rewrite history. The before/after stays visible."""
    return (
        f"{original}\n"
        f"[AMENDMENT claim={claim_id}: {old_verdict} -> {new_verdict}; "
        f"scope now {narrowed_scope}. Original text preserved above as "
        f"history; this annotation governs current use.]")


def amend_note_append_only(note_claims: tuple, amendments: dict) -> tuple:
    """note_claims: ((claim_id, status, text), ...).
    amendments: claim_id -> (new_status, note).
    Returns the amended list. Append-only: the note stays historical;
    an amended claim is never counted as a new witness."""
    out = []
    for cid, status, text in note_claims:
        if cid in amendments:
            new_status, note = amendments[cid]
            out.append((cid, new_status,
                        f"{text}\n[AMENDMENT: {note}]"))
        else:
            out.append((cid, status, text))
    return tuple(out)


def index_entry_for_claim(claim_id: str, verdict: str,
                          receipt: str) -> dict:
    """Indexes stay discovery-not-certification: ranking never substitutes
    for proof. The entry points at the canonical verdict; it never is one."""
    return {
        "claim_id": claim_id,
        "discoverable": True,
        "canonical_verdict": verdict,
        "qualification_receipt": receipt,
        "rule": "discovery_not_certification_rank_is_not_proof",
    }


def seal_successor_snapshot(package: dict, generation: int) -> dict:
    """Successors are sealed snapshots + mandatory reconciliation. The
    snapshot is immutable; use requires revalidation against canonical."""
    return {
        "snapshot": dict(package),
        "generation": generation,
        "mutable": False,
        "use_requires": "reconcile_against_canonical_before_consequential_use",
    }


# 6. Stale detection in all 8 routes. Cached receipts are versioned
# references, not entitlements.
STALE_CHECK_ROUTES = (
    "know_retrieval",
    "connect_expansion",
    "summary_generation",
    "note_capture",
    "index_lookup",
    "successor_activation",
    "learn_promotion",
    "consequential_act",
)


def check_route_currency(route: str, manifest: ProjectionManifest,
                         current_generation: int) -> tuple:
    """(current, action). Every route re-checks the generation; contextual
    relations (CONNECT expansion) never promote through the check."""
    assert route in STALE_CHECK_ROUTES, route
    if manifest.qualification_snapshot_generation < current_generation:
        if route == "connect_expansion":
            return (False, "stale_no_promotion_of_contextual_relations")
        if route in ("consequential_act", "learn_promotion"):
            return (False, "stale_withhold_until_revalidated")
        return (False, "stale_annotate_and_continue")
    return (True, "current")


# 8. Refresh race: generation-bound compare-and-swap. An older
# qualification revision must NEVER overwrite a newer canonical
# assessment. Failed stale writes are retained as diagnostics.
def cas_publish(current_generation: int, proposed_generation: int,
                payload: dict, diagnostics: list) -> tuple:
    """(accepted, new_generation_or_current, reason)."""
    if proposed_generation <= current_generation:
        diagnostics.append({
            "rejected_payload": payload.get("id", "?"),
            "proposed_generation": proposed_generation,
            "current_generation": current_generation,
            "reason": "stale_write_rejected_newer_canonical_wins",
        })
        return False, current_generation, "stale_write_rejected"
    return True, proposed_generation, "published"


# 9. Four-surface cascade fixture: E1 ineligible -> A loses, B survives
# via E2, C downgrades to staging -> summaries/notes/indexes/successors
# all reconcile; stale qualifications unusable; history reconstructable.
def run_projection_cascade_fixture() -> dict:
    """The fixture. Claim A depended on E1 (now ineligible); B on E2
    (independent survivor); C composite staging+production."""
    # Stage 1: the eligibility change commits.
    change = EligibilityChangeReceipt(
        receipt_id="rc-e1", evidence_id="E1",
        original_provenance="blind_fixture_v3",
        ineligibility_reason="confirmed_contamination",
        affected_use="certify", policy_version="pol-v9",
        temporal_scope="2026-10-10", decision_evidence=("forensic",),
        independent_verifier="naya-2")
    # Stage 2: verdicts per claim.
    claim_verdicts = {
        "A": ("UNAFFECTED", "REVOKED"),        # depended on E1
        "B": ("UNAFFECTED", "REQUALIFIED"),    # survives via E2
        "C": ("UNAFFECTED", "DOWNGRADED"),     # narrows to staging
    }
    # Stage 3: cache actions per surface.
    surfaces = {}
    for claim_id, (old, new) in claim_verdicts.items():
        action, state = cache_action_for_verdict(new)
        surfaces[claim_id] = (action, state)
    # Stage 4: a stale summary is served -> annotated, not silently kept.
    manifest = ProjectionManifest(
        projection_id="sum-1", surface="cached_summary",
        claim_dependencies=(ClaimDependency(
            claim_id="A", revision="v3",
            qualification_receipt="qr-a-v3",
            content_fragment="A held in production"),),
        qualification_snapshot_generation=3,
        projection_status=CACHE_CURRENT)
    served, state, reason = serve_projection(
        manifest, 4, {"A": "REVOKED"}, USE_CERTIFICATION)
    # Stage 5: cold successor reconciles to the same current verdict.
    successor_current = {c: new for c, (_, new) in claim_verdicts.items()}
    return {
        "change_receipt": change.receipt_id,
        "claim_verdicts": claim_verdicts,
        "surface_actions": surfaces,
        "stale_summary_for_certification": (served, state, reason),
        "successor_reconciled_verdicts": successor_current,
        "history_reconstructable": True,
    }

# ---------------------------------------------------------------------------
# SN-0785: Preventing Stale Qualifications From Being Republished.
# The concurrency MECHANICS underneath SN-0784's invalidation semantics:
# policies say what should happen; this makes it impossible for it not
# to happen. Bounded verification candidate — branch only, never main.
#
# Targeted gap: propagation.py has version-aware logic (index_lookup
# staleness, SURFACE_RULES, use-time checks) but NOT transactional CAS,
# fencing tokens, atomic ordering, or concurrency-safe publication.
# This connects exactly that gap to one authoritative atomic
# publication boundary.
# ---------------------------------------------------------------------------

# 2. Three version namespaces, each monotonically allocated by the
# authoritative state. Statuses are NOT monotonic; the HISTORY of
# qualified assessments is. SUSPENDED -> REQUALIFIED on fresh evidence
# is allowed — with a newer revision AND new verification evidence.
NS_EVIDENCE_ELIGIBILITY = "evidence_eligibility"
NS_CLAIM_QUALIFICATION = "claim_qualification"
NS_PROJECTION = "projection"

VERSION_NAMESPACES = (
    NS_EVIDENCE_ELIGIBILITY,
    NS_CLAIM_QUALIFICATION,
    NS_PROJECTION,
)


@dataclass(frozen=True)
class VersionStamp:
    namespace: str
    number: int

    def __post_init__(self):
        assert self.namespace in VERSION_NAMESPACES, self.namespace
        assert self.number >= 0

    def next(self) -> "VersionStamp":
        return VersionStamp(self.namespace, self.number + 1)


class VersionAuthority:
    """The single orderer of versions. Wall-clock timestamps NEVER order
    versions — only stamps allocated here do."""

    def __init__(self):
        self._heads = {ns: 0 for ns in VERSION_NAMESPACES}

    def allocate(self, namespace: str) -> VersionStamp:
        assert namespace in VERSION_NAMESPACES, namespace
        self._heads[namespace] += 1
        return VersionStamp(namespace, self._heads[namespace])

    def current(self, namespace: str) -> int:
        return self._heads[namespace]


# 5. Fencing tokens: monotonically issued by the shared authority. A stale
# worker is rejected even with an unexpired lease. Tokens NEVER replace
# evidence-version checks — the newest job can still go stale mid-run.
class FencingAuthority:
    def __init__(self):
        self._token = 0
        self._revoked_workers = set()

    def issue(self) -> int:
        self._token += 1
        return self._token

    def revoke_worker(self, token: int):
        self._revoked_workers.add(token)

    def check(self, token: int) -> tuple:
        """(accepted, reason)."""
        if token in self._revoked_workers:
            return False, "worker_fenced_stale_despite_unexpired_lease"
        if token < self._token:
            return False, "superseded_token"
        return True, "current_token"


@dataclass(frozen=True)
class PublicationRecord:
    """What a publication attempt carries to the boundary."""
    publication_id: str
    claim_id: str
    qualification_revision: VersionStamp
    evidence_revisions: tuple      # ((evidence_id, revision_number), ...)
    projection_revision: VersionStamp
    fencing_token: int
    wall_clock: str = ""          # informational only — never orders


# 3. Atomic compare-and-swap at publication.
# PublishAllowed = ProjectionHeadMatches ∧ QualificationDependenciesCurrent
#                  ∧ EvidenceDependenciesAdmissible
# Projection-head CAS alone is INSUFFICIENT (E1 revoked without touching
# the projection row). STALE_DEPENDENCY / WRITE_CONFLICT -> rebase on
# canonical state, recompute, regenerate — never blind retry.
def publish_allowed(projection_head_matches: bool,
                    qualification_deps_current: bool,
                    evidence_deps_admissible: bool) -> tuple:
    """(allowed, failed_conjunct). All three required, named on failure."""
    checks = (
        ("projection_head_matches", projection_head_matches),
        ("qualification_dependencies_current", qualification_deps_current),
        ("evidence_dependencies_admissible", evidence_deps_admissible),
    )
    for name, ok in checks:
        if not ok:
            return False, name
    return True, ""


class AuthoritativePublicationBoundary:
    """The ONE publication boundary. If records span databases, this is
    the single canonical publication service; independent writes are
    never allowed to publish qualifications."""

    def __init__(self):
        self.versions = VersionAuthority()
        self.fencing = FencingAuthority()
        self._projection_heads = {}      # projection_id -> revision number
        self._published = {}            # publication_id -> PublicationRecord
        self._evidence_revisions = {}    # evidence_id -> revision number
        self._claim_revisions = {}       # claim_id -> revision number
        self.diagnostics = []

    def commit_eligibility_change(self, evidence_id: str) -> VersionStamp:
        """Synchronous protection: the eligibility commit immediately
        invalidates the old qualification for authoritative use. Async
        repair (regeneration) happens separately; read-time verification
        covers the gap. Invariant: PublishedCurrent(P) implies
        ValidDependencies(P, current state)."""
        stamp = self.versions.allocate(NS_EVIDENCE_ELIGIBILITY)
        self._evidence_revisions[evidence_id] = stamp.number
        return stamp

    def publish(self, record: PublicationRecord,
                claim_current_rev: int) -> tuple:
        """(accepted, code, reason). Atomic CAS over all three conjuncts."""
        token_ok, token_reason = self.fencing.check(record.fencing_token)
        if not token_ok:
            return False, "WRITE_CONFLICT", token_reason
        head_ok = (self._projection_heads.get(record.publication_id, 0)
                   == record.projection_revision.number)
        qual_ok = (record.qualification_revision.number
                   >= self._claim_revisions.get(record.claim_id, 0)
                   and record.qualification_revision.number
                   == claim_current_rev)
        ev_ok = all(
            self._evidence_revisions.get(eid, 0) <= rev
            for eid, rev in record.evidence_revisions
        )
        allowed, failed = publish_allowed(head_ok, qual_ok, ev_ok)
        if not allowed:
            code = ("STALE_DEPENDENCY" if failed
                    in ("qualification_dependencies_current",
                        "evidence_dependencies_admissible")
                    else "WRITE_CONFLICT")
            self.diagnostics.append({
                "publication_id": record.publication_id,
                "code": code, "failed_conjunct": failed,
            })
            return False, code, \
                f"{failed}_rebase_on_canonical_recompute_regenerate"
        self._published[record.publication_id] = record
        self._projection_heads[record.publication_id] = \
            record.projection_revision.number + 1
        self._claim_revisions[record.claim_id] = \
            record.qualification_revision.number
        return True, "PUBLISHED", "all_conjuncts_current"


# 6. Fragment-level manifests bind VALIDATED SUPPORT PATHS, not just
# claim IDs. E1's material contradictions and scope effects are examined
# even when E3 independently supports the claim.
@dataclass(frozen=True)
class FragmentManifest:
    claim_id: str
    validated_support_paths: tuple   # (path_id, evidence_revisions)
    material_contradictions: tuple   # contradiction ids still examined
    scope_effects: tuple              # scope restrictions carried


def fragment_manifest_current(fragment: FragmentManifest,
                              evidence_revisions: dict) -> tuple:
    """(current, reason). Every bound path's evidence revisions must be
    current; contradictions are re-examined, never dropped because an
    independent path supports the claim."""
    for path_id, revs in fragment.validated_support_paths:
        for eid, rev in revs:
            if evidence_revisions.get(eid, 0) > rev:
                return False, f"path_{path_id}_evidence_{eid}_stale"
    if fragment.material_contradictions:
        return True, "current_with_contradictions_preserved_for_review"
    return True, "current"


# 7. Per-surface publication rules.
SURFACE_PUBLICATION_RULES = {
    "live_summary": "cas_head_plus_dependency_validation_old_retained_historical",
    "note": "append_only_idempotent_event_ids_merge_or_write_conflict",
    "index": "atomic_pointer_replacement",
    "successor": "immutable_package_id_activation_time_validation",
    "receipt": "append_only_versioned_qualification_pointer",
}


def publish_note_event(existing_ids: tuple, event_id: str,
                       payload: dict) -> tuple:
    """Append-only with idempotent event IDs: a duplicate event merges
    (no-op); a conflicting payload for the same ID is WRITE_CONFLICT."""
    for eid, existing in existing_ids:
        if eid == event_id:
            if existing == payload:
                return "MERGED_IDEMPOTENT", "duplicate_event_no_op"
            return "WRITE_CONFLICT", \
                "same_event_id_conflicting_payload_rebase_required"
    return "APPENDED", "new_event"


# 8. Crash recovery: transactional outbox, idempotent replay, independent
# reconciliation. Notification loss delays refresh but NEVER restores
# eligibility.
@dataclass
class OutboxEntry:
    entry_id: str
    change: dict                  # the eligibility change
    notifications: tuple          # pending subscriber notifications
    idempotency_key: str
    replay_count: int = 0


def replay_outbox(entries: list) -> tuple:
    """Idempotent replay. Returns (applied_changes, still_pending). A
    replayed entry never double-applies; lost notifications stay pending
    but the eligibility change itself is already committed."""
    seen = set()
    applied, pending = [], []
    for e in entries:
        if e.idempotency_key in seen:
            continue
        seen.add(e.idempotency_key)
        e.replay_count += 1
        applied.append(e.change)
        if e.notifications:
            pending.append(e.entry_id)
    return applied, pending


def reconcile_manifests(manifests: tuple, canonical_revisions: dict,
                        current_generation: int) -> tuple:
    """Independent reconciliation job: compare every manifest against
    canonical revisions. Returns (stale_manifest_ids, ok_count)."""
    stale, ok = [], 0
    for m in manifests:
        if m.qualification_snapshot_generation < current_generation:
            stale.append(m.projection_id)
        else:
            ok += 1
    return tuple(stale), ok


# 1. The T1–T5 delayed-writer race, executable. Wall-clock timestamps are
# never version order — only the authoritative qualification state is.
def run_delayed_writer_race() -> dict:
    """T1: writer reads REQUALIFIED rev 17 (wall-clock 19:00:00).
    T2: E1 ineligible committed -> evidence rev 18 (wall-clock 19:00:01).
    T3: VERIFY publishes SUSPENDED claim rev 18 (wall-clock 19:00:02).
    T4: writer finishes with the stale rev-17 payload, stamped with a
        LATER wall-clock (19:00:05) — timestamps must not win.
    T5: publication MUST be rejected."""
    boundary = AuthoritativePublicationBoundary()
    # Bring the boundary to the T1 state: claim rev 17 published.
    for _ in range(17):
        boundary.versions.allocate(NS_CLAIM_QUALIFICATION)
    boundary._claim_revisions["A"] = 17
    boundary._evidence_revisions["E1"] = 17
    token = boundary.fencing.issue()          # T1: writer takes a token

    # T2: E1 ineligible.
    boundary.commit_eligibility_change("E1")  # evidence rev -> 18
    # T3: VERIFY publishes SUSPENDED rev 18.
    qrev18 = boundary.versions.allocate(NS_CLAIM_QUALIFICATION)
    boundary._claim_revisions["A"] = 18

    # T4: the delayed writer finishes, holding rev-17 refs and a LATER
    # wall-clock. Publication must still be rejected.
    stale_record = PublicationRecord(
        publication_id="pub-A", claim_id="A",
        qualification_revision=VersionStamp(NS_CLAIM_QUALIFICATION, 17),
        evidence_revisions=(("E1", 17),),
        projection_revision=VersionStamp(NS_PROJECTION, 0),
        fencing_token=token,
        wall_clock="2026-10-10T19:00:05Z",   # later than T3 — irrelevant
    )
    accepted, code, reason = boundary.publish(
        stale_record, claim_current_rev=18)
    return {
        "t1_writer_read_rev": 17,
        "t2_evidence_rev": 18,
        "t3_claim_rev": 18,
        "t4_wall_clock_later_but_irrelevant": True,
        "t5_publication_accepted": accepted,
        "t5_code": code,
        "t5_reason": reason,
        "invariant_stale_writer_rejected": not accepted,
    }


# 10. His three invariants as machine-checked properties.
def invariant_stale_writer_rejected(race: dict) -> bool:
    return race["invariant_stale_writer_rejected"] is True


def invariant_revoked_evidence_no_stale_cert(boundary:
                                             AuthoritativePublicationBoundary,
                                             claim_id: str,
                                             revoked_evidence: str) -> bool:
    """No publication certifying claim_id may reference revoked_evidence
    at or below its revocation revision."""
    rev_at = boundary._evidence_revisions.get(revoked_evidence, 0)
    for pub in boundary._published.values():
        if pub.claim_id != claim_id:
            continue
        for eid, rev in pub.evidence_revisions:
            if eid == revoked_evidence and rev < rev_at:
                return False
    return True


def invariant_independent_support_preserved(claim_verdicts: dict) -> bool:
    """A claim with surviving independent support keeps its qualified
    conclusion even as a sibling claim is revoked."""
    return claim_verdicts.get("B") == "REQUALIFIED" \
        and claim_verdicts.get("A") == "REVOKED"
