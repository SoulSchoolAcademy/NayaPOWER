#!/usr/bin/env python3
"""Job-runner checkpoint: record the ingest step outcome in run_state.json."""
import json
import os
from datetime import datetime, timezone

STEP_NAME = "ingest"
INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"


def ingest_succeeded(path):
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) == 0:
        return False
    return True


def main():
    if ingest_succeeded(INPUT_FILE):
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_FILE, "w") as handle:
        json.dump(state, handle, indent=2)

    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
