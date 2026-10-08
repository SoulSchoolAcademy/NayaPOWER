"""Job-runner checkpoint: records the outcome of the ingest step in run_state.json."""

import json
from datetime import datetime, timezone
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent

STEP_NAME = "ingest"
INPUT_FILE = WORK_DIR / "input.dat"
STATE_FILE = WORK_DIR / "run_state.json"


def main() -> None:
    content = INPUT_FILE.read_bytes()

    status = "failed"
    if content:
        status = "ok"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {STATE_FILE} -> {state}")


if __name__ == "__main__":
    main()
