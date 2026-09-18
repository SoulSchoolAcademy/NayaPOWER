#!/usr/bin/env python3
"""Narrow boundary from completed execution results to canonical evidence records.

This module does not execute work, verify claims, or store events. It only
constructs and validates the existing naya-power-evidence/v1 record required by
.evidence/evidence_runtime.py. Verification remains authoritative there.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

EVIDENCE_SCHEMA = "naya-power-evidence/v1"
RESULTS = {"PASS", "FAIL", "PARTIAL", "UNKNOWN"}
FORBIDDEN_METHODS = {"model_assertion", "memory_assertion", "user_assertion", "retrieved_content"}
REQUIRED = {"schema", "evidence_id", "claim_id", "observed_at", "method", "command", "observed_output", "result", "commit_sha", "environment", "source"}


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def _parse_time(value: str) -> datetime:
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def validate_execution_result(result: dict[str, Any]) -> list[str]:
    """Validate the observed execution facts needed before evidence exists."""
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["execution result must be an object"]
    if str(result.get("execution_state", "")).upper() != "COMPLETED":
        errors.append("execution result must have execution_state=COMPLETED")
    if not _nonempty(result.get("execution_id")):
        errors.append("execution result requires execution_id")
    if not _nonempty(result.get("action")):
        errors.append("execution result requires action")
    if not _nonempty(result.get("observed_output")):
        errors.append("execution result requires observed_output")
    if not _nonempty(result.get("result")):
        errors.append("execution result requires result")
    elif str(result["result"]).upper() not in RESULTS:
        errors.append("execution result has invalid result")
    if not _nonempty(result.get("commit_sha")):
        errors.append("execution result requires commit_sha")
    return errors


def build_evidence(execution: dict[str, Any], *, evidence_id: str, claim_id: str, method: str, command: str, environment: str, source: str, observed_at: str | None = None) -> dict[str, Any]:
    """Build evidence from completed, observed execution; never marks a claim verified."""
    errors = validate_execution_result(execution)
    if errors:
        raise ValueError("execution result rejected: " + "; ".join(errors))
    if not _nonempty(evidence_id) or not _nonempty(claim_id) or not _nonempty(method) or not _nonempty(command) or not _nonempty(environment) or not _nonempty(source):
        raise ValueError("evidence identity, provenance, command, method, and environment are required")
    if method in FORBIDDEN_METHODS:
        raise ValueError(f"evidence method {method} cannot establish evidence")
    stamp = observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    _parse_time(stamp)
    return {
        "schema": EVIDENCE_SCHEMA,
        "evidence_id": evidence_id,
        "claim_id": claim_id,
        "observed_at": stamp,
        "method": method,
        "command": command,
        "observed_output": execution["observed_output"],
        "result": str(execution["result"]).upper(),
        "commit_sha": execution["commit_sha"],
        "environment": environment,
        "source": source,
        "execution_id": execution["execution_id"],
        "action": execution["action"],
    }


def validate_evidence_boundary(evidence: dict[str, Any]) -> list[str]:
    """Validate boundary output without performing claim verification."""
    if not isinstance(evidence, dict):
        return ["evidence must be an object"]
    errors = [f"missing {sorted(REQUIRED - set(evidence))}"] if REQUIRED - set(evidence) else []
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        errors.append("invalid evidence schema")
    if evidence.get("result") not in RESULTS:
        errors.append("invalid evidence result")
    if evidence.get("method") in FORBIDDEN_METHODS:
        errors.append("forbidden evidence method")
    if not _nonempty(evidence.get("execution_id")):
        errors.append("evidence must identify execution_id")
    if not _nonempty(evidence.get("action")):
        errors.append("evidence must identify action")
    return errors
