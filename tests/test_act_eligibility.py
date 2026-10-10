"""Tests for Phase 2 ACT-wire eligibility — kernel/act_pipeline.

Proves the authorized-apply seam re-checks eligibility AT THE MOMENT OF USE
(Freshness Law): revoked, suspended, and uncertain records never certify
behavior through the ACT wire, fail closed — however they reached the served
set. The store's own filtering is never trusted alone.

Verdict codes live in kernel.memory_metabolism (act_eligibility).
"""

import pytest

from kernel import memory_metabolism as mm
from kernel.act_pipeline import apply_retained_intelligence
from kernel.behavior_policy import BehaviorPolicyStore
from kernel.memory_store import MemoryStore

NOW = "2026-10-10T10:30:00+00:00"
SITUATION = "synth-eligibility-situation"


def _rec(provenance_extra=None, memory_state=None, at=NOW):
    provenance = {"situation": SITUATION, "test": True}
    provenance.update(provenance_extra or {})
    r = mm.create_record(
        "the sky is plaid",
        epistemic_state="VERIFIED_FACT",
        provenance=provenance,
        now=at,
    )
    if memory_state is not None:
        r.memory_state = memory_state
        r.integrity = mm.record_integrity(r)
    return r


def _store(tmp_path, records):
    store = MemoryStore(tmp_path / "memstore")
    for r in records:
        store.save(r, now=NOW)
    return store


def _decide(store, **kwargs):
    kwargs.setdefault("situation", SITUATION)
    kwargs.setdefault("default_behavior", "shrug (default)")
    kwargs.setdefault("now", NOW)
    return apply_retained_intelligence(memory_store=store, **kwargs)


class _SmugglingStore:
    """serve() returns records the real store would filter — proving the
    wire re-checks eligibility at use time instead of trusting serve()."""

    def __init__(self, records):
        self._records = records

    def serve(self, predicate=None, **kwargs):
        items = [
            (r, "smuggled")
            for r in self._records
            if predicate is None or predicate(r)
        ]
        return mm.RetrievalResult(items=items, dropped_integrity_failed=[])


# Revocation verdicts ---------------------------------------------------------

def test_revoked_record_never_certifies(tmp_path):
    store = _store(tmp_path, [
        _rec({"revocation_verdict": "REVOKED"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1
    assert out["memory_records_considered"] == 0


def test_suspended_record_never_certifies(tmp_path):
    store = _store(tmp_path, [
        _rec({"revocation_verdict": "SUSPENDED"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


def test_insufficient_data_revocation_fails_closed(tmp_path):
    # INSUFFICIENT_DATA cannot establish standing: refused, not served.
    store = _store(tmp_path, [
        _rec({"revocation_verdict": "INSUFFICIENT_DATA"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


def test_unrecognized_revocation_verdict_fails_closed(tmp_path):
    store = _store(tmp_path, [
        _rec({"revocation_verdict": "TOTALLY_MADE_UP"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


# Uncertainty assessments -----------------------------------------------------

def test_possibly_compromised_never_certifies(tmp_path):
    store = _store(tmp_path, [
        _rec({"uncertainty_assessment": "possibly_compromised",
              "incident_id": "INC-001"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


def test_confirmed_compromised_never_certifies(tmp_path):
    store = _store(tmp_path, [
        _rec({"uncertainty_assessment": "confirmed_compromised",
              "incident_id": "INC-001"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


def test_unassessed_with_live_incident_refused(tmp_path):
    # Known incident, family never assessed: unknown independence is not
    # proven independence.
    store = _store(tmp_path, [
        _rec({"uncertainty_assessment": "unassessed",
              "incident_id": "INC-001"}),
    ])
    out = _decide(store)
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1


def test_unassessed_without_incident_stays_eligible(tmp_path):
    # No incident on record: the assessment states classify families WITHIN
    # a known incident; absent markers are not an incident.
    store = _store(tmp_path, [
        _rec({"uncertainty_assessment": "unassessed"}),
    ])
    out = _decide(store)
    assert out["via"] == "memory_store"
    assert out["memory_records_refused"] == 0


def test_independently_cleared_stays_eligible(tmp_path):
    store = _store(tmp_path, [
        _rec({"uncertainty_assessment": "independently_cleared",
              "incident_id": "INC-001"}),
    ])
    out = _decide(store)
    assert out["via"] == "memory_store"
    assert out["memory_records_refused"] == 0


def test_downgraded_retains_positive_standing(tmp_path):
    store = _store(tmp_path, [
        _rec({"revocation_verdict": "DOWNGRADED"}),
    ])
    out = _decide(store)
    assert out["via"] == "memory_store"
    assert out["memory_records_refused"] == 0


def test_no_markers_eligible(tmp_path):
    store = _store(tmp_path, [_rec()])
    out = _decide(store)
    assert out["via"] == "memory_store"
    assert out["memory_eligibility"] == mm.ELIGIBLE
    assert out["memory_records_refused"] == 0


# Use-time recheck: never trust the served set --------------------------------

def test_wire_rechecks_non_active_even_when_served():
    # A QUARANTINED record smuggled past the store's filter is still
    # refused by the wire's own use-time check.
    smuggled = _rec(memory_state=mm.QUARANTINED)
    out = _decide(_SmugglingStore([smuggled]))
    assert out["via"] == "default"
    assert out["memory_records_refused"] == 1
    assert out["memory_records_considered"] == 0


def test_revoked_high_weight_does_not_outrank_eligible(tmp_path):
    revoked = _rec({"revocation_verdict": "REVOKED"},
                   at="2026-10-10T10:30:00+00:00")
    revoked.verification_weight = 99.0
    revoked.integrity = mm.record_integrity(revoked)
    eligible = _rec(at="2026-10-10T10:31:00+00:00")
    eligible.verification_weight = 1.0
    eligible.integrity = mm.record_integrity(eligible)
    assert revoked.record_id != eligible.record_id
    store = _store(tmp_path, [revoked, eligible])
    out = _decide(store)
    assert out["via"] == "memory_store"
    assert out["memory_record_id"] == eligible.record_id
    assert out["memory_records_refused"] == 1
    assert out["memory_records_considered"] == 1


# Policy-path eligibility hook --------------------------------------------------

def _policy_with_lesson(tmp_path, lesson_id="LESSON-1"):
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    policy.integrate(
        situation=SITUATION,
        behavior="answer 'plaid'",
        lesson_id=lesson_id,
    )
    return policy


def test_policy_lesson_refused_by_eligibility_hook_falls_through(tmp_path):
    policy = _policy_with_lesson(tmp_path)
    store = _store(tmp_path, [_rec()])
    out = _decide(
        store,
        policy_store=policy,
        lesson_eligibility=lambda lid: mm.INELIGIBLE_REVOKED,
    )
    assert out["via"] == "memory_store"
    assert out["policy_refused"] == mm.INELIGIBLE_REVOKED


def test_policy_lesson_refused_with_no_memory_falls_to_default(tmp_path):
    policy = _policy_with_lesson(tmp_path)
    store = _store(tmp_path, [])
    out = _decide(
        store,
        policy_store=policy,
        lesson_eligibility=lambda lid: mm.INELIGIBLE_SUSPENDED,
    )
    assert out["via"] == "default"
    assert out["policy_refused"] == mm.INELIGIBLE_SUSPENDED


def test_policy_lesson_eligible_hook_serves_policy(tmp_path):
    policy = _policy_with_lesson(tmp_path)
    store = _store(tmp_path, [_rec()])
    out = _decide(
        store,
        policy_store=policy,
        lesson_eligibility=lambda lid: mm.ELIGIBLE,
    )
    assert out["via"] == "behavior_policy"
    assert out["source"] == "lesson:LESSON-1"


def test_policy_path_without_hook_unchanged(tmp_path):
    # Backward compatible: no hook, policy lesson served as before.
    policy = _policy_with_lesson(tmp_path)
    store = _store(tmp_path, [_rec()])
    out = _decide(store, policy_store=policy)
    assert out["via"] == "behavior_policy"
    assert out["policy_refused"] is None
