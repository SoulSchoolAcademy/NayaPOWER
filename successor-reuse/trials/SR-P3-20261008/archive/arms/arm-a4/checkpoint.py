"""Record the outcome of a completed run step to run_state.json."""
import json
from datetime import datetime, timezone

STEP_NAME = "ingest"
SUCCESS = True

def main():
    state = {
        "step": STEP_NAME,
        "success": SUCCESS,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    with open("run_state.json", "w") as f:
        json.dump(state, f, indent=2)
    print("Wrote run_state.json:", state)

if __name__ == "__main__":
    main()
