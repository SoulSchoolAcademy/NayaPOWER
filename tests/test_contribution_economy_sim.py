"""Fast deterministic tests for the Ten-Star progression simulation.

Invariants under test (Issue #1184):
  - raw engagement without verification earns exactly zero (move: activity != value)
  - spam farming, collusion rings, and sybil clusters earn ~zero (move #7)
  - repetition diminishes via repeat_decay (move #6)
  - honest verified contribution progresses monotonically (move #9)
  - simulation is deterministic (seeded)
"""

import pytest

from kernel.contribution_economy_sim import (
    ACTION_PROFILE_V1,
    ContributionEvent,
    Persona,
    repeat_decay,
    run_progression_study,
    score_event,
    simulate,
)
from kernel.smartledger_value_seam import TEN_STAR_TIERS, tier_for_points


def _ev(action_class="create", **overrides):
    params = dict(contributor="u1", actor="peer", action_class=action_class,
                  quality=0.8, relevance=0.8, verification=0.9,
                  independent_fraction=1.0, impact=0.7, novelty=0.8,
                  verified_delta=4.0)
    params.update(overrides)
    return ContributionEvent(**params)


def test_repeat_decay_diminishes():
    assert repeat_decay(1) == pytest.approx(1.0)
    assert repeat_decay(5) < repeat_decay(1)
    assert repeat_decay(100) > 0  # never fully zero, just diminished


def test_raw_engagement_without_verification_earns_zero():
    scored = score_event(_ev("like", verification=0.0, verified_delta=0.0), 0)
    assert scored["points"] == 0.0
    scored = score_event(_ev("comment", verification=0.0), 0)
    assert scored["points"] == 0.0


def test_self_interaction_forces_zero():
    scored = score_event(_ev("create", actor="u1", verification=0.9), 0)
    assert scored["verification_effective"] == 0.0
    assert scored["points"] == 0.0


def test_collusion_ring_only_verification_discounted():
    scored = score_event(_ev("comment", verification=0.9, independent_fraction=0.0), 0)
    assert scored["points"] == 0.0


def test_sybil_flag_kills_novelty():
    scored = score_event(_ev("create", sybil_flag=True), 0)
    assert scored["points"] == 0.0


def test_verified_value_earns_points():
    scored = score_event(_ev("create"), 0)
    assert scored["cvs"] > 0
    assert scored["points"] > 0
    # points == cvs * ppu * decay, exactly
    assert scored["points"] == pytest.approx(
        scored["cvs"] * ACTION_PROFILE_V1["create"] * scored["decay"])


def test_action_profile_weights_are_hypotheses():
    assert set(ACTION_PROFILE_V1) >= {
        "like", "comment", "share", "help", "create", "verify", "reuse"}
    assert ACTION_PROFILE_V1["reuse"] > ACTION_PROFILE_V1["like"]


def test_ten_star_thresholds_monotone_and_75k():
    thresholds = [t for _, _, t in TEN_STAR_TIERS]
    assert thresholds == sorted(thresholds)
    assert len(TEN_STAR_TIERS) == 10
    assert tier_for_points(75_000)["stars"] == 10
    assert tier_for_points(75_000)["name"] == "Primal Master"


def test_simulation_deterministic():
    p = Persona("Steady Sam", "honest_steady", ["sam"])
    r1 = simulate(p, weeks=6, seed=7)
    r2 = simulate(p, weeks=6, seed=7)
    assert r1["total_points"] == r2["total_points"]
    assert r1["milestones"] == r2["milestones"]


def test_honest_progresses_adversaries_do_not():
    honest = simulate(Persona("Steady Sam", "honest_steady", ["sam"]),
                      weeks=6, seed=7)
    spam = simulate(Persona("Spam Farmer", "spam_farmer", ["spammer"]),
                    weeks=6, seed=7)
    ring = simulate(Persona("Collusion Ring", "collusion_ring",
                            [f"ring{i}" for i in range(5)]),
                    weeks=6, seed=7)
    sybil = simulate(Persona("Sybil Cluster", "sybil_cluster",
                             [f"sybil{i}" for i in range(3)]),
                     weeks=6, seed=7)
    assert honest["total_points"] > 0
    assert honest["final_tier"]["stars"] >= 2
    assert spam["total_points"] == 0
    assert ring["total_points"] == 0
    assert sybil["total_points"] == 0
    # the spammer ran far more events yet earned nothing: volume != value
    assert spam["events_scored"] > honest["events_scored"] * 100


def test_progression_study_shape():
    study = run_progression_study(weeks=4)
    assert study["profile_version"].endswith("hypothesis")
    assert len(study["results"]) == 6
    assert len(study["tier_thresholds"]) == 10
