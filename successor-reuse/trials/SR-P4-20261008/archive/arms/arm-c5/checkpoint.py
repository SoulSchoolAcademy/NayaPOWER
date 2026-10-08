"""Job-runner checkpoint: record the ingest step outcome in run_state.json."""
import json
import os
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"
STEP_NAME = "ingest"

# Step 1: check whether input.dat contains any data.
file_size = os.path.getsize(INPUT_PATH)

# Step 2: map the data check to a human-readable status string.
if file_size > 0:
    status = "ok"
else:
    status = "failed"

# Step 3: capture the finish timestamp in ISO 8601 format.
finished_at = datetime.now(timezone.utc).isoformat()

# Step 4: assemble the state record.
state = {
    "step": STEP_NAME,
    "status": status,
    "finished_at": finished_at,
}

# Step 5: write the state record to disk.
with open(STATE_PATH, "w") as f:
    json.dump(state, f, indent=2)

print(f"Wrote {STATE_PATH}: step={STEP_NAME} status={status} finished_at={finished_at}")
