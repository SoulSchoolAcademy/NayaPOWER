"""Job runner checkpoint: records the outcome of the ingest step.

Reads input.dat: if the file is non-empty, the ingest step succeeded;
otherwise it failed. Writes run_state.json with the step name, a
human-readable status string, and the finish timestamp in ISO 8601 format.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
INPUT_FILE = WORK_DIR / "input.dat"
STATE_FILE = WORK_DIR / "run_state.json"


def main() -> None:
    content = INPUT_FILE.read_bytes() if INPUT_FILE.exists() else b""
    status = "ok" if content else "failed"
    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Ingest step {status}; state written to {STATE_FILE}")


if __name__ == "__main__":
    main()
