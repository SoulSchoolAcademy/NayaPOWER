#!/usr/bin/env python3
"""Job-runner checkpoint: record the ingest step outcome in run_state.json.

Reads input.dat; a non-empty file means the ingest step succeeded,
an empty file means it failed. Writes the step name, a human-readable
status string, and the finish timestamp (ISO 8601) to run_state.json.
"""

import json
from datetime import datetime, timezone


def main():
    with open("input.dat", "r") as f:
        data = f.read()

    if data:
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)

    print("wrote run_state.json: step=ingest status=%s" % status)


if __name__ == "__main__":
    main()
