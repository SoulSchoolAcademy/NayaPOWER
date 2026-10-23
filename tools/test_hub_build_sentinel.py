#!/usr/bin/env python3
"""Tests for tools/hub_build_sentinel.py — the Hub build-identity watcher.

Negative controls are the point. On 2026-10-22 a wrong-but-live build
(HTTP 200, every deploy step green) sat on nayanet.live for ~25 minutes
because the only health check asserted liveness. This suite therefore
proves the sentinel FAILS on the stale build: a synthetic stale-monolith
shell MUST diverge and be named, a fallback room MUST diverge, and a dead
sentinel (stale state file) MUST alarm. If the sentinel were mutated to
always return MATCH, the DIVERGED tests below fail — the suite is the
sabotage battery, not a rehearsal of the happy path.

No network: evaluation is driven with fixture pages, and the unreachable
path is driven by a fetcher that raises. The shipped expectations file is
loaded for real, and one test pins its minimum strictness so the file
cannot be quietly weakened into theater.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hub_build_sentinel as s

EXPECTATIONS = s.load_expectations(s.DEFAULT_EXPECTATIONS)


# --------------------------------------------------------------- fixtures


def true_home() -> bytes:
    """A page carrying the true build's identity (measured 2026-10-22)."""
    records = "".join(
        f'{{"id":"SN-{1000 + i}","topics":["Governance"],"topic":"Governance","title":"Note {i}"}},'
        for i in range(150)
    )
    body = (
        "<html><head><title>NayaNET — The Intelligent Hub</title></head><body>"
        "<script>var ROOMS=[{ id: 'factory', name: 'Smart Factory', "
        "accent: 'var(--accent-factory)' }];</script>"
        f"<script>window.NayaWall=[{records}];</script>"
        "<!-- filler to reach the true build's size class -->"
        + ("x" * 1_050_000)
        + "</body></html>"
    )
    return body.encode("utf-8")


def true_room() -> bytes:
    return (
        "<html><head><title>Reports — NayaNET Intelligent Hub</title></head>"
        "<body>Reports room — live numbers, no baked snapshot.</body></html>"
    ).encode("utf-8")


def stale_home() -> bytes:
    """The stale repo monolith's signature (measured 2026-10-22): a baked
    snapshot block as its only note source, 10 cards, monolith-only room
    wiring, no Smart Factory, no wall."""
    cards = "".join(
        f'{{id: "SN-{20 + i}", title: "Early October card {i}"}},' for i in range(10)
    )
    body = (
        "<html><head><title>NayaNET — The Intelligent Hub</title></head><body>"
        '<script>window.NayaContent = { meta: { as_of: "2026-10-02T16:43:37Z", '
        'provenance: "repository-snapshot" }, feed: [' + cards + "] };</script>"
        '<script src="js/mission-room.js"></script>'
        "</body></html>"
    )
    return body.encode("utf-8")


def evaluate(home: bytes, room: bytes) -> dict:
    return s.evaluate(EXPECTATIONS, {"home": home, "room": room})


def failed_ids(outcome: dict) -> set:
    return {r["id"] for r in outcome["failed"]}


# ------------------------------------------------------------------ tests


def test_expectations_are_strict_enough_to_matter():
    """Pin the shipped expectations: weakening any of these into a pass
    for the stale build must break this test."""
    by_id = {c["id"]: c for c in EXPECTATIONS["checks"]}
    assert by_id["note_wall_records"]["min_count"] >= 100
    assert by_id["note_wall_unique_notes"]["min_count"] >= 100
    assert by_id["home_shell_size"]["min_bytes"] >= 1_000_000
    assert by_id["no_monolith_only_room_wiring"]["kind"] == "forbidden"


def test_true_build_matches():
    outcome = evaluate(true_home(), true_room())
    assert outcome["verdict"] == s.VERDICT_MATCH, outcome["failed"]
    assert outcome["suspected_build"] is None


def test_stale_monolith_diverges_and_is_named():
    outcome = evaluate(stale_home(), stale_home())  # room = SPA fallback shell
    assert outcome["verdict"] == s.VERDICT_DIVERGED
    assert "stale repo monolith" in outcome["suspected_build"]
    failed = failed_ids(outcome)
    assert "note_wall_records" in failed
    assert "note_wall_unique_notes" in failed
    assert "smart_factory_room_present" in failed
    assert "no_monolith_only_room_wiring" in failed


def test_unknown_build_diverges_as_unknown():
    outcome = evaluate(b"<html><body>some other site entirely</body></html>", true_room())
    assert outcome["verdict"] == s.VERDICT_DIVERGED
    assert outcome["suspected_build"].startswith("unknown build")


def test_fallback_room_diverges_even_when_home_is_true():
    home = true_home()
    outcome = evaluate(home, home)  # worker serves the shell for the room route
    assert outcome["verdict"] == s.VERDICT_DIVERGED
    assert "room_document_distinct_from_home" in failed_ids(outcome)


def test_unreachable_is_distinct_from_diverged(tmp_path, monkeypatch):
    def boom(url, timeout):
        raise s.FetchError(f"{url}: simulated outage")

    monkeypatch.setattr(s, "fetch_url", boom)
    state = tmp_path / "state.json"
    code = s.main(
        ["check", "--state", str(state), "--expectations", str(s.DEFAULT_EXPECTATIONS)]
    )
    assert code == s.EXIT_UNREACHABLE
    record = json.loads(state.read_text(encoding="utf-8"))
    assert record["verdict"] == s.VERDICT_UNREACHABLE


def test_cli_offline_check_match_exit_0_and_state_written(tmp_path):
    home_f = tmp_path / "home.html"
    room_f = tmp_path / "room.html"
    home_f.write_bytes(true_home())
    room_f.write_bytes(true_room())
    state = tmp_path / "state.json"
    code = s.main(
        [
            "check",
            "--home-file", str(home_f),
            "--room-file", str(room_f),
            "--state", str(state),
            "--expectations", str(s.DEFAULT_EXPECTATIONS),
        ]
    )
    assert code == s.EXIT_MATCH
    record = json.loads(state.read_text(encoding="utf-8"))
    assert record["verdict"] == s.VERDICT_MATCH
    assert record["pages"]["home"]["bytes"] == len(true_home())


def test_cli_offline_check_stale_exit_1(tmp_path):
    stale_f = tmp_path / "stale.html"
    stale_f.write_bytes(stale_home())
    code = s.main(
        [
            "check",
            "--home-file", str(stale_f),
            "--room-file", str(stale_f),
            "--state", str(tmp_path / "state.json"),
            "--expectations", str(s.DEFAULT_EXPECTATIONS),
        ]
    )
    assert code == s.EXIT_DIVERGED


def test_check_state_fresh_stale_and_missing(tmp_path):
    state = tmp_path / "state.json"
    # Missing state file: the sentinel is presumed dead — alarm, never pass.
    code, _ = s.check_state(state, max_age=600)
    assert code == 1
    # Fresh state: alive.
    s.write_state(state, {"ts_epoch": time.time(), "ts_iso": "now", "verdict": "MATCH"})
    code, _ = s.check_state(state, max_age=600)
    assert code == 0
    # Backdated state: a sentinel that stopped running — alarm.
    s.write_state(
        state, {"ts_epoch": time.time() - 3600, "ts_iso": "an hour ago", "verdict": "MATCH"}
    )
    code, message = s.check_state(state, max_age=600)
    assert code == 1
    assert "DEAD" in message
