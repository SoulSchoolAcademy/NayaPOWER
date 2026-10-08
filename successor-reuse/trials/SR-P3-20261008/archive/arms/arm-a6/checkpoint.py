#!/usr/bin/env python3
"""Record the outcome of a completed job-runner run step in run_state.json."""

import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"


def record_checkpoint(step, success):
    state = {
        "step": step,
        "succeeded": success,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    return state


if __name__ == "__main__":
    state = record_checkpoint("ingest", True)
    print(f"Checkpoint recorded: {state}")
