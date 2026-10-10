#!/usr/bin/env python3
"""Job-runner checkpoint: records the outcome of the ingest step in run_state.json."""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"


def main():
    with open("input.dat", "r") as handle:
        contents = handle.read()

    if contents:
        status = "ok"
    else:
        status = "failed"

    finished_at = datetime.now(timezone.utc).isoformat()

    state = {}
    state["step"] = STEP_NAME
    state["status"] = status
    state["finished_at"] = finished_at

    with open("run_state.json", "w") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
