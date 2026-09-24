from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "capabilities" / "registry.v1.json"
LIFECYCLE = (
    "DISCOVER",
    "REQUEST",
    "AUTHORIZE",
    "EXECUTE",
    "RECEIVE",
    "VERIFY",
    "PERSIST",
    "INDEX",
    "LEARN",
)
RECEIPT_SCHEMA = "naya-smart-door-receipt/v1"
RUN_SCHEMA = "naya-smart-door-run/v1"
HEX_256 = 64


class SmartDoorError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SmartDoorError(f"{field} is required")
    return value.strip()


def require_digest(value: Any, field: str) -> str:
    text = require_text(value, field).lower()
    if len(text) != HEX_256 or any(character not in "0123456789abcdef" for character in text):
        raise SmartDoorError(f"{field} must be a SHA-256 hex digest")
    return text


def require_refs(values: Any, field: str) -> list[str]:
    if not isinstance(values, list) or not values:
        raise SmartDoorError(f"{field} must contain at least one reference")
    refs = [require_text(value, field) for value in values]
    if len(refs) != len(set(refs)):
        raise SmartDoorError(f"{field} must not contain duplicate references")
    return refs


def load_capabilities(path: Path = DEFAULT_REGISTRY) -> tuple[str, dict[str, dict[str, Any]]]:
    registry = json.loads(path.read_text(encoding="utf-8"))
    if registry.get("schema") != "NAYA_CAPABILITY_REGISTRY_V1":
        raise SmartDoorError("capability registry schema is invalid")
    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        raise SmartDoorError("capability registry has no capabilities")
    indexed = {capability.get("id"): capability for capability in capabilities}
    if None in indexed or len(indexed) != len(capabilities):
        raise SmartDoorError("capability registry IDs are missing or duplicated")
    return require_text(registry.get("version"), "registry version"), indexed


class SmartDoorRun:
    def __init__(
        self,
        capability_id: str,
        request_id: str,
        idempotency_key: str,
        registry_path: Path = DEFAULT_REGISTRY,
    ) -> None:
        self.capability_id = require_text(capability_id, "capability_id")
        self.request_id = require_text(request_id, "request_id")
        self.idempotency_key = require_text(idempotency_key, "idempotency_key")
        self.registry_version, self.capabilities = load_capabilities(registry_path)
        if self.capability_id not in self.capabilities:
            raise SmartDoorError(f"unknown capability: {self.capability_id}")
        self.capability = copy.deepcopy(self.capabilities[self.capability_id])
        self.state = "DISCOVER"
        self.complete = False
        self.requested_scope: list[str] | None = None
        self.input_sha256: str | None = None
        self.authority_ref: str | None = None
        self.executor_id: str | None = None
        self.receipts: list[dict[str, Any]] = []
        implementation = self.capability["implementation"]
        self._append(
            "DISCOVER",
            {
                "capability_description": self.capability["description"],
                "required_authority": self.capability["required_authority"],
                "allowed_scope": self.capability["allowed_scope"],
                "risk": self.capability["risk"],
                "reversibility": self.capability["reversibility"],
                "receipt_required": self.capability["receipt_required"],
                "verification_required": self.capability["verification_required"],
                "implementation_status": implementation["status"],
                "evidence_state": implementation["evidence_state"],
                "authority_enforcement": implementation["authority_enforcement"],
                "source_paths": implementation["source_paths"],
                "transport_aliases": implementation["transport_aliases"],
            },
        )

    @property
    def terminal_receipt_sha256(self) -> str | None:
        return self.receipts[-1]["receipt_sha256"] if self.complete and self.receipts else None

    def _append(self, state: str, details: dict[str, Any]) -> dict[str, Any]:
        expected_state = LIFECYCLE[len(self.receipts)]
        if state != expected_state:
            raise SmartDoorError(f"lifecycle order violation: expected {expected_state}, received {state}")
        previous = self.receipts[-1]["receipt_sha256"] if self.receipts else None
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "capability_id": self.capability_id,
            "request_id": self.request_id,
            "idempotency_key": self.idempotency_key,
            "registry_version": self.registry_version,
            "sequence": len(self.receipts),
            "state": state,
            "previous_receipt_sha256": previous,
            "details": details,
        }
        receipt["receipt_sha256"] = sha256_value(receipt)
        self.receipts.append(receipt)
        self.state = state
        return copy.deepcopy(receipt)

    def _require_state(self, expected: str) -> None:
        if self.complete or self.state != expected:
            raise SmartDoorError(f"lifecycle requires {expected}; current state is {self.state}")

    def record_request(self, payload: Any, requested_scope: list[str]) -> dict[str, Any]:
        self._require_state("DISCOVER")
        scope = require_refs(requested_scope, "requested_scope")
        allowed_scope = set(self.capability["allowed_scope"])
        if not set(scope).issubset(allowed_scope):
            raise SmartDoorError("requested_scope exceeds the registered allowed_scope")
        self.requested_scope = scope
        self.input_sha256 = sha256_value(payload)
        return self._append("REQUEST", {"input_sha256": self.input_sha256, "requested_scope": scope})

    def record_authorization(
        self,
        authority_ref: str,
        authority_evidence_sha256: str,
        authorization_verifier_id: str,
    ) -> dict[str, Any]:
        self._require_state("REQUEST")
        if self.requested_scope is None or self.input_sha256 is None:
            raise SmartDoorError("authorization requires a recorded request")
        self.authority_ref = require_text(authority_ref, "authority_ref")
        details = {
            "authority_ref": self.authority_ref,
            "authority_status": "AUTHORIZED",
            "authorized_capability_id": self.capability_id,
            "authorized_scope": list(self.requested_scope),
            "authority_evidence_sha256": require_digest(authority_evidence_sha256, "authority_evidence_sha256"),
            "authorization_verifier_id": require_text(authorization_verifier_id, "authorization_verifier_id"),
            "input_sha256": self.input_sha256,
        }
        return self._append("AUTHORIZE", details)

    def record_execution(
        self,
        executor_id: str,
        execution_receipt_ref: str,
        response_sha256: str,
    ) -> dict[str, Any]:
        self._require_state("AUTHORIZE")
        if self.authority_ref is None:
            raise SmartDoorError("execution requires a recorded authority decision")
        self.executor_id = require_text(executor_id, "executor_id")
        details = {
            "authority_ref": self.authority_ref,
            "executor_id": self.executor_id,
            "execution_receipt_ref": require_text(execution_receipt_ref, "execution_receipt_ref"),
            "response_sha256": require_digest(response_sha256, "response_sha256"),
        }
        return self._append("EXECUTE", details)

    def record_receive(self, received_artifact_ref: str, received_sha256: str) -> dict[str, Any]:
        self._require_state("EXECUTE")
        details = {
            "executor_id": self.executor_id,
            "received_artifact_ref": require_text(received_artifact_ref, "received_artifact_ref"),
            "received_sha256": require_digest(received_sha256, "received_sha256"),
        }
        return self._append("RECEIVE", details)

    def record_verification(
        self,
        verifier_id: str,
        evidence_refs: list[str],
        verification_evidence_sha256: str,
    ) -> dict[str, Any]:
        self._require_state("RECEIVE")
        verifier = require_text(verifier_id, "verifier_id")
        if verifier == self.executor_id:
            raise SmartDoorError("verification actor must differ from execution actor")
        if self.capability["verification_required"] is not True and not evidence_refs:
            raise SmartDoorError("verification evidence is required when evidence is supplied")
        details = {
            "verifier_id": verifier,
            "verification_status": "VERIFIED",
            "evidence_refs": require_refs(evidence_refs, "evidence_refs"),
            "verification_evidence_sha256": require_digest(
                verification_evidence_sha256,
                "verification_evidence_sha256",
            ),
        }
        return self._append("VERIFY", details)

    def record_persistence(self, persistence_receipt_ref: str, idempotency_status: str) -> dict[str, Any]:
        self._require_state("VERIFY")
        if idempotency_status not in {"CREATED", "REPLAYED"}:
            raise SmartDoorError("persistence idempotency_status must be CREATED or REPLAYED")
        details = {
            "persistence_receipt_ref": require_text(persistence_receipt_ref, "persistence_receipt_ref"),
            "idempotency_status": idempotency_status,
        }
        return self._append("PERSIST", details)

    def record_index(self, index_receipt_ref: str, indexed_object_refs: list[str]) -> dict[str, Any]:
        self._require_state("PERSIST")
        details = {
            "index_receipt_ref": require_text(index_receipt_ref, "index_receipt_ref"),
            "indexed_object_refs": require_refs(indexed_object_refs, "indexed_object_refs"),
        }
        return self._append("INDEX", details)

    def record_learning(self, learning_receipt_ref: str, disposition: str) -> dict[str, Any]:
        self._require_state("INDEX")
        if disposition not in {"NO_LEARNING", "CANDIDATE_ONLY"}:
            raise SmartDoorError("lifecycle v1 permits only NO_LEARNING or CANDIDATE_ONLY")
        details = {
            "learning_receipt_ref": require_text(learning_receipt_ref, "learning_receipt_ref"),
            "learning_disposition": disposition,
            "authority_unchanged": True,
        }
        return self._append("LEARN", details)

    def complete_run(self) -> dict[str, Any]:
        if self.complete or self.state != "LEARN":
            raise SmartDoorError("only a completed LEARN stage can close the run")
        self.complete = True
        return self.export()

    def export(self) -> dict[str, Any]:
        return {
            "schema": RUN_SCHEMA,
            "capability_id": self.capability_id,
            "request_id": self.request_id,
            "idempotency_key": self.idempotency_key,
            "registry_version": self.registry_version,
            "state": "COMPLETE" if self.complete else self.state,
            "complete": self.complete,
            "required_authority": copy.deepcopy(self.capability["required_authority"]),
            "authority_enforcement_observed": self.capability["implementation"]["authority_enforcement"],
            "receipts": copy.deepcopy(self.receipts),
            "terminal_receipt_sha256": self.terminal_receipt_sha256,
            "truth_boundary": "This lifecycle validates and chains externally produced evidence. It does not call an external capability, mint authority, or turn a receipt into independent verification.",
        }


def validate_run(run: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if run.get("schema") != RUN_SCHEMA:
        return ["run schema is invalid"]
    if run.get("state") not in set(LIFECYCLE) | {"COMPLETE"}:
        errors.append("run state is invalid")
    receipts = run.get("receipts")
    if not isinstance(receipts, list):
        return errors + ["receipts must be a list"]
    previous: str | None = None
    for index, receipt in enumerate(receipts):
        if receipt.get("schema") != RECEIPT_SCHEMA:
            errors.append(f"receipt {index} schema is invalid")
        if receipt.get("sequence") != index:
            errors.append(f"receipt {index} sequence is invalid")
        if index >= len(LIFECYCLE) or receipt.get("state") != LIFECYCLE[index]:
            errors.append(f"receipt {index} lifecycle state is invalid")
        for field in ("capability_id", "request_id", "idempotency_key", "registry_version"):
            if receipt.get(field) != run.get(field):
                errors.append(f"receipt {index} {field} does not match run")
        if receipt.get("previous_receipt_sha256") != previous:
            errors.append(f"receipt {index} previous receipt digest does not match")
        recorded = receipt.get("receipt_sha256")
        material = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        if recorded != sha256_value(material):
            errors.append(f"receipt {index} digest is invalid")
        previous = recorded
    expected_state = "COMPLETE" if run.get("complete") is True else LIFECYCLE[len(receipts) - 1] if receipts else None
    if run.get("state") != expected_state:
        errors.append("run state does not match receipt completion")
    if run.get("complete") is True and len(receipts) != len(LIFECYCLE):
        errors.append("complete run does not contain every lifecycle receipt")
    if run.get("terminal_receipt_sha256") != (receipts[-1].get("receipt_sha256") if run.get("complete") and receipts else None):
        errors.append("terminal receipt digest is invalid")
    return errors
