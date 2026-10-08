#!/usr/bin/env python3
"""Job-runner checkpoint: record the ingest step outcome into run_state.json."""

import json
import os
from datetime import datetime, timezone

WORKDIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(WORKDIR, "input.dat")
STATE_FILE = os.path.join(WORKDIR, "run_state.json")


def main() -> None:
    # If input.dat is non-empty, the ingest step succeeded; otherwise it failed.
    with open(INPUT_FILE, "r") as f:
        content = f.read()
    status = "ok" if content else "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
