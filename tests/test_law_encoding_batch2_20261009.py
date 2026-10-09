"""Tests for the 2026-10-09 law-encoding BATCH 2.

Every law encoded this batch gets the same proof contract:
  - a VIOLATING fixture makes the check FAIL (the encoding fires), and
  - an HONORING fixture makes the check PASS (the encoding stays quiet).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch2_20261009.py
Also pytest-compatible (plain assert functions).

Covers:
  - two_layer.py       (Two-Layer Communication Law)
  - blocker_surfacing.py (Proactive Blocker Surfacing)
  - shape_closed.py    (Fail Closed on Shape — the validator's meta-law)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import (  # noqa: E402
    blocker_surfacing,
    shape_closed,
    two_layer,
)

NOW = "2026-10-09T17:50:00Z"


# ---------------------------------------------------------------- fixtures
def _good_two_layer_report():
    return {
        "report_type": "deliverable_report",
        "title": "Batch 2 encoded",
        "technical": (
            "Encoded the Two-Layer Communication Law as tools/protocol/checks/"
            "two_layer.py with fail-closed shape validation, token-Jaccard "
            "copy detection, and layer-order enforcement on full_text. "
            "21 tests green."
        ),
        "plain_human": (
            "Literally what I'm saying: the computer now reads every report "
            "before it goes out and refuses to send one that is all jargon "
            "with no plain explanation. Think of it like a spell-checker, "
            "but for clarity — no plain words, no send."
        ),
        "audience": "shawn",
        "seat": "naya-5",
    }


def _good_blocker_post():
    return {
        "report_type": "blocker_post",
        "title": "CI artifact download blocked",
        "technical": (
            "The GitHub Actions artifact zip endpoint 401s when the "
            "authd-surrogate Bearer is sent through the redirect: the API "
            "302-redirects to a pre-signed blob URL and the surrogate is "
            "rejected at the blob host."
        ),
        "plain_human": (
            "Literally what I'm saying: imagine ordering a package, and the "
            "delivery driver is allowed into the building but the door of "
            "your apartment rejects his badge. The first door works, the "
            "second door doesn't."
        ),
        "blocker_x": "artifact zip download 401s at the pre-signed blob URL",
        "unblock_action": (
            "two-hop fetch: take the 302 Location from the API call, then "
            "fetch the pre-signed URL with NO Authorization header"
        ),
    }


# ---------------------------------------------------------------- two_layer
def test_two_layer_technicals_only_fails():
    rec = _good_two_layer_report()
    del rec["plain_human"]
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_empty_plain_fails():
    rec = _good_two_layer_report()
    rec["plain_human"] = "   "
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_copypaste_plain_fails():
    rec = _good_two_layer_report()
    rec["plain_human"] = rec["technical"] + " done"
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_no_signal_plain_fails():
    rec = _good_two_layer_report()
    rec["plain_human"] = (
        "The implementation completed successfully with all subsystems "
        "operational and the validation matrix showing comprehensive coverage "
        "across the entire deployment surface area."
    )
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_unknown_type_fails():
    rec = _good_two_layer_report()
    rec["report_type"] = "executive_update"
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_reversed_order_fails():
    rec = _good_two_layer_report()
    rec["full_text"] = (
        "LITERALLY WHAT I'M SAYING: plain words here.\n"
        "THE TECHNICAL: technical words here."
    )
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_two_layer_proper_passes():
    r = two_layer.check(_good_two_layer_report())
    assert r["pass"] is True, r["reasons"]


def test_two_layer_full_text_order_passes():
    rec = _good_two_layer_report()
    rec["full_text"] = (
        "## THE TECHNICAL\ntechnical details here, all of them.\n\n"
        "## LITERALLY WHAT I'M SAYING\n"
        "what this means, in other words: plain explanation for everyone."
    )
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]


def test_two_layer_exempt_ping_passes():
    r = two_layer.check({"report_type": "status_ping", "title": "still working"})
    assert r["pass"] is True, r["reasons"]


def test_two_layer_malformed_record_fails():
    r = two_layer.check("not a dict")
    assert r["pass"] is False, r["reasons"]


# ---------------------------------------------------------------- blocker_surfacing
def _seat(**kw):
    rec = {
        "seat": "naya-5",
        "status": "blocked",
        "checked_at": NOW,
        "stall_window_hours": 3,
        "recent_reports": [],
    }
    rec.update(kw)
    return rec


def test_blocker_blocked_with_silence_fails():
    r = blocker_surfacing.check(_seat())
    assert r["pass"] is False, r["reasons"]


def test_blocker_missing_unblock_action_fails():
    post = _good_blocker_post()
    del post["unblock_action"]
    r = blocker_surfacing.check(_seat(recent_reports=[post]))
    assert r["pass"] is False, r["reasons"]


def test_blocker_missing_x_fails():
    post = _good_blocker_post()
    post["blocker_x"] = ""
    r = blocker_surfacing.check(_seat(recent_reports=[post]))
    assert r["pass"] is False, r["reasons"]


def test_blocker_technicals_only_post_fails():
    post = _good_blocker_post()
    del post["plain_human"]
    r = blocker_surfacing.check(_seat(recent_reports=[post]))
    assert r["pass"] is False, r["reasons"]


def test_blocker_stalled_working_fails():
    r = blocker_surfacing.check(
        _seat(status="working", last_progress_at="2026-10-09T07:00:00Z")
    )
    assert r["pass"] is False, r["reasons"]


def test_blocker_working_no_progress_ts_fails():
    r = blocker_surfacing.check(_seat(status="working"))
    assert r["pass"] is False, r["reasons"]


def test_blocker_unknown_status_fails():
    r = blocker_surfacing.check(_seat(status="busy"))
    assert r["pass"] is False, r["reasons"]


def test_blocker_proper_post_passes():
    r = blocker_surfacing.check(_seat(recent_reports=[_good_blocker_post()]))
    assert r["pass"] is True, r["reasons"]


def test_blocker_working_with_progress_passes():
    r = blocker_surfacing.check(
        _seat(status="working", last_progress_at="2026-10-09T17:00:00Z")
    )
    assert r["pass"] is True, r["reasons"]


def test_blocker_done_passes():
    r = blocker_surfacing.check(_seat(status="done"))
    assert r["pass"] is True, r["reasons"]


# ---------------------------------------------------------------- shape_closed
def _shape_record(**kw):
    schema = {
        "required": ["name", "tags"],
        "types": {"name": "str", "tags": "list", "n": "int"},
        "non_empty": ["name", "tags"],
        "min_length": {"name": 3},
        "allowed": {"kind": ["a", "b"]},
    }
    data = {"name": "abc", "tags": ["x"], "n": 1, "kind": "a"}
    data.update(kw.pop("data", {}))
    return {"schema": schema, "data": data}


def test_shape_absent_field_fails():
    rec = _shape_record()
    del rec["data"]["name"]
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_none_field_fails():
    rec = _shape_record()
    rec["data"]["name"] = None
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_wrong_type_fails():
    rec = _shape_record()
    rec["data"]["tags"] = "x"
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_empty_string_fails():
    rec = _shape_record()
    rec["data"]["name"] = "   "
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_min_length_fails():
    rec = _shape_record()
    rec["data"]["name"] = "ab"
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_unknown_enum_fails():
    rec = _shape_record()
    rec["data"]["kind"] = "c"
    r = shape_closed.check(rec)
    assert r["pass"] is False, r["reasons"]


def test_shape_good_record_passes():
    r = shape_closed.check(_shape_record())
    assert r["pass"] is True, r["reasons"]


# ---------------------------------------------------------------- runner
def main() -> int:
    fns = sorted((n, f) for n, f in globals().items()
                 if n.startswith("test_") and callable(f))
    failures = []
    for name, fn in fns:
        try:
            fn()
            print(f"  ok {name}")
        except AssertionError as e:
            failures.append(name)
            print(f"  FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failures.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - len(failures)}/{len(fns)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
