#!/usr/bin/env python3
"""watchers.py — product watchers v1: pattern signals over the ledger stream.

SN-1855 names three watchers — velocity, pattern, verified_balance_dive —
and the 2026-10-24 census found none of them exists for citizens: every
watcher in the system watches the build, never the people in it. This
module is the product side, v1. It implements:

  (a) velocity        — an actor's action rate inside a sliding window
                        beyond a configured limit;
  (b) balance_dive    — the verified balance falling faster than a
                        configured slope (with a minimum drop, so a slow
                        shallow slide is not a dive);
  (c) repeat_negative — N verified-negative actions inside a window
                        (the "pattern" watcher of SN-1855, v1 form).

Alerts are DATA: plain dicts returned to the caller. This module has no
side effects — posting, mailing, or paging anyone is the caller's job
(WIRING.md). Watchers are advisory signals and evidence; the friction
tiers in friction.py are the automatic consequence, and they key off the
balance alone, never off an alert, so an alert can never punish anyone.

Semantics, pinned:
  - Velocity counts EVERY stream entry for the actor (any posting state):
    rate abuse does not wait for verification. The window anchored at an
    entry t is [t, t + window_seconds); an alert fires when the fullest
    such window holds MORE than max_actions_per_window entries.
  - Balance-dive walks counting entries only, in canonical order, over
    the TRUE balance path — reversals included, because a reversed
    credit really is gone (profile section 3: balance recomputes from
    FINAL entries). To keep correction distinguishable from conduct,
    the alert reports `reversal_points_in_drop`: how much of the
    winning pair's drop was reversal-driven. And it includes the
    implicit zero balance at the first entry's timestamp (a single
    worst-band posting is a dive from standing). Slope uses a
    minimum elapsed of 60 seconds so same-timestamp falls stay finite.
    An alert fires when some pair within window_hours drops at least
    min_drop_points with slope above the configured threshold; the
    reported pair is the steepest (ties: largest drop, then earliest).
  - Repeat-negative counts verified negative actions only
    (balance.is_verified_negative: FINAL, points < 0, not a reversal) —
    a reversal of the actor's own earlier credit is a correction, not
    misconduct, and never counts. An alert fires when some window holds
    AT LEAST min_count of them.
  - Entries without a parseable timestamp are invisible to all three
    watchers (they still count toward balance, which is not time-based).
"""

try:  # package import (tools.friction.watchers)
    from . import balance as _balance
except ImportError:  # direct script / flat sys.path use
    import balance as _balance

WATCHER_PROFILE_ID = "watchers-v1"

# --- CONFIG (versioned; adjust here, never inline) -------------------------
WATCHER_CONFIG = {
    "velocity": {
        "window_seconds": 3600,
        "max_actions_per_window": 120,
    },
    "balance_dive": {
        "window_hours": 24,
        "min_drop_points": 20,
        "slope_points_per_hour": 35.0,
        "min_elapsed_seconds": 60,
    },
    "repeat_negative": {
        "window_seconds": 7 * 24 * 3600,
        "min_count": 3,
    },
}


def _merged_config(config):
    merged = {name: dict(cfg) for name, cfg in WATCHER_CONFIG.items()}
    if config:
        for name, cfg in config.items():
            if name in merged and isinstance(cfg, dict):
                merged[name].update(cfg)
    return merged


def _fullest_window(timed_entries, window_seconds):
    """(max_count, anchor_entry) over windows [t, t+window) anchored at entries.

    timed_entries: normalized entries, all with ts set, any order.
    Ties keep the earliest anchor. Returns (0, None) for an empty list.
    """
    ordered = sorted(timed_entries, key=lambda e: (e["ts"], e["entry_id"] or ""))
    best_count, best_anchor = 0, None
    n = len(ordered)
    j = 0
    for i in range(n):
        if j < i:
            j = i
        limit = ordered[i]["ts"] + window_seconds
        while j < n and ordered[j]["ts"] < limit:
            j += 1
        count = j - i
        if count > best_count:
            best_count, best_anchor = count, ordered[i]
    return best_count, best_anchor


def velocity_alerts(entries, config=None):
    """One alert per actor whose fullest window exceeds the rate limit."""
    cfg = _merged_config(config)["velocity"]
    by_actor = {}
    for raw in entries:
        entry = _balance.normalize(raw)
        if entry["actor"] is None or entry["ts"] is None:
            continue
        by_actor.setdefault(entry["actor"], []).append(entry)
    alerts = []
    for actor in sorted(by_actor, key=str):
        count, anchor = _fullest_window(by_actor[actor], cfg["window_seconds"])
        if count > cfg["max_actions_per_window"]:
            alerts.append(
                {
                    "watcher": "velocity",
                    "actor": actor,
                    "window_seconds": cfg["window_seconds"],
                    "max_actions_in_window": count,
                    "limit": cfg["max_actions_per_window"],
                    "window_start": anchor["occurred_at"],
                    "profile": WATCHER_PROFILE_ID,
                }
            )
    return alerts


def balance_dive_alerts(entries, config=None):
    """One alert per actor whose verified balance dives past the slope."""
    cfg = _merged_config(config)["balance_dive"]
    window_seconds = cfg["window_hours"] * 3600
    actors = set()
    for raw in entries:
        actor = _balance.normalize(raw)["actor"]
        if actor is not None:
            actors.add(actor)
    alerts = []
    for actor in sorted(actors, key=str):
        timeline = [
            (entry, bal)
            for entry, bal in _balance.running_balances(entries, actor)
            if entry["ts"] is not None
        ]
        if not timeline:
            continue
        # (ts, balance) points, opening with the implicit zero at the
        # first entry's timestamp: standing before the fall.
        points = [(timeline[0][0]["ts"], 0)] + [
            (entry["ts"], bal) for entry, bal in timeline
        ]
        raws = [timeline[0][0]["occurred_at"]] + [
            entry["occurred_at"] for entry, _ in timeline
        ]
        best = None  # (slope, drop, -t_i, -t_j, i, j, reversal_points)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                elapsed = points[j][0] - points[i][0]
                if elapsed > window_seconds:
                    break
                drop = points[i][1] - points[j][1]
                if drop < cfg["min_drop_points"]:
                    continue
                hours = max(elapsed, cfg["min_elapsed_seconds"]) / 3600.0
                slope = drop / hours
                if slope <= cfg["slope_points_per_hour"]:
                    continue
                # Points of this drop posted by reversal entries in the
                # span (timeline entries i..j-1 feed points i+1..j):
                # correction made visible, never silently conduct.
                reversal_points = sum(
                    -timeline[k][0]["points"]
                    for k in range(i, j)
                    if timeline[k][0]["reversal_of"]
                )
                candidate = (
                    slope, drop, -points[i][0], -points[j][0], i, j,
                    reversal_points,
                )
                if best is None or candidate[:6] > best[:6]:
                    best = candidate
        if best is not None:
            slope, drop, _, _, i, j, reversal_points = best
            alerts.append(
                {
                    "watcher": "balance_dive",
                    "actor": actor,
                    "window_hours": cfg["window_hours"],
                    "max_drop_points": drop,
                    "slope_points_per_hour": round(slope, 6),
                    "slope_threshold_points_per_hour": cfg[
                        "slope_points_per_hour"
                    ],
                    "min_drop_points": cfg["min_drop_points"],
                    "from_balance": points[i][1],
                    "to_balance": points[j][1],
                    "reversal_points_in_drop": reversal_points,
                    "from_at": raws[i],
                    "to_at": raws[j],
                    "profile": WATCHER_PROFILE_ID,
                }
            )
    return alerts


def repeat_negative_alerts(entries, config=None):
    """One alert per actor with >= min_count verified negatives in a window."""
    cfg = _merged_config(config)["repeat_negative"]
    by_actor = {}
    for raw in entries:
        entry = _balance.normalize(raw)
        if entry["actor"] is None or entry["ts"] is None:
            continue
        if _balance.is_verified_negative(entry):
            by_actor.setdefault(entry["actor"], []).append(entry)
    alerts = []
    for actor in sorted(by_actor, key=str):
        count, anchor = _fullest_window(by_actor[actor], cfg["window_seconds"])
        if count >= cfg["min_count"]:
            alerts.append(
                {
                    "watcher": "repeat_negative",
                    "actor": actor,
                    "window_seconds": cfg["window_seconds"],
                    "negative_actions_in_window": count,
                    "threshold": cfg["min_count"],
                    "window_start": anchor["occurred_at"],
                    "profile": WATCHER_PROFILE_ID,
                }
            )
    return alerts


def run_watchers(entries, config=None):
    """All alerts, sorted by (watcher, actor). Pure function of the stream."""
    entries = list(entries)
    alerts = (
        velocity_alerts(entries, config)
        + balance_dive_alerts(entries, config)
        + repeat_negative_alerts(entries, config)
    )
    alerts.sort(key=lambda a: (a["watcher"], str(a["actor"])))
    return alerts
