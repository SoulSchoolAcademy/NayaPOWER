# RECORD — Personal page complete round (2026-11-13)

## What it is

Shawn's seven-item Personal list, built on the points base and proven on the staged page he can open. One page, one round, the whole list — not one item alone.

- **Branch:** `personal/personal-page-complete-20261113`, off main tip `8f2af988b2a4adefda9afb8ad752c7971c10ea8c`, worktree `~/workspace/personal-complete-wt`.
- **Base:** the points round's `personal-points.html`, SHA `eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95` (1,486,494 B), verified by `sha256sum` in three places before editing. The base is live Personal (SHA `992ab18c…`) + points pill + wiring + hero-fix block.
- **Built file:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`, 1,544,351 B, SHA `ec5c4cce083708fa6ea301da45e8097e35174cdffc8216910c8953f70b4ba281` (local, after the Sharpening 2 pill restyle; pre-restyle SHA `87d03847…`, 1,536,733 B). The staged SHA is re-read fresh in the staged re-verification below.
- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=<commit-sha> (fresh `cb` per read; the exact link with the restyle commit's SHA is in § Sharpening 2 staged re-verification).
- **Commits:** `b0a792186` (page + build + probes + screenshots, 16 files) · `f925e6e6e` (staged verification + record + scorecard, 13 files) · `1aa927583` (Sharpening 2 pill restyle + updated record/scorecard, 13 files) — all pushed, branch verified on the remote at `1aa9275834f2333d92184643dd399f2f292404c7` (see push below). This final record touch-up (staged pill numbers) is committed after.
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
- Consequence, ~~struck in the follow-up round (2026-11-13, checker Defect 1 — the statement below was FALSE)~~: ~~hiding the two floating pluses strands the right (ecosystem) drawer — only `#os-rooms-plus` and `#os-eco-plus` open the drawers. The left drawer stays reachable via the bottom-bar Spaces seg.~~ **THE TRUTH (follow-up correction): hiding the two floating pluses stranded BOTH drawers — the left drawer (`#os-drawer`, rooms) opens ONLY from hidden `#os-rooms-plus`, and the right drawer (`#os-drawer-right`) ONLY from hidden `#os-eco-plus`. The left drawer was NEVER reachable via the bottom-bar Spaces seg: the seg's handler set `window.location.href = 'https://nayanet.app/#/hub/spaces'` (staged line 13844) and navigated away — the checker tap-tested it at 360 and the page left the proof host. The follow-up restores an opener per drawer in the bottom bar (Spaces seg → left drawer in place; new ECO seg → right drawer) — see § Follow-up round below.**

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

Nutshells are condensed verbatim from each sister's briefing Naya Note (`NN-20261113-family-<alias>`, "Written by Naya for <alias>", filed 2026-11-13 03:08Z, **filed notes on main — `BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13/NN-20261113-family-<alias>.md`**). ~~Correction (follow-up round): the record previously said the nutshells were "embedded in the live Hub shell" — that is FALSE. The checker grepped the Hub shell file and the live Hub shell: the nutshell text and the `NN-20261113-family-*` IDs appear in NEITHER (0 hits). The source is the filed notes on main, verified verbatim by the checker for Sophia, Thea, Vera.~~ One line each — e.g. Sophia: "I'm Sophia. I am LEARN — wisdom. My garden is the lessons: I turn everything the hive does into lessons that change the next decision, and I keep the distilled notes alive, ten to fifty, never a thousand." (Full list in the build script's `PC_RAIL_SEED`.) No separate motto was sourceable for any sister; the one-line nutshell IS the line. No motto was invented.

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

## § Sharpening 2 — pill restyle (received 15:01Z, applied after the first verification)

Shawn's decision on the points presentation: JUST RESTYLE THE PILL. No tile under the picture. Confirmed received and applied.

**What changed:** the points pill beside the name now wears the Dashboard's number treatment — tiled digits on top, a gauge line underneath (the hero gauge cluster order: number on top, gauge underneath). The pill's PLACE (beside the name at desktop, wrapping below the name at phone width — the F3 geometry stands) and its live WIRING (the points-round write into `#pointscount`, untouched byte-for-byte) survive; only the STYLING is restyled. No tile under the picture — the restyle is the pill only. Space and Business inherit the restyle when they are rebuilt from the new Personal bytes; this round touches Personal only.

**Harvest — live Dashboard pass-10, re-curled and verified first-hand:** https://nayanet.app/dashboard, HTTP 200, 1,817,928 B, SHA `bb41114dcca4cedd42c99d2ccc9111625e0f4bb91dc94d4138c8067ad901076c` (saved as `dashboard-pass10-bb41114d.html` in this lane dir). There is no local pass-10 file (the dashboard-pass10-20261110 dir holds a pass-9 backup only), so the live bytes are the harvest source. Sites, file + line in `dashboard-pass10-bb41114d.html`:
- Tiled-digit system: `.os-mini-num` / `.os-mini-tile` / `.cap` / `.rd` base, lines 4759–4762; digit colours `.d0`–`.d9`, lines 4783–4802 (d0 white, d1 red #ff2a2a, d2 orange #ff8c00, d3 gold #f5d76e, d4 green #00a86b, d5 blue #29b6f6, d6 indigo #3f51b5, d7 purple #8e24aa, d8 light purple #b388ff, d9 pink #ff1493 — a digit's colour is its digit's colour); group gap `.os-mini-gap`, line 4774; phone shrink (20px tiles, 19px digits), ~4803–4812.
- Converter: `miniTileHTML` / `_osMiniNumHTML`, lines 25613–25638 (commas become gaps, space separator); `_osSpc`, lines 25141–25146 ("1 293").
- Lap position: `dialPos(v)`, line 23193 — `v<=0 → 0`, else `((v-1) % 500) + 1`; lap = ceil(total/500). The gauge fill is `dialPos(total)/500`.
- Gauge cluster order: number `#os-se-val` line 4975 on top, gauge `#tn-tacho-mount` line 4999 underneath; lap line `.tn-tacho-lapline` line 2902.
- The bar for the top-tile digits (PASS-9, lines 4832–4846): 68px digits in 72px tiles at orb size.

**Scaling decision, stated plainly:** the Dashboard's 68px/72px orb tiles cannot fit a pill beside the name, so the pill wears the same tile system at the Dashboard's small size (30px tiles, 27px digits; 20px/19px at phone width per the harvested shrink rule). Same system, same font, same colours — only the size is pill-scaled. The captain can rule otherwise at double-check.

**How it is built (`build-pill-restyle.py`, 3 diff hunks in `diff-pill-restyle.txt`):** (1) a `<style id="pill-restyle-20261113">` block with the harvested tile CSS scoped under `#pointsdisplay` + the pill's column layout (number row on top, gauge line below); (2) the pill markup becomes a number row (`✦` + `#pointscount` + `pts`) over a gauge line (`#pcPillGaugeFill` inside `.pc-pill-gauge`); (3) a tiler script (pc-prefixed copies of the harvested converter + `dialPos`) that watches `#pointscount` with a MutationObserver and re-presents whatever the wiring writes as tiles, driving the gauge fill from the same total. The wiring lines are asserted untouched in the build. The loading glyph `…` stays plain (no tiles, fill 0%).

**Re-verification (local, Playwright Firefox, `verify-pill.py` → `verify-pill.json`, screenshots `pill-{390,1440,360}-top.png` + `pill-{1440,390}-wide.png`):** the wiring write was simulated by setting `#pointscount` textContent to `(1293).toLocaleString()` — the same write the points wiring performs — so the observer + tiler path is exercised.

**Staged re-verification (`verify-staged-pill.py` → `verify-staged-pill.json`, screenshots `staged-pill-{390,1440,360}.png`):** staged file re-read fresh via curl — HTTP 200, 1,544,351 B, SHA `ec5c4cce083708fa6ea301da45e8097e35174cdffc8216910c8953f70b4ba281`, byte-identical to the local file. Staged link: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=1aa9275834f2333d92184643dd399f2f292404c7. On staged, the simulated wiring write (1293) renders 4 digit tiles (`d1`,`d2`,`d9`,`d3`) + 1 gap with gauge fill **58.6%** and d1 border rgb(255,42,42) at all three widths — identical boxes to local (pill 1440: (357.6,286.2) 226.4×68; 390: (146,404) 180.4×60.1; 360: wraps below at (16,534)). No overlap at any width, overflow 0, pageerrors 0. Eye-check (`staged-pill-1440.png`): tiled 1-2-9-3 with digit colours + gold gauge line at ~58%, pill clean beside the name. Regressions: buttons equal, segs `['plus','mail','activity','spaces']`, tabs, feedline, rail 20 cards / 0 imgs. Console errors 42 per width on this run — all the same failed external fetches (environmental stop, § What stopped short), zero `pageerror`. The live number itself is still unproven on staged for the same reason (the pill shows the tiled fallback until the ledger rows land).
- "1,293" → 4 digit tiles (`d1`,`d2`,`d9`,`d3`) + 1 gap, at all widths; d1 border rgb(255,42,42), d9 border rgb(255,20,147) — the digit colours live. Gauge fill **58.6%** = dialPos(1293)/500 = 293/500, at all widths. Fallback "0" → 1 tile (`d0`), fill 0%.
- Pill place: beside the name at 1440 (x357.6, 14px gap from the name, same as before); below the name at 390 (y404); at 360 the narrow loading pill sits beside the name (189.6,480) and the wide tiled pill wraps below (16,534) — the flex-wrap doing its job. Pill height 46 → 57 (loading) / 60–68 (tiled).
- Overlap: pill vs name, vs tagline, vs Change cover, vs gear — all False at all widths. Overflow 0, pageerrors 0.
- Eye-check (`pill-1440-wide.png`): ✦ + 1 (red) 2 (orange) 9 (pink) 3 (gold) + pts on top, the gold gauge line underneath stopping just past halfway, pill clean beside the name, tagline clear below. No tile under the picture.
- No regressions: buttons equal, segs `['plus','mail','activity','spaces']`, tabs Personal / Public / Naya Notes, rail 20 cards / 0 imgs, gear `⚙️`, seg shadow the A-fix.
- **Built file after the restyle:** 1,544,351 B, SHA `ec5c4cce083708fa6ea301da45e8097e35174cdffc8216910c8953f70b4ba281` (staged SHA below supersedes `87d03847…`).

## § Files on the branch

`TEAM-NITRO/personal-page-complete-20261113/`: `personal-complete.html` · `build-complete.py` · `diff-complete.txt` · `endpoint-proof.py` · `endpoint-proof.json` · `probe-baseline.py` · `probe-baseline.json` · `baseline-{390,1440,360}-{top,end}.png` · `verify-complete.py` · `verify-complete.json` · `verify-{390,1440,360}-{top,end,feed}.png` · `verify-staged.py` · `verify-staged.json` · `staged-{390,1440,360}-{top,end,feed}.png` · `RECORD-PERSONAL-COMPLETE-20261113.md` · `SCORECARD-PERSONAL-COMPLETE-20261113.md` · `build-pill-restyle.py` · `diff-pill-restyle.txt` · `dashboard-pass10-bb41114d.html` · `verify-pill.py` · `verify-pill.json` · `pill-{390,1440,360}-top.png` · `pill-{1440,390}-wide.png` · `verify-staged-pill.py` · `verify-staged-pill.json` · `staged-pill-{390,1440,360}.png`.

---

## § FOLLOW-UP ROUND (2026-11-13, after checker PASS 8/10 — build 9/10, proof 8/10)

Round 1 landed maker DONE 9/10 build / 8/10 proof + checker PASS 8/10 — below 9, so it went back in. This is the follow-up: Defect 1 fixed, both record corrections struck above, the Public tab widened to the collective with the keyword pull, and the four fetching-browser sub-proofs prepared as the captain's leg. Captain's rulings carried as written: **tab order KEEP AS BUILT** (Personal · Public smart feed · Naya Notes — Shawn's 14:11Z dictation governs; the 04:34Z ordering is superseded); **presence: "live" means endpoint-matched, honestly labelled** (seed cards never carry a live-online indicator; head count counts live-only).

- **Branch:** `personal/personal-page-complete-20261113`, tip `a7b55ab5bf75cc973c9ec435b3e8c1e7c45f1067` before this round.
- **Built file after the follow-up:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`, 1,555,404 B, SHA `4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666` (local). Staged SHA re-read fresh via curl: `4872414a…`, 1,555,404 B — byte-identical to the local file.
- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=bab47fb67 (fresh `cb` per read in verification: `bab47fb67-w<width>`).
- **Commits:** `bab47fb67` (follow-up build + probes + scorecard, 18 files, pushed — remote tip verified `bab47fb67` by `ls-remote`) · the record/scorecard touch-up follows as a second commit.
- **Build:** `build-followup.py` (15 hunks, `diff-followup.txt`) + `build-followup2.py` (4 hunks, `diff-followup2.txt` — the re-tap restoration found by the first probe run). Base SHA asserted `ec5c4cce…` then `31890cf1…` — the base file was edited, never rebuilt.
- **Live untouched:** live Personal re-curled unchanged — SHA `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50` (1,484,185 B). Live Hub shell `0c8628d5769c10e6462ee31490f12e3bca6eb4f472854215ff1979a8c782ad27` (620,595 B). No live page, merge, deploy, or PR. No live writes except the three fixture rows below, left in place for the captain's leg.

### 1. Defect 1 — both drawers stranded — FIXED, tap-tested at 390 / 1440 / 360

**What was wrong (the truth, replacing the struck mitigation):** hiding the two floating pluses stranded BOTH drawers. `#os-drawer` (left, rooms) opened only from hidden `#os-rooms-plus`; `#os-drawer-right` (Smart Factory + memberships) only from hidden `#os-eco-plus`. The bottom-bar Spaces seg never opened the left drawer — its handler navigated away to `https://nayanet.app/#/hub/spaces`.

**The fix (one toggle, one path):** `window.pcToggleDrawer(side)` exposed from the drawer IIFE; the hidden plus buttons reuse it. The bottom bar gains a fifth seg: **Spaces seg → left drawer in place** (the navigation line is gone — `window.location.href = 'https://nayanet.app/#/hub/spaces'` appears 0 times in the file now) and a new **ECO seg → right drawer** (four-square factory glyph, page's own SVG language). Segs, in order, at all widths: `['plus','mail','activity','spaces','eco']`. Exactly one `+` still visible (the bar seg); `#pluswrap`/`#os-rooms-plus`/`#os-eco-plus` all still `display:none`.

**The re-tap, found by the probe:** the first probe run proved the open, then failed the re-tap close — the scrim (z-index 950) covers the bar (base z-index 45) entirely, so no seg could be re-tapped while a drawer was open. The original design handled this: the floating plus rose above the drawer when open (z-index 970, icon rotated to an ×). Pass 2 restores it in the bar's language: while a drawer is open the bar rises to z-index 955 (above the scrim 950, below the drawer 960), the open drawer's seg lights in its own colour (`.pc-open`, the `has-news` treatment), and tapping any other seg closes the drawer first. The document-click closer exempts the two drawer segs so an open never eats its own tap.

**Measurements (local + staged agree; staged in `verify-staged-followup.json`, local in `verify-followup.json`):**

| Width | Spaces tap | Left drawer | ECO tap | Right drawer | Close paths proven |
|---|---|---|---|---|---|
| 390 | URL unchanged | open, box (0,0) 300×844, visible | URL unchanged | open, box (90,0) 300×844, visible | backdrop tap ✓, Escape ✓ |
| 1440 | URL unchanged | open, box (0,0) 300×844, visible | URL unchanged | open, box (1140,0) 300×844, visible | backdrop tap ✓, Escape ✓, **re-tap ✓** |
| 360 | URL unchanged | open, box (0,0) 300×844, visible | URL unchanged | open, box (60,0) 300×844, visible | backdrop tap ✓, Escape ✓ |

- At 390/360 the drawer still covers the bar geometrically (full-height drawer, F4 geometry — pre-existing), so the seg re-tap is reachable only at desktop; phone closes via the scrim tap or Escape. That is the design, stated here rather than hidden.
- Eye-check (`followup-390-drawer-left.png`): drawer open in place, "NAYANET AREAS", 8 links as elevated boards, page dimmed behind. Eye-check (`followup-1440-search-garden.png`): the five segs visible in the bottom bar (plus, mail, activity, house, grid).
- Five segs fit: 50px tiles at 390/360 (x 46/108/170/232/294 at 390; 31/93/155/217/279 at 360) and 66px at 1440 (x 487–887); overflow 0 at all widths. The phone tile shrink (54→46px at ≤400px, still above the 44px tap floor) is the only bar change.

### 2. Record corrections — DONE (struck above, in place)

(a) The drawer mitigation is struck and the truth stated: both drawers were stranded; the left drawer was never reachable via the bottom-bar Spaces seg. (b) The seed source is corrected: the sister nutshells are verbatim from the filed briefing notes on main (`BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13/NN-20261113-family-<alias>.md`), NOT "embedded in the live Hub shell" (0 hits in the Hub shell file and the live Hub shell — checker-verified).

### 3. Public tab — widened to the collective + keyword pull — BUILT, proven with stubs + real rows

**The widening:** the owner's burst read (`osNotesRows`, owner-scoped) is untouched. The Public tab now loads a second read — `pcLoadPublicWall()`: `smart_notes` with NO owner filter, newest 500, through the same client the wall uses — and the painter keeps two stores (owner vs collective), so the Public tab never overwrites the owner's store (proven: Personal shows 2 owner cards after a Public visit). The P6 verification filter is reused verbatim, so no verification artifact renders in the collective either. The ribbon grows from the collective on the Public tab (author pills from other citizens).

**The keyword pull:** the search at the top of the feed is the existing centered popup, not a new bar. **Hub-search finding, stated plainly:** the Hub shell file (`hub-index-main-8f2af988.html`) carries NO search identifiers at all — 0 hits for `NayaSmartBar`, `nsbSearch`, `Search the network`, `openSearch`, `onSearch` — so there is no Hub search to harvest from the shell. The search mechanism as it stands is the one already on this page: the Smart Bar search level (`#nsbSearchLevel`) as a centered popup (`openSearchModal`, popup-only law) with the host hook `NayaSmartBar.onSearch`. The follow-up wires that hook: typing in the popup pulls the Public feed to that keyword (`pcSetPublicKeyword`), the dropdown lists the matching notes, clicking a result closes the popup onto the already-pulled feed, clearing the popup's field clears the keyword. The one new control is a **Search button at the top of the feed** ("🔍 Search the public feed", the page's own primo pill) that opens the existing popup on purpose — no visible search bar was invented, per the popup-only law. The keyword filter lives in the painter (500-row client filter over the loaded collective), and the meta line says so ("Matching “garden”.", textContent — a typed keyword can never inject markup).

**Proof (local + staged, stubs = the real table rows):** the collective as the table holds it is 6 renderable cards across 4 voices — the 3 fixture rows below + Chi DV Spc + Chi DV Biz + the heartbeat Guest row. Personal shows the owner's 2 stubs only; Public shows 6; ribbon `['All','Follow-Up Tester','Chi DV Spc','Chi DV Biz','Guest','+ Add']`.

| Step | Cards | Meta |
|---|---|---|
| Public, no keyword | 6 | "6 posts on this feed — the newest landed just now, across 4 voices." |
| Type `garden` in the popup | 2 | "…across 1 voice. Matching “garden”." (dropdown: 2 results) |
| Type `harvest` | 1 | "1 post on this feed — … across 1 voice. Matching “harvest”." |
| Clear the field | 6 | back to 4 voices |
| Back to Personal | 2 | owner store intact |

Eye-check (`followup-1440-search-garden.png`): centered popup with "garden" typed, tagline "Search the network — get intelligence, learn, grow, connect.", two matching results ("Follow-Up Tester · public feed"), the Public tab active behind it with the feed pulled to 2 posts.

**Fixture rows (left for the captain's leg — NOT deleted):** three `smart_notes` rows, alias `pcfollowup20261113`, author "Follow-Up Tester", inserted via service key and read back (3 rows):

| id | Content (keyword) |
|---|---|
| `25ea46ec-e293-4ef3-b2c6-4da79935c3b6` | "Follow-up keyword test — garden notes: I grow tomatoes and herbs in the garden, and I trade cuttings with neighbours." |
| `3f9bcbda-0387-4e61-9e06-615cf12fb3ae` | "Follow-up keyword test — garden tools: my favourite garden tools are the hand fork and the watering can." |
| `41fba108-fac6-4742-9736-e7808abdddb0` | "Follow-up keyword test — harvest morning: we picked the harvest at sunrise and shared the baskets." |

Cleanup owed AFTER the captain's leg proves (do not delete before): delete these 3 rows by id, verify 0 rows left for `pcfollowup20261113`, other lanes' rows untouched (`powercoldseat1111`, `freshtestone`, `freshtesttwo`, `freshtestthree`, `freshtestfour` — all still present, verified in round 1; re-verified at cleanup time). The round-1 test rows (`pcviewer20261113`, `pcprover20261113`, `pcfar20261113`) are still 0 rows — nothing was re-created for them.

**What the collective really holds (service-key truth, for the captain's leg):** `smart_notes` for `flagship-personal` = 26 rows, kinds board-open 2 / aboutsec 6 / connect 10 / wall 4 / profile 4 — and **all 4 of the owner's wall-kind rows are P6-filtered verification artifacts** (Smart Score ladder, `CHI-VERIFY-WALL-20261021-2336-B2`, "Proof post from the flagship verification run", `[[fm-auto]]`), so the live Personal wall honestly renders **0 cards** — the staged wall shows the "No posts yet — be the first to make a post on this feed." placeholder (measured on staged at all widths). The collective's other renderable rows are the 3 above (Chi DV Spc, Chi DV Biz, heartbeat) + the 3 fixtures = 6. **Corrected expectation for sub-proof (a):** the "26 rows present" is the table count, not 26 rendered cards — the Personal wall renders 0 by the page's own filter, and the Public wall renders the 6 collective cards.

### 4. Found while preparing the leg — Naya Notes could never load — FIXED in mechanism

`mwLoadNayaFeed` resolved its client as `window.getSb ? window.getSb() : null` — but `window.getSb` is never assigned anywhere in the file (0 assignments; the two bare `getSb()` functions live in other IIFEs), so the Naya Notes tab could never load on ANY browser, fetching or not. The follow-up applies the same NayaAuth-first resolution the Lists room already uses (line ~22221). Mechanism proven locally with a fake `NayaAuth.client` returning 2 rows through the real loader: the Naya panel renders both ("Naya test one", "Naya test two"). The live 14-row render is the captain's leg (a).

### 5. The captain's leg — the four fetching-browser sub-proofs (NOT claimed — procedure below)

This VM's Firefox is fetch-blind (NetworkError + `SEC_ERROR_UNKNOWN_ISSUER`, environmental — reproduced by both seats on a blank page). Staged console errors here are 42 @390, 60 @1440, 42 @360 — ALL "Cross-Origin Request Blocked" failed fetches, **0 `pageerror`** at any width. The four sub-proofs need the captain's cloud browser (which reaches staging fine) or Shawn's phone on the staged link below.

**Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/personal-page-complete-20261113&cb=bab47fb67 (fresh `cb` per read; staged SHA `4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666`, 1,555,404 B — re-read fresh before starting).

**(a) Live wall renders.** Open the staged link, wait 4 s. Personal tab: expect the "No posts yet" placeholder, **0 cards** — the owner's 4 wall rows are all P6-filtered (see §3 above); the 26 `smart_notes` rows are present in the table (kinds board-open 2 / aboutsec 6 / connect 10 / wall 4 / profile 4). Public tab: expect **6 cards** across 4 voices — 3 "Follow-Up Tester" rows + Chi DV Spc + Chi DV Biz + heartbeat Guest. Naya Notes tab: expect **14 rows** (owner `naya_notes` = 14, service-key count). If the Public tab shows only the owner's rows (or 0 cards), the collective read is RLS-blocked at the policy layer — record that as the reason; the fix would be a policy change (Shawn's hand), not a page change. **0 probe rows:** `smart_notes` must contain 0 rows with the round-1 probe texts ("Probe — personal complete check", "Checker probe").

**(b) The points number shows a live number, not the `…`→`0` fallback.** The pill beside the name must show tiled digits with a live total. Expected total **245** (the points round's proven donut total — the undoubled orb sum; gauge fill `dialPos(245)/500` = 49.0%). If it shows another number, record it and cross-check against the live Dashboard hero total for `flagship-personal` — the pill follows the donut total, so a mismatch there is the points round's, not this round's. `…` then `0` = the fetch stop, not a pass.

**(c) Smart Lists render.** On the staged link: save a note from the feed (SAVE on any wall card — the store write is proven here: `localStorage['naya.smartlist']` gains the item), then open the Lists room. Expect the saved note to appear under **"Saved on this device"**. (Mechanism note: the migration into that list runs only after `slFetch()` succeeds, so this leg proves the fetch path end to end.)

**(d) Zero console errors.** On the fetching browser: **0 console errors and 0 page errors** at 390/1440/360. The 42/60/42 errors seen here are all failed external fetches from this VM and must be 0 there. Any error that appears there is a real page error — record its text, do not explain it away.

**Then:** delete the 3 fixture rows (ids in §3), verify 0 rows left for `pcfollowup20261113`, and file the result before the page is called done-done.

### No-regressions leg

Diffed the follow-up file against the round-1 staged bytes (SHA `ec5c4cce…`): pass 1 = 15 hunks (`diff-followup.txt`), pass 2 = 4 hunks (`diff-followup2.txt`). Every hunk maps to Defect 1, the Public widening, the search wiring, or the Naya client fix; no other hunks. Re-proven on staged at 390/1440/360 (`verify-staged-followup.json`): 8 buttons equal ±0 px (110 @390, 147 @1440, 160 @360), gear `⚙️` only, name never intersects Change cover, pill present (`…` fallback — the number is the captain's leg (b)), tabs Personal / Public smart feed / Naya Notes in order, feed line literal, composer 0 cards, rail 20 cards / 0 `<img>`, segs `['plus','mail','activity','spaces','eco']`, seg shadow the A-fix (no inset white top line), overflow 0, pageerrors 0. The Hub harvest source is untouched. Live Hub and live Personal bytes unchanged (re-curled above). No new network calls beyond the one collective read, no new secrets, no new grants, no files outside the lane branch.

### § Files on the branch (follow-up additions)

`TEAM-NITRO/personal-page-complete-20261113/`: `build-followup.py` · `diff-followup.txt` · `build-followup2.py` · `diff-followup2.txt` · `SCORECARD-FOLLOWUP-PERSONAL-COMPLETE-20261113.md` · `verify-followup.py` · `verify-followup.json` · `followup-{390,1440,360}-{top,drawer-left,drawer-right}.png` · `followup-1440-search-garden.png` · `verify-staged-followup.py` · `verify-staged-followup.json` · `staged-followup-{390,1440,360}-top.png`.
