"""qualify_lesson() — proposed promotion gate contract (SPEC, not production code).

Governing principle: intelligence may learn from itself, but it may not
independently verify itself merely by referring back to itself.

This module is a STANDALONE specification of the gate that should sit
between evidence accumulation (strengthen) and behavioral influence
(serve/apply_retained_intelligence). It is intentionally NOT wired into
kernel/ — it is the contract + the tests that prove the contract. Wiring
it into the kernel is a separate authorized change (needs Shawn's word
per the protected-gate rules, and must not duplicate PR #2075/#2079).

Verdict codes (fail-closed: anything unrecognized -> BLOCKED_*):
    ELIGIBLE_FOR_GOVERNED_PROMOTION
    BLOCKED_INTEGRITY
    BLOCKED_CIRCULAR_PROOF
    INSUFFICIENT_INDEPENDENT_EVIDENCE
    CONFLICTED
    INSUFFICIENT_EVALUATION
    BLOCKED_SELF_CERTIFICATION
    BLOCKED_AUTHORITY
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data shapes (minimal; the real kernel types are richer)
# ---------------------------------------------------------------------------

@dataclass
class EvidenceItem:
    """One piece of evidence offered for a lesson."""
    evidence_id: str
    content_hash: str          # sha256 of the evidence content
    origin: str                # who/what produced it (identity-normalized)
    source_record_id: str | None = None   # the record this evidence derives from, if any
    evidence_family: str | None = None    # groups items sharing one ultimate source


@dataclass
class LessonCandidate:
    lesson_id: str
    content: str
    content_hash: str          # sha256 of content; must match recomputation
    lineage: list[str] = field(default_factory=list)  # record_ids this lesson derives from
    evidence: list[EvidenceItem] = field(default_factory=list)
    doer: str = ""
    scorer: str = ""
    verifier: str = ""


@dataclass
class Evaluation:
    uses_held_out_cases: bool
    held_out_case_ids: list[str] = field(default_factory=list)
    formation_case_ids: list[str] = field(default_factory=list)
    verifier_had_answer_key: bool = False


@dataclass
class AuthorityScope:
    authorized_actions: list[str] = field(default_factory=list)
    # the action this lesson would authorize, if promoted


# ---------------------------------------------------------------------------
# Predicates — each has an explicit, testable definition
# ---------------------------------------------------------------------------

def normalize_identity(value: str) -> str:
    """Same contract as tools/learning_admission_gate.normalize_identity."""
    return "".join(str(value or "").strip().lower().split())


def verify_identity_and_hashes(lesson: LessonCandidate) -> bool:
    """True iff lesson_id is non-empty AND content_hash == sha256(content).

    Testable: flip one byte of content -> False. Empty id -> False.
    """
    if not str(lesson.lesson_id or "").strip():
        return False
    recomputed = hashlib.sha256(lesson.content.encode()).hexdigest()
    return bool(lesson.content_hash) and lesson.content_hash == recomputed


def has_dependency_cycle(lesson: LessonCandidate) -> bool:
    """True iff the lesson's evidence lineage loops back to itself.

    A cycle exists when any evidence item's source_record_id is the lesson
    itself, or when any evidence item's source is a descendant of the lesson
    (present in the lesson's lineage closure in reverse). For this spec,
    we check: evidence.source_record_id == lesson.lesson_id (direct
    self-citation), or evidence.source_record_id in lesson.lineage AND the
    lesson is in that source's lineage (mutual descent — passed as
    descendant_map for testability).

    Testable: evidence citing lesson_id -> True. Evidence citing an
    unrelated record -> False.
    """
    for ev in lesson.evidence:
        if ev.source_record_id and normalize_identity(ev.source_record_id) == normalize_identity(lesson.lesson_id):
            return True
    return False


def has_dependency_cycle_deep(lesson: LessonCandidate,
                              descendant_map: dict[str, list[str]]) -> bool:
    """Deep version: True iff any evidence derives from a record that
    descends from the lesson (transitive self-proof through children).

    descendant_map: record_id -> list of record_ids that derive from it.
    Testable: build A->B->C chain where C is evidence for A -> True.
    """
    if has_dependency_cycle(lesson):
        return True
    # transitive closure of the lesson's descendants
    seen: set[str] = set()
    frontier = list(descendant_map.get(lesson.lesson_id, []))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(descendant_map.get(node, []))
    for ev in lesson.evidence:
        if ev.source_record_id and ev.source_record_id in seen:
            return True
    return False


def has_independent_support(lesson: LessonCandidate,
                            family_roots: dict[str, str] | None = None) -> bool:
    """True iff at least one evidence FAMILY traces to an independent root.

    An evidence family is independent iff its ultimate source (family_roots
    map, or the item's own origin when unmapped) is a non-empty identity
    distinct from the lesson's doer and distinct from the lesson itself.
    Five agents in one family = one source; if that source is the doer
    (or unattributed), it is an echo chamber, not independent support.

    Testable: 5 items, 1 family rooted at doer -> False. 2 families with
    distinct independent roots -> True.
    """
    family_roots = family_roots or {}
    independent_families: set[str] = set()
    for ev in lesson.evidence:
        if not ev.origin or not ev.origin.strip():
            continue
        if ev.source_record_id and normalize_identity(ev.source_record_id) == normalize_identity(lesson.lesson_id):
            continue  # self-citation is never independent support
        fam = ev.evidence_family or f"solo:{ev.evidence_id}"
        root = family_roots.get(fam, ev.origin)
        if not root or not root.strip():
            continue
        rn, dn = normalize_identity(root), normalize_identity(lesson.doer)
        if rn and rn != dn and rn != normalize_identity(lesson.lesson_id):
            independent_families.add(fam)
    return len(independent_families) >= 1


def has_unresolved_material_contradiction(lesson: LessonCandidate,
                                          active_lessons: list[dict[str, Any]]) -> bool:
    """True iff an ACTIVE lesson materially contradicts this one and the
    contradiction has no resolution record.

    Material contradiction (testable definition): another active lesson
    whose `contradicts` list names this lesson's id, or whose content_hash
    differs while claiming the same `situation` with an incompatible
    prescribed behavior. Resolution = a supersede/reconcile receipt naming
    both ids.

    Testable: active lesson B with contradicts=[A.id], no resolution -> True.
    Same, with resolution receipt -> False.
    """
    for other in active_lessons:
        if other.get("lesson_id") == lesson.lesson_id:
            continue
        contradicts = other.get("contradicts", []) or []
        if lesson.lesson_id in contradicts and not other.get("resolution_receipt"):
            return True
    return False


def uses_held_out_cases(evaluation: Evaluation) -> bool:
    """True iff evaluation ran on cases disjoint from formation cases AND
    the verifier did not have the answer key beforehand.

    Testable: overlap -> False. verifier_had_answer_key -> False.
    Disjoint + blind -> True.
    """
    if evaluation.verifier_had_answer_key:
        return False
    if not evaluation.held_out_case_ids:
        return False
    overlap = set(evaluation.held_out_case_ids) & set(evaluation.formation_case_ids)
    return not overlap


def verifier_is_independent(lesson: LessonCandidate) -> bool:
    """True iff doer, scorer, verifier are three distinct normalized identities.

    Reuses the admission gate's contract (B6b). Testable: any collision
    (case/whitespace-insensitive) -> False.
    """
    d, s, v = (normalize_identity(x) for x in (lesson.doer, lesson.scorer, lesson.verifier))
    if not d or not s or not v:
        return False
    return len({d, s, v}) == 3


def authority_gate_passed(lesson: LessonCandidate, scope: AuthorityScope,
                          proposed_action: str) -> bool:
    """True iff the action the lesson would authorize is in the scope.

    Testable: action not in authorized_actions -> False.
    """
    return proposed_action in (scope.authorized_actions or [])


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def qualify_lesson(lesson: LessonCandidate, evaluation: Evaluation,
                   scope: AuthorityScope, proposed_action: str,
                   active_lessons: list[dict[str, Any]] | None = None,
                   descendant_map: dict[str, list[str]] | None = None,
                   family_roots: dict[str, str] | None = None) -> str:
    """Run the predicates in fail-closed order. First failure wins."""
    if not verify_identity_and_hashes(lesson):
        return "BLOCKED_INTEGRITY"
    if has_dependency_cycle_deep(lesson, descendant_map or {}):
        return "BLOCKED_CIRCULAR_PROOF"
    if not has_independent_support(lesson, family_roots):
        return "INSUFFICIENT_INDEPENDENT_EVIDENCE"
    if has_unresolved_material_contradiction(lesson, active_lessons or []):
        return "CONFLICTED"
    if not uses_held_out_cases(evaluation):
        return "INSUFFICIENT_EVALUATION"
    if not verifier_is_independent(lesson):
        return "BLOCKED_SELF_CERTIFICATION"
    if not authority_gate_passed(lesson, scope, proposed_action):
        return "BLOCKED_AUTHORITY"
    return "ELIGIBLE_FOR_GOVERNED_PROMOTION"
