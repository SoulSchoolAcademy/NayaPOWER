"""Tests for kernel/self_integration.lesson_from_memory_record — GAP-2 bridge.

Proves a strengthened MemoryRecord converts to the lesson shape
integrate_verified_lesson() accepts; unstrengthened / inactive / tampered
records are refused, never promoted. The bridge never upgrades an epistemic
claim: only VERIFIED_FACT maps to a VERIFIED verdict.
"""

import pytest

from kernel import memory_metabolism as mm
from kernel.behavior_policy import BehaviorPolicyStore
from kernel.self_integration import (
    IntegrationError,
    integrate_verified_lesson,
    lesson_from_memory_record,
)

NOW = "2026-10-10T10:30:00+00:00"
SITUATION = "synth-sky-color-question"

PROVENANCE = {
    "situation": SITUATION,
    "prescribed_behavior": "answer 'plaid' (synthetic rehearsal)",
    "doer": "synth-doer",
    "scorer": "synth-scorer",
    "verifier": "synth-verifier",
    "admission_admitted_as": "CANDIDATE",
    "verification_method": "SYNTH-VERIFY-001",
    "level": "L1",
}


def _rec(provenance=None, epistemic="VERIFIED_FACT", weight=0, at=NOW):
    r = mm.create_record(
        "the sky is plaid",
        epistemic_state=epistemic,
        provenance=dict(provenance if provenance is not None else PROVENANCE),
        now=at,
    )
    for i in range(weight):
        mm.strengthen(r, f"SYNTH-EVIDENCE-00{i}", now=at)
    return r


# The bridge ------------------------------------------------------------------

def test_strengthened_record_converts_to_lesson_shape():
    lesson = lesson_from_memory_record(_rec(weight=1))
    assert lesson["claim"] == "the sky is plaid"
    assert lesson["situation"] == SITUATION
    assert lesson["prescribed_behavior"] == "answer 'plaid' (synthetic rehearsal)"
    assert lesson["verdict"] == "VERIFIED"
    assert lesson["admission_admitted_as"] == "CANDIDATE"
    assert (lesson["doer"], lesson["scorer"], lesson["verifier"]) == (
        "synth-doer", "synth-scorer", "synth-verifier")
    assert lesson["lesson_id"].startswith("MEM-")


def test_full_promotion_path_record_to_policy(tmp_path):
    """End-to-end GAP-2: record → strengthen → bridge → integrate → advise."""
    record = _rec(weight=2)
    lesson = lesson_from_memory_record(record)
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    receipt = integrate_verified_lesson(lesson, policy)
    assert receipt["status"] == "INTEGRATED"
    assert policy.current_version == 1
    advised = policy.advise(SITUATION, default_behavior="shrug")
    assert advised["source"] == f"lesson:{record.record_id}"
    assert advised["behavior"] == "answer 'plaid' (synthetic rehearsal)"


def test_unstrengthened_record_refused():
    with pytest.raises(IntegrationError,
                       match="memory_record_unstrengthened"):
        lesson_from_memory_record(_rec(weight=0))


def test_weight_without_evidence_refused():
    r = _rec(weight=0)
    r.verification_weight = 1.0  # forged without evidence; integrity re-sealed
    r.integrity = mm.record_integrity(r)
    with pytest.raises(IntegrationError,
                       match="memory_record_unstrengthened"):
        lesson_from_memory_record(r)


def test_superseded_record_refused():
    old = _rec(weight=1, at="2026-10-10T10:30:00+00:00")
    new = _rec(weight=1, at="2026-10-10T10:31:00+00:00")
    mm.supersede(old, new, now=NOW)
    with pytest.raises(IntegrationError,
                       match="memory_record_not_active:state=SUPERSEDED"):
        lesson_from_memory_record(old)
    # The winner is still promotable.
    assert lesson_from_memory_record(new)["verdict"] == "VERIFIED"


def test_decayed_record_refused():
    r = _rec(weight=1)
    mm.metabolize([r], now="2027-10-10T10:30:00+00:00", stale_after_days=90.0)
    assert r.memory_state == mm.DECAYED
    with pytest.raises(IntegrationError,
                       match="memory_record_not_active:state=DECAYED"):
        lesson_from_memory_record(r)


def test_tampered_record_refused():
    r = _rec(weight=1)
    r.content = "the sky is green (tampered)"
    with pytest.raises(IntegrationError,
                       match="memory_record_integrity_failed"):
        lesson_from_memory_record(r)


def test_non_record_refused():
    with pytest.raises(IntegrationError,
                       match="memory_record_not_a_record"):
        lesson_from_memory_record({"record_id": "fake"})


def test_non_verified_epistemic_not_upgraded(tmp_path):
    """A strengthened HYPOTHESIS converts but keeps its epistemic state —
    the bridge never upgrades a claim; the integration gate refuses it."""
    lesson = lesson_from_memory_record(_rec(epistemic="HYPOTHESIS", weight=1))
    assert lesson["verdict"] == "HYPOTHESIS"
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="lesson_not_verified"):
        integrate_verified_lesson(lesson, policy)
    assert policy.current_version == 0  # nothing integrated


def test_missing_situation_refused_at_integration_gate(tmp_path):
    """The bridge maps honestly (empty situation); the integration gate —
    not the bridge — refuses the incomplete lesson."""
    prov = dict(PROVENANCE)
    del prov["situation"]
    lesson = lesson_from_memory_record(_rec(provenance=prov, weight=1))
    assert lesson["situation"] == ""
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="lesson_incomplete"):
        integrate_verified_lesson(lesson, policy)


def test_broken_verifier_chain_refused_at_integration_gate(tmp_path):
    prov = dict(PROVENANCE)
    prov["verifier"] = "synth-doer"  # verifier == doer: chain broken
    lesson = lesson_from_memory_record(_rec(provenance=prov, weight=1))
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="verifier_chain_broken"):
        integrate_verified_lesson(lesson, policy)
