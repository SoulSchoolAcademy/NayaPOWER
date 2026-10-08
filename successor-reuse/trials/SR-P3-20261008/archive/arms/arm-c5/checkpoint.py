"""Record the outcome of the completed 'ingest' run step in run_state.json."""

import json
from datetime import datetime, timezone

state = {}
state["step"] = "ingest"
state["succeeded"] = True
state["finished_at"] = datetime.now(timezone.utc).isoformat()

with open("run_state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print("Wrote run_state.json:", state)
