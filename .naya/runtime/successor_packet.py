#!/usr/bin/env python3
"""Generate a successor mission packet from verified current state.

This is a projection of existing control-plane truth, not a new state store.
"""
from __future__ import annotations
from typing import Any

def generate_successor(*, state: dict, block: dict, proof: dict, evidence: list[str]) -> dict:
    action=block.get("next_action")
    if block.get("next_action_count") != 1 or not action:
        raise ValueError("SUCCESSOR_REQUIRES_EXACTLY_ONE_NEXT_ACTION")
    if state.get("status") not in {"LIVE_BOUND","CANONICAL"}:
        raise ValueError("SUCCESSOR_REQUIRES_LIVE_STATE")
    return {
      "schema":"NAYAPOWER_SUCCESSOR_PACKET_V1",
      "status":"READY",
      "mission":state.get("mission"),
      "north_star":state.get("north_star"),
      "active_block":block.get("active_block",{}).get("id"),
      "active_block_status":block.get("active_block",{}).get("status"),
      "next_action":action,
      "evidence":list(evidence),
      "truth_rules":proof.get("separation_rules",[]),
      "instruction":"Restore these canonical sources before consequential action; execute only the single authorized next action; verify independently; rebuild successor state.",
    }
