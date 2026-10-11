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

# Top-level fields present in the canonical BRAIN/03-KERNEL/MANIFEST.json.
# The kernel stores and exposes the manifest dict verbatim (see
# kernel/nayapower_kernel.py: Kernel.manifest), so an unknown extra field
# would ride along unverified inside what reads as "the verified manifest".
# Unknown fields are therefore refused, not ignored. Adding a field to the
# manifest is a deliberate schema change that must be reflected here.
TOP_LEVEL_FIELDS = frozenset(
    {
        "kernel_id",
        "schema",
        "nodes",
        "node_identity_law",
        "runtime_binding",
        "status",
    }
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

    # Fail closed on shape, not just content: a non-dict node entry has no
    # .get() and would otherwise escape the RuntimeError path as
    # AttributeError, violating the fail-closed contract.
    nodes = manifest.get("nodes")
    if any(not isinstance(node, dict) for node in nodes or ()):
        raise RuntimeError(
            "BRAIN manifest contains a non-object node entry; "
            "runtime boot fails closed"
        )

    names = tuple(node.get("name") for node in nodes or ())
    ids = tuple(node.get("id") for node in nodes or ())

    expected_ids = tuple(f"NAYA-KERNEL-{name}" for name in CANONICAL_NODE_NAMES)

    if names != CANONICAL_NODE_NAMES or ids != expected_ids:
        raise RuntimeError(
            "BRAIN manifest node identity/order does not match the canonical "
            "nine-node kernel; runtime boot fails closed"
        )

    unexpected_fields = set(manifest) - TOP_LEVEL_FIELDS
    if unexpected_fields:
        raise RuntimeError(
            "BRAIN manifest carries unexpected top-level fields "
            f"{sorted(unexpected_fields)}; runtime boot fails closed"
        )

    return manifest
