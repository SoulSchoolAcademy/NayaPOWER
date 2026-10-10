"""D32 — Evidence-Bounded Uncertainty Propagation: the evidence-addition path.

Directive D32 (Shawn, 2026-10-10): propagate uncertainty only along the
claims and evidence dependencies that actually require it, while
preserving independently supported conclusions.

Core rule: a downstream claim can never become more certain, broader, or
more causally specific than its admissible evidence supports — but
uncertainty in one upstream source must not invalidate a genuinely
independent, sufficient alternative.

THE GAP THIS FILLS. The existing machinery on main
(drift_canary/uncertainty_propagation.py, propagation.py) governs what
happens when evidence is REMOVED or invalidated: revocation receipts,
dependency-closure recomputation, the five-stage cascade, projection
preservation. What it does not mechanically govern is what happens when
NEW evidence ARRIVES: which additions may legitimately strengthen a
claim, which are mere repetition wearing a new ID, and which are
promotions claiming more than the evidence carries. `_recompute_one`
admits this openly — repetition "never strengthens" only by the caller
passing material changes, i.e. by convention, not by mechanism.

This module makes the addition path mechanical:

1. classify_addition — every incoming evidence item is classified as
   ANCHORING / CORROBORATING / REPEATING / PROMOTING / INADMISSIBLE.
   Repetition is detected structurally (shared origin, ancestor chain,
   secret derivation) and can never raise a verdict. Promotion
   (asserting a stronger verdict, a stronger modality, or a broader
   scope than the evidence carries) is rejected with reasons.
2. No-strengthening ceiling — a REPEATING addition is filtered out of
   every support set before evaluation, so it mechanically cannot move
   any verdict; a verdict may rise only through ANCHORING/CORROBORATING
   additions. Computed, not asserted.
3. recompute_on_addition — given a typed claim graph and a set of
   additions, exactly the claims in the material downstream closure
   recompute (MENTIONS/CONTEXTUAL edges excluded); every other claim is
   UNAFFECTED, computed per claim, not declared.
4. The D32 decisive demonstration — the five-stage fixture extended:
   valid causal evidence arrives, only the affected causal claims
   recompute, the independently observed outcome stays SUPPORTED and
   unchanged, mentioners are untouched, and a repeating "confirmation"
   changes nothing.
5. The false-certainty cascade — an uncertain scheduler hypothesis is
   walked through causal report -> smart note -> brain index ->
   successor package with a promotion attempt at EVERY stage; the
   verifier detects each one, while the independently established
   outcome observation stays usable throughout.

Composition: imports only from on-main modules (uncertainty_propagation,
propagation). Hypothesis verdicts under new evidence come from the
verifier's causal assessment (the `assessed` map) — this module governs
propagation and bounding, not causal inference itself; it never invents
a verdict. Extends the claim envelope's machinery; introduces no new
truth engine. Duck-typed compatible with D30 trace objects (reads
verdicts, modalities, scopes — never D30 internals).
"""

from dataclasses import dataclass, field

from .uncertainty_propagation import (
    MOD_POSSIBLE, MOD_PROBABLE, MOD_CONDITIONAL, MOD_OBSERVED, MOD_VERIFIED,
    propagate_along_edge,
    secret_derivation_check,
    gate_use, USE_CERTIFICATION,
    build_five_stage_cascade_fixture,
)
from .propagation import REGION_VERDICTS

__all__ = [
    "NewEvidence", "ClaimNode",
    "ANCHORING", "CORROBORATING", "REPEATING", "PROMOTING", "INADMISSIBLE",
    "ADDITION_CLASSES",
    "VERDICT_RANK", "MODALITY_RANK",
    "classify_addition", "detect_promotion",
    "material_downstream_closure", "recompute_on_addition",
    "build_d32_addition_fixture", "run_d32_decisive_addition",
    "run_false_certainty_cascade",
]

# ---------------------------------------------------------------------------
# 1. Addition classification.
# ---------------------------------------------------------------------------

ANCHORING = "anchoring"          # new, independently admissible observation
CORROBORATING = "corroborating"  # independent origin, supports existing verdict
REPEATING = "repeating"          # same origin chain / derivation of existing
PROMOTING = "promoting"          # claims more than the evidence carries
INADMISSIBLE = "inadmissible"    # fails basic evidence standards

ADDITION_CLASSES = (ANCHORING, CORROBORATING, REPEATING, PROMOTING,
                    INADMISSIBLE)

KIND_OBSERVATION = "observation"
KIND_DERIVATION = "derivation"
KIND_SUMMARY = "summary"
KIND_COPY = "copy"

EVIDENCE_KINDS = (KIND_OBSERVATION, KIND_DERIVATION, KIND_SUMMARY, KIND_COPY)

# A non-observation can never assert a fresh observed/verified fact: it
# carries no new witnessing, only re-presentation.
KIND_MAX_MODALITY = {
    KIND_OBSERVATION: MOD_VERIFIED,
    KIND_DERIVATION: MOD_CONDITIONAL,
    KIND_SUMMARY: MOD_CONDITIONAL,
    KIND_COPY: MOD_POSSIBLE,
}

MODALITY_RANK = {
    MOD_POSSIBLE: 0,
    MOD_PROBABLE: 1,
    MOD_CONDITIONAL: 1,
    MOD_OBSERVED: 2,
    MOD_VERIFIED: 3,
}

# Certainty rank: how much a verdict settles the question. Both decisive
# verdicts outrank the undecided ones; conflict is informative but not
# decisive.
VERDICT_RANK = {
    "UNDETERMINED": 0,
    "CONFLICTED": 1,
    "REFUTED": 2,
    "SUPPORTED": 2,
}


@dataclass(frozen=True)
class NewEvidence:
    """One incoming evidence item submitted for admission."""
    evidence_id: str
    origin: str                 # independent origin identifier
    kind: str                   # one of EVIDENCE_KINDS
    proposition: str            # the exact proposition it speaks to
    scope: frozenset = field(default_factory=frozenset)
    modality: str = MOD_OBSERVED
    ancestor_chain: tuple = ()  # evidence ids this was produced from
    admissible: bool = True
    inadmissibility_reason: str = ""
    asserted_verdict: str = "UNDETERMINED"  # what the submitter claims
    asserted_modality: str = ""             # "" means: same as modality

    def __post_init__(self):
        assert self.kind in EVIDENCE_KINDS, self.kind
        assert self.asserted_verdict in REGION_VERDICTS, self.asserted_verdict


def _scope_promoted(asserted_scope: frozenset,
                    evidence_scope: frozenset) -> bool:
    """True when the asserted scope is not contained in the evidence
    scope: claiming beyond what was witnessed."""
    return not set(asserted_scope) <= set(evidence_scope)


def classify_addition(new: NewEvidence, existing: tuple,
                      derivation_hints: dict) -> tuple:
    """(classification, reasons). existing: tuple of NewEvidence already
    admitted. derivation_hints maps evidence id -> (origin, transform).

    Order is load-bearing: admissibility first, then promotion (a
    promoting item is rejected even if its origin is fresh), then
    repetition (a fresh ID on old content strengthens nothing), then
    corroborating vs anchoring.
    """
    reasons = []
    if not new.admissible:
        return INADMISSIBLE, (f"inadmissible:{new.inadmissibility_reason}",)

    # --- promotion: claiming more than the evidence carries ---
    # A non-observation re-presents; it inherits its bounds from its
    # declared ancestors, or failing that, from same-origin evidence
    # (a copy carries its origin's bounds). Asserting beyond them is
    # promotion. An observation witnesses directly, so its
    # scope/modality stand as stated (its honesty is the submitter's
    # own qualification).
    eff_modality = new.asserted_modality or new.modality
    if new.kind != KIND_OBSERVATION:
        by_id = {e.evidence_id: e for e in existing}
        ancestors = [by_id[a] for a in new.ancestor_chain if a in by_id]
        if not ancestors:
            ancestors = [e for e in existing if e.origin == new.origin]
        if ancestors:
            cap = max(MODALITY_RANK[a.modality] for a in ancestors)
            if MODALITY_RANK[eff_modality] > cap:
                reasons.append(
                    f"modality_promotion:{new.kind}_exceeds_source_"
                    f"{eff_modality}")
            witnessed = set().union(*(set(a.scope) for a in ancestors))
            if _scope_promoted(new.scope, frozenset(witnessed)):
                reasons.append(
                    "scope_promotion:asserted_beyond_source_scope")
        elif MODALITY_RANK[eff_modality] > MODALITY_RANK[
                KIND_MAX_MODALITY[new.kind]]:
            reasons.append(
                f"modality_promotion:{new.kind}_cannot_assert_{eff_modality}")
    if reasons:
        return PROMOTING, tuple(reasons)

    # --- repetition: same origin chain or a derivation of existing ---
    for old in existing:
        independent, why = secret_derivation_check(
            old.evidence_id, new.evidence_id, derivation_hints)
        if not independent:
            return REPEATING, (f"not_independent_of_{old.evidence_id}:{why}",)
        if new.origin == old.origin and new.kind != KIND_OBSERVATION:
            return REPEATING, (
                f"shared_origin_{new.origin}_without_new_witnessing",)
        if old.evidence_id in new.ancestor_chain:
            return REPEATING, (
                f"ancestor_chain_contains_{old.evidence_id}",)

    # --- corroborating vs anchoring ---
    for old in existing:
        if old.proposition == new.proposition:
            return CORROBORATING, (
                f"independent_origin_{new.origin}_same_proposition_as_"
                f"{old.evidence_id}",)
    return ANCHORING, (f"new_proposition_or_new_resolution_from_{new.origin}",)


# ---------------------------------------------------------------------------
# 2. Promotion detection across projections (the cascade verifier).
# ---------------------------------------------------------------------------

def detect_promotion(asserted_verdict: str, asserted_modality: str,
                     asserted_scope: frozenset, source_verdict: str,
                     source_modality: str, source_scope: frozenset,
                     stage: str) -> tuple:
    """(is_promotion, reasons). A projection may compress words; it may
    never raise certainty, upgrade modality, or widen scope. Every
    promotion is named so the verifier can reject it at the stage where
    it happens."""
    reasons = []
    if VERDICT_RANK[asserted_verdict] > VERDICT_RANK[source_verdict]:
        reasons.append(
            f"verdict_promotion:{source_verdict}_to_{asserted_verdict}")
    if MODALITY_RANK[asserted_modality] > MODALITY_RANK[source_modality]:
        reasons.append(
            f"modality_promotion:{source_modality}_to_{asserted_modality}")
    if _scope_promoted(asserted_scope, source_scope):
        reasons.append("scope_promotion:projection_wider_than_source")
    if reasons:
        return True, (f"{stage}:" + ";".join(reasons),)
    return False, (f"{stage}:no_promotion",)


# ---------------------------------------------------------------------------
# 3. Material downstream closure and recomputation on addition.
# ---------------------------------------------------------------------------

NON_MATERIAL = {"MENTIONS", "CONTEXTUAL"}

_MATERIAL_RELATIONSHIPS = (
    "DERIVED_FROM", "REQUIRES_SUPPORT_FROM",
    "INDEPENDENTLY_CORROBORATED_BY", "PARTIALLY_SUPPORTS",
    "CONTRADICTS", "HYPOTHESIZED_CAUSE_OF",
)


def material_downstream_closure(changed_ids: tuple, claim_graph: dict) -> tuple:
    """claim_graph: claim_id -> ((dep_id, relationship), ...), where
    dep_id may be an evidence id or another claim id. Returns the sorted
    tuple of claim ids reachable from changed_ids through material edges
    only. MENTIONS/CONTEXTUAL edges are citation, not dependence."""
    rev = {}
    for claim_id, deps in claim_graph.items():
        for dep_id, rel in deps:
            rev.setdefault(dep_id, []).append((claim_id, rel))
    seen = set()
    frontier = list(changed_ids)
    while frontier:
        cur = frontier.pop()
        for claim_id, rel in rev.get(cur, ()):
            if rel in NON_MATERIAL or claim_id in seen:
                continue
            seen.add(claim_id)
            frontier.append(claim_id)
    return tuple(sorted(seen))


@dataclass(frozen=True)
class ClaimNode:
    """A claim with its proof dependencies. premises: tuple of
    (premise_id, edge_relationship). composition: 'AND' (all premises
    required) or 'OR' (one sufficient path qualifies)."""
    claim_id: str
    premises: tuple = ()
    composition: str = "AND"
    prior_verdict: str = "UNDETERMINED"

    def __post_init__(self):
        assert self.composition in ("AND", "OR"), self.composition
        assert self.prior_verdict in REGION_VERDICTS, self.prior_verdict


def _compose_verdict(node: ClaimNode, premise_verdicts: dict) -> str:
    """Mechanical verdict from premise verdicts. AND: the weakest premise
    bounds the claim (one unresolved premise blocks qualification through
    that conjunction); a material conflict is preserved, not averaged
    away. OR: the strongest sufficient path qualifies."""
    verdicts = [premise_verdicts[p] for p, _ in node.premises
                if p in premise_verdicts]
    if not verdicts:
        return "UNDETERMINED"
    if node.composition == "AND":
        if "CONFLICTED" in verdicts:
            return "CONFLICTED"
        return min(verdicts, key=lambda v: VERDICT_RANK[v])
    # OR: each premise is a sufficient path. One SUPPORTED path
    # qualifies — but a material independently-supported refutation of
    # the SAME proposition is honored, not erased by the alternative.
    if "SUPPORTED" in verdicts and "REFUTED" in verdicts:
        return "CONFLICTED"
    if "SUPPORTED" in verdicts:
        return "SUPPORTED"
    if all(v == "REFUTED" for v in verdicts):
        return "REFUTED"
    if "CONFLICTED" in verdicts:
        return "CONFLICTED"
    return "UNDETERMINED"


def _topological_claim_order(claims: dict) -> tuple:
    """Claims whose premises are other claims come after them."""
    order, done = [], set()
    remaining = set(claims)
    while remaining:
        progress = False
        for cid in sorted(remaining):
            deps = {p for p, _ in claims[cid].premises if p in claims}
            if deps <= done:
                order.append(cid)
                done.add(cid)
                remaining.remove(cid)
                progress = True
        if not progress:  # cycle: break deterministically, no self-support
            order.extend(sorted(remaining))
            break
    return tuple(order)


def recompute_on_addition(claim_graph: dict, claims: dict,
                          evidence_before: dict, evidence_after: dict,
                          additions: tuple, assessed: dict = None) -> dict:
    """Recompute claim standing after evidence arrives.

    claim_graph: claim_id -> ((dep_id, relationship), ...).
    claims: claim_id -> ClaimNode.
    evidence_before / evidence_after: evidence_id -> verdict.
    additions: tuple of (NewEvidence, classification).
    assessed: optional claim_id -> verdict — the verifier's direct causal
      assessment under the new evidence (for hypothesis claims). This
      module propagates and bounds the assessment; it never invents one.

    Returns claim_id -> (action, reason). Actions:
      UNAFFECTED            outside every material downstream closure
      RECOMPUTED_UNCHANGED  recomputed, verdict identical
      STRENGTHENED          rank rose via ANCHORING/CORROBORATING
      WEAKENED              rank fell
      RESOLVED              UNDETERMINED/CONFLICTED -> decisive verdict
      RECOMPUTED_AMENDMENT_REQUIRED  premises moved under a DERIVED_FROM
                            claim: its stated text is stale, amend it
      PROMOTION_REJECTED    a promoting addition touched it; the promoted
                            assertion was discarded

    The no-strengthening ceiling is structural: REPEATING additions never
    enter any material closure, so they mechanically cannot move any
    verdict; a verdict may rise only through ANCHORING/CORROBORATING.
    """
    assessed = assessed or {}
    material_ids = tuple(ev.evidence_id for ev, cls in additions
                         if cls in (ANCHORING, CORROBORATING))
    promoting_ids = tuple(ev.evidence_id for ev, cls in additions
                          if cls == PROMOTING)

    closure = set(material_downstream_closure(material_ids, claim_graph))
    promoting_closure = set(material_downstream_closure(
        promoting_ids, claim_graph))

    new_verdicts = {}
    out = {}
    for claim_id in _topological_claim_order(claims):
        node = claims[claim_id]
        in_closure = claim_id in closure
        touched_by_promotion = claim_id in promoting_closure
        if not in_closure and not touched_by_promotion:
            out[claim_id] = ("UNAFFECTED",
                             "outside_material_downstream_closure")
            new_verdicts[claim_id] = node.prior_verdict
            continue
        if touched_by_promotion and not in_closure:
            out[claim_id] = ("PROMOTION_REJECTED",
                             "promoting_addition_discarded_verdict_from_"
                             "admissible_evidence_only")
            new_verdicts[claim_id] = node.prior_verdict
            continue

        # Premise verdicts: evidence from the AFTER state, claim
        # premises from their recomputed verdicts.
        premise_verdicts = {}
        for premise_id, rel in node.premises:
            if premise_id in evidence_after:
                v = evidence_after[premise_id]
                if rel in _MATERIAL_RELATIONSHIPS:
                    v, _, _ = propagate_along_edge(v, rel)
                premise_verdicts[premise_id] = v
            elif premise_id in new_verdicts:
                premise_verdicts[premise_id] = new_verdicts[premise_id]

        if claim_id in assessed:
            candidate = assessed[claim_id]
        else:
            candidate = _compose_verdict(node, premise_verdicts) \
                if premise_verdicts else node.prior_verdict

        old_rank = VERDICT_RANK[node.prior_verdict]
        new_rank = VERDICT_RANK[candidate]
        # The ceiling: a rise needs material admissible support in this
        # claim's upstream. Repetition never got into the closure, so a
        # rise here is always via ANCHORING/CORROBORATING.
        if new_rank <= old_rank:
            new_verdicts[claim_id] = candidate
            action = ("RECOMPUTED_UNCHANGED"
                      if candidate == node.prior_verdict else "WEAKENED")
            out[claim_id] = (action, f"{node.prior_verdict}_to_{candidate}")
            continue
        # Rise permitted: the claim is in the material closure.
        new_verdicts[claim_id] = candidate
        action = "RESOLVED" if node.prior_verdict in (
            "UNDETERMINED", "CONFLICTED") else "STRENGTHENED"
        reason = f"{node.prior_verdict}_to_{candidate}_via_material_addition"
        # Amendment check: a DERIVED_FROM claim whose premises moved
        # has stale text — the computed verdict stands, but the claim
        # as stated must be amended, never silently kept.
        premise_moved = any(
            evidence_before.get(p, "UNDETERMINED") != evidence_after.get(p)
            or (p in claims and claims[p].prior_verdict != new_verdicts[p])
            for p, rel in node.premises
            if rel == "DERIVED_FROM")
        if premise_moved and any(rel == "DERIVED_FROM"
                                 for _, rel in node.premises):
            action = "RECOMPUTED_AMENDMENT_REQUIRED"
            reason = (reason + "_premises_moved_text_stale_"
                      "amend_original_preserved")
        out[claim_id] = (action, reason)
    return out


# ---------------------------------------------------------------------------
# 4. The D32 decisive demonstration: valid causal evidence arrives.
# ---------------------------------------------------------------------------

def build_d32_addition_fixture() -> dict:
    """Extends the on-main five-stage cascade fixture with a typed claim
    graph and a genuinely new, independently admissible evidence item:
    the complete dispatch trace for the unobserved interval, from an
    independent telemetry store. The trace shows dispatch WAS issued and
    the lease never reached the worker.

    The graph declares E_trace_complete as a premise of H1/H2 up front:
    the complete trace adjudicates the hypotheses WHEN AVAILABLE. Before
    arrival it is simply absent (UNDETERMINED); arrival is the addition.
    """
    base = build_five_stage_cascade_fixture()

    claims = {
        # The independently observed outcome. Its only premise is the
        # target-state observation: the causal trace is NOT a premise,
        # so causal evidence can never touch it.
        "outcome": ClaimNode(
            claim_id="outcome",
            premises=(("E_outcome", "REQUIRES_SUPPORT_FROM"),),
            composition="AND", prior_verdict="SUPPORTED"),
        # H1: scheduler withheld dispatch. Unresolved until the trace.
        "H1": ClaimNode(
            claim_id="H1",
            premises=(("E_trace_partial", "HYPOTHESIZED_CAUSE_OF"),
                      ("E_trace_complete", "HYPOTHESIZED_CAUSE_OF")),
            composition="AND", prior_verdict="UNDETERMINED"),
        # H2: delivery failed after dispatch. Unresolved until the trace.
        "H2": ClaimNode(
            claim_id="H2",
            premises=(("E_worker_report", "HYPOTHESIZED_CAUSE_OF"),
                      ("E_trace_complete", "HYPOTHESIZED_CAUSE_OF")),
            composition="AND", prior_verdict="UNDETERMINED"),
        # The note's causal sentence derives from the two hypotheses.
        "note_causal": ClaimNode(
            claim_id="note_causal",
            premises=(("H1", "DERIVED_FROM"), ("H2", "DERIVED_FROM")),
            composition="AND", prior_verdict="UNDETERMINED"),
        # A claim that merely mentions the incident keeps its own
        # standing: citation is not dependence.
        "mentioner": ClaimNode(
            claim_id="mentioner",
            premises=(("incident_log", "MENTIONS"),),
            composition="AND", prior_verdict="SUPPORTED"),
    }
    claim_graph = {cid: node.premises for cid, node in claims.items()}

    evidence_before = {
        "E_outcome": "SUPPORTED",        # independent target observation
        "E_trace_partial": "SUPPORTED",  # as observation of the trace
        "E_worker_report": "SUPPORTED",  # as observation of the report
        "incident_log": "SUPPORTED",
        # E_trace_complete absent: the interval is unobserved.
    }
    evidence_after = dict(evidence_before)
    evidence_after["E_trace_complete"] = "SUPPORTED"  # as observation

    new_evidence = NewEvidence(
        evidence_id="E_trace_complete",
        origin="independent_telemetry_store",
        kind=KIND_OBSERVATION,
        proposition="dispatch_issued_SEQ107_110_lease_never_reached_worker",
        scope=frozenset({"SEQ-107:SEQ-110"}),
        modality=MOD_OBSERVED,
        ancestor_chain=(),
        admissible=True,
        asserted_verdict="SUPPORTED",
    )
    # The verifier's causal assessment of the new trace (verifier output,
    # consumed and bounded here — never invented here): dispatch was
    # issued, so "scheduler withheld" is refuted; the lease never
    # arrived, so "delivery failed" is supported.
    causal_assessment = {
        "H1": "REFUTED",
        "H2": "SUPPORTED",
    }
    return {
        "base": base,
        "claims": claims,
        "claim_graph": claim_graph,
        "evidence_before": evidence_before,
        "evidence_after": evidence_after,
        "new_evidence": new_evidence,
        "causal_assessment": causal_assessment,
        "derivation_hints": {
            "E_outcome": ("target_state_sensor", "none"),
            "E_trace_partial": ("scheduler_log", "none"),
            "E_worker_report": ("worker_agent", "none"),
            "incident_log": ("incident_log", "none"),
            "E_trace_complete": ("independent_telemetry_store", "none"),
        },
    }


def _existing_evidence_items():
    return (
        NewEvidence("E_outcome", "target_state_sensor", KIND_OBSERVATION,
                    "workflow_did_not_complete", frozenset({"target"}),
                    MOD_OBSERVED, (), True, "", "SUPPORTED"),
        NewEvidence("E_trace_partial", "scheduler_log", KIND_OBSERVATION,
                    "dispatch_trace_SEQ100_120_partial",
                    frozenset({"SEQ-100:SEQ-120"}), MOD_OBSERVED, (), True,
                    "", "SUPPORTED"),
        NewEvidence("E_worker_report", "worker_agent", KIND_OBSERVATION,
                    "worker_reports_no_lease", frozenset({"worker"}),
                    MOD_OBSERVED, (), True, "", "SUPPORTED"),
    )


def run_d32_decisive_addition() -> dict:
    """The experiment. Valid causal evidence arrives; the verifier must:
    (1) classify it ANCHORING; (2) recompute exactly the affected claims
    (H1, H2, note_causal); (3) leave `outcome` SUPPORTED and unchanged —
    its verdict does not rise, it was already SUPPORTED via its
    independent source; (4) leave `mentioner` UNAFFECTED; (5) demonstrate
    that a repeating 'confirmation' of the new trace changes nothing;
    (6) reject a promoting assertion built on the new evidence."""
    fx = build_d32_addition_fixture()
    new = fx["new_evidence"]
    existing = _existing_evidence_items()
    cls, cls_reasons = classify_addition(new, existing,
                                         fx["derivation_hints"])

    actions = recompute_on_addition(
        fx["claim_graph"], fx["claims"],
        fx["evidence_before"], fx["evidence_after"],
        ((new, cls),), assessed=fx["causal_assessment"])

    # (5) repetition changes nothing: a summary "confirming" the trace.
    repeating = NewEvidence(
        evidence_id="E_trace_complete_summary",
        origin="independent_telemetry_store",
        kind=KIND_SUMMARY,
        proposition=new.proposition,
        scope=new.scope,
        modality=MOD_OBSERVED,
        ancestor_chain=(new.evidence_id,),
        admissible=True,
        asserted_verdict="SUPPORTED",
    )
    rep_cls, rep_reasons = classify_addition(
        repeating, existing + (new,), fx["derivation_hints"])
    rep_actions = recompute_on_addition(
        fx["claim_graph"], fx["claims"],
        fx["evidence_after"], fx["evidence_after"],
        ((repeating, rep_cls),))
    rep_unchanged = all(action == "UNAFFECTED"
                        for action, _ in rep_actions.values())

    # (6) promotion rejected: a summary asserting verified causation of
    # the whole workflow failure from the dispatch trace alone.
    promoting = NewEvidence(
        evidence_id="E_cause_claim",
        origin="analyst_note",
        kind=KIND_SUMMARY,
        proposition="scheduler_caused_workflow_failure",
        scope=frozenset({"SEQ-107:SEQ-110"}),
        modality=MOD_OBSERVED,
        ancestor_chain=(new.evidence_id,),
        admissible=True,
        asserted_verdict="SUPPORTED",
        asserted_modality=MOD_VERIFIED,
    )
    prom_cls, prom_reasons = classify_addition(
        promoting, existing + (new,), fx["derivation_hints"])

    return {
        "addition_classification": (cls, cls_reasons),
        "claim_actions": actions,
        "repetition_classification": (rep_cls, rep_reasons),
        "repetition_changes_nothing": rep_unchanged,
        "promotion_classification": (prom_cls, prom_reasons),
    }


# ---------------------------------------------------------------------------
# 5. The false-certainty cascade: promotion detected at every stage.
# ---------------------------------------------------------------------------

CASCADE_STAGES = ("causal_report", "smart_note", "brain_index",
                  "successor_package")


def run_false_certainty_cascade() -> dict:
    """The sharpest case. An uncertain scheduler explanation (H1:
    UNDETERMINED, MOD_POSSIBLE, scope SEQ-107:SEQ-110) is projected
    through four surfaces. At EVERY stage a promotion is attempted and
    the verifier must detect it. Throughout, the independently
    established outcome observation ('the workflow did not complete':
    SUPPORTED, MOD_OBSERVED, scope {target}) stays usable — checked at
    each stage, not declared.

    Returns per-stage (promotion_detected, reasons) plus the outcome
    standing trace.
    """
    source = {
        "verdict": "UNDETERMINED",
        "modality": MOD_POSSIBLE,
        "scope": frozenset({"SEQ-107:SEQ-110"}),
    }
    outcome = {
        "verdict": "SUPPORTED",
        "modality": MOD_OBSERVED,
        "scope": frozenset({"target"}),
    }
    attempts = {
        # Stage 1: the report asserts the hypothesis as verified fact.
        "causal_report": {
            "verdict": "SUPPORTED", "modality": MOD_VERIFIED,
            "scope": frozenset({"SEQ-107:SEQ-110"})},
        # Stage 2: the note drops 'unresolved' — words carry modality.
        "smart_note": {
            "verdict": "SUPPORTED", "modality": MOD_POSSIBLE,
            "scope": frozenset({"SEQ-107:SEQ-110"}),
            "dropped_word": "unresolved"},
        # Stage 3: the index widens the scope to all sequences.
        "brain_index": {
            "verdict": "UNDETERMINED", "modality": MOD_POSSIBLE,
            "scope": frozenset({"all_sequences"})},
        # Stage 4: the successor package asserts it as the established
        # cause and offers it for certification.
        "successor_package": {
            "verdict": "SUPPORTED", "modality": MOD_OBSERVED,
            "scope": frozenset({"SEQ-107:SEQ-110"})},
    }
    stages = {}
    outcome_trace = []
    for stage in CASCADE_STAGES:
        att = attempts[stage]
        detected, reasons = detect_promotion(
            att["verdict"], att["modality"], att["scope"],
            source["verdict"], source["modality"], source["scope"],
            stage)
        if att.get("dropped_word"):
            detected = True
            reasons = reasons + (
                f"{stage}:dropped_{att['dropped_word']}_"
                f"hypothesis_promoted_to_fact",)
        if stage == "successor_package":
            # Certification use-gate: an UNDETERMINED hypothesis must
            # fail closed for certification at every stage.
            allowed, treatment = gate_use(USE_CERTIFICATION,
                                          source["verdict"])
            if not allowed:
                detected = True
                reasons = reasons + (
                    f"{stage}:certification_use_denied_for_"
                    f"{source['verdict']}_standing:{treatment}",)
        stages[stage] = (detected, reasons)
        outcome_trace.append(
            (stage, outcome["verdict"], outcome["modality"],
             "usable" if outcome["verdict"] == "SUPPORTED" else
             "NOT_USABLE"))
    return {
        "stages": stages,
        "all_promotions_detected": all(d for d, _ in stages.values()),
        "outcome_usable_throughout": all(t[3] == "usable"
                                         for t in outcome_trace),
        "outcome_trace": tuple(outcome_trace),
    }
