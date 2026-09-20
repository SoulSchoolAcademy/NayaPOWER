#!/usr/bin/env python3
"""Continuous Naya Power decision bridge.

Wraps the deterministic constitutional kernel and guarantees a machine-readable
continuation action for every decision outcome. This is the seam where a real
model adapter can be connected without allowing the model to bypass Naya Power.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from naya_power_kernel import evaluate


def continuation_for(receipt: dict[str, Any]) -> dict[str, str]:
    decision = receipt["decision"]
    if decision == "SELECT":
        return {
            "action": "EXECUTE_SELECTED_ACTION",
            "instruction": "Execute only the selected candidate, then independently verify the external outcome.",
        }
    if decision == "ESCALATE":
        reasons = " ".join(
            " ".join(item.get("reasons", []))
            for item in receipt["candidate_evaluations"]
            if item["decision"] == "ESCALATE"
        )
        if "evidence" in reasons.lower():
            return {
                "action": "GATHER_OR_VERIFY_EVIDENCE",
                "instruction": "Resolve the missing or insufficient evidence; do not guess; then re-run the decision gate.",
            }
        return {
            "action": "ESCALATE_FOR_HUMAN_AUTHORITY",
            "instruction": "Obtain the missing authority or context; do not self-authorize; then re-run the decision gate.",
        }
    return {
        "action": "REFUSE_AND_PROPOSE_SAFE_ALTERNATIVE",
        "instruction": "Do not execute the rejected action; generate a safe eligible alternative and re-run the decision gate.",
    }


def run_cycle(request: dict[str, Any], model_adapter: Callable[[dict[str, Any]], list[dict[str, Any]]] | None = None) -> dict[str, Any]:
    if model_adapter is not None:
        request = dict(request)
        request["candidates"] = model_adapter(request)
    receipt = evaluate(request)
    receipt["continuation"] = continuation_for(receipt)
    receipt["flow_state"] = "CONTINUE"
    return receipt


def demo_adapter(_: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic adapter used only for the executable integration smoke test."""
    return [
        {
            "id": "verified-improvement",
            "description": "Run the verified next improvement and inspect the result.",
            "expected_benefit": 90,
            "necessary_cost": 20,
            "risk_loss": 5,
            "authorization": "approved",
            "boundary_violations": [],
            "evidence_state": "VERIFIED",
            "reversible": True,
            "governance_sensitive": False,
        },
        {
            "id": "unverified-shortcut",
            "description": "Take an unverified shortcut.",
            "expected_benefit": 95,
            "necessary_cost": 5,
            "risk_loss": 30,
            "authorization": "approved",
            "boundary_violations": [],
            "evidence_state": "IMPLEMENTED",
            "reversible": False,
            "governance_sensitive": False,
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--demo-adapter", action="store_true")
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    result = run_cycle(request, demo_adapter if args.demo_adapter else None)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
