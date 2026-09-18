#!/usr/bin/env python3
"""Validate the canonical Execution Mode acknowledgement -> action contract.

This guardrail proves the machine-readable governance contract and its RED/GREEN
acceptance behavior. It cannot prove an AI's private reasoning; it proves that
the repository's canonical law requires forward action or an executable
continuation and that the failure/success states are unambiguous.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".naya" / "naya-context-manifest.json"
LAW = ROOT / ".naya" / "NAYA-ACTION-DELIVERY-LAW.md"
LAW_PATH = ".naya/NAYA-ACTION-DELIVERY-LAW.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def execution_gate(*, next_action_known: bool, executed: bool, continuation_ready: bool) -> bool:
    if not next_action_known:
        return True
    return executed or continuation_ready


def main() -> int:
    if not MANIFEST.is_file():
        fail(f"missing canonical manifest: {MANIFEST}")
    if not LAW.is_file():
        fail(f"missing canonical action-delivery law: {LAW}")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    boot = data.get("boot_order", [])
    subjects = data.get("subjects", {})
    routes = data.get("task_routes", {})

    if LAW_PATH not in boot:
        fail("action-delivery law is not in the canonical boot/read order")
    if boot.index(LAW_PATH) <= boot.index(".naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md"):
        fail("action-delivery law must not precede the canonical Runtime Briefing")

    action_subject = subjects.get("action_delivery")
    if not isinstance(action_subject, dict) or action_subject.get("canonical") != LAW_PATH:
        fail("manifest does not register action_delivery as the canonical subject")

    for route, route_subjects in routes.items():
        if "action_delivery" not in route_subjects:
            fail(f"task route {route!r} omits action_delivery")
        if route_subjects.index("action_delivery") <= route_subjects.index("runtime_briefing"):
            fail(f"task route {route!r} places action_delivery before runtime_briefing")

    if data.get("continuity_rules", {}).get("acknowledgement_without_action_is_unfulfilled") is not True:
        fail("continuity rule acknowledgement_without_action_is_unfulfilled is not enabled")
    if data.get("continuity_rules", {}).get("known_next_action_must_be_executed_or_handed_off_as_runnable_continuation") is not True:
        fail("continuity rule for executable next-action delivery is not enabled")

    law_text = LAW.read_text(encoding="utf-8")
    required = [
        "ACKNOWLEDGEMENT WITHOUT ACTION IS UNFULFILLED ACKNOWLEDGEMENT",
        "NAYA POWER MUST NEVER LEAVE THE USER AT “OKAY, NOW WHAT?”",
        "If Naya can perform the next useful action, Naya performs it.",
        "If a genuine external dependency requires another human turn, Naya automatically prepares the complete next execution command.",
        "UNDERSTAND → INVESTIGATE → RECOMMEND → EXECUTE → VERIFY → DELIVER → CONTINUE OR PREPARE NEXT COMMAND",
        "IF ANY CHECK FAILS: FIX THE RESPONSE BEFORE ENDING IT.",
        "WHY IS THIS NOT A 10?",
    ]
    for phrase in required:
        if phrase not in law_text:
            fail(f"canonical action-delivery law missing required phrase: {phrase}")

    # Machine acceptance proof: known next action + no execution/continuation = RED.
    if execution_gate(next_action_known=True, executed=False, continuation_ready=False):
        fail("omitted action/continuation did not produce RED")
    print("RED PROOF: when a known next action is neither executed nor handed off as a runnable continuation, the Execution Mode gate fails.")

    # Inclusion proof: execution OR a complete continuation = GREEN for this gate.
    if not execution_gate(next_action_known=True, executed=True, continuation_ready=False):
        fail("executed action did not produce GREEN")
    if not execution_gate(next_action_known=True, executed=False, continuation_ready=True):
        fail("runnable continuation did not produce GREEN")
    print("GREEN PROOF: executing the known next action OR supplying the complete runnable continuation satisfies the Execution Mode action gate.")

    print("PASS: action-delivery law is canonical, boot-wired after the Runtime Briefing, present on every task route, and machine-enforced with explicit RED/GREEN acceptance behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
