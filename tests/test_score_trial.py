"""Self-test for the A→B→C measurement harness (score-trial.py).

Runs synthetic trial data through the scorer and asserts the expected
verdict for each case. Covers all four verdicts plus the safety veto
and weak-attribution paths.

Run: python3 -m pytest tests/test_score_trial.py -v
     (or: python3 tests/test_score_trial.py)
"""
import json
import subprocess
import sys
import tempfile
import os

HARNESS = os.path.join(os.path.dirname(__file__), "..", "tools",
                       "successor", "score-trial.py")


def make_trial(tid, a, b, c=None, mech=True, refusal="PASS", design=True):
    t = {
        "trial_id": tid,
        "preregistration": {"min_absolute_delta": 0.20, "alpha": 0.05,
                             "n_per_arm": len(a)},
        "arms": {"A": {"outcomes": a}, "B": {"outcomes": b}},
        "design_controls": {
            "briefs_byte_identical": design,
            "same_model": design,
            "only_lesson_differs": design,
        },
        "mechanism_evidence": {"treatment_shows_lesson_behavior": mech},
        "refusal_probe": {"verdict": refusal, "detail": ""},
    }
    if c is not None:
        t["arms"]["C"] = {"outcomes": c}
    return t


def score(trial):
    with tempfile.NamedTemporaryFile("w", suffix=".json",
                                     delete=False) as f:
        json.dump(trial, f)
        path = f.name
    try:
        out = subprocess.run(
            [sys.executable, HARNESS, path],
            capture_output=True, text=True, timeout=60)
        assert out.returncode == 0, f"harness failed: {out.stderr}"
        return json.loads(out.stdout)
    finally:
        os.unlink(path)


def test_improved():
    r = score(make_trial(
        "T-IMPROVED",
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        c=[1, 1, 1, 1, 1, 1, 1, 1, 0, 0]))
    assert r["verdict"] == "IMPROVED", r
    assert r["attribution"]["level"] == "STRONG"
    assert r["comparisons"]["B_vs_A"]["p_value_greater"] < 0.05


def test_no_delta():
    a = [1] * 37 + [0] * 38
    b = [1] * 41 + [0] * 34
    r = score(make_trial("T-NODELTA", a, b))
    assert r["verdict"] == "NO_DELTA", r
    assert r["comparisons"]["B_vs_A"]["adequately_powered"] is True


def test_regressed():
    r = score(make_trial(
        "T-REGRESSED",
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert r["verdict"] == "REGRESSED", r


def test_inconclusive_underpowered():
    r = score(make_trial(
        "T-INCONCLUSIVE",
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0]))
    assert r["verdict"] == "INCONCLUSIVE", r
    assert "underpowered" in r["reasons"][0]


def test_inconclusive_refusal_veto():
    r = score(make_trial(
        "T-REFUSAL",
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        refusal="FAIL"))
    assert r["verdict"] == "INCONCLUSIVE", r
    assert "refusal" in r["reasons"][0].lower()


def test_weak_attribution_flagged():
    r = score(make_trial(
        "T-WEAK",
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        mech=False))
    assert r["verdict"] == "IMPROVED", r
    assert r["attribution"]["level"] == "WEAK"


def test_fail_closed_on_bad_input():
    with tempfile.NamedTemporaryFile("w", suffix=".json",
                                     delete=False) as f:
        f.write('{"not": "a trial"}')
        path = f.name
    try:
        out = subprocess.run(
            [sys.executable, HARNESS, path],
            capture_output=True, text=True, timeout=60)
        assert out.returncode == 2, "must fail closed on bad input"
    finally:
        os.unlink(path)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    sys.exit(1 if failed else 0)
