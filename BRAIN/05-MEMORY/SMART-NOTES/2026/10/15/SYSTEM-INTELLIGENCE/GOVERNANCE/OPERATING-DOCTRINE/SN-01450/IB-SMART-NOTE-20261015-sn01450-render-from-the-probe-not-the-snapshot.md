# Render From the Probe, Not the Snapshot — the MAP-STATE Compiler Doctrine

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01450-render-from-the-probe-not-the-snapshot
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:38 PDT smart-note-distillation tick (2026-10-15) by Naya Clarity Narzan from `hidden_files/director-briefing-2026-10-15.md` §8 (Nitro's living-map synthesis, adopted 2026-10-15) and board #2641 comment 6205722639 — the compiler PR was build-underway, not yet open, as of ~18:15 PDT.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Static maps rot. The compiler fixes that: an hourly job probes live state — table counts, feed freshness, bridge existence, seeds-vs-loaders in deployed rooms, capture runs, dock PR states — and commits `HUB/MAP-STATE.json`. Schematics render FROM that file. Drift becomes structurally impossible: the failure mode is "the measurement broke" (loud — a missing commit everyone can see), never "the map went stale" (silent). The read path runs two lanes: public/collective intelligence → emitters → feed files → CDN, zero auth; personal rows → session-direct to Supabase once the read-path decision is made — the database already enforces the privacy doctrine, so routing personal rows through git is machinery we don't need. The 12th door: the state file feeds the Hub Home health strip — the system watches itself. Judgments stay human (what counts as complete); measurements become mechanical (what's true right now).

## 🩷 HUMAN NOTE

Imagine a team that keeps its map on a whiteboard, redrawn from memory every morning. By noon it's wrong, and nobody knows. Now imagine a camera above the whiteboard that photographs the actual ground every hour and redraws the map from the photos. That's the compiler: it doesn't trust the last drawing — it re-measures the ground and draws from the measurement. If the camera breaks, everyone sees a stale timestamp — loud, not silent.

## 🟣 CHILD NOTE

It's like a treasure map. A treasure map drawn once gets old: trees grow, paths move, and the X is wrong. The new rule says: every hour, a robot walks the island, checks where everything really is, and redraws the map. If the robot breaks, the map says "the robot didn't walk today" — you know it's old instead of being tricked by a pretty-but-wrong map.

## 👵 GRANDMA NOTE

You know how a clock can lie to you quietly if it runs slow? You only find out when you miss the train. The team built a rule: instead of drawing the picture once and hoping it stays right, a little worker checks the real thing every hour and stamps the picture with the time. If the worker stops, the stamp goes missing — and missing is loud. You'd rather see "I don't know" than be told something wrong with confidence.

## 🧠 NAYA NOTE

This is the sender-side answer to the receiver-contract lesson: the hub receiver had an empty frame because the sender never emitted the deep tier (SN-1409-class). The compiler generalizes it — every rendering surface (map, health strip, feed) reads from a probed state file, never from a snapshot committed at build time. The stale-map failure mode was silent-by-default (nothing alerts when a snapshot ages); the compiler converts it to loud-by-default (a missing hourly commit IS the alert). Note the two-lane privacy design riding on it: public rows go through git/CDN; personal rows go session-direct to Supabase — because the database enforces the privacy doctrine, routing personal rows through git is machinery nobody needs. When building any status surface, ask: what re-measures this, on what cadence, and what does "the measurement broke" look like to the reader?

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_snapshot_map_silent_drift",
  "evidence": {
    "briefing": "hidden_files/director-briefing-2026-10-15.md §8 (Nitro's synthesis, adopted 2026-10-15; compiler PR build underway, not yet open as of ~18:15 PDT)",
    "board_post": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6205722639",
    "probes_named": "table counts, feed freshness, bridge existence, seeds-vs-loaders in deployed rooms, capture runs, dock PR states",
    "state_file": "HUB/MAP-STATE.json (hourly commit; schematics render FROM it)",
    "consumer": "Hub Home health strip fed by the state file — the system watches itself"
  },
  "rule": "render_status_surfaces_from_live_probed_state_never_from_build_time_snapshots",
  "decision_changed": "how does the system map (and any status surface) stay current: previously static snapshot pages; now an hourly probe job commits MAP-STATE.json and all schematics render from it",
  "falsifier": "if the compiler stops committing MAP-STATE.json and the schematics keep rendering, the doctrine is violated; if a build-time snapshot is provably fresher than the state file, the claim is wrong",
  "mechanism": "the probe job measures live state hourly and commits the result; the failure mode converts from silent staleness (a snapshot aging invisibly) to loud absence (a missing hourly commit is itself the alert); the two-lane read path keeps public rows on git/CDN and personal rows session-direct, so the privacy doctrine rides the database's RLS instead of extra routing machinery",
  "related": ["SN-1424-adjacent (falsification routes the repair)", "GOVERNANCE/OPERATING-DOCTRINE (installed doctrines)"]
}
~~~
