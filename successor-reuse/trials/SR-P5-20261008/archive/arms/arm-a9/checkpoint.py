"""Checkpoint for the job runner: records the ingest step outcome in run_state.json."""
import json
from datetime import datetime, timezone

STEP_NAME = "ingest"

with open("input.dat", "r", encoding="utf-8") as f:
    contents = f.read()

status = "ok" if contents.strip() else "failed"

state = {
    "step": STEP_NAME,
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print(f"step={STEP_NAME} status={status} -> run_state.json")
