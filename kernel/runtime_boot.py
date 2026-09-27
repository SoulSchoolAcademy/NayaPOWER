"""Manifest-driven NayaPOWER runtime bootstrap.

The executable kernel consumes the canonical BRAIN manifest at boot.
This establishes the binding without claiming persistence, behavioral,
production, or successor proof.
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


def load_runtime_manifest(root: Path | None = None) -> dict:
    repository_root = find_repository_root(root)
    path = repository_root / "BRAIN/03-KERNEL/MANIFEST.json"

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid BRAIN manifest JSON: {path}") from exc

    nodes = manifest.get("nodes")
    names = tuple(node.get("name") for node in nodes or ())
    ids = tuple(node.get("id") for node in nodes or ())

    expected_ids = tuple(f"NAYA-KERNEL-{name}" for name in CANONICAL_NODE_NAMES)

    if names != CANONICAL_NODE_NAMES or ids != expected_ids:
        raise RuntimeError(
            "BRAIN manifest node identity/order does not match the canonical "
            "nine-node kernel; runtime boot fails closed"
        )

    return manifest
