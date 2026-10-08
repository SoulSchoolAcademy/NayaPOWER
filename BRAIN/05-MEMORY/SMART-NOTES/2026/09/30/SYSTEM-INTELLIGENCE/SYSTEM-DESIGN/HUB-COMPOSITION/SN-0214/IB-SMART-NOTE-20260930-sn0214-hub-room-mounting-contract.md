# One Hub-Mounting Convention: Rooms Project Canonical Records, Never Copies

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0214-hub-room-mounting-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5960016699 ([NAYA-4 → NAYA-2] Room 01 + Room 02 backend-connection handshake, 2026-10-02 19:36:52Z), director-directed

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 19:36:52Z, on the Human Director's direction, Naya 4 proposed a single hub-room mounting contract to Naya 2's lane: instead of two independently built rooms drifting into "parallel islands," the hub shell and every room agree on ONE composition convention — shell calls a loader, the loader returns `{records, errors}`, the shell passes them as `ctx`, the room mounts via `NayaRooms.x(el, ctx)`. Room 02 (Your Intelligence Reports) already implements the pattern: all six canonical daily reports (Sep 27 → Oct 2, `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/...`) parse through `HUB/app/js/rooms/reports-adapter.js` and render through `window.NayaRooms.reports(el, ctx)` on branch `naya4/room-02-reports-v2` (`bd6219c`/`ff23c33`); `reports-loader.js` is the transport contract — `ReportsLoader.loadDaily({from, to, base}) → {reports, errors} → ctx.reports → room mount`. The governing principle: a room **projects the canonical Brain records, never a copy** — the room's store is derived from the loader's view of the canonical source at mount time, so the shell owns the data contract and the room owns only the rendering. The open question is Room 01's loader shape (the #1328 v8.3 checkpoint + `INTELLIGENCE-TODAY-MASTER-DIRECTIVE-V1.md` are the source). No shell changes and no merges from the proposing lane — contract first, implementation second. This is a PROPOSAL (CANDIDATE): Naya 2's lane has not yet accepted the convention. If accepted, it becomes hub composition law; until then it binds only the proposing lane's rooms.

Why this is brain-grade: the Hub era's recurring failure was rooms-as-parallel-apps — independently built pieces that can't compose. The contract solves it at the seam, not in either room: one mounting convention means Room 03, 04, … inherit composition for free; "never a copy" means canonical Brain records stay single-source-of-truth through every projection; the loader is the testable boundary (wrong data is the shell/loader's problem, wrong pixels are the room's). A cold successor building the next room needs exactly this: the contract shape, the ctx convention, and the rule that rooms never duplicate canonical content.

## 🩷 HUMAN NOTE

Shawn — a small design-law proposal from this afternoon's board traffic, per your direction to connect Room 01 and Room 02: instead of two rooms drifting into parallel islands, I'm proposing one mounting convention the shell and every room share — the shell loads (loader → ctx → `NayaRooms.x(el, ctx)`), and each room *projects the canonical Brain records, never a copy*. Room 02 already works this way (`reports-loader.js` as the transport contract, six daily reports rendering from the canonical files). The open question back to Naya 2's lane is Room 01's loader shape — no merges, no shell changes from my side, contract first. If her lane accepts, this becomes the law every future room follows.

## 🟣 CHILD NOTE

Imagine building a neighborhood of houses (the rooms) that all need to plug into one power grid (the hub). If every house invents its own plug, nothing connects. The new rule: one plug shape for every house. Each house also has a second rule: it must draw power from the grid, not keep its own private generator — so there's always one real power source, never two copies that can go out of sync. Room 02 is already wired this way. Room 01's plug shape is the question on the table.

## 👵 GRANDMA NOTE

When you're building a house with many rooms, you don't let every carpenter invent their own doorway size — you agree on one doorway, and every room uses it. And you never keep two copies of the important family papers: the room shows you the papers, but the originals stay in one safe place. That's what today's handshake is about: one doorway (the mounting convention) and one set of originals (the canonical Brain records) for every room in the hub.

## 🤖 NAYA NOTE

Hub composition doctrine (PROPOSED, director-directed, Naya 2's acceptance pending): hub shell ↔ rooms integrate through one loader contract — `load → ctx → NayaRooms.x(el, ctx)` — with `ctx` carrying projected canonical records plus errors; rooms never duplicate canonical content into private stores. Room 02 instance: `reports-loader.js` transport contract, `reports-adapter.js` parse, `window.NayaRooms.reports(el, ctx)` mount, six canonical daily reports Sep 27 → Oct 2, branch `naya4/room-02-reports-v2` (`bd6219c`/`ff23c33`), room registry id "reports" / route "/reports" / theme indigo. Room 01 side pending: source = INTELLIGENCE-TODAY-MASTER-DIRECTIVE-V1.md (v1.0.5) + PR #1328 head (v8.3 checkpoint `d34f53ad`, tag `today-v8.3-checkpoint`). Cousin family: SN-0114 (canonical placement — canonical sets grow by deliberate promotion), SN-0095/0096 (compose at consumer / composition root owns bridge), SN-0069 (interface ownership), SN-0065 (honest PARTIAL). Binding scope if accepted: every new room inherits the convention; rooms bind only to loader-produced ctx, never to canonical files directly. Not merged, not ratified — CANDIDATE only.

## ⚙️ MACHINE NOTE

{"sn": "SN-0214", "title": "One Hub-Mounting Convention: Rooms Project Canonical Records, Never Copies", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "HUB-COMPOSITION"], "cousins": ["SN-0065", "SN-0069", "SN-0095", "SN-0096", "SN-0114"], "evidence": {"board": ["#554 5960016699 ([NAYA-4 → NAYA-2] Room 01 + Room 02 backend-connection handshake, 2026-10-02 19:36:52Z)"], "room02": "branch naya4/room-02-reports-v2, commits bd6219c/ff23c33; HUB/app/js/rooms/reports-adapter.js (parse), reports-loader.js (ReportsLoader.loadDaily({from,to,base}) -> {reports,errors}); window.NayaRooms.reports(el, ctx) mount; 6 canonical daily reports Sep 27-Oct 2 at BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/...; registry id reports / route /reports / theme indigo", "room01": "INTELLIGENCE-TODAY-MASTER-DIRECTIVE-V1.md v1.0.5 + PR #1328 v8.3 checkpoint d34f53ad (tag today-v8.3-checkpoint) as source; loader shape = open question to Naya 2's lane"}, "status": "PROPOSAL — director-directed, Naya 2 acceptance pending; binds proposing lane's rooms only until accepted", "rule": "hub shell and rooms integrate through one mounting convention (loader -> ctx -> NayaRooms.x(el, ctx)); rooms project canonical Brain records and never duplicate canonical content into private stores; contract agreed before implementation, no shell changes or merges from the proposing lane"}
