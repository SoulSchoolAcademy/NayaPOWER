#!/usr/bin/env python3
"""Durable outbox state machine primitives. External delivery is caller-owned."""
from __future__ import annotations

ALLOWED={
    "PENDING":{"ATTEMPTED","FAILED"},
    "ATTEMPTED":{"DELIVERED","FAILED","RETRY"},
    "FAILED":{"RETRY"},
    "RETRY":{"ATTEMPTED","FAILED"},
    "DELIVERED":set(),
}

def transition(current: str, target: str) -> dict:
    current=current.upper(); target=target.upper()
    if target not in ALLOWED.get(current,set()):
        raise ValueError(f"invalid delivery transition: {current} -> {target}")
    return {"from":current,"to":target,"valid":True}

def success_receipt(action_id: str, delivery_state: str, evidence: dict|None=None) -> dict:
    state=delivery_state.upper()
    if state != "DELIVERED":
        raise ValueError("successful delivery receipt requires DELIVERED state")
    return {"action_id":action_id,"delivery_state":"DELIVERED","evidence":evidence or {}}
