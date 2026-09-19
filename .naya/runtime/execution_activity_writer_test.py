#!/usr/bin/env python3
"""Tests for the write-authorized execution-boundary Activity writer."""
from __future__ import annotations

import tempfile
from pathlib import Path

from execution_activity_writer import find_daily_activity, write_execution_activity


def _event() -> tuple[dict, dict]:
    execution = {
        "claim_id": "CL-ACTIVITY-TEST",
        "action_id": "ACT-ACTIVITY-TEST",
        "decision_id": "DEC-ACTIVITY-TEST",
        "authority_id": "AUTH-ACTIVITY-TEST",
        "actor_id": "NAYA-TEST",
        "run_id": "RUN-ACTIVITY-TEST",
        "session_id": "NAYA-20260919-121200-ABCD",
        "governance_state": "AUTHORIZED",
        "authorization_verified": True,
    }
    event = {
        "event_id": "SE-20260919-121200-activity-test-abc123",
        "effective_at": "2026-09-19T19:12:00+00:00",
        "event_type": "activity",
        "subject": "Activity writer test",
        "continuity": {"execution_state": "COMPLETED"},
        "activity_feed_projection": {"summary": "durable writer test"},
    }
    return event, execution


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="activity-writer-test-"))
    event, execution = _event()

    result = write_execution_activity(
        event=event,
        execution=execution,
        next_action="continue",
        successor="NEXT-TEST.md",
        evidence=["receipt:test"],
        activity_root=root,
    )
    assert result["status"] == "CREATED"
    record = find_daily_activity(event["event_id"], activity_root=root)
    assert record is not None
    assert record.parent.name == "09"
    assert record.parent.parent.name == "2026"
    assert record.parent.parent.parent == root
    assert "**EVENT:** `" + event["event_id"] + "`" in record.read_text(encoding="utf-8")

    replay = write_execution_activity(
        event=event,
        execution=execution,
        next_action="continue",
        successor="NEXT-TEST.md",
        evidence=["receipt:test"],
        activity_root=root,
    )
    assert replay["status"] == "REPLAY"

    unauthorized = dict(execution)
    unauthorized["authorization_verified"] = False
    try:
        write_execution_activity(
            event=event,
            execution=unauthorized,
            next_action="continue",
            successor="NEXT-TEST.md",
            evidence=["receipt:test"],
            activity_root=root,
        )
    except AssertionError as exc:
        assert "authorization" in str(exc).lower()
    else:
        raise AssertionError("writer accepted an execution without verified authorization")

    print("PASS — write-authorized Activity writer creates exactly one durable day record, replays idempotently, and refuses unverified execution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
