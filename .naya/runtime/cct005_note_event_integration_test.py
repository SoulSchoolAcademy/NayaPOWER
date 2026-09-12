#!/usr/bin/env python3
# CCT-005 integration audit: isolated CI execution fixture.
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cct005_note_event_integration import IntegrationRejected, integrate_verified_note_event


def note_event(status="VERIFIED"):
    return {
        "event_id": "SE-20260829-120000-cct005-integration",
        "event_type": "learning",
        "subject": "verified reusable intelligence",
        "provenance": {"source": "NAYA-A", "kind": "runtime"},
        "evidence": [{"type": "VERIFIED", "ref": "proof-1"}],
        "verification": {"status": status, "receipt": "receipt-1"},
        "effective_at": "2026-08-29T12:00:00-07:00",
        "representations": {
            "naya": {
                "id": "SN-20260829-120000-cct005-integration-naya",
                "canonical_event_id": "SE-20260829-120000-cct005-integration",
                "title": "Reusable intelligence",
                "summary": "A verified reusable lesson.",
                "content": "Use the verified lesson.",
            }
        },
    }


def kwargs(**extra):
    base = dict(
        producer="NAYA-A",
        actor="NAYA-B",
        intended_use="solve-task",
        action="used-block",
        result="task completed",
        classification="SUCCESS",
        evidence=[{"type": "VERIFIED", "ref": "outcome-proof"}],
        confidence=1.0,
        context={"domain": "test"},
        privacy="SCOPED",
        outcome_id="OUT-cct005-integration-001",
    )
    base.update(extra)
    return base


def run(name, fn):
    fn()
    print("PASS", name)


def test_complete_chain():
    event = note_event()
    result = integrate_verified_note_event(event, **kwargs())
    assert result["event_id"] == event["event_id"]
    assert result["block"]["content"]["event_id"] == event["event_id"]
    assert result["outcome"]["provenance"]["source_block"] == result["block"]["block_id"]
    assert result["outcome"]["provenance"]["source_event"] == event["event_id"]
    assert result["value"] > 50.0
    assert "domain" not in result["block"]["content"]


def test_unverified_event_fails_closed():
    try:
        integrate_verified_note_event(note_event("SUPPORTED"), **kwargs())
    except IntegrationRejected:
        return
    raise AssertionError("unverified event was accepted")


def test_missing_smart_note_identity_fails_closed():
    event = note_event(); event["representations"] = {}
    try:
        integrate_verified_note_event(event, **kwargs())
    except IntegrationRejected:
        return
    raise AssertionError("canonical event without Smart Note representation was accepted")


def test_actor_must_be_explicit_consumer():
    try:
        integrate_verified_note_event(
            note_event(),
            **kwargs(actor="NAYA-C"),
            consumers=["NAYA-B"],
        )
    except IntegrationRejected:
        return
    raise AssertionError("unauthorized actor was accepted")


def test_private_context_stays_in_outcome():
    result = integrate_verified_note_event(
        note_event(),
        **kwargs(context={"secret": "do-not-export"}, privacy="PRIVATE", outcome_id="OUT-cct005-private-001"),
    )
    assert result["outcome"]["privacy"] == "PRIVATE"
    assert result["outcome"]["context"]["secret"] == "do-not-export"
    assert "secret" not in result["block"]["content"]


def test_source_event_is_not_mutated():
    event = note_event()
    before = copy.deepcopy(event)
    integrate_verified_note_event(event, **kwargs())
    assert event == before


def test_duplicate_outcome_cannot_inflate_value():
    result = integrate_verified_note_event(note_event(), **kwargs())
    from cct005_value_feedback import value_signal
    assert value_signal([result["outcome"], result["outcome"]]) == result["value"]


def test_unique_outcome_id_allows_distinct_usage():
    from cct005_value_feedback import value_signal
    first = integrate_verified_note_event(note_event(), **kwargs(outcome_id="OUT-cct005-usage-001"))
    second = integrate_verified_note_event(note_event(), **kwargs(outcome_id="OUT-cct005-usage-002", action="reused-block"))
    assert first["outcome"]["outcome_id"] != second["outcome"]["outcome_id"]
    assert value_signal([first["outcome"], second["outcome"]]) == 100.0


if __name__ == "__main__":
    tests = [
        test_complete_chain,
        test_unverified_event_fails_closed,
        test_missing_smart_note_identity_fails_closed,
        test_actor_must_be_explicit_consumer,
        test_private_context_stays_in_outcome,
        test_source_event_is_not_mutated,
        test_duplicate_outcome_cannot_inflate_value,
        test_unique_outcome_id_allows_distinct_usage,
    ]
    for fn in tests:
        run(fn.__name__, fn)
    print(f"PASS {len(tests)} CCT-005 integration tests")
