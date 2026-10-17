#!/usr/bin/env python3
"""Tests for tools/lesson_inject.py — LIL Phase B injector (spec v1 §6.1).

Every test is a real execution against fixture stores. No mocks of the
module's own code.
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

TOOL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "lesson_inject.py"))
sys.path.insert(0, os.path.dirname(TOOL))
import lesson_inject as li  # noqa: E402


def make_lesson(lid, areas=(), classes=(), sigs=(), inj=0, hits=0, misses=0,
                status="active", complete=True):
    lesson = {
        "lesson_id": lid,
        "lesson_statement": f"Statement for {lid}",
        "enforcement": f"Enforcement for {lid}",
        "status": status,
        "injections": inj,
        "hits": hits,
        "misses": misses,
        "applies_when": {
            "areas": list(areas),
            "mission_classes": list(classes),
            "failure_signatures": list(sigs),
        },
    }
    if not complete:
        lesson.pop("applies_when")
    return lesson


@pytest.fixture
def store_path(tmp_path):
    def _write(lessons, as_array=True):
        p = tmp_path / "lessons.jsonl"
        with open(p, "w") as fh:
            if as_array:
                json.dump(lessons, fh)
            else:
                for lesson in lessons:
                    fh.write(json.dumps(lesson) + "\n")
        return str(p)
    return _write


def run_cli(store, *extra):
    cmd = [sys.executable, TOOL, "--store", store, *extra]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


# --- matching (§6.1 step 1) -------------------------------------------------

def test_area_match(store_path):
    p = store_path([make_lesson("L-1", areas=["dispatch"]),
                    make_lesson("L-2", areas=["design-sweep"])])
    sel = li.inject(li.load_store(p), ["dispatch"], [], [])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-1"]


def test_mission_class_match(store_path):
    p = store_path([make_lesson("L-1", classes=["dispatch"])])
    sel = li.inject(li.load_store(p), [], ["dispatch"], [])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-1"]


def test_failure_signature_match(store_path):
    p = store_path([make_lesson("L-1", sigs=["void-dispatch"])])
    sel = li.inject(li.load_store(p), ["dispatch"], [], ["void-dispatch"])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-1"]


def test_no_match_emits_nothing(store_path):
    p = store_path([make_lesson("L-1", areas=["design-sweep"])])
    rc, out, _err = run_cli(p, "--areas", "dispatch")
    assert rc == 0
    assert out.strip() == ""


def test_retired_never_injects(store_path):
    p = store_path([make_lesson("L-1", areas=["dispatch"], status="retired")])
    sel = li.inject(li.load_store(p), ["dispatch"], [], [])
    assert sel == []


def test_incomplete_lesson_bounced(store_path):
    # Spec §6.3: lessons missing applies_when/enforcement never enter the store;
    # the injector must skip them, not crash.
    p = store_path([make_lesson("L-1", areas=["dispatch"], complete=False),
                    make_lesson("L-2", areas=["dispatch"])])
    sel = li.inject(li.load_store(p), ["dispatch"], [], [])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-2"]


def test_jsonl_format_accepted(store_path):
    p = store_path([make_lesson("L-1", areas=["dispatch"])], as_array=False)
    sel = li.inject(li.load_store(p), ["dispatch"], [], [])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-1"]


def test_injection_count_alias_accepted(store_path):
    lesson = make_lesson("L-1", areas=["dispatch"], inj=4, hits=3)
    del lesson["injections"]
    lesson["injection_count"] = 4
    p = store_path([lesson])
    sel = li.inject(li.load_store(p), ["dispatch"], [], [])
    assert sel[0][1] == 4 and sel[0][2] == 3


# --- ranking (§6.1 step 2) ---------------------------------------------------

def test_laplace_ranking_orders_by_score(store_path):
    # A: 9/10 -> 10/12 = 0.833 ; B: 0/0 -> 1/2 = 0.5 ; C: 1/8 -> 2/10 = 0.2
    lessons = [
        make_lesson("L-A", areas=["x"], inj=10, hits=9),
        make_lesson("L-B", areas=["x"], inj=0, hits=0),
        make_lesson("L-C", areas=["x"], inj=8, hits=1),
    ]
    p = store_path(lessons)
    sel = li.inject(li.load_store(p), ["x"], [], [])
    assert [l["lesson_id"] for _, _, _, l in sel] == ["L-A", "L-B", "L-C"]
    scores = [s for s, _, _, _ in sel]
    assert scores == sorted(scores, reverse=True)


def test_cold_start_gets_half_not_zero(store_path):
    p = store_path([make_lesson("L-1", areas=["x"])])
    sel = li.inject(li.load_store(p), ["x"], [], [])
    assert sel[0][0] == pytest.approx(0.5)


# --- selection (§6.1 step 3) -------------------------------------------------

def test_top_five_cap(store_path):
    lessons = [make_lesson(f"L-{i}", areas=["x"], inj=10, hits=i) for i in range(8)]
    p = store_path(lessons)
    sel = li.inject(li.load_store(p), ["x"], [], [], cap=5)
    assert len(sel) == 5


def test_trial_slot_guaranteed(store_path):
    # Five veterans score higher than the one untried lesson; the trial slot
    # must still displace the weakest veteran.
    lessons = [make_lesson(f"L-V{i}", areas=["x"], inj=10, hits=9) for i in range(5)]
    lessons.append(make_lesson("L-NEW", areas=["x"], inj=0, hits=0))
    p = store_path(lessons)
    sel = li.inject(li.load_store(p), ["x"], [], [], cap=5)
    ids = [l["lesson_id"] for _, _, _, l in sel]
    assert "L-NEW" in ids
    assert len(ids) == 5


def test_no_trial_candidates_no_swap(store_path):
    lessons = [make_lesson(f"L-{i}", areas=["x"], inj=10, hits=9 - i) for i in range(6)]
    p = store_path(lessons)
    sel = li.inject(li.load_store(p), ["x"], [], [], cap=5)
    assert len(sel) == 5  # nothing to swap in; selection stands


# --- format (§6.1 step 4) ----------------------------------------------------

def test_brief_line_format(store_path):
    p = store_path([make_lesson("L-9", areas=["x"], inj=4, hits=3)])
    rc, out, _err = run_cli(p, "--areas", "x")
    assert rc == 0
    line = out.strip().split("\n")[0]
    assert line.startswith("- ")
    assert "(L-9, 3/4)" in line
    assert "→" in line


def test_json_format(store_path):
    p = store_path([make_lesson("L-9", areas=["x"], inj=4, hits=3)])
    rc, out, _err = run_cli(p, "--areas", "x", "--format", "json")
    assert rc == 0
    data = json.loads(out)
    assert data[0]["lesson_id"] == "L-9"
    assert data[0]["score"] == pytest.approx(round((3 + 1) / (4 + 2), 4))


def test_missing_store_is_error():
    rc, _out, err = run_cli("/nonexistent/store.jsonl", "--areas", "x")
    assert rc == 2
    assert "error" in err.lower()
