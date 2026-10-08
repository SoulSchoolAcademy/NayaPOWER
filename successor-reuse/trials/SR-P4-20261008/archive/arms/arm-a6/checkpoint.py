#!/usr/bin/env python3
"""Job-runner checkpoint: records the outcome of the ingest step in run_state.json."""

import json
from datetime import datetime, timezone
from pathlib import Path

STEP_NAME = "ingest"
INPUT_FILE = Path("input.dat")
STATE_FILE = Path("run_state.json")


def main():
    data = INPUT_FILE.read_text()
    status = "ok" if data.strip() else "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"checkpoint: step={STEP_NAME} status={status} written to {STATE_FILE}")


if __name__ == "__main__":
    main()
