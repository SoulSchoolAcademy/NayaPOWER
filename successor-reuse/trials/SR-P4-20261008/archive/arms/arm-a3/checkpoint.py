import json
import os
from datetime import datetime, timezone

with open("input.dat", "rb") as f:
    content = f.read()

status = "ok" if len(content) > 0 else "failed"

state = {
    "step": "ingest",
    "status": status,
    "finish_timestamp": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("wrote run_state.json:", state)
