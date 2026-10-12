"""Tests for baseline.py — the pinned human-value baseline snapshot.

The baseline is the instrument's honesty made re-runnable: every number traces
to a ledger record, every ledger record traces to evidence. These tests prove
the snapshot machinery, not any human's experience (all fixtures synthetic).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

BASELINE_PY = REPO_ROOT / "tools" / "human_value" / "baseline.py"


def run_baseline(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BASELINE_PY), *argv],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )


def write_ledger(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def good_event_v2(event_id: str, value_type: str = "useful_outcome",
                  units: int = 1, kind: str = "stated") -> dict:
    return {
        "schema_version": "2",
        "event_id": event_id,
        "recorded_at": "2026-10-12",
        "value_type": value_type,
        "value_units": units,
        "unit_description": f"test: {units} counted thing(s)",
        "evidence": [{"kind": "content_hash", "ref": "sha256:" + "cd" * 32}],
        "observation_kind": kind,
        "subject": "human_self",
        "observed_by": "naya-epsilon",
        "observed_at": "2026-10-12T06:00:00Z",
        "collected_at": "2026-10-12T07:00:00Z",
        "verbatim_hash": "sha256:" + "ab" * 32,
        "authorship": "direct",
        "collector_inference": "test inference",
        "promotion": None,
    }


def good_candidate(cid: str, status: str = "pending") -> dict:
    return {
        "schema_version": "1",
        "candidate_id": cid,
        "graded_value_type": "useful_outcome",
        "graded_units": 7.5,
        "graded_by": "naya-epsilon",
        "graded_at": "2026-10-12T04:00:00+00:00",
        "expires_at": "2026-11-02T04:00:00+00:00",
        "status": status,
    }


def good_sweep(sweep_id: str = "SWEEP-TEST-001") -> dict:
    return {
        "sweep_id": sweep_id,
        "swept_at": "2026-10-12T08:00:00+00:00",
        "watermark_start": "2026-10-07T00:00:00+00:00",
        "watermark_end": "2026-10-12T08:00:00+00:00",
        "channels": ["c1", "c2", "c3"],
        "observations_found": 2,
        "promotions_proposed": 2,
        "null_sweep": False,
        "collector": "naya-epsilon",
    }


@pytest.fixture()
def ledgers(tmp_path: Path) -> Path:
    d = tmp_path / "ledgers"
    d.mkdir()
    write_ledger(d / "observed-events.jsonl", [
        good_event_v2("OBS-T-001", "useful_outcome", 2),
        good_event_v2("OBS-T-002", "attention_demanded", 1, "corrected"),
    ])
    write_ledger(d / "pending-candidates.jsonl", [
        good_candidate("CAND-T-001", "pending"),
        good_candidate("CAND-T-002", "unobserved"),
    ])
    write_ledger(d / "observation-sweeps.jsonl", [good_sweep()])
    return d


def test_baseline_counts_match_ledgers(ledgers: Path, tmp_path: Path):
    out = tmp_path / "baseline.json"
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00")
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    assert b["observed"]["units_by_value_type"] == {"useful_outcome": 2, "attention_demanded": 1}
    assert b["observed"]["event_count"] == 2
    assert b["candidates"]["pending"] == 1
    assert b["candidates"]["unobserved"] == 1
    assert b["candidates"]["pending_ids"] == ["CAND-T-001"]
    assert b["window"]["start"] == "2026-10-07T00:00:00+00:00"
    assert b["window"]["end"] == "2026-10-12T08:00:00+00:00"


def test_baseline_empty_ledgers_is_honest_zeros(tmp_path: Path):
    ledgers = tmp_path / "ledgers"
    ledgers.mkdir()
    for name in ("observed-events.jsonl", "pending-candidates.jsonl", "observation-sweeps.jsonl"):
        (ledgers / name).write_text("")
    out = tmp_path / "baseline.json"
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00")
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    assert b["observed"]["units_by_value_type"] == {}
    assert b["observed"]["event_count"] == 0
    assert b["candidates"]["pending"] == 0
    # Silence is reported as silence, not hidden: the banner still says FORMATIVE.
    assert b["method"]["calibration_banner"].startswith("FORMATIVE")


def test_baseline_banner_calibrated_when_all_checks_pass(ledgers: Path, tmp_path: Path):
    out = tmp_path / "baseline.json"
    status = tmp_path / "status.json"
    status.write_text(json.dumps({"known_answer": "pass", "two_seat_agreement": "pass",
                                  "adversarial_review": "pass"}))
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00",
                     "--calibration-status", str(status))
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    assert b["method"]["calibration_banner"].startswith("CALIBRATED")


def test_baseline_banner_names_pending_check(ledgers: Path, tmp_path: Path):
    out = tmp_path / "baseline.json"
    status = tmp_path / "status.json"
    status.write_text(json.dumps({"known_answer": "pass",
                                  "two_seat_agreement": "provisional-pass",
                                  "adversarial_review": "pass"}))
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00",
                     "--calibration-status", str(status))
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    assert "two_seat_agreement" in b["method"]["calibration_banner"]
    assert b["method"]["calibration_banner"].startswith("FORMATIVE")


def test_baseline_carries_open_questions_and_honesty_notes(ledgers: Path, tmp_path: Path):
    out = tmp_path / "baseline.json"
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00")
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    assert len(b["open_questions"]) >= 1
    assert all("question" in q and "owner" in q for q in b["open_questions"])
    assert any("UNOBSERVED is not zero value" in n for n in b["honesty_notes"])


def test_baseline_fail_closed_on_corrupt_ledger(tmp_path: Path):
    ledgers = tmp_path / "ledgers"
    ledgers.mkdir()
    (ledgers / "observed-events.jsonl").write_text("{not json\n")
    (ledgers / "pending-candidates.jsonl").write_text("")
    (ledgers / "observation-sweeps.jsonl").write_text("")
    out = tmp_path / "baseline.json"
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00")
    assert r.returncode != 0, "corrupt ledger must fail closed, not produce a baseline"
    assert not out.exists() or out.read_text().strip() == ""


def test_baseline_events_carry_verbatim_hashes(ledgers: Path, tmp_path: Path):
    out = tmp_path / "baseline.json"
    r = run_baseline("--ledgers", str(ledgers), "--out", str(out),
                     "--as-of", "2026-10-12T08:00:00+00:00")
    assert r.returncode == 0, r.stderr
    b = json.loads(out.read_text())
    for e in b["observed"]["events"]:
        assert e["verbatim_hash"].startswith("sha256:")
        assert len(e["verbatim_hash"]) == 7 + 64
