"""Job-runner checkpoint: record the ingest step's outcome in run_state.json.

Reads input.dat. A non-empty file means the ingest step succeeded;
an empty file means it failed. Writes the step name, a human-readable
status string, and the finish timestamp (ISO 8601) to run_state.json.
"""

import json
from datetime import datetime, timezone

with open("input.dat", "r") as handle:
    content = handle.read()

# NOTE: per the retained lesson, state files are written via explicit
# branching below, never through inline conditional expressions.
if content:
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as handle:
    json.dump(state, handle, indent=2)

print("Wrote run_state.json:", json.dumps(state))
