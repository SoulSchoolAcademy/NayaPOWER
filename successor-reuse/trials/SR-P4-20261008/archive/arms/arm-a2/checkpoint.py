#!/usr/bin/env python3
"""Job-runner checkpoint: records the ingest step outcome in run_state.json."""
import json
from datetime import datetime, timezone

with open("input.dat", "r") as f:
    data = f.read()

status = "ok" if data.strip() else "failed"

state = {
    "step": "ingest",
    "status": status,
    "finish_timestamp": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print(json.dumps(state, indent=2))
