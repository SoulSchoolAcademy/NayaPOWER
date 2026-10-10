"""Claim-level truth separation (SPEC, not production code).

Shawn's extension (2026-10-10): "One contaminated claim must not
automatically invalidate an entire lesson. One valid claim must not make
its contaminated neighbors trustworthy."

Ratified principle: "Truth belongs to individual claims and their
evidence. Preservation belongs to the original intelligence object.
Authority belongs to LAW."

Seven stages: PRESERVE -> ATOMIZE -> MAP -> VERIFY -> CLASSIFY ->
PROJECT -> MONITOR.

Two classification systems per claim (canonical vocabulary, no competing
lifecycles):
  Evidence verdict: VERIFIED / CANDIDATE / CONFLICTED / REFUTED / UNKNOWN / SUPERSEDED
  Eligibility:      ELIGIBLE / RESTRICTED / QUARANTINED / REVIEW_REQUIRED
A VERIFIED claim can still be RESTRICTED outside its proven scope.

Claim lineage: SUPPORTS, DERIVED_FROM, REQUIRES, CONTRADICTS, SUPERSEDES.
Contamination propagates along MATERIAL dependencies only: if B REQUIRES A
but is also independently supported by X, recalculate B via X — don't
mechanically mark it false.

The critical gate is at point of USE, not storage: every output path
(semantic search, summaries, agent prompts, eval datasets, successor
packages) must obey claim eligibility. A summary must NEVER quietly
reintroduce quarantined claims as authoritative guidance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Vocabularies (canonical — map to existing, don't invent competing ones) ------

VERIFIED, CANDIDATE, CONFLICTED, REFUTED, UNKNOWN, SUPERSEDED = (
    "VERIFIED", "CANDIDATE", "CONFLICTED", "REFUTED", "UNKNOWN", "SUPERSEDED")
VERDICTS = (VERIFIED, CANDIDATE, CONFLICTED, REFUTED, UNKNOWN, SUPERSEDED)

ELIGIBLE, RESTRICTED, QUARANTINED, REVIEW_REQUIRED = (
    "ELIGIBLE", "RESTRICTED", "QUARANTINED", "REVIEW_REQUIRED")
ELIGIBILITIES = (ELIGIBLE, RESTRICTED, QUARANTINED, REVIEW_REQUIRED)

SUPPORTS, DERIVED_FROM, REQUIRES, CONTRADICTS, SUPERSEDES = (
    "SUPPORTS", "DERIVED_FROM", "REQUIRES", "CONTRADICTS", "SUPERSEDES")
RELATIONS = (SUPPORTS, DERIVED_FROM, REQUIRES, CONTRADICTS, SUPERSEDES)

# Material dependencies: contamination propagates along these.
MATERIAL_RELATIONS = (REQUIRES, DERIVED_FROM)


@dataclass(frozen=True)
class ClaimDependency:
    relation: str          # one of RELATIONS
    target_claim_id: str


@dataclass
class ClaimRecord:
    """Machine-readable claim manifest."""
    claim_id: str
    parent_note_id: str
    source_content_hash: str
    claim_text: str
    claim_type: str = "factual"   # factual | procedural | normative | predictive
    scope: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    dependencies: tuple[ClaimDependency, ...] = ()
    independent_evidence_refs: tuple[str, ...] = ()
    verdict: str = UNKNOWN
    eligibility: str = REVIEW_REQUIRED  # default: not yet cleared
    reason: str = ""
    policy_version: str = "claim-truth-v1"

    def __post_init__(self):
        if self.verdict not in VERDICTS:
            raise ValueError(f"verdict_unknown:{self.verdict}")
        if self.eligibility not in ELIGIBILITIES:
            raise ValueError(f"eligibility_unknown:{self.eligibility}")
        for d in self.dependencies:
            if d.relation not in RELATIONS:
                raise ValueError(f"relation_unknown:{d.relation}")


# Stage 2: ATOMIZE ----------------------------------------------------------------
# (Stage 1 PRESERVE is the immutable parent note — handled by the store.)

def atomize(parent_note_id: str, source_content_hash: str,
            claim_texts: list[tuple[str, str, tuple[str, ...]]],
            policy_version: str = "claim-truth-v1") -> list[ClaimRecord]:
    """Split a note into minimal independently evaluable claims.

    claim_texts: list of (claim_text, claim_type, scope).
    Split until evaluable — but not so far that scope, negation, or
    chronology is lost (each claim keeps its scope; negations stay inside
    the claim text, never factored out).

    Every claim starts at verdict=UNKNOWN, eligibility=REVIEW_REQUIRED:
    unevaluated claims are never eligible by default.
    """
    claims = []
    for i, (text, ctype, scope) in enumerate(claim_texts):
        if not text or not text.strip():
            raise ValueError("atomize_empty_claim")
        claims.append(ClaimRecord(
            claim_id=f"{parent_note_id}#C{i+1:02d}",
            parent_note_id=parent_note_id,
            source_content_hash=source_content_hash,
            claim_text=text.strip(), claim_type=ctype, scope=tuple(scope),
            policy_version=policy_version))
    return claims


# Stage 4/5: VERIFY + CLASSIFY ------------------------------------------------------

def classify(claim: ClaimRecord, verdict: str, eligibility: str,
             reason: str) -> ClaimRecord:
    """Set a claim's verdict + eligibility with a reason. Returns new record
    (claims are immutable; reclassification appends a new version)."""
    return ClaimRecord(
        claim_id=claim.claim_id, parent_note_id=claim.parent_note_id,
        source_content_hash=claim.source_content_hash,
        claim_text=claim.claim_text, claim_type=claim.claim_type,
        scope=claim.scope, evidence_refs=claim.evidence_refs,
        dependencies=claim.dependencies,
        independent_evidence_refs=claim.independent_evidence_refs,
        verdict=verdict, eligibility=eligibility, reason=reason,
        policy_version=claim.policy_version)


def propagate_contamination(claims: dict[str, ClaimRecord]) -> dict[str, ClaimRecord]:
    """Propagate contamination along MATERIAL dependencies only.

    Rules:
    - A claim with verdict REFUTED (or eligibility QUARANTINED) contaminates
      dependents linked by REQUIRES or DERIVED_FROM...
    - ...UNLESS the dependent has independent_evidence_refs: then it is
      recalculated via the independent path (eligibility -> REVIEW_REQUIRED
      with reason "recalculate_via_independent_evidence", NOT mechanical false).
    - SUPPORTS / CONTRADICTS / SUPERSEDES do not propagate contamination
      (contradiction is handled by the contradiction predicate; supersession
      by the supersede path).
    - Propagation is one pass over the graph in dependency order; cycles
      are refused (a cycle is itself circular proof — see qualify_lesson).
    Returns a new claims map; originals untouched (preservation).
    """
    result = dict(claims)
    # detect cycles first (fail-closed: refuse to propagate through a cycle)
    visiting: set[str] = set()
    done: set[str] = set()

    def has_cycle(cid: str) -> bool:
        if cid in done:
            return False
        if cid in visiting:
            return True
        visiting.add(cid)
        for dep in result[cid].dependencies:
            if dep.relation in MATERIAL_RELATIONS and dep.target_claim_id in result:
                if has_cycle(dep.target_claim_id):
                    return True
        visiting.discard(cid)
        done.add(cid)
        return False

    for cid in result:
        if has_cycle(cid):
            raise ValueError(f"contamination_cycle_refused:{cid}")

    changed = True
    while changed:
        changed = False
        for cid, claim in result.items():
            if claim.eligibility == QUARANTINED or claim.verdict == REFUTED:
                continue
            for dep in claim.dependencies:
                if dep.relation not in MATERIAL_RELATIONS:
                    continue
                target = result.get(dep.target_claim_id)
                if target is None:
                    continue
                if target.verdict == REFUTED or target.eligibility == QUARANTINED:
                    if claim.independent_evidence_refs:
                        new = classify(claim, claim.verdict, REVIEW_REQUIRED,
                                       f"recalculate_via_independent_evidence:dependency {dep.target_claim_id} contaminated")
                    else:
                        new = classify(claim, claim.verdict, QUARANTINED,
                                       f"material_dependency_contaminated:{dep.target_claim_id}")
                    if new.eligibility != claim.eligibility:
                        result[cid] = new
                        changed = True
                    break
    return result


# Stage 6: PROJECT -------------------------------------------------------------------

@dataclass(frozen=True)
class ProjectedLesson:
    """The safe reusable lesson: eligible claims only + exclusion manifest."""
    lesson_id: str
    claims: tuple[ClaimRecord, ...]          # ELIGIBLE claims only
    excluded: tuple[tuple[str, str, str], ...]  # (claim_id, eligibility, reason)
    parent_note_id: str
    policy_version: str = "claim-truth-v1"


def project_lesson(lesson_id: str, parent_note_id: str,
                   claims: dict[str, ClaimRecord],
                   use: str = "act") -> ProjectedLesson:
    """Build the safe reusable lesson from ELIGIBLE claims only.

    A claim is projectable iff eligibility == ELIGIBLE. RESTRICTED claims
    are projectable only for read-class uses. QUARANTINED / REVIEW_REQUIRED
    never project into consequential uses. The exclusion manifest names
    every excluded claim and why — nothing is silently dropped.
    """
    included: list[ClaimRecord] = []
    excluded: list[tuple[str, str, str]] = []
    for cid in sorted(claims):
        c = claims[cid]
        if c.eligibility == ELIGIBLE:
            included.append(c)
        elif c.eligibility == RESTRICTED and use in ("read", "investigate", "hypothesize"):
            included.append(c)
        else:
            excluded.append((cid, c.eligibility,
                             c.reason or "not_eligible_for_use:" + use))
    return ProjectedLesson(lesson_id=lesson_id, claims=tuple(included),
                           excluded=tuple(excluded), parent_note_id=parent_note_id)


# Point-of-use gate ---------------------------------------------------------------------

def check_claim_use(claim: ClaimRecord, use: str) -> tuple[bool, str]:
    """Every output path calls this. A summary must NEVER quietly
    reintroduce quarantined claims as authoritative guidance.

    Returns (allowed, reason). Fail-closed on unknown eligibility.
    """
    if claim.eligibility == ELIGIBLE:
        return True, "eligible"
    if claim.eligibility == RESTRICTED:
        if use in ("read", "investigate", "hypothesize"):
            return True, "restricted_read_use_permitted"
        return False, "restricted_consequential_use_blocked"
    if claim.eligibility == QUARANTINED:
        return False, "quarantined_claim_blocked_at_use"
    if claim.eligibility == REVIEW_REQUIRED:
        return False, "review_required_not_yet_cleared"
    return False, "unknown_eligibility_fail_closed"


def filter_summary_claims(claims: list[ClaimRecord], use: str = "read") -> list[ClaimRecord]:
    """The summary path: only claims allowed for `use`. Quarantined claims
    are excluded AND named in the returned exclusion list (no quiet drops).

    Returns the allowed claims. Callers must render the exclusion manifest
    alongside — see ProjectedLesson.excluded.
    """
    return [c for c in claims if check_claim_use(c, use)[0]]
