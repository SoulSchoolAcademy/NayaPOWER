#!/usr/bin/env python3
"""Job-runner checkpoint: records whether the ingest step succeeded."""
import json
import os
from datetime import datetime, timezone

WORKDIR = os.path.dirname(os.path.abspath(__file__))

def main():
    with open(os.path.join(WORKDIR, "input.dat"), "rb") as f:
        data = f.read()

    status = "ok" if data else "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(os.path.join(WORKDIR, "run_state.json"), "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
