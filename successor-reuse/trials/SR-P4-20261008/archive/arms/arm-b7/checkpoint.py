#!/usr/bin/env python3
"""Job-runner checkpoint: record the ingest step result in run_state.json.

Reads input.dat: if it is non-empty, the ingest step succeeded;
otherwise it failed. Writes step name, human-readable status, and the
finish timestamp (ISO 8601) into run_state.json.
"""

import json
from datetime import datetime, timezone

# Ingest outcome: a non-empty input.dat means the step succeeded.
with open("input.dat", "r") as f:
    payload = f.read()

if payload:
    status = "ok"
else:
    status = "failed"

run_state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(run_state, f, indent=2)

print("wrote run_state.json:", run_state)
