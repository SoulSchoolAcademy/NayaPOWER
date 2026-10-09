#!/usr/bin/env python3
"""Job-runner checkpoint: records the ingest step outcome into run_state.json."""
import json
import os
from datetime import datetime, timezone

STEP = "ingest"

def main():
    size = os.path.getsize("input.dat") if os.path.exists("input.dat") else 0
    status = "ok" if size > 0 else "failed"
    state = {
        "step": STEP,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()
