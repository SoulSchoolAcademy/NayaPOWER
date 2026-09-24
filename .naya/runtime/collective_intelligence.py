from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Iterable

PLAN_SCHEMA = "NAYAPOWER_COLLECTIVE_INTELLIGENCE_PLAN_V1"
PIPELINE = (
    "PRIVATE_INTELLIGENCE",
    "OWNER_CONSENT",
    "SHARING_POLICY",
    "ANONYMIZATION_IDENTITY_POLICY",
    "COLLECTIVE_INTELLIGENCE",
)
CONSENT_PLAN_SCHEMA = "NAYAPOWER_CONSENT_REVOCATION_PLAN_V1"


class CollectiveIntelligenceError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CollectiveIntelligenceError(f"{field} is required")
    return value.strip()


def refs(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise CollectiveIntelligenceError(f"{field} must contain at least one reference")
    result = sorted(text(item, field) for item in value)
    if len(result) != len(set(result)):
        raise CollectiveIntelligenceError(f"{field} contains duplicate references")
    return result


def state(value: Any) -> str:
    return str(value or "UNKNOWN").strip().upper()


def contribution_references(contributions: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(contributions, list) or not contributions:
        return [], ["CONTRIBUTION_PROVENANCE_REQUIRED"]
    safe = []
    errors = []
    for index, contribution in enumerate(contributions):
        if not isinstance(contribution, dict):
            errors.append(f"CONTRIBUTION_{index}_INVALID")
            continue
        ref = contribution.get("contribution_id") or contribution.get("source_ref") or contribution.get("provenance_ref")
        if not isinstance(ref, str) or not ref.strip():
            errors.append(f"CONTRIBUTION_{index}_REFERENCE_REQUIRED")
            continue
        safe.append(
            {
                "contribution_id": ref.strip(),
                "source_ref": contribution.get("source_ref") if isinstance(contribution.get("source_ref"), str) else None,
                "provenance_hash": contribution.get("provenance_hash") if isinstance(contribution.get("provenance_hash"), str) else None,
                "contributor_scope": contribution.get("contributor_scope") if isinstance(contribution.get("contributor_scope"), str) else None,
            }
        )
    return safe, errors


def consent_plan_context(consent_plan: dict[str, Any] | None) -> tuple[dict[str, Any], set[str], list[str]]:
    if consent_plan is None:
        raise CollectiveIntelligenceError("System 44 consent plan is required")
    if consent_plan.get("schema") != CONSENT_PLAN_SCHEMA or consent_plan.get("mode") != "PROPOSAL_ONLY":
        raise CollectiveIntelligenceError("System 44 consent plan is invalid")
    context = {
        "status": consent_plan.get("status"),
        "revocation_sha256": consent_plan.get("revocation_sha256"),
        "persistence_performed": consent_plan.get("persistence_performed"),
    }
    if consent_plan.get("persistence_performed") is not False:
        raise CollectiveIntelligenceError("consent plan crossed its proposal-only boundary")
    impacted = consent_plan.get("impacted_artifacts")
    if not isinstance(impacted, list):
        impacted = []
    revocation_ids = {item.get("intelligence_id") for item in impacted if isinstance(item, dict) and item.get("intelligence_id")}
    revocation_ids.update(item.get("intelligence_id") for item in consent_plan.get("source_actions", []) if isinstance(item, dict) and item.get("intelligence_id"))
    unresolved = [item for item in consent_plan.get("unresolved", []) if isinstance(item, dict)]
    return context, {item for item in revocation_ids if isinstance(item, str)}, unresolved


def evaluate_collective_intelligence(
    intelligence_items: Iterable[dict[str, Any]],
    consent_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    items = [copy.deepcopy(item) for item in intelligence_items if isinstance(item, dict)]
    if not items:
        raise CollectiveIntelligenceError("at least one intelligence item is required")
    consent_context, revoked_ids, inherited_unresolved = consent_plan_context(consent_plan)
    evaluated = []
    all_reasons = []
    for item in items:
        item_id = text(item.get("intelligence_id") or item.get("event_id") or item.get("id"), "intelligence_id")
        stages = []
        reasons = []

        private_status = "PASS" if state(item.get("visibility")) == "PRIVATE" else "FAIL"
        stages.append({"stage": "PRIVATE_INTELLIGENCE", "status": private_status})
        if private_status == "FAIL":
            reasons.append("INPUT_MUST_BE_PRIVATE")

        consent = item.get("consent") if isinstance(item.get("consent"), dict) else {}
        consent_state = state(consent.get("state"))
        consent_scope = consent.get("scope") if isinstance(consent.get("scope"), list) else []
        consent_status = "PASS" if consent_state in {"ACTIVE", "EXPLICIT", "GRANTED"} and consent.get("grant_id") and "COLLECTIVE" in {str(scope).upper() for scope in consent_scope} else "FAIL"
        stages.append({"stage": "OWNER_CONSENT", "status": consent_status})
        if consent_status == "FAIL":
            reasons.append("OWNER_CONSENT_FOR_COLLECTIVE_REQUIRED")

        policy = item.get("sharing_policy") if isinstance(item.get("sharing_policy"), dict) else {}
        policy_scope = policy.get("allowed_scopes") if isinstance(policy.get("allowed_scopes"), list) else []
        policy_status = "PASS" if state(policy.get("state")) in {"ALLOW", "APPROVED", "ACTIVE"} and policy.get("policy_ref") and "COLLECTIVE" in {str(scope).upper() for scope in policy_scope} else "FAIL"
        stages.append({"stage": "SHARING_POLICY", "status": policy_status})
        if policy_status == "FAIL":
            reasons.append("SHARING_POLICY_REQUIRED")

        identity = item.get("identity_policy") if isinstance(item.get("identity_policy"), dict) else {}
        identity_status = "PASS" if state(identity.get("state")) == "VERIFIED" and identity.get("anonymization_verified") is True and identity.get("identity_boundary") and identity.get("raw_owner_identity_exposed") is not True else "FAIL"
        stages.append({"stage": "ANONYMIZATION_IDENTITY_POLICY", "status": identity_status})
        if identity_status == "FAIL":
            reasons.append("ANONYMIZATION_IDENTITY_POLICY_REQUIRED")

        source_ids = refs(item.get("source_ids"), "source_ids") if item.get("source_ids") is not None else []
        if not source_ids:
            reasons.append("SOURCE_LINEAGE_REQUIRED")
        contributions, contribution_errors = contribution_references(item.get("contribution_provenance"))
        reasons.extend(contribution_errors)
        authority = item.get("source_authority") if isinstance(item.get("source_authority"), dict) else {}
        authority_status = "PASS" if state(authority.get("state")) in {"VERIFIED", "AUTHORIZED", "ACTIVE"} and authority.get("authority_ref") else "FAIL"
        if authority_status == "FAIL":
            reasons.append("SOURCE_AUTHORITY_REQUIRED")
        revocation_state = state(item.get("revocation_state") or consent.get("revocation_state"))
        if revocation_state in {"REVOKED", "INVALID", "BLOCKED"}:
            reasons.append("CONSENT_REVOKED")
        if revoked_ids.intersection(source_ids):
            reasons.append("CONSENT_REVOCATION_REVIEW_REQUIRED")
        usage_scope = text(item.get("usage_scope"), "usage_scope") if item.get("usage_scope") is not None else ""
        if not usage_scope:
            reasons.append("USAGE_SCOPE_REQUIRED")
        collective_status = "PASS" if not reasons else "FAIL"
        stages.append({"stage": "COLLECTIVE_INTELLIGENCE", "status": collective_status})
        projection = None
        if collective_status == "PASS":
            projection = {
                "collective_id": f"collective:{item_id}",
                "status": "PROPOSED",
                "source_authority": {
                    "state": state(authority.get("state")),
                    "authority_ref": authority.get("authority_ref"),
                },
                "contribution_provenance": contributions,
                "consent": {
                    "state": consent_state,
                    "grant_id": consent.get("grant_id"),
                    "scope": sorted(str(scope).upper() for scope in consent_scope),
                },
                "visibility": "COLLECTIVE",
                "revocation_state": revocation_state or "ACTIVE",
                "usage_scope": usage_scope,
                "identity_policy_ref": identity.get("identity_policy_ref") or identity.get("policy_ref"),
                "source_ids": sorted(source_ids),
            }
        evaluated.append(
            {
                "intelligence_id": item_id,
                "eligible": collective_status == "PASS",
                "stages": stages,
                "reasons": sorted(set(reasons)),
                "proposed_collective": projection,
            }
        )
        all_reasons.extend(reasons)
    unresolved = [copy.deepcopy(item) for item in inherited_unresolved]
    if consent_context["status"] not in {"COMPLETE", "NO_KNOWN_DEPENDENTS"}:
        unresolved.append({"code": "CONSENT_PLAN_NOT_COMPLETE", "status": consent_context["status"]})
    if unresolved:
        status = "PARTIAL"
    elif any(not item["eligible"] for item in evaluated):
        status = "BLOCKED"
    else:
        status = "COMPLETE"
    return {
        "schema": PLAN_SCHEMA,
        "status": status,
        "mode": "PROPOSAL_ONLY",
        "pipeline": list(PIPELINE),
        "consent_plan_context": consent_context,
        "items": evaluated,
        "eligible_item_ids": [item["intelligence_id"] for item in evaluated if item["eligible"]],
        "blocked_item_ids": [item["intelligence_id"] for item in evaluated if not item["eligible"]],
        "unresolved": unresolved,
        "execution_performed": False,
        "publication_performed": False,
        "persistence_performed": False,
        "truth_boundary": "This gate proposes metadata-only collective projections. It does not publish, copy private content, bypass consent, or create System 60 federation.",
    }


def validate_collective_plan(plan: dict[str, Any]) -> list[str]:
    errors = []
    if plan.get("schema") != PLAN_SCHEMA or plan.get("mode") != "PROPOSAL_ONLY":
        return ["collective plan schema or mode is invalid"]
    if plan.get("pipeline") != list(PIPELINE):
        errors.append("collective pipeline order is invalid")
    if plan.get("execution_performed") is not False or plan.get("publication_performed") is not False or plan.get("persistence_performed") is not False:
        errors.append("proposal-only boundary is invalid")
    for item in plan.get("items", []):
        if [stage.get("stage") for stage in item.get("stages", [])] != list(PIPELINE):
            errors.append(f"item {item.get('intelligence_id')} pipeline is invalid")
        if item.get("eligible") is True and item.get("proposed_collective") is None:
            errors.append(f"eligible item {item.get('intelligence_id')} has no proposal")
        if item.get("eligible") is False and item.get("proposed_collective") is not None:
            errors.append(f"blocked item {item.get('intelligence_id')} has a proposal")
    return errors
