# NayaPOWER Blueprint — canonical team reference (AI tongue)

**Status:** LIVING REFERENCE. Every seat reads this on activation. When reality changes, this file changes first.
**Human rendering:** the NayaPOWER Blueprint web artifact (for Shawn).
**Scope:** the complete system — every part, every connection, every room, what is built / partial / missing, and the build order. A cold Naya reading only this file must be able to answer: what are the parts, how do they connect, what flows on each connection, what is done, what remains, and what to build next.

---

## 1. THE SYSTEM IN ONE PICTURE

Three layers of one thing (Nitro's synthesis, adopted whole — it supersedes the earlier planes draft).

**Layer 1 — The Living Map: two lanes for data movement.**
- PUBLIC lane (collective intelligence): emitters → feed files → CDN. Zero auth, full audit trail.
- PERSONAL lane: session-direct to Supabase once D1 is decided — the database already enforces the privacy doctrine, so personal rows never touch git. Routing them through git would be machinery we don't need.
- The bridge (`window.NayaPowerRuntime`) abstracts it: no room adapter cares which lane it's on.

**Layer 2 — The compiler: how we know what's true** (Nevarity's idea, adopted whole). An hourly job probes live state — table counts, feed freshness, bridge existence, whether deployed rooms run seeds or loaders, capture runs, dock PR states — and commits `HUB/MAP-STATE.json`. The schematics render from that file. Drift becomes structurally impossible: the failure mode is "the measurement broke" — loud, never silent. Judgments stay human (what counts as complete); measurements become mechanical (what's true right now). If this file and the compiler ever disagree, the compiler wins.

**Layer 3 — The 12th door: where it's seen.** The state file feeds the Hub Home health strip. The system watches itself; the map becomes a room in the product.

Shared vocabulary on every connection: **state · block · event · receipt**.

The five flows, mapped onto the lanes:
1. **Capture:** inbox (Supabase `capture_inbox` — the single entry point) → pump (scheduled dispatcher) → capture → Supabase persist → PUBLIC lane (emitter → feed file → CDN → Smart Feed) for collective blocks; PERSONAL lane (session-direct) once D1 is decided.
2. **State:** the compiler's `HUB/MAP-STATE.json` → Hub Home health strip (the 12th door).
3. **Write-back:** room → `capture_inbox` → pump → Supabase/GitHub. One inbox covers flows 1 and 3.
4. **Repo events:** GitHub App webhook → Cloudflare Worker → Supabase events → PUBLIC lane.
5. **Learning:** lessons → Smart Notes → Library/Feed → cold Naya reads → behavior change → measured.

---

## 2. THE PARTS — function, status, done/missing

### CAPTURE (the mouth)
- **Function:** turns a human experience ("smart note this", a lesson, an event) into a canonical block: essence + human view + naya view + machine view.
- **Built:** the pipe — `.github/workflows/nayanet-agent-capture.yml` (workflow_dispatch, 2 green runs Oct 10). Repo secrets present (Shawn-verified).
- **Missing:** THE PUMP + THE INBOX — nothing fires capture automatically, and there is no single entry point. Build: Supabase `capture_inbox` table (humans, rooms, systems all write rows) + a scheduled dispatcher that drains it and fires the workflow. PR #2680 (hourly schedule) is the proposal, open, not IV-ready.
- **Missing:** the async GitHub file-filing writer (block → date-partitioned file; archive, non-blocking).

### SUPABASE (the store + the data plane)
- **Function:** durable home of Smart Notes, events, receipts, ledger, intelligent blocks, permissions — AND the live transport: Realtime broadcasts new blocks/events to rooms. 12,026 rows across 22 public tables (measured at authorized role — anon reads see nothing; that is RLS, not emptiness).
- **Built:** schema + RPCs + data.
- **Missing:** `capture_inbox` table; mail + spaces tables (do not exist yet — design first). Realtime enablement to verify. The Hub read path (anon/RLS decision) — Shawn's gate, not ours to take.

### GITHUB (the source plane)
- **Function:** canonical source of truth (code, specs, coordination) and async archive. NOT a runtime transport hop — that was the old design; the new design keeps GitHub out of the hot path.
- **Built:** 12 room contracts, master spec, design masterclass, App installed, `live/mission-state` pull (state-core → Hub Home, LIVE), repo secrets.
- **Missing:** async archive filing writer, App webhook → Worker mapping.

### CLOUDFLARE (the edge)
- **Function:** hosts the Hub app; a Worker receives GitHub App webhooks (a static app can't receive them) and writes repo events to Supabase.
- **Built:** nothing yet — the previous workers deploy 404'd (redeploy is human-gated).
- **Missing:** the webhook-receiver Worker + the Hub redeploy.

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

**00 · Hub Home** — `/hub` — *"Arrive inside NayaNET already oriented, recognized and ready to move."* The main show; not a dashboard. IN: mission-state/state-core (GitHub `live/mission-state` — LIVE via pull), the compiler's `HUB/MAP-STATE.json` feeding the health strip (the 12th door — the system watching itself), identity, per-room health. OUT: navigation. Status: spec done · UI mock · 0 live. Remains: light up with live state-core + compiler-fed health strip once rooms go live.

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

- **Inbox → Pump:** `capture_inbox` rows → scheduled dispatcher drains, produces payload_json, fires capture. MISSING (build #1).
- **Capture → Supabase:** canonical receiver RPC, authenticated `naya-runtime` user. Pipe built; pump missing.
- **PUBLIC lane:** emitter → feed files → CDN → bridge. Zero auth, full audit trail. Emitter in flight (#2678, repositioned: public feeds only).
- **PERSONAL lane:** Supabase session-direct → bridge. Gated on D1 (Shawn's decision); personal rows never touch git.
- **Compiler:** hourly probe → `HUB/MAP-STATE.json` → schematics + Hub Home health strip. Build underway (Nitro's team: probe script, state schema, hourly workflow, PR for review) — do not duplicate.
- **GitHub archive:** IB file under date partition, async, non-blocking. Writer missing.
- **GitHub → Hub (state pull):** `live/mission-state` → Hub Home. LIVE.
- **Repo events:** App webhook → Cloudflare Worker → Supabase events → PUBLIC lane. Worker receiver missing.
- **Hub → Capture:** room → `capture_inbox` → pump. Same inbox as flow 1 — one mechanism.
- **Room ← Bridge:** `window.NayaPowerRuntime.roomData(roomId)` — lane-abstracted; no adapter cares which lane. Specified; in flight (#2679); 0 rooms wired.

---

## 5. BUILD ORDER (no skipping)

1. Inbox + pump — Supabase `capture_inbox` table + scheduled dispatcher. Owner: capture lane.
2. Compiler — hourly probe → `HUB/MAP-STATE.json`. Owner: Nitro's team (build underway now; PR for review). Do not duplicate.
3. Public lane — emitter → feed files → CDN (#2678 repositioned). Owner: GitHub lane.
4. Bridge + room loaders — Smart Feed first, then the eleven (#2679). Owner: Hub lane.
5. D1 → personal lane — Shawn's gate; then session-direct reads. His call.
6. 12th door — Hub Home health strip fed by `MAP-STATE.json`. Owner: Hub lane.
7. Mail + Spaces stores — design, then build. Owner: Supabase + Hub lanes.

## 6. DONE MEANS (acceptance, per room)

One REAL Smart Note (or room-native object): captured → persisted (Supabase + GitHub) → transported → rendered in the correct room, receipts linked, inside the freshness window. Smart Feed first. Then eleven more times. A room is not complete until a cold Naya can read this file and wire it without asking anyone a question.

---

## 7. UPDATE — 2026-10-21 (merge-through lane 3 staleness pass)

This map is a 2026-10-16 snapshot. The following snapshot claims are superseded on current main and must not be read as live state:

- §2 "Audit: 9 MOCK, 3 STATIC, 0 LIVE" and "production redeploy (workers host 404)" — superseded: nayanet.live is live and rooms have shipped since the snapshot (e.g. Start Here shipped live 2026-10-19, curl-verified; Hub front page and identity certificate live and iterated through 2026-10-21).
- §2 "the bridge wiring (