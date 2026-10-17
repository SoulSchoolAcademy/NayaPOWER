#!/usr/bin/env python3
"""Tests for tools/lesson_score.py — LIL Phase B scorer (spec v1 §6.2, §6.3).

Every test is a real execution against fixture stores. No mocks of the
module's own code.
"""

import json
import os
import subprocess
import sys

import pytest

TOOL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "lesson_score.py"))
sys.path.insert(0, os.path.dirname(TOOL))
import lesson_score as ls  # noqa: E402


def make_lesson(lid, inj=0, hits=0, misses=0, status="active"):
    return {
        "lesson_id": lid,
        "lesson_statement": f"Statement for {lid}",
        "enforcement": f"Enforcement for {lid}",
        "status": status,
        "applies_when": {"areas": ["x"], "mission_classes": [], "failure_signatures": []},
        "injections": inj,
        "hits": hits,
        "misses": misses,
    }


@pytest.fixture
def store(tmp_path):
    def _write(lessons, judgments, as_array=True):
        sp = tmp_path / "lessons.jsonl"
        fp = tmp_path / "fold.json"
        with open(sp, "w") as fh:
            if as_array:
                json.dump(lessons, fh)
            else:
                for lesson in lessons:
                    fh.write(json.dumps(lesson) + "\n")
        with open(fp, "w") as fh:
            json.dump(judgments, fh)
        return str(sp), str(fp)
    return _write


def run_cli(store_p, fold_p, *extra):
    cmd = [sys.executable, TOOL, "--store", store_p, "--fold", fold_p, *extra]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout) if proc.stdout.strip() else None, proc.stderr


def read_store(path):
    with open(path) as fh:
        raw = fh.read().strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [json.loads(l) for l in raw.split("\n") if l.strip()]


# --- fold counting (§6.3) ------------------------------------------------------

def test_hit_miss_counted(store):
    sp, fp = store([make_lesson("L-1", inj=5, hits=4, misses=0)],
                   [{"lesson_id": "L-1", "verdict": "hit"},
                    {"lesson_id": "L-1", "verdict": "miss"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    lessons = read_store(sp)
    assert (lessons[0]["hits"], lessons[0]["misses"], lessons[0]["injections"]) == (5, 1, 7)
    assert report["counter_deltas"]["L-1"] == {"hits": 1, "misses": 1, "injections": 2}


def test_unclear_not_counted(store):
    sp, fp = store([make_lesson("L-1", inj=5, hits=4, misses=1)],
                   [{"lesson_id": "L-1", "verdict": "unclear"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    lessons = read_store(sp)
    assert (lessons[0]["hits"], lessons[0]["misses"], lessons[0]["injections"]) == (4, 1, 5)
    assert report["judgments_unclear_skipped"] == 1


def test_dispute_is_miss_plus_review_flag(store):
    sp, fp = store([make_lesson("L-1", inj=5, hits=4, misses=0)],
                   [{"lesson_id": "L-1", "verdict": "hit", "dispute": True}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    lessons = read_store(sp)
    assert (lessons[0]["hits"], lessons[0]["misses"]) == (4, 1)  # dispute -> miss
    assert lessons[0]["needs_rewrite_review"] is True
    assert report["disputes_flagged_rewrite_review"] == ["L-1"]


def test_unknown_lesson_id_reported(store):
    sp, fp = store([make_lesson("L-1")],
                   [{"lesson_id": "L-NOPE", "verdict": "hit"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    assert report["unknown_lesson_ids"] == ["L-NOPE"]


def test_jsonl_roundtrip_preserved(store):
    sp, fp = store([make_lesson("L-1", inj=2)], [{"lesson_id": "L-1", "verdict": "hit"}],
                   as_array=False)
    rc, _report, _ = run_cli(sp, fp)
    assert rc == 0
    with open(sp) as fh:
        lines = [l for l in fh.read().strip().split("\n") if l.strip()]
    assert len(lines) == 1
    assert json.loads(lines[0])["injections"] == 3


def test_dry_run_writes_nothing(store):
    sp, fp = store([make_lesson("L-1", inj=2)], [{"lesson_id": "L-1", "verdict": "hit"}])
    rc, report, _ = run_cli(sp, fp, "--dry-run")
    assert rc == 0
    assert report["dry_run"] is True
    assert read_store(sp)[0]["injections"] == 2


# --- weekly review thresholds (§6.2) --------------------------------------------

def test_promote_candidate_at_threshold(store):
    # 4/5 = 0.80 with 5 injections -> doctrine candidate
    sp, fp = store([make_lesson("L-1", inj=4, hits=3, misses=0)],
                   [{"lesson_id": "L-1", "verdict": "hit"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    cands = [c["lesson_id"] for c in report["promote_candidates"]]
    assert cands == ["L-1"]
    # Report only by default: status untouched without --apply.
    assert read_store(sp)[0]["status"] == "active"


def test_promote_below_injection_floor_not_candidate(store):
    # Perfect rate but only 4 injections -> not yet scored.
    sp, fp = store([make_lesson("L-1", inj=3, hits=3, misses=0)],
                   [{"lesson_id": "L-1", "verdict": "hit"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    assert report["promote_candidates"] == []


def test_retire_candidate_below_floor(store):
    # 1/6 = 0.167 < 0.30 with 6 injections -> rewrite/retire candidate
    sp, fp = store([make_lesson("L-1", inj=5, hits=1, misses=4)],
                   [{"lesson_id": "L-1", "verdict": "miss"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    cands = [c["lesson_id"] for c in report["retire_candidates"]]
    assert cands == ["L-1"]


def test_trial_unscored(store):
    sp, fp = store([make_lesson("L-1", inj=1, hits=1, misses=0)],
                   [{"lesson_id": "L-1", "verdict": "hit"}])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    assert report["trial_unscored"] == ["L-1"]
    assert report["promote_candidates"] == []
    assert report["retire_candidates"] == []


def test_apply_flips_statuses(store):
    sp, fp = store([make_lesson("L-1", inj=4, hits=3, misses=0, status="active"),
                    make_lesson("L-2", inj=5, hits=1, misses=4, status="active")],
                   [{"lesson_id": "L-1", "verdict": "hit"},
                    {"lesson_id": "L-2", "verdict": "miss"}])
    rc, report, _ = run_cli(sp, fp, "--apply")
    assert rc == 0
    by_id = {l["lesson_id"]: l for l in read_store(sp)}
    assert by_id["L-1"]["status"] == "promoted"
    assert by_id["L-2"]["status"] == "retired"
    assert sorted(report["statuses_flipped"]) == ["L-1", "L-2"]


def test_retired_lesson_skipped_in_review(store):
    sp, fp = store([make_lesson("L-1", inj=9, hits=0, misses=9, status="retired")], [])
    rc, report, _ = run_cli(sp, fp)
    assert rc == 0
    assert report["retire_candidates"] == []
