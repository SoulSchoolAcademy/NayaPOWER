#!/usr/bin/env python3
"""Checkpoint a completed run step into run_state.json.

Records the step name, whether it succeeded, and the finish timestamp
in ISO 8601 format.
"""
import json
from datetime import datetime, timezone

STATE_FILE = "run_state.json"


def main():
    state = {}
    state["step"] = "ingest"
    state["succeeded"] = True
    state["finished_at"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
