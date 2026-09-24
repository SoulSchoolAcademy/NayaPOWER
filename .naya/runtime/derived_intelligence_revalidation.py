from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict, deque
from typing import Any, Iterable

PLAN_SCHEMA = "NAYAPOWER_DERIVED_INTELLIGENCE_REVALIDATION_PLAN_V1"
DEPENDENCY_RELATIONS = {"DERIVED_FROM", "DEPENDS_ON", "REQUIRES", "PARENT_EVENT", "SOURCE_EVENT", "SOURCE_BUNDLE"}
HISTORICAL_RELATIONS = {"SUPERSEDES", "SUPERSEDED_BY"}
SYSTEM46_ACTIONS = ("INVALIDATE", "RECHECK", "RECALCULATE", "SUPERSEDE")
DEFAULT_MAX_DEPTH = 8


class LineagePlanningError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LineagePlanningError(f"{field} must be a non-empty string")
    return value.strip()


def optional_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def record_aliases(record: dict[str, Any]) -> list[str]:
    identity = record.get("identity") if isinstance(record.get("identity"), dict) else {}
    candidates = [
        identity.get("object_id"),
        identity.get("event_id"),
        record.get("event_id"),
        record.get("block_id"),
        record.get("intelligence_id"),
        record.get("id"),
    ]
    aliases = [value.strip() for value in candidates if isinstance(value, str) and value.strip()]
    return list(dict.fromkeys(aliases))


def primary_record_id(record: dict[str, Any]) -> str | None:
    aliases = record_aliases(record)
    return aliases[0] if aliases else None


def record_kind(record: dict[str, Any]) -> str:
    identity = record.get("identity") if isinstance(record.get("identity"), dict) else {}
    if identity.get("object_id") or record.get("block_id"):
        return "intelligent_block"
    if record.get("event_id"):
        return "event"
    return "intelligence"


def record_status(record: dict[str, Any]) -> str:
    lifecycle = record.get("lifecycle") if isinstance(record.get("lifecycle"), dict) else {}
    truth = record.get("truth") if isinstance(record.get("truth"), dict) else {}
    verification = record.get("verification") if isinstance(record.get("verification"), dict) else {}
    return str(lifecycle.get("stage") or truth.get("state") or verification.get("status") or record.get("status") or "UNKNOWN")


def record_content_hash(record: dict[str, Any]) -> str | None:
    integrity = record.get("integrity") if isinstance(record.get("integrity"), dict) else {}
    return optional_text(integrity.get("content_hash") or record.get("content_hash") or record.get("source_hash") or record.get("hash"))


def reference_target(value: Any) -> str | None:
    if isinstance(value, str):
        return optional_text(value)
    if isinstance(value, dict):
        return optional_text(value.get("source_id") or value.get("target") or value.get("event_id") or value.get("intelligence_id") or value.get("id"))
    return None


def reference_hash(value: Any) -> str | None:
    return optional_text(value.get("hash") or value.get("content_hash")) if isinstance(value, dict) else None


def reference_version(value: Any) -> str | int | None:
    if not isinstance(value, dict):
        return None
    version = value.get("version")
    return version if isinstance(version, (str, int)) and str(version).strip() else None


def edge(target: Any, relation: str, source_hash: str | None = None, source_version: str | int | None = None) -> dict[str, Any] | None:
    target_id = reference_target(target)
    if not target_id:
        return None
    return {
        "target_id": target_id,
        "relation": relation,
        "source_hash": source_hash,
        "source_version": source_version,
    }


def extract_explicit_edges(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    dependencies: list[dict[str, Any]] = []
    historical: list[dict[str, Any]] = []
    aliases = set(record_aliases(record))
    source_hash = optional_text(record.get("source_hash"))
    for value in record.get("source_event_ids") or []:
        item = edge(value, "SOURCE_EVENT", reference_hash(value) or source_hash, reference_version(value))
        if item:
            dependencies.append(item)
    for value in record.get("source_bundle") or []:
        relation = str(value.get("relationship") or "SOURCE_BUNDLE") if isinstance(value, dict) else "SOURCE_BUNDLE"
        item = edge(value, relation, reference_hash(value), reference_version(value))
        if item:
            dependencies.append(item)
    provenance = record.get("provenance") if isinstance(record.get("provenance"), dict) else {}
    for value in provenance.get("derived_from") or []:
        item = edge(value, "DERIVED_FROM", reference_hash(value), reference_version(value))
        if item:
            dependencies.append(item)
    relationships = record.get("relationships") if isinstance(record.get("relationships"), dict) else {}
    for field, relation in (("source_events", "SOURCE_EVENT"), ("depends_on", "DEPENDS_ON"), ("requires", "REQUIRES")):
        for value in relationships.get(field) or []:
            item = edge(value, relation, reference_hash(value), reference_version(value))
            if item:
                dependencies.append(item)
    if relationships.get("parent_event_id"):
        item = edge(relationships.get("parent_event_id"), "PARENT_EVENT")
        if item:
            dependencies.append(item)
    if record.get("parent_event_id"):
        item = edge(record.get("parent_event_id"), "PARENT_EVENT")
        if item:
            dependencies.append(item)
    for relationship in record.get("relationships") or []:
        if not isinstance(relationship, dict):
            continue
        relation = str(relationship.get("relation") or "")
        source = optional_text(relationship.get("source"))
        target = edge(relationship.get("target"), relation)
        if not target or source not in aliases:
            continue
        if relation in DEPENDENCY_RELATIONS:
            dependencies.append(target)
        elif relation in HISTORICAL_RELATIONS:
            historical.append(target)
    unique_dependencies = {
        (item["target_id"], item["relation"], item["source_hash"], item["source_version"]): item
        for item in dependencies
    }
    unique_historical = {
        (item["target_id"], item["relation"], item["source_hash"], item["source_version"]): item
        for item in historical
    }
    return (
        [unique_dependencies[key] for key in sorted(unique_dependencies, key=str)],
        [unique_historical[key] for key in sorted(unique_historical, key=str)],
    )


def normalize_changed_sources(changed_sources: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized = []
    unresolved = []
    seen = set()
    for item in changed_sources:
        source_id = text(item.get("id"), "changed source id")
        if source_id in seen:
            unresolved.append({"code": "DUPLICATE_CHANGED_SOURCE", "source_id": source_id})
            continue
        seen.add(source_id)
        before_hash = optional_text(item.get("before_hash"))
        after_hash = optional_text(item.get("after_hash"))
        if before_hash and after_hash and before_hash == after_hash:
            raise LineagePlanningError(f"changed source hashes are equal: {source_id}")
        if before_hash and after_hash:
            hash_state = "CHANGED_CONFIRMED"
        else:
            hash_state = "UNKNOWN"
            unresolved.append({"code": "CHANGE_HASH_UNKNOWN", "source_id": source_id})
        normalized.append({"id": source_id, "before_hash": before_hash, "after_hash": after_hash, "hash_state": hash_state})
    if not normalized:
        raise LineagePlanningError("at least one changed source is required")
    return sorted(normalized, key=lambda item: item["id"]), unresolved


def plan_revalidation_impact(
    changed_sources: Iterable[dict[str, Any]],
    records: Iterable[dict[str, Any]],
    *,
    authorized_ids: set[str] | None = None,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> dict[str, Any]:
    if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 1:
        raise LineagePlanningError("max_depth must be a positive integer")
    source_changes, unresolved = normalize_changed_sources(changed_sources)
    changed_source_ids = {item["id"] for item in source_changes}
    record_list = [copy.deepcopy(record) for record in records if isinstance(record, dict)]
    if authorized_ids is not None:
        authorized = {text(value, "authorized id") for value in authorized_ids}
        record_list = [record for record in record_list if authorized.intersection(record_aliases(record))]
    records_by_id = {}
    aliases_to_id = {}
    alias_owners = defaultdict(set)
    for record in record_list:
        aliases = record_aliases(record)
        if not aliases:
            unresolved.append({"code": "RECORD_ID_MISSING"})
            continue
        record_id = aliases[0]
        for alias in aliases:
            alias_owners[alias].add(record_id)
        records_by_id[record_id] = record
        for alias in aliases:
            aliases_to_id[alias] = record_id
    for alias, owners in sorted(alias_owners.items()):
        if len(owners) > 1:
            unresolved.append({"code": "DUPLICATE_RECORD_ALIAS", "alias": alias, "record_ids": sorted(owners)})
    traversal_sources = [
        (item["id"], aliases_to_id.get(item["id"], item["id"]))
        for item in source_changes
    ]
    dependents = defaultdict(list)
    historical = []
    for record_id in sorted(records_by_id):
        dependencies, record_historical = extract_explicit_edges(records_by_id[record_id])
        for item in record_historical:
            historical.append({"from_id": record_id, **item})
        for item in dependencies:
            target_id = item["target_id"]
            if authorized_ids is not None and target_id not in aliases_to_id:
                unresolved.append({"code": "UNAUTHORIZED_DEPENDENCY", "dependent_id": record_id})
                continue
            canonical_target = aliases_to_id.get(target_id, target_id)
            changed_source_visible = target_id in changed_source_ids and (authorized_ids is None or target_id in authorized)
            if target_id not in aliases_to_id and not changed_source_visible:
                unresolved.append({"code": "DEPENDENCY_TARGET_MISSING", "dependent_id": record_id, "target_id": target_id})
                continue
            dependents[canonical_target].append(
                {
                    "dependent_id": record_id,
                    "relation": item["relation"],
                    "source_hash": item["source_hash"],
                    "source_version": item["source_version"],
                }
            )
    for target in dependents:
        dependents[target].sort(key=lambda item: (item["dependent_id"], item["relation"], str(item["source_hash"]), str(item["source_version"])))
    candidates: dict[str, dict[str, Any]] = {}
    queue = deque(
        (source_id, traversal_id, 0, [source_id], [traversal_id], [])
        for source_id, traversal_id in traversal_sources
    )
    visited_paths = set()
    while queue:
        changed_source_id, node_id, distance, path, canonical_path, path_edges = queue.popleft()
        visit_key = (changed_source_id, tuple(canonical_path))
        if visit_key in visited_paths:
            continue
        visited_paths.add(visit_key)
        if distance >= max_depth:
            if dependents.get(node_id):
                unresolved.append({"code": "MAX_DEPTH_TRUNCATED", "source_id": changed_source_id, "node_id": node_id})
            continue
        for edge_item in dependents.get(node_id, []):
            dependent_id = edge_item["dependent_id"]
            if dependent_id in canonical_path:
                unresolved.append({"code": "DEPENDENCY_CYCLE", "source_id": changed_source_id, "node_id": dependent_id})
                continue
            next_distance = distance + 1
            next_path = path + [dependent_id]
            next_canonical_path = canonical_path + [dependent_id]
            next_edges = path_edges + [
                {
                    "from_id": node_id,
                    "to_id": dependent_id,
                    "relation": edge_item["relation"],
                    "source_hash": edge_item["source_hash"],
                    "source_version": edge_item["source_version"],
                }
            ]
            candidate = candidates.setdefault(
                dependent_id,
                {
                    "id": dependent_id,
                    "kind": record_kind(records_by_id[dependent_id]),
                    "disposition": "REVALIDATION_CANDIDATE",
                    "current_status": record_status(records_by_id[dependent_id]),
                    "current_content_hash": record_content_hash(records_by_id[dependent_id]),
                    "changed_source_ids": set(),
                    "paths": [],
                },
            )
            candidate["changed_source_ids"].add(changed_source_id)
            path_key = digest_json({"source_id": changed_source_id, "nodes": next_path, "edges": next_edges})
            if all(digest_json(existing) != path_key for existing in candidate["paths"]):
                candidate["paths"].append(
                    {
                        "changed_source_id": changed_source_id,
                        "distance": next_distance,
                        "nodes": next_path,
                        "edges": next_edges,
                    }
                )
            queue.append(
                (changed_source_id, dependent_id, next_distance, next_path, next_canonical_path, next_edges)
            )
    output_candidates = []
    for dependent_id in sorted(candidates):
        candidate = copy.deepcopy(candidates[dependent_id])
        candidate["changed_source_ids"] = sorted(candidate["changed_source_ids"])
        candidate["paths"] = sorted(candidate["paths"], key=lambda item: (item["changed_source_id"], item["distance"], item["nodes"]))
        output_candidates.append(candidate)
    deduplicated_unresolved = []
    seen_unresolved = set()
    for item in sorted(unresolved, key=lambda value: (value.get("code", ""), canonical_json(value))):
        key = digest_json(item)
        if key not in seen_unresolved:
            seen_unresolved.add(key)
            deduplicated_unresolved.append(item)
    if not output_candidates:
        status = "PARTIAL" if deduplicated_unresolved else "NO_KNOWN_DEPENDENTS"
    elif deduplicated_unresolved:
        status = "PARTIAL"
    else:
        status = "COMPLETE"
    lineage_context = sorted(
        [{key: value for key, value in item.items() if value is not None} for item in historical],
        key=lambda item: (item["from_id"], item["target_id"], item["relation"]),
    )
    return {
        "schema": PLAN_SCHEMA,
        "mode": "PLAN_ONLY",
        "status": status,
        "changed_sources": source_changes,
        "revalidation_candidates": output_candidates,
        "impacted_derived_intelligence_ids": [item["id"] for item in output_candidates],
        "lineage_context": lineage_context,
        "unresolved": deduplicated_unresolved,
        "counts": {
            "authorized_records": len(records_by_id),
            "changed_sources": len(source_changes),
            "revalidation_candidates": len(output_candidates),
            "unresolved": len(deduplicated_unresolved),
        },
        "system46_actions_invoked": [],
        "truth_boundary": "This plan identifies explicit dependency impact only. It does not infer lineage from similarity, mutate records, invalidate intelligence, recheck, recalculate, or supersede downstream objects.",
    }
