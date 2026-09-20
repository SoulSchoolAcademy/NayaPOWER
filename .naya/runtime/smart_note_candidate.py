#!/usr/bin/env python3
"""Small, non-persistent boundary from verified execution evidence to a Smart Note candidate.

This module deliberately does not write memory, create Note Events, promote
authority, or alter CCT. It only evaluates whether an execution/evidence result
contains enough durable learning to be represented as a candidate Smart Note.
The existing canonical Note Event store remains the only memory/event authority.
"""
from __future__ import annotations

from typing import Any

CANONICAL_EVIDENCE_SCHEMA = "naya-power-evidence/v1"
ALLOWED_TYPES = {
    "decision", "lesson", "discovery", "correction", "architecture",
    "preference", "milestone", "failure", "fact", "strategy", "insight",
}
REQUIRED_LEARNING = ("what_mattered", "what_was_learned", "future_action")


class SmartNoteCandidateRejected(ValueError):
    """Raised when an execution result does not contain durable learning."""


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _source(evidence: dict[str, Any]) -> dict[str, str]:
    fields = ("execution_id", "evidence_id", "commit_sha")
    missing = [field for field in fields if not _text(evidence.get(field))]
    if missing:
        raise SmartNoteCandidateRejected("evidence missing provenance: " + ", ".join(missing))
    return {field: _text(evidence[field]) for field in fields}


def build_candidate(
    evidence: dict[str, Any],
    learning: dict[str, Any],
    *,
    note_type: str,
) -> dict[str, Any]:
    """Represent durable learning as an unpromoted Smart Note candidate.

    The function is intentionally pure: callers receive a candidate object;
    no note/event file is written and no canonical authority is changed.
    """
    if not isinstance(evidence, dict) or evidence.get("schema") != CANONICAL_EVIDENCE_SCHEMA:
        raise SmartNoteCandidateRejected("canonical execution evidence is required")
    if not isinstance(learning, dict):
        raise SmartNoteCandidateRejected("learning must be an object")
    if note_type not in ALLOWED_TYPES:
        raise SmartNoteCandidateRejected("invalid Smart Note candidate type")

    source = _source(evidence)
    values = {field: _text(learning.get(field)) for field in REQUIRED_LEARNING}
    if any(not value for value in values.values()):
        raise SmartNoteCandidateRejected(
            "durable learning requires what_mattered, what_was_learned, and future_action"
        )

    transcript = _text(evidence.get("transcript"))
    combined = " ".join(values.values())
    if transcript and combined == transcript:
        raise SmartNoteCandidateRejected("raw transcript cannot be promoted as durable learning")

    return {
        "promotion_state": "CANDIDATE",
        "type": note_type,
        "summary": values["what_mattered"],
        "what_we_learned": [values["what_was_learned"]],
        "why_it_matters": values["what_mattered"],
        "next_best_action": values["future_action"],
        "source": source,
    }
