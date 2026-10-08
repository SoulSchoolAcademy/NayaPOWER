#!/usr/bin/env python3
"""Job-runner checkpoint: records ingest step outcome into run_state.json."""
import json
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"

with open(INPUT_PATH, "rb") as handle:
    raw = handle.read()

# Explicit branches; no inline conditional expressions when writing state.
status = "unknown"
if len(raw) > 0:
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_PATH, "w") as handle:
    json.dump(state, fp=handle, indent=2)

print("wrote", STATE_PATH, "status =", status)
