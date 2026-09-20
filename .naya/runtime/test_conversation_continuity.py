#!/usr/bin/env python3
"""Deterministic contract tests for the conversation continuity vertical slice."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import conversation_continuity as cc
from canonical_event_store import create_or_replay


def sample_project() -> dict:
    project = json.loads(
        (cc.MEMORY / "projects" / "CURRENT-DAILY-PROJECT.json").read_text(
            encoding="utf-8"
        )
    )
    return project


def test_event_shape() -> None:
    event = cc.build_conversation_event(
        title="Vertical Slice Test",
        summary="Conversation intelligence must compound.",
        what_happened="A durable mission-state decision was captured.",
        what_we_learned=["Conversation is the live intelligence feed."],
        what_changed=["The Hub mission is now explicit."],
        next_action="Run the vertical slice in an authorized execution plane.",
        effective_at="2026-09-18T12:00:00+00:00",
        source_event_id="CONVERSATION-TEST-001",
        project=sample_project(),
    )
    assert event["event_type"] == "smart-note"
    assert set(event["representations"]) == {"shawn", "naya", "machine"}
    assert len({x["id"] for x in event["representations"].values()}) == 3
    assert all(x["canonical_event_id"] == event["event_id"] for x in event["representations"].values())
    assert event["continuity"]["next_execution_path"] == cc.NEXT_EXECUTION
    assert event["permissions"]["scope"] == "NAYAPOWER"


def test_idempotent_canonical_write() -> None:
    event = cc.build_conversation_event(
        title="Idempotency Test",
        summary="The same conversation must not create duplicates.",
        what_happened="A replay was requested.",
        what_we_learned=["Canonical writes must be repeat-safe."],
        what_changed=["Replay is expected to resolve to the original event."],
        next_action="Verify replay status.",
        effective_at="2026-09-18T12:01:00+00:00",
        source_event_id="CONVERSATION-TEST-IDEMPOTENT",
        project=sample_project(),
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "events"
        index = root / "INDEX.json"
        first = create_or_replay(event, root, index)
        second = create_or_replay(event, root, index)
        assert first["status"] == "CREATED"
        assert second["status"] == "REPLAY"
        assert len(list(root.rglob("SE-*.json"))) == 1


def test_next_execution_is_independently_consumable() -> None:
    successor = cc.consume_next_execution(cc.NEXT_EXECUTION)
    assert successor["project"]
    assert successor["current_state"]
    assert successor["current_objective"]
    assert successor["next_action"]
    assert successor["execution_instructions"]
    assert successor["success_criteria"]
    assert successor["verification_requirements"]


def self_test() -> int:
    test_event_shape()
    test_idempotent_canonical_write()
    test_next_execution_is_independently_consumable()
    print("PASS — conversation continuity contract")
    print("PASS — Shawn/Naya/Machine representations")
    print("PASS — canonical idempotency")
    print("PASS — independent successor consumption")
    print("NOTE — live runtime observation still requires an authorized execution plane")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test())
