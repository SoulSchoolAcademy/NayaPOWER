"""Manifest-driven NayaPOWER runtime bootstrap.

The executable kernel consumes the canonical BRAIN manifest and the canonical
nine-node functional contract at boot. Missing or incomplete contracts fail
closed rather than silently degrading runtime behavior.
"""

from __future__ import annotations

import json
from pathlib import Path


CANONICAL_NODE_NAMES = (
    "SELF",
    "LAW",
    "ACT",
    "KNOW",
    "PROVE",
    "CONNECT",
    "VERIFY",
    "LEARN",
    "EVOLVE",
)

REQUIRED_FUNCTIONAL_CONTRACT_FIELDS = (
    "id",
    "name",
    "purpose",
    "owns",
    "must_accept",
    "must_return",
    "invariants",
    "fail_closed",
    "proof_requirements",
    "handoff",
    "optimization",
)


def find_repository_root(start: Path | None = None) -> Path:
    cursor = Path(start or __file__).resolve()
    if cursor.is_file():
        cursor = cursor.parent

    for candidate in (cursor, *cursor.parents):
        manifest = candidate / "BRAIN/03-KERNEL/MANIFEST.json"
        if manifest.is_file():
            return candidate

    raise RuntimeError(
        "BRAIN manifest not found; runtime boot fails closed rather than "
        "inventing a fallback node configuration"
    )


def _read_json(path: Path, *, label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"{label} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid {label} JSON: {path}") from exc


def load_functional_contract(root: Path | None = None) -> dict:
    repository_root = find_repository_root(root)
    manifest_path = repository_root / "BRAIN/03-KERNEL/MANIFEST.json"
    manifest = _read_json(manifest_path, label="BRAIN manifest")

    contract_ref = manifest.get("functional_contract")
    if not contract_ref:
        raise RuntimeError(
            "BRAIN manifest is missing its canonical functional contract"
        )

    contract_path = repository_root / contract_ref
    contract = _read_json(contract_path, label="nine-node functional contract")

    nodes = contract.get("nodes")
    if not isinstance(nodes, list):
        raise RuntimeError("nine-node functional contract must contain a nodes list")

    names = tuple(node.get("name") for node in nodes if isinstance(node, dict))
    ids = tuple(node.get("id") for node in nodes if isinstance(node, dict))
    expected_ids = tuple(f"NAYA-KERNEL-{name}" for name in CANONICAL_NODE_NAMES)

    if names != CANONICAL_NODE_NAMES or ids != expected_ids:
        raise RuntimeError(
            "nine-node functional contract identity/order does not match the "
            "canonical kernel; runtime boot fails closed"
        )

    for node in nodes:
        missing = sorted(
            field for field in REQUIRED_FUNCTIONAL_CONTRACT_FIELDS if field not in node
        )
        if missing:
            raise RuntimeError(
                "nine-node functional contract is incomplete for "
                f"{node.get('name', '<unknown>')}: missing {', '.join(missing)}"
            )

    return contract


def load_runtime_manifest(root: Path | None = None) -> dict:
    repository_root = find_repository_root(root)
    path = repository_root / "BRAIN/03-KERNEL/MANIFEST.json"
    manifest = _read_json(path, label="BRAIN manifest")

    nodes = manifest.get("nodes")
    names = tuple(node.get("name") for node in nodes or ())
    ids = tuple(node.get("id") for node in nodes or ())

    expected_ids = tuple(f"NAYA-KERNEL-{name}" for name in CANONICAL_NODE_NAMES)

    if names != CANONICAL_NODE_NAMES or ids != expected_ids:
        raise RuntimeError(
            "BRAIN manifest node identity/order does not match the canonical "
            "nine-node kernel; runtime boot fails closed"
        )

    load_functional_contract(repository_root)

    return manifest
