"""Tests for the Three-Try Circuit Breaker on the Builder-Scorer Loop gate
(Shawn, 2026-10-12 — STANDING).

One hypothesis gets exactly three tries. A fourth attempt on the same
hypothesis is not permitted — even with a fabricated 9.5. After three
tries below 9.0, the verdict is REFRAME_REQUIRED: the builder writes the
hypothesis-change note and a DIFFERENT seat's scorer must accept the
reframe before a new three-round budget opens.

Runnable with plain python3 (no pytest required):
    python3 tests/test_builder_scorer_loop_circuit_breaker.py
Also pytest-compatible (plain assert functions):
    python3 -m pytest tests/test_builder_scorer_loop_circuit_breaker.py -v

Covers the amendment to builder_scorer_loop.py:
  - 3 honest rounds, final 9.3 -> PASS (backward compatible)
  - 3 rounds, final 8.4 -> FAIL (below the bar)
  - 4 rounds same hypothesis, 7.2/7.8/8.3/9.5 -> FAIL REFRAME_REQUIRED
    (the false-pass the original gate allowed)
  - 4 rounds with a hypothesis block but no change receipt -> FAIL
  - cosmetic rename (new id, no scorer receipt) -> FAIL
  - genuine reframe + different-seat REFRAME_ACCEPTED -> new budget PASS,
    prior budget retained in details
  - forged scorer (same seat as builder) -> FAIL
  - malformed hypothesis block / receipt -> FAIL (fail closed)
  - 7 rounds even with an accepted reframe -> FAIL (reframe budget
    exhausted)
  - --preflight: attempt 4 same hypothesis, no receipt -> exit 2 BLOCKED;
    unknown state -> exit 2 (fail closed); attempt <= 3 -> exit 0;
    accepted reframe + new hypothesis id -> exit 0; same old id -> exit 2
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import builder_scorer_loop  # noqa: E402


# ================================================================ fixtures

def _round(n, score, changed, moved, gaps):
    return {
        "round": n,
        "score": score,
        "recorded_at": f"2026-10-12T{6 + n:02d}:00:00Z",
        "what_changed": changed,
        "why_score_moved": moved,
        "gaps_found": gaps,
    }


def _three_rounds(scores, tag="h1"):
    return [
        _round(i + 1, s,
               f"fix element {tag}-{i + 1} applied with implementation notes and regression tests",
               f"score moved to {s} because defect {tag}-{i + 1} closed and measured in round {i + 1}",
               [f"remaining gap {tag}-{i + 1} not yet closed"])
        for i, s in enumerate(scores)
    ]


def _base(scores, **kw):
    rec = {"work_product": "synth-circuit-breaker-case",
           "seat": "naya-2",
           "rounds": _three_rounds(scores[:3])}
    if len(scores) > 3:
        extra = [
            _round(i + 1, s,
                   f"another iteration on the same approach, deeper tuning pass {i + 1} with full notes",
                   f"score moved to {s} because the tuning pass {i + 1} improved the measured quality",
                   [f"remaining gap after pass {i + 1}"])
            for i, s in enumerate(scores[3:], start=3)
        ]
        rec["rounds"] = rec["rounds"] + extra
    rec.update(kw)
    return rec


def _accepted_change(prior="h1", new="h2", scorer="naya-4"):
    return {
        "prior_hypothesis_id": prior,
        "new_hypothesis_id": new,
        "why_failed": "three tries tuned the same retry policy; the failure repeats identically each run",
        "failing_evidence": "rounds 1-3 scored 7.2/7.8/8.3, failure fingerprint fp-991: identical timeout signature",
        "new_root_claim": "the timeout is not a tuning parameter problem; the worker consults stale state — a different seam",
        "why_different_at_root": "the old hypothesis said 'tune the policy'; the new hypothesis says 'the state read is wrong' — different root cause, different mechanism, falsifiable by the stale-read probe",
        "scorer_seat": scorer,
        "scorer_verdict": "REFRAME_ACCEPTED",
        "source_pointer": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6120000000",
    }


# ==================================================================== check

def test_three_honest_rounds_still_pass():
    out = builder_scorer_loop.check(_base([7.9, 8.6, 9.3]))
    assert out["pass"] is True, out["reasons"]


def test_three_rounds_below_nine_still_fail():
    out = builder_scorer_loop.check(_base([7.2, 7.8, 8.4]))
    assert out["pass"] is False, out["reasons"]


def test_fourth_same_hypothesis_fails_reframe_required():
    # The false-pass: the original gate PASSED this. The circuit breaker
    # must FAIL it — the fabricated round-4 9.5 does not open the ceiling.
    out = builder_scorer_loop.check(_base([7.2, 7.8, 8.3, 9.5]))
    assert out["pass"] is False, out["reasons"]
    assert "REFRAME_REQUIRED" in out["reasons"][0], out["reasons"]


def test_fourth_round_with_hypothesis_id_but_no_receipt_fails():
    rec = _base([7.2, 7.8, 8.3, 9.5],
                hypothesis={"hypothesis_id": "h1", "hypothesis_change": None})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]
    assert "REFRAME_REQUIRED" in out["reasons"][0], out["reasons"]


def test_cosmetic_rename_without_scorer_receipt_fails():
    # A new label is not a reframe: no accepted scorer receipt.
    rec = _base([7.2, 7.8, 8.3, 9.5],
                hypothesis={"hypothesis_id": "h1-polished",
                             "hypothesis_change": None})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]


def test_genuine_reframe_opens_new_budget():
    change = _accepted_change()
    rec = _base([7.2, 7.8, 8.3, 8.9, 9.4],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is True, out["reasons"]
    det = out["details"]
    assert det["prior_budget"]["status"] == "EXHAUSTED", det
    assert det["prior_budget"]["rounds_exhausted"] == 3, det
    assert det["hypothesis_change"]["verdict"] == "REFRAME_ACCEPTED", det
    assert det["hypothesis_change"]["scorer"] == "naya-4", det


def test_forged_scorer_same_seat_fails():
    change = _accepted_change(scorer="naya-2")  # builder's own seat
    rec = _base([7.2, 7.8, 8.3, 9.4],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]
    assert "DIFFERENT seat" in out["reasons"][0], out["reasons"]


def test_rejected_verdict_fails():
    change = _accepted_change()
    change["scorer_verdict"] = "REFRAME_REJECTED"
    rec = _base([7.2, 7.8, 8.3, 9.4],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]


def test_malformed_hypothesis_block_fails_closed():
    rec = _base([7.2, 7.8, 8.3, 9.5],
                hypothesis={"hypothesis_id": ""})  # no id: fail closed
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]

    rec2 = _base([7.2, 7.8, 8.3, 9.5],
                 hypothesis="just a string")  # not a record: fail closed
    out2 = builder_scorer_loop.check(rec2)
    assert out2["pass"] is False, out2["reasons"]

    change = _accepted_change()
    del change["source_pointer"]  # missing required field: fail closed
    rec3 = _base([7.2, 7.8, 8.3, 9.4],
                 hypothesis={"hypothesis_id": "h2",
                              "hypothesis_change": change})
    out3 = builder_scorer_loop.check(rec3)
    assert out3["pass"] is False, out3["reasons"]


def test_reframe_budget_also_exhausts_at_six():
    # 3 on the prior hypothesis + 3 on the reframe, then a 7th round:
    # the new budget is also exhausted — STOP_OR_HANDOFF, not round 7.
    # (Final >= 9.0 so the score check passes and the ceiling fires.)
    change = _accepted_change()
    rec = _base([7.2, 7.8, 8.3, 8.4, 8.8, 9.2, 9.3],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]
    assert "STOP_OR_HANDOFF" in out["reasons"][0], out["reasons"]


def test_reframe_receipt_with_no_extra_rounds_fails():
    # A paper reframe: the receipt claims a new budget but the record
    # carries only the exhausted three rounds.
    change = _accepted_change()
    rec = _base([7.2, 7.8, 8.3],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    out = builder_scorer_loop.check(rec)
    assert out["pass"] is False, out["reasons"]


# ================================================================ preflight

def _write_receipt(rec):
    fd, path = tempfile.mkstemp(suffix=".json")
    with open(fd, "w") as f:
        json.dump(rec, f)
    return path


def _run_preflight(path, attempt, hyp_id=None):
    cmd = [sys.executable, str(CHECKS / "builder_scorer_loop.py"),
           "--preflight", "--record-file", path, "--attempt", str(attempt)]
    if hyp_id is not None:
        cmd += ["--hypothesis-id", hyp_id]
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=60, cwd=ROOT)


def test_preflight_within_budget_allowed():
    path = _write_receipt(_base([7.2]))
    try:
        run = _run_preflight(path, 2)
        assert run.returncode == 0, run.stdout + run.stderr
    finally:
        Path(path).unlink(missing_ok=True)


def test_preflight_fourth_attempt_blocked_without_receipt():
    path = _write_receipt(_base([7.2, 7.8, 8.3]))
    try:
        run = _run_preflight(path, 4, "h1")
        assert run.returncode == 2, run.stdout + run.stderr
        assert "REFRAME_REQUIRED" in run.stdout, run.stdout
    finally:
        Path(path).unlink(missing_ok=True)


def test_preflight_unknown_state_fails_closed():
    run = _run_preflight("/nonexistent/loop-receipt.json", 4, "h1")
    assert run.returncode == 2, run.stdout + run.stderr


def test_preflight_accepted_reframe_allows_new_attempt():
    change = _accepted_change()
    rec = _base([7.2, 7.8, 8.3],
                hypothesis={"hypothesis_id": "h2",
                             "hypothesis_change": change})
    path = _write_receipt(rec)
    try:
        ok = _run_preflight(path, 4, "h2")
        assert ok.returncode == 0, ok.stdout + ok.stderr
        same_wall = _run_preflight(path, 4, "h1")  # old id: blocked
        assert same_wall.returncode == 2, same_wall.stdout + same_wall.stderr
    finally:
        Path(path).unlink(missing_ok=True)


# ==================================================================== runner

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001 - the runner must report, not hide
            failed += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
