"""Provenance-preserving intelligence propagation (spec).

Principle: "Uncertainty follows evidence dependencies. Eligibility follows
sufficient independent support. Authority remains with LAW."

Separates three things per claim, preserved across every projection:
  1. where it came from (source_refs, dependency_edges)
  2. whether its supporting evidence is independent (independence_state)
  3. whether it has sufficient valid support for its intended use
     (support_sets + region verdicts + strongest defensible conclusion)

Scope-precision layer (Shawn, 2026-10-10):
  "Evidence may support a claim within its demonstrated scope, but it cannot
  automatically establish that claim outside that scope."
  - Meaning envelope: seven scope dimensions on every claim and support set.
    The quantifier is part of the claim and can never be silently changed.
  - For ALL x in D, P(x) with evidence only on S subset of D: the evidence
    supports ALL x in S, P(x). It never upgrades to ALL x in D, P(x).
  - One verified counterexample refutes a universal; 40 successes do not
    prove it. 40-of-40 passed != "100% of production situations are safe."
  - PARTIALLY_SUPPORTS carries an explicit coverage predicate, NOT a
    fractional probability: 2-of-9 nodes verified != "22.2% true". The
    conjunction "all nine" remains unproven.
  - Strongest defensible conclusion: the strongest proposition the admissible
    evidence actually entails — never an aggregate confidence score.

Composes with:
  revocation.py   — six verdicts (UNAFFECTED / REQUALIFIED / DOWNGRADED /
                    INSUFFICIENT_DATA / SUSPENDED / REVOKED). A region can be
                    SUPPORTED while the overall claim is INSUFFICIENT_DATA.
  uncertainty.py  — four assessment states, three-valued propagation,
                    verdict_for_qualification().
  authority.py    — five capabilities, purpose-bound authorization.
  kernel/brain_registry.py — ALLOWED_RELATIONSHIPS. The four propagation
                    relationships map onto existing CONNECT contracts; no
                    parallel edge registry is created.

This module is SPEC + deterministic machinery. NOT wired into kernel/,
KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Relationship types -> existing CONNECT contracts.
# ---------------------------------------------------------------------------
# The four propagation relationships map onto kernel/brain_registry.py
# ALLOWED_RELATIONSHIPS. PARTIALLY_SUPPORTS is a SUPPORTS edge that carries
# a mandatory explicit coverage predicate (which regions it covers) — it is
# not a fractional probability and not a separate registry.
RELATIONSHIP_TO_CONNECT = {
    "MENTIONS": "CONTEXTUALIZES",               # historical reference only
    "DERIVED_FROM": "DERIVED_FROM",             # relies on earlier material
    "REQUIRES_SUPPORT_FROM": "DEPENDS_ON",      # conclusion needs it (AND)
    "INDEPENDENTLY_CORROBORATED_BY": "SUPPORTS",  # separate path (OR)
    "PARTIALLY_SUPPORTS": "SUPPORTS",           # + mandatory coverage predicate
}

# Exposure semantics per propagation relationship. Composes with
# uncertainty.EDGE_EXPOSURE_SEMANTICS: MENTIONS behaves like CITES
# (no propagation); DERIVED_FROM / REQUIRES_SUPPORT_FROM create possible
# exposure; genuine independent corroboration propagates nothing — but a
# corroboration built on a hidden shared origin was never independent
# (see detect_false_corroboration).
RELATIONSHIP_EXPOSURE = {
    "MENTIONS": "no_propagation",
    "DERIVED_FROM": "creates_possible_exposure",
    "REQUIRES_SUPPORT_FROM": "creates_possible_exposure",
    "INDEPENDENTLY_CORROBORATED_BY": "no_propagation_if_genuinely_independent",
    "PARTIALLY_SUPPORTS": "no_propagation_within_coverage",
}

# Independence states, shared with uncertainty.py's four assessment states.
CLEARED = "independently_cleared"
POSSIBLE = "possibly_compromised"
UNASSESSED = "unassessed"
CONFIRMED = "confirmed_compromised"

# Region verdicts: what the admissible evidence says about one region of a
# claim's scope. Distinct from the six qualification verdicts, which judge
# the standing of the qualification as a whole.
REGION_VERDICTS = (
    "SUPPORTED",       # sufficient independent evidence covers this region
    "REFUTED",         # sufficient evidence contradicts the claim here
    "CONFLICTED",      # sufficient evidence both ways — needs adjudication
    "UNDETERMINED",    # no sufficient evidence either way (yet)
    "NOT_APPLICABLE",  # region outside the claim's meaning
)

# Quantifiers. The quantifier is part of the claim's meaning.
QUANTIFIERS = ("universal", "existential", "statistical", "bounded_observation")

# The two propagation metrics, paired. Scope inflation is the characteristic
# failure of this layer: asserting a broader scope than the evidence covers.
PROPAGATION_METRICS = (
    "false_qualification_rate",       # uncertain evidence treated as proof
    "unnecessary_qualification_loss",  # valid conclusions discarded anyway
    "scope_inflation_errors",         # asserted scope exceeds supported scope
)


# ---------------------------------------------------------------------------
# Meaning envelope: the seven scope dimensions of a claim or evidence.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MeaningEnvelope:
    """Structured scope. A dimension set to "any" is genuinely general along
    that axis (demonstrated across it), not merely unspecified."""
    component: str = "any"     # which part: KNOW, ACT, all-nine-nodes, ...
    environment: str = "any"   # staging, production, ...
    population: str = "any"    # 40-controlled-cases, all-production-traffic, ...
    behavior: str = "any"      # rejects-ineligible-evidence, ...
    time: str = "any"          # 2026-10-10, long-term, ...
    conditions: str = "any"    # controlled, adversarial, ...
    outcome: str = "any"       # rejection, accuracy>=0.99, ...
    runtime: str = "any"       # runtime version the evidence was produced under

    DIMENSIONS = ("component", "environment", "population", "behavior",
                  "time", "conditions", "outcome", "runtime")

    @staticmethod
    def _dim_covers(s_val: str, o_val: str) -> bool:
        """One dimension covers another. '+'-separated values are sets:
        'KNOW+ACT' covers 'KNOW' but not vice versa. 'any' on either side
        covers (genuinely general evidence, or an unconstrained target)."""
        if s_val == "any" or o_val == "any":
            return True
        return set(o_val.split("+")) <= set(s_val.split("+"))

    def covers(self, other: "MeaningEnvelope") -> bool:
        """This envelope covers `other` iff every dimension covers it. A
        narrower evidence scope never covers a broader claim scope — but an
        unconstrained obligation dimension is satisfied by specific
        evidence. Cross-evidence consistency (same runtime/policy/predicate
        across combined sets) is the compatibility gate's job, not
        coverage's."""
        return all(self._dim_covers(getattr(self, d), getattr(other, d))
                   for d in self.DIMENSIONS)

    def mismatch_vs(self, other: "MeaningEnvelope") -> tuple:
        """Dimensions where this envelope is narrower than `other` — the
        explicit scope gap. Empty means full coverage."""
        return tuple(d for d in self.DIMENSIONS
                     if not self._dim_covers(getattr(self, d),
                                             getattr(other, d)))


@dataclass(frozen=True)
class ClaimRegion:
    """One region of a claim's scope, assessed independently."""
    region_id: str
    envelope: MeaningEnvelope


# ---------------------------------------------------------------------------
# Support sets: OR between sets, AND within a set.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SupportSet:
    """One combination of evidence that can independently support (or
    contradict) the regions it covers.

    polarity "supports":    the set argues the claim holds in its regions.
    polarity "contradicts": the set argues the claim fails in its regions
                            (a verified counterexample).

    For statistical claims, a support set additionally needs
    sample_representative (the sample represents the claimed population) and
    uncertainty_bounds_stated (explicit bounds, not a bare rate). Without
    both, the set can support only the bounded observation ("99 of 99
    sampled passed"), never the population rate.
    """
    set_id: str
    evidence_refs: tuple
    covers: tuple                      # region_ids this set addresses
    scope: MeaningEnvelope = MeaningEnvelope()  # demonstrated scope of the set
    polarity: str = "supports"         # supports | contradicts
    sample_representative: bool = False
    uncertainty_bounds_stated: bool = False
    policy_version: str = ""           # governing policy the evidence was
                                       # produced under (compatibility gate)

    def __post_init__(self):
        assert self.polarity in ("supports", "contradicts"), self.polarity


@dataclass(frozen=True)
class DependencyEdge:
    """A typed edge from a claim to evidence (or claim to claim). The
    relationship determines propagation; the CONNECT contract is the
    canonical edge type in the graph."""
    from_id: str       # claim or artifact
    to_id: str         # evidence or source claim
    relationship: str  # one of RELATIONSHIP_TO_CONNECT keys

    def __post_init__(self):
        assert self.relationship in RELATIONSHIP_TO_CONNECT, self.relationship

    def connect_contract(self) -> str:
        return RELATIONSHIP_TO_CONNECT[self.relationship]

    def exposure_semantics(self) -> str:
        return RELATIONSHIP_EXPOSURE[self.relationship]


@dataclass
class ClaimEnvelope:
    """The evidence-support envelope carried by every claim on every surface.

    claim_scope is the FULL asserted scope (with quantifier). regions
    partition it. support_sets declare which regions they cover and with
    what polarity. historical_dependencies is append-only: everything that
    ever contributed, never deleted — revocation removes certification
    rights, never observations.
    """
    claim_id: str
    claim_scope: MeaningEnvelope
    quantifier: str = "universal"
    regions: tuple = ()                # ClaimRegion, partition of claim_scope
    support_sets: tuple = ()           # SupportSet
    source_refs: tuple = ()            # original sources, exact provenance
    historical_dependencies: tuple = ()  # append-only
    dependency_edges: tuple = ()       # DependencyEdge
    policy_version: str = ""
    assessment_receipt: str = ""

    def __post_init__(self):
        assert self.quantifier in QUANTIFIERS, self.quantifier


# ---------------------------------------------------------------------------
# Support-set sufficiency.
# ---------------------------------------------------------------------------
def set_sufficient(support_set: SupportSet, region: ClaimRegion,
                   independence_of: dict) -> tuple:
    """(sufficient, reason). A set is sufficient for a region iff every
    evidence item is independently cleared AND the set's demonstrated scope
    covers the region. Scope mismatch is not compromise — it is simply not
    support for that region."""
    if region.region_id not in support_set.covers:
        return False, "region_not_covered"
    for ev in support_set.evidence_refs:
        state = independence_of.get(ev, UNASSESSED)
        if state != CLEARED:
            return False, f"evidence_{ev}_is_{state}"
    gap = support_set.scope.mismatch_vs(region.envelope)
    if gap:
        return False, f"scope_mismatch:{','.join(gap)}"
    return True, "sufficient"


def detect_false_corroboration(support_sets: tuple, region_id: str,
                               origin_of: dict) -> tuple:
    """Two support sets that share a hidden originating source are not two
    independent paths — the OR collapses to one genuine path. Returns pairs
    of set_ids whose claimed independent corroboration is false for this
    region. (Anti-citogenesis: internal repetition is not corroboration.)"""
    covering = [s for s in support_sets
                if region_id in s.covers and s.polarity == "supports"]
    false_pairs = []
    for i, a in enumerate(covering):
        for b in covering[i + 1:]:
            origins_a = {origin_of.get(e, e) for e in a.evidence_refs}
            origins_b = {origin_of.get(e, e) for e in b.evidence_refs}
            if origins_a & origins_b:
                false_pairs.append((a.set_id, b.set_id))
    return tuple(false_pairs)


def genuine_paths(covering_sets: tuple, origin_of: dict) -> tuple:
    """Group covering support sets by origin signature. Each group is one
    genuine independent path, no matter how many sets repeat it. A claim of
    'two independent evaluations' needs two groups, not two sets."""
    groups: dict = {}
    for s in covering_sets:
        sig = frozenset(origin_of.get(e, e) for e in s.evidence_refs)
        groups.setdefault(sig, []).append(s.set_id)
    return tuple(sorted(groups.values()))


# ---------------------------------------------------------------------------
# Region assessment.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RegionAssessment:
    region_id: str
    verdict: str          # one of REGION_VERDICTS
    detail: str           # why: e.g. held_pending_review, support_disqualified
    sufficient_sets: tuple = ()
    genuine_paths: int = 0  # distinct origin-groups among covering sets


def assess_region(region: ClaimRegion, envelope: ClaimEnvelope,
                  independence_of: dict, origin_of: dict) -> RegionAssessment:
    """Assess one region. Uncertainty propagates through dependencies;
    qualification is recomputed from actual independent support.

    Sets sharing a hidden origin collapse to one genuine path (grouped, not
    discarded): repetition is not corroboration, but one valid path still
    supports the claim."""
    covering = [s for s in envelope.support_sets if region.region_id in s.covers]
    if not covering:
        return RegionAssessment(region.region_id, "UNDETERMINED", "no_coverage")

    paths = genuine_paths(covering, origin_of)
    by_id = {s.set_id: s for s in covering}

    def path_sufficient(path) -> tuple:
        ok_sets = []
        for sid in path:
            s = by_id[sid]
            ok, _ = set_sufficient(s, region, independence_of)
            if ok:
                ok_sets.append(sid)
        return ok_sets

    sup, con = [], []
    for path in paths:
        # One vote per genuine path, no matter how many sets repeat it.
        ok_in_path = [sid for sid in path
                      if by_id[sid].polarity == "supports"
                      and set_sufficient(by_id[sid], region,
                                         independence_of)[0]]
        if ok_in_path:
            sup.append(ok_in_path[0])
    for s in covering:
        if s.polarity == "contradicts":
            ok, _ = set_sufficient(s, region, independence_of)
            if ok:
                con.append(s.set_id)

    n_paths = len(paths)
    if sup and con:
        return RegionAssessment(region.region_id, "CONFLICTED",
                                "sufficient_evidence_both_ways",
                                tuple(sup + con), n_paths)
    if con:
        return RegionAssessment(region.region_id, "REFUTED",
                                "verified_counterexample", tuple(con), n_paths)
    if sup:
        return RegionAssessment(region.region_id, "SUPPORTED",
                                "sufficient_independent_support",
                                tuple(sup), n_paths)

    # No sufficient set: characterize the blocker without inventing proof.
    states = {independence_of.get(e, UNASSESSED)
              for s in covering for e in s.evidence_refs}
    if CONFIRMED in states:
        return RegionAssessment(region.region_id, "UNDETERMINED",
                                "support_disqualified", (), n_paths)
    if POSSIBLE in states or UNASSESSED in states:
        return RegionAssessment(region.region_id, "UNDETERMINED",
                                "held_pending_review", (), n_paths)
    return RegionAssessment(region.region_id, "UNDETERMINED",
                            "scope_or_quality_gap", (), n_paths)


# ---------------------------------------------------------------------------
# Strongest defensible conclusion + claim-level verdict.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ClaimAssessment:
    claim_id: str
    region_assessments: tuple   # RegionAssessment per region
    strongest_conclusion: str   # plain statement of the bounded claim
    strongest_scope: tuple      # region_ids that are SUPPORTED
    verdict: str                # one of revocation.VERDICTS
    notes: tuple = ()


def strongest_defensible_conclusion(envelope: ClaimEnvelope,
                                    assessments: tuple) -> tuple:
    """The strongest proposition the admissible evidence actually entails:
    the claim narrowed to its SUPPORTED regions, stated with its quantifier
    intact. Never an aggregate confidence score."""
    supported = [a for a in assessments if a.verdict == "SUPPORTED"]
    region_ids = tuple(a.region_id for a in supported)
    if not supported:
        return ("no region has sufficient independent support", region_ids)
    if envelope.quantifier == "existential":
        first = supported[0]
        return (f"exists: {envelope.claim_id} holds in {first.region_id} "
                f"(one verified example; nothing claimed elsewhere)",
                region_ids)
    return (f"{envelope.claim_id} holds in: "
            f"{', '.join(region_ids)} "
            f"(quantifier '{envelope.quantifier}' applies ONLY within these "
            f"regions; all other regions unestablished)",
            region_ids)


def _recomputation_triggered(envelope: ClaimEnvelope,
                             independence_of: dict) -> bool:
    """True if any historical dependency went through a compromise incident
    (confirmed or possibly compromised). Merely unassessed evidence never
    went through recomputation — it was never assessed at all."""
    return any(independence_of.get(e, UNASSESSED) in (CONFIRMED, POSSIBLE)
               for e in envelope.historical_dependencies)


def evaluate_claim(envelope: ClaimEnvelope, independence_of: dict,
                   origin_of: dict | None = None) -> ClaimAssessment:
    """Full evaluation: region verdicts -> strongest defensible conclusion ->
    one of the six qualification verdicts.

    Composition rule: region verdicts describe evidence; the six verdicts
    describe certification standing. A region can be SUPPORTED while the
    overall claim is INSUFFICIENT_DATA (the universal claim needs ALL
    regions; the evidence covers only some).
    """
    origin_of = origin_of or {}
    assessments = tuple(assess_region(r, envelope, independence_of, origin_of)
                        for r in envelope.regions)
    by_verdict = {}
    for a in assessments:
        by_verdict.setdefault(a.verdict, []).append(a.region_id)

    conclusion, strong_scope = strongest_defensible_conclusion(envelope,
                                                              assessments)
    notes = []
    recomputed = _recomputation_triggered(envelope, independence_of)

    q = envelope.quantifier
    if q == "existential":
        if by_verdict.get("SUPPORTED"):
            verdict = "REQUALIFIED" if recomputed else "UNAFFECTED"
        elif any(a.detail == "held_pending_review" for a in assessments):
            verdict = "SUSPENDED"
        else:
            verdict = "INSUFFICIENT_DATA"
    elif q == "statistical":
        verdict, extra = _evaluate_statistical(envelope, assessments,
                                              independence_of, recomputed)
        notes.extend(extra)
    else:  # universal (and bounded_observation treated strictly per region)
        n_regions = len(envelope.regions)
        n_supported = len(by_verdict.get("SUPPORTED", []))
        if n_regions > 0 and n_supported == n_regions:
            verdict = "REQUALIFIED" if recomputed else "UNAFFECTED"
        elif n_supported == 0:
            if by_verdict.get("REFUTED"):
                verdict = "REVOKED"
                notes.append("no supported region remains; verified "
                             "counterexample exists")
            elif any(a.detail == "support_disqualified" for a in assessments):
                verdict = "REVOKED"
                notes.append("required independent support disqualified; "
                             "observations preserved, certification lost")
            elif any(a.detail == "held_pending_review" for a in assessments):
                verdict = "SUSPENDED"
            else:
                verdict = "INSUFFICIENT_DATA"
        else:
            # Some regions hold on sufficient independent evidence while
            # others do not: narrow the claim, never silently keep the whole.
            verdict = "DOWNGRADED"
            if by_verdict.get("REFUTED"):
                notes.append("refuted regions excluded from the defensible claim")
            if any(a.detail == "support_disqualified" for a in assessments):
                notes.append("disqualified regions excluded; surviving scope "
                             "re-anchored on remaining independent support")
            if any(a.detail == "held_pending_review" for a in assessments):
                notes.append("held regions excluded pending review")
            notes.append("narrower claim supportable on supported regions only")

    # DOWNGRADED must name the surviving scope; it is not a vague demotion.
    if verdict == "DOWNGRADED" and strong_scope:
        notes.append(f"surviving_scope: {', '.join(strong_scope)}")

    return ClaimAssessment(
        claim_id=envelope.claim_id,
        region_assessments=assessments,
        strongest_conclusion=conclusion,
        strongest_scope=strong_scope,
        verdict=verdict,
        notes=tuple(notes),
    )


def _evaluate_statistical(envelope: ClaimEnvelope, assessments: tuple,
                         independence_of: dict,
                         recomputed: bool) -> tuple:
    """A statistical claim needs a representative sample AND explicit
    uncertainty bounds. 99 successes != a 99% population rate. Without both,
    the rate claim is INSUFFICIENT_DATA; the bounded observation
    ("99 of 99 sampled passed") may still be SUPPORTED."""
    notes = []
    # The bounded observation: what was literally measured.
    if any(a.verdict == "SUPPORTED" for a in assessments):
        bounded = (f"bounded observation SUPPORTED: the measured sample "
                   f"passed; no population rate is established")
        notes.append(bounded)
    # The rate claim: needs representativeness + bounds on a sufficient set.
    rate_ok = False
    for s in envelope.support_sets:
        if (s.sample_representative and s.uncertainty_bounds_stated
                and all(independence_of.get(e, UNASSESSED) == CLEARED
                        for e in s.evidence_refs)):
            rate_ok = True
    if rate_ok:
        return ("REQUALIFIED" if recomputed else "UNAFFECTED", notes)
    if any(a.detail == "held_pending_review" for a in assessments):
        return ("SUSPENDED", notes + ["population rate held pending review"])
    return ("INSUFFICIENT_DATA",
            notes + ["sample not shown representative or bounds unstated: "
                     "rate claim unestablished"])


# ---------------------------------------------------------------------------
# Scope-inflation detection.
# ---------------------------------------------------------------------------
def scope_inflation_check(asserted: MeaningEnvelope,
                          strongest_scope_regions: tuple,
                          region_envelopes: dict) -> tuple:
    """Dimensions in which `asserted` exceeds the strongest defensible
    conclusion. A summary that drops the word 'staging' is caught here:
    environment is an inflated dimension."""
    if not strongest_scope_regions:
        return ("no_supported_scope",)
    # Union of supported region envelopes: a dimension is supported only if
    # every asserted value along it is covered by some supported region.
    inflated = []
    for d in MeaningEnvelope.DIMENSIONS:
        asserted_v = getattr(asserted, d)
        if asserted_v == "any":
            continue
        covered = any(MeaningEnvelope._dim_covers(
            getattr(region_envelopes[r], d), asserted_v)
            for r in strongest_scope_regions)
        if not covered:
            inflated.append(d)
    return tuple(inflated)


# ---------------------------------------------------------------------------
# Four-surface propagation rules (centralized policy).
# ---------------------------------------------------------------------------
SURFACE_RULES = {
    "summary": {
        "must_preserve": ("claim_id", "material_qualifiers", "valid_support",
                          "unresolved_dependencies", "scope_limits"),
        "must_never": ("present_uncertain_evidence_as_unqualified_assertion",
                       "drop_scope_qualifiers",
                       "combine_claims_into_new_conclusion_without_qualification"),
        "policy": "compress_words_not_uncertainty",
    },
    "index": {
        "must_preserve": ("evidence_family_ids", "current_eligibility",
                          "qualification_version", "canonical_claim_pointer"),
        "must_never": ("treat_rank_as_proof_of_truth",
                       "serve_stale_cached_verdict_as_current"),
        "policy": "retrieve_first_qualify_separately",
    },
    "smart_note": {
        "must_preserve": ("original_provenance", "derived_from_links",
                          "claim_level_assessment", "separately_qualified_support"),
        "must_never": ("auto_promote_copied_conclusion",
                       "count_repetition_as_corroboration"),
        "policy": "preserve_lineage",
    },
    "successor_package": {
        "must_preserve": ("current_claim", "exact_scope",
                          "eligible_independent_evidence",
                          "undetermined_or_revoked_contributions",
                          "policy_version", "remaining_uncertainty",
                          "required_checks_before_consequential_action"),
        "must_never": ("freeze_old_eligible_verdict_as_permanent_authority",
                       "certify_through_uncertainty_bearing_source"),
        "policy": "revalidate_at_use",
    },
}


def validate_summary(summary_claims: tuple, assessments: dict,
                     region_envelopes: dict) -> tuple:
    """Check summarized claims against their assessments. Each summary claim
    is (claim_id, asserted_envelope). Returns violation strings; empty means
    the summary preserves uncertainty and scope. A summary that drops the
    word 'staging' is caught as scope inflation on the environment
    dimension."""
    violations = []
    for claim_id, asserted in summary_claims:
        a = assessments.get(claim_id)
        if a is None:
            violations.append(f"{claim_id}: no assessment — cannot summarize")
            continue
        inflated = scope_inflation_check(asserted, a.strongest_scope,
                                         region_envelopes)
        if inflated == ("no_supported_scope",):
            violations.append(f"{claim_id}: asserts a claim with no "
                              f"supported scope at all")
        elif inflated:
            violations.append(
                f"{claim_id}: scope inflation on {','.join(inflated)} — "
                f"strongest defensible scope is {a.strongest_scope}")
        for ra in a.region_assessments:
            if ra.verdict not in ("REFUTED", "CONFLICTED"):
                continue
            renv = region_envelopes[ra.region_id]
            overlaps = any(
                getattr(asserted, d) == "any"
                or getattr(renv, d) in ("any", getattr(asserted, d))
                for d in MeaningEnvelope.DIMENSIONS)
            if overlaps:
                violations.append(
                    f"{claim_id}: region {ra.region_id} is {ra.verdict} "
                    f"but the summary asserts it")
    return tuple(violations)


def index_lookup(claim_id: str, cached_entry: dict,
                 canonical_assessment: ClaimAssessment,
                 canonical_version: str) -> dict:
    """The index returns the claim, its receipts, and CURRENT eligibility.
    A stale cached verdict never overrides the canonical graph: on version
    mismatch the canonical assessment wins and the staleness is reported."""
    stale = cached_entry.get("qualification_version") != canonical_version
    return {
        "claim_id": claim_id,
        "cached_verdict": cached_entry.get("verdict"),
        "current_verdict": canonical_assessment.verdict,
        "strongest_conclusion": canonical_assessment.strongest_conclusion,
        "stale_cache_overridden": bool(stale),
        "rule": "canonical graph is authority; index never bypasses revocation",
    }


def copy_to_smart_note(envelope: ClaimEnvelope, new_note_id: str) -> ClaimEnvelope:
    """Copying a claim into a new Smart Note preserves lineage and adds no
    new proof. The copy inherits the exact support sets; repetition is not
    corroboration. The new note's claim gets a MENTIONS edge to the source,
    or DERIVED_FROM if it relies on the source's material."""
    return ClaimEnvelope(
        claim_id=f"{envelope.claim_id}@{new_note_id}",
        claim_scope=envelope.claim_scope,
        quantifier=envelope.quantifier,
        regions=envelope.regions,
        support_sets=envelope.support_sets,  # inherited unchanged: no new proof
        source_refs=envelope.source_refs,
        historical_dependencies=envelope.historical_dependencies
        + (envelope.claim_id,),
        dependency_edges=envelope.dependency_edges + (
            DependencyEdge(from_id=f"{envelope.claim_id}@{new_note_id}",
                           to_id=envelope.claim_id,
                           relationship="DERIVED_FROM"),
        ),
        policy_version=envelope.policy_version,
        assessment_receipt=envelope.assessment_receipt,
    )


def build_successor_package(envelope: ClaimEnvelope,
                            assessment: ClaimAssessment) -> dict:
    """Transfer qualified knowledge, not inherited confidence. The package
    carries everything a cold successor needs to reconstruct the
    qualification — and it must revalidate at use time, never freeze an old
    eligible verdict as permanent authority."""
    return {
        "claim_id": envelope.claim_id,
        "quantifier": envelope.quantifier,
        "exact_scope": envelope.claim_scope,
        "strongest_conclusion": assessment.strongest_conclusion,
        "strongest_scope": assessment.strongest_scope,
        "eligible_independent_evidence": sorted({
            ev for s in envelope.support_sets for ev in s.evidence_refs
        }),
        "region_verdicts": {a.region_id: (a.verdict, a.detail)
                            for a in assessment.region_assessments},
        "current_qualification_verdict": assessment.verdict,
        "policy_version": envelope.policy_version,
        "assessment_receipt": envelope.assessment_receipt,
        "required_checks_before_consequential_action": (
            "revalidate current eligibility at use time; "
            "confirm no revocation since package build; "
            "confirm scope still covers the intended use"),
        "revalidate_at_use": True,
    }


# ---------------------------------------------------------------------------
# The fundamental A/B/C example, executable.
# ---------------------------------------------------------------------------
def abc_envelope() -> ClaimEnvelope:
    """Shawn's fundamental example: A undetermined, B independently
    reproduces the outcome. C is qualified through B within B's scope.
    A stays uncertain; B stays qualified; C is NOT contaminated by A's
    history; B does NOT clear A."""
    region = ClaimRegion("r1", MeaningEnvelope(
        component="brain-index", environment="staging",
        population="controlled-cases", behavior="index-repair",
        time="2026-10-10", conditions="controlled", outcome="check-passes"))
    return ClaimEnvelope(
        claim_id="CLAIM-C",
        claim_scope=region.envelope,
        quantifier="bounded_observation",
        regions=(region,),
        support_sets=(
            SupportSet(set_id="SUPPORT-A", evidence_refs=("EVID-A",),
                       covers=("r1",), scope=region.envelope),
            SupportSet(set_id="SUPPORT-B", evidence_refs=("EVID-B",),
                       covers=("r1",), scope=region.envelope),
        ),
        source_refs=("EVID-A", "EVID-B"),
        historical_dependencies=("EVID-A", "EVID-B"),
        dependency_edges=(
            DependencyEdge("CLAIM-C", "EVID-A", "MENTIONS"),
            DependencyEdge("CLAIM-C", "EVID-B",
                           "INDEPENDENTLY_CORROBORATED_BY"),
        ),
        policy_version="POLICY-SHA",
        assessment_receipt="RECEIPT-ABC",
    )


def abc_matrix() -> dict:
    """C's verdict under every A/B independence combination. The decisive
    property: revoking A never revokes C while B is sufficient; revoking B
    while A stays undetermined costs C its independent qualification."""
    results = {}
    for a_state, b_state in (
            (UNASSESSED, CLEARED), (CLEARED, CLEARED),
            (CONFIRMED, CLEARED), (UNASSESSED, UNASSESSED),
            (CLEARED, CONFIRMED), (CONFIRMED, CONFIRMED),
            (UNASSESSED, CONFIRMED), (POSSIBLE, CLEARED)):
        env = abc_envelope()
        independence_of = {"EVID-A": a_state, "EVID-B": b_state}
        assessment = evaluate_claim(env, independence_of,
                                    {"EVID-A": "origin-a",
                                     "EVID-B": "origin-b"})
        results[(a_state, b_state)] = assessment.verdict
    return results


# ---------------------------------------------------------------------------
# Composition layer: combining partial evidence without inventing completeness.
# ---------------------------------------------------------------------------
# Central rule: "The union of independently supported conclusions may
# establish a broader conclusion only when the evidence covers every required
# part of that conclusion, uses compatible definitions, and satisfies any
# necessary cross-part requirements."
#
# QUALIFIED = Coverage ∧ Evidence admissibility ∧ Compatibility ∧ Composition
# validity. Three separate things: (1) evidence validity — authentic,
# applicable, independently qualified; (2) coverage completeness — the
# combined evidence covers the entire claim; (3) logical sufficiency — that
# coverage actually establishes the broader proposition. (1)+(2) do NOT imply
# (3): some properties are NONCOMPOSITIONAL. Component tests cannot establish
# joint behavior without interface tests, a sound composition argument, or
# end-to-end tests. Never assume it.
#
# Principle: "Combine evidence by verified coverage and valid logical
# composition — not by quantity, agreement, or confidence alone."
#
# Extends (not replaces) the Intelligent Graph Contract V1 (typed
# relationships, PROOF dimension) and the Intelligent Block Protocol V1
# (durable intelligence units): obligations and composition reports are
# projections over the existing envelope/edge structures. No second
# intelligence database.

OBLIGATION_KINDS = ("component", "interaction", "end_to_end", "condition")


@dataclass(frozen=True)
class ProofObligation:
    """One specific requirement a broader claim decomposes into, with
    explicit acceptance criteria. Decompose BEFORE combining evidence.
    Evidence satisfies an obligation only when its proven scope matches the
    obligation's scope — never by upgrading."""
    obligation_id: str
    region: ClaimRegion
    acceptance: str            # explicit acceptance criteria
    kind: str = "component"    # component | interaction | end_to_end | condition

    def __post_init__(self):
        assert self.kind in OBLIGATION_KINDS, self.kind


@dataclass(frozen=True)
class CompositionRule:
    """What the broader claim requires beyond its parts. Set
    requires_interaction / requires_end_to_end when the property is
    noncompositional — component coverage alone must then NOT qualify."""
    requires_all: bool = True
    requires_interaction: bool = False
    requires_end_to_end: bool = False


@dataclass(frozen=True)
class CompatibilityVerdict:
    """Result of the compatibility gate, checked BEFORE combining evidence.
    failures block combination (the parts stay valid-in-their-scopes);
    notes are caveats that do not block (e.g. shared origin counted once)."""
    compatible: bool
    failures: tuple = ()
    notes: tuple = ()


def check_compatibility(sets: tuple, origin_of: dict,
                      require_predicate: bool = True) -> CompatibilityVerdict:
    """Gate before combining evidence.

    Sets combined toward the SAME requirement must agree on the predicate
    (behavior+outcome — e.g. "retrieves correctly" != "refuses unauthorized
    retrieval"), the governing policy version, and the runtime version.
    Across different obligations, the predicate may legitimately differ
    (component vs interaction evidence), but policy and runtime must stay
    consistent — pass require_predicate=False for the cross-obligation check.

    Two reports from one test are one source: shared origin is flagged and
    counted once, never twice — a caveat, not a blocker.
    """
    failures, notes = [], []
    sets = tuple(sets)
    if sets:
        first = sets[0]
        for s in sets[1:]:
            if require_predicate and (
                    (s.scope.behavior, s.scope.outcome)
                    != (first.scope.behavior, first.scope.outcome)):
                failures.append(f"predicate_mismatch:{s.set_id}")
            if s.policy_version != first.policy_version:
                failures.append(f"policy_mismatch:{s.set_id}")
            if s.scope.runtime != first.scope.runtime:
                failures.append(f"runtime_mismatch:{s.set_id}")
    by_origin: dict = {}
    for s in sets:
        for ev in s.evidence_refs:
            by_origin.setdefault(origin_of.get(ev, ev), set()).add(s.set_id)
    for origin, sids in sorted(by_origin.items()):
        if len(sids) > 1:
            notes.append(f"shared_origin:{origin}="
                         f"{','.join(sorted(sids))}:counted_once")
    return CompatibilityVerdict(not failures, tuple(failures), tuple(notes))


@dataclass(frozen=True)
class CompositionReport:
    """Four-part qualification report — more informative than a single score.
    Tells Naya what's proven, what's missing, and which next test adds the
    most coverage. The three measures are reported separately, never merged:
    breadth (distinct obligations covered), depth (independent corroboration
    per obligation), integration (cross-part relationships verified)."""
    claim_id: str
    # Part 1: component-level coverage — obligation_id -> region verdict.
    component_coverage: dict
    # Part 2: cross-node interactions.
    interaction_status: dict
    # Part 3: end-to-end production qualification.
    end_to_end_status: dict
    # Part 4: overall claim verdict (one of revocation.VERDICTS).
    overall_verdict: str
    # The three separate things, kept separate.
    evidence_validity: dict      # obligation_id -> all supporting evidence cleared
    coverage_completeness: dict  # obligation_id -> covered?
    logical_sufficiency: bool   # composition_valid
    # The three measures, kept separate (no double-counting).
    breadth: int                 # distinct obligations with sufficient support
    depth: dict                  # obligation_id -> distinct-origin corroboration count
    integration: tuple           # satisfied interaction/end_to_end obligation ids
    compatibility: CompatibilityVerdict
    composition_valid: bool
    notes: tuple = ()

    def four_part_summary(self) -> str:
        lines = [f"claim {self.claim_id}: {self.overall_verdict}"]
        lines.append(f"  1. component coverage: {self.component_coverage}")
        lines.append(f"  2. interactions: {self.interaction_status}")
        lines.append(f"  3. end-to-end: {self.end_to_end_status}")
        lines.append(f"  4. overall: {self.overall_verdict} "
                     f"(breadth={self.breadth}, depth={self.depth}, "
                     f"integration={self.integration})")
        return "\n".join(lines)


def _obligation_shell(obligations: tuple) -> ClaimEnvelope:
    """Bridge obligations to the region machinery: each obligation becomes a
    region of one synthetic envelope so assess_region does the coverage and
    admissibility work. Composition adds compatibility + validity on top."""
    regions = tuple(o.region for o in obligations)
    return ClaimEnvelope(
        claim_id="__composition__",
        claim_scope=MeaningEnvelope(),
        quantifier="universal",
        regions=regions,
        support_sets=(),
        policy_version="",
    )


def compose_broader_claim(claim_id: str,
                          obligations: tuple,
                          support_sets: tuple,
                          independence_of: dict,
                          origin_of: dict,
                          rule: CompositionRule) -> CompositionReport:
    """Compose a broader claim from partial evidence.

    1. Map every support set to the obligations its scope covers (coverage).
    2. Run the compatibility gate over the sets that would be combined.
    3. Assess each obligation's region (admissibility via assess_region).
    4. Check composition validity (noncompositional properties need their
       interaction / end-to-end obligations satisfied).
    5. Issue the four-part report. Incompatible parts are retained as
       valid-in-their-scopes; the combination is simply not drawn.
    """
    shell = _obligation_shell(obligations)
    shell = ClaimEnvelope(
        claim_id=shell.claim_id, claim_scope=shell.claim_scope,
        quantifier=shell.quantifier, regions=shell.regions,
        support_sets=support_sets, policy_version=shell.policy_version)

    # Per-obligation assessment (coverage + admissibility).
    assessments = {}
    for o in obligations:
        assessments[o.obligation_id] = assess_region(
            o.region, shell, independence_of, origin_of)

    # Depth: distinct origins among sufficient sets (no double-counting).
    depth = {}
    for o in obligations:
        ra = assessments[o.obligation_id]
        origins = set()
        by_id = {s.set_id: s for s in support_sets}
        for sid in ra.sufficient_sets:
            s = by_id.get(sid)
            if s:
                origins.update(origin_of.get(e, e) for e in s.evidence_refs)
        depth[o.obligation_id] = len(origins)

    # Breadth: distinct obligations with sufficient independent support.
    breadth = sum(1 for o in obligations
                  if assessments[o.obligation_id].verdict == "SUPPORTED")

    # Compatibility: per obligation the covering sets must agree on
    # predicate+policy+runtime (they corroborate one requirement); across
    # obligations, policy+runtime must stay consistent while the predicate
    # may legitimately differ (component vs interaction evidence). The gate
    # runs before sufficiency — mismatched sets cannot be combined even if
    # neither alone satisfies the obligation.
    per_obligation = []
    for o in obligations:
        o_sets = tuple(s for s in support_sets
                       if o.region.region_id in s.covers)
        per_obligation.append(check_compatibility(o_sets, origin_of,
                                                  require_predicate=True))
    all_covering = tuple(s for s in support_sets
                         if any(o.region.region_id in s.covers
                                for o in obligations))
    cross = check_compatibility(all_covering, origin_of,
                                require_predicate=False)
    failures = tuple(f for v in per_obligation for f in v.failures) \
        + cross.failures
    notes_c = tuple(n for v in per_obligation for n in v.notes) + cross.notes
    compatibility = CompatibilityVerdict(not failures, failures, notes_c)

    # Composition validity: noncompositional properties need more than parts.
    interaction_obs = [o for o in obligations if o.kind == "interaction"]
    e2e_obs = [o for o in obligations if o.kind == "end_to_end"]
    integration = tuple(
        o.obligation_id for o in interaction_obs + e2e_obs
        if assessments[o.obligation_id].verdict == "SUPPORTED")
    composition_valid = True
    notes = []
    if rule.requires_interaction:
        missing = [o.obligation_id for o in interaction_obs
                   if assessments[o.obligation_id].verdict != "SUPPORTED"]
        if missing:
            composition_valid = False
            notes.append(
                "noncompositional: component tests cannot establish joint "
                f"behavior; interaction unproven for {','.join(missing)}")
    if rule.requires_end_to_end:
        missing = [o.obligation_id for o in e2e_obs
                   if assessments[o.obligation_id].verdict != "SUPPORTED"]
        if missing:
            composition_valid = False
            notes.append(
                "noncompositional: end-to-end behavior unproven for "
                f"{','.join(missing)}")

    # Overall verdict from the four conjuncts.
    required = obligations if rule.requires_all else ()
    failed = [o.obligation_id for o in required
              if assessments[o.obligation_id].verdict != "SUPPORTED"]
    conflicted = [o.obligation_id for o in required
                  if assessments[o.obligation_id].verdict == "CONFLICTED"]
    held = [o.obligation_id for o in required
            if assessments[o.obligation_id].detail == "held_pending_review"]

    if conflicted:
        overall = "SUSPENDED"
        notes.append("contradiction recorded for "
                     f"{','.join(conflicted)}: adjudication required; "
                     "the contradiction is not hidden")
    elif not compatibility.compatible:
        overall = "INSUFFICIENT_DATA"
        notes.append("incompatible evidence not combined; parts retained as "
                     "valid-in-their-scopes: "
                     f"{';'.join(compatibility.failures)}")
    elif not composition_valid:
        overall = "INSUFFICIENT_DATA"
    elif failed and held:
        overall = "SUSPENDED"
    elif failed:
        overall = "INSUFFICIENT_DATA"
        notes.append(f"uncovered obligations: {','.join(failed)}")
    else:
        overall = "UNAFFECTED"
        notes.append("coverage ∧ admissibility ∧ compatibility ∧ "
                     "composition validity all hold")

    def part(kind):
        return {o.obligation_id: assessments[o.obligation_id].verdict
                for o in obligations if o.kind == kind}

    return CompositionReport(
        claim_id=claim_id,
        component_coverage=part("component"),
        interaction_status=part("interaction"),
        end_to_end_status=part("end_to_end"),
        overall_verdict=overall,
        evidence_validity={
            o.obligation_id: all(
                independence_of.get(e, UNASSESSED) == CLEARED
                for sid in assessments[o.obligation_id].sufficient_sets
                for e in by_id[sid].evidence_refs) if assessments[
                    o.obligation_id].sufficient_sets else False
            for o in obligations},
        coverage_completeness={
            o.obligation_id: assessments[o.obligation_id].verdict == "SUPPORTED"
            for o in obligations},
        logical_sufficiency=composition_valid,
        breadth=breadth,
        depth=depth,
        integration=integration,
        compatibility=compatibility,
        composition_valid=composition_valid,
        notes=tuple(notes),
    )


# ---------------------------------------------------------------------------
# Composite Qualification Audit layer.
# ---------------------------------------------------------------------------
# Governing law: "Component success + component success ≠ system success
# unless the interactions, assumptions, and environment transitions have
# also been qualified."
#
# The audit lives in PROVE → CONNECT → VERIFY and answers five questions:
#   1. does each source genuinely establish its requirement?
#   2. do the requirements cover the claim?
#   3. are components compatible and interactions verified?
#   4. does the qualification survive environment/policy/config/time changes?
#   5. can an independent verifier reproduce it without trusting the
#      builder's interpretation?
# Narrower valid conclusions are preserved even when the overall claim fails.
#
# Logical form: (E1 ∧ E2 ∧ ... ∧ En ∧ A) ⇒ C. The audit must VERIFY the
# implication is justified — writing it down is not enough. If an assumption
# (e.g. "same authorization receipt checked at execution") lacks proof, the
# implication is NOT established.
#
# Three levels of proof (a missing layer is a missing proof obligation, not
# a score deduction): components / interactions / environment.
#
# Map onto the four-part CompositionReport: part 1 (components) answers
# questions 1–2; parts 2–3 (interactions, end-to-end) answer question 3;
# the environment difference map answers question 4; the independent proof
# boundary answers question 5.

# The five questions.
AUDIT_QUESTIONS = (
    "source_establishes_requirement",
    "requirements_cover_claim",
    "compatible_and_interactions_verified",
    "survives_environment_changes",
    "independently_reproducible",
)

# What independent VERIFY establishes (five proof obligations).
VERIFY_OBLIGATIONS = (
    "component_correctness",
    "interface_compatibility",   # outputs satisfy the next input contract
    "interaction_correctness",   # ordering, shared state, concurrency, failure
    "environment_applicability",
    "composite_sufficiency",     # verified obligations actually entail the claim
)

# Certificate verdicts: scope-bound proof levels, not permanent labels.
CERTIFICATE_VERDICTS = (
    "COMPONENT_QUALIFIED",
    "INTEGRATION_QUALIFIED",
    "TRANSFER_QUALIFIED",
    "PRODUCTION_PROVEN",
)

ENV_DIFF_CLASSES = ("immaterial", "covered", "requires_bridge", "incompatible")


@dataclass(frozen=True)
class InteractionContract:
    """Per-handoff contract for assume-guarantee reasoning. The sender's
    PROVEN guarantees must satisfy the receiver's assumptions; the shared
    invariant must hold across the handoff. Structural checks cover shared
    resources, cycles, temporal ordering, and concurrency."""
    handoff_id: str
    sender: str
    receiver: str
    sender_guarantee: str
    receiver_assumption: str
    shared_invariant: str
    evidence_ref: str = ""
    shared_resources: tuple = ()
    ordering: str = ""            # required temporal ordering, if any
    concurrency_safe: bool = True

    def assume_guarantee_holds(self, proven_guarantees: dict) -> tuple:
        """(holds, gap). The receiver's assumption must be among the
        sender's PROVEN guarantees — promised is not proven."""
        proven = proven_guarantees.get(self.sender, ())
        if self.receiver_assumption in proven:
            return True, ""
        return False, (f"{self.receiver} assumes '{self.receiver_assumption}' "
                       f"but {self.sender} has only proven {proven}")


@dataclass(frozen=True)
class Assumption:
    """One assumption in the composition argument. An unjustified
    assumption (empty justification) means the implication (E∧A)⇒C is NOT
    established — no matter how strong the evidence is."""
    assumption_id: str
    statement: str
    justification: str = ""

    def is_justified(self) -> bool:
        return bool(self.justification)


@dataclass(frozen=True)
class CompositionArgument:
    """The logical form (E1 ∧ ... ∧ En ∧ A) ⇒ C, made explicit so the audit
    can verify it instead of merely writing it."""
    argument_id: str
    evidence_ids: tuple
    assumptions: tuple           # Assumption
    conclusion: str

    def implication_established(self) -> tuple:
        unjustified = [a.assumption_id for a in self.assumptions
                       if not a.is_justified()]
        if unjustified:
            return False, (f"implication not established: unjustified "
                           f"assumptions {','.join(unjustified)}")
        return True, "all assumptions justified; implication verified"


@dataclass(frozen=True)
class EnvironmentDifference:
    """One versioned staging→production difference. Same code SHA is
    necessary but NOT sufficient for behavioral parity — every material
    difference must be justified."""
    difference_id: str
    description: str
    classification: str          # immaterial|covered|requires_bridge|incompatible
    justification: str = ""

    def __post_init__(self):
        assert self.classification in ENV_DIFF_CLASSES, self.classification


def audit_environment_transfer(differences: tuple) -> tuple:
    """Production qualification proceeds only when every material difference
    is justified. Returns (verdict, notes)."""
    notes = []
    for d in differences:
        if d.classification == "immaterial":
            continue
        if d.classification == "covered":
            if not d.justification:
                return "BLOCKED", (f"{d.difference_id}: marked covered "
                                   f"without justification",)
            continue
        if d.classification == "requires_bridge":
            return "BLOCKED", (f"{d.difference_id}: requires bridge evidence "
                               f"before production qualification",)
        if d.classification == "incompatible":
            return "BLOCKED", (f"{d.difference_id}: incompatible with "
                               f"production — {d.description}",)
    transferable = [d.difference_id for d in differences
                    if d.classification in ("immaterial", "covered")]
    return "TRANSFERABLE", tuple(
        [f"all material differences justified: {','.join(transferable)}"]
        if transferable else ["no material differences"])


@dataclass(frozen=True)
class QualificationCertificate:
    """Scope-bound certificate. Not a permanent platform label: an
    environment change reopens and recomputes it."""
    claim_id: str
    verdict: str                 # one of CERTIFICATE_VERDICTS
    scope: MeaningEnvelope
    evidence_refs: tuple
    assumptions: tuple           # assumption_ids relied upon
    environment: str
    issued_under_policy: str = ""

    def __post_init__(self):
        assert self.verdict in CERTIFICATE_VERDICTS, self.verdict

    def reopen_on_environment_change(self, new_environment: str) -> dict:
        """Environment change reopens the certificate — it does not carry
        over. Returns what must be re-established."""
        return {
            "previous_verdict": self.verdict,
            "previous_environment": self.environment,
            "new_environment": new_environment,
            "status": "REOPENED",
            "requires": ("re-run environment difference map; "
                         "re-verify assumptions under the new environment; "
                         "recompute the certificate — never inherit it"),
        }


@dataclass(frozen=True)
class IndependentReconstruction:
    """The independent proof boundary: what the auditor redoe without
    trusting the builder's interpretation. Open regression results are
    distinguished from blind qualification evidence — the 218 exposed
    files are regression, not fresh blind proof."""
    claim_id: str
    source_reread: bool = False
    outcome_reproduced: bool = False
    derivation_checked: bool = False
    negatives_inspected: bool = False
    target_runtime_verified: bool = False
    blind_evidence: bool = False   # genuinely blind, not exposed fixtures

    def complete(self) -> bool:
        return all([self.source_reread, self.outcome_reproduced,
                    self.derivation_checked, self.negatives_inspected,
                    self.target_runtime_verified])

    def qualifies_as_blind(self) -> bool:
        return self.complete() and self.blind_evidence


@dataclass(frozen=True)
class AuditResult:
    claim_id: str
    answers: dict                # audit question -> (True/False, note)
    certificate: object          # QualificationCertificate | None
    narrower_conclusions: tuple  # preserved valid narrower claims
    notes: tuple = ()


def composition_proof_audit(claim_id: str,
                            report: CompositionReport,
                            interaction_contracts: tuple,
                            proven_guarantees: dict,
                            env_differences: tuple,
                            argument: CompositionArgument,
                            reconstruction: IndependentReconstruction,
                            evidence_refs: tuple = ()
                            ) -> AuditResult:
    """Run the five-question audit over a composition report.

    Preserves narrower valid conclusions even when the overall claim fails:
    every SUPPORTED obligation survives as its own bounded conclusion.
    """
    answers, notes = {}, []

    # Q1: does each source genuinely establish its requirement? Per
    # obligation: sources establish exactly the SUPPORTED obligations — no
    # more, no less.
    established = {oid for oid, v in report.component_coverage.items()
                   if v == "SUPPORTED"}
    answers["source_establishes_requirement"] = (
        True,
        f"sources genuinely establish: {','.join(sorted(established)) or 'none'}")

    # Q2: do the requirements cover the claim?
    q2_ok = report.overall_verdict in ("UNAFFECTED", "REQUALIFIED")
    answers["requirements_cover_claim"] = (
        q2_ok,
        "all required obligations covered" if q2_ok else
        f"uncovered: {report.overall_verdict}")

    # Q3: compatible and interactions verified?
    contracts_ok, gaps = [], []
    for c in interaction_contracts:
        holds, gap = c.assume_guarantee_holds(proven_guarantees)
        contracts_ok.append(holds)
        if gap:
            gaps.append(gap)
    q3_ok = (report.compatibility.compatible and all(contracts_ok)
             and report.composition_valid)
    answers["compatible_and_interactions_verified"] = (
        q3_ok,
        "contracts hold" if q3_ok else
        f"gaps: {'; '.join(gaps + list(report.compatibility.failures)) or 'composition invalid'}")

    # Q4: survives environment/policy/config/time changes?
    transfer_verdict, transfer_notes = audit_environment_transfer(
        env_differences)
    q4_ok = transfer_verdict == "TRANSFERABLE"
    answers["survives_environment_changes"] = (q4_ok, "; ".join(transfer_notes))

    # Q5: independently reproducible?
    impl_ok, impl_note = argument.implication_established()
    q5_ok = reconstruction.complete() and impl_ok
    answers["independently_reproducible"] = (
        q5_ok,
        "auditor can reconstruct without trusting the builder"
        if q5_ok else
        f"reconstruction incomplete or {impl_note}")

    # Certificate: the highest proof level actually established.
    all_yes = all(v[0] for v in answers.values())
    if all_yes and q4_ok:
        cert_verdict = "PRODUCTION_PROVEN"
    elif all_yes:
        cert_verdict = "TRANSFER_QUALIFIED"
    elif answers["compatible_and_interactions_verified"][0]:
        cert_verdict = "INTEGRATION_QUALIFIED"
    elif established:
        cert_verdict = "COMPONENT_QUALIFIED"
    else:
        cert_verdict = None
    certificate = None
    if cert_verdict:
        certificate = QualificationCertificate(
            claim_id=claim_id, verdict=cert_verdict,
            scope=MeaningEnvelope(),
            evidence_refs=tuple(evidence_refs),
            assumptions=tuple(a.assumption_id for a in argument.assumptions),
            environment="production" if cert_verdict == "PRODUCTION_PROVEN"
            else "staging")

    # Narrower conclusions survive regardless.
    narrower = tuple(
        f"{oid}: {verdict}"
        for oid, verdict in report.component_coverage.items()
        if verdict == "SUPPORTED")

    return AuditResult(claim_id=claim_id, answers=answers,
                       certificate=certificate,
                       narrower_conclusions=narrower,
                       notes=tuple(notes))


# ---------------------------------------------------------------------------
# Versioning and retiring composite proof obligations (temporal layer).
# ---------------------------------------------------------------------------
# Governing law: "Requirements may evolve. Historical proof must remain
# intact. Current qualification must always be evaluated against the
# requirements governing its intended use."
#
# Three distinct objects, three different operations:
#   proof obligation        — immutable within a version
#   qualification receipt   — append-only
#   applicability assessment — recomputed when conditions change
# Retiring a requirement ≠ retiring a test ≠ revoking a qualification.
#
# Maps onto Graph Contract V1's SUPERSEDE relationship and temporal
# validity: revisions link by supersession edges, never by overwriting.
# Extension, not a second registry.

OBLIGATION_LIFECYCLE = ("PROPOSED", "ACTIVE", "DEPRECATED",
                        "SUPERSEDED", "RETIRED", "WITHDRAWN")

CHANGE_CLASSES = ("editorial", "stronger", "weaker", "interface_changed",
                  "renamed", "environment_changed", "split", "merged",
                  "removed", "found_invalid")


@dataclass(frozen=True)
class ObligationRevision:
    """One immutable revision of a proof obligation. Semantic change = new
    revision. Split/merge = new identities linked by supersession."""
    obligation_id: str       # stable identity across revisions
    revision_id: str         # immutable, unique per revision
    requirement_text: str
    scope: MeaningEnvelope
    acceptance_predicate: str  # machine-checkable predicate
    proof_standard: str
    assumptions: tuple = ()
    dependencies: tuple = ()   # other obligation_ids
    effective_from: str = ""   # effective time: requirement applies from here
    effective_until: str = ""  # empty = still effective
    supersedes: str = ""       # previous revision_id (SUPERSEDE edge)
    retirement_reason: str = ""
    lifecycle: str = "ACTIVE"

    def __post_init__(self):
        assert self.lifecycle in OBLIGATION_LIFECYCLE, self.lifecycle


@dataclass(frozen=True)
class QualificationReceipt:
    """Append-only proof record. Bitemporal: effective_at (when the
    requirement applied) vs recorded_at (when NayaNET learned it).
    Retiring the obligation never invalidates the receipt — it stays valid
    history of what was established under the then-governing requirement."""
    receipt_id: str
    obligation_id: str
    revision_id: str
    evidence_refs: tuple
    verdict: str
    recorded_at: str
    effective_at: str
    policy_version: str


@dataclass(frozen=True)
class ObligationChange:
    """A classified change to an obligation. Classify BEFORE migrating."""
    change_id: str
    obligation_id: str
    from_revision: str
    to_revision: str           # "" for removed / found_invalid
    change_class: str          # one of CHANGE_CLASSES
    migration_note: str = ""

    def __post_init__(self):
        assert self.change_class in CHANGE_CLASSES, self.change_class


def classify_migration(change: ObligationChange) -> tuple:
    """What happens to existing receipts under this change class.

    Returns (receipt_standing, required_action):
      receipt_standing: "carries_forward" | "preserved_history" |
                        "needs_requalification" | "withdrawn"
    Proof reuse ≠ proof migration: evidence may be reused, but the verdict
    migrates only when the new assessment establishes the evidence
    satisfies the CURRENT obligation. A model's assertion of equivalence
    is insufficient.
    """
    cc = change.change_class
    if cc in ("editorial",):
        return ("carries_forward",
                "record equivalence; retain qualification")
    if cc == "renamed":
        return ("carries_forward",
                "carry forward only with documented compatibility")
    if cc == "weaker":
        return ("preserved_history",
                "preserve history; review authorization for the weaker bar")
    if cc in ("stronger", "interface_changed", "environment_changed",
              "split", "merged"):
        actions = {
            "stronger": "require additional proof for the stronger criterion",
            "interface_changed": "requalify sender + receiver + interaction",
            "environment_changed": "bridge evidence required",
            "split": "map old proof to the exact new obligations",
            "merged": "verify the conjunction under the merged obligation",
        }
        return ("needs_requalification", actions[cc])
    if cc == "removed":
        return ("preserved_history",
                "retire the requirement; preserve receipts as history")
    if cc == "found_invalid":
        return ("withdrawn",
                "withdraw authority; reassess all dependents")
    raise AssertionError(cc)  # unreachable: __post_init__ guards


def governing_revision(revisions: tuple, obligation_id: str,
                       at_time: str) -> ObligationRevision | None:
    """Which revision governed at effective time at_time. Bitemporal audit
    query: 'what requirement governed this action at the time?'"""
    candidates = [r for r in revisions
                  if r.obligation_id == obligation_id
                  and r.effective_from <= at_time
                  and (not r.effective_until or at_time < r.effective_until)]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r.effective_from)


def assess_applicability(receipt: QualificationReceipt,
                         revisions: tuple, at_time: str) -> tuple:
    """Current applicability assessment, recomputed when conditions change.
    Returns (applies, reason). A receipt for a superseded revision does not
    automatically apply to the current one."""
    current = governing_revision(revisions, receipt.obligation_id, at_time)
    if current is None:
        return False, "no governing revision at that time"
    if receipt.revision_id == current.revision_id:
        return True, "receipt matches the governing revision"
    return False, (f"receipt is for {receipt.revision_id}; "
                   f"{current.revision_id} governs — requalification required")


@dataclass(frozen=True)
class MigrationReceipt:
    """Machine-readable migration record. Binds source hashes, the
    requirements manifest, lineage, policy version, reviewer, and affected
    IDs. Activation authority required to execute."""
    migration_id: str
    change: ObligationChange
    source_hashes: tuple
    requirements_manifest: str
    lineage: tuple              # supersession chain
    policy_version: str
    reviewer: str
    affected_ids: tuple         # qualifications, claims, actions, packages
    authorized_by: str = ""


def affected_closure(change: ObligationChange,
                     dependents: dict) -> dict:
    """Trace the change's blast radius: qualifications, composite claims,
    interfaces, bridges, promotions, actions, successor packages.
    dependents maps obligation_id -> {category: [ids]}.
    Reports the EXACT missing obligation, not a vague 'requalify all'."""
    cats = dependents.get(change.obligation_id, {})
    standing, action = classify_migration(change)
    return {
        "change_id": change.change_id,
        "obligation_id": change.obligation_id,
        "change_class": change.change_class,
        "receipt_standing": standing,
        "required_action": action,
        "affected": dict(cats),
        "exact_gap": (f"{change.obligation_id}: {action}"
                      if standing in ("needs_requalification", "withdrawn")
                      else f"{change.obligation_id}: no re-proof required"),
    }


def check_decision_boundary(action_id: str, obligation_id: str,
                            revisions: tuple, receipts: tuple,
                            at_time: str, environment: str,
                            bridge_verified: bool,
                            authorization_permits: bool) -> tuple:
    """At consequential action, LAW/ACT establish (fail-closed):
    1. which revisions govern (environment + effective time),
    2. whether the submitted qualification was evaluated against them,
    3. whether proof was superseded/withdrawn,
    4. whether bridge evidence is verified (if environment changed),
    5. whether current authorization permits.
    Uses a freshness-validated snapshot — no race between retirement and
    execution."""
    reasons = []
    current = governing_revision(revisions, obligation_id, at_time)
    if current is None:
        return False, ("no governing revision for "
                       f"{obligation_id} at {at_time}",)
    reasons.append(f"governing revision: {current.revision_id} "
                   f"(lifecycle {current.lifecycle})")
    if current.lifecycle in ("RETIRED", "WITHDRAWN"):
        return False, tuple(reasons + [
            f"proof {current.lifecycle.lower()}: action blocked"])
    applicable = [r for r in receipts
                  if r.obligation_id == obligation_id
                  and assess_applicability(r, revisions, at_time)[0]]
    if not applicable:
        return False, tuple(reasons + [
            "no qualification receipt applies to the governing revision"])
    reasons.append(f"applicable receipt: {applicable[0].receipt_id}")
    if current.scope.environment != "any" \
            and current.scope.environment != environment:
        if not bridge_verified:
            return False, tuple(reasons + [
                "environment changed without verified bridge evidence"])
        reasons.append("bridge evidence verified")
    if not authorization_permits:
        return False, tuple(reasons + ["current authorization does not permit"])
    return True, tuple(reasons + ["all boundary checks hold"])
