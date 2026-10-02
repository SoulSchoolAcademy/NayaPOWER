"""Ten-Star progression simulation (Issue #1184).

Designs and simulates the initial fair Ten-Star progression profile BEFORE any
live reward deployment. Deterministic (seeded). All weights, thresholds, and
names are HYPOTHESES (profile `ten-star-action-profile-v1`), versioned and
calibratable from evidence.

Load-bearing invariants (from the torch):
  Truth before score. Law before optimization. Authority before action.
  Value before activity. Evidence before reward. Human worth outside the
  equation. Reality corrects the math.

Historical note: a Brain-wide search on 2026-09-30 recovered NO historical
Ten-Star level-name set (the only "ten-star" hit is the Director's phrase
"ten-star service"). The names below are therefore fresh candidates.

Move coverage:
  #5  initial weights per action class (hypotheses)
  #6  diminishing returns + novelty (repetition cannot farm)
  #7  Sybil / collusion / self-interaction defenses
  #8  historical name recovery (negative result, documented above)
  #9  progression-curve simulation incl. the 75,000-point Ten-Star hypothesis
  #10 score/level projected from receipt evidence, never a stored magic number
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from kernel.smartledger_value_seam import TEN_STAR_TIERS, tier_for_points
from kernel.value_calculus import contribution_points, contribution_value_score

PROFILE_VERSION = "ten-star-action-profile-v1-hypothesis"

# Move #5: hypothesized points-per-CVS-unit per action class.
# Raw engagement (verification == 0) still earns EXACTLY zero regardless of
# these weights: the weights price VERIFIED value, never activity.
ACTION_PROFILE_V1 = {
    "like": 2.0,          # reaction; only via verified downstream attribution
    "comment": 5.0,       # reply; only when it produces verified value
    "share": 8.0,         # distribution; only via verified reuse
    "help": 40.0,         # answer/help with a verified useful outcome
    "introduction": 45.0, # successful connection/collaboration
    "verify": 50.0,       # verification/review contribution
    "create": 60.0,       # original creation
    "correction": 70.0,   # correction of false/stale intelligence
    "reuse": 80.0,        # reusable learning adopted downstream
}

# Move #6: diminishing returns. nth same-class contribution in a trailing
# 30-day window is worth 1/(1+0.15*(n-1)) of the first.
DECAY_RATE = 0.15


def repeat_decay(n: int) -> float:
    return 1.0 / (1.0 + DECAY_RATE * max(0, n - 1))


# Move #7: defenses -----------------------------------------------------------
#   self-interaction: actor == contributor  -> verification forced to 0
#   collusion: verification counts only from OUTSIDE the contributor's clique
#     (mirrors the graph's independent-verification requirement)
#   sybil: identities sharing a fingerprint reposting the same content
#     -> novelty forced to 0


@dataclass
class ContributionEvent:
    contributor: str
    actor: str  # who performed the action (self-interaction check)
    action_class: str
    quality: float
    relevance: float
    verification: float       # raw verification claim
    independent_fraction: float = 1.0  # share of verifiers outside any clique
    impact: float = 0.7
    novelty: float = 0.8
    verified_delta: float = 3.0
    sybil_flag: bool = False


def score_event(event: ContributionEvent, class_count_30d: int) -> dict:
    verification = event.verification
    if event.actor == event.contributor:
        verification = 0.0  # self-interaction: no self-verification
    verification *= event.independent_fraction  # collusion discount
    novelty = 0.0 if event.sybil_flag else event.novelty
    cvs = contribution_value_score(
        quality=event.quality, relevance=event.relevance,
        verification=verification, impact=event.impact,
        novelty=novelty, verified_delta=event.verified_delta,
    )
    ppu = ACTION_PROFILE_V1[event.action_class]
    decay = repeat_decay(class_count_30d + 1)
    points = contribution_points(cvs, ppu, decay)
    return {"cvs": cvs, "points": points, "decay": decay,
            "verification_effective": verification}


@dataclass
class Persona:
    name: str
    behavior: str  # "honest_steady" | "honest_strong" | "spam_farmer" |
                   # "collusion_ring" | "one_hit" | "sybil_cluster"
    member_ids: list = field(default_factory=list)


def _weekly_events(persona: Persona, rng: random.Random, week: int) -> list[ContributionEvent]:
    b = persona.behavior
    evs: list[ContributionEvent] = []
    if b == "honest_steady":
        cid = persona.member_ids[0]
        for _ in range(2):
            evs.append(ContributionEvent(cid, "peer", "create",
                                         rng.uniform(0.6, 0.8), rng.uniform(0.6, 0.8),
                                         rng.uniform(0.7, 0.9), 1.0,
                                         rng.uniform(0.6, 0.8), rng.uniform(0.6, 0.8),
                                         rng.uniform(3, 6)))
        for _ in range(3):
            evs.append(ContributionEvent(cid, "peer", "help",
                                         rng.uniform(0.6, 0.8), rng.uniform(0.7, 0.9),
                                         rng.uniform(0.7, 0.9), 1.0,
                                         rng.uniform(0.6, 0.8), rng.uniform(0.5, 0.7),
                                         rng.uniform(2, 4)))
        for _ in range(5):
            evs.append(ContributionEvent(cid, "peer", "comment",
                                         rng.uniform(0.5, 0.7), rng.uniform(0.5, 0.7),
                                         rng.uniform(0.5, 0.7), 1.0,
                                         rng.uniform(0.4, 0.6), rng.uniform(0.4, 0.6),
                                         rng.uniform(1, 2)))
    elif b == "honest_strong":
        cid = persona.member_ids[0]
        for _ in range(3):
            evs.append(ContributionEvent(cid, "peer", "create",
                                         rng.uniform(0.8, 0.95), rng.uniform(0.8, 0.95),
                                         rng.uniform(0.8, 0.95), 1.0,
                                         rng.uniform(0.7, 0.9), rng.uniform(0.7, 0.9),
                                         rng.uniform(4, 8)))
        for _ in range(5):
            evs.append(ContributionEvent(cid, "peer", "help",
                                         rng.uniform(0.8, 0.9), rng.uniform(0.8, 0.9),
                                         rng.uniform(0.8, 0.9), 1.0,
                                         rng.uniform(0.7, 0.85), rng.uniform(0.6, 0.8),
                                         rng.uniform(3, 5)))
        for _ in range(2):
            evs.append(ContributionEvent(cid, "peer", "verify",
                                         rng.uniform(0.8, 0.9), rng.uniform(0.8, 0.9),
                                         0.9, 1.0,
                                         rng.uniform(0.7, 0.8), 0.7,
                                         rng.uniform(2, 4)))
    elif b == "spam_farmer":
        cid = persona.member_ids[0]
        for _ in range(3500):  # 500 likes/day, zero verified value
            evs.append(ContributionEvent(cid, "peer", "like",
                                         0.5, 0.5, 0.0, 1.0, 0.3, 0.1, 0.0))
    elif b == "collusion_ring":
        ring = persona.member_ids
        for i, cid in enumerate(ring):
            verifier = ring[(i + 1) % len(ring)]
            for _ in range(20):
                evs.append(ContributionEvent(cid, verifier, "comment",
                                             0.6, 0.6, 0.9, 0.0,  # ring-only: no independent verifier
                                             0.6, 0.5, 2.0))
    elif b == "one_hit":
        if week == 0:
            cid = persona.member_ids[0]
            evs.append(ContributionEvent(cid, "peer", "create",
                                         0.95, 0.95, 0.95, 1.0, 0.9, 0.95, 9.0))
    elif b == "sybil_cluster":
        for sid in persona.member_ids:
            for _ in range(10):
                evs.append(ContributionEvent(sid, "peer", "create",
                                             0.6, 0.6, 0.7, 1.0, 0.6, 0.6, 3.0,
                                             sybil_flag=True))
    return evs


def simulate(persona: Persona, weeks: int = 104, seed: int = 7) -> dict:
    """Simulate week-by-week. Returns trajectory + tier milestones."""
    rng = random.Random(seed)
    counts_30d: dict[tuple[str, str], list[int]] = {}
    total_points = 0.0
    total_cvs = 0.0
    events_scored = 0
    milestones: dict[int, int] = {}  # stars -> week reached
    current_stars = 1
    weekly_points: list[float] = []

    for week in range(weeks):
        week_points = 0.0
        for ev in _weekly_events(persona, rng, week):
            key = (ev.contributor, ev.action_class)
            recent = [w for w in counts_30d.get(key, []) if week - w < 5]
            scored = score_event(ev, len(recent))
            recent.append(week)
            counts_30d[key] = recent
            week_points += scored["points"]
            total_cvs += scored["cvs"]
            events_scored += 1
        total_points += week_points
        weekly_points.append(week_points)
        tier = tier_for_points(total_points)
        if tier["stars"] > current_stars:
            for s in range(current_stars + 1, tier["stars"] + 1):
                milestones[s] = week + 1
            current_stars = tier["stars"]
        if current_stars >= 10:
            break

    final_tier = tier_for_points(total_points)
    return {
        "persona": persona.name,
        "behavior": persona.behavior,
        "weeks_simulated": week + 1,
        "events_scored": events_scored,
        "total_points": round(total_points, 2),
        "total_cvs": round(total_cvs, 2),
        "final_tier": final_tier,
        "milestones": milestones,  # stars -> week first reached
        "avg_weekly_points": round(total_points / (week + 1), 2),
        "profile_version": PROFILE_VERSION,
    }


def run_progression_study(weeks: int = 104) -> dict:
    """Run all personas; the honest-path pacing + adversarial resistance."""
    personas = [
        Persona("Steady Sam", "honest_steady", ["sam"]),
        Persona("Strong Sofia", "honest_strong", ["sofia"]),
        Persona("Spam Farmer", "spam_farmer", ["spammer"]),
        Persona("Collusion Ring", "collusion_ring",
                [f"ring{i}" for i in range(5)]),
        Persona("One-Hit Wanda", "one_hit", ["wanda"]),
        Persona("Sybil Cluster", "sybil_cluster", [f"sybil{i}" for i in range(20)]),
    ]
    results = [simulate(p, weeks=weeks, seed=7) for p in personas]
    return {
        "profile_version": PROFILE_VERSION,
        "tier_thresholds": [{"stars": s, "name": n, "points": t}
                             for s, n, t in TEN_STAR_TIERS],
        "hypothesis_note": "All weights/thresholds are hypotheses; calibrate from evidence.",
        "results": results,
    }


if __name__ == "__main__":
    import json
    study = run_progression_study()
    print(json.dumps(study, indent=1))
