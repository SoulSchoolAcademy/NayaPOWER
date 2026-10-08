"""Checkpoint script for the job runner.

Records the outcome of the completed "ingest" step into run_state.json:
step name, success flag, and finish timestamp in ISO 8601 format.
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
        f.write("\n")


if __name__ == "__main__":
    main()
