import json
from datetime import datetime, timezone

with open("input.dat", "r") as f:
    data = f.read()

# Decide the status first, using an explicit if/else statement,
# before writing anything to the state file.
if data.strip():
    status = "ok"
else:
    status = "failed"

state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)

print(json.dumps(state, indent=2))
