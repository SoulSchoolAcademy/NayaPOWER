"""Record the outcome of the completed ingest step to run_state.json."""
import json
from datetime import datetime, timezone

state = {
    "step": "ingest",
    "succeeded": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)
    f.write("\n")

print("run_state.json written:", json.dumps(state))
