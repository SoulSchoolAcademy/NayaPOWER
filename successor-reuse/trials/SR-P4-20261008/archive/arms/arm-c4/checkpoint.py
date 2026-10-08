"""Job-runner checkpoint: record the result of the ingest step.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty file means it failed. Writes the outcome to run_state.json.
"""

import json
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"
STEP_NAME = "ingest"

# Step 1: read the input file.
with open(INPUT_FILE, "r") as handle:
    content = handle.read()

# Step 2: decide the human-readable status from the file contents.
if len(content) > 0:
    status = "ok"
else:
    status = "failed"

# Step 3: build the state record with the three required values.
state = {}
state["step"] = STEP_NAME
state["status"] = status
state["finished_at"] = datetime.now(timezone.utc).isoformat()

# Step 4: write the state record to the run-state file.
with open(STATE_FILE, "w") as handle:
    json.dump(state, handle, indent=2)

print("Checkpoint written:", state)
