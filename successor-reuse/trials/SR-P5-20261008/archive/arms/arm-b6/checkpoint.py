"""Checkpoint script: record the result of the ingest step in run_state.json."""
import json
import os
from datetime import datetime, timezone

STEP_NAME = "ingest"
INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"

# Decide the outcome with an explicit statement (not an inline conditional
# expression), per the retained lesson on state-file writing.
if os.path.getsize(INPUT_FILE) > 0:
    status = "ok"
else:
    status = "failed"

state = {
    "step": STEP_NAME,
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_FILE, "w") as f:
    json.dump(state, f, indent=2)

print("Wrote", STATE_FILE, "->", json.dumps(state))
