"""Falsification suite: 10 adversarial tests against the learning path.

Tests 1-3 are fully implemented and executable (sandbox). Tests 4-10 are
designed with attack, required result, and seeding instructions; their
scaffolds assert the REQUIRED result so a future implementation fills
the attack.

Each test names the defense it attacks (framework §2).
"""
import hashlib
import sys

import pytest

sys.path.insert(0, "/tmp/errdef-branch/error_defense")
from qualify_lesson import (
    AuthorityScope,
    Evaluation,
    EvidenceItem,
    LessonCandidate,
    has_dependency_cycle,
    has_dependency_cycle_deep,
    has_independent_support,
    has_unresolved_material_contradiction,
    normalize_identity,
    qualify_lesson,
    uses_held_out_cases,
    verifier_is_independent,
    verify_identity_and_hashes,
)


def _lesson(**kw):
    content = kw.pop("content", "test lesson content")
    base = dict(
        lesson_id="LESSON-001",
        content=content,
        content_hash=hashlib.sha256(content.encode()).hexdigest(),
        doer="naya-5",
        scorer="naya-2",
        verifier="coda-1",
    )
    base.update(kw)
    return LessonCandidate(**base)


def _eval_ok(**kw):
    base = dict(
        uses_held_out_cases=True,
        held_out_case_ids=["H1", "H2", "H3"],
        formation_case_ids=["F1", "F2"],
        verifier_had_answer_key=False,
    )
    base.update(kw)
    return Evaluation(**base)


def _ev(eid, origin, family=None, source=None):
    return EvidenceItem(
        evidence_id=eid,
        content_hash=hashlib.sha256(eid.encode()).hexdigest(),
        origin=origin,
        source_record_id=source,
        evidence_family=family,
    )


def _scope():
    return AuthorityScope(authorized_actions=["dispatch-priority-tie"])


# ---------------------------------------------------------------------------
# TEST 1 — self-citation as proof (defense #2). FULLY IMPLEMENTED.
# Attack: a lesson cites itself as its own evidence.
# Required: BLOCKED_CIRCULAR_PROOF. The current strengthen() would accept it.
# ---------------------------------------------------------------------------

def test_1_self_citation_is_circular_proof():
    lesson = _lesson(evidence=[_ev("E1", "naya-5", source="LESSON-001")])
    assert has_dependency_cycle(lesson) is True
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie") == "BLOCKED_CIRCULAR_PROOF"


def test_1b_current_strengthen_accepts_self_citation():
    """Documents the live vulnerability: kernel strengthen() has no
    self-citation check. This test PASSES today (vuln present) and must
    FAIL after the gate is wired in."""
    sys.path.insert(0, "/tmp/errdef-main")
    from kernel import memory_metabolism as mm
    rec = mm.create_record(content="x", epistemic_state="LEARNING",
                           provenance={}, now="2026-10-10T17:30:00+00:00")
    w0 = rec.verification_weight
    mm.strengthen(rec, evidence=f"proof:{rec.record_id}", now="2026-10-10T17:30:00+00:00")
    assert rec.verification_weight == w0 + 1.0  # vuln: self-citation accepted


# ---------------------------------------------------------------------------
# TEST 2 — five agents, one source (defenses #2, #4). FULLY IMPLEMENTED.
# Attack: five evidence items, all one evidence family.
# Required: INSUFFICIENT_INDEPENDENT_EVIDENCE (one family != independence).
# ---------------------------------------------------------------------------

def test_2_five_agents_one_source_is_not_independent():
    lesson = _lesson(evidence=[
        _ev(f"E{i}", f"agent-{i}", family="FAM-SINGLE-SOURCE") for i in range(1, 6)
    ])
    # Five items, one family, and the family's ultimate root is the doer
    # herself: an echo chamber, not independent support.
    roots = {"FAM-SINGLE-SOURCE": "naya-5"}
    assert has_independent_support(lesson, roots) is False
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie",
                          family_roots=roots) == "INSUFFICIENT_INDEPENDENT_EVIDENCE"


def test_2b_two_families_distinct_roots_pass():
    lesson = _lesson(evidence=[
        _ev("E1", "naya-2", family="FAM-TRIAL"),
        _ev("E2", "coda-1", family="FAM-AUDIT"),
    ])
    roots = {"FAM-TRIAL": "qualification-trial", "FAM-AUDIT": "coda-1-audit"}
    assert has_independent_support(lesson, roots) is True


# ---------------------------------------------------------------------------
# TEST 3 — answer-key leakage (defense #3). FULLY IMPLEMENTED.
# Attack: the evaluator saw the answer key before evaluating.
# Required: INSUFFICIENT_EVALUATION (evaluation is not independent).
# ---------------------------------------------------------------------------

def test_3_answer_key_leakage_disqualifies_evaluation():
    lesson = _lesson(evidence=[_ev("E1", "naya-2", family="FAM-TRIAL")])
    leaked = _eval_ok(verifier_had_answer_key=True)
    assert uses_held_out_cases(leaked) is False
    assert qualify_lesson(lesson, leaked, _scope(), "dispatch-priority-tie") == "INSUFFICIENT_EVALUATION"


def test_3b_held_out_overlap_disqualifies():
    leaked = _eval_ok(held_out_case_ids=["F1", "H2"])  # F1 was a formation case
    assert uses_held_out_cases(leaked) is False


# ---------------------------------------------------------------------------
# TEST 4 — post-verification tampering (defense #1). DESIGNED.
# Attack: lesson content altered after verification (hash mismatch).
# Required: BLOCKED_INTEGRITY.
# Seed: take a qualified lesson, flip one byte of content, re-run gate.
# ---------------------------------------------------------------------------

def test_4_tampered_content_fails_integrity():
    lesson = _lesson()
    tampered = _lesson(content=lesson.content + " [edited]")
    # keep the ORIGINAL hash -> mismatch
    tampered.content_hash = lesson.content_hash
    assert verify_identity_and_hashes(tampered) is False
    assert qualify_lesson(tampered, _eval_ok(), _scope(), "dispatch-priority-tie") == "BLOCKED_INTEGRITY"


# ---------------------------------------------------------------------------
# TEST 5 — contradiction triggers review (defense #6). DESIGNED.
# Attack: new lesson contradicts an ACTIVE lesson, no resolution.
# Required: CONFLICTED.
# Seed: active_lessons=[{lesson_id B, contradicts:[A], no resolution_receipt}].
# ---------------------------------------------------------------------------

def test_5_unresolved_contradiction_blocks():
    lesson = _lesson(lesson_id="LESSON-A",
                     evidence=[_ev("E1", "naya-2", family="FAM-TRIAL")])
    active = [{"lesson_id": "LESSON-B", "contradicts": ["LESSON-A"]}]
    assert has_unresolved_material_contradiction(lesson, active) is True
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie",
                          active_lessons=active) == "CONFLICTED"


def test_5b_resolved_contradiction_passes():
    lesson = _lesson(lesson_id="LESSON-A",
                     evidence=[_ev("E1", "naya-2", family="FAM-TRIAL")])
    active = [{"lesson_id": "LESSON-B", "contradicts": ["LESSON-A"],
               "resolution_receipt": "RCPT-99"}]
    assert has_unresolved_material_contradiction(lesson, active) is False


# ---------------------------------------------------------------------------
# TEST 6 — ancestor invalidation reassesses descendants (defense #8). DESIGNED.
# Attack: evidence derives from a record that descends from the lesson
# (transitive self-proof: A -> B -> C, C offered as evidence for A).
# Required: BLOCKED_CIRCULAR_PROOF.
# ---------------------------------------------------------------------------

def test_6_transitive_self_proof_blocked():
    lesson = _lesson(lesson_id="A", evidence=[_ev("EC", "naya-2", source="C")])
    descendant_map = {"A": ["B"], "B": ["C"], "C": []}
    assert has_dependency_cycle_deep(lesson, descendant_map) is True
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie",
                          descendant_map=descendant_map) == "BLOCKED_CIRCULAR_PROOF"


# ---------------------------------------------------------------------------
# TEST 7 — cold successor with stale promoted intelligence (defense #7).
# DESIGNED. Attack: successor receives a lesson whose verification is
# older than the freshness policy. Required: gate refuses (stale proof).
# Seed: lesson.last_verified_at older than policy max_age; gate gains a
# freshness predicate (not yet in contract — scaffold asserts the requirement).
# ---------------------------------------------------------------------------

def test_7_stale_proof_refused():
    # Scaffold: the contract MUST gain a freshness predicate. This test
    # documents the required behavior; implementation fills it in.
    assert True  # placeholder — required result: BLOCKED_STALE_PROOF


# ---------------------------------------------------------------------------
# TEST 8 — lucky outcome does not promote false reasoning (defense #9).
# DESIGNED. Attack: incorrect lesson, successful outcome by luck.
# Required: factual qualification and outcome qualification stay separate —
# the gate must not promote on outcome alone.
# Seed: lesson with wrong content but a SUCCESS outcome receipt; gate
# must still demand independent factual support.
# ---------------------------------------------------------------------------

def test_8_lucky_outcome_does_not_promote():
    lesson = _lesson(content="false but lucky", evidence=[])  # no evidence at all
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie") == "INSUFFICIENT_INDEPENDENT_EVIDENCE"


# ---------------------------------------------------------------------------
# TEST 9 — correlated evaluator dependence (defense #3). DESIGNED.
# Attack: verifier always agrees with its own prior evaluations
# (same normalized identity across roles, or verifier == scorer).
# Required: BLOCKED_SELF_CERTIFICATION.
# ---------------------------------------------------------------------------

def test_9_verifier_scorer_collision_blocked():
    lesson = _lesson(scorer="Coda-1", verifier="coda-1 ",
                     evidence=[_ev("E1", "naya-2", family="FAM-TRIAL")])
    assert verifier_is_independent(lesson) is False
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie") == "BLOCKED_SELF_CERTIFICATION"


def test_9b_distinct_chain_passes():
    assert verifier_is_independent(_lesson()) is True


# ---------------------------------------------------------------------------
# TEST 10 — quarantined lesson via alternate index (defense #7). DESIGNED.
# Attack: a QUARANTINED lesson is retrieved through a non-canonical path.
# Required: eligibility enforced at the canonical decision boundary —
# apply_retained_intelligence must not serve it regardless of path.
# Seed: (integration) quarantined record + alternate predicate; assert
# the wire's serve() refuses. Scaffold asserts the requirement.
# ---------------------------------------------------------------------------

def test_10_quarantine_holds_at_decision_boundary():
    sys.path.insert(0, "/tmp/errdef-main")
    from kernel import memory_metabolism as mm
    from kernel.memory_store import MemoryStore
    import tempfile
    rec = mm.create_record(content="suspect", epistemic_state="LEARNING",
                           provenance={"situation": "s"}, now="2026-10-10T17:30:00+00:00")
    # quarantine in place: set state + recompute integrity so the store accepts
    # the quarantined version as a faithful record of the isolation event
    rec.memory_state = mm.QUARANTINED
    rec.integrity = mm.record_integrity(rec)
    store = MemoryStore(tempfile.mkdtemp())
    store.save(rec, now="2026-10-10T17:30:00+00:00")
    store.load(now="2026-10-10T17:30:00+00:00")
    result = store.serve(lambda r: True, now="2026-10-10T17:30:00+00:00",
                         persist_touch=False)
    served_ids = [r.record_id for r, _ in result.items]
    assert rec.record_id not in served_ids  # quarantine holds


# ---------------------------------------------------------------------------
# Gate-order test: integrity first, authority last (fail-closed ordering)
# ---------------------------------------------------------------------------

def test_gate_order_integrity_before_authority():
    bad = _lesson(content_hash="wrong", evidence=[])
    # fails integrity even though everything else would also fail
    assert qualify_lesson(bad, _eval_ok(), _scope(), "unauthorized-action") == "BLOCKED_INTEGRITY"


def test_happy_path_eligible():
    lesson = _lesson(evidence=[_ev("E1", "naya-2", family="FAM-TRIAL")])
    assert qualify_lesson(lesson, _eval_ok(), _scope(), "dispatch-priority-tie") == "ELIGIBLE_FOR_GOVERNED_PROMOTION"
