"""Split/merge proof migration (spec).

Principle: "Splitting a requirement must not multiply proof. Merging
requirements must not manufacture integration."

Governing principle: "Preserve historical proof. Reuse its valid evidence.
Require new proof for any meaning, dependency, interaction or environment
assumption that the old evidence did not establish."

Extends the L4 versioning layer (propagation.py: immutable ObligationRevision,
QualificationReceipt, ObligationChange, classify_migration, bitemporal
governing_revision, affected_closure, check_decision_boundary) with detailed
split/merge migration mechanics.

Migrate evidence, not inherited PASS labels. Two migrations, two risks:
  SPLIT (O -> A^B^C): assuming an old composite PASS proves every child.
      Each child's entailment and scope must be established separately.
      A black-box end-to-end success may NOT establish internal invariants.
  MERGE (A^B^C -> M): assuming passing parts prove an integrated whole.
      Composition, compatibility, and cross-part interactions must be
      established. If M adds timing/causality/interaction/reliability/
      environment, those are NEW obligations with their own proof.

Composes with:
  revocation.py   — six qualification verdicts. Migration verdicts map onto
                    them per obligation, never as one blanket PASS/FAIL.
  uncertainty.py  — migration cannot launder compromised receipts: evidence
                    with tainted independence stays ineligible for independent
                    certification no matter how the obligations restructure.
  authority.py    — UNDETERMINED evidence may be examined, never counted as
                    independent proof, in any migration role.
  propagation.py  — ObligationRevision, QualificationReceipt, ObligationChange,
                    classify_migration (split/merge already classified as
                    needs_requalification), compatibility gate
                    (check_compatibility), region verdicts, SupportSet.

Hard rules:
  - No invented entailment: ENTAILS requires an independently established
    justification. It can never be inferred from the fact that the
    requirements were split or merged.
  - No weakening via migration: consequential weakening needs governing
    authority approval; the mechanism cannot lower proof standards itself.
  - No laundering: restructuring obligations never upgrades evidence
    independence. COMPROMISED receipts stay ineligible for independent
    certification.
  - Shared ancestry: one old test supporting two children is one original
    observation, not two independent tests.

This module is SPEC + deterministic machinery. NOT wired into kernel/,
KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .propagation import (
    MeaningEnvelope,
    ObligationRevision,
    QualificationReceipt,
    ObligationChange,
    ProofObligation,
    ClaimRegion,
    SupportSet,
    check_compatibility,
    REGION_VERDICTS,
)
from .revocation import VERDICTS

# ---------------------------------------------------------------------------
# Proof mapping relations.
# ---------------------------------------------------------------------------
# ENTAILS is a scoped, independently justified conclusion — never an
# LLM-generated equivalence label. The justification must name the
# independent basis (verifier receipt, logical decomposition proof, ...).
MAPPING_RELATIONS = (
    "ENTAILS",            # old evidence fully establishes the target part
    "PARTIALLY_SUPPORTS", # old evidence establishes an identifiable part only
    "DOES_NOT_SUPPORT",   # old evidence does not establish the target part
    "UNDETERMINED",       # cannot be established either way from old evidence
)

MIGRATION_OPERATIONS = ("SPLIT", "MERGE")

# Obligation-specific migration verdicts — never one PASS/FAIL for the
# whole operation. Each target obligation gets its own verdict.
MIGRATION_VERDICTS = (
    "CARRIED_FORWARD",     # earlier evidence fully qualifies the new
                           # obligation within a verified matching scope
    "PARTIALLY_MIGRATED",  # some requirements established; others need proof
    "BRIDGE_REQUIRED",     # evidence valid but compatibility/integration
                           # remains unproven
    "REQUALIFIED",         # additional independent evidence now establishes
                           # the new obligation
    "INSUFFICIENT_EVIDENCE",
    "INCOMPATIBLE",        # a material requirement or assumption conflicts
                           # with the old evidence
)

# Backward-fidelity classification for every requirement touched by a
# migration. Every source requirement must be classified — silent drops
# are a fidelity failure.
FIDELITY_CLASSES = (
    "preserved",     # no semantic change
    "strengthened",  # strictly stronger acceptance
    "weakened",      # strictly weaker acceptance — consequential weakening
                     # needs governing authority approval
    "added",         # new requirement with no source counterpart
    "removed",       # source requirement with no target counterpart —
                     # consequential if it was load-bearing
    "re-scoped",     # same requirement, different scope
    "replaced",      # different requirement covering the same intent
)

# Independence states an evidence contribution can carry. Migration never
# upgrades these: restructuring obligations cannot turn compromised or
# undetermined evidence into independent proof.
INDEPENDENCE_STATES = ("QUALIFIED", "UNDETERMINED", "COMPROMISED")


@dataclass(frozen=True)
class EvidenceProposition:
    """One proposition actually established by a historical receipt's
    evidence, with its demonstrated scope and independence state.

    Split/merge migration evaluates the directed implication from THESE
    propositions to each new obligation — never from the old obligation's
    PASS flag. A black-box end-to-end success is one proposition with an
    end-to-end scope; it cannot cover a child that demands an internal
    invariant, because the scope dimensions do not match."""
    evidence_ref: str
    proposition: str
    scope: MeaningEnvelope
    independence: str = "QUALIFIED"  # one of INDEPENDENCE_STATES

    def __post_init__(self):
        assert self.independence in INDEPENDENCE_STATES, self.independence


@dataclass(frozen=True)
class ProofMapping:
    """Maps old evidence to one part of a new obligation.

    relation is one of MAPPING_RELATIONS. ENTAILS requires a non-empty
    justification naming its independent basis — the implication must be
    independently established, never inferred from the restructure itself.
    """
    source_obligation: str   # obligation_id@revision_id
    target_obligation: str   # obligation_id@revision_id
    target_part: str         # which part of the target this mapping addresses
    relation: str            # one of MAPPING_RELATIONS
    evidence_refs: tuple
    justification: str = ""  # independent basis for the implication
    scope_note: str = ""

    def __post_init__(self):
        assert self.relation in MAPPING_RELATIONS, self.relation
        if self.relation in ("ENTAILS", "PARTIALLY_SUPPORTS"):
            assert self.justification, (
                f"{self.relation} requires an independently established "
                "justification — never infer it from the restructure")


@dataclass(frozen=True)
class RequirementChange:
    """One requirement's backward-fidelity classification. The classification
    itself is the independent verifier's judgment; the machinery enforces
    that every requirement is classified and that consequential weakening
    cannot pass without governing authority approval."""
    requirement: str
    from_text: str
    to_text: str
    fidelity: str            # one of FIDELITY_CLASSES
    consequential: bool = False

    def __post_init__(self):
        assert self.fidelity in FIDELITY_CLASSES, self.fidelity


# ---------------------------------------------------------------------------
# Laundering guard: migration never upgrades evidence independence.
# ---------------------------------------------------------------------------
def migration_eligibility(evidence_ref: str, independence_of: dict,
                          role: str) -> tuple:
    """Can this evidence play `role` in a migration? Roles:
      "independent_proof" — counts toward establishing the new obligation.
      "examination"       — may be inspected/investigated, never counted.
      "historical"        — preserved as history only.

    Returns (eligible, reason). COMPROMISED evidence is never eligible as
    proof in any migration — restructuring obligations cannot make a
    compromised historical receipt eligible for independent certification.
    UNDETERMINED evidence may be examined but never counted as independent
    proof (authority.py: no silent promotion).
    """
    state = independence_of.get(evidence_ref, "UNDETERMINED")
    if state == "COMPROMISED":
        if role == "historical":
            return True, "preserved as history; ineligible as proof"
        return False, ("COMPROMISED evidence cannot certify anything — "
                       "migration does not launder independence")
    if state == "UNDETERMINED":
        if role == "independent_proof":
            return False, ("UNDETERMINED evidence may be examined, never "
                           "counted as independent proof")
        return True, "examination permitted with uncertainty preserved"
    return True, "QUALIFIED evidence eligible"


def _independence_sufficient_for(state: str, proof_standard: str) -> bool:
    """A proposition's independence satisfies the child's proof standard.

    Convention (documented, reviewable): a proof_standard containing the
    token "independent" requires QUALIFIED independence. Otherwise
    UNDETERMINED evidence may be examined but caps the mapping at
    PARTIALLY_SUPPORTS — it can never carry an ENTAILS. COMPROMISED is
    never sufficient for any proof standard.
    """
    if state == "COMPROMISED":
        return False
    if "independent" in proof_standard.lower():
        return state == "QUALIFIED"
    return state in ("QUALIFIED", "UNDETERMINED")


# ---------------------------------------------------------------------------
# SPLIT: one obligation becomes several.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SplitPlan:
    """The assessed migration for a split. Per-child mappings and verdicts;
    the overall verdict is the most restrictive child verdict, but every
    child's individual verdict is preserved — never collapsed to one
    PASS/FAIL."""
    old: ObligationRevision
    children: tuple            # ObligationRevision
    mappings: tuple            # ProofMapping, one per child
    shared_ancestry: dict       # evidence_ref -> [child ids it supports]
                               # (one observation, not N independent tests)
    child_verdicts: dict        # child obligation_id -> MIGRATION_VERDICTS
    overall_verdict: str


# The predicate dimensions: what the evidence actually demonstrated.
# A proposition is relevant to a child only when it covers these — sharing
# merely an environment or component is context, not partial support.
PREDICATE_DIMENSIONS = ("behavior", "outcome")


def _proposition_relevant(prop_scope: MeaningEnvelope,
                          child_scope: MeaningEnvelope) -> bool:
    """Relevance gate: the proposition's demonstrated predicate must cover
    the child's required predicate on every predicate dimension."""
    for d in PREDICATE_DIMENSIONS:
        s_val, c_val = getattr(prop_scope, d), getattr(child_scope, d)
        if c_val == "any" or s_val == "any":
            continue
        if not set(c_val.split("+")) <= set(s_val.split("+")):
            return False
    return True


def _dimension_union_coverage(prop_scopes: tuple, child_scope: MeaningEnvelope
                            ) -> tuple:
    """Union coverage: for each required dimension of the child, the union
    of the contributing propositions' dimension-value sets must cover the
    child's required set. A proposition with "any" on a dimension is
    genuinely general there and covers it alone. Returns
    (covered_dimensions, missing_dimensions).

    This is what makes PARTIALLY_SUPPORTS reachable and honest: old
    evidence may cover an identifiable part of the child (some dimensions)
    without covering the whole child. A black-box end-to-end proposition
    contributes nothing to a dimension demanding a specific internal
    behavior, because its value set does not contain the required value.
    """
    covered, missing = [], []
    for d in MeaningEnvelope.DIMENSIONS:
        c_val = getattr(child_scope, d)
        if c_val == "any":
            covered.append(d)
            continue
        c_set = set(c_val.split("+"))
        union: set = set()
        general = False
        for ps in prop_scopes:
            s_val = getattr(ps, d)
            if s_val == "any":
                general = True
                break
            union |= set(s_val.split("+"))
        if general or c_set <= union:
            covered.append(d)
        else:
            missing.append(d)
    return tuple(covered), tuple(missing)


def assess_split_child(old: ObligationRevision,
                       child: ObligationRevision,
                       propositions: tuple,
                       independence_of: dict,
                       entailment_justification: str = "") -> ProofMapping:
    """Assess one split child against the old evidence's actual propositions.

    Coverage rule: a proposition covers the child only when its demonstrated
    scope covers the child's required scope (MeaningEnvelope.covers, every
    dimension) AND its independence satisfies the child's proof standard.

    relation:
      ENTAILS            — full coverage + independently established
                           O=>child implication (justification required).
      PARTIALLY_SUPPORTS — partial coverage of the child's scope, or
                           independence caps at examination level; the
                           covered part is justified.
      DOES_NOT_SUPPORT   — no covering proposition (e.g. black-box
                           end-to-end evidence vs an internal invariant).
      UNDETERMINED       — coverage ambiguous or implication unjustified.

    The old PASS flag is never an input. Only propositions are.
    """
    src = f"{old.obligation_id}@{old.revision_id}"
    tgt = f"{child.obligation_id}@{child.revision_id}"
    contributing = []
    capped = False
    for p in propositions:
        if not _independence_sufficient_for(p.independence,
                                            child.proof_standard):
            capped = True
            continue
        if not _proposition_relevant(p.scope, child.scope):
            # Shares context (environment/component) but demonstrates a
            # different predicate — not partial support for this child.
            continue
        contributing.append(p)
    if not contributing:
        if capped:
            return ProofMapping(src, tgt, child.obligation_id,
                                "UNDETERMINED", (),
                                scope_note="propositions exist but "
                                "independence is insufficient for the "
                                "child's proof standard")
        return ProofMapping(src, tgt, child.obligation_id,
                            "DOES_NOT_SUPPORT", (),
                            scope_note="no old proposition addresses the "
                            "child's scope — black-box success does not "
                            "establish internal invariants")
    covered, missing = _dimension_union_coverage(
        tuple(p.scope for p in contributing), child.scope)
    ev_refs = tuple(p.evidence_ref for p in contributing)
    if missing and not covered:
        return ProofMapping(src, tgt, child.obligation_id,
                            "DOES_NOT_SUPPORT", (),
                            scope_note="no required dimension covered "
                            f"(missing: {','.join(missing)})")
    if not entailment_justification:
        return ProofMapping(src, tgt, child.obligation_id,
                            "UNDETERMINED", ev_refs,
                            scope_note="scope coverage exists but the "
                            "O=>child implication was never independently "
                            "established — cannot infer it from the split")
    if not missing:
        return ProofMapping(src, tgt, child.obligation_id, "ENTAILS",
                            ev_refs, justification=entailment_justification,
                            scope_note="every required dimension covered by "
                            "old propositions within matching conditions")
    return ProofMapping(src, tgt, child.obligation_id, "PARTIALLY_SUPPORTS",
                        ev_refs, justification=entailment_justification,
                        scope_note=f"covered: {','.join(covered)}; missing: "
                        f"{','.join(missing)}")


def _migration_verdict_for_mapping(mapping: ProofMapping,
                                   environment_changed: bool = False,
                                   bridge_verified: bool = False,
                                   new_evidence_establishes: bool = False,
                                   conflicts: bool = False) -> str:
    """Per-obligation migration verdict from one assessed mapping."""
    if conflicts:
        return "INCOMPATIBLE"
    if new_evidence_establishes:
        return "REQUALIFIED"
    if environment_changed and not bridge_verified:
        return "BRIDGE_REQUIRED"
    return {
        "ENTAILS": "CARRIED_FORWARD",
        "PARTIALLY_SUPPORTS": "PARTIALLY_MIGRATED",
        "DOES_NOT_SUPPORT": "INSUFFICIENT_EVIDENCE",
        "UNDETERMINED": "INSUFFICIENT_EVIDENCE",
    }[mapping.relation]


_VERDICT_SEVERITY = {
    "CARRIED_FORWARD": 0,
    "REQUALIFIED": 0,
    "PARTIALLY_MIGRATED": 1,
    "BRIDGE_REQUIRED": 2,
    "INSUFFICIENT_EVIDENCE": 3,
    "INCOMPATIBLE": 4,
}


def plan_split(old: ObligationRevision, children: tuple,
               propositions: tuple, independence_of: dict,
               entailments: dict | None = None,
               environment_changed: bool = False,
               bridge_verified: bool = False,
               new_evidence: dict | None = None) -> SplitPlan:
    """Build the assessed split plan. `entailments` maps child
    obligation_id -> independently established justification for O=>child.
    `new_evidence` maps child obligation_id -> True when additional
    independent evidence supplied during migration establishes the child.

    The old obligation's historical qualification is untouched — this plan
    only assesses what migrates forward.
    """
    entailments = entailments or {}
    new_evidence = new_evidence or {}
    mappings = []
    verdicts = {}
    ancestry: dict = {}
    for child in children:
        m = assess_split_child(old, child, propositions, independence_of,
                               entailments.get(child.obligation_id, ""))
        mappings.append(m)
        for ev in m.evidence_refs:
            ancestry.setdefault(ev, []).append(child.obligation_id)
        verdicts[child.obligation_id] = _migration_verdict_for_mapping(
            m, environment_changed, bridge_verified,
            new_evidence.get(child.obligation_id, False))
    overall = max(verdicts.values(), key=lambda v: _VERDICT_SEVERITY[v])
    return SplitPlan(old=old, children=tuple(children),
                     mappings=tuple(mappings),
                     shared_ancestry={k: sorted(v)
                                      for k, v in sorted(ancestry.items())},
                     child_verdicts=verdicts, overall_verdict=overall)


# ---------------------------------------------------------------------------
# MERGE: several obligations become one.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MergePlan:
    """The assessed migration for a merge. Each source is mapped to its
    assigned part; genuinely new obligations introduced by the merge
    (interactions, timing, causality, ordering, authority preservation,
    shared runtime, outcome verification) are listed as new_obligations and
    must have their own proof — three green component receipts never prove
    an untested interaction."""
    sources: tuple              # ObligationRevision
    merged: ObligationRevision
    mappings: tuple             # ProofMapping, one per source part
    new_obligations: tuple      # ProofObligation introduced by the merge
    unproved_obligations: tuple # obligation_ids lacking sufficient evidence
    connective: str             # "AND" | "OR" — preserved from the merged
                               # requirement's logic; AND needs every part,
                               # OR may qualify on either alternative
    compatibility_notes: tuple
    correlated_sources: tuple   # source ids sharing origin — their success
                               # rates must NOT be multiplied or averaged
    part_verdicts: dict         # source obligation_id -> MIGRATION_VERDICTS
    overall_verdict: str

    def __post_init__(self):
        assert self.connective in ("AND", "OR"), self.connective


def plan_merge(sources: tuple, merged: ObligationRevision,
               part_of: dict, propositions: tuple,
               independence_of: dict, origin_of: dict,
               new_obligations: tuple = (),
               connective: str = "AND",
               entailments: dict | None = None,
               new_evidence: dict | None = None,
               policy_versions: dict | None = None,
               part_scopes: dict | None = None) -> MergePlan:
    """Build the assessed merge plan.

    part_of: source obligation_id -> target part name in the merged claim.
    part_scopes: source obligation_id -> MeaningEnvelope for that part
        (defaults to the merged scope when absent). Each source's evidence
        is assessed against its assigned part's scope (same union-coverage
        rule as split) — never against the whole merged scope, which no
        single component could cover. new_obligations are checked against
        the propositions; uncovered ones become unproved_obligations and
        block the merged qualification.

    Compatibility is checked across sources with require_predicate=False
    (different obligations legitimately test different predicates) but
    policy and runtime must stay consistent. Sources sharing an origin
    are flagged correlated — their rates are never combined arithmetically.
    """
    entailments = entailments or {}
    new_evidence = new_evidence or {}
    policy_versions = policy_versions or {}
    part_scopes = part_scopes or {}
    mappings = []
    verdicts = {}
    for src in sources:
        part = part_of.get(src.obligation_id, src.obligation_id)
        # The source's assigned part is assessed as a pseudo-child whose
        # scope is the merged obligation's scope restricted to that part.
        pseudo_child = ObligationRevision(
            obligation_id=src.obligation_id, revision_id=merged.revision_id,
            requirement_text=f"{merged.requirement_text} [part: {part}]",
            scope=part_scopes.get(src.obligation_id, merged.scope),
            acceptance_predicate=merged.acceptance_predicate,
            proof_standard=merged.proof_standard,
            assumptions=merged.assumptions,
            dependencies=merged.dependencies)
        m = assess_split_child(src, pseudo_child, propositions,
                               independence_of,
                               entailments.get(src.obligation_id, ""))
        # Rewrite as a merge mapping (source -> merged part).
        m = ProofMapping(
            source_obligation=(f"{src.obligation_id}@{src.revision_id}"),
            target_obligation=(f"{merged.obligation_id}@"
                               f"{merged.revision_id}"),
            target_part=part, relation=m.relation,
            evidence_refs=m.evidence_refs, justification=m.justification,
            scope_note=m.scope_note)
        mappings.append(m)
        verdicts[src.obligation_id] = _migration_verdict_for_mapping(
            m, new_evidence_establishes=new_evidence.get(
                src.obligation_id, False))

    # New obligations introduced by the merge need their own proof.
    unproved = []
    for ob in new_obligations:
        covered = any(
            p.scope.covers(ob.region.envelope)
            and _independence_sufficient_for(p.independence, "independent")
            for p in propositions)
        if not covered:
            unproved.append(ob.obligation_id)

    # Compatibility across sources (cross-obligation: predicate may differ).
    # Each set carries only the evidence actually mapped to that source —
    # never the whole proposition pool.
    ev_by_source = {}
    for m in mappings:
        sid = m.source_obligation.split("@")[0]
        ev_by_source.setdefault(sid, set()).update(m.evidence_refs)
    sets = tuple(
        SupportSet(set_id=f"SUPPORT-{s.obligation_id}",
                   evidence_refs=tuple(sorted(
                       ev_by_source.get(s.obligation_id, ()))),
                   covers=(s.obligation_id,),
                   scope=s.scope,
                   policy_version=policy_versions.get(
                       s.obligation_id, ""))
        for s in sources)
    compat = check_compatibility(sets, origin_of, require_predicate=False)

    correlated = []
    by_origin: dict = {}
    for s in sources:
        for m in mappings:
            if m.source_obligation.startswith(s.obligation_id + "@"):
                for ev in m.evidence_refs:
                    by_origin.setdefault(origin_of.get(ev, ev), set()).add(
                        s.obligation_id)
    for origin, sids in sorted(by_origin.items()):
        if len(sids) > 1:
            correlated.append(f"{origin}={'&'.join(sorted(sids))}")

    if unproved or not compat.compatible:
        overall = "INSUFFICIENT_EVIDENCE"
    elif connective == "OR" and any(
            v in ("CARRIED_FORWARD", "REQUALIFIED")
            for v in verdicts.values()):
        # A OR B: evidence sufficient for either alternative may qualify
        # it — requiring both would unnecessarily strengthen the
        # obligation. Take the best established alternative.
        overall = min(verdicts.values(),
                      key=lambda v: _VERDICT_SEVERITY[v])
    else:
        overall = max(verdicts.values(),
                      key=lambda v: _VERDICT_SEVERITY[v])
    return MergePlan(
        sources=tuple(sources), merged=merged, mappings=tuple(mappings),
        new_obligations=tuple(new_obligations),
        unproved_obligations=tuple(unproved), connective=connective,
        compatibility_notes=compat.failures + compat.notes,
        correlated_sources=tuple(correlated),
        part_verdicts=verdicts, overall_verdict=overall)

# ---------------------------------------------------------------------------
# Two-direction migration audit.
# ---------------------------------------------------------------------------
# Forward sufficiency: does the migrated evidence (plus any new evidence)
# support what the new requirement asserts?
#   E_migrated ^ E_new => O_target
# Backward fidelity: has the migration preserved the intended meaning and
# boundaries of the previous obligations, or explicitly documented their
# changes? Differences must be visible and authorized — not necessarily
# equivalent. A merge that removes the independent-verification requirement
# is a substantive weakening, not a harmless consolidation.

def forward_sufficiency_split(plan: SplitPlan,
                              new_evidence_establishes: dict | None = None
                              ) -> tuple:
    """Forward check for a split: every child must have either an ENTAILS
    mapping (migrated evidence suffices) or new evidence that establishes
    it. Returns (holds, gaps) where gaps names the uncovered children."""
    new_evidence_establishes = new_evidence_establishes or {}
    gaps = [cid for cid, m in
            ((c.obligation_id, mp) for c, mp in
             zip(plan.children, plan.mappings))
            if m.relation != "ENTAILS"
            and not new_evidence_establishes.get(cid, False)]
    return (not gaps, tuple(gaps))


def forward_sufficiency_merge(plan: MergePlan,
                               new_evidence_establishes: dict | None = None
                               ) -> tuple:
    """Forward check for a merge: every assigned part must be entailed or
    newly established, AND every new interaction obligation must have its
    own proof. Returns (holds, gaps)."""
    new_evidence_establishes = new_evidence_establishes or {}
    gaps = []
    for m in plan.mappings:
        if m.relation != "ENTAILS" and not new_evidence_establishes.get(
                m.target_part, False):
            gaps.append(f"part:{m.target_part}")
    gaps.extend(f"interaction:{oid}" for oid in plan.unproved_obligations)
    if plan.connective == "AND":
        pass  # every part required — gaps above are exact
    else:  # OR: evidence sufficient for either alternative may qualify
        gaps = [g for g in gaps if not g.startswith("part:")]
        part_gaps = [g for g in
                     (f"part:{m.target_part}" for m in plan.mappings)
                     if m.relation != "ENTAILS"]
        if part_gaps and len(part_gaps) == len(plan.mappings):
            gaps.append("or_alternatives:all_ungrounded")
    return (not gaps, tuple(gaps))


def backward_fidelity(changes: tuple) -> tuple:
    """Backward check: every requirement touched by the migration must be
    classified (no silent drops). Returns (report, needs_authority).

    needs_authority is True when any change is a consequential weakening
    or a consequential removal — the migration mechanism cannot award
    itself permission to lower proof standards. The certificate must then
    carry weakening_approved_by from the governing authority.
    """
    report = {}
    needs_authority = False
    for ch in changes:
        report[ch.requirement] = ch.fidelity
        if ch.consequential and ch.fidelity in ("weakened", "removed"):
            needs_authority = True
    return report, needs_authority


# ---------------------------------------------------------------------------
# Migration certificate: one append-only, machine-readable record.
# ---------------------------------------------------------------------------
# References original test receipts; never invents new independent evidence
# from reused results. Binds source/target manifests, content hashes,
# policy-effective periods, code/runtime versions, and the verifier's
# evidence. Historical receipts are always PRESERVED.
@dataclass(frozen=True)
class MigrationCertificate:
    event_type: str = "COMPOSITE_PROOF_MIGRATION"
    migration_id: str = ""
    operation: str = ""              # SPLIT | MERGE
    source_obligations: tuple = ()   # (obligation_id@revision_id, ...)
    target_obligation: str = ""      # obligation_id@revision_id
    mappings: tuple = ()             # ProofMapping
    unproved_obligations: tuple = ()
    environment_compatibility: str = "PENDING"  # PENDING|VERIFIED|INCOMPATIBLE
    independent_verification: str = "PENDING"   # PENDING|VERIFIED
    per_obligation_verdicts: dict = field(default_factory=dict)
    per_obligation_migration_verdicts: dict = field(default_factory=dict)
    overall_migration_verdict: str = ""
    target_qualification: str = ""   # one of revocation.VERDICTS
    historical_receipts: str = "PRESERVED"
    source_manifest: str = ""
    source_hashes: tuple = ()
    target_manifest: str = ""
    policy_effective_period: str = ""
    code_version: str = ""
    runtime_version: str = ""
    verifier: str = ""
    weakening_approved_by: str = ""  # required when backward fidelity
                                    # found consequential weakening

    def __post_init__(self):
        assert self.operation in MIGRATION_OPERATIONS, self.operation
        assert self.target_qualification in VERDICTS or not \
            self.target_qualification, self.target_qualification


def issue_split_certificate(migration_id: str, plan: SplitPlan,
                            new_evidence: dict | None = None,
                            verifier: str = "",
                            weakening_approved_by: str = "",
                            **bind) -> MigrationCertificate:
    """Build the append-only certificate for a split. The target
    qualification is the per-child composition (see
    qualification_verdict_for); the historical receipt for the old
    obligation is never modified."""
    new_evidence = new_evidence or {}
    holds, _ = forward_sufficiency_split(plan, new_evidence)
    per_child = {}
    for child in plan.children:
        mv = plan.child_verdicts[child.obligation_id]
        per_child[child.obligation_id] = qualification_verdict_for(
            mv, new_evidence_establishes=new_evidence.get(
                child.obligation_id, False))
    overall_q = per_child[max(
        per_child, key=lambda c: _VERDICT_SEVERITY[
            plan.child_verdicts[c]])] if per_child else "INSUFFICIENT_DATA"
    return MigrationCertificate(
        migration_id=migration_id, operation="SPLIT",
        source_obligations=(f"{plan.old.obligation_id}@"
                            f"{plan.old.revision_id}",),
        target_obligation=",".join(
            f"{c.obligation_id}@{c.revision_id}" for c in plan.children),
        mappings=plan.mappings,
        unproved_obligations=tuple(
            c.obligation_id for c in plan.children
            if plan.child_verdicts[c.obligation_id]
            in ("INSUFFICIENT_EVIDENCE",)),
        per_obligation_verdicts=per_child,
        per_obligation_migration_verdicts=dict(plan.child_verdicts),
        overall_migration_verdict=plan.overall_verdict,
        target_qualification=overall_q,
        verifier=verifier, weakening_approved_by=weakening_approved_by,
        **bind)


def issue_merge_certificate(migration_id: str, plan: MergePlan,
                            new_evidence: dict | None = None,
                            verifier: str = "",
                            weakening_approved_by: str = "",
                            **bind) -> MigrationCertificate:
    """Build the append-only certificate for a merge. If new interaction
    obligations are unproved, the target qualification cannot be
    established no matter how green the components are."""
    new_evidence = new_evidence or {}
    holds, _ = forward_sufficiency_merge(plan, new_evidence)
    per_part = {}
    for src in plan.sources:
        mv = plan.part_verdicts[src.obligation_id]
        per_part[src.obligation_id] = qualification_verdict_for(mv)
    target_q = qualification_verdict_for(
        plan.overall_verdict,
        prior_target_verdict="REQUALIFIED"
        if plan.unproved_obligations else None)
    return MigrationCertificate(
        migration_id=migration_id, operation="MERGE",
        source_obligations=tuple(
            f"{s.obligation_id}@{s.revision_id}" for s in plan.sources),
        target_obligation=(f"{plan.merged.obligation_id}@"
                           f"{plan.merged.revision_id}"),
        mappings=plan.mappings,
        unproved_obligations=plan.unproved_obligations,
        per_obligation_verdicts=per_part,
        per_obligation_migration_verdicts=dict(plan.part_verdicts),
        overall_migration_verdict=plan.overall_verdict,
        target_qualification=target_q,
        verifier=verifier, weakening_approved_by=weakening_approved_by,
        **bind)


# ---------------------------------------------------------------------------
# Migration verdicts compose with the six qualification verdicts and the
# region verdicts — per obligation, never as one blanket.
# ---------------------------------------------------------------------------
def qualification_verdict_for(migration_verdict: str,
                              new_evidence_establishes: bool = False,
                              prior_target_verdict: str | None = None
                              ) -> str:
    """Map one obligation's migration verdict onto revocation's six
    qualification verdicts.

      CARRIED_FORWARD    -> the source qualification's verdict is preserved
                            through the migration (evidence re-verified
                            against the new obligation; same standing).
      PARTIALLY_MIGRATED -> DOWNGRADED (a narrower claim remains supportable).
      BRIDGE_REQUIRED    -> SUSPENDED (pending bridge/integration evidence).
      REQUALIFIED        -> REQUALIFIED.
      INSUFFICIENT_EVIDENCE -> INSUFFICIENT_DATA.
      INCOMPATIBLE       -> REVOKED if a standing target qualification relied
                            on the migrated evidence (its basis conflicts);
                            otherwise INSUFFICIENT_DATA with the
                            incompatibility recorded.
    """
    assert migration_verdict in MIGRATION_VERDICTS, migration_verdict
    if migration_verdict == "CARRIED_FORWARD":
        return prior_target_verdict or "REQUALIFIED"
    if migration_verdict == "PARTIALLY_MIGRATED":
        return "DOWNGRADED"
    if migration_verdict == "BRIDGE_REQUIRED":
        return "SUSPENDED"
    if migration_verdict == "REQUALIFIED":
        return "REQUALIFIED"
    if migration_verdict == "INSUFFICIENT_EVIDENCE":
        return "INSUFFICIENT_DATA"
    # INCOMPATIBLE
    return "REVOKED" if prior_target_verdict else "INSUFFICIENT_DATA"


def reconstruct_from_certificate(cert: MigrationCertificate,
                                 receipts: tuple) -> dict:
    """Cold-successor reconstruction: from the certificate and the original
    receipts only — no chat context, no builder interpretation — reproduce
    each target obligation's standing and every outstanding proof gap.

    Deterministic: a fresh Naya with the same inputs reaches the same
    answer. Returns obligation_id -> {migration_verdict,
    qualification_verdict, evidence_refs, gap}.
    """
    receipt_by_ob = {}
    for r in receipts:
        receipt_by_ob.setdefault(
            (r.obligation_id, r.revision_id), []).append(r.receipt_id)
    out = {}
    mig_by_ob = cert.per_obligation_migration_verdicts
    for m in cert.mappings:
        tgt = m.target_part or m.target_obligation
        mv = (mig_by_ob.get(tgt)
              or mig_by_ob.get(m.target_obligation.split("@")[0])
              or mig_by_ob.get(m.source_obligation.split("@")[0])
              or cert.overall_migration_verdict)
        qv = cert.per_obligation_verdicts.get(
            tgt, cert.per_obligation_verdicts.get(
                m.source_obligation.split("@")[0],
                qualification_verdict_for(mv)))
        gap = None
        if mv in ("INSUFFICIENT_EVIDENCE", "PARTIALLY_MIGRATED",
                  "BRIDGE_REQUIRED", "INCOMPATIBLE"):
            gap = (f"{mv}: {m.scope_note or m.relation} — "
                   f"see unproved_obligations={cert.unproved_obligations}")
        out[tgt] = {
            "migration_verdict": mv,
            "qualification_verdict": qv,
            "evidence_refs": m.evidence_refs,
            "receipts": receipt_by_ob.get(
                tuple(m.source_obligation.split("@")), []),
            "gap": gap,
            "historical_receipts": cert.historical_receipts,
        }
    return out


# ---------------------------------------------------------------------------
# Interaction-proof layer (merge migrations): "A merge may inherit valid
# component evidence. It must not inherit proof of an interaction that was
# never established."
# ---------------------------------------------------------------------------
# Administrative merge (unchanged requirements grouped for convenience — no
# new behavioral claim): proof may compose if compatible. Semantic merge
# (components cooperate, exchange info, preserve shared state, operate in
# sequence, produce an end-to-end result): the cooperation IS an additional
# claim requiring proof. Interactions create their own failure modes — a
# component can behave correctly in isolation and still participate in an
# unsafe system-wide execution.
#
# Maps onto CONNECT (identify the interaction) -> PROVE (bind evidence) ->
# VERIFY (qualify the invariant) -> LAW/ACT (apply eligibility).

# Six interaction classes. Discovered from actual handoffs, shared
# resources, and temporal dependencies — never manufactured as all possible
# pairs. No material interaction = no artificial obligation.
INTERACTION_CLASSES = (
    "data_contract",      # producer guarantees vs consumer assumptions
    "ordering_timing",    # sequence, deadlines, freshness at commit boundary
    "shared_state",       # caches, versions, concurrent writers
    "authority_privacy",  # authorization scope, expiry, privacy boundaries
    "failure_coupling",   # retries, partial failures, duplicates, cascades
    "emergent_behavior",  # properties only visible at system level
)

# Five discovery checks run against the merged requirement text and the
# components' actual contracts.
DISCOVERY_CHECKS = (
    "semantic_comparison",   # new words (together/before/always/across/
                             # improves) signal unproven relationships
    "contract_comparison",   # producer guarantees vs consumer assumptions
                             # (e.g. receipt expiry mismatch)
    "dependency_tracing",    # real code paths, event sequences, caches,
                             # shared versions
    "failure_analysis",      # what goes wrong when both are individually
                             # correct (races, duplicates, contradictions)
    "environment_comparison",# staging vs target differences that change the
                             # interaction
)

# Proof ladder: five rungs; use what the risk warrants. A formal argument
# may substitute for testing where rigorous; high-risk distributed
# workflows may need several complementary methods.
PROOF_LADDER = (
    "contract_proof",        # assume-guarantee on the interaction contract
    "pairwise_integration",  # two-party interaction test
    "multi_party_composition",  # 3+ party hyperedge test
    "environment_bridge",    # the interaction holds in the target env
    "independent_end_to_end",# full-path independent demonstration
)

# Semantic triggers: words in a merged requirement that signal an
# unproven relationship between components.
INTERACTION_TRIGGERS = (
    "together", "before", "after", "always", "across", "improves",
    "influences", "preserves", "end-to-end", "jointly", "while",
)


@dataclass(frozen=True)
class InteractionObligation:
    """One interaction introduced by a merge. A hyperedge: participants may
    be 2+ obligations — some failures emerge only with three or more
    parties (e.g. KNOW+LAW+ACT each correct but on inconsistent
    target-resource versions). Represented as an explicit obligation
    linked to canonical objects, not a second graph."""
    interaction_id: str
    participants: tuple          # obligation_ids
    interaction_class: str       # one of INTERACTION_CLASSES
    invariant: str               # e.g. [](ACT commits => currently authorized)
    preconditions: tuple = ()
    environment: str = ""
    proof_ladder_rung: str = ""  # one of PROOF_LADDER when proven
    independent_proof: str = ""  # verifier receipt, or "" if unproved

    def __post_init__(self):
        assert self.interaction_class in INTERACTION_CLASSES, \
            self.interaction_class
        if self.proof_ladder_rung:
            assert self.proof_ladder_rung in PROOF_LADDER, \
                self.proof_ladder_rung


@dataclass(frozen=True)
class InteractionContract:
    """The contract VERIFY must independently qualify. The invariant is a
    specification, not proof — VERIFY must determine the implementation
    upholds it. Success and failure witnesses make the contract falsifiable.
    Never let an agent create an interaction edge and treat the edge's
    existence as proof."""
    interaction_id: str
    participants: tuple
    interaction: str
    precondition: str
    invariant: str
    success_witness: str   # what independent evidence shows it holding
    failure_witness: str   # what would show it violated
    environment: str
    independent_proof: str = ""


@dataclass(frozen=True)
class InteractionReceipt:
    """Append-only evidence that an interaction was qualified (or failed).
    Binds code SHA, policy version, runtime — an interaction qualified in
    staging does not certify production."""
    interaction_id: str
    participants: tuple
    invariant: str
    preconditions: tuple
    code_sha: str
    policy_version: str
    runtime: str
    positive_receipts: tuple = ()
    negative_receipts: tuple = ()
    independent_verification: str = ""
    qualification: str = ""  # one of VERDICTS

    def __post_init__(self):
        if self.qualification:
            assert self.qualification in VERDICTS, self.qualification


def discover_interactions(merged_text: str,
                          component_contracts: tuple) -> tuple:
    """Run the five discovery checks (as far as a spec can): semantic
    triggers in the merged text plus contract mismatches between
    components. Returns candidate InteractionObligation shells
    (interaction_id, participants, class, invariant sketch) for the
    independent verifier to confirm or reject — discovery proposes,
    VERIFY disposes. Never manufactures obligations where no material
    interaction exists."""
    found = []
    lowered = merged_text.lower()
    triggers = [t for t in INTERACTION_TRIGGERS if t in lowered]
    # Contract comparison: producer guarantee vs consumer assumption
    # mismatches on the (guarantee, assumption) pairs supplied.
    for i, (prod_id, guarantees) in enumerate(component_contracts):
        for j, (cons_id, assumptions) in enumerate(component_contracts):
            if i == j:
                continue
            for g in guarantees:
                for a in assumptions:
                    if g != a and g.split(":")[0] == a.split(":")[0]:
                        found.append(InteractionObligation(
                            interaction_id=(
                                f"INT-{prod_id}-{cons_id}-{g.split(':')[0]}"),
                            participants=(prod_id, cons_id),
                            interaction_class=(
                                "authority_privacy"
                                if "authoriz" in g or "expir" in g
                                else "data_contract"),
                            invariant=f"{cons_id} requires {a}; "
                                      f"{prod_id} guarantees {g}",
                            preconditions=(a,)))
    if triggers:
        found.append(InteractionObligation(
            interaction_id="INT-SEMANTIC-TRIGGERS",
            participants=tuple(c[0] for c in component_contracts),
            interaction_class="emergent_behavior",
            invariant=(f"merged requirement asserts {triggers}; each "
                       "triggered relationship needs its own proof"),
            preconditions=tuple(f"trigger:{t}" for t in triggers)))
    # De-duplicate by interaction_id, preserving order.
    seen, out = set(), []
    for ob in found:
        if ob.interaction_id not in seen:
            seen.add(ob.interaction_id)
            out.append(ob)
    return tuple(out)


def interaction_proof_status(obligations: tuple,
                             receipts: tuple) -> dict:
    """Map each discovered interaction obligation to its proof status from
    independent receipts. An interaction with no independent_proof receipt
    is UNPROVED — its existence as a discovered obligation is not evidence
    that it holds."""
    by_id = {}
    for r in receipts:
        by_id.setdefault(r.interaction_id, []).append(r)
    status = {}
    for ob in obligations:
        rs = by_id.get(ob.interaction_id, [])
        proved = [r for r in rs
                  if r.independent_verification and r.qualification
                  in ("REQUALIFIED", "UNAFFECTED")]
        failed = [r for r in rs if r.negative_receipts]
        if proved and not failed:
            status[ob.interaction_id] = ("PROVED", proved[0].interaction_id)
        elif failed:
            status[ob.interaction_id] = ("FAILED", failed[0].interaction_id)
        else:
            status[ob.interaction_id] = ("UNPROVED", None)
    return status


def merge_with_interactions(sources: tuple, merged: ObligationRevision,
                            part_of: dict, propositions: tuple,
                            independence_of: dict, origin_of: dict,
                            component_contracts: tuple = (),
                            interaction_receipts: tuple = (),
                            **merge_kw) -> tuple:
    """plan_merge extended with the interaction-proof layer.

    Discovers candidate interactions from the merged text + component
    contracts, checks their proof status against independent receipts,
    and folds unproved interactions into the plan's unproved_obligations.
    Returns (MergePlan, interaction_status). A merge may inherit valid
    component evidence; it must not inherit proof of an interaction that
    was never established.
    """
    discovered = discover_interactions(merged.requirement_text,
                                       component_contracts)
    status = interaction_proof_status(discovered, interaction_receipts)
    unproved_interactions = tuple(
        ob.interaction_id for ob in discovered
        if status[ob.interaction_id][0] != "PROVED")
    new_obs = tuple(
        ProofObligation(
            obligation_id=ob.interaction_id,
            region=ClaimRegion(
                ob.interaction_id,
                MeaningEnvelope(
                    component="+".join(ob.participants),
                    behavior=f"interaction:{ob.interaction_class}")),
            acceptance=f"invariant holds: {ob.invariant}",
            kind="interaction")
        for ob in discovered)
    plan = plan_merge(sources, merged, part_of, propositions,
                      independence_of, origin_of,
                      new_obligations=new_obs, **merge_kw)
    # Unproved interactions block the merged qualification even when every
    # component carried forward.
    extra_unproved = tuple(
        oid for oid in unproved_interactions
        if oid not in plan.unproved_obligations)
    if extra_unproved:
        plan = MergePlan(
            sources=plan.sources, merged=plan.merged,
            mappings=plan.mappings,
            new_obligations=plan.new_obligations,
            unproved_obligations=(
                plan.unproved_obligations + extra_unproved),
            connective=plan.connective,
            compatibility_notes=plan.compatibility_notes,
            correlated_sources=plan.correlated_sources,
            part_verdicts=plan.part_verdicts,
            overall_verdict="INSUFFICIENT_EVIDENCE")
    return plan, status

# ---------------------------------------------------------------------------
# Multi-obligation interaction invariants (3+ parties).
# ---------------------------------------------------------------------------
# Governing law: "Every consequential multi-node interaction must preserve
# one coherent execution context, satisfy all required obligations
# simultaneously, and demonstrate that their composition maintains the
# intended system-wide guarantees."
#
# Core insight: valid KNOW->LAW + valid LAW->ACT != valid KNOW->LAW->ACT.
# KNOW applies a lesson to decision D-101 (PASS), LAW authorizes D-102
# (PASS), ACT executes with D-102's authorization (PASS locally) — but no
# proof the learned plan and the authorized action are ONE coherent
# decision. Pairwise green, joint execution invalid. The missing piece is
# a joint consistency guarantee via shared execution-context binding: all
# participants agree on identity, operation, target, parameters, evidence
# versions, and authorization conditions.
#
# Principle: "A multi-party interaction is a distinct obligation whenever
# correctness depends on something that can fail despite all participating
# components and pairwise handoffs passing."
#
# Placement: CONNECT represents the interaction (canonical object, not a
# second graph) -> PROVE binds evidence -> VERIFY tests joint behavior ->
# LAW governs -> ACT enforces.

# Join keys: the shared execution context every participant must bind.
JOIN_KEYS = ("decision_id", "principal_id", "action_digest", "target_id")

# Six invariant categories.
INVARIANT_CATEGORIES = (
    "joint_identity",          # cross-receipt binding: one coherent context
    "temporal_ordering",       # causal event-trace ordering constraints
    "shared_consistency",      # snapshot/version validation across parties
    "authority_non_escalation",# KNOW+LEARN cannot override LAW
    "end_to_end_integrity",    # independent source-level replay
    "failure_containment",     # fault injection + concurrency
)

INVARIANT_KINDS = ("SAFETY", "TEMPORAL", "LIVENESS")

# Three complementary verification techniques.
VERIFICATION_TECHNIQUES = (
    "formal_model",          # abstract state machine; invariants checked
                             # over interleavings
    "fault_injection",       # reordered events, stale state, retries,
                             # competing workers, exact traces
    "independent_end_to_end",# verifier reconstructs from code + policies +
                             # traces + environment
)


@dataclass(frozen=True)
class InvariantSpec:
    """One machine-checkable invariant. The predicate is a reference to an
    exact reviewed machine definition — never a free string. Every
    invariant carries both a positive witness and a counterexample: an
    invariant that cannot be falsified cannot be verified. Refusing
    everything proves nothing — usefulness requirements (liveness)
    matter too."""
    invariant_id: str
    category: str              # one of INVARIANT_CATEGORIES
    kind: str                  # SAFETY | TEMPORAL | LIVENESS
    predicate: str             # reviewed machine definition reference
    positive_witness: str
    counterexample: str

    def __post_init__(self):
        assert self.category in INVARIANT_CATEGORIES, self.category
        assert self.kind in INVARIANT_KINDS, self.kind
        assert self.counterexample, \
            "every invariant must state what would falsify it"


@dataclass(frozen=True)
class ExecutionContext:
    """The shared execution context. All participants in a multi-party
    interaction must bind the SAME context — this is the joint consistency
    guarantee that pairwise checks cannot provide."""
    decision_id: str
    principal_id: str
    action_digest: str
    target_id: str

    def matches(self, other: "ExecutionContext") -> bool:
        return (self.decision_id == other.decision_id
                and self.principal_id == other.principal_id
                and self.action_digest == other.action_digest
                and self.target_id == other.target_id)

    def mismatch_fields(self, other: "ExecutionContext") -> tuple:
        return tuple(
            k for k in JOIN_KEYS
            if getattr(self, k) != getattr(other, k))


@dataclass(frozen=True)
class MultiPartyInteraction:
    """A multi-party interaction as a first-class, versioned canonical
    intelligence object — with its own proof identity, but NOT its own
    authority source (authority remains with LAW). Revisions link by
    supersession, like obligations."""
    interaction_id: str
    revision: str
    participant_obligations: tuple  # (obligation_id@revision, ...)
    execution_context: ExecutionContext
    preconditions: tuple = ()
    invariants: tuple = ()          # InvariantSpec
    ordering_constraints: tuple = ()# (earlier_event, later_event) pairs
    shared_state_constraints: tuple = ()
    environment_scope: MeaningEnvelope = MeaningEnvelope()
    proof_requirements: tuple = ()  # subset of VERIFICATION_TECHNIQUES
    supersedes: str = ""

    def __post_init__(self):
        for t in self.proof_requirements:
            assert t in VERIFICATION_TECHNIQUES, t


@dataclass(frozen=True)
class EventRecord:
    """One source-bound event. Ordering is by source-bound sequence ids
    within the decision's correlation scope — timestamps alone are
    insufficient for distributed ordering."""
    event: str
    decision_id: str
    seq: int
    at: str = ""


# Required causal order for learned authorized execution:
# KnowledgeApplied(d) ≺ PlanFinalized(d) ≺ Commit(d).
REQUIRED_ORDER = (("knowledge_applied", "plan_finalized"),
                  ("plan_finalized", "commit"))


def check_joint_consistency(participant_contexts: dict) -> tuple:
    """Do all participants bind the same execution context?

    participant_contexts: participant_id -> ExecutionContext (as bound by
    that participant's receipts). Returns (consistent, mismatches) where
    mismatches lists (participant, fields) that diverge from the first
    participant's context.

    The D-101/D-102 case: KNOW's receipts bind decision D-101, LAW's bind
    D-102 — each pairwise check passes, but the joint execution has no
    coherent decision. This check fails it.
    """
    items = list(participant_contexts.items())
    if not items:
        return True, ()
    _, first = items[0]
    mismatches = []
    for pid, ctx in items[1:]:
        bad = first.mismatch_fields(ctx)
        if bad:
            mismatches.append((pid, bad))
    return (not mismatches, tuple(mismatches))


def check_temporal_order(events: tuple, decision_id: str,
                         required: tuple = REQUIRED_ORDER) -> tuple:
    """Verify the required causal order for one decision, by source-bound
    sequence ids. Returns (holds, violations). A lesson applied AFTER the
    plan was finalized cannot have influenced it — the temporal invariant
    [] (Commit(d) => KnowledgeApplied(d) < PlanFinalized(d) < Commit(d))
    fails regardless of what the components claim."""
    seq_of = {}
    for e in events:
        if e.decision_id == decision_id:
            seq_of.setdefault(e.event, e.seq)
    violations = []
    for earlier, later in required:
        if earlier in seq_of and later in seq_of:
            if not seq_of[earlier] < seq_of[later]:
                violations.append((earlier, later))
        elif earlier not in seq_of:
            violations.append((earlier, "missing"))
    return (not violations, tuple(violations))


def check_commit_eligibility(commit: EventRecord,
                             eligibility_snapshot: dict,
                             revocations: tuple) -> tuple:
    """The T1-T4 race, decided at the commit boundary.

    T1: KNOW returns evidence E1. T2: LAW approves. T3: E1 becomes
    ineligible. T4: ACT commits using E1. Eligibility must be re-verified
    against a consistent snapshot AT COMMIT; any revocation ordered before
    the commit boundary blocks the commit.

    The proof obligation covers the ACTUAL concurrency mechanism
    (transactional checks, version-bound tokens, locking) — not merely
    "a pre-execution check exists". Reread-then-write without a bound
    token leaves a TOCTOU race this check is designed to catch.

    eligibility_snapshot: evidence_ref -> (eligible: bool, snapshot_seq)
    revocations: ((evidence_ref, revoke_seq), ...) ordered before/after.
    Returns (may_commit, reasons).
    """
    reasons = []
    for ev, (eligible, snap_seq) in sorted(eligibility_snapshot.items()):
        if not eligible:
            return False, (f"{ev}: ineligible in commit snapshot",)
        for rev_ev, rev_seq in revocations:
            if rev_ev == ev and rev_seq < commit.seq:
                return False, (
                    f"{ev}: revoked at seq {rev_seq} before commit "
                    f"seq {commit.seq} — commit blocked",)
        reasons.append(f"{ev}: eligible at snapshot seq {snap_seq}")
    return True, tuple(reasons + ["commit boundary eligibility holds"])


@dataclass(frozen=True)
class MultiPartyReceipt:
    """Append-only receipt for a multi-party interaction: which
    verification techniques were applied, positive and negative evidence,
    and the independent verifier. Binds the join keys actually checked."""
    interaction_id: str
    revision: str
    join_keys: dict
    techniques_applied: tuple = ()
    positive_receipts: tuple = ()
    negative_receipts: tuple = ()
    independent_verification: str = ""
    qualification: str = ""
    invalidated_by: str = ""  # receipt id that invalidated this one, if any

    def __post_init__(self):
        for t in self.techniques_applied:
            assert t in VERIFICATION_TECHNIQUES, t
        if self.qualification:
            assert self.qualification in VERDICTS, self.qualification


def assess_multi_party(interaction: MultiPartyInteraction,
                       participant_contexts: dict,
                       events: tuple,
                       receipts: tuple) -> dict:
    """Incremental joint assessment. Returns per-category status plus the
    overall verdict — narrower results are preserved: pairwise
    qualifications (KNOW+LAW context qualified, LAW+ACT handoff qualified)
    survive even when the 3-party composition is not yet qualified.

    Overall is qualified only when: joint consistency holds, temporal
    order holds, and every invariant has an independent positive receipt
    with no unresolved negative receipt. A receipt invalidation
    recalculates this assessment without revoking proven components.
    """
    consistent, mismatches = check_joint_consistency(participant_contexts)
    decision = interaction.execution_context.decision_id
    ordered, violations = check_temporal_order(events, decision)
    by_inv: dict = {}
    for r in receipts:
        if (r.interaction_id == interaction.interaction_id
                and r.revision == interaction.revision
                and not r.invalidated_by):
            by_inv.setdefault(r.interaction_id, []).append(r)
    inv_status = {}
    for inv in interaction.invariants:
        pos = [r for r in receipts
               if r.interaction_id == interaction.interaction_id
               and not r.invalidated_by
               and r.positive_receipts and not r.negative_receipts
               and r.independent_verification
               and r.qualification in ("REQUALIFIED", "UNAFFECTED")]
        neg = [r for r in receipts
               if r.interaction_id == interaction.interaction_id
               and not r.invalidated_by and r.negative_receipts]
        if neg:
            inv_status[inv.invariant_id] = "FAILED"
        elif pos:
            inv_status[inv.invariant_id] = "PROVED"
        else:
            inv_status[inv.invariant_id] = "UNPROVED"
    categories = {}
    for inv in interaction.invariants:
        categories.setdefault(inv.category, []).append(
            inv_status[inv.invariant_id])
    overall_ok = (consistent and ordered
                  and all(s == "PROVED" for s in inv_status.values())
                  and bool(inv_status))
    return {
        "interaction_id": interaction.interaction_id,
        "joint_consistency": "HOLDS" if consistent else "VIOLATED",
        "mismatches": mismatches,
        "temporal_order": "HOLDS" if ordered else "VIOLATED",
        "order_violations": violations,
        "invariant_status": inv_status,
        "categories": {k: sorted(set(v)) for k, v in categories.items()},
        "overall": "QUALIFIED" if overall_ok else "NOT_QUALIFIED",
    }
