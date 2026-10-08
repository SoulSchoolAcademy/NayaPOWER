"""checkpoint.py - Record the outcome of a completed run step.

Writes/updates run_state.json with the step name, success flag,
and the finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone


def main():
    state = {
        "step": "ingest",
        "succeeded": True,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)
    print("Wrote run_state.json:", state)


if __name__ == "__main__":
    main()
