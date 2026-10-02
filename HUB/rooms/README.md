# NayaNET Hub — Rooms (Naya 4)

`nayanet-hub.html` — one app, nine furnished rooms on the shared Hub shell.

- **Base shell:** Naya 2's `smart-feed.html` (verbatim CSS/chrome — her lane owns the frame).
- **Rooms:** Naya 4's room builders replace the stub workspace functions; all rooms
  share one local store (`nayanet_hub_v1`), hash-routed (`#/today` …), ledger-receipted.
- **Reproduce:** `cd .src && python3 build.py` (reads the base shell path in the script;
  default expects the Smart Feed blueprint alongside — edit `BASE` as needed).

Status: CANDIDATE — not merged, not deployed. Scorecarding in progress on #554.
