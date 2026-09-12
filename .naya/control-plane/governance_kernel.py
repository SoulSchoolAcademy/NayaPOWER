#!/usr/bin/env python3
"""NayaPOWER Governance Kernel V1.

Deterministic, model-agnostic control primitives for consequential actions.
This module is intentionally small: it is the constitutional gate, not the
application-specific executor.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = Path(__file__).with_name("GOVERNANCE-KERNEL.json")

SUCCESS_STATES = {
    "PROPOSED", "INVESTIGATING", "READY_FOR_DECISION", "AUTHORIZED",
    "EXECUTING", "EXECUTED", "OBSERVED", "VERIFIED", "ASK", "DEFERRED",
    "REFUSED", "STOPPED", "FAILED", "REQUIRES_REPAIR"
}

REQUIRED_FIELDS = (
    "mission", "actor", "request", "purpose", "authority", "scope",
    "boundaries", "evidence", "uncertainty", "consequence", "reversibility",
    "risk", "alternatives", "value", "required_permission", "decision",
    "execution_plan", "verification_plan", "stop_conditions",
    "receipt_requirements", "learning_output"
)

LEGAL_TRANSITIONS = {
    "PROPOSED": {"INVESTIGATING", "ASK", "DEFERRED", "REFUSED", "STOPPED"},
    "INVESTIGATING": {"READY_FOR_DECISION", "ASK", "DEFERRED", "REFUSED", "STOPPED", "FAILED"},
    "READY_FOR_DECISION": {"AUTHORIZED", "ASK", "DEFERRED", "REFUSED", "STOPPED"},
    "AUTHORIZED": {"EXECUTING", "STOPPED", "REQUIRES_REPAIR"},
    "EXECUTING": {"EXECUTED", "FAILED", "STOPPED", "REQUIRES_REPAIR"},
    "EXECUTED": {"OBSERVED", "FAILED", "STOPPED", "REQUIRES_REPAIR"},
    "OBSERVED": {"VERIFIED", "FAILED", "REQUIRES_REPAIR"},
    "VERIFIED": set(),
    "ASK": set(),
    "DEFERRED": {"INVESTIGATING", "READY_FOR_DECISION"},
    "REFUSED": set(),
    "STOPPED": {"INVESTIGATING", "READY_FOR_DECISION"},
    "FAILED": {"INVESTIGATING", "REQUIRES_REPAIR"},
    "REQUIRES_REPAIR": {"INVESTIGATING", "STOPPED", "DEFERRED"},
}


class GovernanceViolation(ValueError):
    """Fail-closed governance rejection."""


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    tier: str
    governance: str


def _level(value: Any, name: str) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError) as exc:
        raise GovernanceViolation(f"{name} must be an integer 1..5") from exc
    if not 1 <= n <= 5:
        raise GovernanceViolation(f"{name} must be an integer 1..5")
    return n


def assess_risk(uncertainty: Any, consequence: Any, irreversibility: Any, *, prohibited: bool = False) -> RiskAssessment:
    if prohibited:
        return RiskAssessment(score=125, tier="R5", governance="refuse")
    u, c, i = (_level(uncertainty, "uncertainty"), _level(consequence, "consequence"), _level(irreversibility, "irreversibility"))
    score = u * c * i
    if score <= 1:
        tier, governance = "R0", "autonomous"
    elif score <= 8:
        tier, governance = "R1", "lightweight_verification"
    elif score <= 27:
        tier, governance = "R2", "decision_contract"
    elif score <= 64:
        tier, governance = "R3", "explicit_authority_and_strong_evidence"
    else:
        tier, governance = "R4", "human_approval_and_independent_verification"
    return RiskAssessment(score=score, tier=tier, governance=governance)


def validate_decision(decision: Mapping[str, Any]) -> None:
    missing = [key for key in REQUIRED_FIELDS if key not in decision]
    if missing:
        raise GovernanceViolation(f"missing mandatory decision fields: {', '.join(missing)}")
    if not decision.get("actor") or not decision.get("purpose") or not decision.get("request"):
        raise GovernanceViolation("actor, purpose, and request must be non-empty")
    if not isinstance(decision.get("stop_conditions"), (list, tuple)) or not decision["stop_conditions"]:
        raise GovernanceViolation("stop_conditions must be explicit and non-empty")
    if not isinstance(decision.get("verification_plan"), (list, tuple, str)) or not decision["verification_plan"]:
        raise GovernanceViolation("verification_plan is required")


def validate_authority(authority: Mapping[str, Any], *, actor: str, purpose: str, permission: str | None = None) -> None:
    required = ("authority_id", "issuer", "holder", "actor", "purpose", "permissions", "scope", "issued_at", "expires_at", "status")
    missing = [key for key in required if key not in authority]
    if missing:
        raise GovernanceViolation(f"authority missing fields: {', '.join(missing)}")
    if authority.get("status") != "ACTIVE":
        raise GovernanceViolation("authority is not ACTIVE")
    if authority.get("actor") != actor or authority.get("holder") != actor:
        raise GovernanceViolation("authority actor/holder mismatch")
    if authority.get("purpose") != purpose:
        raise GovernanceViolation("authority purpose mismatch")
    if authority.get("revoked_at"):
        raise GovernanceViolation("authority is revoked")
    expires = _parse_time(authority.get("expires_at"))
    if expires <= datetime.now(timezone.utc):
        raise GovernanceViolation("authority is expired")
    if permission is not None and permission not in authority.get("permissions", []):
        raise GovernanceViolation("required permission is not granted")


def _parse_time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise GovernanceViolation("authority timestamp must be timezone-aware ISO-8601")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GovernanceViolation("invalid authority timestamp") from exc
    if parsed.tzinfo is None:
        raise GovernanceViolation("authority timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def transition(current: str, target: str, *, halted: bool = False) -> str:
    if current not in LEGAL_TRANSITIONS or target not in SUCCESS_STATES:
        raise GovernanceViolation("unknown governance state")
    if halted and target not in {"STOPPED", "ASK", "DEFERRED"}:
        raise GovernanceViolation("governance halt blocks continuation")
    if target not in LEGAL_TRANSITIONS[current]:
        raise GovernanceViolation(f"illegal transition: {current} -> {target}")
    return target


@dataclass
class GovernanceKernel:
    halted: bool = False
    halt_reason: str | None = None

    def halt(self, reason: str) -> None:
        if not reason.strip():
            raise GovernanceViolation("halt requires a reason")
        self.halted = True
        self.halt_reason = reason

    def clear_halt(self, *, authorized: bool) -> None:
        if not authorized:
            raise GovernanceViolation("clearing a governance halt requires authorization")
        self.halted = False
        self.halt_reason = None

    def gate(self, decision: Mapping[str, Any], authority: Mapping[str, Any]) -> RiskAssessment:
        validate_decision(decision)
        if self.halted:
            raise GovernanceViolation("governance halt is active")
        validate_authority(
            authority,
            actor=str(decision["actor"]),
            purpose=str(decision["purpose"]),
            permission=str(decision["required_permission"]),
        )
        risk = assess_risk(
            decision["uncertainty"], decision["consequence"], decision["reversibility"],
            prohibited=bool(decision["risk"].get("prohibited", False)) if isinstance(decision["risk"], Mapping) else False,
        )
        if risk.tier == "R5":
            raise GovernanceViolation("R5 prohibited action")
        if decision.get("decision") == "REFUSE":
            raise GovernanceViolation("decision explicitly refuses execution")
        return risk


def receipt(decision: Mapping[str, Any], *, state: str, result: Any = None, observation: Any = None,
            verification: Any = None, failure: Any = None, repair: Any = None,
            next_action: str = "") -> dict[str, Any]:
    body: dict[str, Any] = {
        "receipt_id": f"receipt:{decision.get('decision_id', 'unknown')}",
        "decision_id": decision.get("decision_id"),
        "actor": decision.get("actor"),
        "authority_id": (decision.get("authority") or {}).get("authority_id") if isinstance(decision.get("authority"), Mapping) else decision.get("authority"),
        "request": decision.get("request"),
        "decision": decision.get("decision"),
        "state": state,
        "result": result,
        "observation": observation,
        "verification": verification,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uncertainty": decision.get("uncertainty"),
        "failure": failure,
        "repair": repair,
        "next_action": next_action,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
    body["integrity_hash"] = hashlib.sha256(canonical).hexdigest()
    return body


def self_test() -> dict[str, Any]:
    assert assess_risk(1, 1, 1).tier == "R0"
    assert assess_risk(5, 5, 5).tier == "R4"
    assert assess_risk(1, 1, 1, prohibited=True).tier == "R5"
    assert transition("EXECUTED", "OBSERVED") == "OBSERVED"
    try:
        transition("EXECUTED", "VERIFIED")
    except GovernanceViolation:
        pass
    else:
        raise AssertionError("EXECUTED -> VERIFIED bypass accepted")
    kernel = GovernanceKernel()
    kernel.halt("test stop")
    try:
        transition("AUTHORIZED", "EXECUTING", halted=kernel.halted)
    except GovernanceViolation:
        pass
    else:
        raise AssertionError("STOP did not dominate continuation")
    return {"status": "GREEN", "kernel": "NAYAPOWER-GOVERNANCE-KERNEL-V1", "tests": 6}


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2))
