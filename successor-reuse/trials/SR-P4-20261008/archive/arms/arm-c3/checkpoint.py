"""Job-runner checkpoint script.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty file means it failed. Writes run_state.json with the step
name, a human-readable status string, and an ISO 8601 finish timestamp.
"""

import json
from datetime import datetime, timezone


def main():
    with open("input.dat", "r") as f:
        contents = f.read()

    if contents:
        status = "ok"
    else:
        status = "failed"

    state = {}
    state["step"] = "ingest"
    state["status"] = status
    state["finish_timestamp"] = datetime.now(timezone.utc).isoformat()

    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
