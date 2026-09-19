#!/usr/bin/env python3
"""Read-only adapter from existing evidence records to NAYANET_SELF_PROOF_V1.

The collector observes; evaluate_self_proof judges. This module never writes,
executes actions, verifies claims, or creates Activity/canonical events.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from self_proof import (
    FAIL,
    NOT_VERIFIED,
    PASS,
    REQUIRED_CHECKS,
    evaluate_self_proof,
)

FORBIDDEN_METHODS = {
    "model_assertion",
    "memory_assertion",
    "user_assertion",
    "retrieved_content",
}


def _evidence_values(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item).strip())
    return ()


def _surface(record: Mapping[str, Any]) -> str | None:
    value = record.get("surface") or record.get("proof_surface")
    return str(value) if value in REQUIRED_CHECKS else None


def _status(record: Mapping[str, Any]) -> str:
    value = str(record.get("status") or record.get("result") or "").upper()
    if value == PASS:
        return PASS
    if value == FAIL:
        return FAIL
    return NOT_VERIFIED


def _usable(record: Mapping[str, Any], observed_commit: str) -> bool:
    if _surface(record) is None:
        return False
    if not observed_commit or str(record.get("commit_sha", "")) != observed_commit:
        return False
    method = str(record.get("method", "")).strip()
    if method in FORBIDDEN_METHODS:
        return False
    return bool(_evidence_values(record.get("evidence") or record.get("evidence_ids")))


def collect_from_records(
    records: Iterable[Mapping[str, Any]], *, observed_commit: str
) -> dict[str, Any]:
    """Normalize existing evidence records without adding new truth."""
    evidence: dict[str, dict[str, Any]] = {}
    accepted: list[str] = []
    rejected: list[str] = []

    for index, record in enumerate(records):
        record_id = str(record.get("evidence_id") or record.get("id") or f"record-{index}")
        surface = _surface(record)
        if not _usable(record, observed_commit):
            rejected.append(record_id)
            continue
        values = _evidence_values(record.get("evidence") or record.get("evidence_ids"))
        evidence[surface] = {
            "status": _status(record),
            "evidence": values,
            "detail": f"collected from existing evidence record {record_id}",
        }
        accepted.append(record_id)

    proof = evaluate_self_proof(evidence)
    return {
        "contract": proof["contract"],
        "observed_commit": observed_commit,
        "accepted_records": accepted,
        "rejected_records": rejected,
        "evidence": evidence,
        "proof": proof,
        "read_only": True,
        "persistence": "none",
        "activity_changes": False,
    }


def collect_repository(root: Path, *, observed_commit: str) -> dict[str, Any]:
    """Read .naya/evidence/records only; never creates or updates files."""
    records_root = Path(root) / ".naya" / "evidence" / "records"
    records: list[Mapping[str, Any]] = []
    scanned: list[str] = []
    if records_root.exists():
        for path in sorted(records_root.rglob("*.json")):
            scanned.append(str(path.relative_to(root)))
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(value, Mapping):
                records.append(value)

    result = collect_from_records(records, observed_commit=observed_commit)
    result["records_root"] = str(records_root.relative_to(root))
    result["scanned_files"] = scanned
    result["record_count"] = len(records)
    return result


__all__ = ["collect_from_records", "collect_repository"]
