# HUB 9-CIRCLE BAR OVERFLOW FIX — RECORD (Maker seat, Area #8) — 2026-11-14

## The verdict, in one line

The bar now says there is more and lets you reach it: at 390/360 a lit
right-edge fade + a "›" chevron show at rest, one tap scrolls the hidden
pills into full view (SNAP lands them whole), "‹" brings you back, and a
real touch swipe does the same; at 1440 nothing shows and nothing changes.
Staged only — nothing live, no merge.

## Staged links (the deliverables)

- **Proof-host (stable, branch bytes, immutable):**
  https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref=hub/bar-overflow-fix-20261114&cb=73c9f0be287ddde5200be664ca260639b4c9510b
- **Staging worker (was live with the fix 01:50–~02:00Z, then overwritten by
  another round — see §Staging worker churn):**
  https://naya-public-blog-staging.nayapower.workers.dev/hub
- **Branch:** `hub/bar-overflow-fix-20261114`, commit
  `0fb8fede0b472994034a82f163ffbc33fb934fad` (from main
  `3d3ef4e668804a5d9b775b65994a62f9f4eac938`, re-read first-hand twice).
  One file: `HUB/app/index.html`, blob
  `73c9f0be287ddde5200be664ca260639b4c9510b`, read back via raw byte-identical.
- **Page SHA:** `7d25f59105996fa0c40bde4d3b17a8c5e727e95861fc442b344c9f5ed840797d`
  — template, repo file, proof-host bytes, staging-worker bytes (while it
  served them) all identical. **5,003,256 B** (+3,029 B over the pre-fix
  template).
- **Work dir:** `~/workspace/team-nitro/hub-bar-overflow-fix-20261114/work/`

## 1. Reproduction first (live /hub, read-only, 01:24–01:26Z)

Reproduced the checker's numbers EXACTLY at 390 (settled state, +4 s):

| Pill | Left | Right | Visible |
|---|---|---|---|
| MAIL | 10 | 60 | yes |
| DASHBOARD | 66 | 135 | yes |
| BUSINESS | 141 | 197 | yes |
| SPACE | 203 | 253 | yes |
| GROWTH | 259 | 310 | yes |
| CONNECTIONS | 316 | **397** | **cut at the 390 edge** |
| SMART LISTS | 403 | 475 | no |
| REPORTS | 481 | 532 | no |
| 10 APPS | 538 | 588 | no |

Same at 360 (row 578 wide in a 340 client). At 1440 all 9 fit
(MAIL 382 … 10 APPS 1003–1058). 0 console/page errors at all widths.
Evidence: `repro-live.py`, `repro-live.json`, `repro-live-{390,360,1440}.png`
(screenshot read by eye: "CONNECTIO" cut at the edge, as the checker saw).

**Refinement of the checker's finding (measured, not assumed):** the row
(`.obb-row`) IS already a scroll container — `overflow-x:auto`,
scrollWidth 578, clientWidth 370 — and programmatic
`row.scrollLeft = 200` WORKS (→ 208 after snap, pills move). The defect
is not "no scroll path" mechanically; it is **no VISIBLE affordance**:
the scrollbar is hidden (`scrollbar-width:none`,
`::-webkit-scrollbar{display:none}`), there is no fade, no control, and
nothing that says more exists. A mouse drag does not scroll it (desktop
browsers don't drag-scroll); a touch swipe does, but nothing invites one.
The checker's "unreachable" stands as a user-facing fact; the mechanism
behind it is narrower than stated, and the fix follows from that.

**Modal (measured only, direct /hub load):** the Install overlay
(`.naya-install-overlay.show`) is UP at +4 s settled AND +6 s at 390,
360, AND 1440. (The checker saw none on the note walk — different flow;
on direct Hub load it is up. It intercepts all pointer events until the
visitor taps its own "Not now" button. Not fixed here — out of scope.)

## 2. The fix choice — scorecard

| | (a) Fit all 9 at 390/360 | (b) Scroll + visible affordance |
|---|---|---|
| Needs | 578 px of row in 370 (390) / 340 (360) | row already scrolls; add the cue |
| Cost | jewels 44→~28 px, labels 9→~6 px — unreadable, a redesign, changes the bar's look | +3,029 B, bar-only, no look change |
| 1440 | unchanged only if scoped; still a phone redesign | nothing shows, nothing changes (proven) |
| Bullseye | fits, but breaks "readable labels" | every pill reachable + fully visible when scrolled to, with a visible cue |

**Picked (b).** Fit is not achievable without redesigning the bar; the
scroll mechanics already exist and work, so the fix is the missing
affordance only. One option, not both.

**What the fix is (bar-only, all inside the one-bottom-bar block,
lines 9721–9830 of the shell):**
1. **HTML:** two chevron buttons inside `nav.obb-bar`, after the row:
   `.obb-nav-l` "‹" (Show earlier apps) / `.obb-nav-r` "›" (Show more apps).
   Absolutely positioned at the bar edges; they do not affect layout.
2. **CSS:** edge fades (`.obb-bar::before` left, `::after` right — 34 px
   gradients in the bar's own obsidian, `pointer-events:none`) + chevron
   styling (30 px obsidian circle, white chevron, jewel-style glow).
   All four are shown ONLY by `data-obb-more` on the bar:
   `[data-obb-more~="left"]` → left fade + left chevron, same for right.
3. **JS:** a small IIFE after the lane script reads the row's own scroll
   state (`scrollWidth - clientWidth`, `scrollLeft`) and writes
   `data-obb-more` = `"left"` / `"right"` / `"left right"` / `""` — on
   scroll (passive), resize, load, and +500/+1500 ms settle. A chevron
   tap scrolls the first not-fully-visible pill into view with
   `scrollIntoView({inline:'start', behavior:'smooth'})`.

**The snap lesson (found by measurement, filed so the next seat doesn't
re-learn it):** plain `scrollBy` does NOT travel in this row.
`scroll-snap-stop:always` stops it at the very FIRST snap point
(46 px) no matter the distance — my first chevron handler did exactly
that and the tap went nowhere. `scrollIntoView` on the target pill is
snap-aware and lands cleanly (verified: 0 → 208 smooth, 208 → 183 back).
Snap points at 390: 0, 46, 121, 183, 208 (max).

**Known 5 px edge nick (named, not hidden):** at max scroll (208) the
SPACE pill sits at −5…45 — its first 5 px are off the left edge. Pure
geometry (row 578 wide, window 370, max scroll 208). SPACE is fully
visible one step back (183). The bullseye is met: every pill is fully
visible at some scroll position and reachable by chevron or swipe.

**Build:** `apply-fix.py` — three anchored replacements on the CURRENT
template as read first-hand (sha `4a89ed86…`, 4,999,666 B, first note
SN-2782), each anchor asserted count==1 before replacing. Verified:
markers 4/2/7, `src="/js/naya-search.js"` 1x, SN-2782 + SN-2696 present,
200 notes parsed back **list-identical** to the extract,
node `--check` on ALL 32 inline script blocks: PASS, deploy.py CSS
brace gate: PASS, diff scope: every changed line inside the
one-bottom-bar block. Pre-fix template bytes preserved as
`work/index-2-BEFORE-20261114.html` (sha `4a89ed86…`, verified identical).

## 3. Both files, same bytes

- Bake template `~/workspace/user/files/index-2.html`: written atomically
  (temp + rename in the same directory, size-checked), re-read identical:
  **5,003,256 B, sha `7d25f591…`**.
- Repo `HUB/app/index.html` on branch `hub/bar-overflow-fix-20261114`
  (commit `0fb8fede`, from main `3d3ef4e66`): same bytes, read back via
  raw byte-identical. **Template == repo file, sha `7d25f591…`.**
- NOT touched: `HUB/hub-worker.js`, `HUB/wrangler.toml`,
  `HUB/app/feed-live.json` (stale-877 trap stays a captain's call),
  worker, feed, entrance, modal. No merge. Nothing live.

**Local-checkout trap, found in-round:** the local `nayapower-repo`
checkout sits on branch `nitro/p4-dashboard-strip` (HEAD `1e270485`),
whose `HUB/app/index.html` is an OLD shell (5,467,298 B, 0 route
markers) — NOT main. The branch was filed from remote main
(`3d3ef4e66`, re-read via `git ls-remote` + fetch immediately before
filing), never from the local checkout. The local pre-existing dirty
files (`HUB/walk/worker.js`, welcome-engine) were not touched.

## 4. Next-sync proof (the sync's OWN function)

`sync-smart-notes.py::inject_live_notes` run on a COPY of the new
template (never the live template) with the same 200 notes — `sync-proof.py`:
- Output **5,003,258 B, delta +2 B** — the exact same 1-line
  script-indentation artifact as the live leg (line 3831, +2 B whitespace).
- Markers survive: 4/2/7, absolute search src 1x, `data-obb-more` 7x,
  `obb-nav` 12x; notes parsed back 200, list-identical; node `--check`
  on the obb script block: PASS.
- **The fix survives the re-bake.** The next sync rebakes the FIXED shell.

## 5. Staged proof by eye (390/360/1440, cold link + Hub-direct)

Two staged surfaces were used; the worker one is the complete proof.

### (a) Staging worker (complete — note renders, feed live)

Deployed with `deploy-staging.py` (the bars round's proven flow):
`stage_hub_assets` from main `3d3ef4e66` + fixed shell + the FRESH live
feed (8,489,662 B, count **1085**, first SN-2782) + main's phase-1 worker
(asserted 49,174 B, sha `8ee4f859…`), phase-1-only `run_worker_first`.
PUT success, etag `81fbb511c95657ca`. Curl battery, first-hand:
`/hub` 200, 5,003,256 B, sha `7d25f591…` exact · bot `/s/sn2696` 200,
14,635 B, title "The Infinite Smart Feeds — one feed per topic · NayaNET" ·
`/feed-live.json` 200, count 1085.

Browser walk (`probe-staged-worker.py`, Firefox, fresh context each):

| Width | Flow | Note | Bar at rest | After › tap | After ‹ tap | Errors |
|---|---|---|---|---|---|---|
| 390 | cold `#/smart-notes/sn2696` | title "SN-2696 · SYSTEM / INTELLIGENCE / FEEDS", SN-2696 ✓, IN A NUTSHELL ✓ | `more='right'`, › grid, right fade 1, SL 0 | SL 208, Growth/Connections/Smart Lists/Reports/10 apps ALL fully visible | SL 183 | 0 |
| 390 | direct `/hub` | "Good morning.", SN-2696 ✓ (feed), nutshell ✓ | same | same | same | 0 |
| 360 | cold | same as 390 cold | `more='right'`, › grid, fade 1 | SL 238 (max), last 5 fully visible | SL 183 | 0 |
| 360 | direct | same as 390 direct | same | same | same | 0 |
| 1440 | cold | note renders, SN-2696 ✓ | `more=''`, no chevrons, no fades | n/a (no overflow) | n/a | 0 |
| 1440 | direct | Hub top, feed "1085 Smart Notes" | same, pills MAIL 382 … 10 APPS 1003–1058 — **identical positions to live** | n/a | n/a | 0 |

- **Gems (unregressed):** 3, circles **27×27 at 390/360** (measured on the
  staged bytes), distinct SVGs with lengths **564 / 540 / 676** — the
  checker's numbers exactly. Labels Personal / Business / Thing.
- **Hook (detector note):** my probe's hook check searched for the string
  "The Infinite Smart Feeds" (the bot-page title) and reported False on
  the cold flow — wrong string. The note's hook DOES render, read by eye
  in `staged-w-390-cold-w-rest.png`: "Hook: Not one feed like Facebook —
  infinite feeds, one for…" + CREATE SPACE / FAVORITE / SAVE.
- **Feed (unregressed):** Hub top shows "Intelligence as of Nov 13, 2026 ·
  1085 Smart Notes · 0 days old" with feed cards (The Intelligent
  Internet, AI Is Hiring, NayaNET / Naya, Smart Notes / Learn In a
  Minute…). My probe's `feedCards` selector returned 0 — a selector miss,
  not a feed failure; the feed is visible in the screenshots.
- Screenshots read by my own eye: `staged-w-390-cold-w-rest.png` (note
  renders, › chevron over the cut CONNECTIONS),
  `staged-w-390-cold-w-scrolled.png` (‹ chevron, all five last pills
  whole), `staged-w-1440-direct-w-rest.png` (all 9 centered, no
  affordance, feed live). Plus `staged-w-360-*` and `staged-w-1440-cold-*`.

### (b) Proof-host (stable — bar + shell bytes)

https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref=hub/bar-overflow-fix-20261114&cb=73c9f0be287ddde5200be664ca260639b4c9510b
— 200, 5,003,256 B, sha `7d25f591…` exact (curl, first-hand). Same bar
numbers as the worker probe. **Limit, stated plainly:** the proof-host
serves the bare shell with no worker/feed backend, so `/feed-live.json`
400s there and the cold-link note view stays on "Opening your note…"
(verified at +20 s). That is a proof-host environment limit, not a
regression — the note-loading code is untouched (diff is the obb block
only) and the note renders on the staging worker above. The bar proof on
the proof-host is complete; the note-body proof rests on the worker probe.

### (c) Real touch swipe (Chromium CDP, proof-host bytes)

`Input.dispatchTouchEvent` swipe left across the bar at 390: SL 0 → 183,
visible Space/Growth/Connections/Smart Lists/Reports, `data-obb-more`
flips to `"left right"`; swipe right: SL → 0. (A swipe stops at the
first snap point — 183, not the 208 max — so one swipe reveals five
pills and a second reaches the end. Same snap-stop law as the chevron.)
Gem circles re-measured here on the fixed bytes: 27×27.

### Modal log (staged, measured only)

| Flow | 390 | 360 | 1440 |
|---|---|---|---|
| Cold link (note) | none at +4 s, none at +6 s | none / none | none / none |
| Hub-direct | `show` at +4 s, `show` at +6 s | show / show | show / show |

Note landings suppress the modal (the live leg's slug fix, working);
Hub-direct shows it. Unchanged from live. Not fixed here.

## 6. Staging worker churn (named, not hidden)

The staging worker is shared. My deploy landed 01:50Z and the full
worker probe ran against the fixed bytes (curl-verified sha `7d25f591…`
immediately before the probe). By ~02:05Z, when I re-checked for the
swipe test, the worker was serving a DIFFERENT shell (5,570,515 B, sha
`2c62d243…`, 0 fix markers) — another round redeployed it in between.
I did NOT redeploy over them. Consequence: the checker cannot re-run
the full note walk on the staging worker right now; the stable staged
proof is the proof-host link (immutable branch bytes) plus the completed
worker probe in this record. If the captain wants the worker re-proven,
it needs a re-deploy after the other round's staging is done — a
coordinator call, not a maker one.

## 7. Self-checks (three rounds)

**Round 1 (the build):** reproduction first, exact checker numbers;
scorecard picked scroll+affordance with the reason written down; the
first chevron handler (scrollBy) FAILED in the local probe (tap went
nowhere) and the snap-stop cause was found by measurement, not guessed —
handler rewritten to scrollIntoView and re-proven at all widths before
anything was written to the template.
**Round 2 (the write + the trap):** template written atomically and
re-read identical; repo file filed from re-read main head (not the stale
local checkout — caught in-round); sync proof with the sync's own
function (+2 B, same artifact as the leg); branch read back byte-exact.
**Round 3 (the staged proof):** walked cold + direct at 390/360/1440
with the chevrons actually clicked and a real touch swipe; the note
view, gems, feed, modal timing, and 0 errors all recorded; the
proof-host note-loading limit and the worker overwrite both named
instead of smoothed over; screenshots read by my own eye.

**Seven pre-merge answers (no merge in this round — for the captain):**
1. Three self-checks done? Yes — rounds 1–3 above, each finding new
   things (scrollBy/snap-stop; stale local checkout; worker overwrite).
2. Honest 9+? Yes — 9/10, deduction named below.
3. Blast radius named? Staging only: one branch file (`HUB/app/index.html`),
   the bake template, the staging worker (since overwritten by another
   round — nothing of mine remains live there). No live touch, no main
   change, no worker/feed/entrance/modal change. Rollback = re-deploy the
   previous shell; nothing else to roll back.
4. Checks green? Yes — every number in §5 is first-hand; two known
   limits named: proof-host note view can't load (no feed backend);
   staging worker overwritten after my probe.
5. Five gates? Yes: right (three nav destinations were invisible on the
   phone-first viewport); truly needed (the checker's 8/10 defect, the one
   thing between the Hub leg and done); mine to do (this brief, bar only);
   now (reproduced, fixed, staged, proven in one pass); provable (every
   sha, count, and screenshot in this record).
6. Real proof? Yes — live repro bytes, staged bytes, browser measurements
   and screenshots, all first-hand in this round.
7. No silent known defects? None silent — the 5 px max-scroll nick, the
   one-swipe-per-snap-point behaviour, the proof-host note limit, and the
   worker overwrite are all named here.

## Score: 9/10

What earns the 9: defect reproduced exactly (checker numbers to the
pixel); the right fix chosen by scorecard and the wrong first handler
caught by my own probe and corrected; template + repo byte-identical so
the next sync cannot revert it (proven with the sync's own function,
+2 B); staged proof walked cold + direct at all three widths with
chevrons clicked, a real touch swipe, the note rendering, gems exact,
1440 identical to live, 0 errors; screenshots read by eye.
What costs the point: **the staged proof's fullest surface — the staging
worker — was overwritten by another round before the checker can use it**,
so the checker's re-verification of the note walk must either re-deploy
the worker or rest on my completed probe + the immutable proof-host link.
That is a process gap (shared staging with no lock), not a defect in the
fix — but the proof is weaker for it, and the score says so.

## DONE / NOT-DONE

**DONE:** live defect reproduced first-hand with exact measurements ·
fix chosen by scorecard (scroll + visible affordance) · fixed shell built
from the current template with all gates (markers, 200 list-identical
notes, node --check ×32 blocks, CSS brace gate, diff scoped to the obb
block) · template written atomically + preserved BEFORE copy · repo file
filed on branch `hub/bar-overflow-fix-20261114` from re-read main head,
read back byte-identical · next-sync proof with the sync's own function
(+2 B) · staged to proof-host (stable) + staging worker (verified, then
overwritten by another round — named) · walked cold + direct at
390/360/1440 with chevron clicks + real touch swipe · gems, note route,
SN-2696, feed unregressed · modal presence/absence timed at each width ·
record + scorecard + receipt.
**NOT-DONE (not mine, or owed elsewhere):** merge to main + live deploy
(Shawn's tap, via the captain after the checker) · re-deploy of the
staging worker for the checker's re-run (coordinator call — another
round owns it now) · the stale `HUB/app/feed-live.json` on main (877
notes — captain's call, unchanged) · the Install modal on Hub-direct
(measured only) · the re-entry name-again friction (entrance area).

## Open items for the captain / checker

1. **Checker re-run:** proof-host link is the stable surface (bar +
   shell bytes). The staging worker currently serves another round's
   shell — do not trust it until re-deployed. The note-body render on
   staging rests on my completed worker probe (§5a) — re-deploy to
   re-prove, or accept the probe + live-path note code (untouched).
2. **The 5 px nick** at max scroll (SPACE −5…45) and **one swipe per
   snap point** (swipe stops at 183, second swipe reaches 208) — both
   inherent to the row's geometry + `scroll-snap-stop:always`. Named
   for the checker's judgment; I did not chase them into a redesign.
3. **Chevron overlap:** at rest the › chevron sits over the cut
   CONNECTIONS pill's right half — that IS the affordance, by design.
   If Shawn wants it subtler, that's a design call, not a bug.
