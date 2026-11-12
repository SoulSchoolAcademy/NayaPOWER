"""Job-runner checkpoint for the ingest step.

Reads input.dat: non-empty means the ingest step succeeded, empty means it failed.
Writes run_state.json with the step name, a human-readable status string, and the
finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

WORKDIR = Path(__file__).parent

def main() -> None:
    input_path = WORKDIR / "input.dat"
    state_path = WORKDIR / "run_state.json"

    status = "ok" if input_path.exists() and input_path.read_text().strip() else "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Wrote {state_path.name}: step={state['step']} status={state['status']}")

if __name__ == "__main__":
    main()
