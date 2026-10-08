"""Record the outcome of a completed job-run step in run_state.json."""
import json
from datetime import datetime, timezone


def main():
    state = {}
    state["step"] = "ingest"
    state["success"] = True
    state["finished_at"] = datetime.now(timezone.utc).isoformat()
    with open("run_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
