#!/usr/bin/env python3
"""Repository-level activation gate for the Naya Power executable runtime."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / "NAYA-POWER-RUNTIME-CONTRACT.json"
KERNEL = ROOT / "naya_power_kernel.py"
ORCHESTRATOR_TEST = ROOT / "test_naya_power_orchestrator.py"
HOST_ADAPTER = ROOT / "chatgpt_host_adapter.py"
HOST_ADAPTER_TEST = ROOT / "test_chatgpt_host_adapter.py"
LIVE_HOST = ROOT / "naya_power_live.py"
LIVE_HOST_TEST = ROOT / "test_naya_power_live.py"
EXECUTION_CONTROLLER = ROOT / "execution_controller.py"
RISK_ENGINE = ROOT / "risk_engine.py"
MODEL_TOOL_GATEWAY = ROOT / "model_tool_gateway.py"
MODEL_TOOL_GATEWAY_TEST = ROOT / "test_model_tool_gateway.py"
ADAPTER_CONTRACT = ROOT / "NAYA-POWER-MODEL-ADAPTER-CONTRACT-V1.0.md"
HOST_PROTOCOL = ROOT / "NAYA-POWER-CHATGPT-HOST-INTEGRATION-V1.0.md"


def main() -> int:
    required = [
        CONTRACT, KERNEL, ORCHESTRATOR_TEST, HOST_ADAPTER, HOST_ADAPTER_TEST,
        LIVE_HOST, LIVE_HOST_TEST, EXECUTION_CONTROLLER, RISK_ENGINE,
        MODEL_TOOL_GATEWAY, MODEL_TOOL_GATEWAY_TEST, ADAPTER_CONTRACT, HOST_PROTOCOL,
    ]
    missing = [str(path.relative_to(ROOT.parent.parent)) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"status": "FAIL", "reason": "missing runtime activation artifacts", "missing": missing}, indent=2))
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if contract.get("version") != "1.0.0":
        print(json.dumps({"status": "FAIL", "reason": "unexpected runtime contract version", "version": contract.get("version")}, indent=2))
        return 1

    checks = [
        ("kernel", [sys.executable, str(KERNEL), "--self-test"]),
        ("orchestrator", [sys.executable, str(ORCHESTRATOR_TEST)]),
        ("chatgpt_host_adapter", [sys.executable, str(HOST_ADAPTER_TEST)]),
        ("live_host", [sys.executable, str(LIVE_HOST_TEST)]),
        ("execution_controller", [sys.executable, str(EXECUTION_CONTROLLER), "self-test"]),
        ("risk_engine", [sys.executable, str(RISK_ENGINE), "self-test"]),
        ("model_tool_gateway", [sys.executable, str(MODEL_TOOL_GATEWAY_TEST)]),
    ]
    outputs = {}
    for name, command in checks:
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            return 1
        outputs[name] = result.stdout.strip()

    kernel_result = json.loads(outputs["kernel"])
    receipt = {
        "schema": "naya/runtime-activation-receipt/v1",
        "status": "ACTIVATED_AND_SELF_TESTED",
        "runtime_contract": contract.get("version"),
        "kernel_self_test": f"PASS {kernel_result['passed']}/{kernel_result['total']}",
        "orchestrator_self_test": outputs["orchestrator"],
        "chatgpt_host_adapter_self_test": outputs["chatgpt_host_adapter"],
        "live_host_self_test": outputs["live_host"],
        "execution_controller_self_test": outputs["execution_controller"],
        "risk_engine_self_test": outputs["risk_engine"],
        "model_tool_gateway_self_test": outputs["model_tool_gateway"],
        "model_adapter_contract": "LOADED",
        "chatgpt_host_protocol": "LOADED",
        "execution_state": "READY_FOR_LIVE_CHATGPT_GOVERNED_WORK",
        "next_execution": "Use the live ChatGPT host bridge on a real task, pass consequential actions through the execution claim/gateway boundary, execute only SELECT and AUTHORIZED actions, independently verify the external result, emit the receipt, and continue.",
    }
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
