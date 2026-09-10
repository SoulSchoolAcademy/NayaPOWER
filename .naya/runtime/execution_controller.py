#!/usr/bin/env python3
"""Fail-closed Naya execution control boundary.

This module is the smallest runtime boundary between Naya intent and durable
execution state. It does not execute arbitrary model actions itself; it makes
execution state transitions explicit and rejects transitions that lack the
required claim, observation, evidence, or verification receipt.

States:
  READY -> CLAIMED -> EXECUTING -> OBSERVED -> VERIFIED -> HANDED_OFF

The controller is deliberately deterministic and repository-native so a
future hosted orchestrator can call the same contract without redefining it.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".naya" / "runtime" / "EXECUTION-STATE.json"
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
    if data.get("schema_version") != 1:
        fail("execution state schema is not supported")
    if data.get("status") not in VALID_STATES:
        fail("execution state is invalid")
    return data


def save(data: dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def require_fields(data: dict[str, Any], fields: tuple[str, ...]) -> None:
    missing = []
    for field in fields:
        value = data.get(field)
        if value is None or value == "" or value == [] or value == {}:
            missing.append(field)
    if missing:
        fail("missing required execution fields: " + ", ".join(missing))


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
        require_fields(fields, ("next_action", "handoff"))

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
        require_fields(data, ("next_action", "handoff"))
    history = data.get("history")
    if not isinstance(history, list):
        fail("execution history must be a list")
    return {"status": "GREEN", "execution_status": status, "history_count": len(history)}


def self_test() -> int:
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    try:
        if STATE.exists(): STATE.unlink()
        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="Naya-Test", scope=["test/block"], start_head="test-head")
        transition("EXECUTING")
        transition("OBSERVED", observation="actual runtime observation")
        transition("VERIFIED", evidence=["receipt:test"], verification={"status": "VERIFIED", "method": "test"})
        transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        result = validate()
        assert result["execution_status"] == "HANDED_OFF"
        print("PASS — fail-closed execution state machine GREEN")
        return 0
    finally:
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            return self_test()
        print(json.dumps(validate(), indent=2))
        return 0
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"EXECUTION=RED\nFIRST_DIVERGENCE={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
