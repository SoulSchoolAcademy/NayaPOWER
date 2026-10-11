"""Tests for the Builder-Scorer Loop gate (Shawn, 2026-10-11).

BUILD -> SCORE -> FIX -> SCORE -> FIX -> SCORE -> MERGE -> POST.

Every law encoded gets the same proof contract:
  - a VIOLATING fixture makes the check FAIL (the encoding fires), and
  - an HONORING fixture makes the check PASS (the encoding stays quiet).

Runnable with plain python3 (no pytest required):
    python3 tests/test_builder_scorer_loop.py
Also pytest-compatible (plain assert functions):
    python3 -m pytest tests/test_builder_scorer_loop.py -v

Covers builder_scorer_loop.py:
  - three honest rounds pass (with and without the post recorded)
  - fewer than three rounds fail (the loop is not complete)
  - duplicate change text across rounds fails (theater is detectable)
  - duplicate score-movement text across rounds fails
  - round-1 perfect score fails (nobody scores their own build perfect)
  - final round below 9.0 fails (the loop continues)
  - non-number / NaN / Infinity / out-of-range scores fail
  - empty gaps_found fails (every round must answer "why not 10?")
  - renumbered rounds fail (the loop runs in order)
  - malformed post fails; absent post still passes (feed is for learning,
    never for gating)
"""

import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import builder_scorer_loop  # noqa: E402


# ================================================================ fixtures

def _honoring_record():
    return {
        "work_product": "builder-scorer loop gate",
        "seat": "naya-5",
        "rounds": [
            {
                "round": 1,
                "score": 7.8,
                "recorded_at": "2026-10-11T18:40:00Z",
                "what_changed": (
                    "Initial build: the loop check module with three-round "
                    "enforcement, substance floors, and the post-as-learning "
                    "rule, plus this test file."
                ),
                "why_score_moved": (
                    "First look: the structure is right but the anti-theater "
                    "rules are thin — uniqueness compares raw text and "
                    "nothing guards the round-1 perfect score."
                ),
                "gaps_found": [
                    "No normalization on the duplicate-detection comparison.",
                    "Round 1 could claim 10.0 and pass.",
                    "The open tension with the delegation is not documented.",
                ],
            },
            {
                "round": 2,
                "score": 8.6,
                "recorded_at": "2026-10-11T18:52:00Z",
                "what_changed": (
                    "Added text normalization (case/punctuation/whitespace "
                    "folding) to the duplicate detector and the round-1 "
                    "below-10 rule."
                ),
                "why_score_moved": (
                    "Second look: the theater detectors now fire on the "
                    "exploits I could name, but the open tension with "
                    "DELEGATED-MERGE-AUTHORITY is still only in my head."
                ),
                "gaps_found": [
                    "The tension between 'never gate on feed' and the "
                    "delegation's no-objection window is undocumented.",
                    "Honest bounds are not stated in the module.",
                ],
            },
            {
                "round": 3,
                "score": 9.4,
                "recorded_at": "2026-10-11T19:05:00Z",
                "what_changed": (
                    "Wrote the open-tension and honest-bounds sections into "
                    "the module docstring in plain English and tightened the "
                    "fixture texts so no two rounds repeat."
                ),
                "why_score_moved": (
                    "Third look: every requirement of the law is now "
                    "machine-enforced and every limit is stated honestly. "
                    "The remaining step is independent validation — a "
                    "different seat's eyes."
                ),
                "gaps_found": [
                    "Independent validation by a different seat is still "
                    "ahead of this packet.",
                ],
            },
        ],
        "post": {
            "posted": True,
            "venue": "Lane Alpha feed #1713",
            "content": (
                "Three distinct rounds beat one long review: the uniqueness "
                "rule forced each round to actually find something new, and "
                "the round-1 ceiling killed the urge to score the first "
                "build a 10."
            ),
        },
    }


# ================================================================== passing

def test_honoring_record_passes():
    r = builder_scorer_loop.check(_honoring_record())
    assert r["pass"], r["reasons"]


def test_honoring_without_post_still_passes():
    """The feed is for learning, never for gating — an absent post cannot
    block the loop."""
    rec = _honoring_record()
    del rec["post"]
    r = builder_scorer_loop.check(rec)
    assert r["pass"], r["reasons"]
    assert any("never for" in reason.upper() or "GATING" in reason
               for reason in r["reasons"]), \
        "the pass must say why the missing post does not block"


# ================================================================ failing

def test_fewer_than_three_rounds_fails():
    rec = _honoring_record()
    rec["rounds"] = rec["rounds"][:2]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "two rounds must not satisfy a three-round law"


def test_duplicate_change_text_fails():
    """Theater detector: two rounds claiming the same fix in the same words."""
    rec = _honoring_record()
    rec["rounds"][2]["what_changed"] = rec["rounds"][1]["what_changed"]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "copy-paste change text must fail as theater"


def test_duplicate_change_text_fails_despite_case_and_punctuation():
    """Theater detector with normalization: respelling the same words does
    not pass."""
    rec = _honoring_record()
    same = rec["rounds"][1]["what_changed"]
    rec["rounds"][2]["what_changed"] = same.upper().replace(".", "!")
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "respelling the same fix must still fail"


def test_duplicate_score_movement_text_fails():
    rec = _honoring_record()
    rec["rounds"][2]["why_score_moved"] = rec["rounds"][0]["why_score_moved"]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "copy-paste score explanations must fail"


def test_round_one_perfect_score_fails():
    rec = _honoring_record()
    rec["rounds"][0]["score"] = 10.0
    rec["rounds"][0]["gaps_found"] = ["none — it is perfect"]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], \
        "a perfect first-round self-score is theater and must fail"


def test_final_round_below_nine_fails():
    rec = _honoring_record()
    rec["rounds"][2]["score"] = 8.9
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "below 9.0 the loop continues — no merge"


def test_final_round_exactly_nine_passes():
    rec = _honoring_record()
    rec["rounds"][2]["score"] = 9.0
    r = builder_scorer_loop.check(rec)
    assert r["pass"], r["reasons"]


def test_non_number_score_fails():
    rec = _honoring_record()
    rec["rounds"][1]["score"] = "nine"
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "the 9.0 bar cannot be evaluated on a non-number"


def test_nan_score_fails():
    rec = _honoring_record()
    rec["rounds"][1]["score"] = math.nan
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "NaN must fail closed"


def test_infinity_score_fails():
    rec = _honoring_record()
    rec["rounds"][2]["score"] = math.inf
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "Infinity must fail closed"


def test_out_of_range_score_fails():
    rec = _honoring_record()
    rec["rounds"][0]["score"] = 11.0
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "scores above the 0-10 scale must fail"


def test_empty_gaps_fails():
    rec = _honoring_record()
    rec["rounds"][1]["gaps_found"] = []
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], 'every round must answer "why not 10?"'


def test_blank_gap_entry_fails():
    rec = _honoring_record()
    rec["rounds"][1]["gaps_found"] = ["   "]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "blank gap entries must fail"


def test_renumbered_rounds_fail():
    rec = _honoring_record()
    rec["rounds"][2]["round"] = 4
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "rounds run in sequence; renumbering fails"


def test_bool_round_number_fails():
    """True == 1 in Python — a bool is not a round number."""
    rec = _honoring_record()
    rec["rounds"][0]["round"] = True
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "round numbers must be real integers"


def test_backdated_timestamps_fail():
    """Rounds must run forward in time — a backdated round means the loop
    was assembled after the fact."""
    rec = _honoring_record()
    rec["rounds"][2]["recorded_at"] = "2026-10-11T18:30:00Z"
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "a round dated before the previous round must fail"


def test_unparseable_timestamp_fails():
    rec = _honoring_record()
    rec["rounds"][1]["recorded_at"] = "yesterday-ish"
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "an unreadable timestamp is no timestamp"


def test_mixed_timestamped_and_untimestamped_fails():
    rec = _honoring_record()
    del rec["rounds"][2]["recorded_at"]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "the receipt cannot mix timestamped and untimestamped rounds"


def test_no_timestamps_at_all_passes():
    """Timestamps are optional — the law does not require them, it only
    refuses to be lied to by them."""
    rec = _honoring_record()
    for rnd in rec["rounds"]:
        del rnd["recorded_at"]
    r = builder_scorer_loop.check(rec)
    assert r["pass"], r["reasons"]


def test_fail_result_is_always_json_serializable():
    """Regression: an internal scratch value once leaked a datetime into
    details, crashing --json output on FAIL paths."""
    import json
    rec = _honoring_record()
    rec["rounds"][1]["what_changed"] = "x"  # thin text -> FAIL after timestamps parsed
    r = builder_scorer_loop.check(rec)
    assert not r["pass"]
    json.dumps(r)  # must not raise


def test_explicit_not_posted_passes_as_pending():
    rec = _honoring_record()
    rec["post"] = {"posted": False}
    r = builder_scorer_loop.check(rec)
    assert r["pass"], r["reasons"]


def test_posted_false_with_venue_fails():
    rec = _honoring_record()
    rec["post"] = {"posted": False, "venue": "#1713", "content": "things"}
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "unposted-and-posted is a contradiction"


def test_thin_change_text_fails():
    rec = _honoring_record()
    rec["rounds"][1]["what_changed"] = "fixed stuff"
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "substance floor must catch filler rounds"


def test_malformed_post_fails():
    rec = _honoring_record()
    rec["post"] = {"posted": True, "venue": "", "content": "learned things"}
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "a post with no venue names nothing"


def test_stub_post_content_fails():
    rec = _honoring_record()
    rec["post"]["content"] = "ok"
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "a stub post teaches nothing"


def test_anonymous_work_fails():
    rec = _honoring_record()
    del rec["seat"]
    r = builder_scorer_loop.check(rec)
    assert not r["pass"], "anonymous work carries no loop receipt"


def test_non_dict_record_fails():
    r = builder_scorer_loop.check("not a record")
    assert not r["pass"], "non-dict records fail closed"


def test_cli_passes_and_fails_with_exit_codes():
    """The CLI is the mechanical gate: exit 0 on PASS, 1 on FAIL."""
    import json
    good = _honoring_record()
    bad = _honoring_record()
    bad["rounds"] = bad["rounds"][:1]
    good_path = ROOT / "tmp_bsl_good.json"
    bad_path = ROOT / "tmp_bsl_bad.json"
    try:
        good_path.write_text(json.dumps(good))
        bad_path.write_text(json.dumps(bad))
        ok = subprocess.run(
            [sys.executable, str(CHECKS / "builder_scorer_loop.py"),
             "--record", f"@{good_path}", "--json"],
            capture_output=True, text=True, timeout=60, cwd=ROOT)
        assert ok.returncode == 0, ok.stderr
        assert json.loads(ok.stdout)["pass"] is True
        bad_run = subprocess.run(
            [sys.executable, str(CHECKS / "builder_scorer_loop.py"),
             "--record", f"@{bad_path}", "--json"],
            capture_output=True, text=True, timeout=60, cwd=ROOT)
        assert bad_run.returncode == 1, "one round must exit 1"
        assert json.loads(bad_run.stdout)["pass"] is False
    finally:
        good_path.unlink(missing_ok=True)
        bad_path.unlink(missing_ok=True)


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
