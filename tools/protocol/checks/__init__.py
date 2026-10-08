"""Executable law checks for the Team Naya operating protocol.

Each module enforces one ratified law from tools/protocol/protocol_manifest.json.
Pattern (follows cold_start_gate.py):
  - check(record: dict) -> dict  : pure validation, returns
    {"pass": bool, "reasons": [str], "details": {...}}
  - main()                       : argparse CLI, --record JSON (or @file),
    --json output, exit 0 on PASS / 1 on FAIL.

Fail-closed: any malformed input fails with a specific reason.
A check verifies compliance; it never grants authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_record(spec: str) -> dict:
    """Load a record from a JSON string or @filepath."""
    text = Path(spec[1:]).read_text() if spec.startswith("@") else spec
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("record must be a JSON object")
    return data


def result(passed: bool, reasons: list[str], details: dict | None = None) -> dict:
    return {
        "pass": passed,
        "reasons": reasons,
        "details": details or {},
    }


def emit(result_dict: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(result_dict, indent=2))
    else:
        status = "PASS" if result_dict["pass"] else "FAIL"
        print(status)
        for r in result_dict["reasons"]:
            print(f"  - {r}")
    return 0 if result_dict["pass"] else 1


def fail(reason: str, details: dict | None = None) -> dict:
    return result(False, [reason], details)
