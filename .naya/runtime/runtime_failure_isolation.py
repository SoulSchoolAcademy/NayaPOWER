#!/usr/bin/env python3
"""Capture the first repository-runtime failure when Actions logs are unavailable.

This diagnostic is deliberately non-authoritative: it does not change source state,
persist memory, promote learning, or weaken any gate. It reproduces the canonical
Superbrain gate order (or the system-health contract) and records exact command,
exit code, stdout/stderr, and repository HEAD so a later Naya can repair the first
observed divergence rather than guessing from a red workflow.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_GATE_COMMANDS = [
    ["python", "-m", "py_compile", ".naya/memory/smart_notes_v3.py", ".naya/memory/duplicate_entity_audit.py", ".naya/memory/relationship_graph.py", ".naya/memory/entity_resolution.py", ".naya/memory/contradiction_supersession.py", ".naya/memory/superbrain_health.py", ".naya/memory/retrieval_benchmark.py", ".naya/memory/cis_state.py", ".naya/runtime/continuity_enforcement.py", ".naya/runtime/canonical_event_store.py", ".naya/runtime/canonical_write_inventory.py", ".naya/runtime/outbox.py", ".naya/runtime/restore_context.py", ".naya/runtime/project_execution_contract.py", ".naya/runtime/prompt_architect_contract.py", ".naya/runtime/activation_contract.py", ".naya/runtime/activation_engine.py", ".naya/runtime/customer_activation_mission_boundary.py", ".naya/runtime/customer_activation_loop_test.py", ".naya/runtime/cold_start_activation.py", ".naya/runtime/system_health.py", ".naya/runtime/cct_intelligent_block.py", ".naya/runtime/naya_claim.py", ".naya/runtime/cct_note_event_promotion.py", ".naya/runtime/cct_superbrain_coordination.py"],
    ["python", ".naya/tests/test_canonical_event_store.py"],
    ["python", ".naya/tests/test_canonical_write_inventory.py"],
    ["python", ".naya/runtime/canonical_write_inventory.py"],
    ["python", ".naya/tests/test_cold_start_and_cis.py"],
    ["python", ".naya/memory/smart_notes_v3.py", "index"],
    ["python", ".naya/memory/smart_notes_v3.py", "validate"],
    ["python", ".naya/memory/duplicate_entity_audit.py"],
    ["python", ".naya/memory/relationship_graph.py"],
    ["python", ".naya/tests/test_superbrain_gate.py"],
    ["python", ".naya/tests/test_retrieval_quality.py"],
    ["python", ".naya/tests/test_continuity_enforcement.py"],
    ["python", ".naya/tests/test_project_prompt_contracts.py"],
    ["python", ".naya/tests/test_intelligence_layer.py"],
    ["python", ".naya/tests/test_activation_engine.py"],
    ["python", ".naya/runtime/test_20_pdf_activation.py"],
    ["python", ".naya/runtime/cct_superbrain_coordination_test.py"],
    ["python", ".naya/runtime/customer_activation_loop_test.py"],
    ["python", ".naya/runtime/continuity_enforcement.py", "validate"],
    ["python", ".naya/runtime/project_execution_contract.py", "validate"],
    ["python", ".naya/runtime/prompt_architect_contract.py", "self-test"],
    ["python", ".naya/memory/smart_notes_v3.py", "retrieve", "Superbrain CIS Naya Power", "--limit", "5"],
    ["python", ".naya/memory/retrieval_benchmark.py"],
    ["python", ".naya/memory/superbrain_health.py"],
    ["python", ".naya/memory/cis_state.py", "--day", "2026-08-25", "--timezone", "America/Vancouver"],
]


def git_head() -> str:
    value = os.environ.get("GITHUB_SHA")
    if value:
        return value
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def run(command: list[str]) -> dict[str, object]:
    started = datetime.now(timezone.utc).isoformat()
    try:
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
        return {
            "command": command,
            "started_at": started,
            "exit_code": completed.returncode,
            "stdout": completed.stdout[-12000:],
            "stderr": completed.stderr[-12000:],
        }
    except Exception as exc:
        return {
            "command": command,
            "started_at": started,
            "exit_code": None,
            "stdout": "",
            "stderr": f"diagnostic execution exception: {type(exc).__name__}: {exc}",
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("brain-gate", "system-health"), required=True)
    parser.add_argument("--output", default=".naya/runtime/RUNTIME-FIRST-FAILURE-RECEIPT.json")
    args = parser.parse_args()

    if args.mode == "system-health":
        commands = [["python", ".naya/runtime/system_health.py", "--receipt", ".naya/runtime/SYSTEM-HEALTH-RECEIPT.json"]]
    else:
        commands = BRAIN_GATE_COMMANDS

    results: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None
    for command in commands:
        result = run(command)
        results.append(result)
        if result["exit_code"] != 0:
            first_failure = result
            break

    receipt = {
        "schema": "naya/runtime-first-failure-receipt/v1",
        "status": "FIRST_FAILURE_CAPTURED" if first_failure else "NO_FAILURE_REPRODUCED",
        "mode": args.mode,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "head": git_head(),
        "github_run": os.environ.get("GITHUB_RUN_ID", "UNKNOWN"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "UNKNOWN"),
        "first_failure": first_failure,
        "commands_executed": len(results),
        "results": results,
        "truth_rule": "This receipt records observed command results only. It never converts UNKNOWN into GREEN and never replaces canonical verification.",
    }

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    # Diagnostic must not mask the original gate result.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
