"""Tests for the Shawn Feel Gate (tools/protocol/checks/feel_gate.py).

Shawn's directive (2026-10-11): "A claimed 9.0 that doesn't feel like 9.0 in
use gets the model revisited."

The gate is a required human attestation before any 9.0+ claim: six feel
questions answered honestly by the builder, confirmed by a different seat.

Runnable with plain python3 (no pytest required):
    python3 tests/test_feel_gate.py
Also pytest-compatible (plain assert functions).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import feel_gate  # noqa: E402


def _yes(note="evidence note"):
    return {"answer": "yes", "note": note}


def _no(note="evidence note", remediation="tracked fix plan here"):
    return {"answer": "no", "note": note, "remediation": remediation}


def _full_feel(**overrides):
    feel = {
        "first_read": _yes("a non-technical reader understood it first try"),
        "no_surprises": _yes("behavior matches the documented contract"),
        "smooth": _yes("no jank observed in the walkthrough"),
        "world_ready": _yes("would show this publicly today"),
        "true_words": _yes("every claim traced to evidence"),
        "bullseye": _yes("best version we know how to build"),
    }
    feel.update(overrides)
    return feel


def _record(**overrides):
    rec = {
        "deliverable": "test deliverable",
        "claimed_score": 9.2,
        "feel": _full_feel(),
        "builder": "naya-alpha",
        "validator": "naya-beta",
        "validator_confirms": True,
    }
    rec.update(overrides)
    return rec


# ---------------------------------------------------------------- happy path
def test_all_yes_passes():
    r = feel_gate.check(_record())
    assert r["pass"] is True, r["reasons"]
    assert len(r["reasons"]) >= 8  # 6 questions + builder/validator + confirm


def test_honest_no_with_remediation_passes():
    rec = _record()
    rec["feel"]["smooth"] = _no("animation stutters on first load",
                               "preload assets before first paint; tracked in issue")
    r = feel_gate.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert any("smooth: no" in x for x in r["reasons"])


# ------------------------------------------------------- 9.0+ requires feel
def test_nine_plus_without_attestation_fails():
    rec = _record()
    del rec["feel"]
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("no feel attestation" in x for x in r["reasons"])


def test_exactly_nine_requires_attestation():
    rec = _record(claimed_score=9.0)
    del rec["feel"]
    r = feel_gate.check(rec)
    assert r["pass"] is False


def test_below_nine_without_attestation_passes():
    rec = _record(claimed_score=8.9)
    del rec["feel"]
    r = feel_gate.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert any("not required" in x for x in r["reasons"])


def test_below_nine_with_bad_attestation_still_fails():
    # A present attestation is validated even when not required.
    rec = _record(claimed_score=8.5, builder="same-seat", validator="same-seat")
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("same seat" in x for x in r["reasons"])


# ------------------------------------------------------------------- answers
def test_no_without_remediation_fails():
    rec = _record()
    rec["feel"]["world_ready"] = {"answer": "no", "note": "rough edges remain"}
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("remediation" in x for x in r["reasons"])


def test_missing_question_fails():
    rec = _record()
    del rec["feel"]["bullseye"]
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("bullseye" in x and "missing" in x for x in r["reasons"])


def test_missing_note_fails():
    rec = _record()
    rec["feel"]["true_words"] = {"answer": "yes", "note": "   "}
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("evidence note" in x for x in r["reasons"])


def test_invalid_answer_fails():
    rec = _record()
    rec["feel"]["smooth"] = {"answer": "maybe", "note": "unsure"}
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("must be 'yes' or 'no'" in x for x in r["reasons"])


def test_all_six_questions_required():
    assert len(feel_gate.FEEL_KEYS) == 6
    for key in ["first_read", "no_surprises", "smooth",
                "world_ready", "true_words", "bullseye"]:
        assert key in feel_gate.FEEL_KEYS


# ------------------------------------------------------------------ identity
def test_builder_equals_validator_fails():
    r = feel_gate.check(_record(builder="naya-alpha", validator="naya-alpha"))
    assert r["pass"] is False
    assert any("same seat" in x for x in r["reasons"])


def test_validator_not_confirmed_fails():
    r = feel_gate.check(_record(validator_confirms=False))
    assert r["pass"] is False
    assert any("not confirmed" in x for x in r["reasons"])


def test_unnamed_builder_fails():
    r = feel_gate.check(_record(builder="  "))
    assert r["pass"] is False
    assert any("builder unnamed" in x for x in r["reasons"])


def test_unnamed_validator_fails():
    rec = _record()
    del rec["validator"]
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("validator unnamed" in x for x in r["reasons"])


# ------------------------------------------------------------------ malformed
def test_missing_score_fails():
    rec = _record()
    del rec["claimed_score"]
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("claimed_score" in x for x in r["reasons"])


def test_non_dict_feel_fails():
    r = feel_gate.check(_record(feel="looks good"))
    assert r["pass"] is False


def test_non_dict_record_fails():
    r = feel_gate.check("not a dict")
    assert r["pass"] is False


def test_missing_deliverable_fails():
    # An unnamed 9.0+ claim cannot pass — the gate judges a named thing.
    rec = _record()
    del rec["deliverable"]
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("deliverable" in x for x in r["reasons"])


def test_short_note_fails():
    # A one-word note is not evidence.
    rec = _record()
    rec["feel"]["smooth"] = {"answer": "yes", "note": "fine"}
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("evidence note" in x for x in r["reasons"])


def test_short_remediation_fails():
    rec = _record()
    rec["feel"]["smooth"] = {"answer": "no", "note": "it stutters badly",
                            "remediation": "fix it"}
    r = feel_gate.check(rec)
    assert r["pass"] is False
    assert any("remediation" in x for x in r["reasons"])


# ------------------------------------------------------------------ CLI smoke
def test_cli_pass_and_fail():
    import json
    import subprocess
    ok_record = json.dumps(_record())
    p = subprocess.run(
        [sys.executable, str(CHECKS / "feel_gate.py"),
         "--record", ok_record],
        capture_output=True, text=True, timeout=30)
    assert p.returncode == 0, p.stderr
    assert "PASS" in p.stdout

    bad_record = json.dumps(_record(builder="x", validator="x"))
    p = subprocess.run(
        [sys.executable, str(CHECKS / "feel_gate.py"),
         "--record", bad_record],
        capture_output=True, text=True, timeout=30)
    assert p.returncode == 1
    assert "FAIL" in p.stdout


if __name__ == "__main__":
    fns = sorted((v for k, v in list(globals().items())
                  if k.startswith("test_") and callable(v)),
                 key=lambda f: f.__name__)
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"ok - {fn.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL - {fn.__name__}: {exc}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
