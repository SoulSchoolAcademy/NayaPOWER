"""Machine-executable integrity layer for N9-000/N9-001.

This module validates experiment receipts and enforces fail-closed admission.
It deliberately does not claim that a validated receipt is runtime proof unless
the receipt contains independently captured runtime evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable


NODES = (
    "MN-01",
    "MN-02",
    "MN-03",
    "MN-04",
    "MN-05",
    "MN-06",
    "MN-07",
    "MN-08",
    "MN-09",
)

ALLOWED_CONDITIONS = {"control", "treatment"}
REQUIRED_FIELDS = {
    "experiment_id",
    "test_id",
    "source_sha",
    "runtime_id",
    "runtime_version",
    "deployment_identity",
    "owner_id",
    "session_id",
    "control_or_treatment",
    "scenario_hash",
    "input_hash",
    "node_invocations",
    "authority_decision",
    "decision_before",
    "decision_after",
    "action",
    "observed_outcome",
    "verification",
    "causal_delta",
    "status",
}


@dataclass(frozen=True)
class ValidationResult:
    status: str
    reason: str = ""


def _hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def build_receipt(
    *,
    experiment_id: str,
    test_id: str,
    source_sha: str,
    runtime: dict[str, Any],
    control_or_treatment: str,
    scenario: Any,
    input_payload: Any,
    node_invocations: list[dict[str, Any]],
    authority_decision: str,
    decision_before: Any,
    decision_after: Any,
    action: Any,
    observed_outcome: Any,
    verification: dict[str, Any],
    causal_delta: dict[str, Any],
    expected_source_sha: str | None = None,
    expected_owner_id: str | None = None,
    expected_session_id: str | None = None,
) -> dict[str, Any]:
    _require(control_or_treatment in ALLOWED_CONDITIONS,
             "control_or_treatment must be control or treatment")
    _require(bool(source_sha), "source_sha is required")
    _require(bool(runtime.get("runtime_id")), "runtime_id is required")
    _require(runtime.get("version") is not None, "runtime version is required")
    _require(bool(runtime.get("deployment_identity")), "deployment_identity is required")
    if expected_source_sha is not None:
        _require(source_sha == expected_source_sha, "source SHA mismatch")
    if expected_owner_id is not None:
        _require(runtime.get("owner_id") == expected_owner_id, "owner mismatch")
    if expected_session_id is not None:
        _require(runtime.get("session_id") == expected_session_id, "session mismatch")

    return {
        "experiment_id": experiment_id,
        "test_id": test_id,
        "source_sha": source_sha,
        "runtime_id": runtime["runtime_id"],
        "runtime_version": runtime["version"],
        "deployment_identity": runtime["deployment_identity"],
        "owner_id": runtime.get("owner_id"),
        "session_id": runtime.get("session_id"),
        "control_or_treatment": control_or_treatment,
        "scenario_hash": _hash(scenario),
        "input_hash": _hash(input_payload),
        "node_invocations": node_invocations,
        "authority_decision": authority_decision,
        "decision_before": decision_before,
        "decision_after": decision_after,
        "action": action,
        "observed_outcome": observed_outcome,
        "verification": verification,
        "causal_delta": causal_delta,
        "status": "PROVEN",
    }


def validate_receipt(
    receipt: dict[str, Any],
    *,
    expected_source_sha: str | None = None,
    expected_owner_id: str | None = None,
    expected_session_id: str | None = None,
    expected_condition: str | None = None,
) -> ValidationResult:
    missing = REQUIRED_FIELDS.difference(receipt)
    if missing:
        return ValidationResult("FAIL", f"missing required fields: {sorted(missing)}")

    condition = receipt["control_or_treatment"]
    if condition not in ALLOWED_CONDITIONS:
        return ValidationResult("FAIL", "invalid control/treatment condition")
    if expected_condition is not None and condition != expected_condition:
        return ValidationResult("FAIL", "control/treatment condition mismatch")

    if expected_source_sha is not None and receipt["source_sha"] != expected_source_sha:
        return ValidationResult("FAIL", "source SHA mismatch")
    if expected_owner_id is not None and receipt["owner_id"] != expected_owner_id:
        return ValidationResult("FAIL", "owner mismatch")
    if expected_session_id is not None and receipt["session_id"] != expected_session_id:
        return ValidationResult("FAIL", "session mismatch")

    if not receipt["runtime_id"] or receipt["runtime_version"] is None:
        return ValidationResult("FAIL", "unknown runtime identity/version")
    if not receipt["deployment_identity"]:
        return ValidationResult("FAIL", "unknown deployment identity")

    invocations = receipt["node_invocations"]
    if not isinstance(invocations, list):
        return ValidationResult("FAIL", "node attribution must be a list")

    node_ids = {item.get("node_id") for item in invocations if isinstance(item, dict)}
    if node_ids != set(NODES):
        return ValidationResult("FAIL", "node attribution is incomplete")

    for item in invocations:
        if not all(item.get(k) for k in (
            "node_id", "invocation_id", "input_hash", "output_hash",
            "evidence_ids", "downstream_consumers"
        )):
            return ValidationResult("FAIL", "node attribution contains incomplete invocation evidence")
        if not item["evidence_ids"]:
            return ValidationResult("FAIL", "node attribution lacks runtime evidence")

    verification = receipt["verification"]
    if not isinstance(verification, dict) or not verification.get("independent"):
        return ValidationResult("FAIL", "independent verification evidence is required")
    if not verification.get("evidence_ids"):
        return ValidationResult("FAIL", "independent verification evidence is required")

    if receipt["status"] == "PROVEN":
        if not receipt["causal_delta"]:
            return ValidationResult("FAIL", "causal delta is required for PROVEN")
    elif receipt["status"] not in {
        "PARTIALLY_PROVEN", "NOT_PROVEN", "FAILED", "BLOCKED", "UNKNOWN", "STALE"
    }:
        return ValidationResult("FAIL", "invalid receipt status")

    return ValidationResult("PASS")


def compare_control_treatment(
    control: dict[str, Any],
    treatment: dict[str, Any],
) -> dict[str, Any]:
    """Return the observed decision/outcome delta only for matched experiments."""
    if control.get("experiment_id") != treatment.get("experiment_id"):
        raise ValueError("control/treatment experiment mismatch")
    if control.get("scenario_hash") != treatment.get("scenario_hash"):
        raise ValueError("control/treatment scenario mismatch")
    if control.get("input_hash") != treatment.get("input_hash"):
        raise ValueError("control/treatment input mismatch")
    if control.get("control_or_treatment") != "control":
        raise ValueError("first receipt must be control")
    if treatment.get("control_or_treatment") != "treatment":
        raise ValueError("second receipt must be treatment")

    return {
        "decision_changed": control.get("decision_after") != treatment.get("decision_after"),
        "outcome_changed": control.get("observed_outcome") != treatment.get("observed_outcome"),
        "action_changed": control.get("action") != treatment.get("action"),
    }


def validate_ablation(full: dict[str, Any], ablated: dict[str, Any], node_id: str) -> ValidationResult:
    if node_id not in NODES:
        return ValidationResult("FAIL", "unknown node")
    if full.get("scenario_hash") != ablated.get("scenario_hash"):
        return ValidationResult("FAIL", "ablation scenario changed")
    if full.get("input_hash") != ablated.get("input_hash"):
        return ValidationResult("FAIL", "ablation input changed")
    full_nodes = {x.get("node_id") for x in full.get("node_invocations", [])}
    ablated_nodes = {x.get("node_id") for x in ablated.get("node_invocations", [])}
    if full_nodes != set(NODES):
        return ValidationResult("FAIL", "full run lacks all nodes")
    if node_id in ablated_nodes:
        return ValidationResult("FAIL", "ablated node still has execution evidence")
    if ablated_nodes != set(NODES) - {node_id}:
        return ValidationResult("FAIL", "ablation changed more than one node")
    return ValidationResult("PASS")
