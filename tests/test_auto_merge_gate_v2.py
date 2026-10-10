"""Tests for the V2 §5.2 amendment to tools/auto_merge_gate.py.

Run: python -m pytest tests/test_auto_merge_gate_v2.py -q   (from repo root)

Covers: (1) legacy SCORECARD-LAW-V1 behavior unchanged; (2) V2 receipts
(engine == "SCORECARD-LAW-V2") validated by kernel/scorecard_law, the single
canonical receipt mechanism (V2 §7.11).
"""

from datetime import datetime, timedelta, timezone

import pytest

from kernel.scorecard_law import run_scorecard
from tools.auto_merge_gate import (
    V2_GRANT_CLAUSES,
    V2_RECEIPT_ENGINE,
    may_auto_merge,
)


def fresh_ts():
    return (datetime.now(timezone.utc) - timedelta(seconds=60)).isoformat()


def base_pr_state():
    tip = "abc123" * 10
    return {
        "evaluation_now": datetime.now(timezone.utc).isoformat(),
        "evidence_fetched_at": fresh_ts(),
        "checks_green_on_head": True,
        "head_sha": tip,
        "head_sha_verified_live": True,
        "mergeable": True,
        "has_conflicts": False,
        "base_sha": tip,
        "main_tip_sha": tip,
        "main_tip_at_merge": tip,
        "intent_comment_id": 6098821717,
        "deconfliction_refetch_at": fresh_ts(),
        "same_topic_race": False,
        "revertable_one_commit": True,
        "changed_files": ["kernel/scorecard_law.py"],
        "is_production_deploy_or_dispatch": False,
        "is_production_db_access": False,
        "touches_credentials_or_money": False,
        "is_destructive_or_irreversible": False,
        "is_constitutional_or_evolve_ratification": False,
    }


def legacy_receipt():
    return {
        "decision_id": "SC-LEGACY-1",
        "engine": "SCORECARD-LAW-V1",
        "decided_at": fresh_ts(),
        "decided_by": "naya-4",
        "rigor_tier": "LIGHT",
        "lane": "compile-law",
        "owner_seat": "naya-4",
        "author_seat": "naya-4",
        "author_lane": "compile-law",
        "step1_enumerate": {"options": [{"id": "merge"}, {"id": "wait"}]},
        "step2_score": {"scores": {
            "merge": {"value": 9, "consequences": 9, "mission_vision_alignment": 9,
                      "situational_awareness": 9},
            "wait": {"value": 5, "consequences": 5, "mission_vision_alignment": 5,
                     "situational_awareness": 5},
        }},
        "step3_gate": {"reversible": True, "no_major_damage": True,
                       "positive_forward_effect": True},
        "step4_decide": {
            "winner": "merge",
            "strongest_alternative": {"summary": "wait: safer but loses the window"},
            "falsifier": "if CI goes red on the head after this check, the decision is wrong",
        },
        "step5_receipt": {"receipt_posted_comment_id": 6098821717},
    }


def v2_receipt(**overrides):
    r = run_scorecard(
        option_ids=["merge", "wait"],
        scores={
            "merge": {"mission_alignment": 9, "value_produced": 9, "consequences": 9,
                      "collective_impact": 8, "risk": 9, "reversibility": 9},
            "wait": {"mission_alignment": 5, "value_produced": 5, "consequences": 5,
                     "collective_impact": 5, "risk": 5, "reversibility": 5},
        },
        gates={
            "merge": {"reversible": True, "no_major_damage": True, "positive_forward_effect": True},
            "wait": {"reversible": True, "no_major_damage": True, "positive_forward_effect": True},
        },
        decision_id="SC-V2-1",
        decided_by="naya-4",
        decided_at="2026-10-10T15:00:00Z",
        receipt_posted_comment_id=6098821717,
    ).receipt
    for k, v in overrides.items():
        r[k] = v
    return r


# ---- Legacy behavior preserved ------------------------------------------------


def test_legacy_receipt_still_merges():
    state = base_pr_state()
    state["scorecard_receipt"] = legacy_receipt()
    allowed, reasons = may_auto_merge(state)
    assert allowed, reasons


def test_legacy_receipt_still_refuses_on_missing_intent():
    state = base_pr_state()
    state["scorecard_receipt"] = legacy_receipt()
    del state["intent_comment_id"]
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("P5" in r for r in reasons)


def test_legacy_receipt_still_refuses_unposted_receipt():
    state = base_pr_state()
    rec = legacy_receipt()
    del rec["step5_receipt"]["receipt_posted_comment_id"]
    state["scorecard_receipt"] = rec
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("step5" in r for r in reasons)


# ---- V2 receipt path ----------------------------------------------------------


def test_v2_receipt_merges_when_everything_holds():
    state = base_pr_state()
    rec = v2_receipt()
    assert rec["engine"] == V2_RECEIPT_ENGINE
    state["scorecard_receipt"] = rec
    allowed, reasons = may_auto_merge(state)
    assert allowed, reasons


def test_v2_receipt_tampered_winner_is_refused():
    state = base_pr_state()
    rec = v2_receipt()
    rec["step4_decide"]["winner"] = "wait"  # not the highest valid total
    state["scorecard_receipt"] = rec
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("NOT_HIGHEST" in r for r in reasons)


def test_v2_receipt_unposted_is_refused():
    state = base_pr_state()
    rec = v2_receipt()
    rec["step5_receipt"]["receipt_posted_comment_id"] = None
    state["scorecard_receipt"] = rec
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("NOT_POSTED" in r for r in reasons)


def test_v2_receipt_gate_killed_winner_is_refused():
    state = base_pr_state()
    r = run_scorecard(
        option_ids=["merge", "wait"],
        scores={
            "merge": {"mission_alignment": 10, "value_produced": 10, "consequences": 10,
                      "collective_impact": 10, "risk": 10, "reversibility": 10},
            "wait": {"mission_alignment": 5, "value_produced": 5, "consequences": 5,
                     "collective_impact": 5, "risk": 5, "reversibility": 5},
        },
        gates={
            "merge": {"reversible": False, "no_major_damage": True, "positive_forward_effect": True},
            "wait": {"reversible": True, "no_major_damage": True, "positive_forward_effect": True},
        },
        decision_id="SC-V2-2",
        decided_by="naya-4",
        decided_at="2026-10-10T15:00:00Z",
        receipt_posted_comment_id=6098821717,
    ).receipt
    # the engine correctly decided "wait"; tamper the claim to the killed option
    r["step4_decide"]["winner"] = "merge"
    state["scorecard_receipt"] = r
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("FAILED_GATE" in r for r in reasons)


def test_v2_receipt_still_needs_all_preconditions():
    state = base_pr_state()
    state["scorecard_receipt"] = v2_receipt()
    state["checks_green_on_head"] = False
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("P1" in r for r in reasons)


def test_v2_grant_clauses_cover_every_precondition_family():
    # every V2 §5.2 clause maps to enforced preconditions — no clause is prose-only
    flat = {p for ps in V2_GRANT_CLAUSES.values() for p in ps}
    assert flat == {"P1", "P2", "P3", "P4", "H2", "P5", "P7", "P8", "H1", "H4"}
    assert len(V2_GRANT_CLAUSES) == 6


def test_missing_receipt_is_refused():
    state = base_pr_state()
    allowed, reasons = may_auto_merge(state)
    assert not allowed
    assert any("P8" in r for r in reasons)


def test_non_dict_state_fails_closed():
    allowed, reasons = may_auto_merge("nope")
    assert not allowed and reasons
