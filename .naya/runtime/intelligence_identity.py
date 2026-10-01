#!/usr/bin/env python3
"""NayaNET Governed Intelligence Identity Envelope V1.

This is an identity/provenance envelope for intelligence-bearing actors.
It does not replace account identity, the canonical identity registry, or the
NayaPOWER authority registry. It does not mint authority.

The envelope answers thirteen questions:

1. Who are you?
2. What are you?
3. Who created/delegated you?
4. What do you know?
5. What can you do?
6. What are you authorized to do?
7. Who authorized that?
8. What did you receive from another agent?
9. What provenance came with it?
10. What can you delegate?
11. What did you actually do?
12. What happened?
13. What did you learn?
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping


ACTOR_CLASSES = {"HUMAN", "NAYA", "AGENT", "MACHINE", "SYSTEM", "COLLECTIVE", "UNKNOWN"}
EPISTEMIC_STATES = {"KNOWN", "OBSERVED", "VERIFIED", "INFERRED", "ASSUMED", "UNKNOWN"}
OUTCOME_STATES = {"UNVERIFIED", "OBSERVED", "VERIFIED"}
LEARNING_STATES = {"PROPOSED", "SUPPORTED", "VERIFIED"}


@dataclass(frozen=True)
class IdentityValidation:
    valid: bool
    errors: tuple[str, ...]
    identity_fingerprint: str


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def identity_fingerprint(envelope: Mapping[str, Any]) -> str:
    payload = dict(envelope)
    payload.pop("identity_fingerprint", None)
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def validate_identity_envelope(envelope: Mapping[str, Any], *, consequential: bool = False) -> IdentityValidation:
    errors: list[str] = []
    if not isinstance(envelope, Mapping):
        return IdentityValidation(False, ("identity envelope must be an object",), "")

    required = (
        "schema_version",
        "identity_id",
        "actor_class",
        "who_created_or_delegated",
        "knowledge",
        "capabilities",
        "authority",
        "authorized_by",
        "received_artifacts",
        "provenance",
        "delegation",
        "actual_actions",
        "outcomes",
        "learning",
    )
    for key in required:
        if key not in envelope:
            errors.append(f"missing required identity field: {key}")

    if envelope.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    identity_id = envelope.get("identity_id")
    if not isinstance(identity_id, str) or not identity_id.strip():
        errors.append("identity_id must be non-empty")

    actor_class = envelope.get("actor_class")
    if actor_class not in ACTOR_CLASSES:
        errors.append("actor_class is invalid")

    if consequential and actor_class == "UNKNOWN":
        errors.append("UNKNOWN identity cannot perform consequential actions")

    lineage = envelope.get("who_created_or_delegated")
    if not isinstance(lineage, Mapping):
        errors.append("who_created_or_delegated must be an object")
    else:
        state = lineage.get("lineage_state")
        if state not in {"ROOT", "CREATED", "DELEGATED", "UNKNOWN"}:
            errors.append("invalid lineage_state")
        if state == "DELEGATED" and not lineage.get("delegator_ref"):
            errors.append("DELEGATED identity requires delegator_ref")

    knowledge = envelope.get("knowledge")
    if not isinstance(knowledge, list):
        errors.append("knowledge must be a list")
    else:
        for index, item in enumerate(knowledge):
            if not isinstance(item, Mapping):
                errors.append(f"knowledge[{index}] must be an object")
                continue
            if not item.get("knowledge_id") or not item.get("claim"):
                errors.append(f"knowledge[{index}] requires knowledge_id and claim")
            sources = item.get("source_refs")
            if not isinstance(sources, list) or not sources:
                errors.append(f"knowledge[{index}] requires source_refs")
            if item.get("epistemic_state") not in EPISTEMIC_STATES:
                errors.append(f"knowledge[{index}] has invalid epistemic_state")

    capabilities = envelope.get("capabilities")
    if not isinstance(capabilities, list) or any(not isinstance(x, str) or not x.strip() for x in capabilities):
        errors.append("capabilities must be a list of non-empty strings")

    authority = envelope.get("authority")
    if not isinstance(authority, Mapping):
        errors.append("authority must be an object")
    elif not isinstance(authority.get("authority_ids"), list):
        errors.append("authority.authority_ids must be a list")

    authorized_by = envelope.get("authorized_by")
    if not isinstance(authorized_by, list):
        errors.append("authorized_by must be a list")
    else:
        for index, item in enumerate(authorized_by):
            if not isinstance(item, Mapping) or not item.get("authority_id") or not item.get("authorizer_ref"):
                errors.append(f"authorized_by[{index}] requires authority_id and authorizer_ref")

    received = envelope.get("received_artifacts")
    if not isinstance(received, list):
        errors.append("received_artifacts must be a list")
    else:
        for index, item in enumerate(received):
            if not isinstance(item, Mapping):
                errors.append(f"received_artifacts[{index}] must be an object")
                continue
            for key in ("artifact_id", "artifact_type", "source_ref", "received_at"):
                if not item.get(key):
                    errors.append(f"received_artifacts[{index}] requires {key}")

    provenance = envelope.get("provenance")
    if not isinstance(provenance, list):
        errors.append("provenance must be a list")
    else:
        for index, item in enumerate(provenance):
            if not isinstance(item, Mapping):
                errors.append(f"provenance[{index}] must be an object")
                continue
            for key in ("subject_id", "source_ref", "relation"):
                if not item.get(key):
                    errors.append(f"provenance[{index}] requires {key}")

    delegation = envelope.get("delegation")
    if not isinstance(delegation, Mapping):
        errors.append("delegation must be an object")
    else:
        can_delegate = delegation.get("can_delegate")
        if not isinstance(can_delegate, bool):
            errors.append("delegation.can_delegate must be boolean")
        if can_delegate and not envelope.get("authority", {}).get("authority_ids"):
            errors.append("can_delegate=true requires an explicit authority reference")
        if can_delegate and not delegation.get("chain"):
            errors.append("can_delegate=true requires a delegation chain")

    actions = envelope.get("actual_actions")
    if not isinstance(actions, list):
        errors.append("actual_actions must be a list")
    else:
        for index, item in enumerate(actions):
            if not isinstance(item, Mapping):
                errors.append(f"actual_actions[{index}] must be an object")
                continue
            for key in ("execution_id", "action_ref", "receipt_ref"):
                if not item.get(key):
                    errors.append(f"actual_actions[{index}] requires {key}")

    outcomes = envelope.get("outcomes")
    if not isinstance(outcomes, list):
        errors.append("outcomes must be a list")
    else:
        for index, item in enumerate(outcomes):
            if not isinstance(item, Mapping):
                errors.append(f"outcomes[{index}] must be an object")
                continue
            for key in ("execution_id", "outcome_ref", "evidence_refs"):
                if not item.get(key):
                    errors.append(f"outcomes[{index}] requires {key}")
            if item.get("verification_state") not in OUTCOME_STATES:
                errors.append(f"outcomes[{index}] has invalid verification_state")

    learning = envelope.get("learning")
    if not isinstance(learning, list):
        errors.append("learning must be a list")
    else:
        for index, item in enumerate(learning):
            if not isinstance(item, Mapping):
                errors.append(f"learning[{index}] must be an object")
                continue
            for key in ("learning_id", "claim", "source_refs"):
                if not item.get(key):
                    errors.append(f"learning[{index}] requires {key}")
            if item.get("derivation_state") not in LEARNING_STATES:
                errors.append(f"learning[{index}] has invalid derivation_state")

    # Authority is never inferred from capability.
    if envelope.get("capabilities") and not envelope.get("authority", {}).get("authority_ids"):
        errors.append("capability presence does not establish authority")

    return IdentityValidation(not errors, tuple(dict.fromkeys(errors)), identity_fingerprint(envelope))
