"""Job-runner checkpoint script.

Reads input.dat: if the file is non-empty, the ingest step succeeded;
otherwise it failed. Records the result in run_state.json with the step
name, a human-readable status string, and the finish timestamp (ISO 8601).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
INPUT_FILE = WORKDIR / "input.dat"
STATE_FILE = WORKDIR / "run_state.json"


def read_input(path: Path) -> str:
    """Read the input file, returning its contents (empty string if missing)."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def main() -> None:
    data = read_input(INPUT_FILE)

    if data.strip():
        status = "ok"
    else:
        status = "failed"

    state = {
        "step": "ingest",
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"Checkpoint written: {state}")


if __name__ == "__main__":
    main()
