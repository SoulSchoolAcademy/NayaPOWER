"""Record the outcome of a completed run step to run_state.json."""
import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
SUCCEEDED = True

state = {
    "step": STEP_NAME,
    "succeeded": SUCCEEDED,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w", encoding="utf-8") as handle:
    json.dump(state, handle, indent=2)
    handle.write("\n")

print("checkpoint written:", state)
