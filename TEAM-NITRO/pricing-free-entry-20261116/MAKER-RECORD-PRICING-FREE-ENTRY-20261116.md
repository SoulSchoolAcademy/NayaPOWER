# MAKER RECORD — PRICING: FREE-ENTRY ROUTE + FREE BUTTON ON TOP (F4, v78, 2026-11-17)

Maker: pricing free-entry round (F4). Brief: `~/workspace/team-nitro/BRIEF-PRICING-FREE-ENTRY-20261116.md`
(Shawn's order 2026-11-17 00:03Z: pricing v77 is live but has NO free-entry route — build the real
route, then the free button goes on top. No dead buttons.) Built 2026-11-17 ~00:06–00:33Z.

## DELIVERABLES

- **1. The free-entry route, real** — staged worker `naya-pricing-free-staging`:
  `https://naya-pricing-free-staging.nayapower.workers.dev/free`
  - Worker script 3,615,644 B, sha256 `7a6a90959ced7d104b7e0781de023396412cea2eadfc504db309e964fc66a41c`
    (gzip ~2.54 MB — measured on the pre-fix build, fix adds 6 bytes; PUT accepted).
  - Entry (free identity page): 307,918 B, sha256 `e0534a61441dd6f4f643b79a74a9d1a8479c8c41cb2d6abf126d3b7fd87eb1ab`
  - Walk (free mode): 3,288,471 B, sha256 `ea1e77a67cbdc34d5829d8a4f09bceba0338ca3efac8483d84703d69521191cc`
  - Index: 1,966 B, sha256 `085939f6f1a8bc0106f54434f5dc27ef12e7a17c8733ca792d8ad61e8521c47e`
  - KV binding `WELCOME_ASSETS` (namespace `1cf80db6183245d19dd5296645a12bd0`, shared with the
    walk staging worker).
- **2. The free button, on top** — pricing v78:
  `~/workspace/team-nitro/pricing/v78/pricing-v78.html`
  - **11,360,503 bytes, sha256 `ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2`**
  - Built from the live v77 source (`~/workspace/team-nitro/pricing/v77/pricing-v77.html`,
    11,355,594 B, sha `b043167b…`). Delta: **+4,909 bytes**. Diff v77→v78: 51 lines, 8,941 B
    (`v78/diff-v78.txt` — pending disk write, see "Honestly not done").
  - Staged at `https://naya-pricing-f4-staging.nayapower.workers.dev/`
    (worker `naya-pricing-f4-staging`, spliced script 11,374,930 B,
    sha `9aeacc886b3bded323ceb528fada066dd7327bcaed7c55e23ef56910516f62f0`, bindings `[]`).
- Build/stage scripts (this round's dir `~/workspace/team-nitro/pricing-free-entry-20261116/`):
  `build-v78.py`, `build-free-staging-worker.py`, `stage-in-memory.py` (the staging run),
  `stage-free-route.py`, `stage-pricing-v78.py`, `check-free-route.mjs`,
  `pricing/v78/check-worker.mjs`, `pricing/v78/check-worker-markers.mjs`.
- This record: `~/workspace/team-nitro/pricing-free-entry-20261116/MAKER-RECORD-PRICING-FREE-ENTRY-20261116.md`

## WHAT WAS BUILT

### The route (free worker) — entry → walk → Hub, Hub first

- **`/free`** — the entry page, harvested verbatim from the walk round's
  `identity-fixed.html` (305,681 B), with 3 free-mode patches: `WALKTHROUGH_URL`
  `/welcome` → `/free/walk`; a free line under ENTER ("Enter free — no payment, no card.")
  with the canonical info-eye (SVG harvested verbatim from the pricing page's `.plan-eye`)
  toggling the explainer ("Naya Free is the free way in: your Smart Name, your pages, your
  Hub — zero cost, zero risk. Step up any time in Settings."); CSS for the line/eye appended
  before `</style>`. Name + alias claimed via same-origin `/api/claim`, same as the walk.
- **`/free/walk`** — the walk, harvested verbatim from `walk-beginning-fixed.html`
  (3,288,041 B), with 4 free-mode patches: (P1) the recommendation paragraph now recommends
  the Hub first ("Recommended first — start in your Hub. Everything, in one place — then get
  your Smart Link on your Dashboard."); (P2) end doors reordered **Hub, Dashboard, Personal,
  Business, Space** — Hub takes `.p3-door-rec` with sub "Everything, in one place — start
  here", Dashboard loses the rec and "recommended first"; (P3) end-slide free line after the
  welcome paragraph ("You're in on Naya Free — zero cost, zero risk. Step up any time in
  Settings."); (P4) boot flag `localStorage.setItem('nayanet_free_entry','1')`.
- **`/free/hub`** — 302 to `https://nayanet.app/` (the Hub). The walk's own Hub door also
  points there (`Hub: 'https://nayanet.app/'` in the served bytes).
- **`/api/claim`, `/api/welcome/me`, `/api/welcome/complete`** — the fetch handler harvested
  verbatim from the walk staging worker (`walk-beginning-staging-worker.js`), page branches
  renamed to the free copies, alias redirects kept (`/<alias>` → 302 live nayanet.app pages).
  Unknown paths → plain 404 naming `/free`. `/` serves a small index naming the route.
- **Two workers, not one** — one worker cannot hold pricing 11.36 MB + walk 3.29 MB under
  the 10 MB gzip limit, so the pricing page and the free route are separate staging workers.
  The v78 button href and the v78 `FREE_ENTRY_URL` const carry the staged free URL with a
  comment: live deploy swaps that one string for the live walk entry.

### The button (v78) — under the trial banner, in the language

- **Placement — READ THIS FIRST.** The button sits **directly under the trial banner**,
  in the visible hero, above the chart. Rationale: v77 proved the banner fully in viewport
  at scroll 0 at 1440×900 and 390×844; placing the button above the banner, or in the
  letter-controls row, would push the banner below the fold at 390. The button is the first
  action under the trial promise — the promise ("Nine days free…") and the free way in,
  together, at first paint. The button is a plain `<a>` link — it works with JS off, so it
  is never a dead button even without JS.
- **The object:** obsidian pill (`.primo` harvested verbatim from the Hub, lines 689–698,
  NAYA-BTN-005: obsidian gradient, 1.5px white rim, radius 999px, `primo-sheen` 3.5s, hover
  lifts −2px + `var(--glow)`), rim in **green `#2fe89e`** (free/positive on the Naya Code
  spectrum — distinct from the paid purple Start), white word "Enter free", sub "Zero cost,
  zero risk" (both words harvested from the page), star jewel modeled on `.finale-star` in
  green. **Orbit:** two glint orbs circling the button's outline on a measured rounded-rect
  `offset-path` set by a small JS IIFE — CW 60s + CCW 90s (the vortex, alternating, slow),
  two static faint green rings as the track; `prefers-reduced-motion` stops the orbs; JS off,
  the orbs sit still and the button still works. **Alive on hover** — lifts and lights up
  whole; dead on hover would be a FAIL and it is not.
- **Change groups (exactly 3):** (G1) CSS — `.free-entry-btn` + orbit + star rules; (G2) HTML
  — the button section after the trial banner (+ placement-note comment); (G3) JS —
  `FREE_ENTRY_URL` const + orbit IIFE + the two free controls rewired (see the flagged change
  below).

### ⚠️ DELIBERATE FLAGGED CHANGE — the two existing free controls now open the route

`#finaleFree` ("or continue with Naya Free") and `#chooserFree` (chooser foot) previously only
wrote a welcome note into `#massiveNote` and scrolled to it — a dead end, the exact defect
this round kills. They now do `window.location.href = FREE_ENTRY_URL` — they open the route.
The note text ("Welcome in — you're starting on Naya Free…") is gone from the page
("Welcome in — you" 0× in v78). **This is part of "the route", not a removal for its own
sake — but it changes two controls the brief did not name, so it is flagged here in bold:
if the captain disagrees, strike it and the controls go back to the note.** Paid paths are
untouched: all four Start buttons still call `openChooser(chosen)` only; the nine tiles
still link to their paid PayPal Smart Links (`nayanet.app/power-monthly` … `max-yearly`);
trial banner verbatim; prices shown once, in the chart only.

## HARVESTED VERBATIM — FROM WHERE

- Pricing v77 source → v78 base (`pricing/v77/pricing-v77.html`, sha `b043167b…`).
- Walk `walk-beginning-fixed.html` (3,288,041 B, sha starts `df17ac67`) → `walk-free.html`.
- Entry `identity-fixed.html` (305,681 B, sha starts `84c2b29a`) → `free-entry.html`.
- Walk staging worker fetch handler (`walk-beginning-staging-worker.js`) → free worker
  handler (extracted programmatically from `export default {`, branches renamed).
- `.primo` (Hub lines 689–698) + `.finale-btn`/`.finale-star`/`.finale-copy`/`.finale-title`/
  `.finale-sub` + `orb-spin` keyframes → the free button.
- Info-eye SVG (`.plan-eye` on the pricing page) → the entry page's free eye.
- Supabase anon key read programmatically from `identity-live-extracted.html`, embedded only
  in the staging worker, never printed (it is the public anon key already shipped in the
  live page). Cloudflare account `b5e2a51b3e883f7722287c5f51b1196b`; deploy pattern from
  `deploy-v77-live.py` / `deploy-ninaya.py` (`js_encode`, `set_page_value`, `split_multipart`).

## DIFF VERDICT — ONLY THE ROUTE AND THE BUTTON

`diff` v78 vs v77 (51 lines, 8,941 B): exactly **3 change groups** — (G1) CSS rules for the
free button + orbit; (G2) the button section after the trial banner; (G3) JS: the
`FREE_ENTRY_URL` const, the orbit IIFE, and the two free-control handlers rewired to the
route. Nothing else differs: **no price, strikethrough, Smart Link, period label, founders
strip, plug-in row, letter, or chart line appears in the diff.** Counts in v78:
`FREE_URL` 2×; `id="freeEntry"` 1×; `<span class="plan-free">Nine days free</span>` 9×;
"Welcome in" 0×; `openChooser` 7×; tile hrefs `power-monthly`/`max-yearly` 1× each;
`bonus`/`bottomStart`/`blockchain` 0×.

## STAGED VERIFICATION (all before reporting; NO live touch — live still serves v77)

Staging run `stage-in-memory.py` (2026-11-17 ~00:26–00:31Z), exit 0. All checks through the
workers' **real fetch handlers in Node** (js_decode never used — lossy) plus live HTTP.

- **Live pre-state re-proven:** `https://nayanet.app/pricing` serves v77 byte-exact
  (Node driver MATCH: true, 11,355,594 B, sha `b043167b…`; HAVE trial banner + plan-free
  spans; NOT `freeEntry`/`free-entry-btn`/`FREE_ENTRY_URL`). **Live untouched.**
- **Staged pricing serves v78 byte-exact:** spliced worker + read-back both MATCH
  (11,360,503 B, sha `ca2eafeb…`). Markers HAVE: `id="freeEntry"`, the staged free URL,
  "Enter free", "Zero cost, zero risk", banner sentence verbatim, plan-free spans,
  "or continue with Naya Free", founders strip, "Plug in your AI", "WANT THE FULL
  PICTURE", "If PayPal holds a payment", `power-monthly`, `max-yearly`, `openChooser`.
  NOT: `bonus`, `bottomStart`, `blockchain`, "Welcome in — you". **DRIVER: PASS.**
- **Free worker PUT:** 200, created `2026-11-17T00:25:51.126496Z`, tag
  `9878c6f9c3254788ab4b2f970df50b5d`; subdomain enabled (200). Read-back sha MATCH.
- **Free routes byte-exact over HTTP:** `/` 1,966 B MATCH; `/free` 307,918 B MATCH
  (sha `e0534a61…`); `/free/walk` 3,288,471 B MATCH (sha `ea1e77a6…`). Node drivers PASS
  (entry: free line + `freeEye` + `WALKTHROUGH_URL = '/free/walk'`; walk: `nayanet_free_entry`,
  `data-door="Hub"`, free line).
- **Walk end doors in the SERVED bytes, in order:** Hub, Dashboard, Personal, Business,
  Space. Hub is rec-first (`.p3-door-rec`); Hub door URL `https://nayanet.app/`;
  `pricingBtn` still → `https://nayanet.app/pricing`.
- **`/free/hub`:** 302 → `https://nayanet.app/` (the Hub). **DRIVER: PASS.**
- **API, live against the staging worker:** POST `/api/welcome/complete`
  (test alias `f4probeex`) → 200, reveal pages returned
  (`personal: /f4probeex`, `business: /f4probeex/business`, `space: /f4probeex/space`,
  `dashboard: https://nayanet.app/dashboard?name=F4%20Probe&alias=f4probeex`);
  GET `/api/welcome/complete?alias=f4probeex` → 200, alias read-back MATCH;
  GET `/f4probeex` → 302 to the live personal page. Same checks passed in the staging run
  for aliases `f4testekcpgpnv` and `f4testmhxphhky`.
- **The free button's href answers:** GET the staged free URL from the staged pricing
  page → 200, 307,918 B — the route answers. End to end: staged pricing → free button →
  entry → walk (Hub first) → Hub 302. No payment asked anywhere on the route.
- **Test aliases left in KV** (shared `WELCOME_ASSETS`, test-only, named here):
  `complete_f4testekcpgpnv`, `complete_f4testmhxphhky`, `complete_f4probeex`.

## THE EPERM FLAKE — STAGING PIVOT (why files are not all on disk)

Since ~00:11Z every VM filesystem content write fails (`[Errno 1] Operation not permitted`
from python, shell, and Node alike; small writes sometimes "succeed" as silent 0-byte files;
disk has 92 GB free). The round pivoted to **staging entirely in memory**
(`stage-in-memory.py`): v78 + the free worker were built, spliced, PUT, and verified with
zero big disk writes — the staged workers ARE the byte-exact record, and the served bytes
match the in-memory shas above. Two background retry loops (pids 267882, 267883, started
~00:29Z) keep attempting the disk writes (`build-v78.py`, `build-free-staging-worker.py`)
and will land the files when the flake clears. **As of 00:30Z the flake is still up:**
`pricing/v78/pricing-v78.html`, `v78/diff-v78.txt`, `walk-free.html`, `free-entry.html`,
`free-index.html`, `free-staging-worker.js` are all 0-byte files on disk. The small files
(this record, the build/stage scripts, the check scripts) ARE on disk — the file tools
work for small writes. Anything can be reconstructed byte-exact from the staged workers'
served bytes at the shas above.

## HONESTLY NOT DONE

1. **No browser eye has walked the route.** VM browsers are dead (Firefox exit 139,
   Chromium exit 133). Everything above is mechanical proof: byte-exact served bytes,
   real fetch handlers, HTTP status + Location, API round-trips. The checker MUST click
   through the staged route at 390 / 1440 / 1851×1009 — entry, walk, end doors, Hub —
   and read the free button on the staged pricing page (orbit, alive on hover, banner
   still fully in viewport at scroll 0). No eye proof exists until then.
2. **Big files not yet on disk** (flake, above). Retry loops running; shas to verify
   against when they land: v78 `ca2eafeb…`, walk-free `ea1e77a6…`, free-entry `e0534a61…`,
   free worker `7a6a9095…`.
3. **GitHub filing** — DONE: branch `pricing-f4-free-entry-20261116` in
   `SoulSchoolAcademy/NayaPOWER` (TEAM-NITRO is a folder inside that repo),
   commit `44d58b59206c2fecc5979c00500a50c58f84bf08` (+ this record's amendment
   commit — see the report), 9 blobs, maker-record blob read-back MATCH.
   NOT merged. The 11 MB v78 source is not filed; the staged worker serves it
   byte-exact. `diff-v78.txt` not filed (0 bytes on disk — flake).
4. **Live deploy** — not mine, not run. Live still serves v77. The live deploy swaps ONE
   string: the staged free URL in v78 (`FREE_ENTRY_URL` + button href) for the live walk
   entry, per the comment in the file. That swap is Shawn's tap.
5. **Checker cold verification** — this record is the maker's staged proof only; the
   independent checker verifies from served bytes (brief items 1–4: route whole, button on
   top in the language, paid paths untouched, diff scope only).
