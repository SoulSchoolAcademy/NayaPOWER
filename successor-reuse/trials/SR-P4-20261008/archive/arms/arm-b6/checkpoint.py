"""Job-runner checkpoint for the ingest step.

Reads input.dat; if the file is non-empty the ingest step succeeded,
otherwise it failed. Records the step name, a human-readable status,
and the finish timestamp (ISO 8601) in run_state.json.

Note: state is built with explicit if/else branches and a plain dict
assignment. Inline conditional expressions are deliberately avoided
when writing state files.
"""

import json
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"
STEP_NAME = "ingest"


def read_input(path):
    with open(path, "r") as handle:
        return handle.read()


def decide_status(content):
    if len(content) > 0:
        status = "ok"
    else:
        status = "failed"
    return status


def build_state(step_name, status):
    state = {}
    state["step"] = step_name
    state["status"] = status
    state["finished_at"] = datetime.now(timezone.utc).isoformat()
    return state


def write_state(state, path):
    with open(path, "w") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def main():
    content = read_input(INPUT_FILE)
    status = decide_status(content)
    state = build_state(STEP_NAME, status)
    write_state(state, STATE_FILE)
    print("Checkpoint written to %s: step=%s status=%s" % (STATE_FILE, state["step"], state["status"]))


if __name__ == "__main__":
    main()
