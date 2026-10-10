"""Tests for kernel/act_pipeline.apply_retained_intelligence — GAP-1 wire.

Proves retrieval actually reaches the action decision: ACTIVE records served
from the MemoryStore bind to the authorized-apply seam; integrated policy
lessons outrank retained memory; QUARANTINED records never reach action
(adversarial); retrieval is read-only.
"""

import pytest

from kernel import memory_metabolism as mm
from kernel.act_pipeline import apply_retained_intelligence
from kernel.behavior_policy import BehaviorPolicyStore
from kernel.memory_store import MemoryStore

NOW = "2026-10-10T10:30:00+00:00"
SITUATION = "synth-sky-color-question"
OTHER_SITUATION = "synth-unrelated-situation"


def _rec(content="the sky is plaid", situation=SITUATION,
         epistemic="VERIFIED_FACT", weight=0, at=NOW):
    r = mm.create_record(
        content,
        epistemic_state=epistemic,
        provenance={"situation": situation, "test": True},
        now=at,
    )
    for i in range(weight):
        mm.strengthen(r, f"evidence-{i}", now=at)
    return r


def _store(tmp_path, records):
    store = MemoryStore(tmp_path / "memstore")
    for r in records:
        store.save(r, now=NOW)
    return store


def _decide(store, situation=SITUATION, policy_store=None,
            default="shrug (default)"):
    return apply_retained_intelligence(
        memory_store=store,
        policy_store=policy_store,
        situation=situation,
        default_behavior=default,
        now=NOW,
    )


# The wire --------------------------------------------------------------------

def test_memory_record_reaches_action_decision(tmp_path):
    store = _store(tmp_path, [_rec(weight=1)])
    out = _decide(store)
    assert out["source"].startswith("memory:")
    assert out["behavior"] == "the sky is plaid"
    assert out["situation"] == SITUATION
    assert out["via"] == "memory_store"
    assert out["memory_verification_weight"] == 1.0
    assert out["memory_records_considered"] == 1


def test_policy_lesson_outranks_retained_memory(tmp_path):
    store = _store(tmp_path, [_rec("the sky is plaid", weight=2)])
    policy = BehaviorPolicyStore(tmp_path / "policy.json")
    policy.integrate(situation=SITUATION, behavior="answer 'plaid'",
                     lesson_id="LESSON-1")
    out = _decide(store, policy_store=policy)
    assert out["source"] == "lesson:LESSON-1"
    assert out["behavior"] == "answer 'plaid'"
    assert out["via"] == "behavior_policy"
    assert out["memory_record_id"] is None
    # The memory record was still considered (transparency), not hidden.
    assert out["memory_records_considered"] == 1


def test_default_when_nothing_retained(tmp_path):
    store = _store(tmp_path, [])
    out = _decide(store, default="shrug (default)")
    assert out["source"] == "default"
    assert out["behavior"] == "shrug (default)"
    assert out["via"] == "default"


def test_situation_isolation(tmp_path):
    store = _store(tmp_path, [_rec("plaid sky", situation=OTHER_SITUATION,
                                  weight=1)])
    out = _decide(store, situation=SITUATION)
    assert out["source"] == "default"
    out2 = _decide(store, situation=OTHER_SITUATION)
    assert out2["source"].startswith("memory:")


def test_strongest_record_wins(tmp_path):
    weak = _rec("weak claim", weight=1)
    strong = _rec("strong claim", weight=3)
    store = _store(tmp_path, [weak, strong])
    out = _decide(store)
    assert out["behavior"] == "strong claim"
    assert out["memory_verification_weight"] == 3.0
    assert out["memory_records_considered"] == 2


def test_missing_inputs_refused(tmp_path):
    store = _store(tmp_path, [])
    with pytest.raises(ValueError, match="memory_store_required"):
        apply_retained_intelligence(
            memory_store=None, situation=SITUATION,
            default_behavior="x", now=NOW)
    with pytest.raises(ValueError, match="situation_required"):
        apply_retained_intelligence(
            memory_store=store, situation="  ",
            default_behavior="x", now=NOW)
    with pytest.raises(ValueError, match="policy_store_invalid"):
        apply_retained_intelligence(
            memory_store=store, policy_store=object(),
            situation=SITUATION, default_behavior="x", now=NOW)


# Adversarial: quarantined / non-active records --------------------------------

def test_quarantined_records_never_reach_action(tmp_path):
    store = _store(tmp_path, [_rec("good record", weight=1)])
    with store.records_path.open("a", encoding="utf-8") as fh:
        fh.write("{this is not json\n")
    fresh = MemoryStore(store.directory)
    fresh.load(now=NOW)
    quarantined = [r for r in fresh._records.values()
                   if r.memory_state == mm.QUARANTINED]
    assert len(quarantined) == 1  # the trap is set
    out = _decide(fresh)
    assert out["behavior"] == "good record"  # quarantined never surfaces
    assert out["memory_records_considered"] == 1


def test_only_quarantined_falls_back_to_default(tmp_path):
    store = _store(tmp_path, [])
    store.directory.mkdir(parents=True, exist_ok=True)
    with store.records_path.open("a", encoding="utf-8") as fh:
        fh.write("{this is not json\n")
    fresh = MemoryStore(store.directory)
    fresh.load(now=NOW)
    assert any(r.memory_state == mm.QUARANTINED
               for r in fresh._records.values())
    out = _decide(fresh, default="shrug (default)")
    assert out["source"] == "default"
    assert out["behavior"] == "shrug (default)"


def test_superseded_and_decayed_never_surface(tmp_path):
    old = _rec("old claim", weight=1)
    new = _rec("new claim", weight=1)
    mm.supersede(old, new, now=NOW)
    stale = _rec("stale claim", weight=1)
    mm.metabolize([stale], now="2027-10-10T10:30:00+00:00",
                  stale_after_days=90.0)
    assert stale.memory_state == mm.DECAYED
    store = _store(tmp_path, [old, new, stale])
    out = _decide(store)
    assert out["behavior"] == "new claim"
    assert out["memory_records_considered"] == 1


def test_retrieval_is_read_only(tmp_path):
    store = _store(tmp_path, [_rec(weight=1)])
    before = store.records_path.read_text(encoding="utf-8")
    _decide(store)
    after = store.records_path.read_text(encoding="utf-8")
    assert before == after  # deciding never mutates the store
