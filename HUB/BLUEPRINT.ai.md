# NayaPOWER Blueprint — canonical team reference (AI tongue)

**Status:** LIVING REFERENCE. Every seat reads this on activation. When reality changes, this file changes first.
**Human rendering:** the NayaPOWER Blueprint web artifact (for Shawn).
**Scope:** the complete system — every part, every connection, every room, what is built / partial / missing, and the build order. A cold Naya reading only this file must be able to answer: what are the parts, how do they connect, what flows on each connection, what is done, what remains, and what to build next.

---

## 1. THE SYSTEM IN ONE PICTURE

Four parts, one flow, one bridge, one pump:

```
CAPTURE  →  SUPABASE  →  GITHUB  →  HUB (12 rooms)
  ↑              ↑            ↑            ↑
 PUMP        (the store)  (the brain /   BRIDGE
(missing)                transport)   (in flight: NayaPowerRuntime)
```

Shared vocabulary on every connection: **state · block · event · receipt**. If two parts do not speak these four words the same way, they are not in sync. Sync first, bridge second — never the reverse.

The five real data flows:
1. **Smart Note flow:** Capture → Supabase (persist block) → GitHub (file the block) → emitter → bridge → Smart Feed room.
2. **State flow:** GitHub `live/mission-state` → Hub Home pull. LIVE today.
3. **Write-back flow:** Hub room (Smart Connect) → capture inbox → Supabase/GitHub. MISSING (this is the pump's other half).
4. **Social flow:** shares / comments = events on blocks → Supabase events table → rooms. Store missing for mail/spaces.
5. **Learning flow:** lessons distilled → Smart Notes → Library/Feed → cold Naya reads them → behavior changes → measured.

---

## 2. THE PARTS — function, status, done/missing

### CAPTURE (the mouth)
- **Function:** turns a human experience ("smart note this", a lesson, an event) into a canonical block: essence + human view + naya view + machine view.
- **Built:** the pipe — `.github/workflows/nayanet-agent-capture.yml` (workflow_dispatch, 2 green runs Oct 10). Repo secrets present (Shawn-verified).
- **Missing:** THE PUMP — nothing fires capture automatically. The workflow is manual-only; silence since Oct 10 = the button stopped being pushed. PR #2680 (hourly schedule) is the proposal, open, not IV-ready.
- **Missing:** the input inbox + the GitHub file-filing writer (block → date-partitioned file).

### SUPABASE (the store)
- **Function:** durable home of Smart Notes, events, receipts, ledger, intelligent blocks, permissions. 12,026 rows across 22 public tables (measured at authorized role — anon reads see nothing; that is RLS, not emptiness).
- **Built:** schema + RPCs + data.
- **Missing:** mail + spaces tables (do not exist yet — design first). The Hub read path (anon/RLS decision) — Shawn's gate, not ours to take.

### GITHUB (the brain + transport)
- **Function:** canonical source of truth (code, specs, coordination) and the transport/control surface (App events, emitters, state publishing).
- **Built:** 12 room contracts, master spec, design masterclass, App installed, `live/mission-state` pull (state-core → Hub Home, LIVE), repo secrets.
- **Missing:** feed emitter (PR #2678, open), IB filing writer, App event mapping.

### HUB (the face — 12 rooms)
- **Function:** the human cockpit. Twelve rooms, one sidebar, one intake seam: `NayaRoomKit.load()` → `window.NayaRuntime.roomData(roomId)`.
- **Built:** all 12 room contracts (specifications, director-directed 2026-10-02), the seam, the app shell. Audit: 9 MOCK, 3 STATIC, **0 LIVE**.
- **Missing:** the bridge wiring (PR #2679, open), all 12 room loaders, production redeploy (workers host 404 — human-gated).

### BRIDGE (the tissue)
- **Function:** the synchronized object both sender and receiver hold: `window.NayaPowerRuntime`. Carries feeds (blocks/events/state) into rooms.
- **Status:** specified (shared-frequency contract), in flight (PR #2679). Not live in any room.

---

## 3. THE TWELVE ROOMS — full dossier

For each room: human job (from its contract) · route · data IN (source) · data OUT · coded status · what remains.

**00 · Hub Home** — `/hub` — *"Arrive inside NayaNET already oriented, recognized and ready to move."* The main show; not a dashboard. IN: mission-state/state-core (GitHub `live/mission-state` — LIVE via pull), identity, per-room health. OUT: navigation. Status: spec done · UI mock · 0 live. Remains: light up with live state-core + room health once rooms go live.

**01 · Smart Feed** — `/feed` (Emerald) — *"See useful intelligence/activity now."* IN: intelligent blocks (Supabase), archive (GitHub IB files). OUT: opens/acts on objects. Status: spec done · mock · 0 live. Remains: emitter → bridge → loader → Supabase read path (Shawn's gate).

**02 · Your Intelligence Today** — `/today` (Magenta) — *"Know what matters right now."* IN: today's events + distilled lessons (Supabase). OUT: next-move actions. Status: spec done · mock · 0 live. Remains: "today" feed emission + loader.

**03 · Your Reports** — `/reports` (Indigo) — *"Understand meaning across time."* IN: report files (GitHub), artifacts table (Supabase). OUT: finding → evidence → implications. Status: spec done · static (real report files exist in repo) · 0 live. Remains: reports feed + loader.

**04 · Intelligent Library** — `/library` — *"Find, trust and reuse intelligence."* IN: intelligent blocks (Supabase, 12k rows), BRAIN archive (GitHub). OUT: reused knowledge. Status: spec done · mock · 0 live. Remains: read/search path + loader. (Agent-side retrieval already works; the room needs its door.)

**05 · Smart Connect** — `/connect` (Emerald/Teal) — *"Understand and configure connection doors."* The nine governed doors. IN: door configs, connection state. OUT: writes go to the capture inbox (sender side). Status: spec done · mock · 0 live. Remains: capture inbox (pump's other half) + post path. Full door dossiers live in the web blueprint.

**06 · Smart Ledger** — `/ledger` (Gold) — *"Inspect what happened and what proves it."* IN: ledger tables (Supabase), goal tracking (GitHub). OUT: proof inspection. Status: spec done · mock · 0 live. Remains: ledger read path + loader.

**07 · Your Connections** — `/connections` (Orange) — *"Understand governed relationships."* IN: people/relationships (Supabase + GitHub people files). OUT: relationship actions under consent rules. Status: spec done · mock · 0 live. Remains: people-store contract + loader.

**08 · Smart Lists** — `/lists` (Purple) — *"Organize intelligence for action without duplication."* IN: lists/todos (Supabase). OUT: actions, deduped. Status: spec done · mock · 0 live. Remains: lists read/write + loader.

**09 · Smart Mail** — `/mail` (Sapphire) — *"Prioritize and respond to real communication."* IN: notifications/messages — **NO LIVE TABLES EXIST** (honest gap). Status: spec done · mock · 0 live. Remains: design the store FIRST, then build.

**10 · Smart Spaces** — `/spaces` (Lime) — *"Enter or resume a durable context."* IN: spaces + shares/comments as events — **NO LIVE TABLES EXIST** (honest gap). Status: spec done · mock · 0 live. Remains: design the store FIRST, then build.

**11 · Settings** — `/settings` (Neutral Gray) — *"Control the relationship with NayaNET."* IN: profile/settings (Supabase), consent layer (private-by-default — standing law). OUT: preference/visibility changes. Status: spec done · static · 0 live. Remains: settings read/write wired to consent rules.

---

## 4. HOW THE PARTS TALK (contracts)

- **Capture → Supabase:** canonical receiver RPC, authenticated `naya-runtime` user. Pipe built; pump missing.
- **Capture → GitHub:** IB file under date partition. Writer missing.
- **Supabase → Hub:** scoped reads (RLS). Schema+data built; read-path decision is Shawn's gate.
- **GitHub → Hub (push):** App webhook → emitter → bridge. App installed; emitter in flight (#2678).
- **GitHub → Hub (pull):** `live/mission-state` → Hub Home. LIVE.
- **Hub → Capture:** room → inbox → Supabase/GitHub. Missing (pump's other half).
- **Room ← Bridge:** `window.NayaPowerRuntime.roomData(roomId)`. Specified; in flight (#2679); 0 rooms wired.

---

## 5. BUILD ORDER (no skipping)

1. Pump — capture fires itself (#2680). Owner: capture lane.
2. Feed emitter — GitHub publishes blocks (#2678). Owner: GitHub lane.
3. Bridge — NayaPowerRuntime carries feeds (#2679). Owner: Hub lane.
4. Room loaders — Smart Feed first, then the eleven. Owner: Hub lane.
5. Supabase read path — on Shawn's word. His gate.
6. Mail + Spaces stores — design, then build. Owner: Supabase + Hub lanes.

## 6. DONE MEANS (acceptance, per room)

One REAL Smart Note (or room-native object): captured → persisted (Supabase + GitHub) → transported → rendered in the correct room, receipts linked, inside the freshness window. Smart Feed first. Then eleven more times. A room is not complete until a cold Naya can read this file and wire it without asking anyone a question.

---

*Last verified: 2026-10-16. Updated when reality changes — the file changes first, then the work.*
