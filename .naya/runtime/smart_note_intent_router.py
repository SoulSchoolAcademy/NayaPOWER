#!/usr/bin/env python3
"""Deterministic conversational intent boundary for canonical Smart Note capture.

This module is intentionally narrow. It does not persist memory, allocate an IB,
or create a Smart Link. It converts an unambiguous human capture request into
the one canonical operation the execution layer MUST perform.

The purpose is to prevent the failure mode where Naya explains the Smart Note
system instead of executing the requested capture.
"""
from __future__ import annotations

import re
from typing import Any

CAPTURE_PATTERNS = (
    re.compile(r"\bsmart\s+note\s+this\b", re.I),
    re.compile(r"\bmake\s+(?:this|that)\s+(?:a\s+)?smart\s+note\b", re.I),
    re.compile(r"\bcapture\s+(?:this|that)\s+(?:as\s+)?a?\s*smart\s+note\b", re.I),
    re.compile(r"\bsave\s+(?:this|that)\s+(?:as\s+)?a?\s*smart\s+note\b", re.I),
    re.compile(r"\bturn\s+(?:this|that)\s+into\s+(?:a\s+)?smart\s+note\b", re.I),
)

QUESTION_OR_LOOKUP_PATTERNS = (
    re.compile(r"^\s*what\s+is\s+a?\s*smart\s+note\b", re.I),
    re.compile(r"^\s*(?:show|find|where\s+is)\b.*\bsmart\s+note\b", re.I),
    re.compile(r"^\s*where\s+is\s+(?:the\s+)?smart\s+link\b", re.I),
)

REQUIRED_EVIDENCE = [
    "receiver_persistence",
    "intelligent_block_id",
    "repository_projection",
    "verified_smart_link",
]


def _normalize(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()


def resolve_smart_note_intent(text: str) -> dict[str, Any]:
    """Resolve a human request without inventing ambiguity or authority."""
    normalized = _normalize(text)
    if not normalized:
        return {
            "intent": "UNKNOWN",
            "operation": "NONE",
            "requires_clarification": True,
            "reason": "empty input",
        }

    if any(pattern.search(normalized) for pattern in QUESTION_OR_LOOKUP_PATTERNS):
        return {
            "intent": "SMART_NOTE_QUERY",
            "operation": "NONE",
            "requires_clarification": False,
        }

    if any(pattern.search(normalized) for pattern in CAPTURE_PATTERNS):
        return {
            "intent": "CANONICAL_SMART_NOTE_CAPTURE",
            "operation": "CREATE",
            "canonical_receiver": "v7-smart-note-canonical",
            "requires_clarification": False,
            "required_evidence": list(REQUIRED_EVIDENCE),
            "smart_link_type": "DIRECT_GITHUB_SMART_NOTE",
            "completion_rule": "NO_SMART_LINK_NO_COMPLETION",
            "execution_mode": "EXECUTE_OR_REPORT_EXACT_BLOCKER",
        }

    return {
        "intent": "OTHER",
        "operation": "NONE",
        "requires_clarification": False,
    }


__all__ = ["resolve_smart_note_intent"]
