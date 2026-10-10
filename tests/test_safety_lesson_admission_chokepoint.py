"""SAFETY falsifiers: the lesson-integration admission gate must be a choke point.

Module under test: kernel/self_integration.py :: integrate_verified_lesson.

The seam's own contract (module + function docstrings): "Gates (all must
hold; anything failing raises IntegrationError and the store is untouched)"
and "anything failing is refused, never integrated". Gate 4 names the
admission gate "the admission gate's choke point".

A choke point that can be skipped by omitting the admission field is not a
choke point. These tests pin: a lesson carrying NO admission record — one
that never passed the admission gate at all — must be refused, exactly like
a REJECTED one. (Pre-fix, it integrated: the fail-open.)
"""
import pytest

from kernel.behavior_policy import BehaviorPolicyStore
from kernel.self_integration import IntegrationError, integrate_verified_lesson

SITUATION = "dispatch:duplicate-learning-write"


def _lesson(**kw):
    base = {
        "lesson_id": "SN-0601",
        "claim": "Unverified candidates must never enter the learning system",
        "situation": SITUATION,
        "prescribed_behavior": "run the admission gate before writing any candidate row",
        "doer": "naya-5",
        "scorer": "naya-1",
        "verifier": "naya-2",
        "verdict": "VERIFIED",
        "admission_admitted_as": "CANDIDATE",
    }
    base.update(kw)
    return base


def _store_untouched(store):
    assert store.current_version == 0
    assert store.advise(SITUATION, "default-behavior")["source"] == "default"


def test_missing_admission_record_is_refused(tmp_path):
    """No admission record at all = never passed the choke point = refused."""
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    lesson = _lesson()
    del lesson["admission_admitted_as"]
    with pytest.raises(IntegrationError, match="lesson_not_admitted"):
        integrate_verified_lesson(lesson, store)
    _store_untouched(store)


def test_empty_admission_record_is_refused(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="lesson_not_admitted"):
        integrate_verified_lesson(_lesson(admission_admitted_as=""), store)
    _store_untouched(store)


def test_whitespace_admission_record_is_refused(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="lesson_not_admitted"):
        integrate_verified_lesson(_lesson(admission_admitted_as="   "), store)
    _store_untouched(store)


def test_rejected_admission_record_is_refused(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="lesson_not_admitted"):
        integrate_verified_lesson(_lesson(admission_admitted_as="REJECTED"), store)
    _store_untouched(store)


def test_candidate_admission_still_integrates(tmp_path):
    """Backward compatibility: the legit path is untouched by the fix."""
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    receipt = integrate_verified_lesson(_lesson(), store)
    assert receipt["status"] == "INTEGRATED"
    assert store.current_version == 1
