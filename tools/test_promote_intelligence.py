#!/usr/bin/env python3
"""Dependency-free acceptance tests for Promotion Engine v1."""
from __future__ import annotations

import tempfile
from pathlib import Path

import promote_intelligence as pe


def event(event_id: str, lesson: str, homes=None):
    return {
        "event_id": event_id,
        "timestamp": "2026-08-29T19:00:00-07:00",
        "project": "TestProject",
        "lesson": lesson,
        "source": ["test"],
        "evidence_state": "IMPLEMENTED",
        "promotion_status": "WRITTEN",
        "candidate_homes": homes or ["NAYA_NOTE", "HUMAN_SMART_NOTE"],
        "evidence": ["test-proof"],
        "successor_instruction": "Use the promoted lesson.",
    }


def test_validation():
    errors = pe.validate_event(event("INT-TEST-001", "A durable lesson"), Path("event.json"))
    assert errors == [], errors


def test_fingerprint_and_exact_dedup():
    a = event("INT-TEST-001", "Use verified runtime evidence before claiming completion.")
    b = event("INT-TEST-002", "Use verified runtime evidence before claiming completion.")
    index = pe.load_prior_event_index([(Path("a.json"), a), (Path("b.json"), b)])
    duplicate, score = pe.find_duplicate(a, index)
    assert duplicate == "INT-TEST-002"
    assert score == 1.0


def test_semantic_dedup():
    a = event("INT-TEST-001", "Do not claim completion without verified runtime evidence.")
    b = event("INT-TEST-002", "Do not claim completion without verified runtime evidence in production.")
    index = pe.load_prior_event_index([(Path("a.json"), a), (Path("b.json"), b)])
    duplicate, score = pe.find_duplicate(a, index)
    assert duplicate == "INT-TEST-002", (duplicate, score)
    assert score >= 0.82, score


def test_authority_boundary():
    homes, decision = pe.classify(event("INT-TEST-003", "A governance rule", ["LAW"]))
    assert homes == ["LAW"]
    assert decision == "PROMOTION_PROPOSAL_REQUIRES_AUTHORITY"


def test_idempotent_note_and_feed_paths():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "notes"
        e = event("INT-TEST-004", "A durable note")
        original_root = pe.ROOT
        try:
            pe.ROOT = root
            first = pe.write_note(e, target, "NAYA NOTE")
            before = (target / "INT-TEST-004.md").read_text(encoding="utf-8")
            second = pe.write_note(e, target, "NAYA NOTE")
            after = (target / "INT-TEST-004.md").read_text(encoding="utf-8")
            assert first == second
            assert before == after
        finally:
            pe.ROOT = original_root


def test_verification_is_not_self_certified():
    assert pe.EVIDENCE_STATES == {
        "UNKNOWN", "IMPLEMENTED", "TESTED", "VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"
    }


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Promotion Engine v1 tests passed: {len(tests)}")


if __name__ == "__main__":
    main()
