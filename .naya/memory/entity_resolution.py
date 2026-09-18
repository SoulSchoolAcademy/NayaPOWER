#!/usr/bin/env python3
"""Safe entity-resolution decisions built on the existing deterministic audit."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import duplicate_entity_audit as audit

DECISIONS = {"CREATE", "UPDATE", "LINK", "SUPERSEDE", "REVIEW"}

def decide(existing: dict, incoming: dict) -> dict:
    result = audit.classify(existing, incoming)
    if result["decision"] == "DUPLICATE":
        action = "UPDATE"
        reason = "deterministic content fingerprint is identical"
    elif result["decision"] == "LINK_OR_REVIEW":
        action = "REVIEW"
        reason = "similarity is material but automatic merge is not proven safe"
    else:
        action = "CREATE"
        reason = "no high-confidence identity equivalence established"
    return {**result, "action": action, "reason": reason}

def apply_decision(existing: dict, incoming: dict, action: str) -> dict:
    """Return a proposed transition; persistence remains an explicit caller action."""
    action = action.upper()
    if action not in DECISIONS:
        raise ValueError(f"unsupported resolution action: {action}")
    if action == "REVIEW":
        return {"action": "REVIEW", "requires_human_or_authorized_ai_decision": True, "existing_event_id": existing.get("event_id"), "incoming_event_id": incoming.get("event_id")}
    if action == "CREATE":
        return {"action": "CREATE", "preserve_existing": True, "incoming_event_id": incoming.get("event_id")}
    if action == "UPDATE":
        return {"action": "UPDATE", "target_event_id": existing.get("event_id"), "preserve_history": True}
    if action == "LINK":
        return {"action": "LINK", "target_event_id": existing.get("event_id"), "preserve_both": True}
    return {"action": "SUPERSEDE", "superseded_event_id": existing.get("event_id"), "replacement_event_id": incoming.get("event_id"), "preserve_history": True}
