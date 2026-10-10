import json
import os
from datetime import datetime, timezone

INPUT = "input.dat"
STATE = "run_state.json"

def main():
    if os.path.isfile(INPUT) and os.path.getsize(INPUT) > 0:
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"Wrote {STATE}: step={state['step']} status={state['status']}")

if __name__ == "__main__":
    main()
