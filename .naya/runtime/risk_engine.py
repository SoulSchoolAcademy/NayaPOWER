#!/usr/bin/env python3
"""Deterministic, conservative risk classifier for Naya execution.

Risk is derived from the requested action rather than trusted from the model's
self-declared label. Unknown action types and sensitive targets default to L3.
This is intentionally a small policy engine; it can later be replaced by a
richer policy service without changing the gateway contract.
"""
from __future__ import annotations

import argparse
import json
from typing import Any

SENSITIVE_TERMS = (
    "production", "deploy", "delete", "credential", "secret", "auth",
    "payment", "billing", "database", "migration", "security", "permission",
)
WRITE_TYPES = {"repository_write", "file_write", "database_write", "config_change"}
READ_TYPES = {"read", "search", "inspect", "test", "lint"}


def classify(action: dict[str, Any]) -> str:
    action_type = str(action.get("action_type", "")).strip().lower()
    target = str(action.get("target", "")).strip().lower()
    purpose = str(action.get("purpose", "")).strip().lower()
    combined = f"{action_type} {target} {purpose}"

    if not action_type or not target:
        raise ValueError("risk classification requires action_type and target")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            return self_test()
        raise AssertionError("only self-test is available in this repository-native contract")
    except (AssertionError, ValueError) as exc:
        print(f"RISK=RED\nFIRST_DIVERGENCE={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
