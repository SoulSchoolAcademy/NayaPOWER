#!/usr/bin/env python3
"""Narrow CSI boundary: validated durable learning -> future-execution improvement.

This module does not store events/notes, promote intelligence, verify claims, or
rewrite law. It packages an already validated learning item into a measurable
future-execution change that a successor can consume.
"""
from __future__ import annotations
from typing import Any

VALID_EVIDENCE = {"VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"}
VALID_PROMOTION = {"VERIFIED", "CANONICAL"}
REQUIRED = {"event_id", "lesson", "source", "evidence_state", "promotion_status"}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def build_compounding_change(intelligence: dict[str, Any], *, baseline: str, expected_improvement: str, measurement: str) -> dict[str, Any]:
    """Package validated learning as a measurable future-execution change."""
    if not isinstance(intelligence, dict):
        raise ValueError("intelligence must be an object")
    missing = REQUIRED - set(intelligence)
    if missing:
        raise ValueError(f"missing intelligence fields: {sorted(missing)}")
    if not _text(intelligence.get("event_id")) or not _text(intelligence.get("lesson")):
        raise ValueError("event_id and lesson are required")
    if intelligence.get("evidence_state") not in VALID_EVIDENCE:
        raise ValueError("learning is not independently validated")
    if intelligence.get("promotion_status") not in VALID_PROMOTION:
        raise ValueError("learning is not durably promoted")
    source = intelligence.get("source")
    if not isinstance(source, list) or not source or any(not _text(x) for x in source):
        raise ValueError("provenance source is required")
    for name, value in (("baseline", baseline), ("expected_improvement", expected_improvement), ("measurement", measurement)):
        if not _text(value):
            raise ValueError(f"{name} is required")
    return {
        "kind": "csi-compounding-change/v1",
        "source_event_id": intelligence["event_id"],
        "lesson": intelligence["lesson"].strip(),
        "provenance": list(source),
        "baseline": baseline.strip(),
        "expected_improvement": expected_improvement.strip(),
        "measurement": measurement.strip(),
        "state": "PROPOSED_FUTURE_EXECUTION_CHANGE",
        "authority": "CSI_BOUNDARY_ONLY",
    }
