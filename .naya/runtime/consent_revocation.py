from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Iterable

import derived_intelligence_revalidation as lineage

PLAN_SCHEMA = "NAYAPOWER_CONSENT_REVOCATION_PLAN_V1"
ARTIFACT_TYPES = {
    "ORIGINAL",
    "DERIVED",
    "SUMMARY",
    "COLLECTIVE_INSIGHT",
    "CACHE",
    "EMBEDDING",
    "DOWNSTREAM_CONCLUSION",
}
POLICIES = {
    "DERIVED": ("RESTRICT_DERIVED_USE", "RECOMPUTE_WITHOUT_REVOKED_SOURCE"),
    "SUMMARY": ("RESTRICT_SUMMARY_USE", "REVALIDATE_SUMMARY"),
    "COLLECTIVE_INSIGHT": ("EXCLUDE_REVOKED_LINEAGE", "RECOMPUTE_COLLECTIVE_INSIGHT_IF_CONTENTS_ARE_NOT_PROVEN_ANONYMOUS"),
    "CACHE": ("PROPOSE_CACHE_INVALIDATION",),
    "EMBEDDING": ("PROPOSE_EMBEDDING_DELETION_IF_CONTENT_CONTAINS_REVOKED_SOURCE",),
    "DOWNSTREAM_CONCLUSION": ("RESTRICT_DOWNSTREAM_USE", "REVALIDATE_DOWNSTREAM_CONCLUSION"),
}
REQUIRED_REVOCATION_FIELDS = {"revocation_id", "authority_ref", "revoked_by", "reason", "evidence_refs", "idempotency_key", "sources"}


class ConsentRevocationError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConsentRevocationError(f"{field} is required")
    return value.strip()


def digest(value: Any, field: str) -> str:
    value = text(value, field).lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ConsentRevocationError(f"{field} must be a SHA-256 hex digest")
    return value


def refs(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ConsentRevocationError(f"{field} must contain at least one reference")
    result = sorted(text(item, field) for item in value)
    if len(result) != len(set(result)):
        raise ConsentRevocationError(f"{field} contains duplicate references")
    return result


def record_id(record: dict[str, Any]) -> str | None:
    return lineage.primary_record_id(record)


def artifact_type(record: dict[str, Any]) -> str | None:
    for value in (
        record.get("artifact_type"),
        record.get("storage", {}).get("artifact_type") if isinstance(record.get("storage"), dict) else None,
        record.get("consent", {}).get("artifact_type") if isinstance(record.get("consent"), dict) else None,
    ):
        if isinstance(value, str) and value.strip():
            return value.strip().upper()
    return None


def consent_state(record: dict[str, Any]) -> str:
    for value in (
        record.get("consent_state"),
        record.get("privacy", {}).get("consent_state") if isinstance(record.get("privacy"), dict) else None,
        record.get("consent", {}).get("state") if isinstance(record.get("consent"), dict) else None,
    ):
        if isinstance(value, str) and value.strip():
            return value.strip().upper()
    return "UNKNOWN"


def validate_revocation(revocation: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_REVOCATION_FIELDS - set(revocation)
    if missing:
        raise ConsentRevocationError("revocation missing fields: " + ", ".join(sorted(missing)))
    sources = revocation.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ConsentRevocationError("revocation sources are required")
    normalized = []
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ConsentRevocationError("revocation source entries must be objects")
        source_id = text(source.get("intelligence_id"), "revoked intelligence_id")
        if source_id in seen:
            raise ConsentRevocationError("revocation contains duplicate source IDs")
        seen.add(source_id)
        previous = digest(source.get("previous_consent_sha256"), "previous_consent_sha256")
        revoked = digest(source.get("revoked_consent_sha256"), "revoked_consent_sha256")
        if previous == revoked:
            raise ConsentRevocationError(f"consent state hashes are equal: {source_id}")
        normalized.append(
            {
                "intelligence_id": source_id,
                "previous_consent_sha256": previous,
                "revoked_consent_sha256": revoked,
            }
        )
    return {
        "revocation_id": text(revocation.get("revocation_id"), "revocation_id"),
        "authority_ref": text(revocation.get("authority_ref"), "authority_ref"),
        "revoked_by": text(revocation.get("revoked_by"), "revoked_by"),
        "reason": text(revocation.get("reason"), "reason"),
        "evidence_refs": refs(revocation.get("evidence_refs"), "evidence_refs"),
        "idempotency_key": text(revocation.get("idempotency_key"), "idempotency_key"),
        "sources": sorted(normalized, key=lambda item: item["intelligence_id"]),
    }


def plan_consent_revocation(
    revocation: dict[str, Any],
    records: Iterable[dict[str, Any]],
    *,
    authorized_ids: set[str] | None = None,
) -> dict[str, Any]:
    normalized = validate_revocation(revocation)
    record_list = [copy.deepcopy(record) for record in records if isinstance(record, dict)]
    if authorized_ids is not None:
        authorized = {text(value, "authorized id") for value in authorized_ids}
        record_list = [record for record in record_list if authorized.intersection(lineage.record_aliases(record))]
    records_by_id = {}
    for record in record_list:
        current_id = record_id(record)
        if current_id is None:
            continue
        records_by_id[current_id] = record
    unresolved = []
    visible_sources = []
    for source in normalized["sources"]:
        source_id = source["intelligence_id"]
        if authorized_ids is not None and source_id not in authorized:
            unresolved.append({"code": "REVOKED_SOURCE_NOT_AUTHORIZED", "source_id": source_id})
            continue
        visible_sources.append(
            {
                "id": source_id,
                "before_hash": source["previous_consent_sha256"],
                "after_hash": source["revoked_consent_sha256"],
            }
        )
    if not visible_sources:
        raise ConsentRevocationError("no authorized revocation source remains")
    lineage_plan = lineage.plan_revalidation_impact(
        visible_sources,
        record_list,
        authorized_ids=authorized_ids,
    )
    unresolved.extend(copy.deepcopy(lineage_plan.get("unresolved", [])))
    source_actions = [
        {
            "intelligence_id": source["intelligence_id"],
            "artifact_type": artifact_type(records_by_id[source["intelligence_id"]]) if source["intelligence_id"] in records_by_id else "ORIGINAL",
            "required_actions": ["STOP_FUTURE_SHARING", "RECORD_CONSENT_REVOCATION"],
            "preserve_original": True,
            "execution_performed": False,
        }
        for source in normalized["sources"]
        if source["intelligence_id"] in {item["id"] for item in visible_sources}
    ]
    impacted = []
    candidate_by_id = {item["id"]: item for item in lineage_plan.get("revalidation_candidates", [])}
    for candidate_id in sorted(candidate_by_id):
        record = records_by_id.get(candidate_id)
        kind = artifact_type(record) if record is not None else None
        if kind not in ARTIFACT_TYPES:
            unresolved.append({"code": "ARTIFACT_TYPE_UNKNOWN", "intelligence_id": candidate_id})
            kind = "UNKNOWN"
        required_actions = list(POLICIES.get(kind, ("REVIEW_REQUIRED",)))
        impacted.append(
            {
                "intelligence_id": candidate_id,
                "artifact_type": kind,
                "current_consent_state": consent_state(record) if record is not None else "UNKNOWN",
                "required_actions": required_actions,
                "changed_source_ids": candidate_by_id[candidate_id].get("changed_source_ids", []),
                "paths": candidate_by_id[candidate_id].get("paths", []),
                "preserve_history": True,
                "execution_performed": False,
            }
        )
    unique_unresolved = []
    seen = set()
    for item in sorted(unresolved, key=lambda value: (value.get("code", ""), canonical_json(value))):
        key = digest_value(item)
        if key not in seen:
            seen.add(key)
            unique_unresolved.append(item)
    if not impacted and not unique_unresolved:
        status = "NO_KNOWN_DEPENDENTS"
    elif unique_unresolved:
        status = "PARTIAL"
    else:
        status = "COMPLETE"
    return {
        "schema": PLAN_SCHEMA,
        "status": status,
        "mode": "PROPOSAL_ONLY",
        "revocation": normalized,
        "revocation_sha256": digest_value(normalized),
        "source_actions": source_actions,
        "impacted_artifacts": impacted,
        "lineage_impact": {
            "status": lineage_plan["status"],
            "impacted_derived_intelligence_ids": lineage_plan["impacted_derived_intelligence_ids"],
            "unresolved": lineage_plan["unresolved"],
        },
        "unresolved": unique_unresolved,
        "original_preservation": "PRESERVE_OWNER_ORIGINAL",
        "history_preserved": True,
        "persistence_performed": False,
        "canonical_records_modified": False,
        "truth_boundary": "This plan proposes consent restrictions and artifact-specific propagation. It does not delete originals, summaries, caches, embeddings, or downstream conclusions, and it does not persist a revocation.",
    }


def validate_revocation_plan(plan: dict[str, Any]) -> list[str]:
    errors = []
    if plan.get("schema") != PLAN_SCHEMA or plan.get("mode") != "PROPOSAL_ONLY":
        return ["revocation plan schema or mode is invalid"]
    if plan.get("persistence_performed") is not False or plan.get("canonical_records_modified") is not False:
        errors.append("proposal-only boundary is invalid")
    if plan.get("history_preserved") is not True or plan.get("original_preservation") != "PRESERVE_OWNER_ORIGINAL":
        errors.append("history or original-preservation boundary is invalid")
    if plan.get("revocation_sha256") != digest_value(plan.get("revocation")):
        errors.append("revocation fingerprint is invalid")
    for item in plan.get("source_actions", []):
        if item.get("preserve_original") is not True or item.get("execution_performed") is not False:
            errors.append("source action crosses the preservation boundary")
    for item in plan.get("impacted_artifacts", []):
        if item.get("execution_performed") is not False or item.get("preserve_history") is not True:
            errors.append("impacted artifact crosses the proposal boundary")
    return errors
