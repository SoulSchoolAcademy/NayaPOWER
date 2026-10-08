"""Record the outcome of a completed run step in run_state.json."""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
SUCCESS = True
FINISH_TIMESTAMP = datetime.now(timezone.utc).isoformat()

run_state = {
    "step": STEP_NAME,
    "success": SUCCESS,
    "finish_timestamp": FINISH_TIMESTAMP,
}

with open("run_state.json", "w") as f:
    json.dump(run_state, f, indent=2)

print(f"Recorded step '{STEP_NAME}' (success={SUCCESS}) at {FINISH_TIMESTAMP}")
