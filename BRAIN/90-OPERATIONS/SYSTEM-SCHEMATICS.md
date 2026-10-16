# NayaPOWER — System Schematics

> **Peer review (2026-10-16, three cold readers):** R1 adapter-builder 7.5/10 · R2 return-loop builder 7.0/10 · R3 system-understanding 8.7/10.
> **Dock validation (2026-10-16, independent):** all four dock PRs NEED WORK — #2680 payload blocker fixed, re-validating; #2678 refresh + docs; #2679 doc fix; #2676 CI + evidence. Merge order: #2680→#2678→#2679→#2676.
> Known gaps are work-ordered as F1–F9 inside — not hidden. Self-score 9.4.


Intelligence travels a loop: capture → store → emit → distribute → bridge → render → apply → return → learn. This document is the complete engineering picture — every part, every wire, every remaining build, in order. A cold reader should be able to explain the system and pick up any single item knowing exactly what to build, where, and how to prove it.

  8wires specified
  3steps flowing
  4steps in the dock
  5steps missing
  4decisions open
  0/181functions on real data

## ① The Picture

Twelve steps, one path. Read left to right, top to bottom — the dashed line loops it back. Green flows today. Gold waits in the dock. Red isn't built. Purple needs Shawn's word.

*[Diagram: see the visual HTML edition — nayapower-schematics.html]*

## ② The Why

Six decisions that shaped the system. Everything below follows from these — a cold reader who absorbs this section understands why the parts are arranged the way they are.
1 · Private by default, shared by choice, collective by consent.

Identity is never shared; distilled wisdom flows to the collective. In the build this becomes: RLS authenticated-only, zero anon policies, anon reads locked by design. Feeds carry public/collective rows only; personal rows need an authenticated session (decision D1).
2 · One intelligence, many views, one identity.

Twelve rooms, one pipe. Every room resolves the same bridge object (window.NayaPowerRuntime) through the same envelope — per-room adapters, never per-room backends.
3 · The hub renders; it doesn't think.

No capture database in the hub, no intelligence produced browser-side. Capture belongs to the engine path; the hub invokes and displays. This is why the return loop (wire W7) is events, not writes to tables from the browser.
4 · GitHub is the skull: distribution + projection + the machine.

Three distinct jobs, one repo: feed files served as a CDN after merge, Smart Note projections committed as markdown, and the 31-workflow machine that runs the team. The lane app is the machine's hands, not the product door.
5 · Wisdom flows like water.

Emitters push on schedule or on change; rooms never query the database directly. The hub reads feed files through the bridge — graded fallback: live feed → localStorage → honest "not verified" copy. Never fixtures presented as real.
6 · Prove it in use.

Nothing is declared live because it was built. Green in this document means measured evidence. The finish line is the 12-step proof run repeatedly — capture → receipt → cold retrieve → apply → verify → learn → successor reuse.

## ③ The Parts

Every component that makes the system run — where it lives (exact path), what it does, and its honest status. Evidence, not claims.

| # | Part | Lives at | Does what | Status |
|---|---|---|---|---|


**Supabase — the system of record · project dahisasgpfvziswqvmvm**

| P1 | nayanet_intelligent_blocks | Supabase · 191 rows | Canonical Smart Note blocks; columns verified via OpenAPI | live |

| P2 | nayanet_intelligence_index | Supabase | Cross-table index of intelligence objects | live |

| P3 | nayanet_smart_ledger | Supabase · 381 rows | Execution receipts, last-100 window per feed | live |

| P4 | members | Supabase · 7,472 rows | Relationship graph (id + display_name exposed) | live |

| P5 | smart_note_artifacts | Supabase · 108 rows | Note artifacts (cards, renders) | live |

| P6 | smart_note_events | Supabase | Return-loop target: room actions land here | table exists · unwritten |

| P7 | smart_note_receipts | Supabase | Capture receipts | live |

| P8 | v7_smart_note_transactions | Supabase · 27 rows Oct 7–10 | Single-transaction authority grants | live |

| P9 | 14 further tables | Supabase · 12,026 rows / 22 tables total | Authority, retrieval, learning, receipt, successor domains | live |

| P10 | RPC v7_create_smart_note | Supabase | Canonical capture entrypoint | live |

| P11 | RPC verify_smart_note | Supabase | Note verification | live |

| P12 | RPC nayanet_record_ledger_event | Supabase | Ledger event recording | live |

| P13 | Edge fn v7-smart-note-canonical | Supabase functions | Canonical receiver for captures | live |

| P14 | Edge fn nayanet-github-dispatch | Supabase functions | Fail-closed, idempotent projection to repo | live |


**GitHub — distribution + projection + the machine · SoulSchoolAcademy/NayaPOWER**

| P15 | nayanet-agent-capture.yml | .github/workflows/ | Capture workflow — dispatch-only today, no schedule | needs pump |

| P16 | PR #2680 — hourly pump | open · mergeable | Adds the schedule trigger to P15 | in the dock |

| P17 | emit_hub_feeds.py | PR #2678 | Reads Supabase → writes HUB/FEEDS/*.json | in the dock · 3/12 feeds |

| P18 | HUB/FEEDS/*.json | repo → raw.githubusercontent.com | Public feed files; the CDN layer | 3 live after merge |

| P19 | IB-######/smart-note.md | repo | Projection target for dispatched notes | wired |

| P20 | PR #2676 — feed notes | open · mergeable | Canonical 9-note Smart Feed source | in the dock |

| P21 | PR #2679 — bridge | open · mergeable | window.NayaPowerRuntime, 38 accessors, harness 23/23 | in the dock |

| P22 | nayapower-lane-agent app | GitHub App · installed | Lane-attributed writes, PRs, pushes — verified end to end | live |

| P23 | 31 workflows | .github/workflows/ | The team's machine: CI, capture, dispatch | live |

| P24 | Board #2641 | repo issues | Team coordination + receipts | live |


**Hub — the face · 12 room files**

| P25 | index-2.html — Smart Feed | ~/workspace/user/files/ → /hub/ | Seed: OFFICIAL_NOTES :2811 · seam :2395-2440 | on seeds |

| P26 | today.html · lists.html · spaces.html | room files → /hub/* | Feeds in #2678; adapters unwritten | feed in dock |

| P27 | reports.html · library.html · ledger.html · mail.html · connections.html · identity.html · index.html · start.html | room files → /hub/* | On seeds; connections serves old version live; settings 404 | on seeds |

| P28 | Bridge runtime | PR #2679 | window.NayaPowerRuntime — the one pipe | in the dock |

| P29 | 12 adapter swaps | per room file | Seeds → bridge loaders; specs drafted file:line | specced · unbuilt |

| P30 | Hub authenticated session | unbuilt | Access-token reads for personal rows (after D1) | needs D1 |


**Return path — the second half**

| P31 | Return loop | unbuilt | Room actions → smart_note_events (P6) | not built |

| P32 | Learn loop | unbuilt · blocked on P31 | Engine compounds events into intelligence | blocked |

## ④ The Rooms — every function, honestly

Fourteen surfaces, ~181 functions enumerated from the code. The headline: 0 work with real server data. localStorage is the entire backend. The write path is UI-complete but backend-absent — every save/like/rate/comment/share/pin/post/chat/send handler is coded against localStorage, in-memory, or nowhere. Expand any room for its full function table.
| Room | Functions | Real data | Seed-fed | Local-only | Dead / missing |
|---|---|---|---|---|---|

| --- | --- | --- | --- | --- | --- |

| 1. Smart Feed | 18 | 0% | ~22% | ~50% | ~11% (+2 partial) |

| 2. Settings | 4 sections | 0% | 0% (static copy) | 0% | 100% (no controls at all) |

| 3. Connect door board | 12 rows | 0% | n/a (registry mirror) | 0% | 100% (toast-only / badge-only) |

| 4. Today | 13 | 0% | 62% | 38% | 3 sections not coded |

| 5. Lists | 13 | 0% | ~100% content | ~90% bookkeeping | 0% |

| 6. Spaces | 23 | 0% | ~15% theater | ~85% local | 2 functional bugs + header bug |

| 7. Mail | 16 | 6% (voice dictation only) | 81% | — | 13% toast-pretending |

| 8. Reports | 11 | 0% | 73% | 27% action-real | 0% |

| 9. Ledger | 12 rows | 0% | ~100% | 0% | 2 features absent |

| 10. Library | 14 rows | ~15% local | ~75% | — | ~10% dead code |

| 11. Connections | 12 rows | 0% | ~70% | — | ~30% |

| 12. Hub Home | 6 | external links real | 0% | nav works | auto-login first-timer dead |

| 13. Identity | 6 | 0% | 0% | device flow works | theater (fake key, fake badge) |

| 14. Get Started | 9 rows | steps 1–2 real links | 0% | rail animates | 4 dead CTAs |

1 · No bridge traffic exists.

Most rooms don't reference `NayaPowerRuntime` at all — the integration isn't stubbed, it's absent. The one file with the full bridge contract (`index-2.html`) has no provider and its feed never calls `R.roomData('feed')` anyway.
2 · localStorage is the entire backend.

~20 keys across rooms hold lists, tabs, pins, spaces, posts, chat, contacts, notes, send-copies, activity. It works on one device and is invisible to the system.
3 · Honesty is mixed.

Some rooms label themselves honestly ("SIMULATED LIVE", "No backend space is being claimed", "Notes stay on this device"). Others mislead: ledger's "Every beat verified. Every action recorded." footer over randomly generated beats; identity's permanent "Security Key Configured" badge; mail's privacy slogan while rendering full bodies.
4 · Dead code and dead links are scattered:

library's tab editor (fully coded, zero callers), connections' add-contact (defined, no button), spaces' `smartmail-v1.2.html` (doesn't exist), today's `yourinteltoday.html` (wrong filename), spaces' orphaned seed ids, lists' untraced tab sort.
5 · The write path is UI-complete but backend-absent.

Save/favorite/like/rate/comment/share/pin/post/chat/invite/compose/send/schedule are all coded — against localStorage, in-memory, or nowhere. When the return loop (wire W7) is specified, these handlers are the exact call sites to repoint: `nayanet-board-actions-v1`, `boardId:contributions`, `naya.spaces.posts.v1`, `naya.spaces.chat.v1`, `naya.smartmail.sent`, `naya.library.blocks.v3`, `naya.connections.notes`, `naya.spaces.pins.v1`.

### 1. Smart Feed
Real backend data: 0/18 (0%).
Device-local functional (works on this device, no backend): ~9 — voice ×2, share ×2, powercasts link, favorite/save/love/like/rate/tabs/activity-search.
Seed-fed content: 4 — cards, layers, lens content, tab topics.
Dead/partial by design: 2 — Ask Naya → always not_verified toast; Create Space → intent recorded, toast admits no space is claimed.
Biggest gap: the entire feed renders a hardcoded baked-in snapshot and the governed runtime pipe resolves to not_verified — no live data path exists anywhere in the feed. Write-only hole: Add Intel contributions are stored but never read back.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Ask Naya / Search ("Search your intelligence…") | Feed top, full-width searchWrap (§3630) | yes (§3637 keydown → R.search) | none — R.search (§2452) goes to bridge, always not_verified | bridge method (searchIntelligence/askNaya) — unresolved, no provider | no | a runtime provider exposing searchIntelligence |
| Lens switch (Collective / Personal / Activity) | Lens tabs above feed (§4158–4178) | yes (router navigate) | Collective: hardcoded OFFICIAL_NOTES+NOTES (§2811–2812); Personal: n.personal filter → always empty; Activity: localStorage + hardcoded showcase (§4320) | nowhere (router-only) | no | real feed per lens from runtime |
| Smart Tabs topic filter | Smart Tab strip under lenses (§3665+, §4189–4199) | yes (snPill → activeSmartTab, §3831) | topic list derived from seed notes' topics; active tab in module var | nowhere | no | topics from live intelligence |
| Add Tab (＋ Add) | Right end of Smart Tab strip (§3866) | yes (openTabEditor(null, true, …), §3869) | localStorage nayanet.feed.smartTabs.v1 (§3654–3660) | localStorage only | no (device-only by design) | nothing functional; sync across devices needs backend |
| Tab ⋯ menu (Edit / Heart / Star / Remove) | ⋯ on each smart tab (§3847) | yes (openTabMenu → tabMenuAction, §3746–3797) | localStorage same key | localStorage only | no (device-only) | nothing functional |
| Note card render | Main stream, one card per note (§4414 intelBoard) | yes (full builder §4414–4520) | hardcoded NOTES (§2812) | nowhere | no | runtime feed via R.roomData('feed',…) |
| Layer expand/collapse | Per note card, layer headers (§4463) | yes (lh click toggles lb.hidden) | hardcoded layer bodies | nowhere | no | live layer content |
| Layer play (▶ per layer) | Play button in each layer head (§4466) | yes → window.NayaVoice.play (§4471–4494) | seed layer body text | device speechSynthesis | partial — device TTS works, not a governed voice | governed voice / server audio |
| ▶ Naya Voice (read whole note) | Top-right board actions (§3224–3251) | yes (full handler) | board DOM textContent (seed text) | device speechSynthesis | partial — device TTS works | governed voice |
| Create Space (from a note) | Top-right board actions (§3253–3259) | partial — records intent only | localStorage flag + toast; "No backend space is being claimed" | localStorage + ActivityLog | no | spaces backend / room creation |
| Favorite | Top-right board actions (§3272–3283) | yes (toggle + ActivityLog.log) | localStorage nayanet-board-actions-v1 | localStorage only | no (device-only) | backend persistence / sync |
| Save | Top-right board actions (§3272–3283) | yes (toggle, also writes naya.smartlist) | localStorage nayanet-board-actions-v1 + naya.smartlist | localStorage only | no (device-only) | backend persistence / sync |
| Love / Like | Bottom action bar (§3308–3358) | yes (toggle + device-local count badge) | localStorage count keys | localStorage only | no (device-only) | backend counts |
| 5-star rating | Bottom action bar, center (§3362–3398) | yes (stars → boardId:rate) | localStorage | localStorage only | no (device-only) | backend ratings |
| Share Intel | Bottom action bar, right — collective lens only (§3400–3416) | yes (navigator.share → clipboard fallback) | shares location.href (generic, no per-note deep link) | device share sheet / clipboard | partial — share sheet opens but only shares the generic page URL | per-note deep links / share backend |
| Add Intel (comment input) | Under each card (§3418–3444) | partial — writes, never re-renders | localStorage boardId:contributions | localStorage only | no | backend; contributions are write-only (never displayed) |
| Activity search | Activity lens search box (§4295) | yes (input → renderGroups) | localStorage naya.activity (user timeline only) | localStorage only | no for showcase | backend activity; only filters the user timeline, not the static showcase |
| Global share FAB | Bottom-right floating ＋ (all surfaces, §4072–4090) | yes (navigator.share → clipboard fallback) | location.href | device share sheet / clipboard | partial — works device-level | per-content deep links |
| Powercasts | Top-bar 🎧 button (§3612) | yes — external anchor | hardcoded URL https://powercasts.nayapower.workers.dev/ | external site | yes (real link) | nothing functional |

### 2. Settings
Interactive controls: 0/4 (0%) — there are no settings to actually set.
Informational-static: 4/4. No seed data (purely descriptive copy), no dead buttons (no buttons at all), no localStorage, no bridge calls.
Biggest gap: the Settings room is a display board with no settings — every labeled category is a text tile with no control behind it.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Identity / Privacy / Connections / Notifications / Appearance | "Your Hub, your rules" board — category tiles (§5371–5377) | no — descriptive text only, zero controls | static HTML strings | nowhere | n/a | actual controls (toggles/fields) for each category |
| Ownership ("Private by default · shared by choice · collective by consent") | "Your intelligence" board (§5379–5384) | no — static metrics/paragraph | static strings | nowhere | n/a | everything |
| Doors inventory ("Your doors", X of Y live) | Doors board (§5386–5394) | no — static list render | bundled R.DOORS mirror array (§2289), not the fetched registry | nowhere | no — mirror only | wire to loaded registry + real door states |
| About this Hub | "About this Hub" board (§5396–5400) | no — static paragraph | static string | nowhere | n/a | nothing (informational) |

### 3. Smart Connect door board
Real connections: 0/9 (0%). 2 live doors = badge-only (no action); 7 contract doors = toast-only buttons.
Biggest gap: the door board is a registry *viewer* with an honest no-op action layer — every "connect" pathway ends in a toast; nothing crosses any actual door.
Honesty note: framing is explicit and consistent (registry "SHOWING BUNDLED MIRROR AS NOT VERIFIED") — the gap is capability, not deception.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| AI Connect door | Door grid, position 1 | partial — rendered only, "IN USE" badge, no button (§3061–3065) | bundled DOORS mirror (§2293) | nowhere | no | actual connection status + handshake |
| Supabase / Data Connect door | Door grid, position 2 | partial — rendered only, "IN USE" badge, no button | bundled DOORS mirror (§2296) | nowhere | no | real data-substrate connection |
| GitHub Connect door | Door grid, position 3 | partial — "Contract" button → R.connectDoor → toast (§5339–5346) | bundled DOORS mirror (§2300) | toast-only (message logic, no network) | no | GitHub OAuth / App handshake + backend |
| MCP Connect door | Door grid, position 4 | partial — "Contract" button → toast | bundled DOORS mirror (§2304) | toast-only | no | MCP session negotiation |
| Naya-to-Naya Connect door | Door grid, position 5 | partial — "Contract" button → toast | bundled DOORS mirror (§2308) | toast-only | no | seat-to-seat protocol |
| Email Connect door | Door grid, position 6 | partial — "Contract" button → toast | bundled DOORS mirror (§2312) | toast-only | no | email adapter credentials + backend |
| Calendar Connect door | Door grid, position 7 | partial — "Contract" button → toast | bundled DOORS mirror (§2316) | toast-only | no | calendar OAuth + backend |
| Voice Connect door | Door grid, position 8 | partial — "Contract" button → toast | bundled DOORS mirror (§2320) | toast-only | no | voice pipeline backend |
| Web Connect door | Door grid, position 9 | partial — "Contract" button → toast | bundled DOORS mirror (§2324) | toast-only | no | web adapter backend |
| Registry status line ("CANONICAL REGISTRY LOADED" / "NOT VERIFIED") | Above door grid (§5342–5352) | yes (loadRegistry) | fetch(../../BRAIN/…registry…json); falls back to bundled mirror on failure | file fetch (fails in deployment → mirror) | no | served registry file + runtime verification |
| Roadmap horizon list | Below grid (§5322–5329) | no — static render | R.DOOR_ROADMAP hardcoded ideas (§2337) | nowhere | n/a | nothing (informational by design) |
| The Door Law | Below roadmap (§5330–5339) | no — static copy | static strings | nowhere | n/a | nothing (informational by design) |

### 4. Your Intelligence Today
Real-data: 0/13 (0%). Seed-fed: 8/13 (62%) — every data-bearing surface renders window.__fixtures.
Client-side-only but functional: 5/13 (38%) — save/remove (localStorage bookmarks), share (Web Share/clipboard), modal close, drawer toggles, drawer nav (mis-wired).
Dead/not coded: 3 sections (WATCH, WAITING, LEARNED) + zero bridge references anywhere.
Biggest gap: the entire data layer is missing — NayaRoomKit.load unconditionally serves 12 hardcoded fixtures, and there is zero code (no fetch, no bridge call, no Supabase reference) connecting this room to nayanet_intelligent_blocks via today(). Everything else is plumbing with no engine behind it.
Coverage note: NayaRooms.feed (also in this file) sampled only — it is not rendered by this page's entry point.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Room data load | on room mount (TodayRoom) | yes — stubbed | window.__fixtures (L1651, 12 hardcoded notes) | nowhere; no fetch/Supabase/bridge | no | Implement load to call today() bridge → nayanet_intelligent_blocks (191 rows) |
| Orient header (time-of-day greeting + play/saved counts) | top of stage, above tabs | yes | system clock + fixture count | nowhere | no | real counts from backend |
| Time tabs: TODAY / YESTERDAY / LAST WEEK | tab row under orient | yes | fixture period field ('today'/'yesterday'/'week') | fixture array | no | real per-period query; tab labels currently slice the same 12 seeds |
| Search filter | search bar under tabs | yes | substring match on fixture title+nutshell | fixture array | no | backend search — NayaRuntime.search is an async stub |
| NOW board (ranked highlight cards) | NOW section ("plays-river") | yes | fixtures filtered by tab + search | nowhere | no | real ranked highlights; currently max 6/3/3 seeds per tab |
| SAVE (bookmark play) | each card's action row | yes | localStorage nayanet.today.smartlist.v1 (L2090–2094); array of fixture IDs | localStorage only | local-only | Supabase-backed smart list; cross-device sync; only fixture IDs stored |
| SHARE | each card's action row | yes | builds URL location.origin+pathname+'#/today/'+p.id | Web Share API / clipboard fallback | client-side yes | deep-link #/today/ is never parsed on load — the link just reloads the same fixture page |
| VIEW FULL NOTE | each card's action row ("VIEW FULL NOTE" — card body itself is not clickable) | yes | fixture layers (nutshell/human/child/grandma/naya/machine/learning/means/value) | fixture array | no | real note content from nayanet_intelligent_blocks |
| Note modal close | modal × button, overlay click, Escape key | yes | n/a (UI only) | DOM only | yes (UI-only) | — |
| Smart List (REMEMBER) + Remove | REMEMBER section (only renders when list non-empty) | yes | localStorage key above + fixture titles resolved via allPlays.find | localStorage only | local-only | same as SAVE; orphaned IDs (fixtures gone) silently dropped |
| Drawer room navigation | left drawer, per-room buttons | partial | ROOM_FILES (L2618) | location.href | local-only | The entire ROOM_FILES map is stale — not just today: feed:'index.html', today:'yourinteltoday.html', reports:'reports.html', library:'index.html#/hub/library', connect:'smartconnect.html', ledger:'smartledger.html', connections:'yourconnections.html', lists:'smartlists.html', mail:'smartmail.html', spaces:'smartspaces.html', settings:'index.html#/hub/settings' — nearly every entry points to a wrong or nonexistent filename (independently verified 2026-10-16) |
| Drawer toggles / backdrop click / Escape | hub chrome (corner buttons) | yes | n/a (UI only) | DOM only | yes (UI-only) | — |
| Not-verified fallback panel | HubView fallback (only when a room has no renderer) | yes — not used on this route | stub NOT_VERIFIED_COPY | nowhere (its one action calls stubbed NayaRouter.navigate = console.log) | no | real runtime + router for rooms that hit this path |

### 5. Smart Lists
Real server data: 0%. Seed-fed for content: ~100% (the corpus is a baked-in 205KB fixture).
UI controls functionally coded: ~90% — the local bookkeeping layer (create/rename/delete/heart/star/save/filter/search) genuinely works against localStorage.
Biggest gap: there is no code path that calls the lists() bridge method or reads HUB/FEEDS/lists.json — the entire note corpus is RAW (L1368).

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| + NEW LIST (create custom list) | Header button, top-right | yes — openNewListModal() (~L1331) | localStorage naya.smartlist | localStorage-only | partial (list names persist; note membership is note-ids from fixture) | Feed from lists() bridge + Supabase table |
| Search notes | Toolbar search box | yes — input handler (L580) | RAW fixture parsed by parseNote | nowhere | no — searches fixture notes only | Bridge feed + server search |
| Category tab pills (filter) | SmartTabs ribbon, click pill | yes — snPill()/go() (L849) | categories derived from RAW paths | nowhere | no | Bridge-provided taxonomy |
| Tab ⋯ menu: Edit / 💜 / ⭐ / Remove | Ribbon pill "⋯" or right-click | yes — openTabMenu()/tabMenuAction() (L842–975) | localStorage naya.smartlist | localStorage-only | yes (local prefs) | nothing for local use; sync needs backend |
| ＋ Add tab pill (create tab) | Ribbon end | yes — openTabEditor(null, true) (L787) | localStorage | localStorage-only | yes (local) | Backend sync |
| Restore hidden tabs | Tab editor "HIDDEN — TAP TO RESTORE" | yes (L1004) | localStorage hiddenTabs | localStorage-only | yes (local) | Backend sync |
| Custom list pills (view list) | Ribbon, left of category tabs | yes — listPill() (L871) | localStorage store.custom (note-id arrays) | localStorage-only | partial (membership real locally; notes are fixture) | Bridge feeds |
| Custom list ⋯ menu: Rename / 💜 / ⭐ / Remove | Custom list pill "⋯" or right-click | yes — openListMenu()/openListEditor() (L883–938) | localStorage | localStorage-only | yes (local) | Backend sync |
| × CLEAR (clear filter) | Toolbar | yes (L588) | none | nowhere | n/a | — |
| Note card → View full note | Card click / VIEW FULL NOTE button | yes — openNoteModal() (L1261) | RAW fixture body | nowhere | no — note body is fixture markdown | Bridge note detail |
| SAVE TO LIST (add/remove note) | Card + modal button | yes — openPickerModal() (L1284), incl. inline "CREATE + SAVE" | localStorage store.custom | localStorage-only | partial (local bookkeeping works; notes are fixture) | Real note ids from bridge |
| SAVED FROM TODAY tab | Ribbon pill (appears when Today saves exist) | yes — resolveToday() (L1124); unknown ids get an honest "Saved from Today" placeholder, never invented titles | localStorage nayanet.today.smartlist.v1 (read-only) | localStorage-only | partial | Today room must actually write note ids |
| Truth-state pill (RATIFIED/CANDIDATE) | Note card header | yes — display only (truthClass, L1114) | parsed from fixture Truth state: | nowhere | no | Bridge-provided truth state |

### 6. Smart Spaces
Real server data: 0%.
Coded and genuinely working local-first: ~85% — create/join/invite/pin/unpin/post/like/chat/voice/contacts/schedule-picker all function against localStorage.
Seed-fed theater or broken: ~15% — likes/comments on pinned blocks lost on reload; "✉ Mail Space" navigates to non-existent smartmail-v1.2.html; post/member "Message" buttons are toast-only with no navigation; "💬 Message Space" broadcasts to no one; scheduled posts never fire.
Biggest gap: the pin like/comment persistence hole + the dead smartmail-v1.2.html link are the two functional bugs; the missing piece is the spaces() bridge feed + a real transport for posts/chat/invites.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Smart Tabs filter (All / My Spaces / topics) | Discovery tab ribbon | yes — renderSnTabs() (L1118); persists to naya.spaces.tabs.v1 | SEED_SPACES + custom | localStorage-only | no (seed spaces) | spaces() bridge feed |
| Search spaces | Discovery toolbar | yes (L1312) | effectiveSpaces() | nowhere | no | Bridge search |
| ＋ Create Space | Discovery toolbar button | yes — openCreateModal() (L1998: name/topic/desc/privacy/color) | writes naya.spaces.custom.v1, auto-joins | localStorage-only | yes (local user spaces work) | Server persistence + real members |
| Space card → open detail | Card click | yes (L1405) | effectiveSpaces() | nowhere | no | — |
| Join / Leave space | Card + detail buttons | yes — naya.spaces.mine.v1 (L1438, L1485) | localStorage | localStorage-only | yes (local) | Real membership service |
| Invited-for-you join | Marquee strip on discovery | yes (L1337 + delegated L1353) | SEED_SPACES official | localStorage-only | no | Real invites |
| ✉ Invite | Detail header button | yes — openInviteModal() (L2081); adds memberIds to custom space or naya.spaces.memberov.v1 override for seed spaces | naya.people.registry (seeded) | localStorage-only | no (fake people) | Real identity/contact service |
| 💬 Message Space (broadcast) | Detail header button | yes — broadcastToSpace(s,'message') (L1641): appends a "broadcast" message to the *local* chat log | naya.spaces.chat.v1 | localStorage-only | no — simulated broadcast, no member is reached | Real messaging transport |
| ✉ Mail Space | Detail header button | partial / bug — writes naya.mail.compose.request then location.href='smartmail-v1.2.html' | localStorage | nowhere — smartmail-v1.2.html does not exist; the real mail room is mail.html | no | Point at real mail room / real compose |
| ＋ Pin Intelligent Block | Posts tab | yes — openBlockPicker() (L1608) lists SEED_BLOCKS; pins stored in naya.spaces.pins.v1 | SEED_BLOCKS fixture | localStorage-only | no | Bridge intelligent-block feed |
| ♥ Like pinned block | Pinned card | partial — session-only illusion: mutates b.likes on the in-memory seed object, but savePins() persists only pin *ids* — likes are lost on reload | in-memory seed | nowhere | no | Persist likes server-side |
| Comment on pinned block | Pinned card "Send" | partial — same hole — doComment() (L1594) pushes to seed-object comments, never persisted | in-memory seed | nowhere | no | Persist comments server-side |
| ↗ Share pinned block | Pinned card | yes (L1566) — clipboard copy + toast | clipboard | nowhere | n/a (device clipboard works) | — |
| Unpin | Pinned card | yes — unpinBlock() (L1574) | naya.spaces.pins.v1 | localStorage-only | yes (local) | Backend sync |
| Post to space (composer) | Posts tab textarea + Post button | yes — addPost() → naya.spaces.posts.v1 (L1675) | localStorage | localStorage-only | yes (local posts work) | Server feed + real audience |
| 🕐 Schedule post | Composer schedule picker | partial — openSchedulePicker() (L2128) stores {freq,label,date,time} on the post and renders a badge; nothing ever publishes on schedule | localStorage | nowhere | no | Scheduler / publish job |
| ♥ Like post | Post card | yes — toggleLike() → saveJSON(LS_POSTS) (L1057) | localStorage | localStorage-only | yes (local) | Backend |
| ✉ Message (post author / member) | Post card, member row | toast-only dead end — writes naya.mail.compose.request + toast (L1726, L1772) but never navigates | localStorage key | nowhere | no | Wire to mail room |
| Chat send | Chat tab input + Send | yes — doSend() → naya.spaces.chat.v1 (L1884) | localStorage | localStorage-only | yes (local chat works) | Real realtime transport |
| 🎤 Voice message | Chat tab mic button | yes — toggleRecording() (L1817, MediaRecorder → dataURL in chat msg); honest "stored on this device only" note | localStorage (dataURL — size caveat) | localStorage-only | partial (works on-device) | Server audio storage |
| ＋ Save as Contact | Members tab | yes — savePerson() → naya.people.registry (L1759) | localStorage | localStorage-only | yes (local) | Real connections service |
| Detail tabs: Posts / Members / Chat / About | Detail tab bar | yes (L1512) | mixed seeds + local | localStorage-only | mixed | — |
| 🔌 Connect door CTA | About tab, sp-door-* spaces only | yes — window.NayaGate.require() → connect.html (L1937); honestly gated, not faked | naya.connection.v1 | localStorage + page nav | yes (gating logic works) | Live door connections behind it |

### 7. Smart Mail
Real: 1/16 (6%) — voice dictation is the only feature that touches a real data path (browser speech API).
Seed-fed with working UI: 13/16 (81%) — folders, list, search, filters, thread view, compose UI, QA panels, shortcuts, cross-room handoff all fully coded over hardcoded demo data.
Toast-pretending: 2/16 (13%) — Send and Schedule have complete handlers with success toasts but nothing ever leaves the browser.
Dead buttons: 0 — every button has a handler; no star/archive feature exists at all (no such UI).
Biggest gap: no message store and not even a bridge stub — zero fetch(/bridge calls in the whole file. The privacy doctrine (snippets-only, shareable-to-hub-only) is enforced nowhere: the read pane renders full bodies, search indexes full bodies, and the only "privacy" is a static drawer slogan.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Folder navigation (INBOX / UNREAD / SENT / SCHEDULED / SMART POSTS / DRAFTS) | Left rail folder buttons | yes — renderRail (L836), click ~L861 | THREADS seed const (L2005, all demo:true) | in-memory array only | no | A real message store (Supabase/GitHub) behind MailAdapter |
| Thread list + search | Middle column; "Search mail…" input | yes — renderList (L994), input handler (L1005) | Filters THREADS seed in-memory (matches subject/body/from, L1041) | in-memory | no | Real corpus to search |
| Filter chips (ALL / WITH NOTES / UNREAD) + bulk SELECT toggle | Above thread list | yes — chip handler ~L1017, SELECT toggle ~L1010 | In-memory filter of seed threads | in-memory | no | Real data |
| Bulk MARK READ / DELETE | Bulk action bar (visible when selecting) | partial — bulkMarkRead (L1140), bulkDelete (L1147) | Read flag = in-memory only; delete splices the hardcoded THREADS array (lost on reload) | in-memory + toast; persistSent() on delete only | no | Persist read flags; delete against real store |
| Thread view (select + read pane) | Right reading pane | yes — selectThread (L1130), renderRead (L1185) | Thread from THREADS seed; unread=false set in-memory only (L1135, never persisted) | in-memory | no | Real message fetch + durable read state |
| Snippet vs. full body | List rows show snippet (L1104); read pane shows full body (L1234–1251) | yes — snippet-only doctrine not enforced | Seed bodies | in-memory | no | Enforce snippets-only; add shareable-to-hub gating (none exists — only a static drawer slogan at L2079–2080) |
| Reply | REPLY button in reading pane | partial — handler L1255 | Opens composer prefilled Re:; no threading, no send | composer UI only | no | Real reply threading + delivery |
| MARK UNREAD | Ghost button in reading pane | partial — handler L1260 | In-memory flag flip, no persistence | in-memory | no | Durable state |
| ADD TO CONNECTIONS | Reading pane, when sender unknown to registry | partial — handler L1267 | window.NayaPeople registry → localStorage naya.people.registry, seeded from CONTACTS const via ensureSeeded (L654) | localStorage only | partial (local only) | Real identity graph |
| Compose — COMPOSE + 3 modes (INBOX / INSTANT / SMART POST) | Top +COMPOSE button; modal with mode tabs | yes — openCompose (L1285), syncModeUI (L1743), post preview updatePreview (L1759) | Recipients: CONTACTS/SPACES seeds; recents: ml-recents localStorage; attach: SMART_NOTES sample const (L1964–2002, vision samples) | localStorage + seeds | no | Real contacts, lists, notes sources |
| Voice dictation (mic) | Composer body toolbar | partial — setMicUI/rec (L1472, L1501) | Browser Web Speech API | browser API, nowhere else | yes (where API exists) | None — only client feature that's genuinely real |
| Send | SEND NOW button | partial — send handler ~L1786 | Builds thread object, threads.unshift, persistSent → localStorage naya.smartmail.sent (L1939–1943, cap 50), toast "Sent to N recipients" (L1875) | localStorage only — room's own banner: "Nothing leaves the network" | no | Real delivery transport (mail / Space-feed write path) |
| Schedule for later + recurrence | Composer "Schedule for later" toggle; once/daily/weekly/monthly + time | partial — schedLink handler ~L1881, syncSchedUI (L1685), updateSchedSummary (L1733) | Thread with status:'scheduled' in localStorage; toast "Scheduled …" (L1873) | localStorage only | no | A scheduler — nothing ever fires a scheduled send |
| Save draft on cancel | Cancel button in composer | partial — handler ~L1891 | threads.unshift in-memory only — not persisted (label says "Your unsent work saves here"; it doesn't) | in-memory | no | Persist drafts to localStorage at minimum |
| Quick Access panels (CONTACTS / SMART LISTS / SPACES) | Rail "QUICK ACCESS" section | yes — openQaPanel (L891) | Renders CONTACTS seed; lists always empty (CONTACT_LISTS undefined); SPACES seed — read-only rows, zero actions | renders only | no | Real data + actions (add/remove) |
| Keyboard shortcuts (c / ↑↓ / Esc) + cross-room compose handoff | Global | yes — keydown handler ~L1118; handoff via localStorage naya.mail.compose.request (L2008, 10-min TTL, consumed once) | localStorage handoff; in-memory shortcuts | localStorage | partial (local glue works) | A real producer of compose requests |

### 8. Your Reports
Real data: 0/11 (0%).
Action-real-but-seed-content: 3/11 (27%) — copy link, MD download, copy prompt genuinely work as client features; what they copy/download is the hardcoded seed.
Seed-fed: 8/11 (73%) — tabs, search, week navigation, cards, full board, scorecard dials, threads, navigation all fully coded over the hardcoded RAW_MD corpus.
Dead buttons: 0.
Biggest gap: no report source at all — the room's entire "brain memory" is a const on line 1720. The fixture fallback (SAMPLE_REPORTS) and the "Adapter output wins" comment show the seam was designed, but no adapter input is ever provided and no bridge call exists. Scores on the scorecard dials are distilled from prose, not computed from evidence.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Period tabs (DAILY / WEEKLY / MONTHLY / YEARLY) | Top tab bar | yes — periodTabs (L1291) | ALL_REPORTS from RAW_MD seed (L1720) parsed in-memory | in-memory | no | Query v7_intelligence_reports by period via bridge |
| Search with highlight | Search bar under tabs | yes — searchBar (L1304), hl (L999) | Searches parsed seed reports in-memory | in-memory | no | Real corpus |
| Week strip / week rail / day board navigation | "THIS WEEK" section + day chips | yes — weekStrip (L1108), weekRail (L1522), goDay (L1517), dayBoard (L1125) | Derived from seed daily reports (newestKey/weekOf) | in-memory | no | Real report-date calendar |
| Report cards | List view cards | yes — reportCard (L1349) | Seed reports; footer shows IB id + word count + section count | in-memory | no | Real data |
| Read the report (full board) | "READ THE REPORT →" button → full board | yes — fullReport (L1578) | Seed markdown distilled into sections (hero, big picture, nutshell, points, scorecard, prompt) | in-memory | no | Real canonical report record + evidence |
| Scorecard dials | Inside full board, SCORECARD sections | yes — scorecardSection (L1456); scores distilled from markdown text by distillSection (L804) | Text-parsed numbers from the hardcoded markdown — no verified score source | in-memory | no | Scores computed from real evidence via the decision calculus |
| Cross-day THREADS links | Card "THREADS ·" term links | yes — threadsBlock (L1315), threadsFor (L992) | Hardcoded THREADS const (L1015) | nowhere (fixture) | no | Real cross-report term graph |
| Export: COPY LINK + ↓ MD download | Card footer | yes — exportRow (L1329) | Link = location.href + #report= + id (deep-link works, initialReport from hash L~1748); MD download re-serves the seed's raw markdown via blob | clipboard / local blob | partial (action real, content seed) | Real canonical report markdown (repo path in the seed's own record) |
| Copy prompt | Prompt blocks in full report | yes — promptSection (L1484) | Prompt distilled from seed markdown | clipboard | partial (action real, content seed) | Real report content |
| Keep reading / back navigation | Full board ("← ALL … REPORTS", keep-reading nav) | yes — keepReading (L1545), back button (L1593) | In-memory navigation | in-memory | no | Real data |
| NEW badges | Card kicker | yes — isNew (L991) | localStorage naya_reports_last_visit timestamp | localStorage | partial (works as designed; dates are seed dates) | Real visit history keyed to real report dates |
| Filters by lane/seat, evidence links, time ranges | — | no — no such UI exists | — | — | — | Lane/seat filters, evidence-link rendering, range picker |

### 9. Smart Ledger (Living Intel room)
Real: 0% · Seed/demo-fed: ~100% · Dead (button with no handler): 0% — every coded function works, but every data item is a hardcoded or randomly generated demo beat (demo:true), including the hero "SIMULATED LIVE" banner and the misleading "Every beat verified. Every action recorded." footer.
Biggest gap: no code path reaches nayanet_smart_ledger — the 28 demo beats + 1–2 "realReceipts" (themselves demo-staging artifacts) stand in for 381 real rows; no bridge method ledger() is called anywhere.
Also missing: the lane/seat/action filtering and export that an accountability surface needs — they are absent, not partial.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Live hero stats (ITEMS FLOWING / SOURCES ALIVE / NEWEST) | Top hero section | yes (~770–790) | in-memory allItems array from PACKS | nowhere (computed locally) | no | real event counts from nayanet_smart_ledger via ledger() |
| Source jewel filter buttons (INTEL REPORTS / SMART NOTES / LEDGER / CONNECT) | Jewel row under hero | yes (~815) | hardcoded meta map + setFilter() | nowhere | no | nothing structural; just needs real item counts |
| Stream tabs ALL / INTEL / ACTIONS / CONNECTIONS | Tabs bar | yes (~856–880 setFilter) | FILTERS (~687) | nowhere | no | add lane / seat / action-kind / proof-state filters; none exist |
| Search ("Search the heartbeat — …") | Search bar under jewels | yes (~837, 180ms debounce) | filters in-memory items | nowhere | no | backend search over nayanet_smart_ledger |
| Event rows (stream cards) | Main stream | yes (cardNode ~903) | demo stream + parsed PACKS | nowhere | no | swap demoStream() for ledger() rows (381 rows exist) |
| Heartbeat inspect modal (proof/evidence detail) | Card click → modal | yes (openModal ~1077) | item object: Outcome, Q, ΔV, Confidence, Proof stat, spark/bar graph, explain text | nowhere | no | real receipt fields from nayanet_smart_ledger; "realReceipts" items are demo-staging artifacts, not production rows |
| Simulated-live ticker (new beat every 8s) | Stream top, auto-insert | yes (~1037–1052) | LedgerAdapter.demoBeat() random generator | nowhere | no | real event subscription; labeled honestly as SIMULATED LIVE today |
| Reset view button | Appears when filtered/searching | yes (~966) | clears state | nowhere | n/a (UI chrome) | none |
| Time-ago ticker (refreshes timestamps) | All [data-ts] nodes | yes (~1127, 30s interval) | item timestamps | nowhere | n/a (UI chrome) | none |
| Drawer nav (left/right panels, brand) | Header | yes (~1246–1310) | static | location.href='index.html' | n/a (UI chrome) | none |
| Search ledger by lane / seat / action | — | no | none | nowhere | no | entire feature: no per-event lane/seat/action fields rendered, no filter UI |
| Export ledger (CSV/JSON) | — | no | none | nowhere | no | entire feature: no export button exists |

### 10. Intelligent Library
Real: ~15% (pin/edit persistence, share, export work locally) · Seed-fed: ~75% (all 26 blocks are the static CANON_BLOCKS seed; edits persist only in this browser) · Dead: ~10% (tab editor/menu fully coded but un-wired; ref-count display permanently 0; naya.library.pins.v1 key defined but unused).
Biggest gap: no call to library() / nayanet_intelligent_blocks + nayanet_intelligence_index — the corpus is frozen at the 26-block seed, so search/tabs/provenance/ref-counts all operate on static content.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Category tabs (All 26 / Features / Smart Connect / The Ecosystem) | Tab row above grid | yes (renderSnTabs ~658) | hardcoded array in loadSnTabs() (~506) | nowhere | no | derive tabs/facets from nayanet_intelligence_index |
| Search blocks (debounced) | Toolbar search input | yes (~927–932) | in-memory blocks (title/summary/content/topics) | nowhere | no | search against nayanet_intelligent_blocks |
| Block cards grid + pin badges | Main grid | yes (renderBlocks ~702) | localStorage naya.library.blocks.v3 ← CANON_BLOCKS seed | localStorage only | partial (pins persist; corpus is seed) | corpus from nayanet_intelligent_blocks via library() |
| Block detail modal (what/why/how, layers, connections) | Card click | yes (openBlockDetail ~764) | block object from localStorage | nowhere | no | layer text + what/why/how from real block rows |
| Provenance display | Modal "Provenance" section + card meta row | yes (~827–835) | hardcoded provenance object per block | nowhere | no | real provenance from capture pipeline |
| Connected-area chips (jump to another block) | Modal "Connected areas" | yes (~806) | b.connections (empty in seeds — renders nothing today) | nowhere | no | real block-graph edges; connections array is always empty |
| Pin to Space picker | Modal "📌 Pin to Space" button → openPinPicker (~861) | yes | 9 hardcoded spaces; writes pinnedSpaces → localStorage naya.library.blocks.v3 | localStorage only | partial (persists locally) | real Space registry; note: pins live inside block objects, not the defined-but-unused naya.library.pins.v1 key (~455) |
| Share (copy to clipboard) | Modal "Share" button (~840) | yes | navigator.clipboard + showToast | clipboard only | n/a (works) | nothing functional |
| Export block (downloads .md) | Modal "Export" button → exportBlock (~892) | yes | block object → Blob download | nowhere (file download) | n/a (works) | nothing functional |
| "Read the full Intelligent Block →" CTA | Card body link | yes (~738) | b.feedUrl (hardcoded https://hub.nayapower.workers.dev/hub/#/hub/feed) | external URL | n/a (link) | none |
| Result count ("N blocks") | Toolbar | yes (renderBlocks) | filtered list length | nowhere | n/a (UI chrome) | none |
| Ref count ("Linked to N areas") | Modal provenance | partial (~833) | b.refCount — always 0, never incremented | nowhere | no | compute from real references in nayanet_intelligence_index |
| Custom tab creation / editing | — | no (dead code) | openSnTabMenu/openSnTabEditor never wired to any button | nowhere | no | wire the existing editor to a "+ tab" affordance and persist via saveSnTabs |
| Block creation (write a new Smart Note) | — | no | none | nowhere | no | entire feature: capture flow into nayanet_intelligent_blocks |

### 11. Your Connections
Real: 0% (from the intended members source) · Seed-fed: ~70% (5 hardcoded contacts; lists/notes persist in localStorage so the *mechanics* work locally) · Dead: ~30% — NayaPeople.add/promptName wired to nothing; strength/last-contact/search don't exist at all.
Biggest gap: zero connection to members — 7,472 rows exist and no code path calls connections(); the room can never show anyone beyond the 5 hardcoded seeds without the add-contact button being wired.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Relationship cards (avatar, name, role, list membership) | Contact grid | yes (card ~530) | NayaPeople.ensureSeeded ← hardcoded PACK → localStorage | localStorage only | no | rows from members (7,472) via connections() |
| Filter chips (All + lists, with counts) | Filter row | yes (renderFilters ~462, chip ~502) | localStorage naya.connections.lists | localStorage only | partial (lists persist locally) | real list/segment source |
| + New list | Filter row button | yes (~472–499 inline form) | user input → localStorage | localStorage only | partial (works locally) | sync lists to a real store |
| Detail modal (name, role, note) | Card click → openModal (~574) | yes | contact object | nowhere | no | real member profile fields |
| Save-to-list toggle | Modal "SAVE TO LIST" | yes (~601–605) | toggles membership → localStorage | localStorage only | partial (works locally) | real list membership |
| Notes about contact | Modal textarea + "SAVE NOTE" | yes (~610–624) | localStorage naya.connections.notes | localStorage only | partial (works locally, device-only by design) | opt-in sync if desired; honest as-is |
| Write mail (message action) | Modal "✉ WRITE MAIL" | partial (~588–593) | writes compose request → location.href='mail-preview.html' | localStorage handoff + navigation | no | Smart Mail room must consume naya.mail.compose.request |
| Empty state ("This list is empty…") | List view | yes (~522–526) | visible() result | nowhere | n/a (UI chrome) | none |
| Add contact | — | no (dead code) | NayaPeople.add + promptName defined, never wired | nowhere | no | add a button calling the existing functions |
| Connection strength | — | no | none | nowhere | no | entire feature: no strength data or UI |
| Last contact / recency | — | no | none | nowhere | no | entire feature: no timestamps tracked |
| Search contacts | — | no | none | nowhere | no | entire feature: no search box exists |

### 12. Hub Home
What works: Real navigation — 12 external links, name → identity handoff, and the welcome-back/alias-clear flow are all coded and functional on-device.
What's broken/dead: Auto-Login is silent-dead for first-timers (just an alert()); there is no health/status strip and no room drawer in this file — the shell nav is 12 external icons, not room links.
Biggest gap: HUB_APP_URL = 'hub/' (relative) is the deployment seam; the "one deployment seam" comment is the only integration thinking — no fetch, no server identity, no room nav.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Auto-Login button → checkAutoLogin() (~L1705, wired onclick ~L1278) | Header, "Auto-Login" | yes | localStorage key nayanet_smart_alias | nowhere (redirect only) | no | A first-timer path — it just alert()s ("No saved key found…"). Nothing for new users. |
| Name entry form submit (~L1740) | Hero, "Enter NayaNET →" + name field | yes | input value + sessionStorage.nayanet_user_name | navigates to identity.html?name=… | partial (real nav, device-only identity) | Server identity/account creation. |
| "Jump back in →" (welcomeBack IIFE ~L1869) | Welcome-back panel (returning visitors only) | yes | localStorage nayanet_smart_name/nayanet_smart_alias | redirects to hubEntryUrl() | partial | Works as a local bookmark; no credential verification. |
| "Use a different identity" (welcomeBack ~L1878) | Welcome-back panel | yes | none (deletes keys) | localStorage-only | no | Nothing missing — it does what it claims. |
| 12 eco-dot destination links (~L1177–L1280) | Inline nav, header | yes | hardcoded URLs | External sites (GroovePages, GrooveMember, academy, powercasts, etc.) | yes (real links, verified verbatim in markup) | None for nav; note: 5-Day Challenge & Academy both point to academy.nayanet.app (duplicate target). |
| Jewel positioning / color script | Decorative | yes | none | nowhere | n/a | — |

### 13. Smart Identity
What works: The full device-local flow works as designed — alias entry live-updates the 4 tiles, activation persists name/alias/random key and hands off to the hub with query params.
What's broken/dead: Everything behind the flow is device-local theater: random "vault key," unprovisioned Smart Link domain, a permanently-visible security badge, a dead hub-app.html guard, and a "Naya Player" button that isn't a player.
Biggest gap: No server-side identity — the key never leaves the device, so "auto-login" anywhere else is just reading another browser's localStorage; cross-device identity doesn't exist.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Alias input → updateSmartCredentials() (~L210) | "Type Your Custom Smart Alias" field | yes | input value, regex [a-z0-9] | 4 tiles in-page | no | Smart Link (alias.nayanet.app) is a claimed domain that is never provisioned; mail ID is a label. Nothing checks availability/resolves. |
| "Enter the Intelligent Hub →" → activateAndRedirect() (~L217) | Big CTA | yes | input + random nayanet_key_ string | localStorage x3, then redirect to hub/?name=…&alias=… | partial | The "key" is Math.random() — device-local, not a credential; the honesty-guard checking for 'hub-app.html' is dead code (HUB_APP_URL is 'hub/', never matches). |
| Greeting + daypart (daypart(), rawName from URL/session) | Card title | yes | URL param / sessionStorage / fallback "Pioneer" | nowhere | no | Fine as-is. |
| Brand logo click | Header | yes | none | nav to index.html | yes (real nav) | — |
| "🎧 Naya Player" button (~L111) | Header | yes (nav) | none | navigates to 'hub/' | no | Mislabeled — it's not a player, it just links to hub root. No player exists anywhere in the 3 entry files. |
| Status badge "Auto-Login Security Key Configured" | Above tiles | no (static HTML, always shown) | none | nowhere | no | Misleading — badge claims a configured security key before the user does anything; there's no real key. |

### 14. Get Started
What works: Steps 1–2 are genuinely functional (real external links to claude.ai and the NayaPOWER fork page); the completion-rail UI animates correctly per click.
What's broken/dead: Steps 3, 4, "Open Smart Doors," and the finale CTA are all self-anchors — the four most important actions on the page go nowhere. Step progress isn't persisted.
Biggest gap: The onboarding funnel ends at step 2 — steps 3–4 are placeholders dressed as CTAs; the page is a 4-step flow where half the steps are dead.

| Function | Where | Coded? | Data today | Talks to | Real? | Missing |
|---|---|---|---|---|---|---|
| Scroll-reveal (IntersectionObserver ~L243) | All sections | yes (cosmetic) | none | nowhere | n/a | — |
| Step-completion handler ([data-step] click ~L257) | Every step button | partial | none | in-page only (adds .is-done, rail ✓) | no | No persistence — progress isn't saved; refresh resets all four checkmarks. |
| Step 1 "Get Muse — free" | Step 1 action | yes | hardcoded URL | https://claude.ai (external) | yes (real link) | — |
| Step 1 alt "Skip ahead" | Step 1 | yes | none | #s2 anchor | yes | — |
| Step 2 "Fork NayaPOWER on GitHub" | Step 2 action | yes | hardcoded URL | https://github.com/SoulSchoolAcademy/NayaPOWER/fork (external) | yes (real link) | Repo slug verified verbatim: SoulSchoolAcademy/NayaPOWER. |
| Step 3 "Get the activation documents" | Step 3 action | dead | none | href="#s3" — self-anchor, goes nowhere | no | The actual activation-documents link/pack. |
| Step 4 "Connect to GitHub" | Step 4 action | dead | none | href="#s4" self-anchor | no | The actual GitHub-door connect flow (OAuth/install). |
| "Open Smart Doors" alt link | Step 4 alt | dead | none | href="#s4" self-anchor | no | Smart Doors target doesn't exist. |
| Finale "Enter NayaNET" | Bottom CTA | dead | none | href="#finale" self-anchor | no | Should route to identity/hub; currently scrolls to itself. |

## ⑤ The Wires

The schematics core: exactly what travels between parts, how, and whether it flows. A builder implementing any wire finds the contract here.

| Wire | From → To | Carries | How | Status |
|---|---|---|---|---|

| W1 capture | Scheduler → v7_create_smart_note (P10) | Note payload → transaction row (P8) | Workflow P15 with secrets NAYA_SUPABASE_URL · NAYA_SUPABASE_ANON_KEY · NAYA_RUNTIME_EMAIL · NAYA_RUNTIME_PASSWORD. Ran 14× Oct 7–10, 2 successes, then silence — no schedule trigger exists. | PR #2680 adds hourly pump |

| W2 canonicalize | Edge fn v7-smart-note-canonical (P13) → tables | Raw capture → canonical block rows (P1) + artifacts (P5) + receipts (P7) | Deployed Supabase function; 27 transactions Oct 7–10 measured. | flows |

| W3 project | Edge fn nayanet-github-dispatch (P14) → repo | Canonical note → IB-######/smart-note.md commit | Fail-closed, idempotent, single-transaction authority grant. 9 receipts and counting. | flows |

| W4 emit | emit_hub_feeds.py (P17) → HUB/FEEDS/*.json (P18) | Table rows → public JSON: today.json (← nayanet_intelligence_index + smart_note_artifacts — settled by #2678 diff read 2026-10-16; was provisionally attributed to blocks) · lists.json · spaces.json. 9 feeds remain: reports, library, connect, ledger, connections, mail, settings, manifest, feed. | Reads Supabase via the Management API server-side (bypasses RLS — settled by #2678 diff read; must stay server-side-only and documented as such); writes JSON to repo; merge-gated. Staleness caveat: committed JSONs are stale-on-arrival without a refresh mechanism — capped below the merge bar until one exists. | 3/12 in PR #2678 |

| W5 distribute | Merge → raw.githubusercontent.com | Committed feed files → CDN bytes | Nothing to build — merge is the deploy. Feed freshness = emitter cadence + merge latency. | waiting on merges |

| W6 bridge | Feed files / session → room adapters | Envelope {ok, state, data, method, runtime_connected} · 38 accessors (smartFeed, today(), lists(), spaces(), …) · graded fallback: live → localStorage → honest "not verified" copy | window.NayaPowerRuntime (P28); seam index-2.html:2395-2440; harness 23/23 green. Audit finding: most rooms don't reference the bridge at all — the integration isn't stubbed, it's absent. | PR #2679 in the dock |

| W7 return | Room actions → smart_note_events (P6) | Interaction events: saves, ratings, shares, comments, list/space membership. Contract not yet specified — field mapping requires one authenticated row read of P6; no fields invented here. | Unbuilt. Design law: events, not direct table writes from the browser (Why #3). Call sites ready to repoint (exact localStorage keys from the room audit): nayanet-board-actions-v1, boardId:contributions, naya.spaces.posts.v1, naya.spaces.chat.v1, naya.smartmail.sent, naya.library.blocks.v3, naya.connections.notes, naya.spaces.pins.v1. | not built |

| W8 learn | smart_note_events → engine | Compounded events → updated blocks, index entries, successor state | Unbuilt; blocked on W7. This is where "saved" becomes "learned." | blocked |

Read the colors as a story: W2–W3 flow (capture works when triggered, projection works), W1/W4–W6 wait in the dock (four merges), W7–W8 don't exist (the second half of the puzzle). The system's read path is one merge-away from alive; its write path is one design-away from existing.

## ⑥ The Order

Builds have a strict sequence — each row names what blocks it and the exact acceptance test. Nothing starts until its blockers clear.

*[Diagram: see the visual HTML edition — nayapower-schematics.html]*

| # | Build | Blocked by | Done when |
|---|---|---|---|

| B1 | Merge the dock: #2676 #2678 #2679 #2680 | Review (merge bar: green CI, ≥9.5, different seat, no objection) | All four merged; HUB/FEEDS/today.json served from raw.githubusercontent.com |

| B2 | Capture pump runs; bridge deployed; 3 feeds flowing | B1 | Hourly workflow run succeeds; bridge object resolves in a live room |

| B3 | 12 adapter swaps (specs drafted, file:line cited) | B2 · Interfaces: Naya 3 decides | Each room renders bridge data; zero fixtures presented as real |

| B4 | Deploy nav-fixed rooms + new connections + start | B3 · Shawn's gate | /hub/* live, drawer nav clean, Spaces header fixed |

| B5 | Real apply: saves, lists, spaces used with live data | B4 | Actions taken against real rows, observed end to end |

| B6 | Return loop: specify W7 contract from one live smart_note_events row, then implement | B5 (for volume) · contract needs no blocker | Room action → event row → visible in Supabase |

| B7 | Learn loop: engine reads events, compounds | B6 | An applied action changes a later retrieval — demonstrated |

| B8 | Re-prove: run the 12-step proof on schedule | B7 | Proof run completes, measured, independent verifier — repeatedly |

| B9 | 9 remaining emitters (reports, library, connect, ledger, connections, mail, settings, manifest, feed) | B1 (pattern) · D2 for mail | Each feed file committed on its cadence; rooms swapped |

| B10 | UI honesty + dead-link sweep (any seat) | none | Spaces header reads SMART SPACES; ROOM_FILES map corrected; smartmail-v1.2.html dead link repointed; mail enforces snippets-only; identity badge honest; start.html CTAs land somewhere real |

D5 · Write-side auth for the return loopShawn decides

Options: (a) session-token writes via RLS; (b) edge-function intermediary holding the service key. The browser is anon and the table is RLS-locked — schema without auth is a doc, not a build. Unblocks: W7/B6.

Peer-review work orders (F1–F9)

From the three cold peer reviews (R1 7.5 · R2 7.0 · R3 8.7). Resolved items stay listed so the history is visible.

| # | Fix | Status |
|---|---|---|

| F1 | today.json source contradiction (W4 vs loader spec) | resolved — index + artifacts, via #2678 diff read |

| F2 | Feed JSON schema ownership: emitter defines, room consumes | open |

| F3 | B3 startability ruling: prep now, implement post-B2; D3 gates targets | open |

| F4 | Write-side auth decision | D5 — Shawn |

| F5 | W7 event contract from one live smart_note_events row read | open |

| F6 | B6 blocker wording: correctness (seed ids ≠ real block ids), not volume | applied |

| F7 | Identify the engine's learn/distill component, or mark B7-must-specify | open |

| F8 | Glossary: door (hub room, 12) vs connect-door (integration, 9) vs surface (audited UI, 14) vs step (loop stage, 12) | applied below |

| F9 | Enumerate the 12 proof steps, or mark 4 TBD (8 named today) | open |

Glossary (F8): a door is a hub room (12); a connect-door is an integration on the door board (9: AI, Data, GitHub, MCP, Naya-to-Naya, Email, Calendar, Voice, Web); a surface is an audited UI surface (14, incl. entry pages); a step is a loop stage (12). A wire is an interface contract between parts (8).

## ⑦ The Decisions

Four open questions. Each names the options, who decides, and what unblocks when it's decided. Nothing here is built on an assumed answer.
D1 · The authenticated read path (B1/B2)Shawn decides

Personal rows are RLS-locked; the hub reads as anon and sees nothing. Options: (a) the hub holds a session and reads with the user's access token; (b) a scoped service reader for collective-plus-personal. Unblocks: P30, private reads in every room, B4-complete.
D2 · The mail privacy lineShawn decides

Options: (a) snippets-only allowlist — only threads marked shareable-to-hub emit; (b) no mail feed at all. Unblocks: mail emitter (B9), the ✉️ door.
D3 · The hub's future: hash-SPA vs standaloneNaya 3 decides (Interfaces)

/hub/#/hub and /hub/* coexist today — two systems. Options: (a) standalone pages win, SPA retired; (b) SPA wins, pages retired. Unblocks: B3 adapter targets, B4 deploy scope.
D4 · Library feed strategyEngine / team

Options: (a) top-50 paginated emitter, hourly; (b) full corpus snapshot, daily. Unblocks: library emitter (B9) — hardest feed, goes last regardless.

## ⑧ The Proof

How "complete" is verified — the standard every part above is held to.
Complete =

All twelve loop steps green, all twelve doors live on real data, the 12-step proof run repeatedly: capture → persist → receipt → cold retrieve → apply → verify → learn → successor reuse. We don't declare Naya alive because we built it — we demonstrate it, in use.
Evidence standard.

A green box in this document means measured evidence: a live API read, a merged commit, a passing harness, a row count from the database. "PR open" means verified open and mergeable via API — not merge-ready (merge bar still applies). Anything inferred is labeled.
The 12-step proof (B8).

Has never run once. When it does: a scheduled run captures a note, persists it, receipts it, cold-retrieves it, applies it in a room, verifies the application, learns from it, and hands working intelligence to a successor — measured end to end by an independent verifier. That run, repeated, is the finish line.

NayaPOWER System Schematics · the staple document.

Drawn from live bytes: Supabase OpenAPI pull (47 paths), workflow run history, PR states via API, room-file audit (file:line), Shawn's 12-door model. Statuses verified 2026-10-16. Green means evidence; everything else says what it is. Provenance note: the 12,026-row / 22-table totals were independently verified via Management API; per-table counts (191 blocks, 381 ledger rows, 7,472 members) are relayed from the system map and not yet independently reproduced.

Dock validation (2026-10-16, independent): all four dock PRs NEED WORK — #2680 payload blocker fixed, re-validating; #2678 needs refresh mechanism + server-side docs; #2679 needs envelope doc correction; #2676 needs green CI + receiver evidence. Merge order: #2680 → #2678 → #2679 → #2676, each gated on its fixes.
Self-score 9.4 (peer builders'-briefing scores 7.0–8.7; gaps work-ordered above, not hidden).
Companion depth: team-nitro/complete-puzzle/room-function-audit.md (the 181-function audit) · team-nitro/complete-puzzle/blueprint.md (per-door dossiers) · team-nitro/loader-specs.md (adapter specs) · team-nitro/runtime-contract.md (bridge contract) · team-nitro/data-flow-map.md (sender→receiver audit).
