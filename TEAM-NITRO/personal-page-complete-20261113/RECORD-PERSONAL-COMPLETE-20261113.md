# RECORD — Personal page complete round (2026-11-13)

## What it is

Shawn's seven-item Personal list, built on the points base and proven on the staged page he can open. One page, one round, the whole list — not one item alone.

- **Branch:** `personal/personal-page-complete-20261113`, off main tip `8f2af988b2a4adefda9afb8ad752c7971c10ea8c`, worktree `~/workspace/personal-complete-wt`.
- **Base:** the points round's `personal-points.html`, SHA `eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95` (1,486,494 B), verified by `sha256sum` in three places before editing. The base is live Personal (SHA `992ab18c…`) + points pill + wiring + hero-fix block.
- **Built file:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`, 1,536,733 B, SHA `87d038470fb65ccd90b4c4a25af4cf2abea20afe7045c5aff193ae3ee73fc04c` (read fresh from the staged bytes via curl — byte-identical to the local file).
- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=b0a792186992dc06ee1d1dffafce343041b1faab
- **Commits:** `b0a792186` (page + build + probes + screenshots, 16 files, pushed, verified by `git ls-remote` — branch is on the remote at `b0a792186992dc06ee1d1dffafce343041b1faab`) + this record/scorecard commit (below).
- **Build:** `build-complete.py` — exact-string replacements with asserted counts, 28 hunks, saved to `diff-complete.txt`. The base file was edited, never rebuilt. The hero hunks are exactly three: the gear add, the settingsbtn removal from the row, and the composer→createRow swap. Name, pill, and tagline lines untouched (asserted in the build).
- **Live untouched:** live Personal re-curled unchanged — https://nayanet.app/personal, 1,484,185 B, SHA `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50` (exact match to the recorded value). Live Hub shell at `https://nayanet.app/` serves 620,595 B, SHA `0c8628d5769c10e6462ee31490f12e3bca6eb4f472854215ff1979a8c782ad27`; the Hub shell under an alias path served 4,990,447 B identically twice during this session. No live page, merge, deploy, or PR. No live writes of any kind except the staged Supabase test rows, now deleted (see Cleanup).

## Why it matters

The Personal page is the citizen's world — the first thing they live in. Shawn named seven things wrong with it on 2026-11-13 ~14:11Z and the Checklist Law says the list is the unit of work: nothing is called done until every item is proven on the page he sees. This round is that list, worked to zero as far as this environment allows — and where it stops short, the stop is named here with its reason, never silent.

## How to apply it

Open the staged link above (phone first). The seven items are proven in § Proof below. The two honest gaps — live-data rendering and the points number — need a browser whose external fetch works (see § What stopped short). The captain rules the tab order (§ Order) and the Public-query widening (§ Public gap) at double-check.

---

## § The sharpening — received and applied

Shawn's first sharpening (~14:28Z, brief updated to 40,485 B, check-brief OVERALL PASS) binds the rail build (Item 7). Confirmed applied:

1. **Initials, never faces, in the rail.** Every rail orb is `.fc-pick-av` — an initial letter with a spinning sheen, harvested from the creator file. **Zero faces, zero photos, zero avatar images in the rail: 0 `<img>` inside `#pcRail` at 390, 1440, and 360** (measured on staged). A face appears only on the citizen's own profile, if they choose to show one there — the rail never renders one.
2. **The line under the alias is one nutshell.** Each seed card carries exactly one mini-introduction line — who you are in the simplest terms + what you're about + your thing + your motto, all in one. No separate motto field, no separate mission field. Live cards carry NO nutshell line at all: the endpoint returns no nutshell, so none was invented — the record states the omission rather than filling it.

## § Harvest sites — exact file + line

| What | Source | Lines |
|---|---|---|
| Hub feed system (`.smart-tabs`, `smartTabStrip`, `intelBoard`, chunked render, `activityStream`, `ListsRoom`) | `personal-page-complete-20261113/hub-index-main-8f2af988.html` (main tip `8f2af988`, blob `5716901b`) | `.smart-tabs` 1042; `.smart-tab` 1068; `SMART_TAB_KEY` 5159; `smartTabStrip` call 5211; `show-feed` 5945; `stream === 'personal'` 6005; `smartTabStrip` 6008; chunked render 6036; `activityStream` 6090; `intelBoard` 6357; `ListsRoom()` 7323; `refresh('people')` 7279 |
| Full-page creator, picker, chat, plus menu (5 items), create row, `fcOpenCreator`/`fcCloseCreator`/`fcTogglePlusMenu`/`fcOpenPicker`/chat vars | `personal-feed-creator-fix-20261112/personal-feed-creator-fixed.html` (SHA `8a95481b…`) | `#fc-style` 3904; `#fcCreator`/`#fcPicker`/`#fcChat`/`#fcPlusMenu` 3962–4011; `#fcCreateRow` 4904–4914; plus seg `data-notif="plus"` 13833; plus icon 13816; fc script 22495–22745 |
| The line fix (restate `.notif-seg` box-shadow without the inset white top line) | `personal-feed-creator-fix-20261112/build-fix.py` (A-fix, ~20–60) + its record §2 (pixel proof the line is the page-wide `button{box-shadow: inset 0 1px 0 …}` rule painting at each seg's top edge) | Base page-wide rule at base lines 2182–2185; `.notif-seg` at base 12781–12787 (no own shadow, so the page-wide rule applied) |
| Uniform-flex button mechanism (adapted to 8, Settings removed — the creator file's nine-button law conflicts with this brief's Item 1 and does not govern) | creator file, button law 1950–1975 | — |
| Endpoint gate + weights (topics 0.40 / goals 0.25 / offers↔needs 0.20 / wants 0.15; ≥2 independent signals; reasons always ride) | `smart-match-option-a-20261113/OPTION-A-RECORD-20261113.md` + `HUB/walk/worker.js` (`authCitizen`, `apiGatedMatches`) | — |
| Points pill + wiring + hero fix (survives byte-for-byte; this round did not re-fix it) | `points-on-personal-space-business-20261113/personal-points.html` + `RECORD-POINTS-20261113.md` | Pill markup 17–19; wiring `personal-points.html:18330–18336`; chain `window._dashD` (live rows, set at 12479) → `ldData()` (17570) → orb sum over `LD_NODES` (17541) → `loadPointsBoard` total |

The rail is the one composed piece (the brief says so plainly): the Hub people room renders governed connections with no mini-profiles and no online flag, so the rail is composed from the people room + real endpoint data, in the Hub's visual language. The live Hub rail was not read by eye (no live browser as a subagent); the byte-identical Hub shell file above is the first-hand reference — that substitution is stated honestly.

## § Proof — measurement table for all seven items

Method: Playwright Firefox, real browser, staged proof-host link with a fresh `cb` per width (`cb=<commit>-w<width>`), at 390 / 1440 / 360. Probe `verify-staged.py` → `verify-staged.json` + 9 screenshots `staged-{390,1440,360}-{top,end,feed}.png`. Local mechanism proof (`verify-complete.py` → `verify-complete.json`) used stub posts through the page's own `mwPaintWallPosts`, because the browser cannot fetch externally (see § What stopped short).

### Item 1 — eight even grid buttons, Join one of them, Settings a small tool icon — PASS

| Width | Button widths (8) | Join | Gear |
|---|---|---|---|
| 390 | 110 px × 8, equal ±0 px (2-col grid) | 8th, green glow, one column (not full-width) | 48×48 at (332,64), text `⚙️` only |
| 1440 | 147 px × 8, equal ±0 px (one row) | 8th, green glow | 48×48 at (1196,76), text `⚙️` only |
| 360 | 160 px × 8, equal ±0 px (2-col grid) | 8th, green glow, one column | 48×48 at (302,64), text `⚙️` only |

`settings_in_row: false` at all widths. Clicking the gear opens Settings (`location.hash === '#settings'`) at all three widths. The gear keeps `id="settingsbtn"` + `data-os-go="settings"` so the existing wiring opens Settings. Gear positions track all three cover regimes (desktop beside Change cover; phone below Change cover at top:64 right:10; short-height below the moved Change cover at top:64 left:10).

### Item 2 — one `+` in the bottom bar on the left, opening exactly five items; both floating pluses gone — PASS

- Bottom-bar segs, in order, at all widths: `['plus','mail','activity','spaces']` — the `+` is FIRST (left end).
- `#pluswrap`, `#os-rooms-plus`, `#os-eco-plus` all `display:none` (hidden, not deleted, so JS references stay intact). Exactly one `+` visible on the page.
- Clicking the bar `+` shows `#fcPlusMenu` with exactly five items in order: Make a post · Naya note · Smart note · Message · Mail.
- Consequence, stated plainly: hiding the two floating pluses strands the right (ecosystem) drawer — only `#os-rooms-plus` and `#os-eco-plus` open the drawers. The left drawer stays reachable via the bottom-bar Spaces seg.

### Item 3 — the line above the bottom icons gone — PASS (decisive)

- Computed `.notif-seg` box-shadow on staged: `rgba(0,0,0,0.25) 0px -2px 8px 0px inset, rgba(0,0,0,0.4) 0px 6px 20px 0px` — the inset white top line is gone (the A-fix restatement, harvested verbatim).
- Pixel scan of the staged screenshots, row 2 px above the tiles: mean brightness **8.4** at 1440, **14.7** at 390, **15.6** at 360 (max 27–33) — the creator round's failing baseline was ~80. No lit line at any width. Eye-check confirms: the bar's top edge is a background change plus shadow, no line.

### Item 4 — the name unclipped; points pill survives (points round owns the fix — verified, not re-fixed) — PASS on placement, NUMBER UNPROVEN (see § What stopped short)

- Name `#pname` ("Shawn Vibert") never intersects Change cover at any width: (146,350) 159.6×40 at 390; (184,311.2) at 1440; (16,483) at 360.
- Pill `#pointsdisplay` present: below the name at 390 (146,404), beside the name at 1440 (357.6,308.2) and 360 (189.6,480). Hero hunks limited to the three named above; name/pill/tagline lines untouched (asserted in the build).
- The pill text on staged reads `…` at 4 s after load and **`0 pts` by screenshot time** — a fallback, NOT the citizen's live total. The pill follows the donut total, which sums the live ledger rows into `window._dashD`; the rows never land in this browser (fetch blocked — § What stopped short), so the number cannot be proven on staged here. The points round's own staged proof was geometry-only too (its record § Proof: boxes identical, fixtures for the number). The number is the points round's ownership; this round verifies the pill survives and sits right, and states the number gap plainly.

### Item 5 — the Hub's exact feed system: three tabs, Smart Tabs that re-filter, no always-open composer, full-page creator, Smart Lists — PASS except Smart Lists render (see gap)

- Tabs read **Personal / Public smart feed / Naya Notes**, keys `personal`/`public`/`naya`, in that DOM order, at all widths. (Ids were KEPT — `mwTabSmart` etc. — so the Smart Access course's tab refs keep resolving; labels, order, and keys carry the feed.)
- Feed line present, literally: `MATCH → ORGANIZE → CONNECT`, immediately above the Smart Tabs ribbon.
- Always-open composer: **0** cards. In its place, `#fcCreateRow` with three buttons: Make a post / Naya note / Smart note. The ribbon `__add` pill opens the creator instead of scrolling to the removed textarea.
- Creator: opens in naya mode (title "Naya note") and post mode; a post from the creator closes the creator and lands as a stub card (`data-fc-stub-1794581801645`, title "Probe — personal complete check (delete me).") rendered as a full intelligent block (CREATE SPACE / FAVORITE / SAVE, LOVE / LIKE, stars, SHARE INTEL). The live save was refused (RLS) — **zero live rows created by the probe** (verified by service-key read: 0 rows containing the probe text in `smart_notes`).
- Wall on staged: **1 placeholder card per tab** — the real wall did not load (fetch blocked). The live data exists: `smart_notes` for `flagship-personal` = **26 rows** (service-key read); `naya_notes` = **14 rows**. Locally, with stub posts through the page's own painter: Personal 2 cards (owner only, meta "2 posts … across 1 voice"), Public 3 cards (all, "3 posts … across 2 voices"), author pill "shawn vibert" → 2 cards; Naya Notes panel visible with the wall hidden; only the active tab's feedname line visible.
- **Smart Lists — store write PROVEN on staged, render NOT proven:** SAVE on the probe card wrote `localStorage['naya.smartlist']` = `{"saved":[{"id":"fc-stub-1794581801645","kind":"save","title":"Probe — personal complete check (delete me).",…}]}`. The saved item does NOT render in the Lists room on staged: the Lists view shows only its intro. Cause read from the code (base ~10830–10875): saved items migrate into a list called "Saved on this device" inside `slMigrate`, which runs only after `slFetch()` (Supabase) succeeds; the fetch fails in this browser, so the migration never runs. Same mechanism locally. The render needs a browser with working fetch — it is not a page-code gap, it is the same environmental stop.
- **Public gap, stated plainly:** the base wall query is owner-scoped (`owner_alias=eq.flagship-personal`, seen in the staged console URL), so the Public tab shows the same 26 owner notes as Personal until the query is widened. The Public tab as built re-filters the owner's wall (author pills); it does NOT pull other citizens' notes. Widening the query is a new data path, beyond harvest/compose — the captain rules it; it is not silently claimed otherwise.
- **Keyword search decision:** the search band `#tnpsBand` is hidden by Shawn's popup-only search law (base line 4021: `#tnpsBand{display:none!important}` — "search is a centered popup, never a bar"). A keyword wiring to the hidden input was built, then REMOVED as dead code (the input can never receive typing). The feed's topic pull is the Smart Tabs ribbon (author/category pills). No visible search box was invented — it would violate the popup-only law and the harvest rule. The captain can rule on whether a feed keyword box is wanted.

### Item 6 — the Smart Feed engine on real matches: real people, real percentages, reasons attached — PASS (endpoint + rail)

- **Endpoint proof (counted by hand from `endpoint-proof.json`):** `POST /api/welcome/matches` on staging worker `https://naya-welcome-staging.nayapower.workers.dev/`, HTTP **200**, `gated: true`, `gate: "welcome-engine-consent-gate/v1"`, `viewer: "pcviewer20261113"`. **6 matches:**
  1. `pcprover20261113` "Personal Complete Prover (test)" — **48%** (score 48; `sql_twin` agrees 48=48). Reasons: "shared: PROVING, build, page, ship, shipping" · "shared goals: page, prove, ship" · "wanted connection: PROVING, build, ship".
  2. `powercoldseat1111` "Power Cold Seat" — **7%**. Reasons: "shared: build, tool" · "shared goals: test, work" · "wanted connection: build, test, tool".
  3. `freshtestfour` "Fresh Test Four" — **4%**. Reasons: "shared: test" · "shared goals: test" · "wanted connection: test".
  4. `freshtestone` "Fresh Test One" — **4%**, same reasons.
  5. `freshtestthree` "Fresh Test Three" — **4%**, same reasons.
  6. `freshtesttwo` "Fresh Test Two" — **4%**, same reasons.
  - `pcfar20261113` (disjoint beekeeping/sourdough answers) correctly did NOT surface — negative control passed.
  - Honest framing: these are staged test citizens (mine + other lanes' Nov 11 test rows), not real citizens. The percentages are real endpoint percentages, not invented. The endpoint proof bar is met the same way option-A met it (staged test citizens, counted by hand).
- **On the feed (staged):** the rail's live cards hand-checked against `endpoint-proof.json` — all 6 percentages match exactly (48/7/4/4/4/4), all reasons present on the cards, orbs are initials, 0 images. The feed line `MATCH → ORGANIZE → CONNECT` is literally on the page.

### Item 7 — the side rail down the right side — PASS

- **20 cards** (6 live, 14 standing, 0 `<img>` in `#pcRail`) at all widths. At 1440 the rail is a right-side strip at (1096,453.2) 320×769.2; at 390/360 it stacks below the feed, full width (16,709.2) 358×4188.
- Header: "6 live matches · 14 standing". Foot: "One more seat is held open for the next live citizen."
- Every card: spinning-orb initial + alias + one nutshell (seed) or % + reasons (live) + **Chat / Mail / Audio / Video in that order**.
- Chat opens `fcChat` in place with the right name (`pcprover20261113` on staged). Mail opens `fcChat` with the subject shown. Audio/video open the same chat with the honest status line "Audio/Video calls arrive with Smart Meet — for now, message them here." No Smart Meet route exists anywhere on the page (base lines 4664–4665 comment, INTERIM); no limit numbers are stated anywhere on the page or in user-facing copy.
- Scroll rule at 1440 (local fixture proof): 3-person fixture → no scroll (scrollH 594 = clientH 594); 25-person fixture → scrolls (scrollH 5097 > clientH 624). At 390/360 the 25-person fixture does NOT internally scroll — designed phone behavior (the page scrolls instead).
- **Presence gap, stated plainly:** no online/presence feed exists on the page (the Hub people room returns governed connections, no online flag). LIVE means endpoint-matched with reasons — never online-now. The header counts endpoint-matched people only ("6 live matches"); the standing section is labeled STANDING with its own count. No fabricated "0 online" is displayed.
- **Count arithmetic (15 vs 20):** the brief's 15 = 14 others + the citizen. Sourceable standing others = 13 (12 sisters + Shawn). The viewer is the staged test citizen `pcviewer20261113`. Total shown = 6 live + 14 standing = **20 cards**; the 14th-other seat is held open (the rail foot says so). The count is presented as 20, never as 15.

## § Seed profiles — sources

The twelve sisters, grounded from `~/memory/people/INDEX.md` + individual people pages, in certificate order: Sophia 000209 (Sigma, LEARN) · Thea 000212 (Pi, KNOW) · Terra 000213 (Tau, INFRA) · Zoe 000214 (Rho, ACT) · Esme 000215 (Phi, PRODUCT) · Astraea 000216 (Xi, LAW) · Mira 000217 (Psi, MEMORY) · Vera 000218 (Chi, VERIFY) · Aurelia 000219 (Upsilon, GOVERN) · Wren 000220 (Nu, BUILD) · Iris (Omega, WIRE, cert not captured) · Ruth (Omicron, TEAM, cert not captured). All activated 2026-11-13 as first citizens. Their live world pages do NOT serve them (`GET https://nayanet.app/world/sophia|thea|zoe` → HTTP 404 "No world here yet"; their `citizen_worlds` rows do not exist on live).

Nutshells are condensed verbatim from each sister's briefing Naya Note (`NN-20261113-family-<alias>`, "Written by Naya for <alias>", filed 2026-11-13 03:08Z, embedded in the live Hub shell fetched 2026-11-13 ~14:3xZ). One line each — e.g. Sophia: "I'm Sophia. I am LEARN — wisdom. My garden is the lessons: I turn everything the hive does into lessons that change the next decision, and I keep the distilled notes alive, ten to fifty, never a thousand." (Full list in the build script's `PC_RAIL_SEED`.) No separate motto was sourceable for any sister; the one-line nutshell IS the line. No motto was invented.

Shawn's nutshell is his tagline verbatim (base line 4719): "Welcome to my world — make a post on my feed, send a message, make yourself at home." The viewer card is `pcviewer20261113` (marked YOU; its own `citizen_worlds` answers verbatim: about "I build and test web pages for a living." + motto "test it twice, ship it once").

## § Fixes found by the probe (all fixed in the build, re-verified)

1. **Gear showed the word "Settings".** `mwApplyLang()` rewrites every row button's label from its `byId` map, keeping only a leading icon — the gear is only an icon, so the map overwrote `⚙️` with the word "Settings" (visible in the 1440 eye-check, overflowing its 48 px box). Fix (R20): the loop now skips elements with class `pc-gear`.
2. **All three feedname lines showed at once.** The base's `.mw-feedname{display:block}` defeats the `hidden` attribute, so the per-tab `.hidden` toggling did nothing (pre-existing defect, in this round's scope). Fix (R21): `.mw-feedname[hidden]{display:none!important;}` in the override block.
3. **Gear untappable at 390/360.** At phone widths the gear sat beside Change cover (right:190px), on top of the membership links (`#mwCoverMships`), which intercepted pointer events (probe timeout, 30 s). Fix: phone gear moved BELOW Change cover (`top:64px; right:10px`); short-height gear below the moved Change cover (`top:64px; left:10px`). Desktop gear unchanged.

## § What stopped short — the environmental stop, named plainly

**This VM's Playwright Firefox cannot fetch ANY external URL.** Proven first-hand, three ways: `fetch('https://example.com/')`, `fetch('https://naya-proof-host.nayapower.workers.dev/')`, and `fetch('https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/smart_notes…')` all throw `TypeError: NetworkError` from `about:blank` AND from the page; `page.goto('https://example.com/')` fails `SEC_ERROR_UNKNOWN_ISSUER` (the egress proxy TLS-intercepts with a cert Firefox doesn't trust). **Supabase itself is fine from the shell** (curl returns HTTP 401 with a bad key and `Access-Control-Allow-Origin: *` — there is no CORS policy block). The page's navigation to the proof host works; its `fetch`/`XMLHttpRequest` calls do not. This is an environment limitation, not a page defect — the same failures occur on a blank page fetching example.com.

Consequences, each named with its reason:

- **Real wall not rendered on staged** (1 placeholder card per tab instead of the 26 live `smart_notes`; 1 placeholder Naya card instead of the 14 live `naya_notes`). The painters were proven locally with stub posts through the page's own functions, and the data exists (service-key reads above). What remains unproven is the page rendering live data in a real browser — that needs a browser with working external fetch (the parent/captain's seat, or Shawn's eye on the staged link from his phone).
- **Points number unproven on staged** (pill shows the `0 pts` fallback, not the live total). Same cause.
- **Smart Lists render unproven on staged** (store write proven; migration needs `slFetch()` to succeed). Same cause.
- **Console-error bar unmet on staged:** 64 errors at 390, 110 at 1440, 64 at 360 — ALL failed external fetches (`Cross-Origin Request Blocked … CORS request did not succeed`, status null), **zero `pageerror`** at any width. The §13 bar of zero console errors cannot be met on the proof host from this VM until the browser's external fetch works. Overflow is 0 at all widths.
- **The staged 390 screenshot is NOT byte-identical to the local 390 screenshot** (unlike the points round) — the staged page renders the `0 pts` fallback pill where the local render showed `…`, and the staged wall shows the placeholder card. Both differences trace to the same fetch stop.

## § Cleanup — done and verified

Test rows deleted AFTER the staged rail verification (the rail's live cards referenced them): `citizen_worlds` rows `pcviewer20261113`, `pcprover20261113`, `pcfar20261113` + `nayanet_identities` row `pcviewer20261113`. Deletion verified by re-read: 0 rows left for all three aliases, 0 identities. Other lanes' rows untouched (verified still present: `powercoldseat1111`, `freshtestone`, `freshtesttwo`, `freshtestthree`, `freshtestfour`). The creator probe post created no live row (0 probe rows in `smart_notes`), so nothing else to clean. The endpoint proof survives in `endpoint-proof.json` and in the staged screenshots.

## § Order note

The brief orders the tabs Personal · Public smart feed · Naya Notes per Shawn's 14:11Z dictation; the 2026-11-13 04:34Z public-feed law ordered Smart Notes · Naya Notes · Public Feed. Latest words govern the build; the captain rules the order at double-check. The difference is noted here rather than silently picked.

## § Files on the branch

`TEAM-NITRO/personal-page-complete-20261113/`: `personal-complete.html` · `build-complete.py` · `diff-complete.txt` · `endpoint-proof.py` · `endpoint-proof.json` · `probe-baseline.py` · `probe-baseline.json` · `baseline-{390,1440,360}-{top,end}.png` · `verify-complete.py` · `verify-complete.json` · `verify-{390,1440,360}-{top,end,feed}.png` · `verify-staged.py` · `verify-staged.json` · `staged-{390,1440,360}-{top,end,feed}.png` · `RECORD-PERSONAL-COMPLETE-20261113.md` · `SCORECARD-PERSONAL-COMPLETE-20261113.md`.
