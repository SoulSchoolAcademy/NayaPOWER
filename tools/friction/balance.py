#!/usr/bin/env python3
"""balance.py — the verified-balance projection over the Smart Ledger point stream.

This module is the read side of the points profile (`points-profile-v1`):
it consumes ledger-shaped CONTRIBUTION_VALUE entries (the profile's §7
dashboard contract) and projects each actor's *verified balance* and *level*.
It never re-derives awards, CVS, or decay — those are computed upstream by
the profile derivation rule (profile §2) and posted onto the entry as
`points`. This projection trusts the posted points and applies exactly one
filter, the profile's posting state machine (profile §3):

  - an entry counts toward balance iff its posting state is FINAL
    (evidence VERIFIED / assessment VERIFIED_VALUE);
  - PENDING and PENDING_WINDOW postings never count;
  - ESTIMATED / OBSERVED evidence posts nothing countable;
  - a reversal is a separate FINAL entry with negative points and
    `reversal_of` naming the original entry (profile §3: the original is
    never edited or deleted), so it cancels its target arithmetically.

Levels are a pure function of the lifetime FINAL balance (profile §6,
director's ruling 2026-10-24: derived levels stand, in both directions).

Entry field spellings: both the profile contract (`actor_id`,
`posting_state`) and the short form (`actor`, `state`) are accepted.
Counting state names after normalization: FINAL, VERIFIED, VERIFIED_VALUE.

Determinism: the projection is a pure function of the entry stream. Sums
are order-free; where a sequence is needed (running balances), entries are
processed in the canonical order defined here: timestamp ascending,
then entry_id, then original stream position. Entries without a parseable
timestamp still count toward balance (balance is not time-based) and sort
after timestamped ones; the time-windowed consumers (watchers) skip them.

Ambiguity resolved here, stated once: the profile ladder starts at 0
(Level 1, Member) and names no band below it, so a negative balance floors
at Level 1 "Member". Friction tiers (friction.py) key off the balance
directly, so this floor affects only the displayed level.
"""

from datetime import datetime, timezone

POINTS_PROFILE_ID = "points-profile-v1"

# Posting states that put points into the verified balance (profile §3).
COUNTING_STATES = frozenset({"FINAL", "VERIFIED", "VERIFIED_VALUE"})

# Our own emitted decision records (friction.py) must never feed back into
# the balance if a caller replays the full stream; they carry no points.
NON_POSTING_CLASSES = frozenset({"friction_transition"})

# Profile §6 ladder: (lifetime FINAL threshold, level, name).
LADDER = (
    (0, 1, "Member"),
    (150, 2, "Emerging"),
    (1500, 3, "Developing"),
    (5000, 4, "Advancing"),
    (15000, 5, "Mastering"),
    (20500, 6, "Six-star"),
    (28500, 7, "Seven-star"),
    (39500, 8, "Eight-star"),
    (54500, 9, "Nine-star"),
    (75000, 10, "Ten-star"),
)


def parse_time(value):
    """Parse an ISO-8601 timestamp to epoch seconds (float), or None.

    Naive timestamps are read as UTC. Anything unparseable returns None —
    callers treat None as "no known time", never as an error.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def normalize(entry):
    """Normalize one ledger-shaped entry dict to the projection's shape.

    Returns a new dict; the input is never mutated. Unknown keys are
    ignored. `points` defaults to 0 and is coerced to int.
    """
    actor = entry.get("actor", entry.get("actor_id"))
    state = entry.get("state", entry.get("posting_state", ""))
    occurred_raw = entry.get("occurred_at", entry.get("ts", entry.get("timestamp")))
    points = entry.get("points", 0)
    try:
        points = int(points)
    except (TypeError, ValueError):
        points = 0
    return {
        "actor": actor,
        "action_class": entry.get("action_class", ""),
        "state": str(state).strip().upper(),
        "points": points,
        "entry_id": entry.get("entry_id", entry.get("id")),
        "reversal_of": entry.get("reversal_of"),
        "occurred_at": occurred_raw,
        "ts": parse_time(occurred_raw),
    }


def counts_toward_balance(norm_entry):
    """True iff a normalized entry moves the verified balance."""
    return (
        norm_entry["state"] in COUNTING_STATES
        and norm_entry["action_class"] not in NON_POSTING_CLASSES
    )


def is_verified_negative(norm_entry):
    """True iff a normalized entry is a verified negative-value action.

    A reversal (reversal_of set) is a correction of a prior credit, not a
    negative action by the actor, and never counts here. Under the
    profile, only the `negative_value_action` class can produce a
    non-reversal negative FINAL posting.
    """
    return (
        counts_toward_balance(norm_entry)
        and norm_entry["points"] < 0
        and not norm_entry["reversal_of"]
    )


def canonical_order(norm_entries):
    """Sort normalized entries into the one canonical processing order."""
    indexed = list(enumerate(norm_entries))
    indexed.sort(
        key=lambda pair: (
            pair[1]["ts"] is None,
            pair[1]["ts"] if pair[1]["ts"] is not None else 0.0,
            pair[1]["entry_id"] if pair[1]["entry_id"] is not None else "",
            pair[0],
        )
    )
    return [entry for _, entry in indexed]


def level_for_balance(balance):
    """(level, name) for a lifetime FINAL balance, per the profile ladder."""
    level, name = LADDER[0][1], LADDER[0][2]
    for threshold, lvl, nm in LADDER:
        if balance >= threshold:
            level, name = lvl, nm
        else:
            break
    return level, name


def project(entries):
    """Project the full stream: {actor: {balance, level, level_name, ...}}.

    Every actor seen in the stream appears, even if nothing they posted
    counts (balance 0). Pure function of the input.
    """
    actors = {}
    for raw in entries:
        entry = normalize(raw)
        actor = entry["actor"]
        if actor is None:
            continue
        slot = actors.setdefault(
            actor, {"balance": 0, "counted_entries": 0, "pending_entries": 0}
        )
        if counts_toward_balance(entry):
            slot["balance"] += entry["points"]
            slot["counted_entries"] += 1
        elif entry["state"].startswith("PENDING"):
            slot["pending_entries"] += 1
    out = {}
    for actor in sorted(actors, key=str):
        slot = actors[actor]
        level, name = level_for_balance(slot["balance"])
        out[actor] = {
            "balance": slot["balance"],
            "level": level,
            "level_name": name,
            "counted_entries": slot["counted_entries"],
            "pending_entries": slot["pending_entries"],
        }
    return out


def running_balances(entries, actor):
    """[(norm_entry, balance_after)] for one actor, canonical order.

    Only counting entries appear — this is the timeline friction and the
    balance-dive watcher walk.
    """
    mine = []
    for raw in entries:
        entry = normalize(raw)
        if entry["actor"] == actor and counts_toward_balance(entry):
            mine.append(entry)
    out = []
    balance = 0
    for entry in canonical_order(mine):
        balance += entry["points"]
        out.append((entry, balance))
    return out
