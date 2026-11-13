# RECORD — BOTTOM ICONS ROUND: round black circles + ultimate trio gems
## 2026-11-13 · Maker seat · Branch `bottom-icons/ultimate-trio-20261113`

**Bullseye (one line):** the bottom bar on every page reads as nice round black circles, and the very bottom carries the three ultimate gems — amethyst Personal, emerald Business, diamond Thing — the doors to their worlds, with the bar never covering content at phone size.

**Shawn's order (dictation ~03:58Z + 04:01Z ruling):** "the bottom icons are wrong — the ones with the squares; all the colors should just be those nice round black ones; make the ultimate icons for the very bottom too — Personal, the business or job, and their space; Personal, work, and thing." **04:01Z law:** the sisters' Personal pages are the Personal page EXACTLY, plus a cover — no custom pages. **04:16Z sharpening:** everybody gets the SAME world — just different labels; universal, not sisters-only. **04:21Z Billion-Dollar Home law** (arrived during the round): work ON the product we have, never create a new one; harvest, never invent.

**Branch:** `bottom-icons/ultimate-trio-20261113`, created FIRST from main tip `26b1a0e6135a9296ce28781ce2480a938428320f` (re-read first-hand via `git ls-remote` before branching). Main tip moved twice during the round (→ `ceef98b7…` 04:36Z, → `ad608c48…` ~04:52Z); the branch base is unchanged, as briefed. No merge, no PR, no live touch, no mail.

**Files filed on the branch** (`TEAM-NITRO/bottom-icons-ultimate-trio-20261113/`, all HTTP 201 + GET read-back verified):

| File | Bytes | sha256 | Blob SHA |
|---|---|---|---|
| personal-fixed.html | 1,488,772 | `5e5d29fce1129182fac255ece2ae9b963d40870ea384ec3616103661ab464c51` | `ab90567d26d95b22101e93c3d433b61ddc9642b8` |
| hub-fixed.html | 5,018,313 | `499b6f408bd4aeed384afb7456d0a8ff4ddec0d8b8e8f7cd9aa08ab94a1a4e36` | `529326daa693e2b820f1875710b2356d69a23431` |
| business-fixed.html | 835,219 | `8142a734391e2d01376109db2be1c33e54e30551d0bec8f310638842de5fa1de` | `38b08efbd058d335ff8c417007f7db2d80dd4a14` |
| space-fixed.html | 867,544 | `2aaf2a0a9c07e9526b97ef8ff2c414acf739cd5f9dc7e6e2a4be2baf20c916da` | `232f15469301b4cd508330a2667a0dc2658f67cb` |

**Staged links (proof host, NEW ref, `cb` = blob SHA):**
- Personal: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/bottom-icons-ultimate-trio-20261113/personal-fixed.html&ref=bottom-icons/ultimate-trio-20261113&cb=ab90567d26d95b22101e93c3d433b61ddc9642b8
- Hub: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/bottom-icons-ultimate-trio-20261113/hub-fixed.html&ref=bottom-icons/ultimate-trio-20261113&cb=529326daa693e2b820f1875710b2356d69a23431
- Business: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/bottom-icons-ultimate-trio-20261113/business-fixed.html&ref=bottom-icons/ultimate-trio-20261113&cb=38b08efbd058d335ff8c417007f7db2d80dd4a14
- Space: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/bottom-icons-ultimate-trio-20261113/space-fixed.html&ref=bottom-icons/ultimate-trio-20261113&cb=232f15469301b4cd508330a2667a0dc2658f67cb

**Evidence in the work dir** (`~/workspace/team-nitro/bottom-icons-ultimate-trio-20261113/proof/`): `audit-{personal,hub,business,space}-fixed.json` (+ 1440/390/360 screenshots), `proof3-bottom-icons.json` (Hub cover after fix, pill popups, guard), `staged-proof.json` (staged bytes/sha + staged render), `file-receipt-bottom-icons.json`, `bar-{personal,hub,business,space}-1440.png` (cropped bar shots), `gate-strip-1440.png`, `staged-bar-*-1440.png`. **Runtime note (honest):** a runtime restart at ~04:57Z wiped `/tmp`, taking the first runs' `proof-bottom-icons.json`, `proof2-bottom-icons.json` and the first screenshots with it. The audit + proof3 were re-run into `proof/` (durable) and match the pre-restart numbers exactly; the proof1/proof2 numbers below are transcribed from those runs as printed and analyzed in-session before the wipe. The probe scripts that produced them (`probe-proof.py`, `probe-proof2.py`) remain in the work dir and are re-runnable.

**Activation reads (all before design work):** Orientation, Wake-Up Protocol, Bullseye, Naya Brand, Playbook, Design Intelligence Report, Anatomy, Heart of the Machine, Intelligent Block Rules (LAW, read in full through Part 5/conflicts/gaps as returned), Clarity Confirmation Act DRAFT (read §§1–2 in full — fingerprint, conduct, five gates, scorecard, operating rules — plus the section map §§3–6, gaps, conflicts; §§3–6 detail skimmed via headers only — noted honestly here), the trio law (`NOTIFICATION-SYSTEM-SPEC-20261112.md`), the gate object (`hub-bar-round-icons-fixed.html`), the gems (`smart-messenger.html` + `rb-gem-naming.md`), the v2 record (lessons carried: measure the PILL never the jewel · labels sized by the widest label · phone row scrolls).

## §1 — AUDIT (live baselines, first-hand)

| Page | Live size / sha | Bottom bar as found |
|---|---|---|
| Personal v9 (`nayanet.app/personal`) | 1,484,185 B, sha256 `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50` (re-verified against the live URL first; matched the brief's harvest exactly) | ONLY bar is `#naya-notif-bar` (NayaNotif trio), 78px. 3 tiles 54×54, **border-radius 16px (rounded squares)**, blue `#3fb8ff` MAIL / green `#2fe89e` ACTIVITY / gold `#ffbf3d` SPACES, no visible labels, counts all 0. `#nsbBottom` does NOT mount (Smart Bar bottom removed 2026-11-12). Body padding-bottom 78px = trio height. Zero overflow. |
| Hub live | 5,013,119 B | TWO stacked rows: `.eco-bottombar` (75px desktop, 121px phone — two rows) + `#naya-notif-bar` trio (101px, same 3 square 54px/16px tiles WITH labels MAIL/ACTIVITY/SPACES). **Eco row ALREADY compliant:** `.eco-bb-btn` 46px `border-radius:50%`, `.eco-dot` 38px `border-radius:50%`. Pre-existing 7px overlap eco/trio. Install overlay (`#naya-install-overlay`, z 3000) covers full screen — pre-existing, captain already flagged, out of scope. No `nsb-trio-faded` fade mechanism on Hub (Personal-only behavior). |
| Business live | 818,845 B | `#nsbBottom` mounts (142px desktop, 140px phone). 11 network pill tabs (Home, Dashboard, Personal, Business, Space, Intel Today, Smart Mail, Smart Lists, Library, Project Intel, Pricing + ＋ Add), 999px pills, each with a **29px `.nsb-jewel` chip, border-radius 9px (rounded square, colored)** — 11 unique + 11 duplicates = 22 chips. **NO trio at all.** Search FAB `#nsbSearchFab` 48px circle, `bottom:76px`. Body padding-bottom 142/140px = bar height. |
| Space live | 851,170 B | Same template as Business (same Smart Bar v1 system, same anchors, different line numbers). |

**Second-row question (brief Task 1):** on Personal there is no second row; the trio IS the bottom row. The fresh evidence's "second row of three large buttons (mail, activity, home)" was on the staged transparency page, where the trio sat BELOW a 7-tab nav — the trio IS that second row; it belongs (settled trio shape, spec 20:34Z) but re-keyed to worlds.

**v2 audit:** the staged round-icons v2 file was built on Hub v3 base (5,611,576 B); live Hub has moved past it (5,013,119 B, 0 `.obb-pill`). The v2 change was carried forward onto the fresh harvest, not the v2 file — per brief Task 4.

## §2 — WHAT WAS BUILT (bar only; pages stay the Personal page)

**Decisions (captain-decides, with rationale):**
1. **Trio re-key, not add:** the existing trio row is transformed in place into the worlds trio (same row, shape, fade, bubbles). Two trios would be the doubling-up defect. Mail/Activity channels lose their bottom-bar door; mail lives in the page's inbox view / Smart Mail — recorded as a consequence.
2. **Tile shape = `.obb-pill` object verbatim** (hub-bar-round-icons-fixed.html lines 9691–9705): 38px desktop / 27px phone, `border-radius:50%`, two-tone rim, twin radial gradients, 5-layer shadow, own-color rest glow (`--obb` → `--nc`). Three named adaptations: (1) no `margin-bottom:16px` (label rides in flow); (2) hover host is the segment button, effect lands on the tile; (3) tile color is the messenger's (`color-mix 72% --nc + white`), not the gate's `#fff`, so the gem keeps identity at rest. Old `::before` gloss deleted (twin gradients ARE the gloss). Phone label 10px (messenger label has no phone size; gate's 9px would pinch "Business"); count bubble slims to 20px on the 27px circle.
3. **Gems verbatim from messenger** (smart-messenger.html lines 408/411/414 + `rb-gem-naming.md`): amethyst round brilliant Personal `#a06bff`, emerald cut Business `#2fe89e`, diamond classic brilliant Thing `#e8eaf2`; 25px SVG desktop / 14px phone. Labels Personal/Business/Thing; third NEVER labelled "space" (label/aria only — the `localStorage` key `nayanet.notif.spaces` is a stored counter name, NOT renamed because the Hub writes it).
4. **Counts mapping (live, no stubs):** Personal = ActivityLog unread; Business = `nayanet.notif.mail`; Thing = `nayanet.notif.spaces`. Storage keys unchanged; only segments re-keyed. Per-world live delivery path still owed (per spec) — open item.
5. **Taps:** Personal page — Personal→`osShowView('myworld')` (in-page), Business→`https://nayanet.app/business`, Thing→`https://nayanet.app/space`; count clears on tap as before. Hub — all three by full-URL `location.href`. Business/Space — Personal→`/personal`, Business→same-path guard (scroll to top instead of reloading when already there), Thing→`/space` (same guard pattern).
6. **Hub leg:** live Hub moved past the v2 file — v2 change carried forward onto the fresh harvest. Live eco row already carries the gate circles, so NO eco-row change; only trio tiles + eco offset follows the new trio height (94px → 85px desktop, new ≤640px variant 71px). `.main` padding was NOT 186/250 as first read — see the clearance catch below.
7. **Business/Space leg:** (a) `.nsb-jewel` → round black circle, **scoped to `#nsbBottom` only** (top-bar chips stay square — named open follow-on); the 24px `.nsb-net-glyph` chip got the same treatment. (b) Transplanted the fixed trio (CSS + NayaNotif worlds + fold script) from Personal; `#nsbBottom` rides above it via `bottom: var(--notif-h, 0px)`; pad() edited in place to add trio height to body padding; search FAB lifted by trio height via `bottom: calc(76px + var(--notif-h, 0px))`. Total bottom chrome ~211–226px; content clears via padding, not height.

**Diff confinement (re-verified after every rebuild — bar only):**
- personal-fixed: hunks only at lines 12782–12848 (CSS trio) and 13534–13693 (JS trio).
- hub-fixed: hunks only at 360–435 (CSS trio + eco offset), 676 (content clearance), 6896–7000 (JS trio).
- business-fixed: 3 hunks only — CSS insert at 9399, pad() at 10336, JS insert at 10355.
- space-fixed: 3 hunks only — CSS insert at 10699, pad() at 11592, JS insert at 11611.

## §3 — MEASUREMENTS (Playwright Firefox, 1440/390/360)

**Icon radii (computed border-radius of the icon element itself — brief §5):**

| Page | Trio tiles 1440 | Trio tiles 390/360 | Bottom jewels | Top-bar jewels |
|---|---|---|---|---|
| Personal | 38×38, 50% (×3) | 27×27, 50% (×3) | — | — |
| Hub | 38×38, 50% (×3) | 27×27, 50% (×3) | eco dots 38px 50% (pre-existing, unchanged) | — |
| Business | 38×38, 50% (×3) | 27×27, 50% (×3) | 22/22 chips 29×29, 50% | 26 chips 29×29, 9px (scoped out — open item) |
| Space | 38×38, 50% (×3) | 27×27, 50% (×3) | 22/22 chips 29×29, 50% | 26 chips 29×29, 9px (scoped out — open item) |

Net glyph (`#nsbBottom .nsb-net-glyph`): 50% on Business/Space. Remaining `border-radius:16px` rules (31 Personal / 6 Hub / 25 Business / 23 Space) are all non-bar boards/images (`.sb-truth`, `.board-h .bh-icon`, `.product-img`, `.sa-cover`) — not bottom icons. (An earlier count of "3" was a miscount of one pattern; corrected here.)

**Bar geometry (all widths):** Personal bar 85px desktop / 71px phone; body padding-bottom matches exactly (85/71/71). Hub trio 86/72; eco bottom 815 vs trio top 814 = 1px overlap by design (offset 85 = trio 86 − 1). Business/Space seam 0px at every width (`#nsbBottom` bottom = trio top: 815/815, 773/773, 729/729); FAB clears the trio (bottom 739 vs trio top 815 at 1440; 697 vs 773 at 390). Body padding Business/Space 227/211/211 = bar + trio exactly. **Zero overflow** (`docScrollW` == viewport) on all four files at all widths. **Zero non-Supabase console errors** on all four files at all widths, local and staged.

**Supabase CORS errors — pre-existing, proven not ours:** staged Personal throws ~40 Supabase CORS blocks, Space 2, Business 0, Hub 0. Live check (Playwright, `nayanet.app`, 1440): Personal live 42, Space live 4, Business live 0 — same kind, same order. The proof host is not the cause; the pages' own data loads fail the same way on live. Not a defect of this round; not fixed here (bar scope).

**Trio state (preset `localStorage` mail=3, spaces=2 before load):** labels Personal/Business/Thing on all four files at all widths; gem SVG present on every segment (three distinct silhouettes); bubbles live — Business `3` shown, Thing `2` shown, Personal `0` hidden (ActivityLog empty on fresh load — the count is live, just zero). `--notif-h`: Personal `86px` (nothing consumes it there), Business/Space `85px`/`71px` exact.

**Fade:** Personal/Business/Space fade on scroll down and return after 1.5s at all widths. One anomaly, resolved honestly: the first probe read Personal/1440 `fadedAfterScroll=False`; an instrumented re-run (4 samples) showed `true` at 200/400/800ms and `false` at 1600ms — the first read was a timing artifact; the instrumented evidence stands. Hub: no fade — by design, it never had one; verified it stays visible.

**Cover (rect-by-rect at max scroll):**
- Personal: lowest flow content "No posts yet" ends 204px above the bar top (1440) — clear.
- Business: lowest flow content "No posts yet" ends 204px above the bar top (1440) — clear.
- Space: lowest flow content "Try again" button ends 190px above the bar top (1440) — clear.
- Hub: **the clearance catch (self-check, found in-round).** The audit first read `.main` padding as 186px desktop / 250px phone and declared the stack covered. The probe's COMPUTED style said 80px at all widths — the later rule `.main { min-width: 0; padding-bottom: 80px; }` (line 711) wins over the 186/250 rules (same specificity, later in the sheet). The stack is 161px desktop / 193px phone, so the last 81/113px of Hub content sat UNDER the bars at max scroll — measured: the last quote paragraph ended 96px under the bar top at 390. This was pre-existing on live (stack 176/222 vs 80px); the trio shrink alone did not cure it. **Fixed in-round:** a later `.main` rule sets the clearance to 161px desktop / 193px at ≤640px (diff hunk 676). After the fix, computed padding is 161/193 and the last text paragraph clears the bar top by 17px at 1440 and 17px at 390. One decorative SVG circle still extends past the Hub document end (no text, pre-existing page art, outside the flow) — named, not content.
- Method note: the first cover probe's `coveredLeaf` check was invalid (it only excluded elements whose OWN position is fixed, not descendants of fixed containers — the install overlay's and popovers' children polluted it). Cover v2 excludes any element with a fixed ancestor; the numbers above are from v2/v3.

**Clicks — trio (12, real Playwright clicks, one fresh load each):**

| File | Personal | Business | Thing |
|---|---|---|---|
| Personal | in-page: hash `#myworld`, view `myworld` on, no nav | → `https://nayanet.app/business` ("Acme Corp") | → `https://nayanet.app/space` ("Our Community") |
| Hub | → `https://nayanet.app/personal` ("Shawn Vibert") | → `https://nayanet.app/business` | → `https://nayanet.app/space` |
| Business | → `https://nayanet.app/personal` | SAME-PATH GUARD: no nav, scrolls to top (0 by 1.6s) | → `https://nayanet.app/space` |
| Space | → `https://nayanet.app/personal` | → `https://nayanet.app/business` | SAME-PATH GUARD: no nav, scrolls to top (0 by 1.6s) |

Hub trio clicks dismiss the Install overlay first with "Not now" — the real user flow; overlay presence recorded. Guard note: on `file://` the guard cannot match (pathname is the file path, not `/business`), so it was proven over a local HTTP server serving the fixed files at `/business` and `/space` — the exact live path shape. The guard's smooth scroll takes ~1.5s (an earlier 1500ms read caught it at 300; the instrumented run shows 0 at 1600ms) — standard smooth-scroll pacing, not a defect. (The first space guard attempt clicked `#segSpace` — a test bug: the segment is `#segThing`, not `#segSpace`. Corrected and re-proven.)

**Clicks — bottom pills (22, Business + Space, 11 unique each):** every pill opens its correct live destination in a NEW TAB (`window.open(dest,'_blank')` — the pill handler's design; the main page URL correctly does not change) with the clicked pill marked active. Destinations proven by popup URL + title: Home → `https://nayanet.app/` · Dashboard → `/dashboard` · Personal → `/personal` · Business → `/business` · Space → `/space` · Intel Today → `/rooms/today` · Smart Mail → `/rooms/mail` · Smart Lists → `/lists#/hub` · Library → `/rooms/library` · Project Intel → `/pi` · Pricing → `/pricing`. Identical on both pages. (The first pill probe read only the main-page URL and looked like "no navigation" — the handler navigates by new tab; the popup capture is the correct proof.)

**Staged proof (proof host, first curl + render):** all four staged URLs serve byte-identical content (curl bytes == local bytes; sha256 matches: Personal `5e5d29fc…`, Hub `499b6f40…`, Business `8142a734…`, Space `2aaf2a0a…`). Staged render at 1440 + 390: trio present, tiles 50%, labels, bubbles 3/2 live, zero overflow, zero non-Supabase console errors. Staged bar screenshots: `proof/staged-bar-*-1440.png`.

**Screenshots:** cropped bar shots at 1440 — `proof/bar-{personal,hub,business,space}-1440.png`; full-page audit shots at 1440/390/360 — `proof/audit-*-fixed-{1440,390,360}.png`; gate comparison — `proof/gate-strip-1440.png`. The gate preview file renders as a full page, not a strip; its bottom eco row (round black circles) is the reference shape — the fixed tiles match it: round, black, own-color glow, gem inset. Business bar crop confirms the pill jewels read round with distinct per-tab glow colors and the trio gems read as three distinct silhouettes (amethyst purple, emerald green, diamond white).

## §4 — SELF-CHECKS (three, each finding NEW things)

**Self-check 1 (static, after all four files built):** (a) script/style tag balance: the imbalance is PRE-EXISTING in the live files (Personal live 36/32, fixed 36/32 identical; Hub 28/28 identical; Business live 17/18 → fixed 19/20, +2/+2 = exactly my two transplant scripts, balanced; Space 23/24 → 25/26, same). No tag damage from my edits. (b) The 16px-radius count: an earlier "3 remaining" was a miscount of one pattern — the true counts are 31/6/25/23, all on non-bar boards/images (listed in §3). (c) SEGS arrays in all four files are the worlds (`personal/Business/Thing`), no `Space` label; the remaining `MAIL`/`ACTIVITY`/`SPACES` strings in hub-fixed are pre-existing page data (Smart Spaces/Mail kickers, feed-activity nav data, filter labels) — the old SEGS line (live line 6931) is gone.

**Self-check 2 (re-read of the built regions):** (a) Personal trio tile CSS is the gate object verbatim (38px, 50%, two-tone rim, twin gradients, 5-layer shadow, own-color glow). (b) Hub eco offsets are `calc(85px…)` / `calc(71px…)` as designed. (c) Business/Space pad() comments present. (d) Gate preview file exists. (e) NEW: Hub line 2768 carries a pre-existing ask-room override (`body:has(.naya-ask-room) .notif-bar{bottom:calc(71px…)}`) — untouched, untested in this round (open item). (f) NEW: the Hub clearance read (186/250) was stylesheet text, not computed style — this is what led to the clearance catch in §3 (the audit's one wrong call, found and fixed in-round by the probe).

**Self-check 3 (final pass, after all rebuilds):** (a) Diff confinement re-verified for all four files after the last rebuild (hunks listed in §2 — bar only, nothing else moved). (b) `--smartbar-h` consumers counted: Personal 4, Hub 0, Business/Space 5 each — the trio sits at bottom:0 on all four (measured), so no stray lift. (c) Gate-strip comparison done by eye: the gate preview is a full page, not a strip; its bottom eco row is the reference round-circle shape and the fixed tiles match it. (d) Business bar crop re-viewed: jewels round, trio gems distinct. (e) NEW: the pill-click proof method itself was wrong the first time (main-page URL read vs new-tab navigation) — corrected with popup capture; the guard proof method was wrong the first time too (`file://` pathname can never match) — corrected with the local HTTP server at live path shapes.

## §5 — GATES

**Design-contract gate (a)–(i) (measured by hand — `check-gate.py` has not landed yet):**
- (a) Zero white/light backgrounds — PASS for this round's diff: the bar change adds only obsidian gradients; no light background introduced. Whole-page scan not re-run (page unchanged outside the bar).
- (b) Every element raised/elevated — PASS for the bar: tiles/jewels carry the 5-layer shadow + rim; the trio bar carries its shadow; pills already elevated.
- (c) Gauges/numbers alive — PASS (scoped): the bar's numbers are the count bubbles, and they are live (3/2 proven from the shared stores).
- (d) No text-in-image, no pasted document — PASS: no new images; gems are inline SVG.
- (e) No bare text blocks — PASS (bar): labels live in segments/pills.
- (f) No look-alike — PASS: tiles ARE the harvested gate object verbatim; gems verbatim from the messenger.
- (g) `##` sections on notes — N-A (no notes in this round).
- (h) Banned blunt phrases — N-A (no new public copy; labels are single words).
- (i) Title+subtitle+nutshell + face alternation — N-A (no boards/faces in this round).

**L1–L7:**
- L1 Stranger test — PASS (scoped): a stranger sees three labelled doors (Personal/Business/Thing) with distinct gems; the bar answers "where do I go" with the doors themselves. Evidence: the labelled-trio screenshots.
- L2 His words are INPUT (perfect-words law) — PASS: the labels are his words (Personal, Business, Thing), crafted, no dictation or process talk on the page.
- L3 Title + subtitle + nutshell — N-A: the trio is a nav element, not a content board; its single-word label is its title by design.
- L4 Naya speaks, faces alternate — N-A: no faces in this round.
- L5 The test in his head — PASS: 10-star? The bar is round black circles + gems as ordered. Obvious? Labels + gems. Useful? Doors to their worlds. Done clearly? Measured throughout §3. (The named opens in NOT-DONE are the "not yet" part.)
- L6 Smart-note `##` format — N-A (no notes).
- L7 One ultimate ten — N-A (not a ten-list round).

**Human checks H1–H5:** H1 stranger test — PASS (as L1). H2 perfect-words law — PASS (as L2). H3 face quality — N-A (no faces). H4 test in his head — PASS (as L5). H5 one ultimate ten — N-A. Verdict: PASS — MACHINE + HUMAN (scoped to the bar; H3/H5 N-A, not pending).

## §6 — APPLIED-LAWS TABLE (law read → quoted verbatim → part it produced)

| Law read | Quoted verbatim | Part it produced |
|---|---|---|
| THE-ULTIMATE-ORIENTATION.md | (Orientation: who we are, how it works, the laws we live by — read on wake, before any work.) | The round's posture: bar only, harvest, verify before reporting. |
| THE-BULLSEYE.md | (The bullseye is defined BEFORE the action: what the page must be, exactly, and what must NOT be there.) | Bullseye line at the top of this record; the 50% / zero-overflow / zero-cover measurements are the bullseye made checkable. |
| THE-NAYA-BRAND.md | (Real objects, obsidian gloss black, ALL buttons elite and lit the same, every number alive.) | Tiles as real objects (rim, gradients, shadow, own-color glow); count bubbles live. |
| THE-PLAYBOOK.md | (The HOW: the formula, the steps, the laws.) | Edit-in-place flow, anchored replacements, probe-then-record order. |
| DESIGN-INTELLIGENCE-REPORT.md | (The WHY: what was got wrong, what was learned.) | Measure the PILL never the jewel (v2 lesson applied — computed radius of the tile itself, §3). |
| THE-ANATOMY-OF-A-SMART-APP-PAGE.md | (The MAP — what a smart app page is, the core apps and their functions, how they connect.) | The four pages treated as one family: the same trio rides all four, not four different bars. |
| THE-HEART-OF-THE-MACHINE.md | (The psychology, the mission, the heart.) | The trio as the worlds' doors — Personal, work, thing — so people find themselves and others like them. |
| Intelligent Block Rules (LAW, ratified 2026-11-06) | (The fingerprint, the conduct before acting, the design, all 22 elements — read in full through Part 5/conflicts/gaps.) | Tile construction (elevated, lit, real objects); the bar's lane discipline. |
| Clarity Confirmation Act DRAFT (§§1–2 read in full) | (Five gates before every action: Is it right? Is it what they truly need? Is it mine to do? Is now the time? Can I prove it?) | The five gates run before the Hub clearance fix and before every filing (see pre-merge Q5). §§3–6 detail skimmed via headers only — noted honestly in the header. |
| NOTIFICATION-SYSTEM-SPEC-20261112.md (settled 20:34Z) | "Personal activity · Business activity · Thing activity. Three buttons, right at the bottom." / "The three buttons are their worlds, not the channels." / "Not a new bar, and not a fourth button. Three buttons, the same trio shape every page already carries." | The trio re-key (not add) on all four pages; third button labelled Thing, never space. |
| THE REAL OBJECT LAW | "Every element is a real physical object. Not a flat shape with effects. Not a diagram." / "If it doesn't look touchable, it doesn't ship." | `.obb-pill` harvested verbatim (rim, twin gradients, 5-layer shadow, glow) instead of a flat recolor. |
| Personal Pages Law (Shawn 04:01Z) | "A sister's Personal page looks EXACTLY like the normal Personal page, and she puts one of the beautiful smart covers on it. Same as ours. No different page." | Bar-only scope: no custom pages, no new page, the Personal page stays the Personal page. |
| Everybody Gets the Same World (Shawn 04:16Z) | "everybody gets the SAME world — just different labels." | One trio, one tile object, on all four pages — not a sisters-only variant. |
| THE BILLION-DOLLAR HOME LAW (Shawn 04:21Z) | "work ON the product we have, never create a new one; harvest, never invent; learn the system first, then do the work." | All four fixes are edits in place on harvested objects; the Business/Space trio is a transplant of the Personal trio, not a new build. |
| The Five Gates + Sense Check | "The user sees the PAGE, not the diff." / "is it logical? Is it sensible? Is it intelligent? Should this be here? Does it make sense? Am I doubling up?" | The Hub clearance catch (the page, not the diff, showed content under the bar) and the trio re-key (no doubling up). |
| The Self-Check Law (Shawn 2026-11-11) | "The maker checks their own work THREE TIMES (each round finding NEW things; below honest 9+ → fix it yourself), answers the seven pre-merge questions IN WRITING, then the CAPTAIN double-checks before it reaches Shawn and before the maker merges." | §4 self-checks ×3 + §7 seven answers; score 8 (below 9) → merge withheld per the law and the brief. |
| Harvest law (Shawn 04:34Z, via the feed round) | "take that EXACT system — not one like it — just take it and put it into the Personal page, and just change some of the labels." | Gems and tile taken verbatim; only labels/keys re-keyed. (Context: the 04:34Z public-feed ruling itself belongs to the sisters' Personal-pages round, not this one — noted, not acted on here.) |

## §7 — SEVEN PRE-MERGE ANSWERS (in writing, per `PRE-MERGE-QUESTIONS.md`)

1. **Did I check my own work three times?** YES — §4, three rounds, each finding NEW things (tag-balance/16px correction; ask-room override + clearance-read error; diff confinement + two proof-method corrections).
2. **Is it 9 or better by my own honest score?** NO — 8/10 (see scorecard). Below 9, so per the law I do not merge. The merge is withheld in any case: the brief orders merge + live deploy to wait for Shawn's eye and his tap, after the captain's double-check.
3. **What could this break?** Named: (a) trio tap destinations on all four pages — worlds navigation (proven by the 12 clicks); (b) the Mail/Activity channel doors removed from the bar (mail now only via inbox/Smart Mail — a consequence, not a break); (c) Business/Space body padding (227px chrome — proven to clear content); (d) Hub `.main` padding (161/193 — proven to clear content after the fix); (e) search FAB position (lifted by trio height — proven clear); (f) Smart Bar fold behavior (trio fade added where none existed — proven at all widths); (g) `localStorage` count keys — UNCHANGED, only segments re-keyed. If any of these regressed, the §3 measurements would have caught it; they did not.
4. **Are the automatic checks green?** No automatic check suite exists for this round (`check-gate.py` has not landed — the gate was measured by hand per the brief). The Playwright probes are the automated evidence and are green except the pre-existing Supabase CORS blocks, which match live exactly (proven not ours). No check was overridden.
5. **Does it follow the ultimate objectives?** The five gates, honestly: RIGHT — it serves the worlds navigation Shawn ordered. WHAT THEY TRULY NEED — the doors to Personal, work, and thing, so people find themselves and others like them. MINE TO DO — briefed maker seat, bar only, no protected gate touched. NOW THE TIME — the round was dispatched and the files are filed. CAN I PROVE IT — §3 throughout (bytes, radii, clicks, popups, cover rects, staged sha).
6. **Did I prove it with real measurements?** YES — live bytes, rendered pages at 1440/390/360, real clicks (12 trio + 22 pills with popup URLs), rect-by-rect cover, staged byte/sha verification. No claim without its measurement.
7. **Is there anything in here not ten out of ten that I'm knowingly leaving?** YES — named in NOT-DONE below. Nothing left silently.

## §8 — DONE and NOT-DONE

**DONE:** the bottom bar on Personal, Hub, Business, and Space reads as nice round black circles (measured 50% on the icon element itself at all widths); the very bottom carries the three ultimate gems (amethyst Personal, emerald Business, diamond Thing — verbatim messenger gems, three distinct silhouettes, labelled Personal/Business/Thing, third never "space"); every bottom icon + the trio click-proven to its real destination (12 trio clicks, 22 pill popups); the bar never covers content at any width (rect-by-rect, including the Hub clearance fix found and fixed in-round); zero overflow; zero non-Supabase console errors; staged links byte-identical and re-proven on the staged host; all four files on the branch with read-back-verified blob SHAs.

**NOT-DONE (named, not silent):**
- Top-bar `.nsb-jewel` chips on Business/Space still square (9px) — the fix was scoped to `#nsbBottom` only. Follow-on: same round treatment for the top bar.
- Per-world live delivery path (real-time socket/push) still owed — per the trio spec; counts use the existing shared stores.
- Hub trio has no scroll-fade (Personal-only behavior, by design — never had one).
- Hub install overlay covers the full screen until dismissed (pre-existing, captain already flagged); a first-visit user must tap "Not now" before tapping the trio.
- Hub ask-room bottom override (`body:has(.naya-ask-room) .notif-bar{bottom:calc(71px…)}`) untouched and untested in this round.
- One decorative SVG circle bleeds past the Hub document end (pre-existing page art, no text) — cosmetic.
- Supabase CORS blocks on Personal (~40) and Space (2–4) — pre-existing on live, identical counts; outside bar scope.
- The `nayanet.notif.spaces` storage key keeps its name (the Hub writes it) while the segment is labelled Thing — documented, not renamed.
- Checker + captain double-check still owed; merge + live deploy wait for Shawn's eye and his tap.

**Honest score: 8/10** — see `SCORECARD-BOTTOM-ICONS-ULTIMATE-TRIO-20261113.md`. Below 9, so no merge (per the Self-Check Law) — and the brief withholds the merge in any case.
