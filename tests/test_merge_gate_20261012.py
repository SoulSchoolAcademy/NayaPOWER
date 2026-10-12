"""Tests for the merge-authority check #4 EXECUTOR (Naya Delta rec A, 2026-10-12).

The check existed; nothing executed it. These tests prove the executor
fires where it must and stays quiet where it should:

  - a VIOLATING packet (the #2434/#2435 class: builder self-score, no
    independent validation) makes the gate REFUSE the ref update;
  - an HONORING packet (all five ratified conditions) makes the gate PASS;
  - a missing packet, a missing check module, and a smuggled non-main
    target all fail closed — never default to permitted.

Runnable with plain python3 (no pytest required):
    python3 tests/test_merge_gate_20261012.py
Also pytest-compatible (plain assert functions).

Covers: tools/protocol/checks/merge_gate.py (the check #4 executor).
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import merge_gate  # noqa: E402
from checks.merge_gate import GateRefused, enforce  # noqa: E402


# ================================================================ fixtures

def _valid_packet(**over):
    """A packet honoring all five ratified delegation conditions."""
    p = {
        "target": "main",
        "branch": "naya5/some-feature",
        "seat": "naya 5",
        "tests_green": True,
        "test_evidence": "pytest 2836 passed, 0 failed (CI run 12345)",
        "self_scorecard": {
            "score": 9.5,
            "evidence_backed": True,
            "value_calculus_run": True,
        },
        "independent_validator": "naya epsilon",
        "posted_to_1354": True,
        "team_objections": 0,
        "post_merge_report_planned": True,
    }
    p.update(over)
    return p


def _pre_iv_packet():
    """The #2434/#2435 failure class: builder 9.5 self-score, merge
    attempted BEFORE independent validation finished."""
    p = _valid_packet()
    del p["independent_validator"]
    return p


def _refuses(ref, packet):
    try:
        enforce(ref, packet)
    except GateRefused as e:
        return e.reasons
    raise AssertionError(f"gate ALLOWED what it must refuse (ref={ref})")


def _allows(ref, packet):
    try:
        return enforce(ref, packet)
    except GateRefused as e:
        raise AssertionError(
            f"gate REFUSED what it must allow (ref={ref}): {e.reasons}")


# ================================================================ the core proof

def test_fires_on_pre_iv_merge_attempt():
    """The exact #2434/#2435 class: 9.5 builder self-score, no independent
    validator named — the gate must refuse the main-ref update."""
    reasons = _refuses("refs/heads/main", _pre_iv_packet())
    blob = " ".join(reasons).lower()
    assert "independent" in blob, f"refusal must name the missing IV: {reasons}"
    assert "shawn" in blob, f"refusal must say whose word is needed: {reasons}"


def test_fires_on_self_validation():
    """independent_validator == seat is not independent validation."""
    reasons = _refuses("refs/heads/main",
                       _valid_packet(independent_validator="naya 5",
                                     seat="naya 5"))
    assert any("not independent validation" in r for r in reasons), reasons


def test_fires_on_normalized_self_validation():
    """'naya-5' vs 'Naya 5' is one seat wearing different punctuation."""
    reasons = _refuses("refs/heads/main",
                       _valid_packet(independent_validator="naya-5",
                                     seat="Naya 5"))
    blob = " ".join(reasons).lower()
    assert "same seat" in blob or "not independent" in blob, reasons


def test_fires_on_missing_packet():
    """No packet at all: absence fails closed, never defaults to permitted."""
    reasons = _refuses("refs/heads/main", None)
    blob = " ".join(reasons).lower()
    assert "no merge packet" in blob, reasons
    assert "shawn" in blob, reasons


def test_passes_on_properly_validated_packet():
    """All five ratified conditions honored: the gate stays quiet."""
    res = _allows("refs/heads/main", _valid_packet())
    assert res["allowed"] is True
    assert any("all 5 delegation conditions met" in r
               for r in res["reasons"]), res["reasons"]


# ================================================================ scope and anti-smuggle

def test_scope_pass_for_non_main_ref():
    """The delegation covers main only — a feature-branch ref update passes
    by scope without a packet (the law's own boundary, not a loophole)."""
    res = _allows("refs/heads/naya5/some-feature", None)
    assert res["allowed"] is True
    assert any("not applicable" in r or "by scope" in r
               for r in res["reasons"]), res["reasons"]


def test_target_pin_no_scope_smuggle():
    """A packet stamped target='other' cannot smuggle past the gate: the
    executor pins target='main' (scope enforcement, not a new condition).
    Without the pin, the check's own scope rule would PASS-by-scope."""
    bad = _valid_packet(target="other")
    del bad["independent_validator"]  # also missing the IV
    reasons = _refuses("refs/heads/main", bad)
    assert any("independent" in r.lower() for r in reasons), reasons


def test_target_pin_does_not_add_conditions():
    """A fully honoring packet stamped with a stale target still passes —
    the pin binds scope, it does not invent a sixth condition."""
    res = _allows("refs/heads/main", _valid_packet(target="stale-value"))
    assert res["allowed"] is True


# ================================================================ every condition fails closed

def test_each_condition_fails_closed():
    cases = {
        "tests_green false": ({"tests_green": False}, "tests green"),
        "evidence missing": ({"test_evidence": ""}, "test_evidence"),
        "score below 9.0": ({"self_scorecard": {
            "score": 8.9, "evidence_backed": True,
            "value_calculus_run": True}}, "9.0"),
        "scorecard not evidence-backed": ({"self_scorecard": {
            "score": 9.5, "evidence_backed": False,
            "value_calculus_run": True}}, "evidence-backed"),
        "no value calculus": ({"self_scorecard": {
            "score": 9.5, "evidence_backed": True,
            "value_calculus_run": False}}, "value calculus"),
        "not posted": ({"posted_to_1354": False}, "posted"),
        "team objection": ({"team_objections": 1}, "objects"),
        "no report planned": ({"post_merge_report_planned": False}, "report"),
    }
    for name, (over, needle) in cases.items():
        reasons = _refuses("refs/heads/main", _valid_packet(**over))
        blob = " ".join(reasons).lower()
        assert needle.lower() in blob, f"{name}: refusal must name it: {reasons}"


# ================================================================ receipt honesty

def test_receipt_names_live_feed_binding():
    """The PASS receipt says plainly that posted_to_1354 binds to the live
    team feed (#2154), because #1354 is comment-locked."""
    res = _allows("refs/heads/main", _valid_packet())
    blob = " ".join(res["reasons"])
    assert "#2154" in blob and "comment-locked" in blob, res["reasons"]


def test_refusal_states_honest_limit():
    """Every refusal names the honest limit: the gate binds the team's
    scripts; raw API access is the residual, and the ledger is the audit
    surface."""
    reasons = _refuses("refs/heads/main", _pre_iv_packet())
    blob = " ".join(reasons).lower()
    assert "raw api" in blob or "audit surface" in blob, reasons


def test_missing_check_module_fails_closed():
    """If merge_authority cannot be imported, the gate refuses — a missing
    check never means 'allowed'."""
    old = merge_gate._CHECK_AVAILABLE
    merge_gate._CHECK_AVAILABLE = False
    try:
        reasons = _refuses("refs/heads/main", _valid_packet())
    finally:
        merge_gate._CHECK_AVAILABLE = old
    blob = " ".join(reasons).lower()
    assert "could not be loaded" in blob or "missing check" in blob, reasons


# ================================================================ CLI contract

def _cli(*args):
    return subprocess.run(
        [sys.executable, str(CHECKS / "merge_gate.py"), *args],
        capture_output=True, text=True)


def test_cli_refuses_pre_iv_exit_1(tmp_path=None):
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            import json
            json.dump(_pre_iv_packet(), f)
        r = _cli("--ref", "refs/heads/main", "--record", "@" + path)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "REFUSED" in r.stdout, r.stdout
    finally:
        os.unlink(path)


def test_cli_passes_valid_exit_0(tmp_path=None):
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            import json
            json.dump(_valid_packet(), f)
        r = _cli("--ref", "refs/heads/main", "--record", "@" + path)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "PASSED" in r.stdout, r.stdout
    finally:
        os.unlink(path)


def test_cli_unparseable_packet_exit_2():
    r = _cli("--ref", "refs/heads/main", "--record", "{not json")
    assert r.returncode == 2, r.stdout + r.stderr


# ================================================================ runner

if __name__ == "__main__":
    fns = [(k, v) for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for name, fn in fns:
        try:
            fn()
            print(f"  ok  {name}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {name}: {type(e).__name__}: {e}")
    print(f"{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
