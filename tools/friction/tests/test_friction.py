"""Tests for tools/friction — balance projection, friction tiers, watchers.

Every behavior the brief pins has a test:
  honest actor never leaves T0 - dive walks T1->T2->T3 in order -
  recovery climbs back automatically - PENDING never moves balance -
  velocity flagged at the configured threshold, one-below not flagged -
  byte-identical determinism - friction transitions appear in the events.
Plus the profile-semantics guards: reversals net out and are not
misconduct, repeat-negative needs the full count inside the window, and
emitted friction events replay neutrally (they are records, not postings).
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import balance
import cli
import friction
import watchers

BASE = datetime(2026, 10, 24, 0, 0, 0, tzinfo=timezone.utc)


def at(minutes=0, days=0):
    return (BASE + timedelta(minutes=minutes, days=days)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def E(actor, points, state="FINAL", cls="smart_note_verified", ts=None,
      eid=None, reversal_of=None):
    entry = {
        "actor": actor,
        "action_class": cls,
        "state": state,
        "points": points,
    }
    if ts is not None:
        entry["occurred_at"] = ts
    if eid is not None:
        entry["entry_id"] = eid
    if reversal_of is not None:
        entry["reversal_of"] = reversal_of
    return entry


def NEG(actor, points, ts, eid):
    return E(actor, points, cls="negative_value_action", ts=ts, eid=eid)


# --- balance projection ----------------------------------------------------


def test_levels_follow_the_profile_ladder():
    entries = [
        E("new", 0, eid="a"),
        E("emerging", 150, eid="b"),
        E("almost", 149, eid="c"),
        E("top", 75000, eid="d"),
        NEG("diver", -10, at(minutes=1), "e"),
    ]
    proj = balance.project(entries)
    assert proj["new"]["level"] == 1 and proj["new"]["level_name"] == "Member"
    assert proj["emerging"]["level"] == 2
    assert proj["emerging"]["level_name"] == "Emerging"
    assert proj["almost"]["level"] == 1
    assert proj["top"]["level"] == 10 and proj["top"]["level_name"] == "Ten-star"
    # Negative balance floors at Level 1 (the ladder names no band below 0).
    assert proj["diver"]["balance"] == -10 and proj["diver"]["level"] == 1


def test_profile_field_spellings_count_the_same():
    entries = [
        {"actor_id": "a", "posting_state": "VERIFIED_VALUE",
         "action_class": "smart_note_verified", "points": 5},
        {"actor": "a", "state": "VERIFIED",
         "action_class": "smart_note_verified", "points": 5},
        {"actor": "a", "state": "FINAL",
         "action_class": "smart_note_verified", "points": 5},
        {"actor_id": "a", "posting_state": "PENDING",
         "action_class": "smart_note_verified", "points": 500},
    ]
    assert balance.project(entries)["a"]["balance"] == 15


def test_pending_never_moves_balance():
    entries = [
        E("a", 5, eid="f1"),
        NEG("a", -35, at(minutes=1), "p1") | {"state": "PENDING"},
        E("a", 500, state="PENDING_WINDOW", ts=at(minutes=2), eid="p2"),
        E("a", 100, state="ESTIMATED", ts=at(minutes=3), eid="p3"),
        E("a", 100, state="OBSERVED", ts=at(minutes=4), eid="p4"),
    ]
    proj = balance.project(entries)
    assert proj["a"]["balance"] == 5
    states, events = friction.evaluate(entries)
    assert states["a"]["tier"] == "T0"
    assert events == []
    # A PENDING negative is not a verified negative action.
    alerts = watchers.run_watchers(
        entries, {"repeat_negative": {"min_count": 1}}
    )
    assert alerts == []


def test_reversal_nets_out_and_is_not_misconduct():
    entries = [
        E("a", 100, ts=at(minutes=0), eid="orig"),
        E("a", -100, ts=at(minutes=10), eid="rev", reversal_of="orig"),
    ]
    assert balance.project(entries)["a"]["balance"] == 0
    states, events = friction.evaluate(entries)
    assert states["a"]["tier"] == "T0" and events == []
    alerts = watchers.run_watchers(
        entries, {"repeat_negative": {"min_count": 1}}
    )
    # Not misconduct: no repeat-negative alert for a correction.
    assert [a for a in alerts if a["watcher"] == "repeat_negative"] == []
    # The fall is real, so the dive watch may report it — but the alert
    # must name it as reversal-driven, never silently as conduct.
    dives = [a for a in alerts if a["watcher"] == "balance_dive"]
    assert len(dives) == 1
    assert dives[0]["reversal_points_in_drop"] == 100
    assert dives[0]["max_drop_points"] == 100


# --- friction tiers ----------------------------------------------------------


def test_honest_actor_never_leaves_t0():
    entries = [
        E("honest", 5 + (i % 7), ts=at(minutes=i), eid=f"h{i}")
        for i in range(200)
    ]
    states, events = friction.evaluate(entries)
    assert states["honest"]["tier"] == "T0"
    assert states["honest"]["balance"] == sum(e["points"] for e in entries)
    assert events == []


def _dive_stream(actor="diver"):
    return [
        NEG(actor, -10, at(minutes=0), "d1"),    # -10  -> T1
        NEG(actor, -10, at(minutes=10), "d2"),   # -20  -> T2
        NEG(actor, -35, at(minutes=20), "d3"),   # -55  -> T3
    ]


def test_dive_walks_t1_t2_t3_in_order():
    states, events = friction.evaluate(_dive_stream())
    assert [e["to_tier"] for e in events] == ["T1", "T2", "T3"]
    assert [e["from_tier"] for e in events] == ["T0", "T1", "T2"]
    assert states["diver"]["tier"] == "T3"
    assert states["diver"]["balance"] == -55


def test_friction_transition_event_shape():
    _, events = friction.evaluate(_dive_stream())
    first = events[0]
    assert first["event_type"] == "friction_transition"
    assert first["action_class"] == "friction_transition"
    assert first["actor"] == "diver"
    assert first["balance"] == -10
    assert first["entry_id"] == "d1"
    assert first["profile"] == friction.FRICTION_PROFILE_ID


def test_recovery_climbs_back_automatically():
    entries = _dive_stream() + [
        E("diver", 20, ts=at(minutes=30), eid="r1"),  # -35 -> T2
        E("diver", 20, ts=at(minutes=40), eid="r2"),  # -15 -> T1
        E("diver", 20, ts=at(minutes=50), eid="r3"),  #   5 -> T0
    ]
    states, events = friction.evaluate(entries)
    assert [e["to_tier"] for e in events] == ["T1", "T2", "T3", "T2", "T1", "T0"]
    assert states["diver"]["tier"] == "T0"
    assert states["diver"]["balance"] == 5


def test_tier_boundaries_match_the_posting_arithmetic():
    assert friction.tier_for_balance(0) == "T0"
    assert friction.tier_for_balance(-1) == "T1"
    assert friction.tier_for_balance(-19) == "T1"
    assert friction.tier_for_balance(-20) == "T2"
    assert friction.tier_for_balance(-45) == "T2"  # worst band + light stays T2
    assert friction.tier_for_balance(-49) == "T2"
    assert friction.tier_for_balance(-50) == "T3"
    t3 = friction.tier_state(-55)
    assert t3["permitted_action_classes"] == friction.VALUE_REPAIRING_CLASSES
    assert friction.tier_state(0)["permitted_action_classes"] is None


def test_emitted_events_replay_neutrally():
    stream = _dive_stream()
    _, events = friction.evaluate(stream)
    replayed = stream + events
    assert balance.project(replayed) == balance.project(stream)
    _, events2 = friction.evaluate(replayed)
    assert events2 == events


# --- watchers ------------------------------------------------------------------


def test_velocity_flagged_above_threshold_not_at_it():
    cfg = {"velocity": {"window_seconds": 3600, "max_actions_per_window": 5}}
    five = [E("busy", 0, cls="engagement_signal", ts=at(minutes=i), eid=f"v{i}")
            for i in range(5)]
    assert watchers.velocity_alerts(five, cfg) == []
    six = five + [E("busy", 0, cls="engagement_signal", ts=at(minutes=5), eid="v5")]
    alerts = watchers.velocity_alerts(six, cfg)
    assert len(alerts) == 1
    assert alerts[0]["watcher"] == "velocity"
    assert alerts[0]["max_actions_in_window"] == 6
    assert alerts[0]["limit"] == 5


def test_repeat_negative_needs_full_count_inside_window():
    three = [
        NEG("r", -10, at(days=0), "n1"),
        NEG("r", -10, at(days=3), "n2"),
        NEG("r", -10, at(days=6), "n3"),
    ]
    alerts = watchers.repeat_negative_alerts(three)
    assert len(alerts) == 1 and alerts[0]["negative_actions_in_window"] == 3
    assert watchers.repeat_negative_alerts(three[:2]) == []
    spread = [
        NEG("s", -10, at(days=0), "s1"),
        NEG("s", -10, at(days=5), "s2"),
        NEG("s", -10, at(days=9), "s3"),  # no 7-day window holds all three
    ]
    assert watchers.repeat_negative_alerts(spread) == []


def test_balance_dive_fast_fall_flags_slow_or_shallow_does_not():
    fast = [
        NEG("f", -10, at(minutes=0), "f1"),
        NEG("f", -35, at(minutes=30), "f2"),  # -45 within the hour
    ]
    alerts = watchers.balance_dive_alerts(fast)
    assert len(alerts) == 1
    assert alerts[0]["watcher"] == "balance_dive"
    assert alerts[0]["max_drop_points"] == 45
    assert alerts[0]["reversal_points_in_drop"] == 0  # pure conduct
    slow = [
        NEG("s", -10, at(days=0), "s1"),
        NEG("s", -10, at(days=5), "s2"),
        NEG("s", -20, at(days=9), "s3"),  # deep overall, never steep in 24h
    ]
    assert watchers.balance_dive_alerts(slow) == []
    shallow = [NEG("h", -15, at(minutes=0), "h1")]  # steep but below min drop
    assert watchers.balance_dive_alerts(shallow) == []


# --- determinism + CLI ---------------------------------------------------------


def _mixed_stream():
    return (
        _dive_stream("diver")
        + [E("diver", 20, ts=at(minutes=30), eid="r1")]
        + [E("honest", 150, ts=at(minutes=1), eid="h1"),
           E("honest", 5, state="PENDING", ts=at(minutes=2), eid="h2")]
        + [NEG("rude", -20, at(minutes=3), "x1"),
           NEG("rude", -20, at(minutes=4), "x2"),
           NEG("rude", -20, at(minutes=5), "x3")]
    )


def test_render_is_byte_identical_and_order_insensitive():
    stream = _mixed_stream()
    first = cli.render(stream)
    assert cli.render(stream) == first
    assert cli.render(list(reversed(stream))) == first
    doc = json.loads(first)
    assert doc["actors"]["diver"]["tier"] == "T2"  # -55 + 20 = -35
    assert doc["actors"]["honest"]["level"] == 2
    assert any(a["watcher"] == "repeat_negative" and a["actor"] == "rude"
               for a in doc["alerts"])
    assert len(doc["friction_events"]) == 6  # diver T1,T2,T3,T2 + rude T2,T3


def test_cli_subprocess_byte_identical(tmp_path):
    stream = _mixed_stream()
    src = tmp_path / "stream.jsonl"
    src.write_text(
        "".join(json.dumps(e) + "\n" for e in stream), encoding="utf-8"
    )
    cli_path = cli.__file__
    outputs = []
    for name in ("out1.json", "out2.json"):
        out = tmp_path / name
        proc = subprocess.run(
            [sys.executable, cli_path, "--input", str(src),
             "--output", str(out)],
            capture_output=True, text=True, timeout=60,
        )
        assert proc.returncode == 0, proc.stderr
        outputs.append(out.read_bytes())
    assert outputs[0] == outputs[1]
    doc = json.loads(outputs[0])
    assert set(doc["actors"]) == {"diver", "honest", "rude"}
