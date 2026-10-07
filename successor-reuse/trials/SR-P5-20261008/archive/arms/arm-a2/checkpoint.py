#!/usr/bin/env python3
"""Job-runner checkpoint: record the outcome of the ingest step."""
import json
from datetime import datetime, timezone

STATE_PATH = "run_state.json"

with open("input.dat") as f:
    payload = f.read()

succeeded = len(payload.strip()) > 0

state = {
    "step": "ingest",
    "status": "ok" if succeeded else "failed",
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_PATH, "w") as f:
    json.dump(state, f, indent=2)

print(f"Checkpoint written: step={state['step']} status={state['status']}")
