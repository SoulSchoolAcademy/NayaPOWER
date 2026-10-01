#!/usr/bin/env python3
"""Fail-closed structural gate for the canonical nine-node runtime registry."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BRAIN/03-KERNEL/MANIFEST.json"
REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
REQUIRED = ("status", "entrypoint", "persisted_transitions", "proof_boundary")

def fail(msg: str) -> int:
    print("NODE-RUNTIME-BINDING-GATE FAIL:", msg)
    return 1

def main() -> int:
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
        return fail(f"binding set mismatch: expected={sorted(nodes)} actual={sorted(bindings)}")

    violations = []
    for node in nodes:
        b = bindings[node]
        if not isinstance(b, dict):
            violations.append(f"{node}: binding is not an object")
            continue
        for field in REQUIRED:
            value = b.get(field)
            if not isinstance(value, str) or not value.strip():
                violations.append(f"{node}: missing {field}")

    if violations:
        for v in violations:
            print(" -", v)
        return fail(f"{len(violations)} violation(s)")

    print("NODE-RUNTIME-BINDING-GATE PASS: 9/9 nodes have one canonical binding + persistence + proof boundary")
    return 0

if __name__ == "__main__":
    sys.exit(main())
