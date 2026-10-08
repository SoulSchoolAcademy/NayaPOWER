import json
from datetime import datetime, timezone

with open("input.dat", "r") as f:
    content = f.read()

status = "ok" if content else "failed"

with open("run_state.json", "w") as f:
    json.dump({
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }, f, indent=2)

print("wrote run_state.json with status:", status)
