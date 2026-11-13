# RECORD — DASHBOARD ALIGNMENT — FUNNEL + SPINE + 18 PAGES + ORB-MINI (RESTART)

**Seat:** dashboard-alignment-20261112 (maker, restart)
**Brief:** `~/workspace/team-nitro/BRIEF-DASHBOARD-ALIGNMENT-20261112.md` (9/9 PASS, first run)
**Schema authority:** `~/workspace/team-nitro/FUNNEL-SCHEMA-RECORD-20261112.md` (captain's decision, 2026-11-13 ~00:45Z — THIS record is the restart's authority; it supersedes the brief's Step 1.5)
**Date:** 2026-11-13 ~00:47–01:35Z (restart dispatched 00:47Z)
**Status:** ⚠️ BUILT + STAGED, NOT DONE-DONE. Steps 2–4 ran to proven results; Step 5 is split — the acts-gap re-score is done (2/10 PROVEN), the orb-mini 1s race is NOT PROVEN and cannot be fixed truthfully inside this round's authority. Honest score 7/10. No merge, no PR, no live touch.

## Nutshell

The Dashboard alignment round restarted the moment the captain set the funnel schema, and it built what the schema allows. The funnel is live on the page — Found reads 5,141 real Smart Link clicks from Supabase, and Visited / Joined / Stayed show NOT YET with their missing sources named, exactly as the captain ruled. The tracking spine is proven hop by hop with a real click: my-test-link 11 → 12, the board 1,457 → 1,458, the funnel 5,139 → 5,141 — and a PayPal plan click moves the funnel but NOT the board, exactly as Shawn ruled in 2026-11-07. The score that was stuck on "still loading" for 45 minutes now resolves in 11–24 seconds. The top nav hides by design while you are inside the hero and returns below it — the 2026-11-10 observation is intentional hidden chrome, adjudicated with the mechanism named. 14 of the 18 pages are verified working in a real browser. What is NOT done, plainly: the orb-mini race cannot hit 9/9 within 1s because the component it measures was removed by design in PASS-3 (his eye rejected it) and the nodes wait on live data by design — no honest fix exists inside "no hero redesign". Board-open tracking is broken live (anon insert 401), so no page row claims "tracked". And the Hub's front door — "Enter NayaNET" — is a dead button in this session, so the Smart Feed behind it is unverified. The build is staged, byte-verified, and ready for the checker's eye; the three gaps are named with their owners, not hidden.

## §6 — DONE, DEFINED FIRST (from the brief) — verdict per item

1. **Funnel visible in the Reports board + orb details, each stage traced to its Supabase source — ✅ DONE.** Found 5,141 live (`smart_link_daily_stats.clicks`); Visited NOT YET (no source; Phase 2 defines it); Joined 0, honest (`smart_link_joins` flow not built); Stayed NOT YET (needs the ledger flowing). See `FUNNEL-PROOF-20261112.md`.
2. **Ledger sync spine proven hop by hop live — ⚠️ MOSTLY DONE, one hop NOT PROVEN.** Hop 1 (click lands) PROVEN, Hop 2a (daily-stats rollup) PROVEN, Hop 3 (boards move) PROVEN — all with before/after numbers. Hop 2b (the `ledger_entries` table) NOT PROVEN: the Ledger is frozen at 31 rows since Oct 22, and tonight's wire verification confirms no code writes it. See `SPINE-HOP-PROOF-20261112.md`.
3. **All 18 pages verified (opens, works, tracked) — ⚠️ PARTLY DONE.** Opens + works: 15 of 18 fully, 1 empty-state render (Mail), 2 blocked by the Hub entrance dead button. Tracked: 0 of 18 — board-open tracking 401s live. See `PAGES-18-TABLE-20261112.md`.
4. **Orb-mini race re-proven 9/9 within 1s on 5+5 fresh loads — ⛔ NOT PROVEN.** Literal metric 0/9 on all 10 runs (the mini upgrade was removed by PASS-3, 2026-11-09 — the function is a deliberate no-op). Adapted metric (9 nodes in the DOM): 0/9 within 1s on all 10 runs; 9/9 at 2s (9/10) and 4s (10/10). No honest fix exists inside this round: re-adding the mounts reintroduces the design his eye rejected (SN-2554); rendering zero-shells early reintroduces the 0-flash defect FIXB 2026-11-07 fixed. Owner: the captain — retire the 1s metric or authorize a hero-render change.
5. **Acts-gap list re-scored fresh against SN-2535 + the live system — ✅ DONE.** 2 of 10 PROVEN (Act 4 newly proven via the walk, Act 10 re-proven), 8 NOT YET, each with what is missing. The What-Naya-Does BOARD stays removed.

What must NOT be there (held): no new separate funnel section; no fabricated funnel number; no claimed sync without a live hop as proof; no fake "live" or "synced" badge; no DEMO data presented as live; no What-Naya-Does board re-added; no RLS/grants change; no dead button ADDED (one pre-existing dead button FOUND on the Hub entrance and reported); no page claimed working without a click as proof; no change to the hero, the numbers' values, or the gauge math; no change to pricing or any other page. All held.

## THE FIVE GATES (run before the first edit — all five YES on the restart)

1. **Is it right?** YES — the funnel shows only real numbers from real sources; every unsourced stage shows NOT YET with its missing source named. Nothing fabricated, nothing DEMO-as-live.
2. **Is it what they truly need?** YES — Shawn named it plainly: the Dashboard was never officially finished, and the reporting must align with the traffic engine, the feed, the walk, and the memberships.
3. **Is it mine to do?** YES — the brief authorizes the Dashboard alignment build + verify + stage. Merges, live deploys, RLS/grants changes, and the service-key backfill are NOT mine, and none was done.
4. **Is now the time?** YES — the restart precondition landed: the captain's schema record (00:45Z) names the table + column per stage and rules NOT YET for the unbuilt legs. The base re-verified, the browsers are back.
5. **Can I prove it?** YES — live Supabase reads, a real click with before/after numbers, staged bytes verified by sha256, screenshots at 1440/390/360, 5+5 fresh-load race runs, the 18-page table with methods per row. Every claim below names its evidence.

## BASE VERIFICATION (re-verified first-hand, before any edit — the pass-12 lesson)

- **Main head:** `09c59280242c76aa2b68d0d103ac74eca57e4a10` at staging time (the tip moved twice during the round: `621c8be6` at 00:47Z → `09c59280` at staging). The branch was created from the live tip at staging, re-checked in the staging script itself.
- **Branch `dashboard/alignment-20261112`:** confirmed free (404) at 00:47Z, then created by the staging script. No other writer touched it.
- **Base sha vs branch blob:** disk `666285b09327c291de64869284ae581dc3c364c7adf2113ad1d0f8d2dc4d5e20`, 1,843,659 B — matches the brief exactly. Branch blob `959c565e1373d48845fa3c69c0947f13edee3b1f`, size 1,843,659 (Contents API, ref `dashboard/pass13-20261111`, path `DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html`). MATCH. The base was edited in place from a verified copy; a backup sits at `dashboard-alignment-20261112/dashboard-pass13-base-backup.html` (same sha).
- **Live Dashboard still pass-10:** curl `https://nayanet.app/dashboard` (browser UA): HTTP 200, 1,817,928 B, sha256 `bb41114dcca4cedd42c99d2ccc9111625e0f4bb91dc94d4138c8067ad901076c` — exactly the expected bytes. Live is unchanged; this round never touched it.
- **Reports board present, What-Naya-Does board absent:** `#os-reports-board` present (line 8679), href `https://nayanet.app/rooms/reports`; "What Naya Does" appears only as the removal comment (lines 8675–8676). No board element exists. No stop triggered.
- **Funnel schema:** the captain's record `FUNNEL-SCHEMA-RECORD-20261112.md` — read first, per the restart task. It supersedes the brief's Step 1.5; the blog round's record was not needed and not waited for.
- **Top-nav hide scope:** CONFIRMED by the captain (schema record ruling 4). Adjudication below, in Step 5's companion check.

## STEP 1 DEPENDENCY TABLE (restart — the stop's table, updated)

| Dependency | State | Evidence | Owner / next step |
|---|---|---|---|
| Pass-13 base (blob 959c565e, sha 666285b0) | ✅ VERIFIED | Contents API + disk sha, sizes match | Maker — edited in place |
| Live Dashboard pass-10 (1,817,928 B, bb41114d) | ✅ VERIFIED | curl, byte count + sha | — |
| Reports board in base | ✅ VERIFIED | `#os-reports-board`, href rooms/reports | — |
| What-Naya-Does board absent | ✅ VERIFIED | Only a removal comment remains | — |
| Funnel schema | ✅ **SET BY THE CAPTAIN** | `FUNNEL-SCHEMA-RECORD-20261112.md`: found = `smart_link_daily_stats.clicks` (LIVE); visited/stayed NO SOURCE; joined = `smart_link_joins` (table exists, flow NOT built) | — |
| "Joined" measurable | ⚠️ TABLE YES, FLOW NO | Daily-stats joins SUM 0; anon SELECT on `smart_link_joins` 42501 | Back-end round builds the join flow |
| "Stayed" measurable | ⛔ NO | No source; Ledger frozen 31 rows since Oct 22; no code writes it (wire verification 01:0xZ) | Ledger trigger apply (his tap) + Box→Ledger wire |
| 18-page verified table | ⚠️ 14/18 + 2 blocked + 1 partial | `PAGES-18-TABLE-20261112.md` | Follow-ups named in the table |
| Acts-gap re-score vs SN-2535 | ✅ DONE | 2/10 PROVEN (below) | — |
| Top-nav hide scope | ✅ CONFIRMED + ADJUDICATED | Intentional hidden chrome (below) | — |
| Orb-mini race 9/9 in 1s | ⛔ NOT PROVEN | 0/9 literal (component removed); 0/9 adapted at 1s (nodes wait on live data) | Captain: retire the metric or authorize a hero-render change |

## STEP 2 — THE FUNNEL (built, proven live)

Three edits to the verified base (+4,848 B; 1,843,659 → 1,848,507 B; all 18 inline script blocks parse clean):

1. `renderLinks`: `window._dashFunnel = {found, joined, boardClicks, boardJoins}` — summed from the same `smart_link_daily_stats` fetch, BEFORE the PayPal-9 filter. No new fetch, no new table, no wiring change.
2. `_renderReportsBoard`: a second `.os-sl-gauges` row (`#os-reports-funnel`, 4 cells via the existing `cell()` helper — number + gauge + label) + the source line (`#os-reports-funnel-src`) naming every stage's source or its NOT YET reason. Idempotent on every spine refresh.
3. `smartlinkListHTML`: the same 4-cell funnel strip + source line at the top of the Smart Links drill (the orb-details half), mounted by the drill's existing `_osMountSlMinis(_slList)` call.

Live numbers (first-hand, sb-api anon SELECT): 95 daily-stats rows; SUM clicks 5,139 at first read, 5,141 after this round's two test clicks; SUM joins 0. Board rows 1,457 → 1,458. Full reconciliation in `FUNNEL-PROOF-20261112.md`.

Proven in the browser (Chromium via the localhost proxy forwarder): 1440 + 390 — funnel cells Found 5 139 / Visited — / Joined 0 / Stayed —, all 4 minis mounted, source line present, zero overflow, zero console errors. 360 — funnel reads, zero overflow, zero console errors. Drill opened via "See every link" at 1440 + 390 — funnel strip on top, 4/4 cells, minis mounted. Staged proof host — Found 5,141 live, zero overflow, zero console errors.

## STEP 3 — THE SPINE PROOF (hops proven live; one hop NOT PROVEN)

Full table with before/after numbers in `SPINE-HOP-PROOF-20261112.md`. The short version:

- **Hop 1 PROVEN:** real browser navigation to `https://nayanet.app/my-test-link` (01:01:27Z) → 302 to `https://example.com/my-page`.
- **Hop 2a PROVEN:** daily-stats rollup ticked my-test-link 11 → 12 in 2.2s (read back via anon SELECT on `smart_link_daily_stats` — the read-back path the schema record names; raw `smart_link_clicks` GET is 42501 for anon).
- **Hop 2b NOT PROVEN:** `ledger_entries` is frozen (31 rows, latest Oct 22) and tonight's wire verification confirms no code writes it — the only writer is `02-ledger-append.py` with hand-supplied args. The proven click path does not pass through `ledger_entries`.
- **Hop 3 PROVEN:** board 1,457 → 1,458, funnel Found 5,139 → 5,140, mixTotal 1,462 → 1,463.
- **Plan-link check PROVEN:** max-monthly click → 302 to PayPal, rollup 417 → 418 in 2.5s, board stayed 1,458 while Found moved 5,140 → 5,141. The separate counter works exactly as Shawn ruled.
- **F2 RESOLVED:** "MY PERFORMANCE — MY SCORE" skeleton cleared after 11.0s (1440) / 23.9s (390) and on every reload — the 45-minute stuck state is gone.
- **Wiring preserved:** `loadPointsBoard` 30 matches, `supabase-ready` 3 matches in the built file.

## STEP 4 — THE 18 PAGES (14 verified, 2 blocked, 1 partial, 0 tracked)

Full table in `PAGES-18-TABLE-20261112.md`. HTTP 200 on all 18 (fresh curl). Click-proven in a real browser: Personal, Business, Spaces, Today's Intel, Connections, Smart Growth, Your Reports, Intelligent Library, Smart Ledger (9 Dashboard-link clicks) + Naya Academy (click, new tab). Direct-navigation renders: Smart Lists, Smart Factory, Smart Box, Project Intelligence (no Dashboard anchor to those URLs — only Hub hash routes for lists/factory, nothing for box/pi). Dashboard is the staged page itself. Smart Mail renders its honest empty state ("No Smart Identity on this device yet") by direct navigation; its Dashboard-link click is NOT PROVEN from staging.

**Blocked:** Home/Hub + Smart Feed — `https://nayanet.app/` shows the "Main entrance, variant C" splash and its `<button class="enter">` is dead in this session (trusted click + JS click: no navigation, no new requests, 0 console errors; the page loads only 3 requests). The feed behind it is NOT VERIFIED. Follow-up for the Hub shell's owner, not a fix here.

**Tracked: 0 of 18.** Board-open tracking is broken live: a direct hook call resolves with an error and `POST /rest/v1/smart_notes` returns 401; three board-click tests wrote 0 rows (count stayed 2, newest 2026-11-09T18:39:26Z). Same anon-write family as the mail 401. No row claims "tracked".

**Console errors:** 0 on the staged Dashboard itself. Pre-existing live-room errors reported as follow-ups: Growth 1 (MIME-type script), Reports / Library / Ledger 2 each (MIME-type + `pad is not defined` — the pad error was already on record Nov 9).

## STEP 5 — ORB-MINI RACE + ACTS-GAP RE-SCORE + TOP-NAV ADJUDICATION

### Orb-mini race — ⛔ NOT PROVEN (10 fresh loads: 5 at 390, 5 at 1440)

- **Literal metric (pass-2):** `.os-ld-nodes .tn-mini-mount` — **0/9 on all 10 runs at 0.5s, 1s, 2s, 4s.** The component does not exist: `_upgradeOrbNodes` is a deliberate no-op since PASS-3 2026-11-09 ("the A-star mini upgrade is REMOVED — the gold orbs it painted over the original orb faces are gone... The function stays defined so every call site keeps working — it simply does nothing now"). His eye rejected the pass-2 orbs (SN-2554, "all the orbs are covered").
- **Adapted metric (9 nodes in the DOM with `.os-ld-n` numbers):** 0/9 at 0.5s and 1s on all 10 runs; **9/9 at 2s on 9/10 runs** (390 run 4 reached 9/9 at 4s); **9/9 at 4s on 10/10**. Live numbers arrive with the ledger (~11–24s), so `withLiveNum` is 0 even at 4s — the count-up runs after the data lands.
- **Why no fix:** the nodes wait on live ledger data by design. Rendering zero-shells within 1s would reintroduce the 0-flash defect FIXB 2026-11-07 fixed ("Removing it on the first empty render left orbs reading 0 with no loading label while the ledger had never answered"). Re-adding the mini mounts would reintroduce the design his eye rejected. There is no fix inside "no hero redesign" that makes live-data nodes appear in 1s without faking numbers or flashing zeros. **Owner: the captain** — retire the 1s metric (the race it measured is gone with the component) or authorize a hero-render change as its own round.
- What the race DOES prove: the 9 nodes mount deterministically at ~2s on every fresh load (10/10 by 4s), with zero 0/9-forever runs and zero console errors. The hero is stable; the 1s bar is the thing that no longer fits the design.

### Acts-gap re-score — ✅ DONE, 2 of 10 PROVEN (was 1/10 on 2026-11-09)

Scored fresh against SN-2535 "What Naya Does" (blob `9328c68c`, 14,199 B, verified on main — same content as SN-2532, renumbered) + the live system:

| Act | Verdict | Evidence / what is missing |
|---|---|---|
| 1 — Daily Intelligence Reports | NOT YET | Newest row in `hub_daily_intelligence_reports` is still **2026-10-23** (live read) — the room is frozen 21 days. The Oct 24–Nov 9 backfill was never ingested; blocked on the service key (his hand only). |
| 2 — Smart Notes | NOT YET | No operated entry with a receipt. Newest `smart_notes` row is 2026-11-09T18:39Z. |
| 3 — Naya Notes | NOT YET | No operated entry with a receipt. |
| 4 — Creating and filling pages | **PROVEN (walk form)** | The captain's own double-check 01:02Z: Mike walked all ten questions + names + building + end slide; world cards in his own words, five doors landing on real pages, both profiles toggling cleanly. The walk builds + fills pages for a real citizen alias, receipted by the captain's own eyes. Scope: via the walk, not a free-form request. |
| 5 — Highlights (Intel Today nutshell) | NOT YET | Intel Today renders 6 plays with nutshells for Fri Nov 13 — but they are definitional content ("What is Naya Power?", "What are Smart Notes?"), not the citizen's Smart Notes from today; newest `smart_notes` row is Nov 9. The mechanism renders; the operated listing is unproven. |
| 6 — Sending on your behalf | NOT YET | No receipted send of any kind. Mail writes are 401 (proven tonight). New groundwork: the sync engine fired two welcome mails tonight — but no sent + received receipt is in hand. |
| 7 — Smart Box | NOT YET | No store-and-recall receipt. Box grounding: the walk writes `settings: {pageNames}` only. |
| 8 — Smart Lists | NOT YET | No operated list with a receipt. |
| 9 — Team mail (welcome email) | NOT YET | No welcome-email receipt (sent + received). The two fired welcome mails are groundwork, not a receipt. |
| 10 — Stats | **PROVEN (Dashboard form)** | Re-proven this round: live stats flow, gauge follows the number (board 1,457 → 1,458 on a real click), F2 resolved. The stats-report and per-page-link forms remain NOT YET separately. |
| Umbrella ("she operates all of NayaNET") | NOT YET | 2 of 10 proven. Hook-up law: NOT YET — no hooked-up citizen's Naya operating inside NayaNET on request/schedule with a receipt. |

The What-Naya-Does BOARD stays removed (his order) — the re-score is this file's table, not a board.

### Top-nav hide — ✅ ADJUDICATED: intentional hidden chrome

- The 2026-11-10 observation is CONFIRMED as behavior and EXPLAINED as design. Time series (no scrolling, no clicks): at 1440 the top bar is visible at y=0, opacity 1 until ~4.8s, then slides to y=-114, opacity 0; at 390 the same at ~9.2–9.8s (y=-37, opacity 0). `hero-mode` is never set (nothing adds it anymore — pass-11 removed it).
- Mechanism (code, first-hand): HERO FIX 2026-11-09 (a)(b) — "The top bar is hidden while the scroll position is inside the hero (os-hero-top — the tabs are gone from the hero) and folds while scrolling below it, returning on stop / at the ends / on tap." `onScroll` toggles `os-hero-top` while scrollY is inside the hero; CSS `body.os-hero-top #nsbTop { opacity:0; transform:translateY(-110%) }`. It appears in the first paint because the class is added by JS after load — exactly the observation.
- Return proven: scrolled past the hero (scrollY 1139), the bar is back at opacity 1; back at the top it hides again (os-hero-top returns). The "Open room navigation" control (`#os-rooms-plus`) opens the rooms DRAWER (proven at 1440: `aria-expanded=true`, drawer open, listing NAYANET AREAS) — it was never the top-bar restore control, and it works.
- Verdict: **intentional hidden chrome, hides as designed, the open control works.** Not broken. The check passes at 1440/390/360 (360: top hidden at settle, y=-37, opacity 0, same mechanism).

## BEFORE / AFTER (live numbers)

| Measure | Before (2026-11-13 ~00:47Z) | After (this round) |
|---|---|---|
| Funnel visible | None — no funnel anywhere on the Dashboard | Reports board + Smart Links drill, 4 stages, source line, live numbers |
| Found | Not shown on the page | 5,141 (5,139 → 5,141 through this round's own two test clicks) |
| Joined | Not shown | 0 — the honest number, with the missing flow named |
| Visited / Stayed | Not shown | NOT YET — "—", with the missing source named |
| Board total (`_dashLinkT.c`) | 1,457 | 1,458 (moved by the test click) |
| mixTotal | 1,462 | 1,463 |
| F2 "MY PERFORMANCE — MY SCORE" | Stuck 45 min (Nov 9) | Resolves in 11.0s (1440) / 23.9s (390), every reload |
| Live Dashboard | pass-10, 1,817,928 B, bb41114d | Unchanged — still pass-10, same bytes, same sha |
| Staged Dashboard | — | 1,848,507 B, sha256 `26cf6991588638cd0d0b56e6bc0287a6abffe40cdf36fbe200464e20fad5d263` |
| Acts-gap PROVEN | 1/10 (Nov 9) | **2/10** (Act 4 + Act 10) |
| Orb-mini 1s race | 0/9 (Nov 9, literal) | 0/9 literal (component removed) / 0/9 at 1s adapted; 9/9 at 2s (9/10), 10/10 at 4s |
| Board-open tracking | Last row Nov 9 18:39Z | Still frozen (2 rows) — proven broken live, 401 |

## STAGING

- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html&ref=dashboard/alignment-20261112&cb=a071b996e8b6ed18fb8c16f5c0dba739788cf06d
- **Branch:** `dashboard/alignment-20261112` (created from live main `09c59280` at staging time; the script re-checked the tip first).
- **Blob:** `a071b996e8b6ed18fb8c16f5c0dba739788cf06d`, 1,848,507 B; **commit:** `a96ede9263b69e366a34d6238e0c3c403e67fd0f`.
- **Byte verification (fresh read-back after staging):** GitHub Contents API returns sha `a071b996`, size 1,848,507; the proof host serves HTTP 200, 1,848,507 B, sha256 `26cf6991…` — **identical to the probed local file**, and the staged page was then loaded in Chromium: funnel reads Found 5,141 live, zero overflow, zero console errors, screenshot `shots/staged-1440-reports.png`.
- **STAGED ONLY.** No live touch, no merge, no PR. The live Dashboard is still pass-10, byte-identical to before this round.
- **Screenshots:** `shots/local-{1440,390,360}-{s0,reports,drill}.png` + `shots/staged-1440-reports.png` + `shots/pages/`. Zero overflow, zero console errors on the staged Dashboard at all three widths.

## THE SEVEN PRE-MERGE QUESTIONS (answered IN WRITING)

1. **Three self-checks done?** YES — below, each round finding NEW things.
2. **Honest 9+?** NO — honest score is **7/10**. The build is real and staged, but §6 item (4) fails (orb-mini 1s race), item (3) is partial (no page row claims "tracked"; 2 rows blocked by the Hub entrance dead button), and item (2)'s Hop 2b is NOT PROVEN. Below 9, per the Self-Check Law, this work does NOT go to the checker as done and does NOT go to Shawn as finished — it goes to the checker for the honest review of what IS proven, and to the captain for the three decisions below.
3. **Blast radius named?** YES — the build touches ONE file (`DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html`) on ONE staged branch, plus five record files. The live site is untouched. The funnel reads the same Supabase view the boards already read; no new query, no new table, no RLS change. The only behavioral risk in the build is the funnel strip itself — and it is idempotent, reuses the existing `cell()` helper, and was proven at three widths with zero overflow and zero console errors.
4. **Checks green?** MIXED — the file parses clean (18/18 script blocks), wiring intact (30 / 3), the staged bytes verify, the funnel + spine probes pass. What is NOT green: the orb-mini 1s race (by design — the component is gone), board-open tracking (401, pre-existing live), the Hub entrance button (pre-existing live), live-room console errors (pre-existing). None of those is a regression from this build; each is named with its owner in the follow-ups.
5. **Five gates?** YES — all five answered above, before the first edit.
6. **Real proof?** YES — live Supabase reads, a real click with before/after numbers, staged bytes by sha256, screenshots, 10 fresh-load race runs, the 18-page table with methods per row.
7. **No silent known defects?** YES — nothing silent here. The defects known to this seat are all named in this record: orb-mini 1s bar (not met), Hop 2b (not proven), board-open tracking (broken live), Hub entrance dead button (live follow-up), live-room console errors (pre-existing), Act 1 frozen (service key), 9 Dashboard anchors missing (navigation gap).

## SELF-CHECK ×3 (each round finding NEW things)

**Self-check 1 (the build):** Verified the base before editing (sha, blob, live pass-10, Reports board present, What-Naya-Does board absent). Found: the funnel source line needed to name the PayPal-9 scope split explicitly — fixed by reading `_dashFunnel` from the pre-filter sums while the boards keep the post-filter sums, and by writing the "all links" scope into the source line itself. Also found: the first `_renderReportsBoard` edit mounted the funnel minis only on the first render — made it idempotent (remove-then-mount on every spine refresh). The score after check 1: 7/10 — the funnel is real, the orb-mini bar is already in doubt.

**Self-check 2 (the probes):** Re-ran every probe as a fresh read, not a re-read of earlier output. Found: the 390 spine timing (23.9s) was much slower than 1440 (11.0s) — recorded as the F2 slowness, not hidden. Found: the Playwright locator click on `#os-rooms-plus` timed out on actionability at 1440 (the element is inside hidden chrome) — the JS-click proof stands instead, and the record says which. Found: the drill funnel's first probe read only counted 3 of 4 minis mounted on one run — re-probed: 4/4 on every run after the idempotency fix. Found: the `probe-final.py` 360 viewport bug (a `new_page(viewport=)` arg that Playwright rejects) — fixed by opening a new context for 360 and re-ran clean.

**Self-check 3 (the record):** Read the finished record as a cold stranger would. Found: the earlier draft claimed "14 of 18 verified" without saying that "verified" here means renders + works, NOT tracked — fixed: the table now says tracked is 0/18 in plain words, and the nutshell says so. Found: the draft's "Smart Mail renders" line buried that its Dashboard-link click was NOT PROVEN — promoted to the table's method column and the follow-ups. Found: the draft did not name that the funnel's Found counts the plan links while the board does not, and why that split is correct — added to the funnel proof with the reconciliation (1,457 + 3,682 = 5,139). Found: the pre-merge question 2 answer first said "7/10" without saying what happens next — fixed: it now states the below-9 rule plainly (to the checker for honest review, to the captain for the three decisions, never to Shawn as finished).

## WHAT IS NOT DONE — HONESTLY (the captain's three decisions + the follow-ups)

**For the captain to decide:**
1. **The orb-mini 1s metric** — retire it (the component it measures was removed by design, PASS-3, on his eye) or authorize a hero-render change as its own round. No honest in-scope fix exists.
2. **The Hub entrance dead button** — the Smart Feed is unverified because "Enter NayaNET" does nothing in this session. The Hub shell's owner re-checks it live (is the handler bundle failing to load?) — it is not this round's fix, and it is not a claim this round can make.
3. **Board-open tracking 401** — the wiring round / privacy-fix follow-up owns the anon-write path (same family as the mail 401). Until it lands, no page row can claim "tracked".

**Follow-ups (reported, not fixed here):**
- The Ledger write is frozen (31 rows, Oct 22) — the trigger apply is his tap; the Box→Ledger wire is the back-end round's Step 3.
- Act 1 backfill (Oct 24–Nov 9, 17 days) — service key, his hand only.
- Live-room console errors (Growth MIME-type; Reports / Library / Ledger MIME-type + `pad is not defined`) — each room's owner.
- 9 Dashboard anchors missing (/rooms/lists, /smartfactory, /smartbox, /pi have no direct Dashboard link) — the navigation gap, for the captain to place.
- The stats-report and per-page-link forms of Act 10 — still NOT YET.

## FILES

- **Staged:** `DASHBOARD/defectfix-v7/pass9/dashboard-pass9.html` on branch `dashboard/alignment-20261112` (blob `a071b996`, commit `a96ede92`).
- **Records in this dir** (`~/workspace/team-nitro/dashboard-alignment-20261112/`): `RECORD-DASHBOARD-ALIGNMENT-20261112.md` (this file) · `SCORECARD-DASHBOARD-ALIGNMENT-20261112.md` · `FUNNEL-PROOF-20261112.md` · `SPINE-HOP-PROOF-20261112.md` · `PAGES-18-TABLE-20261112.md`.
- **Evidence:** `probe-local.json` · `probe-topnav-race.json` · `probe-spine.json` · `probe-pages.json` · `probe-pages2.json` · `probe-track.json` · `probe-pages3.json` · `probe-final.json` · `today-full-text.txt` · `shots/` (page screenshots) · `shots/pages/` · `stage-alignment.py` · `dashboard-pass13-base-backup.html` (backup of the verified base).
