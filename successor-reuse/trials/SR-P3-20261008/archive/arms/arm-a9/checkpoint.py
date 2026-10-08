#!/usr/bin/env python3
"""Record the outcome of a completed run step in run_state.json."""

import json
from datetime import datetime, timezone

run_state = {
    "step": "ingest",
    "succeeded": True,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(run_state, f, indent=2)

print("run_state.json updated:", run_state)
