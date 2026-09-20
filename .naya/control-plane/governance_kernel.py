#!/usr/bin/env python3
"""Compatibility self-test shim for the canonical NayaPOWER governance kernel.

The executable governance implementation lives in:
    .naya/governance/governance_kernel.py

This control-plane path is retained only because the control-plane validator
historically loaded a local ``self_test`` module. It MUST NOT become a second
policy implementation or authority surface.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_TEST = ROOT / ".naya" / "governance" / "test_governance_kernel.py"
CANONICAL_IMPL = ROOT / ".naya" / "governance" / "governance_kernel.py"


def self_test() -> dict[str, object]:
    """Run the canonical governance-kernel test suite; fail closed."""
    if not CANONICAL_IMPL.is_file():
        raise AssertionError("canonical governance kernel is missing")
    if not CANONICAL_TEST.is_file():
        raise AssertionError("canonical governance kernel tests are missing")
    result = subprocess.run(
        [sys.executable, str(CANONICAL_TEST)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + "\n" + result.stderr).strip()
        raise AssertionError(f"canonical governance-kernel tests failed: {detail}")
    return {
        "status": "GREEN",
        "kernel": "NAYAPOWER-GOVERNANCE-KERNEL-V1",
        "implementation": ".naya/governance/governance_kernel.py",
        "tests": "test_governance_kernel.py",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(self_test(), indent=2))
