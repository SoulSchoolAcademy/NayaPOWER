"""Job-runner checkpoint: record the ingest step outcome in run_state.json.

Reads input.dat; a non-empty file means ingest succeeded. Writes the
step name, a human-readable status string, and an ISO 8601 finish
timestamp. The state file is written through ordinary statements, not
inline conditional expressions.
"""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"


def main():
    with open("input.dat", "r") as f:
        content = f.read()

    if content.strip():
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
