#!/usr/bin/env python3
"""Job-runner checkpoint.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty (or missing) file means it failed. Records the outcome in
run_state.json with the step name, a human-readable status, and an
ISO 8601 finish timestamp.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
STATE_FILENAME = "run_state.json"


def read_input(path):
    """Return the raw text of the input file, or "" if it is missing."""
    if path.is_file():
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    return ""


def main():
    input_path = WORKDIR / "input.dat"
    state_path = WORKDIR / STATE_FILENAME

    content = read_input(input_path)

    if content:
        status = "ok"
    else:
        status = "failed"

    state = {}
    state["step"] = "ingest"
    state["status"] = status
    state["finished_at"] = datetime.now(timezone.utc).isoformat()

    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")

    print("step=ingest status=" + status + " -> " + STATE_FILENAME)


if __name__ == "__main__":
    main()
