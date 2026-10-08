import json
from datetime import datetime, timezone

step_name = "ingest"
succeeded = True
finished_at = datetime.now(timezone.utc).isoformat()

state = {
    "step": step_name,
    "succeeded": succeeded,
    "finished_at": finished_at,
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("wrote run_state.json")
