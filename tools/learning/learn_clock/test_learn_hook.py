"""Tests for tools/learning/learn_clock/learn_hook.py — graduation F-3.

F-3 (Epsilon w141): the hook meta log ignored retroactive `--ts` —
`_meta_write()` always stamped wall-clock `now`, so bootstrap meta rows
carried mint-time while the clock JSONL carried the true retroactive
stamp. The fix: meta `ts` == the clock row's event `ts`
(`event_ts=rec["ts"]`), with `written_ts` recording the append time.

The pre-fix code fails test 1 and test 3 below: meta `ts` would be
today's wall-clock time, not the retroactive event time. These tests pin
the fix; they are the F-3 receipt.
"""

import json
from datetime import datetime, timezone

from tools.learning.learn_clock import learn_clock as lc
from tools.learning.learn_clock import learn_hook as hook


def _rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _today_prefix():
    return "LC-" + datetime.now(timezone.utc).strftime("%Y%m%d") + "-"


def test_meta_ts_equals_clock_ts_on_retroactive_ts(tmp_path):
    clock_path = tmp_path / "clock.jsonl"
    meta_path = tmp_path / "meta.jsonl"
    retro_t0 = "2026-10-12T14:02:00+00:00"
    retro_t1 = "2026-10-12T14:20:00+00:00"
    lid = _today_prefix() + "001"
    assert hook.main(
        ["t0", "--title", "retro lesson", "--evidence", "old wave log",
         "--ts", retro_t0],
        clock_path=clock_path, meta_log=meta_path) == 0
    assert hook.main(
        ["t1", lid, "--evidence", "sign-out win+why",
         "--ts", retro_t1],
        clock_path=clock_path, meta_log=meta_path) == 0
    clock_rows = _rows(clock_path)
    meta_rows = _rows(meta_path)
    assert [r["ts"] for r in clock_rows] == [retro_t0, retro_t1]
    # The F-3 pin: meta ts is the EVENT time, not the mint time.
    assert [r["ts"] for r in meta_rows] == [retro_t0, retro_t1]
    assert meta_rows[0]["lesson_id"] == lid
    assert meta_rows[0]["title"] == "retro lesson"
    assert meta_rows[1]["evidence"] == "sign-out win+why"


def test_meta_ts_equals_clock_ts_on_live_emit(tmp_path):
    clock_path = tmp_path / "clock.jsonl"
    meta_path = tmp_path / "meta.jsonl"
    assert hook.main(
        ["t0", "--title", "live lesson", "--evidence", "test went red"],
        clock_path=clock_path, meta_log=meta_path) == 0
    clock_rows = _rows(clock_path)
    meta_rows = _rows(meta_path)
    assert len(clock_rows) == len(meta_rows) == 1
    assert meta_rows[0]["ts"] == clock_rows[0]["ts"]


def test_meta_written_ts_records_append_time_not_event_time(tmp_path):
    # Retroactive rows must keep mint-time visible separately: `ts` is the
    # event, `written_ts` is the append. Pre-fix code had no `written_ts`
    # distinction at all (ts == write time).
    clock_path = tmp_path / "clock.jsonl"
    meta_path = tmp_path / "meta.jsonl"
    retro = "2026-10-12T14:02:00+00:00"
    assert hook.main(
        ["t0", "--title", "retro", "--evidence", "old log",
         "--ts", retro],
        clock_path=clock_path, meta_log=meta_path) == 0
    meta = _rows(meta_path)[0]
    assert meta["ts"] == retro
    assert datetime.fromisoformat(meta["written_ts"]) > datetime.fromisoformat(retro)


def test_default_log_points_at_repo_path_not_scratch():
    assert str(lc.DEFAULT_LOG).endswith(
        "BRAIN/07-LEARNING/learn-clock/learn-clock.jsonl")
    # The scratch instrument home, not any checkout dir that happens to
    # sit under a _scratch parent (e.g. this worktree).
    assert "_scratch/learn-clock" not in str(lc.DEFAULT_LOG)


def test_meta_log_points_at_repo_path_not_scratch():
    assert str(hook.META_LOG).endswith(
        "BRAIN/07-LEARNING/learn-clock/learn-lessons.jsonl")
    assert "_scratch/learn-clock" not in str(hook.META_LOG)


def test_hook_rejects_missing_evidence(tmp_path):
    # Fail-closed survives the carry: --evidence is REQUIRED.
    import pytest
    with pytest.raises(SystemExit) as exc:
        hook.main(["t0", "--title", "no evidence"],
                  clock_path=tmp_path / "c.jsonl",
                  meta_log=tmp_path / "m.jsonl")
    assert exc.value.code == 2


def test_hook_t0_mints_sequential_ids(tmp_path):
    clock_path = tmp_path / "clock.jsonl"
    meta_path = tmp_path / "meta.jsonl"
    prefix = _today_prefix()
    for _ in range(2):
        assert hook.main(
            ["t0", "--title", "seq", "--evidence", "e"],
            clock_path=clock_path, meta_log=meta_path) == 0
    assert [r["lesson_id"] for r in _rows(clock_path)] == [
        prefix + "001", prefix + "002"]
