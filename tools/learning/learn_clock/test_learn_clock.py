"""Battery for the learn-clock (2026-10-14).

The clock is the measurement behind "near-instant": every one of these
must hold, or learning latency is a story, not a number.

Carried verbatim from scratch in graduation F-3, except the import
moved to the repo home and `test_module_level_api` imports the repo
module instead of a top-level `learn_clock`; the 16 test bodies are
unchanged.
"""

from datetime import datetime, timedelta, timezone

from tools.learning.learn_clock.learn_clock import (
    LearnClock, OutOfOrderError, STAGES, N_STAGES,
    meets_target as _unused)  # noqa: F401  (module API exists)

BASE = datetime(2026, 10, 14, 3, 0, tzinfo=timezone.utc)


def iso(dt):
    return dt.isoformat()


def full_lesson(clock, lid, t0=BASE, span_min=45):
    """Drive T0..T6 with evenly spaced timestamps over span_min."""
    step = timedelta(minutes=span_min / 6)
    for s in range(7):
        clock.emit(lid, s, ts=iso(t0 + step * s))
    return t0


def test_full_lifecycle_measures_known_latency(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    full_lesson(c, "L1", span_min=45)
    assert c.latency("L1") == 45.0


def test_latency_none_before_t6(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE))
    c.emit("L1", 1, ts=iso(BASE + timedelta(minutes=5)))
    assert c.latency("L1") is None
    assert c.meets_target("L1") is False  # fail-closed: no claim without T6


def test_out_of_order_rejected(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE))
    try:
        c.emit("L1", 2, ts=iso(BASE + timedelta(minutes=5)))
    except OutOfOrderError as e:
        assert "T1_CAPTURED" in str(e) and "T2_TRIAGED" in str(e)
    else:
        raise AssertionError("skipped stage was accepted")


def test_duplicate_stage_rejected(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE))
    try:
        c.emit("L1", 0, ts=iso(BASE + timedelta(minutes=1)))
    except OutOfOrderError:
        pass
    else:
        raise AssertionError("duplicate stage was accepted")


def test_timestamp_regression_rejected(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE + timedelta(minutes=10)))
    try:
        c.emit("L1", 1, ts=iso(BASE))
    except OutOfOrderError as e:
        assert "regressed" in str(e)
    else:
        raise AssertionError("regressed timestamp was accepted")


def test_bad_stage_rejected(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    for bad in (-1, 8, "T0", None):
        try:
            c.emit("L1", bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"bad stage {bad!r} was accepted")


def test_incomplete_lesson_flags_missing(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE))
    c.emit("L1", 1, ts=iso(BASE + timedelta(minutes=2)))
    st = c.status("L1")
    assert st["hit"] == ["T0_EVENT", "T1_CAPTURED"]
    assert st["missing"] == [STAGES[s] for s in range(2, N_STAGES)]
    assert st["complete_through"] == "T1_CAPTURED"


def test_status_unknown_lesson(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    st = c.status("NOPE")
    assert st["hit"] == [] and st["complete_through"] is None
    assert len(st["missing"]) == N_STAGES


def test_meets_target_true_and_false(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    full_lesson(c, "FAST", span_min=45)
    full_lesson(c, "SLOW", span_min=75)
    assert c.meets_target("FAST") is True
    assert c.meets_target("FAST", minutes=30) is False
    assert c.meets_target("SLOW") is False          # 75 > default 60
    assert c.meets_target("SLOW", minutes=90) is True


def test_concurrent_lessons_dont_interleave(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    t = BASE
    for s in range(7):  # interleave A and B stage by stage
        c.emit("A", s, ts=iso(t))
        c.emit("B", s, ts=iso(t + timedelta(seconds=30)))
        t += timedelta(minutes=10)
    assert c.latency("A") == 60.0
    assert c.latency("B") == 60.0
    assert c.status("A")["missing"] == ["T7_COMPOUNDED"]
    assert c.status("B")["missing"] == ["T7_COMPOUNDED"]
    assert c.meets_target("A") is True and c.meets_target("B") is True


def test_retroactive_bootstrap(tmp_path):
    """The spec's bootstrap: reconstruct T0..T6 from evidence after the fact."""
    c = LearnClock(tmp_path / "lc.jsonl")
    t0 = BASE - timedelta(hours=5)
    for s, gap in enumerate([0, 12, 40, 90, 150, 200, 260]):  # minutes after T0
        c.emit("OLD", s, ts=iso(t0 + timedelta(minutes=gap)))
    assert c.latency("OLD") == 260.0
    assert c.meets_target("OLD") is False  # hours, not minutes: baseline honesty


def test_secondary_lags(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    t = BASE
    gaps = [0, 5, 10, 20, 35, 50, 58]  # T0..T6
    for s, g in enumerate(gaps):
        c.emit("L1", s, ts=iso(t + timedelta(minutes=g)))
    lags = c.lags("L1")
    assert lags["capture_lag"] == 5.0
    assert lags["injection_lag"] == 15.0
    assert lags["verification_lag"] == 8.0


def test_lags_none_when_unmeasurable(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    c.emit("L1", 0, ts=iso(BASE))
    lags = c.lags("L1")
    assert lags == {"capture_lag": None, "injection_lag": None,
                    "verification_lag": None}


def test_t7_extends_beyond_latency(tmp_path):
    """T7 is recorded but never moves the latency number (latency = T6 − T0)."""
    c = LearnClock(tmp_path / "lc.jsonl")
    full_lesson(c, "L1", span_min=45)
    c.emit("L1", 7, ts=iso(BASE + timedelta(minutes=120)))
    assert c.latency("L1") == 45.0
    assert c.status("L1")["missing"] == []
    assert c.status("L1")["complete_through"] == "T7_COMPOUNDED"


def test_emit_returns_receipt(tmp_path):
    c = LearnClock(tmp_path / "lc.jsonl")
    for s in range(3):
        c.emit("L1", s)
    r = c.emit("L1", 3)
    assert r["lesson_id"] == "L1" and r["stage"] == 3
    assert r["stage_name"] == "T3_DISTILLED" and "ts" in r


def test_module_level_api(tmp_path, monkeypatch):
    from tools.learning.learn_clock import learn_clock
    monkeypatch.setattr(learn_clock, "_default", LearnClock(tmp_path / "m.jsonl"))
    learn_clock.emit("M", 0, ts=iso(BASE))
    assert learn_clock.status("M")["complete_through"] == "T0_EVENT"
    assert learn_clock.latency("M") is None
    assert learn_clock.meets_target("M") is False
