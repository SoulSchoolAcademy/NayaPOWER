"""Tests for drink_first_gate.py — every verdict asserted exactly.

Fail-closed contract: any doubt about activation -> a FAIL-* verdict, never PASS.
"""
from datetime import datetime, timedelta, timezone

import pytest

from drink_first_gate import check

LIVE = "e22fde029ee34125547bd9e8e660b951a71fbd63"
NOW = datetime(2026, 10, 9, 14, 55, 0, tzinfo=timezone.utc)


def fresh_receipt(**over):
    r = {
        "schema": "naya.activation.receipt.v1",
        "status": "ACTIVATED",
        "main_sha": LIVE,
        "timestamp": (NOW - timedelta(minutes=30)).isoformat(),
        "activation_protocol": "NayaPOWER Portable Activation Protocol V1",
        "loaded": ["constitution", "design-doctrine", "smart-blocks"],
    }
    r.update(over)
    return r


def test_pass_fresh_receipt_on_live_tip():
    verdict, detail = check(fresh_receipt(), LIVE, now=NOW)
    assert verdict == "PASS", detail


def test_pass_abbreviated_sha_prefix_matches():
    verdict, _ = check(fresh_receipt(main_sha=LIVE[:12]), LIVE, now=NOW)
    assert verdict == "PASS"


def test_fail_tip_moved():
    verdict, detail = check(
        fresh_receipt(main_sha="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
        LIVE, now=NOW)
    assert verdict == "FAIL-TIP-MOVED", detail


def test_fail_unactivated():
    verdict, detail = check(fresh_receipt(status="UNACTIVATED"), LIVE, now=NOW)
    assert verdict == "FAIL-UNACTIVATED", detail


def test_fail_stale_receipt():
    verdict, detail = check(
        fresh_receipt(timestamp=(NOW - timedelta(hours=5)).isoformat()),
        LIVE, max_age_hours=4, now=NOW)
    assert verdict == "FAIL-STALE", detail


def test_pass_at_freshness_boundary():
    verdict, _ = check(
        fresh_receipt(timestamp=(NOW - timedelta(hours=3, minutes=59)).isoformat()),
        LIVE, max_age_hours=4, now=NOW)
    assert verdict == "PASS"


def test_fail_schema_missing_main_sha():
    r = fresh_receipt()
    del r["main_sha"]
    verdict, _ = check(r, LIVE, now=NOW)
    assert verdict == "FAIL-SCHEMA"


def test_fail_schema_empty_loaded():
    verdict, _ = check(fresh_receipt(loaded=[]), LIVE, now=NOW)
    assert verdict == "FAIL-SCHEMA"


def test_fail_schema_not_a_dict():
    verdict, _ = check(["not", "a", "dict"], LIVE, now=NOW)
    assert verdict == "FAIL-SCHEMA"


def test_fail_future_timestamp():
    verdict, _ = check(
        fresh_receipt(timestamp=(NOW + timedelta(hours=1)).isoformat()),
        LIVE, now=NOW)
    assert verdict == "FAIL-SCHEMA"


def test_citation_required_and_present():
    product = "<html><!-- activated %s --></html>" % LIVE
    verdict, _ = check(fresh_receipt(), LIVE, now=NOW,
                       product_text=product, require_citation=True)
    assert verdict == "PASS"


def test_citation_required_and_missing():
    verdict, detail = check(fresh_receipt(), LIVE, now=NOW,
                            product_text="<html>no receipt cited</html>",
                            require_citation=True)
    assert verdict == "FAIL-CITATION", detail


def test_citation_not_required_by_default():
    verdict, _ = check(fresh_receipt(), LIVE, now=NOW,
                       product_text="<html>no receipt cited</html>")
    assert verdict == "PASS"


def test_live_tip_required():
    with pytest.raises(ValueError):
        check(fresh_receipt(), "", now=NOW)
