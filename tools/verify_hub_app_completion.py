#!/usr/bin/env python3
"""Consistency gate for HUB/APP-COMPLETION-MATRIX-V1.json.

This does not claim the app is complete. It prevents false-completion claims,
missing declared rooms, missing implementation files, and status inflation.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "HUB" / "APP-COMPLETION-MATRIX-V1.json"
REQUIRED_ROOMS = [
    "feed","today","reports","library","connect","ledger",
    "connections","lists","mail","spaces","settings"
]
LEGAL = {
    "NOT_STARTED","SPEC_READY","DESIGN_READY","IMPLEMENTED","TESTED",
    "INTEGRATED","INDEPENDENTLY_VERIFIED","PRODUCTION_PROVEN"
}
ORDER = {name:i for i,name in enumerate([
    "NOT_STARTED","SPEC_READY","DESIGN_READY","IMPLEMENTED","TESTED",
    "INTEGRATED","INDEPENDENTLY_VERIFIED","PRODUCTION_PROVEN"
])}

def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)

def main() -> int:
    errors: list[str] = []
    data = json.loads(MATRIX.read_text())
    declared = data.get("required_primary_rooms", [])
    if declared != REQUIRED_ROOMS:
        fail(f"required_primary_rooms must equal canonical 11 in order; got {declared}", errors)

    rooms = data.get("rooms", {})
    if set(rooms) != set(REQUIRED_ROOMS):
        fail(f"room keys mismatch; missing={sorted(set(REQUIRED_ROOMS)-set(rooms))}, extra={sorted(set(rooms)-set(REQUIRED_ROOMS))}", errors)

    for rid in REQUIRED_ROOMS:
        room = rooms.get(rid, {})
        state = room.get("state")
        if state not in LEGAL:
            fail(f"{rid}: illegal state {state!r}", errors)
        file_rel = room.get("file")
        if not file_rel or not (ROOT / file_rel).is_file():
            fail(f"{rid}: implementation file missing: {file_rel}", errors)
        if state == "PRODUCTION_PROVEN" and not room.get("proof"):
            fail(f"{rid}: PRODUCTION_PROVEN requires proof[]", errors)
        if room.get("runtime") == "NOT_VERIFIED" and state in {"INTEGRATED","INDEPENDENTLY_VERIFIED","PRODUCTION_PROVEN"}:
            fail(f"{rid}: state {state} exceeds NOT_VERIFIED runtime evidence", errors)

    for sid, surface in data.get("surfaces", {}).items():
        state = surface.get("state")
        if state not in LEGAL:
            fail(f"surface {sid}: illegal state {state!r}", errors)
        for rel in surface.get("files", []):
            if not (ROOT / rel).is_file():
                fail(f"surface {sid}: missing file {rel}", errors)

    for gid, gate in data.get("shared_gates", {}).items():
        state = gate.get("state")
        if state not in LEGAL:
            fail(f"gate {gid}: illegal state {state!r}", errors)
        if state == "PRODUCTION_PROVEN" and not gate.get("evidence"):
            fail(f"gate {gid}: PRODUCTION_PROVEN requires evidence", errors)

    for journey in data.get("whole_app_journeys", []):
        state = journey.get("state")
        if state not in LEGAL:
            fail(f"journey {journey.get('id')}: illegal state {state!r}", errors)
        if state == "PRODUCTION_PROVEN" and not journey.get("proof"):
            fail(f"journey {journey.get('id')}: PRODUCTION_PROVEN requires proof", errors)

    if data.get("overall_state") in {"COMPLETE","PRODUCTION_PROVEN"}:
        incomplete = [rid for rid,r in rooms.items() if r.get("state") != "PRODUCTION_PROVEN"]
        if incomplete:
            fail(f"overall cannot be complete; rooms below PRODUCTION_PROVEN: {incomplete}", errors)
        journey_incomplete = [j.get("id") for j in data.get("whole_app_journeys", []) if j.get("state") != "PRODUCTION_PROVEN"]
        if journey_incomplete:
            fail(f"overall cannot be complete; journeys below PRODUCTION_PROVEN: {journey_incomplete}", errors)

    canonical_room_path = ROOT / "HUB" / "NAYANET-SMART-APP-ROOMS-V1.json"
    if not canonical_room_path.is_file():
        fail("canonical machine room contract is missing", errors)
    else:
        canonical_room_data = json.loads(canonical_room_path.read_text())
        if canonical_room_data.get("schema") != "nayanet.smart-app.rooms.v1":
            fail(f"unexpected canonical room schema: {canonical_room_data.get('schema')!r}", errors)
        canonical_ids = [r.get("id") for r in canonical_room_data.get("rooms", [])]
        if canonical_ids != REQUIRED_ROOMS:
            fail(f"canonical room contract identities/order mismatch: {canonical_ids}", errors)

    index = (ROOT / "HUB" / "app" / "index.html").read_text()
    required_scripts = [
        "js/room-contract.js","js/runtime-live.js","js/room-socket.js","js/rooms/shared.js",
        *[f"js/rooms/{rid}.js" for rid in REQUIRED_ROOMS if rid not in {"connect","settings"}],
        "js/rooms/connect.js","js/rooms/settings.js"
    ]
    for src in required_scripts:
        if f'src="{src}"' not in index:
            fail(f"index.html does not load {src}", errors)

    if errors:
        print("HUB COMPLETION MATRIX: FAIL")
        for e in errors: print(" -", e)
        return 1

    print("HUB COMPLETION MATRIX: CONSISTENT")
    print("This is a consistency result, NOT a completion claim.")
    print(f"Rooms declared: {len(REQUIRED_ROOMS)}")
    print(f"Production-proven rooms: {sum(1 for r in rooms.values() if r.get('state') == 'PRODUCTION_PROVEN')}")
    print(f"Overall state: {data.get('overall_state')}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
