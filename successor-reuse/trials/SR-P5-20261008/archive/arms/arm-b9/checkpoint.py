"""Job-runner checkpoint for the ingest step.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty file means it failed. Writes run_state.json with the step
name, a human-readable status, and the finish timestamp in ISO 8601.
"""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"


def read_ingest_input(path):
    """Return the raw contents of the ingest input file."""
    with open(path, "r") as handle:
        return handle.read()


def determine_status(raw_contents):
    """Map input contents to a human-readable status string.

    Uses an explicit if/else block rather than an inline conditional
    expression, so the state decision stays easy to audit.
    """
    if raw_contents:
        return "ok"
    else:
        return "failed"


def finish_timestamp():
    """Current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def write_state(path, step, status, finished_at):
    """Write the checkpoint state file."""
    state = {
        "step": step,
        "status": status,
        "finished_at": finished_at,
    }
    with open(path, "w") as handle:
        json.dump(state, handle, indent=2)


def main():
    raw = read_ingest_input("input.dat")
    status = determine_status(raw)
    write_state("run_state.json", STEP_NAME, status, finish_timestamp())
    print("Checkpoint written: step=%s status=%s" % (STEP_NAME, status))


if __name__ == "__main__":
    main()
