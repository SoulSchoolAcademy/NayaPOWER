#!/usr/bin/env python3
"""Fail-closed capacity admission for existing PARALLEL-EXECUTION-V1.

This is a capacity-only preflight, not an alternate scheduler, LAW grant,
billing operation or dispatcher. CAPACITY_READY never means AUTHORIZED or
EXECUTED. A caller must authenticate evidence and still apply LAW.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Any

MAX_AGE_SECONDS = 300


def _finite_nonnegative(value: Any) -> bool:
    return (isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0)


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if instant.tzinfo is None or instant.utcoffset() is None:
        return None
    return instant.astimezone(timezone.utc)


def _verdict(decision: str, reasons: list[str], ref: str | None,
             width: int = 0) -> dict[str, Any]:
    return {
        "decision": decision, "reasons": reasons,
        "evidence_refs": [ref] if ref else [],
        "max_ready_tasks": width,
        "dispatch_performed": False,
        "law_authorized": False,
    }


def classify_brainbase_failure_event(event: dict[str, Any], *,
                                      observed_at: str,
                                      evidence_ref: str) -> dict[str, Any]:
    """Normalize a supplied provider refusal, never invent positive capacity.

    The caller authenticates the source. An event's timestamp must reflect
    the actual observation, not when a stale record was retrieved.
    """
    details = event.get("details") if isinstance(event, dict) else None
    if isinstance(details, str):
        try:
            details = json.loads(details)
        except (ValueError, TypeError):
            details = None
    if not isinstance(details, dict):
        details = {}
    ent = details.get("entitlement_error")
    if not isinstance(ent, dict):
        ent = {}
    is_refusal = (
        isinstance(event, dict) and event.get("type") == "idle"
        and details.get("http_status") == 402
        and ent.get("error") == "CREDITS_EXHAUSTED"
        and _finite_nonnegative(ent.get("allocated"))
        and _finite_nonnegative(ent.get("used"))
    )
    return {
        "provider": "brainbase", "evidence_ref": evidence_ref,
        "observed_at": observed_at, "measured": is_refusal,
        "unit": "credits",
        "allocated": ent.get("allocated") if is_refusal else None,
        "used": ent.get("used") if is_refusal else None,
        "error_code": "CREDITS_EXHAUSTED" if is_refusal else "UNKNOWN",
    }


def assess_capacity(snapshot: dict[str, Any], request: dict[str, Any], *,
                    now: datetime | None = None,
                    max_age_seconds: int = MAX_AGE_SECONDS) -> dict[str, Any]:
    """Fail closed unless fresh measured evidence supports the cost.

    Snapshot: provider, evidence_ref, observed_at, measured, unit,
    allocated, used, optional error_code. Request: unit, per_task_cost,
    cost_measured, ready_tasks. This function never actually dispatches.
    """
    if not isinstance(snapshot, dict) or not isinstance(request, dict):
        return _verdict("BLOCKED_EVIDENCE", ["snapshot/request must be objects"], None)
    ref = snapshot.get("evidence_ref")
    ref = ref.strip() if isinstance(ref, str) and ref.strip() else None
    provider = snapshot.get("provider")
    if not ref or not isinstance(provider, str) or not provider.strip():
        return _verdict("BLOCKED_EVIDENCE", ["provider and evidence_ref required"], ref)
    observed = _parse_utc(snapshot.get("observed_at"))
    if observed is None:
        return _verdict("BLOCKED_EVIDENCE", ["aware observed_at required"], ref)
    now = now or datetime.now(timezone.utc)
    if (not isinstance(now, datetime) or now.tzinfo is None
        or now.utcoffset() is None or not isinstance(max_age_seconds, int)
        or isinstance(max_age_seconds, bool) or max_age_seconds < 0):
        return _verdict("BLOCKED_EVIDENCE", ["invalid clock or freshness policy"], ref)
    age = (now.astimezone(timezone.utc) - observed).total_seconds()
    if age < 0 or age > max_age_seconds:
        return _verdict("BLOCKED_EVIDENCE", ["capacity evidence future-dated or stale"], ref)
    if snapshot.get("measured") is not True:
        return _verdict("BLOCKED_EVIDENCE", ["provider capacity not measured"], ref)
    if (not isinstance(snapshot.get("unit"), str)
        or snapshot.get("unit") != request.get("unit")):
        return _verdict("BLOCKED_EVIDENCE", ["capacity/cost unit mismatch"], ref)
    allocated, used = snapshot.get("allocated"), snapshot.get("used")
    if (not _finite_nonnegative(allocated) or not _finite_nonnegative(used)
        or used > allocated):
        return _verdict("BLOCKED_EVIDENCE", ["invalid provider counters"], ref)
    if snapshot.get("error_code") == "CREDITS_EXHAUSTED":
        return _verdict("BLOCKED_RESOURCE", ["credits exhausted; do not retry this lane"], ref)
    if snapshot.get("error_code") not in (None, ""):
        return _verdict("BLOCKED_EVIDENCE", ["unclassified provider error"], ref)
    cost, ready = request.get("per_task_cost"), request.get("ready_tasks")
    if (request.get("cost_measured") is not True
        or not _finite_nonnegative(cost) or cost <= 0
        or not isinstance(ready, int) or isinstance(ready, bool) or ready < 1):
        return _verdict("BLOCKED_EVIDENCE",
                        ["measured positive task cost and ready count required"], ref)
    available = allocated - used
    if available < cost:
        return _verdict("BLOCKED_RESOURCE", ["insufficient measured capacity"], ref)
    return _verdict(
        "CAPACITY_READY",
        ["capacity only: separately verify LAW, dependencies and execution"], ref,
        min(ready, int(available // cost)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capacity preflight; never dispatches or authorizes work")
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--now", help="Offset-aware time for exact replay")
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        request = json.loads(args.request.read_text(encoding="utf-8"))
        now = _parse_utc(args.now) if args.now else None
        if args.now and now is None:
            raise ValueError("invalid replay timestamp")
        result = assess_capacity(snapshot, request, now=now)
    except (OSError, ValueError, TypeError) as exc:
        result = _verdict("BLOCKED_EVIDENCE",
                          [f"invalid input: {type(exc).__name__}"], None)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["decision"] == "CAPACITY_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
