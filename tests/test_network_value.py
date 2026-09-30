"""Tests for kernel/network_value.py.

Adversarial focus: raw activity must never outrank verified value
(spam resistance), duplicate content earns zero, negative contributions
never auto-punish, and authority is never derived from reputation.
"""

import pytest

from kernel.network_value import (
    LEVELS,
    MICRO_ACTION_PARAMS,
    Profile,
    contribution_credit,
    contribution_points,
    contribution_receipt,
    credit_micro_action,
    grant_authority,
    level_for,
)


# ---------------------------------------------------------------------------
# Contribution credit math
# ---------------------------------------------------------------------------

def test_perfect_contribution_scores_nine():
    c = contribution_credit(1, 1, 1, 1, 1, delta_v_verified=12.0)
    assert c["cvs"] == pytest.approx(9.0)
    assert c["sign"] == 1.0


def test_zero_factor_zeroes_credit():
    # Brilliant but unverified -> nothing until verified.
    c = contribution_credit(1, 1, 0, 1, 1, delta_v_verified=12.0)
    assert c["cvs"] == pytest.approx(0.0)


def test_negative_value_contribution_is_recorded_negative():
    c = contribution_credit(0.8, 0.8, 0.9, 0.7, 0.6, delta_v_verified=-5.0)
    assert c["cvs"] < 0
    assert c["sign"] == -1.0


def test_neutral_contribution_earns_nothing():
    c = contribution_credit(1, 1, 1, 1, 1, delta_v_verified=0.0)
    assert c["cvs"] == pytest.approx(0.0)


def test_factors_must_be_unit():
    with pytest.raises(ValueError):
        contribution_credit(1.5, 1, 1, 1, 1, delta_v_verified=1.0)


# ---------------------------------------------------------------------------
# Spam resistance: 10,000 low-value actions cannot outrank one discovery
# ---------------------------------------------------------------------------

def test_year_of_max_like_spam_loses_to_one_discovery():
    spam_points = 0.0
    for _day in range(365):
        for n in range(MICRO_ACTION_PARAMS["daily_caps"]["like"]):
            spam_points += credit_micro_action("like", n)["points"]
    discovery = contribution_credit(1, 1, 1, 1, 1, delta_v_verified=20.0)
    discovery_points = contribution_points(discovery)
    assert discovery_points == pytest.approx(4500.0)
    assert spam_points < discovery_points


def test_daily_cap_blocks_flooding():
    assert credit_micro_action("like", 20)["points"] == pytest.approx(0.0)
    assert credit_micro_action("like", 20)["reason"] == "daily_cap_reached"


def test_duplicate_content_earns_zero():
    r = credit_micro_action("comment", 0, is_duplicate=True)
    assert r["points"] == pytest.approx(0.0)
    assert r["reason"] == "duplicate_content"


def test_diminishing_returns_within_day():
    first = credit_micro_action("like", 0)["points"]
    tenth = credit_micro_action("like", 9)["points"]
    assert tenth < first


# ---------------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------------

def test_ten_star_at_75000():
    p = Profile("shawn", contribution_points=75000.0,
                reliability=0.9, conduct=1.0)
    assert level_for(p).name == "Ten-Star"
    assert level_for(p).rank == 10


def test_level_thresholds():
    assert level_for(Profile("x", contribution_points=0)).name == "New"
    assert level_for(Profile("x", contribution_points=150)).name == "Emerging"
    assert level_for(Profile("x", contribution_points=4000)).name == "Five-Star"


def test_points_without_standing_cannot_buy_status():
    # 80k points but poor conduct -> capped below Advanced (rank 6).
    p = Profile("y", contribution_points=80000.0,
                reliability=0.9, conduct=0.5)
    assert level_for(p).rank < 6


def test_ten_levels_exist():
    assert len(LEVELS) == 10
    assert LEVELS[0].name == "New"
    assert LEVELS[-1].name == "Ten-Star"
    thresholds = [lv.points_threshold for lv in LEVELS]
    assert thresholds == sorted(thresholds)


# ---------------------------------------------------------------------------
# No auto-punishment; reliability learns gently
# ---------------------------------------------------------------------------

def test_negative_contribution_does_not_ban_or_subtract():
    p = Profile("z", contribution_points=1000.0)
    bad = contribution_credit(0.8, 0.8, 0.9, 0.7, 0.6, delta_v_verified=-5.0)
    before = p.reliability
    out = p.record_contribution(bad)
    assert out["points_added"] == pytest.approx(0.0)
    assert p.contribution_points == pytest.approx(1000.0)
    assert p.active is True
    assert p.conduct == pytest.approx(1.0)  # conduct untouched by the math
    assert p.reliability < before            # but reliability learns


def test_profile_update_accumulates():
    p = Profile("w")
    good = contribution_credit(1, 1, 1, 1, 1, delta_v_verified=10.0)
    out = p.record_contribution(good)
    assert out["points_added"] == pytest.approx(4500.0)
    assert p.verified_contributions == 1


# ---------------------------------------------------------------------------
# Authority != Reputation, always
# ---------------------------------------------------------------------------

def test_authority_grant_ignores_reputation():
    nobody = Profile("nobody")  # zero points, brand new
    grant = grant_authority("nobody", granted_by="shawn",
                            scope="deploy:staging", reason="trusted operator")
    assert grant["derived_from_reputation"] is False
    assert grant["scope"] == "deploy:staging"


def test_massive_reputation_grants_no_authority_by_itself():
    star = Profile("star", contribution_points=75000.0,
                   reliability=0.9, conduct=1.0)
    assert level_for(star).name == "Ten-Star"
    # There is no function turning points into authority: the only path
    # is an explicit governance grant.
    with pytest.raises(ValueError):
        grant_authority("star", granted_by="", scope="admin", reason="x")


# ---------------------------------------------------------------------------
# Trust is derived and bounded; receipt shape
# ---------------------------------------------------------------------------

def test_trust_is_bounded_and_contextual():
    p = Profile("t", contribution_points=75000.0, reliability=0.9, conduct=1.0)
    t = p.trust(recency=1.0)
    assert 0.0 <= t <= 1.0
    assert p.trust(recency=0.0) < t


def test_contribution_receipt_stream_b_shape():
    c = contribution_credit(0.9, 0.9, 0.9, 0.8, 0.7, delta_v_verified=8.0)
    r = contribution_receipt("shawn", "contrib-1", "owner:shawn", c,
                             provenance="hub:post:123",
                             privacy_consent="public")
    assert r["receipt_type"] == "contribution"
    assert r["contributor_id"] == "shawn"
    assert "downstream_verified_value" in r
