"""Tests for the Next-Best-Action priority combination layer.

RED phase: these tests define the deterministic contract before implementation.
"""

import pytest

from kernel.value_calculus import (
    ACTION_DIMENSIONS,
    NextBestActionProfile,
    NextBestActionCandidate,
    combine_next_best_action_score,
    rank_next_best_actions,
)


def candidate(cid, **scores):
    base = {d: 5.0 for d in ACTION_DIMENSIONS}
    base.update(scores)
    return NextBestActionCandidate(candidate_id=cid, scores=base)


def test_exactly_ten_dimensions_and_default_weights_sum_to_one():
    assert len(ACTION_DIMENSIONS) == 10
    profile = NextBestActionProfile.default()
    assert sum(profile.weights.values()) == pytest.approx(1.0)
    assert set(profile.weights) == set(ACTION_DIMENSIONS)


def test_combination_is_deterministic_weighted_score():
    p = ActionProfile.default()
    a = candidate("a", mission_value=10, human_value=10, urgency=0, leverage=0,
                  evidence=10, risk=0, cost=0, dependencies=0, reversibility=10,
                  compounding_continuity=10)
    assert combine_next_best_action_score(a, p) == pytest.approx(
        sum(p.weights[d] * a.scores[d] for d in ACTION_DIMENSIONS)
    )


def test_hard_risk_cap_blocks_even_a_high_average():
    p = ActionProfile.default()
    a = candidate("danger", mission_value=10, human_value=10, evidence=10,
                  leverage=10, risk=9.0, cost=0, dependencies=10,
                  reversibility=10, urgency=10, compounding_continuity=10)
    result = rank_next_best_actions([a], p)
    assert result[0].status == "BLOCKED"
    assert result[0].reason == "RISK_CAP"


def test_low_evidence_routes_to_read_more_not_act():
    p = ActionProfile.default()
    a = candidate("unknown", mission_value=10, human_value=10, urgency=10,
                  leverage=10, evidence=5.9, risk=1, cost=1, dependencies=10,
                  reversibility=10, compounding_continuity=10)
    result = rank_actions([a], p)
    assert result[0].status == "READ_MORE"
    assert result[0].reason == "EVIDENCE_FLOOR"


def test_thresholds_apply_after_score_and_before_selection():
    p = ActionProfile.default()
    low = candidate("low", mission_value=2, human_value=2, urgency=2, leverage=2,
                    evidence=10, risk=0, cost=0, dependencies=0, reversibility=10,
                    compounding_continuity=2)
    result = rank_actions([low], p)
    assert result[0].status == "BELOW_STANDARD"


def test_tie_breakers_are_deterministic_and_ordered():
    p = ActionProfile.default()
    a = candidate("a", mission_value=9, human_value=9, urgency=5, leverage=9,
                  evidence=9, risk=2, cost=5, dependencies=5, reversibility=9,
                  compounding_continuity=9)
    b = candidate("b", mission_value=9, human_value=9, urgency=5, leverage=9,
                  evidence=9, risk=2, cost=5, dependencies=5, reversibility=9,
                  compounding_continuity=9)
    ranked = rank_actions([b, a], p)
    assert [r.candidate_id for r in ranked] == ["a", "b"]


def test_top_level_selection_requires_margin_when_two_options_are_close():
    p = ActionProfile.default()
    a = candidate("a", mission_value=10, human_value=10, urgency=10, leverage=10,
                  evidence=10, risk=0, cost=0, dependencies=10, reversibility=10,
                  compounding_continuity=10)
    b = candidate("b", mission_value=9.9, human_value=9.9, urgency=10, leverage=10,
                  evidence=10, risk=0, cost=0, dependencies=10, reversibility=10,
                  compounding_continuity=10)
    ranked = rank_actions([a, b], p)
    assert ranked[0].status == "READ_MORE"
    assert ranked[0].reason == "NO_CLEAR_DOMINANT_OPTION"


def test_profile_rejects_unknown_dimensions_and_invalid_weights():
    with pytest.raises(ValueError):
        NextBestActionProfile(profile_id="x", version="1", weights={"mission_value": 1, "bogus": 1})
    with pytest.raises(ValueError):
        ActionProfile(profile_id="x", version="1",
                      weights={d: 0 for d in ACTION_DIMENSIONS})


def test_compounding_and_continuity_are_one_dimension_not_two():
    assert "compounding" not in ACTION_DIMENSIONS
    assert "continuity" not in ACTION_DIMENSIONS
    assert "compounding_continuity" in ACTION_DIMENSIONS
