"""Deterministic validation for the materialized NayaPOWER brain population."""

from __future__ import annotations

import json
from pathlib import Path

NODE_NAMES = ("SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE")
NODE_IDS = tuple(f"NAYA-KERNEL-{name}" for name in NODE_NAMES)

ALLOWED_RELATIONSHIPS = {
    "DERIVED_FROM", "SUPPORTS", "CONTRADICTS", "DEPENDS_ON", "IMPLEMENTS",
    "GOVERNS", "AUTHORIZED_BY", "USED_BY", "CAUSED", "RESULTED_IN",
    "VERIFIED_BY", "LEARNED_FROM", "SUPERSEDES", "SUCCEEDS", "RELATED_TO",
    "CONTEXTUALIZES", "INVALIDATES", "REFINES", "CORRECTS", "ENABLES",
    "PRODUCES", "APPLIES_TO",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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

    for label, ids in (
        ("manifest", [node["id"] for node in manifest.get("nodes", [])]),
        ("registry", registry.get("node_ids", [])),
        ("index", [node["id"] for node in index.get("nine_nodes", [])]),
    ):
        if tuple(ids) != NODE_IDS:
            errors.append(f"{label}_node_ids_do_not_match_canonical_order")

    object_dir = base / "BRAIN/04-INTELLIGENCE/OBJECTS"
    object_ids = []
    objects: dict[str, dict] = {}
    for node_id in NODE_IDS:
        path = object_dir / f"{node_id}.json"
        if not path.exists():
            errors.append(f"missing:object:{node_id}")
            continue
        obj = _read_json(path)
        objects[node_id] = obj
        object_ids.append(obj.get("object_id"))
        if obj.get("object_id") != node_id:
            errors.append(f"object_id_mismatch:{node_id}")
        if obj.get("object_type") != "NODE":
            errors.append(f"object_type_mismatch:{node_id}")
    if tuple(object_ids) != NODE_IDS:
        errors.append("node_object_set_incomplete")

    edges = graph.get("edges", [])
    graph_relationships: dict[str, dict] = {}
    for edge in edges:
        relationship_id = edge.get("relationship_id")
        if edge.get("type") not in ALLOWED_RELATIONSHIPS:
            errors.append(f"unsupported_relationship:{edge.get('type')}")
        if not relationship_id or not edge.get("source_id") or not edge.get("target_id"):
            errors.append("relationship_identity_incomplete")
        if not edge.get("provenance"):
            errors.append(f"relationship_missing_provenance:{relationship_id}")
        if relationship_id:
            if relationship_id in graph_relationships:
                errors.append(f"duplicate_relationship_id:{relationship_id}")
            graph_relationships[relationship_id] = edge

    # A relationship may legitimately be materialized on both endpoint objects.
    # Validate every materialization against the single graph-seed definition,
    # but do not misclassify identical endpoint copies as duplicate relationships.
    object_relationship_ids: set[str] = set()
    for node_id, obj in objects.items():
        for rel in obj.get("relationships", []):
            relationship_id = rel.get("relationship_id")
            if not relationship_id:
                errors.append(f"node_relationship_identity_incomplete:{node_id}")
                continue
            object_relationship_ids.add(relationship_id)
            seed = graph_relationships.get(relationship_id)
            if seed is None:
                errors.append(f"node_relationship_missing_from_graph:{node_id}:{relationship_id}")
                continue
            expected = (
                seed.get("source_id"), seed.get("target_id"),
                seed.get("type"), seed.get("epistemic_state"),
            )
            actual = (
                rel.get("source_object_id"), rel.get("target_object_id"),
                rel.get("type"), rel.get("epistemic_state"),
            )
            if actual != expected:
                errors.append(f"node_relationship_drift:{node_id}:{relationship_id}")

    for relationship_id in sorted(set(graph_relationships) - object_relationship_ids):
        errors.append(f"graph_relationship_missing_from_node_objects:{relationship_id}")

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
