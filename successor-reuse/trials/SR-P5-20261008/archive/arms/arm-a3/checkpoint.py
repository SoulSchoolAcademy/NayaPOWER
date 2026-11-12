"""Job runner checkpoint: record the result of the ingest step in run_state.json."""

import json
import os
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"

with open(INPUT_FILE, "rb") as f:
    payload = f.read()

status = "ok" if len(payload) > 0 else "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open(STATE_FILE, "w") as f:
    json.dump(state, f, indent=2)

print(f"checkpoint written: step=ingest status={status}")
