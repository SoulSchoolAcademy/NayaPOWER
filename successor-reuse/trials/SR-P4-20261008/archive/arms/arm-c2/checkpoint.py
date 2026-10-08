"""Job-runner checkpoint for the ingest step.

Reads input.dat: non-empty means the ingest step succeeded,
empty means it failed. Records the outcome in run_state.json.
"""
import json
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"
STEP_NAME = "ingest"

# Step 1: read the input file.
with open(INPUT_PATH, "r") as f:
    content = f.read()

# Step 2: decide the human-readable status.
if content.strip():
    status = "ok"
else:
    status = "failed"

# Step 3: stamp the finish time in ISO 8601 format.
finished_at = datetime.now(timezone.utc).isoformat()

# Step 4: build the state object.
state = {
    "step": STEP_NAME,
    "status": status,
    "finished_at": finished_at,
}

# Step 5: write the state file.
with open(STATE_PATH, "w") as f:
    json.dump(state, f, indent=2)

print(f"checkpoint written: step={STEP_NAME} status={status} finished_at={finished_at}")
