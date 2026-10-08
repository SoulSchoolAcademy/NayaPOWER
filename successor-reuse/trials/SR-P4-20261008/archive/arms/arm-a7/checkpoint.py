import json
from datetime import datetime, timezone

with open("input.dat", "r") as f:
    data = f.read()

status = "ok" if data else "failed"

run_state = {
    "step": "ingest",
    "status": status,
    "finished_at": datetime.now(timezone.utc).isoformat(),
}

with open("run_state.json", "w") as f:
    json.dump(run_state, f, indent=2)

print(json.dumps(run_state, indent=2))
