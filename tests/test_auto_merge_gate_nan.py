#!/usr/bin/env python3
"""Regression tests for the NaN/Infinity score bypass in tools/auto_merge_gate.py.

Found by the SAFETY red-team (2026-10-07): the step-2 dimension check used
`v < 0 or v > 10`, and every comparison against NaN is False — so NaN passed
the range check, the total became NaN, and the winner check also passed.
A fabricated scorecard with NaN scores would authorize a merge.

The fix: require math.isfinite(v) in the step-2 scoring loop.
These tests pin that behavior permanently.
"""

import json
import subprocess
import sys
import tempfile
import os
from datetime import datetime, timezone
from pathlib import Path

GATE = Path(__file__).resolve().parent.parent / "tools" / "auto_merge_gate.py"
DIMS = ("value", "consequences", "mission_vision_alignment", "situational_awareness")


def run_gate(scores):
    now = datetime.now(timezone.utc).isoformat()
    tip = "f06903ff2f06903ff2f06903ff2f06903ff2f06903ff"
    receipt = {
        "decision_id": "test-nan-001",
        "engine": "test",
        "decided_at": now,
        "decided_by": "test",
        "step1_enumerate": {"options": [{"id": "a"}, {"id": "b"}]},
        "step2_score": {"scores": scores},
        "step3_gate": {"gates": {"reversible": True, "no_major_damage": True,
                                 "positive_forward_effect": True}},
        "step4_decide": {"winner": "a", "strongest_alternative": "b",
                         "falsifier": "test"},
        "step5_receipt": {"posted": True, "receipt_url": "https://example.com/x",
                          "comment_id": 12345},
    }
    state = {
        "pr_number": 9999,
        "pr_head_sha": tip,
        "pr_base_sha": tip,
        "head_sha": tip,
        "checks_green_on_head": True,
        "head_sha_verified_live": True,
        "mergeable": True,
        "has_conflicts": False,
        "base_sha": tip,
        "main_tip_sha": tip,
        "main_tip_at_merge": tip,
        "intent_comment_id": 12345,
        "deconfliction_refetch_at": now,
        "same_topic_race": False,
        "revertable_one_commit": True,
        "changed_files": ["tools/auto_merge_gate.py"],
        "is_production_deploy_or_dispatch": False,
        "is_production_db_access": False,
        "touches_credentials_or_money": False,
        "is_destructive_or_irreversible": False,
        "is_constitutional_or_evolve_ratification": False,
        "scorecard_receipt": receipt,
        "evaluation_now": now,
        "evidence_fetched_at": now,
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(state, f)
        fname = f.name
    try:
        r = subprocess.run([sys.executable, str(GATE), fname],
                           capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout)
    finally:
        os.unlink(fname)


def step2_reasons(result):
    return [r for r in result.get("reasons", []) if "step2" in r.lower()]


def test_nan_winner_rejected():
    scores = {"a": {d: float("nan") for d in DIMS},
              "b": {d: 5.0 for d in DIMS}}
    result = run_gate(scores)
    assert result["allowed"] is False, "NaN winner score must not authorize a merge"
    assert step2_reasons(result), "rejection must cite step2"


def test_nan_loser_rejected():
    scores = {"a": {d: 8.0 for d in DIMS},
              "b": {d: float("nan") for d in DIMS}}
    result = run_gate(scores)
    assert result["allowed"] is False, "NaN loser score must not authorize a merge"
    assert step2_reasons(result), "rejection must cite step2"


def test_infinity_rejected():
    scores = {"a": {d: float("inf") for d in DIMS},
              "b": {d: 5.0 for d in DIMS}}
    result = run_gate(scores)
    assert result["allowed"] is False, "Infinity score must not authorize a merge"
    assert step2_reasons(result), "rejection must cite step2"


def test_negative_infinity_rejected():
    scores = {"a": {d: float("-inf") for d in DIMS},
              "b": {d: 5.0 for d in DIMS}}
    result = run_gate(scores)
    assert result["allowed"] is False, "-Infinity score must not authorize a merge"
    assert step2_reasons(result), "rejection must cite step2"


def test_legit_scores_pass_step2():
    scores = {"a": {d: 8.0 for d in DIMS},
              "b": {d: 5.0 for d in DIMS}}
    result = run_gate(scores)
    assert not step2_reasons(result), \
        f"legitimate scores must pass step2, got: {step2_reasons(result)}"


def test_boundary_scores_pass_step2():
    scores = {"a": {d: 10.0 for d in DIMS},
              "b": {d: 0.0 for d in DIMS}}
    result = run_gate(scores)
    assert not step2_reasons(result), \
        f"boundary scores (0, 10) must pass step2, got: {step2_reasons(result)}"


if __name__ == "__main__":
    test_nan_winner_rejected()
    test_nan_loser_rejected()
    test_infinity_rejected()
    test_negative_infinity_rejected()
    test_legit_scores_pass_step2()
    test_boundary_scores_pass_step2()
    print("6/6 NaN regression tests green")
