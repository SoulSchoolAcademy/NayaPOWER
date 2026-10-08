import json
from datetime import datetime, timezone

step_name = "ingest"
succeeded = True
finished_at = datetime.now(timezone.utc).isoformat()

run_state = {
    "step": step_name,
    "succeeded": succeeded,
    "finished_at": finished_at,
}

with open("run_state.json", "w") as f:
    json.dump(run_state, f, indent=2)
