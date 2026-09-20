#!/usr/bin/env python3
"""Dependency-free Team Naya claim/lease contract.

Claims coordinate repository work; they do not grant authority to overwrite
canonical truth. The contract uses optimistic base-commit binding so a stale
claim cannot safely authorize a write against a changed repository state.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

ACTIVE = {"CLAIMED", "IN_PROGRESS", "VERIFYING"}
TERMINAL = {"DONE", "BLOCKED", "SUPERSEDED", "ABANDONED"}
STATES = ACTIVE | TERMINAL | {"QUEUED"}


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@dataclass(frozen=True)
class Claim:
    work_id: str
    owner_naya: str
    task_id: str
    scope: str
    affected_files: tuple[str, ...]
    base_commit: str
    acceptance: str
    status: str
    started_at: str
    expires_at: str
    last_verified: str | None = None
    result_commit: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["affected_files"] = list(self.affected_files)
        return value


def validate_claim(claim: Claim, *, now: str | None = None) -> tuple[bool, str]:
    if not claim.work_id or not claim.owner_naya or not claim.task_id:
        return False, "identity fields are required"
    if not claim.scope or not claim.affected_files:
        return False, "scope and affected_files are required"
    if not claim.base_commit or not claim.acceptance:
        return False, "base_commit and acceptance are required"
    if claim.status not in STATES:
        return False, "invalid claim status"
    current = _utc(now) if now else datetime.now(timezone.utc)
    if _utc(claim.expires_at) <= _utc(claim.started_at):
        return False, "expiry must be after start"
    if claim.status in ACTIVE and _utc(claim.expires_at) <= current:
        return False, "active claim is expired"
    return True, "valid"


def conflicts(candidate: Claim, existing: list[Claim], *, now: str | None = None) -> list[str]:
    """Return active claims overlapping the candidate scope/files."""
    result: list[str] = []
    candidate_ok, _ = validate_claim(candidate, now=now)
    if not candidate_ok:
        return result
    candidate_files = set(candidate.affected_files)
    for item in existing:
        ok, _ = validate_claim(item, now=now)
        if not ok or item.status not in ACTIVE or item.work_id == candidate.work_id:
            continue
        if item.scope == candidate.scope or candidate_files.intersection(item.affected_files):
            result.append(item.work_id)
    return sorted(result)


def authorize_write(claim: Claim, *, current_commit: str, existing: list[Claim], now: str | None = None) -> tuple[bool, str]:
    valid, reason = validate_claim(claim, now=now)
    if not valid:
        return False, reason
    if claim.status not in {"CLAIMED", "IN_PROGRESS", "VERIFYING"}:
        return False, "claim is not writable"
    if claim.base_commit != current_commit:
        return False, "stale base commit"
    overlap = conflicts(claim, existing, now=now)
    if overlap:
        return False, "conflicting active claims: " + ", ".join(overlap)
    return True, "write permitted"
