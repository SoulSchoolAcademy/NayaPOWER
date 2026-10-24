#!/usr/bin/env python3
"""friction.py — automatic friction tiers driven by the verified balance.

This is the missing third leg of SN-1855 ("Security Is Light"): the census
(2026-10-24) scored automatic friction 0 YES / 0 PARTIAL / 9 NO across every
surface. SN-1855's rule — "a profile whose verified balance dives gets
tighter limits and more verification, and reopens as the record recovers —
consequences by math, never bans by opinion" — is implemented here as a
pure function of the ledger stream. This module *decides*; surfaces enforce
(see WIRING.md). It ships dark: nothing in production calls it yet.

TIER DESIGN — thresholds are anchored to the points profile's own posting
arithmetic, not invented. The negative class (`negative_value_action`,
director's ruling 2026-10-24) posts in exactly three sizes: B1 -10,
B2 -20, B3 -35 (bands of verified harm, symmetric to
`problem_solved_verified`). The tier floors are chosen against those sizes:

  T0 normal        balance >= 0
      Zero is the profile's bright line: honest verified earnings are
      final, and a brand-new citizen (Part #19, level 1) sits at 0 by
      definition. Any floor above 0 would punish newcomers, so T0 must
      include 0 and everything above it. No friction at all.
  T1 watch         -19 .. -1
      Entered by a single light verified negative posting (one B1, -10)
      or any shallow verified deficit. The mildest possible response:
      sensitive actions require extra verification; nothing is limited.
  T2 restricted    -49 .. -20
      -20 is exactly one mid-band posting (B2) from standing, or two
      light ones — the point where a *pattern*, not an incident, is
      established. Rate limits tighten (x0.5) and sensitive actions are
      held for review instead of merely re-verified.
  T3 recovery-only balance <= -50
      -50 exceeds any single posting (max -35) and any worst-band +
      light combination (-35 + -10 = -45 stays in T2). Reaching T3
      requires either sustained verified harm (three or more postings)
      or two mid/worst-band postings (-35 + -20 = -55). At that depth
      the only permitted actions are value-repairing ones — the positive
      contribution classes of the profile — until the record recovers.

Transitions are automatic in BOTH directions: the tier is recomputed from
the running verified balance after every counting entry, and climbing out
is exactly as mechanical as falling in (SN-1855: friction "reopens as the
record recovers"). Every transition emits a ledger-shaped event
(action_class "friction_transition") so the friction decision itself lands
on the record it governs; balance.py refuses to count those events as
postings, so replaying the full stream cannot double-apply a decision.

There are no bans and no opinions in this module: no identity lists, no
manual overrides, no irreversible states. Thresholds are CONFIG below —
a versioned profile (FRICTION_PROFILE_ID), adjustable through the same
recalibration discipline as the points profile, never mutated silently.
"""

try:  # package import (tools.friction.friction)
    from . import balance as _balance
except ImportError:  # direct script / flat sys.path use
    import balance as _balance

FRICTION_PROFILE_ID = "friction-profile-v1"

# --- CONFIG (versioned profile; adjust here, never inline) -----------------
# Minimum verified balance per tier. T3 is everything below T2's floor.
TIER_FLOORS = {"T0": 0, "T1": -19, "T2": -49}
TIER_ORDER = ("T0", "T1", "T2", "T3")

# The profile's positive contribution classes — the actions that can
# produce verified positive value, and therefore the only ones permitted
# at T3 ("value-repairing"). engagement_signal is excluded (it posts
# nothing and repairs nothing); negative_value_action is a posting against
# an actor, not an action an actor takes.
VALUE_REPAIRING_CLASSES = (
    "smart_note_verified",
    "space_created_verified",
    "note_verified_by_another",
    "note_reused_downstream",
    "problem_solved_verified",
    "lesson_changed_decision",
    "connection_formed_via_match",
    "verification_work_performed",
    "correction_prevented_error",
    "citizen_helped_verified_outcome",
    "ambassador_attributed_join",
)

# Per-tier limits data. This module decides tiers; surfaces read these
# fields and enforce them in their own write path (WIRING.md).
TIERS = {
    "T0": {
        "tier": "T0",
        "name": "normal",
        "rate_multiplier": 1.0,
        "extra_verification_required": False,
        "sensitive_actions": "allowed",
        "held_for_review": False,
        "permitted_action_classes": None,  # None = all actions
    },
    "T1": {
        "tier": "T1",
        "name": "watch",
        "rate_multiplier": 1.0,
        "extra_verification_required": True,
        "sensitive_actions": "extra_verification",
        "held_for_review": False,
        "permitted_action_classes": None,
    },
    "T2": {
        "tier": "T2",
        "name": "restricted",
        "rate_multiplier": 0.5,
        "extra_verification_required": True,
        "sensitive_actions": "held_for_review",
        "held_for_review": True,
        "permitted_action_classes": None,
    },
    "T3": {
        "tier": "T3",
        "name": "recovery-only",
        "rate_multiplier": 0.25,
        "extra_verification_required": True,
        "sensitive_actions": "held_for_review",
        "held_for_review": True,
        "permitted_action_classes": VALUE_REPAIRING_CLASSES,
    },
}


def tier_for_balance(balance):
    """The tier id for a verified balance, per TIER_FLOORS."""
    for tier in TIER_ORDER[:-1]:
        if balance >= TIER_FLOORS[tier]:
            return tier
    return "T3"


def tier_state(balance):
    """The full limits dict for a verified balance (a fresh copy)."""
    state = dict(TIERS[tier_for_balance(balance)])
    state["balance"] = balance
    return state


def evaluate_actor(entries, actor):
    """(final_state, transition_events) for one actor.

    Walks the actor's counting entries in canonical order, recomputing
    the tier after each; every change of tier — down or up — emits one
    ledger-shaped transition event naming the entry that caused it.
    """
    state = tier_state(0)
    current = "T0"
    events = []
    for entry, balance_after in _balance.running_balances(entries, actor):
        new_tier = tier_for_balance(balance_after)
        if new_tier != current:
            events.append(
                {
                    "event_type": "friction_transition",
                    "action_class": "friction_transition",
                    "actor": actor,
                    "from_tier": current,
                    "to_tier": new_tier,
                    "balance": balance_after,
                    "entry_id": entry["entry_id"],
                    "occurred_at": entry["occurred_at"],
                    "profile": FRICTION_PROFILE_ID,
                }
            )
            current = new_tier
        state = tier_state(balance_after)
    state["actor"] = actor
    return state, events


def evaluate(entries):
    """({actor: tier_state}, [all transition events]) for a whole stream.

    Actors are processed in sorted order so the event list is
    deterministic for a given stream.
    """
    entries = list(entries)
    actors = set()
    for raw in entries:
        actor = _balance.normalize(raw)["actor"]
        if actor is not None:
            actors.add(actor)
    states = {}
    events = []
    for actor in sorted(actors, key=str):
        state, actor_events = evaluate_actor(entries, actor)
        states[actor] = state
        events.extend(actor_events)
    return states, events
