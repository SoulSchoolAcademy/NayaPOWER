"""Job-runner checkpoint for the ingest step.

Reads input.dat: non-empty means the ingest step succeeded, empty means it failed.
Writes run_state.json with the step name, a human-readable status, and an
ISO 8601 finish timestamp.
"""

import json
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"

with open(INPUT_PATH, "rb") as handle:
    payload = handle.read()

if payload:
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_PATH, "w") as handle:
    json.dump(state, handle, indent=2)
    handle.write("\n")

print("checkpoint written:", STATE_PATH, "status:", status)
