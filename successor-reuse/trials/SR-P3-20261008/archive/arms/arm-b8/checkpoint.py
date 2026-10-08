#!/usr/bin/env python3
"""Checkpoint: record the outcome of a completed run step in run_state.json.

The state payload is written plainly and explicitly. Per the retained lesson,
state files are never written through inline conditional expressions, so the
payload below uses ordinary literals and assignments only.
"""

import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
SUCCEEDED = True


def main():
    run_state = {
        "step": STEP_NAME,
        "success": SUCCEEDED,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open("run_state.json", "w", encoding="utf-8") as f:
        json.dump(run_state, f, indent=2)
        f.write("\n")
    print("checkpoint written to run_state.json")


if __name__ == "__main__":
    main()
