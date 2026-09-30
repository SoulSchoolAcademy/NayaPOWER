#!/usr/bin/env python3
"""Node-binding gate (GAP A enforcement).

Every node in the canonical nine-node manifest (BRAIN/03-KERNEL/MANIFEST.json)
MUST have exactly one binding in BRAIN/03-KERNEL/NODE-BINDINGS.json with:
  - an executable (code path that runs the node)
  - a persisted_transitions store (where the node's transitions are recorded)

SPEC_ONLY bindings are permitted but MUST carry an explicit activation_event
and MUST NOT be presented as active. A node with no binding, or a binding
without an executable, fails the gate.

Usage: python scripts/check-node-bindings.py
Exit 0 = gate passes. Exit 1 = gate fails (prints violations).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "BRAIN" / "03-KERNEL" / "MANIFEST.json"
BINDINGS_PATH = ROOT / "BRAIN" / "03-KERNEL" / "NODE-BINDINGS.json"

ALLOWED_ACTIVATION = {"ACTIVE", "PARTIAL", "SPEC_ONLY"}


def fail(msg: str) -> int:
    print(f"NODE-BINDING-GATE FAIL: {msg}")
    return 1


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        bindings_doc = json.loads(BINDINGS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        return fail(f"missing required file: {exc.filename}")
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    manifest_nodes = [n["name"] for n in manifest.get("nodes", [])]
    if len(manifest_nodes) != 9:
        return fail(f"manifest must declare exactly nine nodes, found {len(manifest_nodes)}")

    bindings = bindings_doc.get("bindings", [])
    by_node: dict[str, list[dict]] = {}
    for b in bindings:
        by_node.setdefault(b.get("node"), []).append(b)

    violations = 0
    for node in manifest_nodes:
        entries = by_node.get(node, [])
        if len(entries) == 0:
            violations += fail(f"node {node}: no binding (GAP A — node unbound)")
            continue
        if len(entries) > 1:
            violations += fail(f"node {node}: {len(entries)} bindings, exactly one required")
            continue
        b = entries[0]
        if not b.get("executable"):
            violations += fail(f"node {node}: binding has no executable")
        if not b.get("persisted_transitions"):
            violations += fail(f"node {node}: binding has no persisted_transitions store")
        activation = b.get("activation")
        if activation not in ALLOWED_ACTIVATION:
            violations += fail(
                f"node {node}: activation must be one of {sorted(ALLOWED_ACTIVATION)}, got {activation!r}"
            )
        if activation == "SPEC_ONLY" and not b.get("activation_event"):
            violations += fail(f"node {node}: SPEC_ONLY binding must name its activation_event")

    bound_names = set(by_node)
    for node in sorted(bound_names - set(manifest_nodes)):
        violations += fail(f"binding for unknown node {node} (not in manifest)")

    if violations:
        print(f"NODE-BINDING-GATE: {violations} violation(s)")
        return 1
    spec_only = sorted(n for n in manifest_nodes if by_node[n][0]["activation"] == "SPEC_ONLY")
    print(f"NODE-BINDING-GATE PASS: 9/9 nodes bound" + (f" ({len(spec_only)} SPEC_ONLY: {', '.join(spec_only)})" if spec_only else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
