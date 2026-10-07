#!/usr/bin/env python3
"""Fail-closed structural + behavioral-contract gate for the canonical nine-node runtime registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BRAIN/03-KERNEL/MANIFEST.json"
REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
REQUIRED = ("status", "entrypoint", "persisted_transitions", "proof_boundary")
BEHAVIORAL_REQUIRED = ("test", "mode", "falsifier", "production_boundary")


def fail(msg):
    print("NODE-RUNTIME-BINDING-GATE FAIL:", msg)
    return 1


def main():
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return fail(str(exc))

    nodes = [n["name"] for n in manifest.get("nodes", [])]
    if len(nodes) != 9 or len(set(nodes)) != 9:
        return fail(f"manifest must declare exactly nine unique nodes; got {nodes!r}")

    bindings = registry.get("node_runtime_bindings")
    if not isinstance(bindings, dict):
        return fail("node_runtime_bindings missing or not an object")
    if set(bindings) != set(nodes):
        return fail(
            f"binding set mismatch: expected={sorted(nodes)} actual={sorted(bindings)}"
        )

    violations = []
    for node in nodes:
        binding = bindings[node]
        if not isinstance(binding, dict):
            violations.append(f"{node}: binding is not an object")
            continue

        for field in REQUIRED:
            value = binding.get(field)
            if not isinstance(value, str) or not value.strip():
                violations.append(f"{node}: missing {field}")

        contract = binding.get("behavioral_contract")
        if not isinstance(contract, dict):
            violations.append(f"{node}: missing behavioral_contract")
            continue

        for field in BEHAVIORAL_REQUIRED:
            value = contract.get(field)
            if not isinstance(value, str) or not value.strip():
                violations.append(f"{node}: behavioral_contract missing {field}")

        test_path = contract.get("test")
        if isinstance(test_path, str) and test_path.strip():
            if not (ROOT / test_path).is_file():
                violations.append(
                    f"{node}: behavioral_contract.test does not exist: {test_path}"
                )

        boundary = str(contract.get("production_boundary") or "").lower()
        if "production" not in boundary or "not" not in boundary:
            violations.append(
                f"{node}: behavioral_contract.production_boundary must explicitly deny production proof"
            )

    if violations:
        for violation in violations:
            print(" -", violation)
        return fail(f"{len(violations)} violation(s)")

    print(
        "NODE-RUNTIME-BINDING-GATE PASS: 9/9 nodes have one canonical binding + "
        "persistence + explicit behavioral contract + proof boundary"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
