"""NayaPOWER network value — contribution credit, profiles, and levels.

Spec authority: Decision Value Calculus V2.1 section 11
("Human contribution / reputation law"), issue #1182.

This module implements the NETWORK-VALUE mathematics:

    contribution -> provenance -> novelty -> quality -> relevance
        -> verification -> impact -> reuse -> downstream verified value

It is deliberately separate from the DECISION mathematics
(kernel/value_calculus_v2.py). One shared SmartLedger substrate, two typed
receipt streams; different semantics, writers, and trust computations.

NON-NEGOTIABLE INVARIANTS (from the spec):
  - Never score human worth. The profile is a 4-tuple (C, R, K, T); no
    single scalar is exposed as a person's value.
  - Activity != Value. Raw action counts never earn reputation by
    themselves; credit flows only through verified value.
  - No single negative contribution automatically punishes or bans a person.
  - No amount of contribution grants authority. Authority is granted by
    governance through a separate path and is never derived from points.
  - No high reputation overrides privacy, consent, law, rights, governance.

Truth state: CANDIDATE baseline. Weights, caps, and thresholds are
versioned hypotheses that change only through verified learning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence
import math

ENGINE_VERSION = "NETWORK-VALUE-V2.1.0"
SPEC_VERSION = "decision-value-calculus-v2.1.0"

# ---------------------------------------------------------------------------
# Contribution credit: CVS_j = sign(dV) * 9 * (Q*Rel*Ver*Impact*Novelty)^(1/5)
# ---------------------------------------------------------------------------


def _unit(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def contribution_credit(quality: float, relevance: float, verification: float,
                        impact: float, novelty: float,
                        delta_v_verified: float) -> dict:
    """Credit for one verified contribution.

    The geometric mean means a zero on any factor zeroes the credit: a
    brilliant but unverified claim earns nothing until verified; a verified
    but irrelevant or duplicated item earns ~nothing. sign(dV) keeps
    destructive contributions negative (recorded, never auto-punishing).
    """
    factors = {
        "quality": _unit(quality, "quality"),
        "relevance": _unit(relevance, "relevance"),
        "verification": _unit(verification, "verification"),
        "impact": _unit(impact, "impact"),
        "novelty": _unit(novelty, "novelty"),
    }
    delta_v_verified = float(delta_v_verified)
    if not math.isfinite(delta_v_verified):
        raise ValueError("delta_v_verified must be finite")
    sign = 1.0 if delta_v_verified > 0 else (-1.0 if delta_v_verified < 0 else 0.0)
    geo = math.prod(factors.values()) ** (1.0 / 5.0)
    cvs = sign * 9.0 * geo
    return {"cvs": cvs, "factors": factors,
            "delta_v_verified": delta_v_verified, "sign": sign}


# ---------------------------------------------------------------------------
# Contribution receipt (SmartLedger stream B)
# ---------------------------------------------------------------------------


def contribution_receipt(contributor_id: str, contribution_id: str,
                        owner_boundary: str,
                        credit: dict,
                        provenance: str,
                        privacy_consent: str,
                        reuse_count: int = 0,
                        downstream_verified_value: float = 0.0) -> dict:
    """CONTRIBUTION / NETWORK-VALUE RECEIPT (stream B)."""
    return {
        "receipt_type": "contribution",
        "engine_version": ENGINE_VERSION,
        "spec_version": SPEC_VERSION,
        "contributor_id": contributor_id,
        "contribution_id": contribution_id,
        "owner_boundary": owner_boundary,
        "credit": credit,
        "provenance": provenance,
        "reuse_count": int(reuse_count),
        "downstream_verified_value": float(downstream_verified_value),
        "privacy_consent": privacy_consent,
    }


# ---------------------------------------------------------------------------
# Micro-action rubric (candidate, versioned)
# ---------------------------------------------------------------------------

# Small, capped, diminishing credit for lightweight engagement signals.
# These are WEAK evidence of value, weighted accordingly: even a full year
# of maxed-out liking cannot outrank one extraordinary verified
# contribution. Identical/repeated content earns zero (spam control).
MICRO_ACTION_PARAMS = {
    "version": "micro-action-rubric-v2.1.0",
    "weights": {"like": 0.5, "comment": 2.0, "share": 3.0},
    "daily_caps": {"like": 20, "comment": 10, "share": 5},
    "decay": 0.9,  # credit_n = base * decay^(n-1) within the day
}


def credit_micro_action(action: str, n_today: int,
                        is_duplicate: bool = False,
                        params: Mapping = MICRO_ACTION_PARAMS) -> dict:
    """Credit for one micro-action; n_today counts prior same-actions today."""
    if action not in params["weights"]:
        raise ValueError(f"unknown micro-action '{action}'")
    if is_duplicate:
        return {"action": action, "points": 0.0, "reason": "duplicate_content"}
    cap = params["daily_caps"][action]
    if n_today >= cap:
        return {"action": action, "points": 0.0, "reason": "daily_cap_reached"}
    base = params["weights"][action]
    points = base * (params["decay"] ** n_today)
    return {"action": action, "points": points, "reason": "credited"}


# Points per unit of verified contribution credit (candidate scale).
CONTRIBUTION_POINTS_PER_CVS = 500.0


def contribution_points(credit: dict) -> float:
    """Verified contributions convert to points; negative credit never
    subtracts points (recorded in reliability instead — no auto-punish)."""
    return max(0.0, credit["cvs"]) * CONTRIBUTION_POINTS_PER_CVS


# ---------------------------------------------------------------------------
# Profile: (C, R, K, T)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Level:
    rank: int
    name: str
    points_threshold: float
    min_reliability: float = 0.0
    min_conduct: float = 0.0


LEVELS: Sequence[Level] = (
    Level(1, "New", 0),
    Level(2, "Emerging", 100),
    Level(3, "Developing", 500),
    Level(4, "Advancing", 1500),
    Level(5, "Five-Star", 4000),
    Level(6, "Advanced", 9000, min_reliability=0.70, min_conduct=0.80),
    Level(7, "Expert", 18000, min_reliability=0.70, min_conduct=0.80),
    Level(8, "Elite", 32000, min_reliability=0.80, min_conduct=0.90),
    Level(9, "Master", 52000, min_reliability=0.80, min_conduct=0.90),
    Level(10, "Ten-Star", 75000, min_reliability=0.85, min_conduct=0.95),
)


@dataclass
class Profile:
    """Multidimensional profile. There is no single 'worth' scalar.

    C = contribution_points: cumulative verified contribution value.
    R = reliability: accuracy/usefulness over time, EWMA of verifications.
    K = conduct: rule compliance; changed only by governance events.
    T = trust: derived, contextual; recomputed, never stored as identity.
    """
    contributor_id: str
    contribution_points: float = 0.0
    reliability: float = 0.5
    conduct: float = 1.0
    verified_contributions: int = 0
    micro_action_points: float = 0.0
    active: bool = True  # only governance can deactivate; never the math

    def record_contribution(self, credit: dict,
                            reliability_alpha: float = 0.2) -> dict:
        """Apply a verified contribution receipt to the profile."""
        pts = contribution_points(credit)
        self.contribution_points += pts
        self.verified_contributions += 1
        # Reliability tracks verification outcomes: positive verified value
        # raises it, negative lowers it — gently, via EWMA. Never a ban.
        outcome = 1.0 if credit["sign"] > 0 else (0.0 if credit["sign"] < 0 else 0.5)
        self.reliability = ((1 - reliability_alpha) * self.reliability
                            + reliability_alpha * outcome)
        return {"points_added": pts,
                "contribution_points": self.contribution_points,
                "reliability": self.reliability}

    def record_micro_action(self, points: float) -> None:
        self.micro_action_points += points
        self.contribution_points += points

    def trust(self, recency: float = 1.0) -> float:
        """T = f(C, R, K, provenance, recency, domain). Candidate formula:
        contribution normalized on the Ten-Star scale, mixed with
        reliability, conduct, and recency. Contextual, recomputed per use."""
        c_norm = min(1.0, self.contribution_points / 75000.0)
        return max(0.0, min(1.0,
                            0.40 * c_norm + 0.30 * self.reliability
                            + 0.20 * self.conduct + 0.10 * recency))


def level_for(profile: Profile) -> Level:
    """Highest level whose points threshold AND reliability/conduct gates
    are satisfied. Points alone never confer status without standing."""
    current = LEVELS[0]
    for lv in LEVELS:
        if profile.contribution_points < lv.points_threshold:
            break
        if profile.reliability < lv.min_reliability:
            break
        if profile.conduct < lv.min_conduct:
            break
        current = lv
    return current


# ---------------------------------------------------------------------------
# Authority is never derived from reputation
# ---------------------------------------------------------------------------


def grant_authority(contributor_id: str, granted_by: str, scope: str,
                   reason: str) -> dict:
    """Authority grants are governance acts. Points, levels, and trust are
    inputs a human governor may consider, but this function takes no
    profile and computes nothing from reputation: Authority != Reputation."""
    if not granted_by or not scope:
        raise ValueError("authority requires a granter and a scope")
    return {"contributor_id": contributor_id, "granted_by": granted_by,
            "scope": scope, "reason": reason,
            "derived_from_reputation": False}
