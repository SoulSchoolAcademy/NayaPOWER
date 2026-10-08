"""Record the outcome of a completed job-run step.

Writes run_state.json with the step name, success flag, and finish
timestamp. Plain sequential writes only.
"""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
SUCCEEDED = True

state = {
    "step": STEP_NAME,
    "success": SUCCEEDED,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Wrote run_state.json:", state)
