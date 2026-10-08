#!/usr/bin/env python3
"""Checkpoint for the job runner: record the ingest step outcome in run_state.json."""

import json
import os
from datetime import datetime, timezone

INPUT_PATH = "input.dat"
STATE_PATH = "run_state.json"


def input_is_nonempty(path):
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) > 0:
        return True
    return False


def main():
    if input_is_nonempty(INPUT_PATH):
        status = "ok"
    else:
        status = "failed"

    state = {}
    state["step"] = "ingest"
    state["status"] = status
    state["finished_at"] = datetime.now(timezone.utc).isoformat()

    with open(STATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
