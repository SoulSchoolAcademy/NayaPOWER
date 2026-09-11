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
ADAPTER_CONTRACT = ROOT / "NAYA-POWER-MODEL-ADAPTER-CONTRACT-V1.0.md"


def main() -> int:
    required = [CONTRACT, KERNEL, ORCHESTRATOR_TEST, ADAPTER_CONTRACT]
    missing = [str(path.relative_to(ROOT.parent.parent)) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"status": "FAIL", "reason": "missing runtime activation artifacts", "missing": missing}, indent=2))
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if contract.get("version") != "1.0.0":
        print(json.dumps({"status": "FAIL", "reason": "unexpected runtime contract version", "version": contract.get("version")}, indent=2))
        return 1

    kernel = subprocess.run([sys.executable, str(KERNEL), "--self-test"], text=True, capture_output=True)
    if kernel.returncode != 0:
        print(kernel.stdout)
        print(kernel.stderr)
        return 1
    kernel_result = json.loads(kernel.stdout)

    orchestrator = subprocess.run([sys.executable, str(ORCHESTRATOR_TEST)], text=True, capture_output=True)
    if orchestrator.returncode != 0:
        print(orchestrator.stdout)
        print(orchestrator.stderr)
        return 1

    receipt = {
        "schema": "naya/runtime-activation-receipt/v1",
        "status": "ACTIVATED_AND_SELF_TESTED",
        "runtime_contract": contract.get("version"),
        "kernel_self_test": f"PASS {kernel_result['passed']}/{kernel_result['total']}",
        "orchestrator_self_test": orchestrator.stdout.strip(),
        "model_adapter_contract": "LOADED",
        "execution_state": "READY_FOR_REAL_MODEL_ADAPTER",
        "next_execution": "Connect one real model adapter, normalize its candidates, pass them through the kernel, execute only SELECT, independently verify the result, and record the receipt.",
    }
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
