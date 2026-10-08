import json
from datetime import datetime, timezone

state = {
    "step": "ingest",
    "succeeded": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("checkpoint recorded:", state)
