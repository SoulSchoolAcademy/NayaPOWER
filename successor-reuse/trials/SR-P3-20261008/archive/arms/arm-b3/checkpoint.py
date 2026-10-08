import json
from datetime import datetime, timezone

# Records the outcome of the completed "ingest" run step.
state = {
    "step": "ingest",
    "succeeded": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)
