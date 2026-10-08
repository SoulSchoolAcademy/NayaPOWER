"""Job-runner checkpoint: record the outcome of a completed run step."""

import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"

def main():
    state = {
        "step": "ingest",
        "succeeded": True,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Checkpoint written to {STATE_FILE}: {state}")

if __name__ == "__main__":
    main()
