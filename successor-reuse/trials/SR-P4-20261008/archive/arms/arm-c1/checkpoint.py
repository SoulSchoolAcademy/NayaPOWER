"""Job-runner checkpoint: records the result of the ingest step."""

import json
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"


def main():
    # Step 1: read the input file.
    with open(INPUT_FILE, "r") as handle:
        content = handle.read()

    # Step 2: decide the outcome. A non-empty file means ingest succeeded.
    if content.strip():
        status = "ok"
    else:
        status = "failed"

    # Step 3: capture the finish time in ISO 8601 format.
    finished_at = datetime.now(timezone.utc).isoformat()

    # Step 4: build the state record, one field at a time.
    state = {}
    state["step"] = "ingest"
    state["status"] = status
    state["finished_at"] = finished_at

    # Step 5: write the state record to disk.
    with open(STATE_FILE, "w") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
