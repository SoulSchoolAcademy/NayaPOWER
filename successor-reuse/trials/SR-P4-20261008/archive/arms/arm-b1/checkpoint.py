import json
from datetime import datetime, timezone

step = "ingest"

with open("input.dat", "r") as f:
    content = f.read()

if content.strip():
    status = "ok"
else:
    status = "failed"

finished_at = datetime.now(timezone.utc).isoformat()

with open("run_state.json", "w") as f:
    json.dump({"step": step, "status": status, "finished_at": finished_at}, f, indent=2)
