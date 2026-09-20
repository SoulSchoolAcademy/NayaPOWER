#!/usr/bin/env python3
"""One-command live host bridge for Naya Power.

Input is a JSON request containing base request fields plus model-generated
candidate actions. Candidates are normalized by the ChatGPT host adapter,
then evaluated by the constitutional kernel and no-dead-end orchestrator.
This CLI never claims to have executed an external action; it returns the
selected/refused/escalated decision and the mandatory continuation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from chatgpt_host_adapter import build_request
from naya_power_orchestrator import run_cycle


def load_payload(path: Path | None) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("live host payload must be a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Naya Power live host bridge")
    parser.add_argument("--request", type=Path, help="JSON request file; stdin when omitted")
    args = parser.parse_args()

    payload = load_payload(args.request)
    candidates = payload.pop("candidates", None)
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("payload.candidates must be a non-empty list")

    request = build_request(payload, candidates)
    receipt = run_cycle(request)
    output = {
        "schema": "naya/runtime/live-host-result/v1",
        "host": "ChatGPT",
        "runtime": "Naya Power Runtime Kernel",
        "request": request,
        "receipt": receipt,
        "external_execution": "NOT_EXECUTED_BY_CLI",
        "next_action": receipt["continuation"],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(2)
