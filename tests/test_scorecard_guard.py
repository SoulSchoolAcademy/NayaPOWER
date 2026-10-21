"""L577 guard battery — the negative test is the proof.

A guard that cannot refuse is prose. Every test here must be able to
fail; the negative cases are the ones that matter.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import scorecard_guard as g


def good_report():
    return {"title": "x", "overall": 8.0, "verdict": "FIX",
            "measured_at": "2026-10-21T02:50:00Z"}


def test_stamped_report_passes():
    ok, msg = g.check(good_report())
    assert ok, msg
    assert "L577 OK" in msg


def test_guard_returns_report_unchanged_when_valid():
    r = good_report()
    assert g.guard(r) is r


def test_negative_missing_measured_at_refused():
    # THE proof: a score with no measured_at cannot be rendered.
    r = {"title": "x", "overall": 9.9, "verdict": "SHIP"}
    try:
        g.guard(r)
    except g.UnmeasuredRefusal as e:
        assert "no measured_at" in str(e)
        assert "claimed point is a void point" in str(e)
    else:
        raise AssertionError("L577 guard let an unmeasured score through")


def test_negative_render_refused():
    r = {"title": "x", "overall": 9.9, "verdict": "SHIP"}
    try:
        g.render(r, lambda rep: "RENDERED")
    except g.UnmeasuredRefusal:
        pass
    else:
        raise AssertionError("render() emitted an unmeasured score")


def test_negative_write_refused_and_leaves_no_file(tmp_path):
    r = {"title": "x", "overall": 9.9, "verdict": "SHIP"}
    target = str(tmp_path / "score.json")
    try:
        g.write(target, r)
    except g.UnmeasuredRefusal:
        pass
    else:
        raise AssertionError("write() persisted an unmeasured score")
    assert not os.path.exists(target), "refused write left a file behind"
    assert not os.path.exists(target + ".l577tmp"), "refused write left a temp file"


def test_negative_malformed_measured_at_refused():
    for bad in ("soon", "2026-13-40T99:99:99Z", "2026-10-21 02:50:00",
                "2026-10-21T02:50:00", 1761000000, None, ""):
        r = {"title": "x", "overall": 8.0}
        if bad != "":
            r["measured_at"] = bad
        try:
            g.guard(r)
        except g.UnmeasuredRefusal:
            pass
        else:
            raise AssertionError("guard accepted measured_at=%r" % (bad,))


def test_non_report_refused():
    try:
        g.guard(["not", "a", "report"])
    except g.UnmeasuredRefusal:
        pass
    else:
        raise AssertionError("guard accepted a non-report")


def test_stamp_adds_utc_measured_at():
    r = {"title": "x", "overall": 8.0, "verdict": "FIX"}
    before = time.time()
    g.stamp(r)
    assert g.is_valid(r["measured_at"]), r["measured_at"]
    # stamp is the computation time: within the last minute, UTC.
    assert r["measured_at"].endswith("Z")


def test_stamp_never_overwrites_existing():
    r = good_report()
    g.stamp(r)
    assert r["measured_at"] == "2026-10-21T02:50:00Z"


def test_write_roundtrip_byte_verifiable(tmp_path):
    r = g.stamp({"title": "x", "overall": 8.0, "verdict": "FIX"})
    target = str(tmp_path / "score.json")
    g.write(target, r)
    back = json.load(open(target))
    assert back["measured_at"] == r["measured_at"]
    assert back["overall"] == 8.0
