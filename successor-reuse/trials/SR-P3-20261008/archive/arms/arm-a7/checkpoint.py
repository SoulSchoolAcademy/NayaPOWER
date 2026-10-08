#!/usr/bin/env python3
"""Record the outcome of a completed job-runner step in run_state.json."""

import json
from datetime import datetime, timezone

state = {
    "step": "ingest",
    "success": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("wrote run_state.json:", json.dumps(state))
