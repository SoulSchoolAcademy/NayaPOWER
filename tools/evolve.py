#!/usr/bin/env python3
"""EVOLVE successor package (Phase 4 / GAP 6): the governed handoff package.

``SelfNode.successor_packet()`` carries raw continuity; EVOLVE wraps it into a
minimal, hash-sealed successor handoff that a cold successor can verify before
trusting anything inside it.

Fail-closed rules:
- build: any missing/empty required input raises ValueError, and every
  ``current_truth`` entry must already be at or above ACTIVE.
- verify: all REQUIRED_FIELDS present, package_hash recomputes exactly, and
  every ``current_truth`` entry still carries truth_state in
  {ACTIVE, LEARNED, RATIFIED}. Tampering with any field breaks the hash.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

SCHEMA = "naya.evolve.successor-package.v1"

REQUIRED_FIELDS = [
    "schema",
    "identity_context",
    "mission",
    "current_truth",
    "authority_boundary",
    "material_blockers",
    "next_action",
    "package_hash",
    "built_at",
    "built_by",
]

# A successor may only inherit learnings that are already live knowledge.
EVOLVE_TRUTH_STATES = frozenset({"ACTIVE", "LEARNED", "RATIFIED"})


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def _body_hash(package: dict[str, Any]) -> str:
    body = {k: v for k, v in package.items() if k != "package_hash"}
    return hashlib.sha256(_canonical(body)).hexdigest()


def _freeze(value: Any) -> Any:
    """Deep-copy JSON-safe values so later caller mutation cannot silently
    invalidate a sealed package."""
    return json.loads(json.dumps(value))


def _require_nonempty(name: str, value: Any) -> None:
    if value is None or (hasattr(value, "__len__") and len(value) == 0):
        raise ValueError(f"evolve: required input missing or empty: {name}")


def build_successor_package(
    identity_context,
    mission,
    current_truth,
    authority_boundary,
    material_blockers,
    next_action,
    built_by: str = "evolve",
) -> dict:
    """Assemble the minimal viable successor handoff.

    current_truth: list of ACTIVE+ learnings (each {id, truth_state}).
    material_blockers: list (may be empty — "no material blockers" is a
    meaningful claim); must not be None.
    Raises ValueError on missing/empty required inputs (fail closed at build
    time). Returns the package dict with sha256 package_hash over canonical
    JSON of all fields except package_hash itself.
    """
    _require_nonempty("identity_context", identity_context)
    _require_nonempty("mission", mission)
    _require_nonempty("current_truth", current_truth)
    _require_nonempty("authority_boundary", authority_boundary)
    if material_blockers is None:
        raise ValueError("evolve: required input missing or empty: material_blockers")
    _require_nonempty("next_action", next_action)
    _require_nonempty("built_by", built_by)

    frozen_truth = [_freeze(e) for e in current_truth]
    for entry in frozen_truth:
        truth_state = entry.get("truth_state") if isinstance(entry, dict) else None
        if truth_state not in EVOLVE_TRUTH_STATES:
            raise ValueError(
                f"evolve: current_truth entry below ACTIVE cannot seed a successor: {entry!r}"
            )

    package = {
        "schema": SCHEMA,
        "identity_context": _freeze(identity_context),
        "mission": _freeze(mission),
        "current_truth": frozen_truth,
        "authority_boundary": _freeze(authority_boundary),
        "material_blockers": _freeze(material_blockers),
        "next_action": _freeze(next_action),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "built_by": built_by,
    }
    package["package_hash"] = _body_hash(package)
    return package


def verify_successor_package(package: dict) -> dict:
    """Verify a successor package.

    Returns {"valid": True} or {"valid": False, "reasons": [...]}.
    Checks: all REQUIRED_FIELDS present; package_hash matches recomputation;
    current_truth entries all have truth_state in {ACTIVE, LEARNED, RATIFIED}.
    Tampering with any field -> hash mismatch -> invalid.
    """
    reasons: list[str] = []
    if not isinstance(package, dict):
        return {"valid": False, "reasons": ["package_not_a_dict"]}

    for field_name in REQUIRED_FIELDS:
        if field_name not in package:
            reasons.append(f"missing_field:{field_name}")

    if "package_hash" in package:
        expected = _body_hash(package)
        if package.get("package_hash") != expected:
            reasons.append("package_hash_mismatch")

    truth = package.get("current_truth")
    if "current_truth" in package:
        if not isinstance(truth, list):
            reasons.append("current_truth_not_a_list")
        else:
            for entry in truth:
                truth_state = entry.get("truth_state") if isinstance(entry, dict) else None
                entry_id = entry.get("id") if isinstance(entry, dict) else None
                if truth_state not in EVOLVE_TRUTH_STATES:
                    reasons.append(f"current_truth_below_active:{entry_id or '?'}")

    if reasons:
        return {"valid": False, "reasons": reasons}
    return {"valid": True}
