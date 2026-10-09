"""Hardening tests for law-encoding BATCH 2 (2026-10-09).

The independent re-validator scored batch 2 at 8.5 and named 4 gaps.
Each gap gets: a test proving the BYPASS fails post-fix, plus tests
proving the HONORING side still passes (no over-correction).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch2_hardened_20261009.py
Also pytest-compatible (plain assert functions).
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

NOW = "2026-10-09T18:05:00Z"

TECHNICAL = (
    "The GitHub Actions artifact zip endpoint 401s when the authd-surrogate "
    "Bearer is sent through the redirect: the API 302-redirects to a "
    "pre-signed blob URL and the surrogate is rejected at the blob host."
)
PLAIN_GOOD = (
    "Literally what I'm saying: imagine ordering a package, and the "
    "delivery driver is allowed into the building but the door of your "
    "apartment rejects his badge. The first door works, the second "
    "door doesn't."
)


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


def _good_blocker_post():
    return {
        "report_type": "blocker_post",
        "title": "CI artifact download blocked",
        "technical": TECHNICAL,
        "plain_human": PLAIN_GOOD,
        "blocker_x": "artifact zip download 401s at the pre-signed blob URL",
        "unblock_action": "two-hop fetch: take the 302 Location, then fetch "
        "the pre-signed URL with NO Authorization header",
    }


# ------------------------------------------------- Gap 1: relabel bypass
def test_h1_blocker_relabel_status_ping_fails():
    post = _good_blocker_post()
    post["report_type"] = "status_ping"
    del post["technical"]
    del post["plain_human"]
    r = blocker_surfacing.check(_seat(recent_reports=[post]))
    assert r["pass"] is False, r["reasons"]
    assert "not 'blocker_post'" in r["reasons"][0]


def test_h1_blocker_relabel_coordination_note_fails():
    post = _good_blocker_post()
    post["report_type"] = "coordination_note"
    del post["technical"]
    del post["plain_human"]
    r = blocker_surfacing.check(_seat(recent_reports=[post]))
    assert r["pass"] is False, r["reasons"]


def test_h1_blocker_proper_label_still_passes():
    r = blocker_surfacing.check(_seat(recent_reports=[_good_blocker_post()]))
    assert r["pass"] is True, r["reasons"]


# --------------------------------- Gap 2: exempt content guard
def test_h2_long_report_labeled_ping_fails():
    rec = {
        "report_type": "coordination_note",
        "title": "big update",
        "technical": "Subsystem telemetry nominal across the matrix. " * 200,
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_h2_long_message_on_ping_fails():
    rec = {
        "report_type": "status_ping",
        "title": "update",
        "message": "Subsystem telemetry nominal. " * 200,  # ~6000 chars
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_h2_short_technical_field_voids_too():
    # Even a SHORT technical field is report-shaped: a ping never carries
    # one. The exemption voids, the consequential path fails on layers.
    rec = {
        "report_type": "status_ping",
        "title": "update",
        "technical": "db is down",
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_h2_boundary_299_char_message_still_ping():
    rec = {
        "report_type": "status_ping",
        "title": "update",
        "message": "x" * 299,
    }
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert "exemption_voided" not in r["details"]


def test_h2_boundary_300_char_message_voids():
    rec = {
        "report_type": "status_ping",
        "title": "update",
        "message": "x" * 300,
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert r["details"].get("exemption_voided")


def test_h2_one_line_ping_still_passes():
    r = two_layer.check({"report_type": "status_ping", "title": "still working"})
    assert r["pass"] is True, r["reasons"]


def test_h2_voided_but_honored_still_passes():
    # Content decides the path: a ping-labeled record that IS two-layered
    # passes — now via the consequential path.
    rec = {
        "report_type": "status_ping",
        "title": "update",
        "technical": TECHNICAL,
        "plain_human": PLAIN_GOOD,
    }
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert r["details"].get("exemption_voided")


# --------------------------------- Gap 3: heuristic gaming
def test_h3_sprinkled_signal_fails():
    rec = {
        "report_type": "deliverable_report",
        "title": "sprinkle attack",
        "technical": TECHNICAL,
        "plain_human": (
            "The authentication surrogate token propagation mechanism "
            "experienced a 401 authorization rejection at the pre-signed "
            "blob storage endpoint after the API redirect; in other words, "
            "the credential relay subsystem failed validation."
        ),
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert "Flesch" in r["reasons"][0]


def test_h3_paraphrase_with_signal_fails():
    rec = {
        "report_type": "deliverable_report",
        "title": "paraphrase attack",
        "technical": TECHNICAL,
        "plain_human": (
            "In other words: the compressed artifact retrieval endpoint "
            "returns an unauthorized status when the credential delegation "
            "token traverses the redirection to the signed storage URL, "
            "because the delegation credential is refused at the storage host."
        ),
    }
    r = two_layer.check(rec)
    assert r["pass"] is False, r["reasons"]
    assert "Flesch" in r["reasons"][0]


def test_h3_honoring_plain_still_passes():
    rec = {
        "report_type": "deliverable_report",
        "title": "honoring",
        "technical": TECHNICAL,
        "plain_human": PLAIN_GOOD,
    }
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]
    assert r["details"]["plain_flesch"] >= 50.0


def test_h3_bound_vacuous_readable_documents_limit():
    # THE HONEST BOUND, pinned in code: the check proves READABILITY, not
    # truthfulness. A readable-but-vacuous layer passes the mechanics
    # while explaining nothing. High-stakes reports still need a human.
    rec = {
        "report_type": "deliverable_report",
        "title": "vacuous",
        "technical": TECHNICAL,
        "plain_human": (
            "In other words, think of it like a car. For example, imagine "
            "the car is red and it drives down a long road."
        ),
    }
    r = two_layer.check(rec)
    assert r["pass"] is True, r["reasons"]  # documented: readability != truth


# --------------------------------- Gap 4: bool is not int/float
def _shape(typespec, value):
    return {
        "schema": {"required": ["v"], "types": {"v": typespec}},
        "data": {"v": value},
    }


def test_h4_bool_rejected_as_int():
    r = shape_closed.check(_shape("int", True))
    assert r["pass"] is False, r["reasons"]
    assert any("bool" in x for x in r["reasons"]), r["reasons"]


def test_h4_bool_rejected_as_float():
    r = shape_closed.check(_shape("float", False))
    assert r["pass"] is False, r["reasons"]
    assert any("bool" in x for x in r["reasons"]), r["reasons"]


def test_h4_real_int_and_float_still_pass():
    assert shape_closed.check(_shape("int", 1))["pass"] is True
    assert shape_closed.check(_shape("int", 0))["pass"] is True
    assert shape_closed.check(_shape("float", 1.5))["pass"] is True
    assert shape_closed.check(_shape("float", 2))["pass"] is True  # int ok as float


def test_h4_bool_type_still_accepts_bool():
    r = shape_closed.check(_shape("bool", True))
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
