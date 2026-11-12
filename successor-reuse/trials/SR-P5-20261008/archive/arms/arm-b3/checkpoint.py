#!/usr/bin/env python3
"""Job-runner checkpoint: records the outcome of the ingest step.

Reads input.dat; a non-empty file means the ingest step succeeded.
Writes run_state.json with the step name, a human-readable status
string, and the finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"


def main():
    with open(INPUT_PATH, "rb") as handle:
        data = handle.read()

    status = "ok"
    if not data:
        status = "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_PATH, "w") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
