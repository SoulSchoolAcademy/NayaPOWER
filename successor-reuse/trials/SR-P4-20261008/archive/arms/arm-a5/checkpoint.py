#!/usr/bin/env python3
"""Checkpoint for the job runner ingest step.

Reads input.dat: non-empty means the ingest step succeeded, empty means it failed.
Writes run_state.json with the step name, human-readable status, and ISO 8601 finish timestamp.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

STEP_NAME = "ingest"
INPUT_FILE = Path("input.dat")
STATE_FILE = Path("run_state.json")


def main():
    data = INPUT_FILE.read_bytes()
    status = "ok" if data else "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Checkpoint written: step={state['step']} status={state['status']}")


if __name__ == "__main__":
    main()
