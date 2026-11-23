"""Offline adversarial tests for the public Hub feed publication proof."""
import json
from datetime import datetime, timezone

from tools.prove_hub_feed import inspect, main


def feed(notes, count=None):
    return json.dumps({"count": len(notes) if count is None else count,
                       "notes": notes, "generated_from": "registry@abc123"},
                      separators=(",", ":")).encode()


def note(n, when="2026-11-23T22:00:00Z"):
    return {"id": n, "created_at": when, "layers": [{"body": "Example"}]}


def test_pass_exact_served_artifact():
    raw = feed([note("IB-SMART-NOTE-1"), note("IB-SMART-NOTE-2")])
    r = inspect(raw, raw, max_age_hours=24, required_ids=("IB-SMART-NOTE-2",),
                now=datetime(2026, 11, 23, 23, tzinfo=timezone.utc))
    assert r["status"] == "PASS" and r["count"] == 2


def test_missing_new_note_fails_even_if_live_count_is_valid():
    old = feed([note("1")])
    wanted = feed([note("1"), note("2")])
    r = inspect(old, wanted)
    assert r["status"] == "FAIL" and r["missing_count"] == 1


def test_same_ids_but_stale_body_fails_hash_proof():
    raw = feed([note("1")])
    altered = raw.replace(b"Example", b"Outdated")
    r = inspect(altered, raw)
    assert r["status"] == "FAIL" and "served bytes differ" in str(r["reasons"])


def test_wrong_count_denied():
    assert inspect(feed([note("1")], count=22))["status"] == "FAIL"


def test_duplicate_id_denied():
    assert inspect(feed([note("1"), note("1")]))["status"] == "FAIL"


def test_missing_stable_id_denied():
    assert inspect(feed([{"title": "No id"}]))["status"] == "FAIL"


def test_stale_last_note_denied():
    raw = feed([note("1", "2026-11-14T00:00:00Z")])
    r = inspect(raw, max_age_hours=48, now=datetime(2026, 11, 23, tzinfo=timezone.utc))
    assert r["status"] == "FAIL" and r["newest_age_hours"] > 48


def test_future_clock_spoof_denied():
    raw = feed([note("1", "2026-12-01T00:00:00Z")])
    assert inspect(raw, max_age_hours=48,
                   now=datetime(2026, 11, 23, tzinfo=timezone.utc))["status"] == "FAIL"


def test_bad_source_expected_is_error_not_pass():
    assert inspect(feed([note("1")]), b"not-json")["status"] == "ERROR"


def test_no_timestamp_blocks_age_proof():
    assert inspect(feed([{"id": "1"}]), max_age_hours=1)["status"] == "FAIL"


def test_no_credentials_and_file_url_end_to_end(tmp_path, capsys):
    p = tmp_path / "feed.json"
    p.write_bytes(feed([note("1")]))
    assert main(["--url", p.as_uri(), "--expected-file", str(p), "--require-id", "1"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "PASS"


def test_unreachable_file_exits_error(tmp_path, capsys):
    assert main(["--url", (tmp_path / "missing.json").as_uri()]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "ERROR"
