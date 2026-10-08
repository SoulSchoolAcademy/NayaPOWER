"""Record the outcome of a completed run step in run_state.json."""

import json
import os
from datetime import datetime, timezone

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_state.json")

state = {}
if os.path.exists(STATE_PATH):
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

state.update({
    "step": "ingest",
    "success": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
})

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print(json.dumps(state, indent=2))
