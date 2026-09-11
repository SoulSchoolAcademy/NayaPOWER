#!/usr/bin/env python3
"""Executable gateway boundary tests."""
from __future__ import annotations

import json
from pathlib import Path

from execution_controller import STATE, transition
from model_tool_gateway import authorize


def action(risk="L2"):
    return {
        "action_id": "ACT-TEST",
        "action_type": "repository_write",
        "target": "docs/Naya",
        "purpose": "test gateway",
        "risk": risk,
        "protected_baseline": "test-head",
        "observation_target": "changed file state",
        "evidence_requirement": ["commit_sha"],
        "verification_requirement": ["runtime_or_ci"],
    }


def main() -> int:
    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    try:
        if STATE.exists(): STATE.unlink()
        try:
            authorize(action())
        except AssertionError as exc:
            assert "CLAIMED" in str(exc)
        else:
            raise AssertionError("gateway authorized without a claim")

        transition("CLAIMED", claim_id="CL-TEST", block_id="B-TEST", owner="Naya-Test", scope=["docs/Naya"], start_head="test-head")
        result = authorize(action())
        assert result["status"] == "AUTHORIZED"
        assert result["execution_status"] == "EXECUTING"

        invalid = json.loads(json.dumps(action("L1")))
        try:
            authorize(invalid)
        except AssertionError as exc:
            assert "does not match derived risk" in str(exc)
        else:
            raise AssertionError("gateway trusted a caller-supplied lower risk")

        print("PASS 3/3 model tool gateway tests")
        return 0
    finally:
        if original is None:
            if STATE.exists(): STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
