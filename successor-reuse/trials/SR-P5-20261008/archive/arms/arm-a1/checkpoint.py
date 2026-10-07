#!/usr/bin/env python3
"""Checkpoint for the ingest step of the job runner.

Reads input.dat: non-empty means the ingest step succeeded, empty means it
failed. Updates run_state.json with the step name, a human-readable status
string, and the finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

STEP_NAME = "ingest"
INPUT_FILE = Path("input.dat")
STATE_FILE = Path("run_state.json")


def main():
    data = INPUT_FILE.read_bytes() if INPUT_FILE.exists() else b""
    status = "ok" if data else "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"step={STEP_NAME} status={status} -> {STATE_FILE}")


if __name__ == "__main__":
    main()
