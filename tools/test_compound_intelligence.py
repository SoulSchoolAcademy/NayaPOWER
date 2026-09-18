#!/usr/bin/env python3
"""Acceptance tests for the Compounding Intelligence Bridge."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import compound_intelligence as ci


def event(consent=True, evidence="VERIFIED"):
    return {
        "event_id": "INT-COMPOUND-001",
        "timestamp": "2026-09-06T07:00:00-07:00",
        "project": "Naya Power",
        "lesson": "Verified lessons should become reusable future intelligence.",
        "source": ["smart-note:SN-001"],
        "evidence_state": evidence,
        "promotion_status": "CANONICAL",
        "what_happened": "A meaningful outcome occurred.",
        "actual_outcome": "The outcome was independently verified.",
        "evidence": ["independent-observation"],
        "collective_consent": consent,
        "smart_note_id": "SN-001",
    }


def test_consent_is_explicit():
    assert ci.has_collective_consent(event(True)) is True
    assert ci.has_collective_consent(event(False)) is False
    assert ci.has_collective_consent({}) is False


def test_candidate_preserves_smart_link_and_privacy():
    candidate = ci.build_candidate(event(False))
    assert candidate is not None
    assert candidate["smart_note_id"] == "SN-001"
    assert candidate["smart_link"] == "intelligence-event:INT-COMPOUND-001"
    assert candidate["visibility"] == "PRIVATE"


def test_daily_only_publishes_verified_consented_lessons():
    events = [event(True), {**event(False), "event_id": "INT-COMPOUND-002"}, {**event(True), "event_id": "INT-COMPOUND-003", "evidence_state": "TESTED"}]
    learnings = [ci.build_candidate(x) for x in events]
    learnings = [x for x in learnings if x]
    report = ci.daily_synthesis(events, learnings, "2026-09-06")
    assert report["counts"]["verified_lessons"] == 2
    assert report["counts"]["collective_lessons"] == 1
    assert report["private_lessons_count"] == 1


def test_run_writes_daily_collective_and_feed_projection():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        old_event = ci.EVENT_DIR
        old_learning = ci.LEARNING_DIR
        old_daily = ci.DAILY_DIR
        old_collective = ci.COLLECTIVE_DIR
        old_feed = ci.FEED_DIR
        try:
            ci.EVENT_DIR = root / "events"
            ci.LEARNING_DIR = root / "learning"
            ci.DAILY_DIR = ci.LEARNING_DIR / "DAILY"
            ci.COLLECTIVE_DIR = ci.LEARNING_DIR / "COLLECTIVE"
            ci.FEED_DIR = root / "feed"
            ci.EVENT_DIR.mkdir(parents=True)
            (ci.EVENT_DIR / "event.json").write_text(json.dumps(event(True)), encoding="utf-8")
            report = ci.run("2026-09-06")
            assert report["counts"]["collective_lessons"] == 1
            assert (ci.DAILY_DIR / "2026-09-06.json").exists()
            assert (ci.COLLECTIVE_DIR / "2026-09-06.md").exists()
            assert (ci.FEED_DIR / "WHAT-WE-LEARNED-2026-09-06.json").exists()
            projection = json.loads((ci.FEED_DIR / "WHAT-WE-LEARNED-2026-09-06.json").read_text(encoding="utf-8"))
            assert projection["feed_type"] == "DAILY_COLLECTIVE_LEARNING"
            assert len(projection["items"]) == 1
        finally:
            ci.EVENT_DIR = old_event
            ci.LEARNING_DIR = old_learning
            ci.DAILY_DIR = old_daily
            ci.COLLECTIVE_DIR = old_collective
            ci.FEED_DIR = old_feed


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Compounding Intelligence Bridge tests passed: {len(tests)}")


if __name__ == "__main__":
    main()
