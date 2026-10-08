"""Job-runner checkpoint: record the outcome of a completed run step."""
import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"


def record_checkpoint(step_name, succeeded):
    finish_ts = datetime.now(timezone.utc).isoformat()

    state = {}
    state["step"] = step_name
    state["succeeded"] = succeeded
    state["finish_timestamp"] = finish_ts

    with open(STATE_FILE, "w") as fh:
        json.dump(state, fh, indent=2)

    return state


if __name__ == "__main__":
    step_name = "ingest"
    succeeded = True
    result = record_checkpoint(step_name, succeeded)
    print("Checkpoint recorded:")
    print(json.dumps(result, indent=2))
