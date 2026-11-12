#!/usr/bin/env python3
"""Job-runner checkpoint: records the ingest step outcome to run_state.json."""

import json
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = f.read()

# Status is decided explicitly before any file write happens.
if data:
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print(f"Checkpoint written: step=ingest status={status}")
