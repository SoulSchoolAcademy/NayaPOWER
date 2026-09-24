from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

PLAN_SCHEMA = "NAYAPOWER_DISTRIBUTED_CONTINUITY_PLAN_V1"
RUNTIMES = {"LOCAL", "CLOUD", "MOBILE", "WEB", "AI_PROVIDER", "AGENT", "NAYANET"}
REQUIRED_DIMENSIONS = ("identity", "authority", "memory", "provenance", "governance", "continuity", "consent")
FORBIDDEN_PAYLOAD_KEYS = {"payload", "content", "raw_payload", "data", "body"}


class DistributedContinuityError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def text(value: Any, field: str, reasons: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        reasons.append(f"{field.upper()}_MISSING")
        return None
    return value.strip()


def refs(value: Any, field: str, reasons: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        reasons.append(f"{field.upper()}_MISSING")
        return []
    result = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(result) != len(value) or len(result) != len(set(result)):
        reasons.append(f"{field.upper()}_INVALID")
    return sorted(result)


def valid_state(value: Any, accepted: set[str]) -> bool:
    return isinstance(value, str) and value.strip().upper() in accepted


def plan_distributed_continuity(envelope: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(envelope, dict):
        raise DistributedContinuityError("continuity envelope must be an object")
    reasons: list[str] = []
    forbidden = sorted(FORBIDDEN_PAYLOAD_KEYS.intersection(envelope))
    if forbidden:
        reasons.extend(f"RAW_PAYLOAD_FIELD_FORBIDDEN:{field}" for field in forbidden)
    envelope_id = text(envelope.get("envelope_id"), "envelope_id", reasons)
    source_runtime = text(envelope.get("source_runtime"), "source_runtime", reasons)
    target_runtime = text(envelope.get("target_runtime"), "target_runtime", reasons)
    if source_runtime and source_runtime not in RUNTIMES:
        reasons.append("SOURCE_RUNTIME_UNKNOWN")
    if target_runtime and target_runtime not in RUNTIMES:
        reasons.append("TARGET_RUNTIME_UNKNOWN")
    if source_runtime and target_runtime and source_runtime == target_runtime:
        reasons.append("SAME_RUNTIME_ROUTE_NOT_DISTRIBUTED")
    identity = envelope.get("subject_identity") if isinstance(envelope.get("subject_identity"), dict) else {}
    subject_id = text(identity.get("subject_id"), "subject_id", reasons)
    binding_status = text(identity.get("binding_status"), "identity_binding_status", reasons)
    if subject_id == "NAYA" and binding_status != "VERIFIED":
        reasons.append("NAYA_SUBJECT_BINDING_NOT_ESTABLISHED")
    elif not subject_id or binding_status != "VERIFIED":
        reasons.append("IDENTITY_BINDING_UNVERIFIED")
    authority = envelope.get("authority") if isinstance(envelope.get("authority"), dict) else {}
    authority_ref = text(authority.get("authority_ref"), "authority_ref", reasons)
    if not valid_state(authority.get("state"), {"VERIFIED", "AUTHORIZED", "ACTIVE"}):
        reasons.append("AUTHORITY_UNVERIFIED")
    memory = envelope.get("memory") if isinstance(envelope.get("memory"), dict) else {}
    memory_refs = refs(memory.get("refs"), "memory_refs", reasons)
    if not valid_state(memory.get("state"), {"VERIFIED", "CURRENT"}):
        reasons.append("MEMORY_UNVERIFIED")
    provenance = envelope.get("provenance") if isinstance(envelope.get("provenance"), dict) else {}
    provenance_refs = refs(provenance.get("refs"), "provenance_refs", reasons)
    if not valid_state(provenance.get("state"), {"VERIFIED", "CURRENT"}):
        reasons.append("PROVENANCE_UNVERIFIED")
    if not isinstance(provenance.get("payload_sha256"), str) or len(provenance.get("payload_sha256", "")) != 64:
        reasons.append("PAYLOAD_DIGEST_MISSING")
    governance = envelope.get("governance") if isinstance(envelope.get("governance"), dict) else {}
    policy_ref = text(governance.get("policy_ref"), "governance_policy_ref", reasons)
    if not valid_state(governance.get("state"), {"VERIFIED", "AUTHORIZED", "ACTIVE"}):
        reasons.append("GOVERNANCE_UNVERIFIED")
    continuity = envelope.get("continuity") if isinstance(envelope.get("continuity"), dict) else {}
    continuity_ref = text(continuity.get("receipt_ref"), "continuity_receipt_ref", reasons)
    if not valid_state(continuity.get("state"), {"VERIFIED", "CURRENT"}):
        reasons.append("CONTINUITY_UNVERIFIED")
    consent = envelope.get("consent") if isinstance(envelope.get("consent"), dict) else {}
    if not valid_state(consent.get("state"), {"ACTIVE", "EXPLICIT", "VERIFIED"}):
        reasons.append("CONSENT_NOT_ACTIVE")
    if consent.get("revocation_plan_status") not in {"COMPLETE", "NO_KNOWN_DEPENDENTS"}:
        reasons.append("CONSENT_REVOCATION_PLAN_NOT_COMPLETE")
    registry_version = text(envelope.get("capability_registry_version"), "capability_registry_version", reasons)
    lifecycle_version = text(envelope.get("smart_door_lifecycle_version"), "smart_door_lifecycle_version", reasons)
    dimensions = {
        "identity": {"status": "VERIFIED" if subject_id and binding_status == "VERIFIED" and "NAYA_SUBJECT_BINDING_NOT_ESTABLISHED" not in reasons else "BLOCKED", "subject_id": subject_id, "binding_status": binding_status},
        "authority": {"status": "VERIFIED" if authority_ref and "AUTHORITY_UNVERIFIED" not in reasons else "BLOCKED", "authority_ref": authority_ref},
        "memory": {"status": "VERIFIED" if memory_refs and "MEMORY_UNVERIFIED" not in reasons else "BLOCKED", "refs": memory_refs},
        "provenance": {"status": "VERIFIED" if provenance_refs and "PROVENANCE_UNVERIFIED" not in reasons and "PAYLOAD_DIGEST_MISSING" not in reasons else "BLOCKED", "refs": provenance_refs, "payload_sha256": provenance.get("payload_sha256")},
        "governance": {"status": "VERIFIED" if policy_ref and "GOVERNANCE_UNVERIFIED" not in reasons else "BLOCKED", "policy_ref": policy_ref},
        "continuity": {"status": "VERIFIED" if continuity_ref and "CONTINUITY_UNVERIFIED" not in reasons else "BLOCKED", "receipt_ref": continuity_ref},
        "consent": {"status": "VERIFIED" if "CONSENT_NOT_ACTIVE" not in reasons and "CONSENT_REVOCATION_PLAN_NOT_COMPLETE" not in reasons else "BLOCKED", "state": consent.get("state"), "revocation_plan_status": consent.get("revocation_plan_status")},
    }
    normalized = {
        "envelope_id": envelope_id,
        "source_runtime": source_runtime,
        "target_runtime": target_runtime,
        "subject_identity": identity,
        "authority": authority,
        "memory": memory,
        "provenance": provenance,
        "governance": governance,
        "continuity": continuity,
        "consent": consent,
        "capability_registry_version": registry_version,
        "smart_door_lifecycle_version": lifecycle_version,
    }
    unique_reasons = sorted(set(reasons))
    status = "COMPLETE" if not unique_reasons else "BLOCKED"
    return {
        "schema": PLAN_SCHEMA,
        "status": status,
        "mode": "PLAN_ONLY",
        "envelope": normalized,
        "envelope_sha256": digest_value(normalized),
        "required_dimensions": list(REQUIRED_DIMENSIONS),
        "dimensions": dimensions,
        "eligible_for_transport": not unique_reasons,
        "blocked_reasons": unique_reasons,
        "execution_performed": False,
        "network_transport_performed": False,
        "payload_propagated": False,
        "federation_created": False,
        "truth_boundary": "This gate validates a metadata-only continuity envelope. It does not bind NAYA to an invented identity, transmit payloads, call providers, or create federation.",
    }


def validate_continuity_plan(plan: dict[str, Any]) -> list[str]:
    errors = []
    if plan.get("schema") != PLAN_SCHEMA or plan.get("mode") != "PLAN_ONLY":
        return ["continuity plan schema or mode is invalid"]
    if plan.get("eligible_for_transport") is True and plan.get("status") != "COMPLETE":
        errors.append("eligible plan status is invalid")
    if plan.get("execution_performed") is not False or plan.get("network_transport_performed") is not False or plan.get("payload_propagated") is not False or plan.get("federation_created") is not False:
        errors.append("transport-only boundary is invalid")
    if plan.get("envelope_sha256") != digest_value(plan.get("envelope")):
        errors.append("envelope fingerprint is invalid")
    if set(plan.get("required_dimensions", [])) != set(REQUIRED_DIMENSIONS):
        errors.append("required continuity dimensions are invalid")
    if plan.get("status") == "BLOCKED" and not plan.get("blocked_reasons"):
        errors.append("blocked plan has no reasons")
    if plan.get("status") == "COMPLETE" and plan.get("blocked_reasons"):
        errors.append("complete plan has blocked reasons")
    return errors
