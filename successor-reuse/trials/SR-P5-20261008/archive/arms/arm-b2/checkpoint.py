#!/usr/bin/env python3
"""Job-runner checkpoint for the ingest step.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty file means it failed. Writes the outcome into run_state.json.
"""

import json
import os
from datetime import datetime, timezone

STEP_NAME = "ingest"
INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"


def read_status():
    status = "failed"
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "rb") as f:
            content = f.read()
        if len(content) > 0:
            status = "ok"
    return status


def main():
    status = read_status()
    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    print("Step '{}' finished with status '{}'.".format(STEP_NAME, status))


if __name__ == "__main__":
    main()
