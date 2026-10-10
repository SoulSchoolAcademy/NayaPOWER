#!/usr/bin/env python3
"""Job-runner checkpoint: records the ingest step outcome into run_state.json."""
import json
import os
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"


def main():
    try:
        non_empty = os.path.getsize(INPUT_FILE) > 0
    except FileNotFoundError:
        non_empty = False
    status = "ok" if non_empty else "failed"
    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
