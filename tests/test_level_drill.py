"""Battery for the level drill (Naya Verity, 2026-10-14).

The drill must be a fair ruler: the key is self-consistent, the grader
is exact, and a perfect subject passes while a careless one fails.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from level_drill import SCENARIOS, VALID_RUNGS, grade, key, run_drill


def test_key_rungs_are_valid():
    for sid, rung in key().items():
        assert rung in VALID_RUNGS, (sid, rung)


def test_key_labels_match_doctrine():
    doctrine = (Path(__file__).resolve().parents[1] / "docs"
                / "HIERARCHY-OF-INTELLIGENCE.md").read_text()
    for s in SCENARIOS:
        assert s["label"].lower() in doctrine.lower(), s["id"]


def test_grader_math():
    assert grade(4, 4) == 1.0
    assert grade(5, 4) == 0.5
    assert grade(3, 4) == 0.5
    assert grade(6, 4) == 0.0
    assert grade(-9, 9) == 0.0


def test_perfect_subject_passes():
    verdict, detail = run_drill(key())
    assert verdict == "PASS", detail
    assert detail["score"] == 1.0


def test_careless_subject_fails():
    bad = {sid: 0 for sid in key()}  # everything "neutral"
    verdict, detail = run_drill(bad)
    assert verdict == "FAIL", detail


def test_incomplete_drill_refused():
    try:
        run_drill({"S1": 2})
    except ValueError as e:
        assert "incomplete" in str(e)
    else:
        raise AssertionError("incomplete drill was accepted")


def test_off_ladder_answer_refused():
    answers = key()
    answers["S1"] = 10
    try:
        run_drill(answers)
    except ValueError as e:
        assert "not a ladder rung" in str(e)
    else:
        raise AssertionError("off-ladder rung was accepted")
