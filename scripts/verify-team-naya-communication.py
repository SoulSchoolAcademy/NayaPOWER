#!/usr/bin/env python3
"""End-to-end proof for the Team Naya shared Activity communication surface."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

from team_activity import emit_team_activity  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="naya-team-activity-") as tmp:
        root = Path(tmp) / "events"
        index = root / "INDEX.json"
        mission = "Prove Team Naya can communicate through one durable Activity surface."
        common = dict(mission=mission, recipients=["TEAM-NAYA"], events_root=root, index_path=index)

        first = emit_team_activity(intent="NAYA_SIGNED_IN", actor_id="NAYA-A", session_id="SESSION-A", message="NAYA-A signed in and is taking ownership of the communication test.", next_action="Inspect the shared Activity event store.", **common)
        second = emit_team_activity(intent="NAYA_DISCOVERY", actor_id="NAYA-A", session_id="SESSION-A", message="The canonical event store accepts Team Naya communication events.", next_action="Hand the verified discovery to NAYA-B.", recipients=["NAYA-B"], evidence=[first["event_id"]], **{k: v for k, v in common.items() if k != "recipients"})
        handoff = emit_team_activity(intent="NAYA_HANDOFF", actor_id="NAYA-A", session_id="SESSION-A", message="NAYA-A is handing the verified communication state to NAYA-B.", next_action="NAYA-B must retrieve the discovery and continue from it.", successor="NEXT-NAYA-COMMUNICATION-CONTINUATION", recipients=["NAYA-B"], evidence=[first["event_id"], second["event_id"]], **{k: v for k, v in common.items() if k != "recipients"})
        continuation = emit_team_activity(intent="NAYA_CONTINUING", actor_id="NAYA-B", session_id="SESSION-B", message="NAYA-B retrieved the shared handoff and is continuing the mission.", next_action="Verify the shared event count and replay idempotency.", evidence=[handoff["event_id"]], **common)
        replay = emit_team_activity(intent="NAYA_SIGNED_IN", actor_id="NAYA-A", session_id="SESSION-A", message="NAYA-A signed in and is taking ownership of the communication test.", next_action="Inspect the shared Activity event store.", **common)

        payload = json.loads(index.read_text(encoding="utf-8"))
        event_files = list(root.rglob("SE-*.json"))
        assert payload["status"] == "CANONICAL"
        assert payload["event_count"] == 4 == len(event_files)
        assert replay["status"] == "REPLAY"
        assert replay["event_id"] == first["event_id"]
        assert continuation["event"]["team"]["recipients"] == ["TEAM-NAYA"]
        assert handoff["event"]["continuity"]["handoff_ready"] is True
        assert handoff["event"]["continuity"]["successor"] == "NEXT-NAYA-COMMUNICATION-CONTINUATION"
        assert all(row["type"] == "team-communication" for row in payload["events"])
        print("TEAM_NAYA_COMMUNICATION=PASS")
        print(f"TEAM_NAYA_EVENTS={payload['event_count']}")
        print(f"TEAM_NAYA_SIGN_IN={first['event_id']}")
        print(f"TEAM_NAYA_DISCOVERY={second['event_id']}")
        print(f"TEAM_NAYA_HANDOFF={handoff['event_id']}")
        print(f"TEAM_NAYA_CONTINUATION={continuation['event_id']}")
        print("TEAM_NAYA_IDEMPOTENCY=PASS")
        print("TEAM_NAYA_SHARED_INDEX=PASS")


if __name__ == "__main__":
    main()
