"""Tests for SN-IV-DEFAULT — Independent Verification by Default.

"A defended 7.5 beats a wished 9.0."

A 9.0+ scorecard claim must carry a validator receipt from a DIFFERENT seat.
Below 9.0 the gate does not apply. Fail-closed on malformed input.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "protocol"))

from checks import independent_verify as iv  # noqa: E402


def _valid_claim(**over):
    rec = {
        "claim": "PR #9999 merge-ready",
        "claimed_score": 9.2,
        "builder": "naya5",
        "validator": "naya3",
        "validator_checked": [
            "re-ran pytest on the merged tree",
            "verified the three-pass receipt",
        ],
        "validator_score": 9.0,
        "validator_verdict": "PASS",
        "validator_evidence": "3809 passed, 1 pre-existing failure",
    }
    rec.update(over)
    return rec


# --- the core contract -----------------------------------------------------

def test_valid_receipt_passes():
    r = iv.check(_valid_claim())
    assert r["pass"], r["reasons"]


def test_missing_validator_fails_at_9plus():
    rec = _valid_claim()
    del rec["validator"]
    r = iv.check(rec)
    assert not r["pass"]
    assert "no validator receipt" in r["reasons"][0]


def test_empty_validator_fails():
    r = iv.check(_valid_claim(validator="   "))
    assert not r["pass"]


def test_same_seat_validator_fails():
    r = iv.check(_valid_claim(validator="naya5"))
    assert not r["pass"]
    assert "cannot verify yourself" in r["reasons"][0]


def test_same_seat_case_insensitive_fails():
    r = iv.check(_valid_claim(validator="  NAYA 5 "))
    assert not r["pass"]


def test_validator_verdict_fail_blocks_claim():
    r = iv.check(_valid_claim(validator_verdict="FAIL"))
    assert not r["pass"]
    assert "blocked" in r["reasons"][0]


def test_validator_verdict_missing_blocks_claim():
    rec = _valid_claim()
    del rec["validator_verdict"]
    r = iv.check(rec)
    assert not r["pass"]


def test_validator_disagreeing_score_blocks_claim():
    # Builder claims 9.2, validator independently scores 8.5.
    r = iv.check(_valid_claim(validator_score=8.5))
    assert not r["pass"]
    assert "disagrees" in r["reasons"][0]


def test_validator_score_exactly_9_sustains():
    r = iv.check(_valid_claim(claimed_score=9.5, validator_score=9.0))
    assert r["pass"], r["reasons"]


# --- the 9.0 boundary -------------------------------------------------------

def test_below_9_no_receipt_needed():
    rec = _valid_claim(claimed_score=8.9)
    for k in ("validator", "validator_checked", "validator_score",
              "validator_verdict", "validator_evidence"):
        rec.pop(k, None)
    r = iv.check(rec)
    assert r["pass"], r["reasons"]
    assert any("not applicable" in reason for reason in r["reasons"])


def test_exactly_9_requires_receipt():
    rec = _valid_claim(claimed_score=9.0)
    del rec["validator"]
    r = iv.check(rec)
    assert not r["pass"]


def test_exactly_9_with_receipt_passes():
    r = iv.check(_valid_claim(claimed_score=9.0))
    assert r["pass"], r["reasons"]


# --- receipt substance ------------------------------------------------------

def test_empty_checked_list_fails():
    r = iv.check(_valid_claim(validator_checked=[]))
    assert not r["pass"]
    assert "what they checked" in r["reasons"][0]


def test_blank_checked_items_fail():
    r = iv.check(_valid_claim(validator_checked=["   ", ""]))
    assert not r["pass"]


def test_missing_validator_score_fails():
    rec = _valid_claim()
    del rec["validator_score"]
    r = iv.check(rec)
    assert not r["pass"]


def test_validator_score_out_of_range_fails():
    r = iv.check(_valid_claim(validator_score=11))
    assert not r["pass"]


def test_validator_score_nan_fails():
    r = iv.check(_valid_claim(validator_score=float("nan")))
    assert not r["pass"]


def test_evidence_optional():
    rec = _valid_claim()
    del rec["validator_evidence"]
    r = iv.check(rec)
    assert r["pass"], r["reasons"]


# --- fail-closed -------------------------------------------------------------

def test_non_dict_record_fails():
    r = iv.check(["not", "a", "dict"])
    assert not r["pass"]


def test_missing_claimed_score_fails():
    rec = _valid_claim()
    del rec["claimed_score"]
    r = iv.check(rec)
    assert not r["pass"]


def test_claimed_score_out_of_range_fails():
    r = iv.check(_valid_claim(claimed_score=12))
    assert not r["pass"]


def test_anonymous_builder_fails():
    r = iv.check(_valid_claim(builder=""))
    assert not r["pass"]


def test_claimed_score_string_fails():
    r = iv.check(_valid_claim(claimed_score="9.2"))
    assert not r["pass"]


# --- CLI ---------------------------------------------------------------------

def test_cli_pass_and_fail_exit_codes(tmp_path):
    import json
    import subprocess

    good = tmp_path / "good.json"
    good.write_text(json.dumps(_valid_claim()))
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(_valid_claim(validator="naya5")))

    exe = str(ROOT / "tools" / "protocol" / "checks" / "independent_verify.py")
    ok = subprocess.run([sys.executable, exe, "--record", f"@{good}"],
                        capture_output=True, text=True, cwd=ROOT)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "PASS" in ok.stdout

    no = subprocess.run([sys.executable, exe, "--record", f"@{bad}"],
                        capture_output=True, text=True, cwd=ROOT)
    assert no.returncode == 1, no.stdout + no.stderr
    assert "FAIL" in no.stdout


# --- law registration -------------------------------------------------------

def test_law_registered_in_manifest():
    import json
    manifest = json.loads((ROOT / "kernel" / "protocol" / "protocol_manifest.json").read_text())
    laws = {l["id"]: l for l in manifest["laws"]}
    assert "SN-IV-DEFAULT" in laws, "SN-IV-DEFAULT must be a registered law"
    law = laws["SN-IV-DEFAULT"]
    assert law["check"] == "tools/protocol/checks/independent_verify.py"
    assert (ROOT / law["check"]).exists(), "law's check file must exist"


def test_law_ids_still_unique():
    import json
    manifest = json.loads((ROOT / "kernel" / "protocol" / "protocol_manifest.json").read_text())
    ids = [l["id"] for l in manifest["laws"]]
    assert len(ids) == len(set(ids)), "duplicate law IDs = ambiguous authority"


def test_unnamed_claim_fails():
    r = iv.check(_valid_claim(claim="   "))
    assert not r["pass"]
