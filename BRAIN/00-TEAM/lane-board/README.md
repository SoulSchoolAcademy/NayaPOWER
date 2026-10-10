# 🛰️ Live Lane Board

**In plain words:** this is the team's pulse — who's working on what, right now.
#1354 stays the permanent record. This board is the live picture, not the archive.

- **Live view:** [LANE-BOARD.md](LANE-BOARD.md) — regenerated on every update, plain words.
- **Machine view:** [lane-board.json](lane-board.json) — the same state as JSON.
- **Per-lane truth:** [lanes/](lanes/) — one file per lane; the schema is in [lanes/_schema.json](lanes/_schema.json).

## Use it in one command (from the repo root)

```bash
# start work
python3 tools/lane_board.py sign-in --lane ws-5 --seat naya-4 --task "Building the board"

# I'm alive (every 15 min while active)
python3 tools/lane_board.py heartbeat --lane ws-5 --seat naya-4

# change what you're doing
python3 tools/lane_board.py set-task --lane ws-5 --seat naya-4 --task "New task in plain words"

# blocked? say so — it shows up red
python3 tools/lane_board.py set-blocker --lane ws-5 --seat naya-4 --blocker "Waiting on WS-3's loader"
python3 tools/lane_board.py set-blocker --lane ws-5 --seat naya-4 --clear-blocker

# done for now
python3 tools/lane_board.py sign-out --lane ws-5 --seat naya-4

# read the live board
python3 tools/lane_board.py show
```

Pick your lane id from [LANE-BOARD.md](LANE-BOARD.md): `ws-0`…`ws-10` for the ten
charter workstreams (+ WS-0 ratification landing), `team-1865`…`team-1873` for
the nine standing teams.

## The rules

1. **Heartbeat every 15 minutes** while you're active on a lane.
2. **Older than 30 minutes = STALE**, marked automatically by the renderer — no
   one has to call it out.
3. **Blocked lanes name the blocker and who can unblock.** A blocker stuck more
   than 30 minutes gets surfaced on #1354 tagged to the lane that can unblock.
4. The board is the pulse; **#1354 is the permanent record**. Receipts,
   decisions, and ratifications still go there.

## Design decisions (why it looks like this)

- **One file per lane, not one big JSON.** Two lanes heartbeating at the same
  second never fight over the same file — concurrent writes can't conflict.
  The single-JSON and rendered views are *generated* from the lane files.
- **Live state on a dedicated `lane-board` branch, written directly, no PR.**
  The board needs sub-minute write latency; review would defeat the purpose.
  Heartbeats also must not spam CI on main (the Waste Meter workstream would
  flag that). The branch never merges back into main — main carries the
  tooling, the docs, and a reviewed seed snapshot.
- **Confined blast radius.** The updater only ever writes inside
  `BRAIN/00-TEAM/lane-board/` on the `lane-board` branch. It cannot touch code,
  tests, or production. Ref updates retry if the tip moved (last-writer-wins
  per lane, which is correct for heartbeats).
- **Staleness is derived, never stored.** The renderer computes it from
  `heartbeat_utc` at read time, so a dead lane can't lie about being fresh.

## Files

| Path | What it is |
|---|---|
| `tools/lane_board.py` | The updater CLI (stdlib only). |
| `lanes/<lane>.json` | Source of truth, one file per lane. |
| `lane-board.json` | Generated aggregate snapshot. |
| `LANE-BOARD.md` | Generated human-readable view. |
| `lanes/_schema.json` | The lane record schema. |
