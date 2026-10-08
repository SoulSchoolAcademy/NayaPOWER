"""Checkpoint the ingest step of the job runner.

Reads input.dat: a non-empty file means the ingest step succeeded,
an empty (or missing-content) file means it failed. Updates run_state.json
with the step name, a human-readable status, and an ISO 8601 finish timestamp.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent

def main():
    input_path = WORKDIR / "input.dat"
    state_path = WORKDIR / "run_state.json"

    try:
        content = input_path.read_text()
        succeeded = len(content) > 0
    except FileNotFoundError:
        succeeded = False

    state = {
        "step": "ingest",
        "status": "ok" if succeeded else "failed",
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()
