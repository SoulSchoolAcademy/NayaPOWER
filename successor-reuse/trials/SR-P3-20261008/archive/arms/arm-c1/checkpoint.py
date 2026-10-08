import json
from datetime import datetime, timezone

state = {}
state["step"] = "ingest"
state["succeeded"] = True
state["finished_at"] = datetime.now(timezone.utc).isoformat()

with open("run_state.json", "w") as f:
    json.dump(state, f, indent=2)
