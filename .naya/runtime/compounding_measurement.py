#!/usr/bin/env python3
"""V1 canonical compounding measurement attachment for verified executions.

This module does not create a second event/state system. It builds a measurement
object that is embedded in the existing canonical Activity event.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

SCHEMA = "naya-power-compounding-measurement/v1"
STATUS = "VERIFIED_CAPTURED"


def _require(value: Any, name: str) -> None:
    if value in (None, "", [], {}):
        raise ValueError(f"compounding measurement requires {name}")


def _wall_time_ms(history: list[dict[str, Any]]) -> Optional[int]:
    claimed = next((x.get("at") for x in history if x.get("to") == "CLAIMED"), None)
    verified = next((x.get("at") for x in reversed(history) if x.get("to") == "VERIFIED"), None)
    if not claimed or not verified:
        return None
    try:
        start = datetime.fromisoformat(str(claimed).replace("Z", "+00:00"))
        end = datetime.fromisoformat(str(verified).replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0, int((end - start).total_seconds() * 1000))


def build_compounding_measurement(
    *,
    event: dict[str, Any],
    execution: dict[str, Any],
    evidence: list[str],
    history: Optional[list[dict[str, Any]]] = None,
    resource_usage: Optional[dict[str, Any]] = None,
    knowledge_reuse: Optional[dict[str, Any]] = None,
    new_learning: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build the first measurement attached to an already-verified Activity event.

    Only observed/provided telemetry is recorded. Missing future/downstream
    evidence is explicitly marked unobserved; nothing is inferred as saved or
    compounded.
    """
    event_id = event.get("event_id")
    action_id = execution.get("action_id")
    run_id = execution.get("run_id")
    _require(event_id, "canonical Activity event_id")
    _require(action_id, "action_id")
    _require(run_id, "run_id")
    _require(evidence, "verification evidence")

    usage = dict(resource_usage or {})
    if "wall_time_ms" not in usage:
        measured = _wall_time_ms(history or [])
        if measured is not None:
            usage["wall_time_ms"] = measured

    state_change_id = f"VSC-{event_id}"
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "measurement_id": f"CM-{event_id}",
        "recorded_at": event.get("effective_at"),
        "request_id": execution.get("claim_id"),
        "action_id": action_id,
        "run_id": run_id,
        "activity_event_id": event_id,
        "provenance_refs": list(evidence),
        "resource_usage": usage,
        "verified_state_change": {
            "state_change_id": state_change_id,
            "before_state_ref": f"execution:{run_id}:OBSERVED",
            "after_state_ref": event_id,
            "change_type": "governed_execution_verified",
            "verification_status": "VERIFIED",
            "evidence_refs": list(evidence),
        },
        "knowledge_reuse": knowledge_reuse or {
            "reused": False,
            "knowledge_refs": [],
            "applicability_basis": None,
            "retrieval_cost": None,
            "estimated_rederivation_cost": None,
            "avoided_resource_units": None,
            "reuse_verification": "NOT_OBSERVED",
        },
        "new_learning": new_learning or {
            "created": False,
            "learning_ref": None,
            "distillation_ref": None,
            "provenance_refs": list(evidence),
            "verification_receipt_ref": None,
            "retention_status": "NOT_CREATED",
        },
        "downstream_compounding": {
            "observed": False,
            "later_action_ref": None,
            "learning_application_ref": None,
            "baseline_measurement_ref": None,
            "comparison_measurement_ref": None,
            "deltas": {},
            "improvement_verified": False,
        },
        "false_economy_check": {
            "performed": False,
            "quality_preserved_or_improved": None,
            "provenance_preserved": True,
            "rework_not_increased": None,
            "verification_passed": True,
            "status": "DEFERRED_UNTIL_COMPARATIVE_TELEMETRY",
        },
        "promotion": {
            "stored": True,
            "retrieved": False,
            "applied": False,
            "verified": True,
            "compounded": False,
        },
    }


__all__ = ["SCHEMA", "STATUS", "build_compounding_measurement"]
