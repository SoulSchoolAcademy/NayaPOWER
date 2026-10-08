#!/usr/bin/env python3
"""Checkpoint the ingest step of the job runner.

Reads input.dat: non-empty means the ingest step succeeded, empty means it
failed. Updates run_state.json with the step name, a human-readable status,
and the finish timestamp in ISO 8601 format.

State-file writing uses explicit branching only (per retained lesson:
never write state files through inline conditional expressions).
"""

import json
import os
from datetime import datetime, timezone

WORKDIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(WORKDIR, "input.dat")
STATE_PATH = os.path.join(WORKDIR, "run_state.json")


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as handle:
        content = handle.read()

    if content:
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")

    print("wrote {}: step=ingest status={}".format(STATE_PATH, status))


if __name__ == "__main__":
    main()
