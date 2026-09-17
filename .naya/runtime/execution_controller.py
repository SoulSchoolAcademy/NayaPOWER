#!/usr/bin/env python3
"""Fail-closed execution state machine for Naya Power consequential actions."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".naya" / "runtime" / "EXECUTION-STATE.json"
ACTIVITY_EVENTS_ROOT = ROOT / ".naya" / "memory" / "events"
VALID_STATES = {"READY", "CLAIMED", "EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}
TRANSITIONS = {
    "READY": {"CLAIMED"},
    "CLAIMED": {"EXECUTING"},
    "EXECUTING": {"OBSERVED"},
    "OBSERVED": {"VERIFIED"},
    "VERIFIED": {"HANDED_OFF"},
    "HANDED_OFF": set(),
}


def fail(message: str) -> None:
    raise AssertionError(message)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load() -> dict[str, Any]:
    if not STATE.exists():
        return {"schema_version": 1, "status": "READY", "history": []}
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("status") not in VALID_STATES:
        fail("execution state is invalid")
    return data


def save(data: dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def require_fields(data: dict[str, Any], fields: tuple[str, ...]) -> None:
    missing = [field for field in fields if data.get(field) in (None, "", [], {})]
    if missing:
        fail("missing required execution fields: " + ", ".join(missing))


def _find_activity_event(event_id: str) -> dict[str, Any] | None:
    if not event_id or not ACTIVITY_EVENTS_ROOT.exists():
        return None
    for path in ACTIVITY_EVENTS_ROOT.rglob("SE-*.json"):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if event.get("event_id") == event_id:
            return event
    return None


def _require_activity_event(fields: dict[str, Any], execution_id: str) -> None:
    """Terminal completion requires a real canonical event marked feed-posted."""
    event_id = str(fields.get("activity_event_id") or "")
    if not event_id:
        fail("execution cannot complete without activity_event_id")
    event = _find_activity_event(event_id)
    if event is None:
        fail(f"execution cannot complete: Activity Feed event not found: {event_id}")
    if event.get("execution_id") != execution_id:
        fail("execution cannot complete: Activity event execution_id does not match execution")
    verification = event.get("verification")
    if not isinstance(verification, dict) or verification.get("feed_posted") is not True:
        fail("execution cannot complete: Activity Feed event is not verified as feed_posted")


def transition(target: str, **fields: Any) -> dict[str, Any]:
    data = load()
    current = data["status"]
    if target not in TRANSITIONS[current]:
        fail(f"invalid execution transition: {current} -> {target}")
    if target == "CLAIMED":
        require_fields(fields, ("claim_id", "block_id", "owner", "scope", "start_head"))
    elif target == "EXECUTING":
        require_fields(data, ("claim_id", "block_id", "owner", "scope", "start_head"))
    elif target == "OBSERVED":
        require_fields(fields, ("observation",))
    elif target == "VERIFIED":
        require_fields(fields, ("evidence", "verification"))
    elif target == "HANDED_OFF":
        require_fields(fields, ("next_action", "handoff", "activity_event_id"))
        _require_activity_event(fields, str(data.get("claim_id") or ""))
    event = {"at": now(), "from": current, "to": target, **fields}
    data.update(fields)
    data["status"] = target
    data.setdefault("history", []).append(event)
    save(data)
    return data


def validate(data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or load()
    status = data.get("status")
    if status not in VALID_STATES:
        fail("invalid execution status")
    if status in {"CLAIMED", "EXECUTING", "OBSERVED", "VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("claim_id", "block_id", "owner", "scope", "start_head"))
    if status in {"OBSERVED", "VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("observation",))
    if status in {"VERIFIED", "HANDED_OFF"}:
        require_fields(data, ("evidence", "verification"))
    if status == "HANDED_OFF":
        require_fields(data, ("next_action", "handoff", "activity_event_id"))
        _require_activity_event(data, str(data.get("claim_id") or ""))
    if not isinstance(data.get("history"), list):
        fail("execution history must be a list")
    return {"status": "GREEN", "execution_status": status, "history_count": len(data["history"])}


def self_test() -> int:
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    original_events_root = ACTIVITY_EVENTS_ROOT
    test_events_root = ROOT / ".naya" / "runtime" / "_test_activity_events"
    try:
        if STATE.exists(): STATE.unlink()
        if test_events_root.exists():
            import shutil
            shutil.rmtree(test_events_root)
        globals()["ACTIVITY_EVENTS_ROOT"] = test_events_root

        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="Naya-Test", scope=["test/block"], start_head="test-head")
        transition("EXECUTING")
        transition("OBSERVED", observation="actual runtime observation")
        transition("VERIFIED", evidence=["receipt:test"], verification={"status": "VERIFIED", "method": "test"})

        # Negative proof: substantive work cannot reach terminal handoff without
        # a durable, feed-posted canonical Activity event.
        try:
            transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"}, activity_event_id="SE-20990101-000001-missing")
        except AssertionError as exc:
            assert "Activity Feed event not found" in str(exc)
        else:
            raise AssertionError("missing Activity Feed event was accepted")

        # Positive proof: once the canonical event exists and is marked feed-posted,
        # the same execution may complete and validate.
        event_dir = test_events_root / "2099/01/01/00"
        event_dir.mkdir(parents=True, exist_ok=True)
        event_id = "SE-20990101-000002-feed-proof"
        (event_dir / f"{event_id}.json").write_text(
            json.dumps({
                "event_id": event_id,
                "execution_id": "CL-TEST",
                "event_type": "execution-milestone",
                "verification": {"status": "VERIFIED", "feed_posted": True},
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"}, activity_event_id=event_id)
        result = validate()
        assert result["execution_status"] == "HANDED_OFF"
        try:
            transition("READY")
        except AssertionError:
            pass
        else:
            raise AssertionError("terminal state accepted an invalid transition")
        print("PASS — P0-01 Activity Feed completion gate GREEN")
        return 0
    finally:
        globals()["ACTIVITY_EVENTS_ROOT"] = original_events_root
        if test_events_root.exists():
            import shutil
            shutil.rmtree(test_events_root)
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["self-test", "validate"])
    args = parser.parse_args()
    try:
        if args.command == "self-test": raise SystemExit(self_test())
        print(json.dumps(validate(), indent=2))
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"EXECUTION=RED\nFIRST_DIVERGENCE={exc}")
        raise SystemExit(1)
