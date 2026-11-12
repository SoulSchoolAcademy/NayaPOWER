"""Tests for tools/hub_sync_heartbeat.py — hub-sync heartbeat + liveness
(Balanced Machine step 4, DESIGN.ai.md §5.1).

Negative controls required by the design:
* a STALE heartbeat fixture fires the alarm;
* a MISSING heartbeat fires the alarm (silence is the failure mode);
* a FRESH heartbeat stays quiet;
* the committed seed artifact (pre-adoption, ts_epoch 0) alarms — the honest
  state until the live watcher adopts `beat`.
"""
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))
import hub_sync_heartbeat as hb


def test_beat_writes_parseable_heartbeat(tmp_path: Path):
    path = tmp_path / "hb.json"
    payload = hb.beat(path, detail="cycle 1", epoch=1_000.0)
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert on_disk == payload
    assert on_disk["ts_epoch"] == 1_000.0 and on_disk["cycle_ok"] is True


def test_fresh_heartbeat_stays_quiet_and_stale_fires():
    fresh, msg = hb.evaluate({"ts_epoch": 1_000.0}, "fixture", 600, epoch=1_599.0)
    assert fresh and "fresh" in msg
    fresh, msg = hb.evaluate({"ts_epoch": 1_000.0}, "fixture", 600, epoch=1_601.0)
    assert not fresh and "ALARM" in msg


def test_missing_heartbeat_alarms(tmp_path: Path):
    payload, why = hb.load_heartbeat(tmp_path / "nope.json", None, None)
    assert payload is None
    fresh, msg = hb.evaluate(payload, why, 600)
    assert not fresh and "ALARM" in msg


def test_cli_check_exit_codes(tmp_path: Path):
    path = tmp_path / "hb.json"
    hb.beat(path, epoch=time.time() - 10_000)  # long stale
    assert hb.main(["check", "--file", str(path)]) == 1
    hb.beat(path)  # fresh, real now
    assert hb.main(["check", "--file", str(path)]) == 0


def test_seed_artifact_alarms_until_watcher_adopts():
    seed = REPO_ROOT / "HUB" / "sync-heartbeat.json"
    payload = json.loads(seed.read_text(encoding="utf-8"))
    fresh, msg = hb.evaluate(payload, "seed artifact", hb.DEFAULT_MAX_AGE)
    assert not fresh and "ALARM" in msg
