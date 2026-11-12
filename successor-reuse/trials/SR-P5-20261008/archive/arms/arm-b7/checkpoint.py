#!/usr/bin/env python3
"""Job-runner checkpoint: records the ingest step result in run_state.json."""

import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"
INPUT_FILE = "input.dat"


def main():
    with open(INPUT_FILE, "rb") as f:
        raw = f.read()

    if raw:
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
