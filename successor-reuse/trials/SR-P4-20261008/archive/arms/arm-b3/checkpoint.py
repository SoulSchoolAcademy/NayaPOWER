#!/usr/bin/env python3
"""Job runner checkpoint: record the ingest step's outcome in run_state.json."""
import json
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"

with open(INPUT_PATH, "r") as f:
    contents = f.read()

# Explicit branching (no inline conditional) to decide the status.
if contents.strip():
    status = "ok"
else:
    status = "failed"

# Build the state record with plain statements.
record = {}
record["step"] = "ingest"
record["status"] = status
record["finished_at"] = datetime.now(timezone.utc).isoformat()

# Write the state file with an explicit call.
with open(STATE_PATH, "w") as f:
    json.dump(record, f, indent=2)
    f.write("\n")

print("Wrote", STATE_PATH, ":", record)
