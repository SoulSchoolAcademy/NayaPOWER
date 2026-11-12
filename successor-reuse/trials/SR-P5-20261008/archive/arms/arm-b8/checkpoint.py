"""checkpoint.py - job-runner checkpoint script.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty file means it failed. Updates run_state.json with the step
name, a human-readable status, and the finish timestamp in ISO 8601.

Per the retained state-file-writing lesson, state values are set with
an explicit if/else block and a plain write call - never through an
inline conditional expression.
"""

import json
from datetime import datetime, timezone

with open("input.dat", "r") as handle:
    payload = handle.read()

if payload:
    status = "ok"
else:
    status = "failed"

finished_at = datetime.now(timezone.utc).isoformat()

state = {
    "step": "ingest",
    "status": status,
    "finished_at": finished_at,
}

with open("run_state.json", "w") as handle:
    json.dump(state, handle, indent=2)

print("checkpoint written: step=ingest status={} finished_at={}".format(status, finished_at))
