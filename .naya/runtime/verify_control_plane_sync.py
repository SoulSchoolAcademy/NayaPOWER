#!/usr/bin/env python3
"""Check canonical control-plane next-action synchronization."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"control-plane"
state=json.loads((ROOT/"STATE.json").read_text())
blocks=json.loads((ROOT/"BLOCKS.json").read_text())
baton=json.loads((ROOT/"BATON.json").read_text())
errors=[]
expected=blocks["active_block"]["next_action"]
if state.get("single_next_action")!=expected: errors.append("STATE_NEXT_ACTION_MISMATCH")
if baton.get("next_action",{}).get("action")!=expected: errors.append("BATON_NEXT_ACTION_MISMATCH")
if blocks["active_block"].get("next_action_count")!=1: errors.append("BLOCK_NEXT_ACTION_COUNT_NOT_ONE")
if baton.get("next_action",{}).get("count")!=1: errors.append("BATON_NEXT_ACTION_COUNT_NOT_ONE")
print({"status":"PASS" if not errors else "STALE_OR_CONFLICTED","errors":errors})
raise SystemExit(0 if not errors else 1)
