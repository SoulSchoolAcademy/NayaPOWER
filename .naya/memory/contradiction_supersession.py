#!/usr/bin/env python3
"""Explicit contradiction/supersession transitions; history is never erased."""
from __future__ import annotations
from copy import deepcopy


def propose_supersession(previous: dict, replacement: dict, evidence: dict) -> dict:
    if not previous.get("event_id") or not replacement.get("event_id"):
        raise ValueError("both previous and replacement events require stable IDs")
    if not evidence:
        raise ValueError("supersession requires evidence")
    return {
        "decision": "SUPERSEDE",
        "previous_event_id": previous["event_id"],
        "replacement_event_id": replacement["event_id"],
        "evidence": deepcopy(evidence),
        "history_preserved": True,
        "current_event_id": replacement["event_id"],
    }


def apply_supersession(previous: dict, replacement: dict, evidence: dict) -> tuple[dict, dict]:
    """Produce non-destructive event updates. Caller owns persistence."""
    proposal = propose_supersession(previous, replacement, evidence)
    old = deepcopy(previous)
    new = deepcopy(replacement)
    old.setdefault("relationships", {}).setdefault("superseded_by", []).append(new["event_id"])
    old["status"] = "SUPERSEDED"
    old.setdefault("supersession", {})["replacement_event_id"] = new["event_id"]
    old["supersession"]["evidence"] = deepcopy(evidence)
    new.setdefault("relationships", {}).setdefault("supersedes", []).append(old["event_id"])
    new.setdefault("supersession", {})["previous_event_id"] = old["event_id"]
    new["supersession"]["evidence"] = deepcopy(evidence)
    return old, new
