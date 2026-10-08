"""Job-runner checkpoint: record the outcome of the ingest step in run_state.json."""

import json
import os
from datetime import datetime, timezone

INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"
STEP_NAME = "ingest"

def main():
    # Ingest succeeded if input.dat exists and is non-empty.
    succeeded = (
        os.path.exists(INPUT_FILE)
        and os.path.getsize(INPUT_FILE) > 0
    )
    status = "ok" if succeeded else "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")

    print(f"step={state['step']} status={state['status']} finished_at={state['finished_at']}")

if __name__ == "__main__":
    main()
