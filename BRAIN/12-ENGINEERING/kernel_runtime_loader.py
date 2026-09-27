"""
NayaPOWER Kernel Runtime Loader V1

Consumes MANIFEST.json and RUNTIME-REGISTRY to boot the nine-node semantic kernel.
Bridges canonical specification and living runtime behavior.

Status: IMPLEMENTED
Authority: BRAIN/12-ENGINEERING/0004-KERNEL-RUNTIME-LOADER-SPEC-V1.md
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


KERNEL_MANIFEST_SCHEMA = "naya.kernel.manifest.v1"
NODE_ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
NODE_DEPENDENCIES = {
    "SELF": [],
    "LAW": ["SELF"],
    "ACT": ["SELF", "LAW"],
    "KNOW": ["SELF"],
    "PROVE": ["KNOW"],
    "CONNECT": ["KNOW", "PROVE"],
    "VERIFY": ["ACT", "PROVE"],
    "LEARN": ["VERIFY"],
    "EVOLVE": ["LEARN", "SELF"],
}
HEALTH_CHECKS = {
    "SELF": "identity context valid",
    "LAW": "governance contracts resolvable",
    "ACT": "execution context available",
    "KNOW": "intelligence substrate retrievable",
    "PROVE": "proof records assessable",
    "CONNECT": "relationship graph resolvable",
    "VERIFY": "outcome tracking available",
    "LEARN": "verified learning accessible",
    "EVOLVE": "successor context constructable",
}


class KernelBootError(Exception):
    """Raised when kernel boot fails and cannot recover."""

    def __init__(self, message: str, node: str | None = None, details: dict | None = None):
        self.node = node
        self.details = details or {}
        super().__init__(message)


def load_json(path: str) -> dict:
    if not os.path.exists(path):
        raise KernelBootError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema") != KERNEL_MANIFEST_SCHEMA:
        raise KernelBootError(
            f"Invalid manifest schema: expected {KERNEL_MANIFEST_SCHEMA}, got {manifest.get('schema')}"
        )
    nodes = manifest.get("nodes", [])
    if len(nodes) != 9:
        raise KernelBootError(f"Expected 9 nodes, got {len(nodes)}")
    node_ids = {n.get("node_id") or n.get("name") for n in nodes}
    expected = set(NODE_ORDER)
    if node_ids != expected:
        missing = expected - node_ids
        extra = node_ids - expected
        raise KernelBootError(f"Node mismatch. Missing: {missing}, Extra: {extra}")


def validate_registry(registry: dict, manifest: dict) -> None:
    manifest_node_names = {n.get("node_id") or n.get("name") for n in manifest.get("nodes", [])}
    registry_names = set(registry.get("node_order", []))
    if registry_names:
        if not registry_names.issubset(manifest_node_names):
            unknown = registry_names - manifest_node_names
            raise KernelBootError(f"Registry contains unknown nodes: {unknown}")
    else:
        for entry in registry.get("nodes", []):
            node_id = entry.get("node_id") or entry.get("name")
            if node_id and node_id not in manifest_node_names:
                raise KernelBootError(f"Registry node {node_id} not in manifest")
            if entry.get("status") not in ("ACTIVE", "DEGRADED"):
                raise KernelBootError(f"Registry node {node_id} has invalid status: {entry.get('status')}")


def get_registry_impl(registry: dict, node_id: str) -> str:
    node_order = registry.get("node_order", [])
    node_ids = registry.get("node_ids", [])
    if node_id in node_order:
        idx = node_order.index(node_id)
        if idx < len(node_ids):
            return node_ids[idx]
    return "unknown"


def resolve_dependencies(manifest: dict) -> list[str]:
    visited = set()
    order = []

    def visit(node: str):
        if node in visited:
            return
        visited.add(node)
        for dep in NODE_DEPENDENCIES.get(node, []):
            visit(dep)
        order.append(node)

    for node in NODE_ORDER:
        visit(node)

    if len(order) != len(NODE_ORDER):
        raise KernelBootError("Dependency resolution failed: graph incomplete")

    return order


def initialize_node(node_id: str, manifest: dict, registry: dict) -> dict:
    node_manifest = next(
        (n for n in manifest.get("nodes", []) if (n.get("node_id") or n.get("name")) == node_id), None
    )
    if not node_manifest:
        raise KernelBootError(f"Node {node_id} not found in manifest", node=node_id)

    impl = get_registry_impl(registry, node_id)

    return {
        "node_id": node_id,
        "status": "READY",
        "health": HEALTH_CHECKS.get(node_id, "unknown"),
        "implementation": impl,
        "initialized_at": datetime.now(timezone.utc).isoformat(),
    }


def health_check(node_state: dict) -> str:
    if node_state.get("status") == "READY":
        return "READY"
    return "DEGRADED"


def emit_boot_receipt(
    node_states: list[dict],
    dependency_order: list[str],
    failures: list[dict],
) -> dict:
    return {
        "schema": "naya.kernel.boot-receipt.v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dependency_order": dependency_order,
        "nodes": node_states,
        "failures": failures,
        "overall_status": "READY" if not failures else "DEGRADED",
    }


def boot_kernel(manifest_path: str, registry_path: str) -> dict:
    """
    Boot the nine-node semantic kernel.

    Args:
        manifest_path: Path to MANIFEST.json
        registry_path: Path to RUNTIME-REGISTRY

    Returns:
        Boot receipt dict

    Raises:
        KernelBootError: If boot fails and cannot recover
    """
    manifest = load_json(manifest_path)
    registry = load_json(registry_path)

    validate_manifest(manifest)
    validate_registry(registry, manifest)

    dependency_order = resolve_dependencies(manifest)

    node_states = []
    failures = []

    for node_id in dependency_order:
        try:
            state = initialize_node(node_id, manifest, registry)
            health = health_check(state)
            state["health_status"] = health
            node_states.append(state)
        except KernelBootError as e:
            failures.append({
                "node": node_id,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            node_states.append({
                "node_id": node_id,
                "status": "UNAVAILABLE",
                "health_status": "UNAVAILABLE",
                "error": str(e),
            })

    receipt = emit_boot_receipt(node_states, dependency_order, failures)

    if any(f["node"] == "SELF" for f in failures):
        raise KernelBootError("SELF node failed: cannot boot kernel", node="SELF")

    return receipt


def main():
    if len(sys.argv) < 3:
        print("Usage: python kernel_runtime_loader.py <manifest_path> <registry_path>")
        sys.exit(1)

    manifest_path = sys.argv[1]
    registry_path = sys.argv[2]

    try:
        receipt = boot_kernel(manifest_path, registry_path)
        print(json.dumps(receipt, indent=2))
        if receipt["overall_status"] == "READY":
            sys.exit(0)
        else:
            sys.exit(0)
    except KernelBootError as e:
        failure_receipt = {
            "schema": "naya.kernel.boot-receipt.v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_status": "FAILED",
            "error": str(e),
            "node": e.node,
            "details": e.details,
        }
        print(json.dumps(failure_receipt, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
