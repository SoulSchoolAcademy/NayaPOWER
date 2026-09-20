#!/usr/bin/env python3
"""Universal host-agent boundary for Naya Power.

This module is deliberately narrow. It adapts an external AI/agent host into a
stable Naya Power envelope without becoming an authority for mission, priority,
execution, verification, memory, promotion, or CSI.

It is transport/contract normalization only:
  host agent -> Naya Power envelope -> existing canonical authorities

No persistence, network calls, tool execution, memory writes, or authority
promotion occur here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PROTOCOL = "naya-power-agent-interface/v1"
REQUIRED = {"agent_id", "host", "session_id", "request_id", "input"}


class AgentInterfaceError(ValueError):
    """Raised when a host-agent envelope cannot be safely normalized."""


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AgentInterfaceError(f"{field} is required")
    return value.strip()


def _optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise AgentInterfaceError(f"{field} must be a non-empty string when provided")
    return value.strip()


def _string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise AgentInterfaceError(f"{field} must be a list of non-empty strings")
    return [item.strip() for item in value]


@dataclass(frozen=True)
class NayaAgentEnvelope:
    agent_id: str
    host: str
    session_id: str
    request_id: str
    input: str
    model: str | None
    mission_ref: str | None
    source_refs: tuple[str, ...]
    capabilities: tuple[str, ...]
    constraints: tuple[str, ...]

    def to_kernel_input(self) -> dict[str, Any]:
        """Return a stable handoff to existing Naya Power authorities."""
        return {
            "schema": PROTOCOL,
            "agent": {
                "id": self.agent_id,
                "host": self.host,
                "model": self.model,
                "session_id": self.session_id,
            },
            "request_id": self.request_id,
            "request": self.input,
            "mission_ref": self.mission_ref,
            "source_refs": list(self.source_refs),
            "capabilities": list(self.capabilities),
            "constraints": list(self.constraints),
            "authority": "transport boundary only; existing canonical authorities remain authoritative",
            "persistence": "NONE",
        }


def normalize_agent_input(raw: dict[str, Any]) -> NayaAgentEnvelope:
    """Normalize a host-agent request without changing its meaning."""
    if not isinstance(raw, dict):
        raise AgentInterfaceError("agent input must be an object")
    missing = REQUIRED - set(raw)
    if missing:
        raise AgentInterfaceError(f"missing required fields: {sorted(missing)}")
    protocol = raw.get("protocol", PROTOCOL)
    if protocol != PROTOCOL:
        raise AgentInterfaceError(f"unsupported protocol: {protocol!r}")
    return NayaAgentEnvelope(
        agent_id=_required_text(raw.get("agent_id"), "agent_id"),
        host=_required_text(raw.get("host"), "host"),
        session_id=_required_text(raw.get("session_id"), "session_id"),
        request_id=_required_text(raw.get("request_id"), "request_id"),
        input=_required_text(raw.get("input"), "input"),
        model=_optional_text(raw.get("model"), "model"),
        mission_ref=_optional_text(raw.get("mission_ref"), "mission_ref"),
        source_refs=tuple(_string_list(raw.get("source_refs"), "source_refs")),
        capabilities=tuple(_string_list(raw.get("capabilities"), "capabilities")),
        constraints=tuple(_string_list(raw.get("constraints"), "constraints")),
    )


def validate_agent_result(result: dict[str, Any]) -> dict[str, Any]:
    """Validate a host response envelope without declaring work successful."""
    if not isinstance(result, dict):
        raise AgentInterfaceError("agent result must be an object")
    for field in ("agent_id", "session_id", "request_id"):
        _required_text(result.get(field), field)
    status = result.get("status")
    if status not in {"ACCEPTED", "COMPLETED", "FAILED", "UNKNOWN"}:
        raise AgentInterfaceError("status must be ACCEPTED, COMPLETED, FAILED, or UNKNOWN")
    evidence_refs = _string_list(result.get("evidence_refs"), "evidence_refs")
    return {
        "schema": PROTOCOL,
        "agent_id": result["agent_id"].strip(),
        "session_id": result["session_id"].strip(),
        "request_id": result["request_id"].strip(),
        "status": status,
        "output": result.get("output"),
        "evidence_refs": evidence_refs,
        "authority": "result transport only; verification authority remains external",
    }
