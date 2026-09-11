#!/usr/bin/env python3
"""Executable tests for the live ChatGPT host bridge."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLI = ROOT / "naya_power_live.py"


def run(payload: dict) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(CLI)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
    )
    return result.returncode, json.loads(result.stdout or result.stderr)


def candidate(cid: str, benefit: int, cost: int, risk: int, auth: str = "approved", boundaries=None, evidence="VERIFIED"):
    return {
        "id": cid,
        "description": cid,
        "expected_benefit": benefit,
        "necessary_cost": cost,
        "risk_loss": risk,
        "authorization": auth,
        "boundary_violations": boundaries or [],
        "evidence_state": evidence,
        "reversible": True,
        "governance_sensitive": False,
    }


def main() -> int:
    base = {
        "request_id": "LIVE-SELFTEST",
        "mission": "Test live host bridge.",
        "context": {"mode": "self-test"},
        "authority": {"actor": "test-harness", "scope": "runtime-evaluation"},
        "constitution_version": "1.0.0",
    }

    code, result = run({**base, "candidates": [
        candidate("best", 95, 10, 5),
        candidate("worse", 80, 20, 10),
    ]})
    assert code == 0 and result["receipt"]["decision"] == "SELECT"
    assert result["receipt"]["selected_candidate"] == "best"
    assert result["next_action"]["action"] == "EXECUTE_SELECTED_ACTION"

    code, result = run({**base, "request_id": "LIVE-ESCALATE", "candidates": [
        candidate("unknown", 100, 0, 0, auth="unknown"),
    ]})
    assert code == 0 and result["receipt"]["decision"] == "ESCALATE"
    assert result["next_action"]["action"] == "ESCALATE_FOR_HUMAN_AUTHORITY"

    code, result = run({**base, "request_id": "LIVE-REFUSE", "candidates": [
        candidate("harm", 100, 0, 0, boundaries=["HUMAN_LIFE_PROTECTED"]),
    ]})
    assert code == 0 and result["receipt"]["decision"] == "REFUSE"
    assert result["next_action"]["action"] == "REFUSE_AND_PROPOSE_SAFE_ALTERNATIVE"

    print("PASS 3/3 live host bridge tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
