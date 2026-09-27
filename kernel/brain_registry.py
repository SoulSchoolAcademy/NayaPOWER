"""Deterministic validation for the materialized NayaPOWER brain population."""

from __future__ import annotations

import json
from pathlib import Path

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

    manifest_registry_index_parity = True
    for label, ids in (
        ("manifest", manifest_ids),
        ("registry", registry_ids),
        ("index", index_ids),
    ):
        if tuple(ids) != NODE_IDS:
            manifest_registry_index_parity = False
            errors.append(f"{label}_node_ids_do_not_match_canonical_order")

    if manifest.get("kernel_id") != registry.get("kernel_id"):
        manifest_registry_index_parity = False
        errors.append("manifest_registry_kernel_id_mismatch")

    if registry.get("manifest") != "BRAIN/03-KERNEL/MANIFEST.json":
        manifest_registry_index_parity = False
        errors.append("registry_manifest_pointer_mismatch")

    object_dir = base / "BRAIN/04-INTELLIGENCE/OBJECTS"
    object_ids = []
    object_envelope_errors: list[str] = []
    required_object_fields = (
        "schema", "object_id", "object_type", "version", "canonical_status",
        "owner_id", "scope", "human_view", "ai_view", "machine_view",
        "provenance", "proof", "relationships", "successor_effect",
    )
    for node_id in NODE_IDS:
        path = object_dir / f"{node_id}.json"
        if not path.exists():
            errors.append(f"missing:object:{node_id}")
            continue
        obj = _read_json(path)
        object_ids.append(obj.get("object_id"))
        for field in required_object_fields:
            if field not in obj:
                object_envelope_errors.append(f"{node_id}:missing:{field}")
        if obj.get("schema") != "naya.intelligent.object.v1":
            object_envelope_errors.append(f"{node_id}:schema_mismatch")
        if obj.get("object_id") != node_id:
            errors.append(f"object_id_mismatch:{node_id}")
        if obj.get("object_type") != "NODE":
            errors.append(f"object_type_mismatch:{node_id}")
        machine = obj.get("machine_view") or {}
        if machine.get("stable_id") != node_id or machine.get("node_name") != node_id.removeprefix("NAYA-KERNEL-"):
            object_envelope_errors.append(f"{node_id}:machine_identity_mismatch")
        if not isinstance(obj.get("provenance"), dict) or not obj.get("provenance", {}).get("derived_from"):
            object_envelope_errors.append(f"{node_id}:provenance_missing")

    if tuple(object_ids) != NODE_IDS:
        errors.append("node_object_set_incomplete")

    edges = graph.get("edges", [])
    canonical_node_set = set(NODE_IDS)
    for edge in edges:
        if edge.get("type") not in ALLOWED_RELATIONSHIPS:
            errors.append(f"unsupported_relationship:{edge.get('type')}")
        if not edge.get("relationship_id") or not edge.get("source_id") or not edge.get("target_id"):
            errors.append("relationship_identity_incomplete")
        if edge.get("source_id") not in canonical_node_set:
            errors.append(f"unknown_graph_node:source:{edge.get('source_id')}")
        if edge.get("target_id") not in canonical_node_set:
            errors.append(f"unknown_graph_node:target:{edge.get('target_id')}")
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
        "errors": errors + [f"object_envelope:{e}" for e in object_envelope_errors],
        "manifest_registry_index_parity": manifest_registry_index_parity,
        "object_envelope_errors": object_envelope_errors,
    }
