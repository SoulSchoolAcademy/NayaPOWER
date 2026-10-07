"""Job-runner checkpoint: record the ingest step's outcome in run_state.json.

Reads input.dat; non-empty means the ingest step succeeded, empty means it
failed. Writes the step name, status, and finish timestamp to run_state.json.
"""

import json
from datetime import datetime, timezone

with open("input.dat", "r") as f:
    data = f.read()

# Compute the status with an explicit if/else, before any file write happens.
if data:
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Wrote run_state.json:", state)
