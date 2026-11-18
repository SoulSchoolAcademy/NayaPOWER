# MAKER REPORT — Pricing Free Taken-State Certificate Fix
**Round:** BRIEF-PRICING-TAKEN-STATE-FIX-20261117 · **Date:** 2026-11-17 ~03:40–04:05Z
**Maker:** Naya Nitro Narzan · **Branch:** `pricing-f4-free-entry-20261116` (PR open, unmerged)
**Base:** Marcellus swap tip commit `c74f6dae` — `/free` 310,212 B,
sha256 `dfe70a8c8a4d89aa49a31aa56d077b51867ef4e42f276ce28bc39d23fa6370b2`
**Staged:** https://naya-pricing-free-staging.nayapower.workers.dev/free
**Nothing live, no merge.** The live step stays HELD until this round's eye passes.

## What changed — exact diff

### 1. `/free` entry — one appended taken-state block, nothing else

New entry: **311,426 B (+1,214)**, sha256
`3d5b913f117b90a1fdd3e72347f8458c4de4429972eb05a38c6fb118f7fbf285`.
The diff is additions only. The block (lines 1154–1160 of the staged entry):

```css
/* TAKEN STATE (2026-11-17): the taken document takes the fresh certificate's own presentation — the name sits IN FLOW in the center (as the certified name does), carries the certified glow, the face flows and the plaque scrolls when the document is taller than the viewport, and the start-over control shows. Gated on the taken state only — the fresh certificate is untouched. */
.cert-plaque:has(.alias-status[data-state="taken"]) .cert-name{position:static;transform:none;width:auto;pointer-events:auto;text-shadow:0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55);}
.cert-plaque:has(.alias-status[data-state="taken"]){overflow-y:auto}
.cert-plaque:has(.alias-status[data-state="taken"]) .identity-face{position:static;display:flex;flex-direction:column;justify-content:center;min-height:100%;box-sizing:border-box}
.cert-plaque:has(.alias-status[data-state="taken"]) .face-head,.cert-plaque:has(.alias-status[data-state="taken"]) .face-foot{align-self:auto}
.cert-plaque:has(.alias-status[data-state="taken"]) .face-foot{margin-top:16px}
.cert-plaque:has(.alias-status[data-state="taken"]) #startOverBtn{display:inline-flex;align-items:center;justify-content:center}
```

What each line does, and which item it serves:

- **Name in flow** (`position:static; transform:none; width:auto`): the taken
  name was `position:absolute; bottom:calc(100% + clamp(...))` above the
  input, growing upward as it wrapped until it struck through the title and
  "This certifies that". Static puts it in the center row below the head band,
  exactly where the fresh certificate's name sits. **Item 1.**
- **Certified glow, verbatim** (`text-shadow: 0 0 38px rgba(160,107,255,0.16),
  0 3px 30px rgba(0,0,0,0.55)`): the exact glow from
  `.cert-plaque.is-certified .cert-name` (SN-2922: official, glowing, solid).
  Base `.cert-name` had `text-shadow: none`. **Item 2.**
- **Start-over shows** (`#startOverBtn{display:inline-flex; ...}`): the
  button was `display:none` except under `.is-certified`, which the taken
  state never has. Same ghost button, same existing click handler (clears
  `nayanet_smart_alias`, `nayanet_smart_name`, `nayanet_vault_key`,
  `naya_welcome_right_v1`, `nayanet_free_entry` + session `nayanet_user_name`,
  `nayanet_pending_route`, then reloads). **Item 3.**
- **Plaque scrolls + face flows** (`overflow-y:auto` on the plaque;
  `.identity-face` static flex column, `min-height:100%`): mirrors the
  follow-on round's proven flow+scroll cure for the certified state. The
  scroll rule is deliberately NOT gated on `max-height:700px` — the taken
  foot is taller than the certified one (benefit + privacy + hubNote), so a
  height gate would still strand ENTER at desktop with a long name.
  `overflow-y:auto` scrolls exactly when content exceeds and centers when it
  fits. **Item 4.**

Untouched, byte-verified: all `.cert-plaque.is-certified` rules, all old
`.cert-name` rules, and all 9 old `text-shadow` declarations are byte-identical
(new total is 10 — the one extra is the taken glow). The fresh certificate is
UNTOUCHED. `/free/walk` UNCHANGED: 3,292,257 B, sha256
`2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea`.

Root cause (why all four items were one fix): every follow-on narrow fix was
gated on `.is-certified`, which the taken state never has — the taken plaque
kept the base absolute-name / no-glow / hidden-start-over / `overflow:hidden`
behavior while the fresh certificate got the cured presentation.

### 2. Staging worker — `/sw.js` + `/manifest.webmanifest` served (item 5)

New worker sha256 `b70538d6ec32cba95d280a3e33f5e73bde24698112dafc1f97f90b338376d66a`
(Cloudflare read-back MATCH, gzip under the 10 MB limit). Two new routes,
both harvested VERBATIM from live `https://nayanet.app`:

- `/sw.js` — 567 B, sha256 `abac2ab507fc162788d9bdcd60f895049222e125d1445a4870be71342625d6a3`,
  `Content-Type: application/javascript`. The live self-retiring service
  worker (registers, then unregisters itself — the cure for the stale worker).
- `/manifest.webmanifest` — 581 B, sha256
  `b4abd81c41e85f4149be355f740dd8ff9b136f6ea85e8b5874073a0686c67e81`,
  `Content-Type: application/manifest+json`.

The entry already registers `sw.js` (line ~1728,
`navigator.serviceWorker.register('sw.js')`, rejection swallowed) and links
the manifest + `icons/apple-touch-icon.png`; the worker's final fallback was a
plain 404, and `sw.js` / `manifest.webmanifest` sat in the worker's `reserved`
list, so they never hit the alias-redirect branch — they 404'd, and every run
logged `error: A bad HTTP response code (404) was received when fetching the
script.`

## Live verification — all five items, fresh AND taken

Probe: Playwright Chromium through the localhost forwarder
(`127.0.0.1:18080`); Firefox fires zero Supabase reads in this VM.
Test aliases claimed on staging via `/api/claim`: long
`alexanderchristopherbennett` / "Alexander Christopher Bennett" (29 chars,
cert 753, device key `nayanet_key_takenfix001`) and short `takenfixshort` /
"Taken Fix Short" (cert 755, device key `nayanet_key_takenfix002`). Taken
state = fresh browser profile re-entering the claimed alias (own-device
restore = fresh state for the regression check).
Scripts: `probe-after.py`, `probe-after2.py`, `sw-poll2.py`, `shots-clean.py`;
results in `probe-after.json`, `probe-after2.json`; screenshots in
`shots-after/` and `shots-after2/`.

### Item 1 — taken name never overlaps the title / "This certifies that" — PASS
- **390×844 taken (long):** name `position:static`, box y275–430, below the
  head band. Screenshot `shots-after/taken-390x844-load.png`: "CERTIFICATE OF
  SMART IDENTITY" and "This certifies that" fully legible, clear gap above
  the glowing name ("Alexanderchri / stopherbenne / tt" — 3 lines in Marcellus;
  the before-probe's Georgia fallback rendered 2 lines). Before the fix the
  name struck through "This certifies that" at this width.
- **635×349 taken (long):** name box y275–382. Screenshot
  `shots-after2/taken-long-635x349-load.png`: title + certifies line clear,
  glowing name flowing below ("Alexanderchristopherbe / nnett"). Before the
  fix the name box sat at y7–114, painted over the seal/top-bar area.
- **1440×900 taken (long):** name box y332–409, single line.
  Screenshot `shots-after2/taken-long-1440x900-load-clean.png`: the whole
  certificate reads clean — title, certifies line, one-line glowing name,
  input, "already claimed", Smart Link, Mail, ENTER, USE A DIFFERENT ALIAS.
  Before the fix the name overlapped BOTH the title and the certifies line.
- **Short alias taken** (390 + 1440): name static, one line, no overlap
  (name box y275–327 at 390).
- Method note: the probe's Range line-box overlap test still reports a
  small overlap against the "This certifies that" line box at 390/635 — it
  reports the SAME overlap on the eye-passed FRESH certificate at the same
  widths (tight Marcellus leading: line-height 0.98em < font ascent). The
  line-box test over-reports; the screenshots are the arbiter, and they show
  clear glyph separation at every width, taken and fresh alike.

### Item 2 — taken name carries the certified glow — PASS
Taken name computed `text-shadow` at all widths, both aliases:
`rgba(160, 107, 255, 0.16) 0px 0px 38px, rgba(0, 0, 0, 0.55) 0px 3px 30px`
— identical to the fresh certificate's glow. Before the fix it was
`text-shadow: none`. The glow is visible in every after screenshot (purple
aura around the Marcellus letters). `document.fonts.check('52px Marcellus')`
true in all runs.

### Item 3 — "USE A DIFFERENT ALIAS" present and working in the taken state — PASS
- `display:flex` in the taken state at 390 / 635 / 1440, both aliases
  (before: `display:none` everywhere). Button box e.g. 390: x82–307, y736–776.
- Click test (390, taken, long alias): after ENTER-on-taken the hubNote shows
  ("That alias is already claimed on another device. Pick a different alias
  to continue."); clicking USE A DIFFERENT ALIAS returns to composing:
  status `neutral`, input empty, plaque class back to
  `identity-pro-card cert-plaque`, and all five localStorage keys read
  `null` (cleared). The reload path works from the hubNote state too.

### Item 4 — taken page scrolls at 635×349 so ENTER is reachable — PASS
- At load, 635 taken (long): ENTER box y597–655, below the 349px fold;
  plaque `overflow-y:auto`, `scrollable:true`.
- **User wheel scroll** (`mouse.wheel`, veil dismissed — see probe note):
  plaque `scrollTop` 0 → 22 AND document `window.scrollY` 0 → 400; ENTER
  moves to y175–233, `inViewport:true`. A second clean run:
  `scrollTop` 0 → 22, `scrollY` 0 → 557, ENTER y17.6–75.6.
  Screenshot `shots-after2/taken-long-635x349-scrolled-clean.png` shows
  ENTER in the viewport after scrolling (its top sits under the sticky top
  bar at that exact offset — one more wheel notch centers it; normal scroll
  behavior, same as the fresh certificate).
- 390: wheel moves the plaque 0 → 23 (short alias: 0 → 23, `scrollY` 0 → 4);
  ENTER already in viewport at load. 1440: ENTER in viewport at load.
- Before the fix: `overflow:hidden`, no user scroll path at all, ENTER
  stranded below the fold.

### Item 5 — console 404 ("404 when fetching the script") — PASS, fixed
- Before: every run logged `error: A bad HTTP response code (404) was
  received when fetching the script.` Cause confirmed by curl: staged worker
  404'd `/sw.js`, `/manifest.webmanifest`, and `/icons/apple-touch-icon.png`.
- After: **zero console errors across all 11 probe runs** (6 in round 1, 5 in
  round 2). Live HTTP (re-checked 2026-11-17 ~04:03Z): `/sw.js` 200, 567 B,
  `application/javascript;charset=utf-8`, sha256 match; `/manifest.webmanifest`
  200, 581 B, `application/manifest+json;charset=utf-8`, sha256 match.
- Registration proven live, not just by HTTP: a 100 ms poll from navigation
  (`sw-poll2.py`) caught `navigator.serviceWorker.getRegistration()` returning
  scope `https://naya-pricing-free-staging.nayapower.workers.dev/` at ~2.0 s,
  and `context.service_workers` lists
  `https://naya-pricing-free-staging.nayapower.workers.dev/sw.js` as a live
  worker — the self-retiring script registers, runs, and unregisters itself,
  exactly as the localhost test of the live copy showed (registered OK,
  self-unregistered, no reload, zero console errors). Playwright's page
  `request` listener never surfaces service-worker script fetches — that is a
  probe observability quirk, not a page fact.
- The only other console entry seen anywhere in the round: a single HTTP 409
  on `/api/claim` when ENTER is pressed on a taken alias — the claim
  endpoint's by-design "already claimed" response, handled by the page
  (hubNote). Not an error, not in scope.

### Fresh certificate regression — UNCHANGED, passes
Fresh (own-device restore, same long alias) at 390 / 635 / 1440: name glowing
(same shadow string), ENTER visible at load at 390/1440 (y630–688 / y708–766),
start-over `display:flex`, no overlap in the screenshots. Fresh 635 ENTER at
load y558–616 (below the fold, as before — the fresh state was already
scrollable and is untouched by this diff).

## Probe notes (for the checker)

- **The Install App veil** (`#installVeil`) auto-shows a few seconds after
  load on fresh profiles and intercepts pointer events + covers screenshots.
  It is pre-existing, untouched by this round, and a user dismisses it with
  NOT NOW / ×. Round-1 probes dismissed it once after load; the veil can
  re-show minutes later, which ate one wheel test and two screenshots.
  Round-2 probes dismiss it immediately before EVERY measurement, screenshot,
  and wheel test — that is the shape to copy.
- **`/icons/apple-touch-icon.png` still 404s** on the staged worker — only
  fetched on iOS add-to-home-screen, never on desktop load; out of scope for
  item 5 (its bytes are not harvested anywhere in scope). Noted, not fixed.
- **Staging caveat:** the live manifest's `start_url` is `/index.html`,
  which 404s on the staging worker — staging-only; nobody installs staging.
- **Test Supabase rows:** certs 753 (`alexanderchristopherbennett`) and 755
  (`takenfixshort`) are this round's; certs 737–746 from the F4 + follow-on
  rounds are still open, plus cert 754 (claimed by another lane between my
  two claims — not mine). They need a keyed delete or Shawn's hand, as prior
  checkers recorded; no delete was attempted in this round.

## Filing

- Branch: `pricing-f4-free-entry-20261116` — round commit `31f4ddc5` on top of
  `c74f6dae`, plus filing-completion commit `SEE BELOW` adding the two
  evidence scripts the first filing's file list missed (see note), no merge,
  nothing live. Files on the branch (small files only; the 3.2 MB walk /
  3.6 MB worker sources are NOT filed — the staged workers are the byte-exact
  record, as in prior rounds): this report, `build-taken-fix.py`,
  `probe-after.py`, `probe-after2.py`, `sw-poll2.py`, `shots-clean.py`.
- **Filing note (honest record):** the first filing run's file list carried
  only 4 of the 6 files (a sed left the two extra entries out of the list),
  so commit `31f4ddc5` holds the report + build + two probes. This report
  was corrected to say so and re-filed with `sw-poll2.py` +
  `shots-clean.py` in the follow-up commit below — the branch now holds
  everything this report claims.
- Build script: `build-taken-fix.py` — regenerates the Marcellus-tip base in
  memory, asserts base shas, verifies live staged `/free` still serves the
  tip entry, harvests the live PWA assets, applies the taken fix, patches
  the worker, Node-drives the worker, stages, read-backs, live-verifies.
- Live re-verification at filing time (~04:03Z): `/free` 200, 311,426 B,
  sha256 `3d5b913f…`; `/free/walk` 200, 3,292,257 B, sha256 `2370eae2…`;
  `/sw.js` 200, 567 B; `/manifest.webmanifest` 200, 581 B.
- **Filed commit SHA: (recorded in the parent handoff — the branch tip IS the
  commit; verify with `gh-direct.py GET /repos/SoulSchoolAcademy/NayaPOWER/git/ref/heads/pricing-f4-free-entry-20261116`.)**
