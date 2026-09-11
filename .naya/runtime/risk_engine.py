#!/usr/bin/env python3
"""Conservative risk classifier; caller-supplied risk never outranks derived risk."""
from __future__ import annotations

import argparse
from typing import Any

SENSITIVE_TERMS = ("production", "deploy", "delete", "credential", "secret", "auth", "payment", "billing", "database", "migration", "security", "permission")
WRITE_TYPES = {"repository_write", "file_write", "database_write", "config_change"}
READ_TYPES = {"read", "search", "inspect", "test", "lint"}


def classify(action: dict[str, Any]) -> str:
    action_type = str(action.get("action_type", "")).strip().lower()
    target = str(action.get("target", "")).strip().lower()
    purpose = str(action.get("purpose", "")).strip().lower()
    if not action_type or not target:
        raise ValueError("risk classification requires action_type and target")
    combined = f"{action_type} {target} {purpose}"
    if any(term in combined for term in SENSITIVE_TERMS):
        return "L3"
    if action_type in READ_TYPES:
        return "L1"
    if action_type in WRITE_TYPES:
        return "L2"
    return "L3"


def self_test() -> int:
    assert classify({"action_type": "inspect", "target": "docs/Naya", "purpose": "read"}) == "L1"
    assert classify({"action_type": "repository_write", "target": "docs/Naya", "purpose": "update"}) == "L2"
    assert classify({"action_type": "repository_write", "target": "production/config", "purpose": "update"}) == "L3"
    assert classify({"action_type": "mystery", "target": "docs/Naya", "purpose": "unknown"}) == "L3"
    print("PASS — conservative risk classifier self-test GREEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["self-test"])
    args = parser.parse_args()
    raise SystemExit(self_test())
