"""checkpoint.py - record the outcome of a completed run step.

Updates run_state.json with the step name, success flag, and
finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"


def main():
    state = {
        "step": "ingest",
        "succeeded": True,
        "finish_timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print(f"Wrote {STATE_FILE}: {state}")


if __name__ == "__main__":
    main()
