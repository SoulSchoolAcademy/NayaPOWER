# Mission State as Data — the twin and its wiring

**What this is.** `BRAIN/CURRENT-MISSION-STATE.md` is the canonical mission
snapshot — prose, hand-refreshed by the director pass ("Snapshot refresh"
commits, ~30 min cadence; there is no code builder behind it).
`tools/build_mission_state.py` emits its machine-readable twin,
`BRAIN/MISSION-STATE.json` (schema: `tools/mission_state.schema.json`,
`$id: naya.mission-state/1`), deriving every fact in one run from the same
sources the snapshot rests on: the .md itself (parsed structurally —
header, TOP-10 standing line, TEAM STATUS table, KEY NUMBERS line,
WHERE TO GO) plus live GitHub state at emit time (tip via
`GET /git/refs/heads/main`, open PRs paginated, the live board's comment
count). The twin keeps the two fact classes apart — `snapshot` (what the
director published, anchored to its last-verified instant) vs `live`
(what is true at derivation time) — with per-section provenance in
`sources`.

**The drift check.** `tools/check_mission_state_drift.py` re-derives the
snapshot facts from the .md and FAILS (exit 1, one line per drifted field
with the cure) if the committed twin disagrees on any shared fact; it also
schema-validates the twin and enforces the venue scrub (the twin names
the live board only — retired venue 2765 never appears). `--live`
additionally compares the twin's live block against a fresh derivation.

```sh
python3 tools/build_mission_state.py emit          # regenerate the twin
python3 tools/check_mission_state_drift.py         # offline pair check
python3 tools/check_mission_state_drift.py --live  # + fresh-derivation check
python3 -m pytest tools/test_mission_state.py      # parser/drift tests
```

**Refresh cadence (the honest wiring state).** The twin is fresh exactly
when it is regenerated. Two existing refresh loops could carry it, and
both are other lanes' single-writer surfaces (L16: no duplicate
publishers), so this PR ships the tool + the first twin and names the
adoptions rather than seizing them:

1. **Director pass (owner of the .md).** After each snapshot refresh
   commit, run `python3 tools/build_mission_state.py emit` and land the
   regenerated `BRAIN/MISSION-STATE.json` in the same commit. Until the
   director adopts this step, the drift check failing on a refreshed .md
   is the signal that the twin is stale — by design, never silent.
2. **Hourly hub refresh (`hub-state-builder.py`, off-repo, goal
   `hidden_files`).** This is the job that publishes `MISSION-STATE.md` /
   `HUB-STATE.md` to `live/mission-state` (and the ride-along the
   `tools/OPERATING-STATE.md` wiring already specifies for
   OPERATING-STATE.json + QUEUE-CONTRACT.json). The same owner can add
   one step — copy the committed `BRAIN/MISSION-STATE.json` into the
   publish staging dir — and the twin rides the existing publish. At the
   time of writing the `live/mission-state` branch itself is stale (last
   publish 2026-10-17T03:06:44Z, and its `STATE-CORE.json` still names a
   retired board as `venue.live`), so "published state ≤10 min old"
   remains unmet at the publisher layer regardless of the twin; curing
   that belongs to the hub-refresh/state-core owners.

**Consumers.** A cold seat loads `BRAIN/MISSION-STATE.json` for the
mission picture (identity, standing TOP-10, per-area status, key
numbers) and reads the `live` block for the tip/queue/board truth as of
`live.derived_utc` — or re-runs the emitter for a to-the-second read.
OPERATING-STATE.json (tools/operating_state.py) remains the queue/gauge
artifact; the twin is the mission artifact. They are complements, not
rivals.
