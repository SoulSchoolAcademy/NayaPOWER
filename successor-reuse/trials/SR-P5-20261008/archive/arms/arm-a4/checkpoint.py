import json
import os
from datetime import datetime, timezone

STEP_NAME = "ingest"
INPUT_FILE = "input.dat"
STATE_FILE = "run_state.json"


def main():
    try:
        size = os.path.getsize(INPUT_FILE)
    except OSError:
        size = 0

    status = "ok" if size > 0 else "failed"

    state = {
        "step": STEP_NAME,
        "status": status,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print("step: {}".format(STEP_NAME))
    print("status: {}".format(status))
    print("state written to {}".format(STATE_FILE))


if __name__ == "__main__":
    main()
