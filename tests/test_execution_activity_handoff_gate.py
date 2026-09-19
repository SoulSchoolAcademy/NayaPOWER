#!/usr/bin/env python3
"""Regression proof that missing Team Naya Activity blocks HANDED_OFF."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

import canonical_event_store as CES
import execution_activity_writer as EAW
import execution_controller as EC
from activity_event import build_activity_event
from execution_preflight_gate import approved_preflight


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="activity-handoff-gate-"))
    saved = (
        EC.STATE,
        EC.EVENTS_ROOT,
        EC.INDEX_PATH,
        EC.SESSIONS_ROOT,
        EC.SESSIONS_INDEX_PATH,
        EAW.ACTIVITY_ROOT,
    )
    try:
        EC.STATE = tmp / "EXECUTION-STATE.json"
        EC.EVENTS_ROOT = tmp / "events"
        EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
        EC.SESSIONS_ROOT = tmp / "sessions"
        EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"
        EAW.ACTIVITY_ROOT = tmp / "NAYA-TEAM"

        event_id = "SE-20260919-191200-handoff-gate-test"
        claim_id = "CL-HANDOFF-GATE-TEST"
        action_id = "ACT-HANDOFF-GATE-TEST"
        event = build_activity_event(
            event_id=event_id,
            claim_id=claim_id,
            action_id=action_id,
            decision_id="DEC-HANDOFF-GATE-TEST",
            authority_id="AUTH-HANDOFF-GATE-TEST",
            actor_id="NAYA-TEST",
            subject="Handoff gate test",
            summary="canonical Activity exists but the durable Team Naya record is intentionally missing",
            receipt_id="RCP-HANDOFF-GATE-TEST",
            next_action="continue",
            successor="NEXT-HANDOFF-GATE-TEST.md",
            evidence=["receipt:test"],
            run_id="RUN-HANDOFF-GATE-TEST",
        )
        CES.create_or_replay(event, EC.EVENTS_ROOT, EC.INDEX_PATH)

        EC.STATE.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "VERIFIED",
                    "claim_id": claim_id,
                    "block_id": "B-HANDOFF-GATE-TEST",
                    "owner": "NAYA-TEST",
                    "scope": ["test/activity-handoff"],
                    "start_head": "test-head",
                    "run_id": "RUN-HANDOFF-GATE-TEST",
                    "action": {
                        "action_id": action_id,
                        "decision_id": "DEC-HANDOFF-GATE-TEST",
                    },
                    "observation": "observed",
                    "evidence": ["receipt:test"],
                    "verification": {"status": "VERIFIED", "method": "test"},
                    "activity_event_id": event_id,
                    "preflight": approved_preflight(),
                    "history": [{"from": "OBSERVED", "to": "VERIFIED"}],
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(EAW, "find_daily_activity", return_value=None):
            try:
                EC.transition(
                    "HANDED_OFF",
                    next_action="continue",
                    handoff={"current_state": "VERIFIED"},
                )
            except AssertionError as exc:
                message = str(exc)
                assert "NO DAILY RECORD = NO HANDOFF" in message
            else:
                raise AssertionError("HANDED_OFF succeeded without the durable Team Naya Activity record")

        print("PASS — missing durable Team Naya Activity is a hard HANDED_OFF failure.")
        return 0
    finally:
        (
            EC.STATE,
            EC.EVENTS_ROOT,
            EC.INDEX_PATH,
            EC.SESSIONS_ROOT,
            EC.SESSIONS_INDEX_PATH,
            EAW.ACTIVITY_ROOT,
        ) = saved


if __name__ == "__main__":
    raise SystemExit(main())
