"""Deterministic validation for the materialized NayaPOWER brain population."""

from __future__ import annotations

import json
from pathlib import Path

# RATIFICATION PIN, not a second source of truth.
#
# The canonical nine-node order is defined by BRAIN/03-KERNEL/MANIFEST.json.
# These constants exist only so validation can detect drift in the manifest
# instead of merely agreeing with it: a validator that derives its expectation
# from the file it is checking proves nothing. The runtime
# (kernel/nayapower_kernel.py) deliberately does NOT use these constants; it
# loads the manifest. tests/test_kernel_manifest_binding.py asserts the two
# still agree, which is what makes the pin meaningful.
CANONICAL_MANIFEST_PATH = "BRAIN/03-KERNEL/MANIFEST.json"

NODE_NAMES = (
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

NODE_IDS = tuple(f"NAYA-KERNEL-{name}" for name in NODE_NAMES)


class BrainIntegrityError(RuntimeError):
    """The canonical brain could not be read as a well-formed kernel.

    Raised instead of returning a partial result. A caller that receives this
    has NOT learned what the kernel is, and must fail closed.
    """

ALLOWED_RELATIONSHIPS = {
    "DERIVED_FROM",
    "SUPPORTS",
    "CONTRADICTS",
    "DEPENDS_ON",
    "IMPLEMENTS",
    "GOVERNS",
    "AUTHORIZED_BY",
    "USED_BY",
    "CAUSED",
    "RESULTED_IN",
    "VERIFIED_BY",
    "LEARNED_FROM",
    "SUPERSEDES",
    "SUCCEEDS",
    "RELATED_TO",
    "CONTEXTUALIZES",
    "INVALIDATES",
    "REFINES",
    "CORRECTS",
    "ENABLES",
    "PRODUCES",
    "APPLIES_TO",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_root() -> Path:
    """Repository root, derived from this file's location."""
    return Path(__file__).resolve().parents[1]


def load_canonical_kernel(root: Path | None = None) -> dict:
    """Read the canonical kernel manifest and return its node records in order.

    This is the single entry point every consumer should use to learn what the
    nine Master Nodes are. It fails loudly rather than degrading: a missing,
    unreadable, malformed or ambiguous manifest raises BrainIntegrityError,
    because a partially-understood kernel is worse than an absent one.
    """
    base = Path(root) if root is not None else repo_root()
    path = base / CANONICAL_MANIFEST_PATH

    if not path.exists():
        raise BrainIntegrityError(f"missing_manifest:{CANONICAL_MANIFEST_PATH}")

    try:
        manifest = _read_json(path)
    except json.JSONDecodeError as exc:
        raise BrainIntegrityError(f"unparseable_manifest:{exc}") from exc

    if not isinstance(manifest, dict):
        raise BrainIntegrityError("manifest_is_not_an_object")

    nodes = manifest.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise BrainIntegrityError("manifest_declares_no_nodes")

    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    records: list[dict] = []
    problems: list[str] = []

    for position, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            problems.append(f"node_{position}_is_not_an_object")
            continue
        node_id = node.get("id")
        name = node.get("name")
        if not isinstance(node_id, str) or not node_id.strip():
            problems.append(f"node_{position}_missing_id")
            continue
        if not isinstance(name, str) or not name.strip():
            problems.append(f"node_{position}_missing_name:{node_id}")
            continue
        if node_id in seen_ids:
            problems.append(f"duplicate_node_id:{node_id}")
            continue
        if name in seen_names:
            problems.append(f"duplicate_node_name:{name}")
            continue
        seen_ids.add(node_id)
        seen_names.add(name)
        records.append({"id": node_id, "name": name, "responsibility": node.get("responsibility")})

    if problems:
        raise BrainIntegrityError(";".join(problems))

    # The count is a ratified invariant, not a derivable one. This is the one
    # place the pin below is used as an expectation rather than a convenience:
    # a manifest that declares fewer than the ratified nine is a truncated
    # kernel, and a runtime that loaded it would report a smaller brain while
    # still claiming to be governed by the full one.
    if len(records) != len(NODE_NAMES):
        raise BrainIntegrityError(
            f"node_count_mismatch:expected_{len(NODE_NAMES)}_got_{len(records)}"
        )

    return {
        "kernel_id": manifest.get("kernel_id"),
        "status": manifest.get("status"),
        "node_count": len(records),
        "nodes": records,
    }


def load_canonical_node_names(root: Path | None = None) -> tuple[str, ...]:
    """Canonical node names in manifest order."""
    return tuple(node["name"] for node in load_canonical_kernel(root)["nodes"])


def load_canonical_node_ids(root: Path | None = None) -> tuple[str, ...]:
    """Canonical node ids in manifest order."""
    return tuple(node["id"] for node in load_canonical_kernel(root)["nodes"])


def load_and_validate_brain(root: Path, root_override: Path | None = None) -> dict:
    base = Path(root_override) if root_override is not None else Path(root)
    errors: list[str] = []

    required = [
        base / "BRAIN/03-KERNEL/MANIFEST.json",
        base / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json",
        base / "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
        base / "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json",
        base / "BRAIN/04-INTELLIGENCE/GRAPH/0002-KNOWLEDGE-TO-NODE-MAP-V1.json",
        base / "BRAIN/11-KNOWLEDGE/0003-KNOWLEDGE-POPULATION-MAP-V1.json",
        base / "BRAIN/11-KNOWLEDGE/0004-HUMAN-AI-MACHINE-REPRESENTATION-V1.md",
    ]

    for path in required:
        if not path.exists():
            errors.append(f"missing:{path.relative_to(base)}")

    if errors:
        return {"ok": False, "node_count": 0, "source_count": 0, "graph_edge_count": 0, "errors": errors}

    manifest = _read_json(required[0])
    registry = _read_json(required[1])
    index = _read_json(required[2])
    graph = _read_json(required[3])
    population = _read_json(required[5])

    manifest_ids = [node["id"] for node in manifest.get("nodes", [])]
    registry_ids = registry.get("node_ids", [])
    index_ids = [node["id"] for node in index.get("nine_nodes", [])]

    for label, ids in (
        ("manifest", manifest_ids),
        ("registry", registry_ids),
        ("index", index_ids),
    ):
        if tuple(ids) != NODE_IDS:
            errors.append(f"{label}_node_ids_do_not_match_canonical_order")

    object_dir = base / "BRAIN/04-INTELLIGENCE/OBJECTS"
    object_ids = []
    for node_id in NODE_IDS:
        path = object_dir / f"{node_id}.json"
        if not path.exists():
            errors.append(f"missing:object:{node_id}")
            continue
        obj = _read_json(path)
        object_ids.append(obj.get("object_id"))
        if obj.get("object_id") != node_id:
            errors.append(f"object_id_mismatch:{node_id}")
        if obj.get("object_type") != "NODE":
            errors.append(f"object_type_mismatch:{node_id}")

    if tuple(object_ids) != NODE_IDS:
        errors.append("node_object_set_incomplete")

    edges = graph.get("edges", [])
    for edge in edges:
        if edge.get("type") not in ALLOWED_RELATIONSHIPS:
            errors.append(f"unsupported_relationship:{edge.get('type')}")
        if not edge.get("relationship_id") or not edge.get("source_id") or not edge.get("target_id"):
            errors.append("relationship_identity_incomplete")
        if not edge.get("provenance"):
            errors.append(f"relationship_missing_provenance:{edge.get('relationship_id')}")

    source_count = population.get("source_count")
    if source_count != 15 or len(population.get("source_mappings", [])) != 15:
        errors.append("source_population_is_not_1_to_15")

    return {
        "ok": not errors,
        "node_count": len(object_ids),
        "source_count": len(population.get("source_mappings", [])),
        "graph_edge_count": len(edges),
        "errors": errors,
    }
