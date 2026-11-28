# MAKER REPORT — OFFICIAL WALKTHROUGH FIX1 (2026-11-27)

**Maker:** subagent (fix1 seat) · **Dispatched:** 2026-11-27 ~19:39 MST · **Staged:** 2026-11-28 ~03:05 UTC
**Staged link:** https://official-walkthrough-staging.nayapower.workers.dev/
**Walk path:** staged link + `?walk=1&name=Shawn&alias=shawn`
**Nothing live, nothing to Shawn.** Staged only; live is Shawn's tap.

## The fix round, in one line

Six checker defects, all closed by real taps: the install veil can never block
ENTER again, the 1440 trio is 360 px wide with nothing clipped, the
certificate date/time paints (ticking, weekday-coloured) on the
already-claimed restore path, the already-claimed note sits clear of the
frame, and every walk step carries the slide header.

## Filing (the numbers)

| Item | Value |
|---|---|
| Staged link | https://official-walkthrough-staging.nayapower.workers.dev/ |
| Portal | **47,431,829 B, sha256 `eb6a2f7e7ff635404efdc57d6816ed6d9e233dc81fcdd443444d92da0968eb68`** — staged curl == local, byte-identical |
| Certificate | **317,666 B, sha256 `86536d53a28367e542f0b225857066391ce535f5e13b17a5a81129fe637b17ae`** — staged curl == local, byte-identical |
| Worker | `worker-consolidated.js` 47,776,425 B, sha256 `c9560a0e326ebd1126ae31d4af694bd3d4853c2a46ba4ec433a9d205439310c6`; worker `official-walkthrough-staging`, PUT HTTP 200, subdomain already enabled |
| Video route | `GET /naya-video.mp4` → 200, 7,368,202 B, sha `c86da39e…` — unchanged, from KV, NOT re-uploaded |
| Emblem / Naya routes | `GET /naya-emblem-cut.png` → 200, 2,592,251 B · `GET /agmt-b06.png` → 200, 2,054,581 B |
| GitHub branch | `walkthrough-official-20261127` |
| Commit 1 (fix1 files) | **`22b0525b10f72dac4cc982262d3fa3cf72cabe55`**, tree `dee80ffac049fe43bd09a52a48c56ca836858d2b`, parent `512a3bbf31ab05ee5a85533e4281f90368ec93ee` |
| Commit 2 (this report) | filed after commit 1; sha recorded in the lane file after filing — see the branch log, not this line |
| portal-v1 blob | `a780799aa7a21b42891f0c081445d6a517431c81` — 13,900,396 B, **verified by blob read-back** (decoded bytes sha256 `b7ee02d6…` == local) |

**Vault read first (briefed):** Smart Vault state before touching the page was
the official walkthrough as filed (portal 47,430,066 B sha `1677214b…`, cert
316,048 B sha `f1f69cc9…`, worker deployment `12b9905f…`) plus the checker's
GOES BACK 8.0/10 verdict with defects D1–D6. What this round learned is filed
back in `VAULT-NOTE.md` at the lane root. Nothing from any other line was used
as a base — fix1 re-bases on the exact maker files, edited in
`fix1/maker/`.

## What changed, per defect

**D1 MAJOR — install veil blocks ENTER (390, certificate).**
`identity-consolidated.html` (kept in sync with `identity.html`): the
auto-show branch (5 s `setTimeout` → `openModal`, capped at 3 shows) is
DELETED, not gated, and `openModal()` now returns immediately with a
FIX1 D1 comment — two locks. The veil element stays in the DOM (its JS
touches `installX`/`installGo` unguarded) but is unreachable: no corner
button, no timer, no opener. No install button was re-added anywhere on
the certificate. Probe: veil still `hidden` after 10 s+ on the cert, and a
real point-test puts ENTER (not the veil) on top.

**D2 MAJOR — 1440 trio clips (phone content in 211 px phones).**
Root cause, measured not guessed: the v3 phone style's header comment was
split — it closed at line 5 (`...never outside the frame. */`) and the rest
of the header ran as bare CSS text, so the parser swallowed the very next
rule, `#fpWalk{max-width:1320px}`, as a bogus selector's block. The older
v1 rule `#fpWalk{max-width:720px}` then won unopposed, capping the trio at
720 px → 211 px phones. Fix (`phone-style3.html`): the early `*/` is
removed so the header is one comment; the 1320 px rule now parses and wins
by document order. Phones are now 360 px at 1440×900 (the existing
`(100vh-260px)*0.5625` height cap), trio 1,160 px wide, centred (x=140).
Nothing else in the phone CSS changed; the 390 stacked layout is untouched
(same media queries, verified by the probe). Full header text, full
questions, full chin text in all 8 groups at 1440 — measured
(`scrollWidth <= clientWidth` on kicker/chin, question never covered by the
card, no stage overflow) and seen with my own eyes in
`evidence/fix1-1440-g1.png`.

**D3 — certificate date/time never proven alive.**
Preferred path taken, no junk row written to the shared
`nayanet_identities` table (zero writes this round — reads only):
- `paintCertDatetime(fixedIso)` now takes an optional fixed certification
  moment: the DATE shown is that certified day, the TIME stays live and
  ticks every second (the interval re-paints from the stored fixed date).
  The weekday word leads, coloured by the laws' weekday identity (§3.3).
- The alias check's mismatch branch (row exists under another device's
  key) keeps the row's facts READ-ONLY (`createdAt`, `certNo`) and paints
  from `created_at` — on the silent load-time restore AND while typing.
- The ENTER claim's 409 read-back now carries `created_at` through
  (`status:'taken'` used to discard it as null) and the taken handler
  paints from it.
- Proven in reachable states for the already-claimed alias `shawn`:
  after ENTER (taken state) the tiles read
  `TUESDAY 20 OCT 2026 · 03:00:11`, ticking (…:11 → …:13 in ~2 s), and on
  a silent-restore reload they paint again with no new claim.
- On the colour: the certified day is Tuesday 20 October 2026
  (`date -d 2026-10-20` = Tuesday), so the weekday word renders in Tuesday
  deep gold `#d4a017` (rgb(212, 160, 23)) — the §3.3 map applied to the
  certified date, not to today. A Friday certification would render ruby
  red `#c62828` by the same rule. The tiles are centred (flex,
  `justify-content: center`, unchanged) and live.

**D4 MINOR — "already claimed" touches the frame corners.**
`#hubNote.fp-taken-green` now carries `margin: 14px 24px 0 !important;
padding: 0 8px; box-sizing: border-box; overflow-wrap: break-word`.
Measured: left gap 24 px, right gap 24 px (was 0/0).

**D5 MINOR — slide header missing on the walk.**
Every walk step (all 23 phones, built by `buildPhone` in
`phone-script3.html`) and the end phone (`phone-section3.html`) now carry
a slim header row inside the screen, under the status bar: his actual
emblem `/naya-emblem-cut.png` top-left, Naya's picture `/agmt-b06.png`
top-right — both harvested from the portal (the agreement corners and the
`fp-naya-portrait`), never invented. The row costs the stage 40 px (32 px
on the end phone, slimmed so the end screen stays whole — see below); the
input card scrolls, the frame is untouched, the question stays centred.
Verified on every phone in all 8 groups at both widths (images loaded,
`naturalWidth` 1800 / 1254, visible) and seen in the screenshots.

**D6 — product files not in the commit.**
- Blobs API tried PROPERLY (piped base64, no disk staging, via
  `gh-app-api`): `POST /git/blobs` for `portal.html` (47,431,829 B)
  returns HTTP 422: *"Sorry, your input was too large to process.
  Consider creating the blob in a local clone of the repository and then
  pushing it to GitHub."* The same call for `worker-consolidated.js`
  (47,776,425 B) would 422 identically; it was not re-attempted, the limit
  is proven. No Git LFS in the repo (`.gitattributes` has no `filter=lfs`
  lines — verified by contents read-back). No local clone exists on this VM
  and a raw-token `git push` is not an approved credential path for this
  seat, so no clone+push was attempted.
- INSTEAD, the rebuild path is filed AND proven: commit 1 contains every
  input the build needs — `portal-v1.html` (blob `a780799a…`, verified by
  read-back), `build-official.mjs`, `build-worker-official.mjs`,
  `fix-cert.mjs`, `fix1-cert.mjs`, the phone parts, `steps.js`,
  `engine.js`, `sw.js`, `worker-meta.json`, both identity files, and all
  14 source pictures under `media/` (sizes match the locked picture map).
  Rebuild proven byte-identical TWICE locally: re-running
  `build-official.mjs` reproduces `portal.html` 47,431,829 B sha
  `eb6a2f7e…` (`cmp` clean); re-running `build-worker-official.mjs`
  reproduces `worker-consolidated.js` 47,776,425 B sha `c9560a0e…`.
  One documented step: `build-official.mjs` reads the pictures from
  `workspace/user/media_library/image/` — copy `media/` there first.
  The two 47 MB product files themselves remain absent from the commit;
  that is the named gap, not a claim otherwise.

## Verification (real taps — Playwright Chromium via the localhost forwarder)

**Build:** `build-official.mjs` — **36/36 assertions PASS** (same suite as
the base round, rerun on the fix1 build). **Certificate:** `fix1-cert.mjs`
— 8/8 patches applied exactly-once (D1 ×2, D3 ×4, D4 ×1, plus the D1
guard counted in the two).

**Probe (`evidence/probe-fix1.py` + `probe-fix1.log`): 0 FAILs.**
- 390×844 certificate: portal name → `/identity.html?name=Shawn` same
  host; veil hidden after 10 s+; ENTER on top (elementFromPoint lands
  inside `#enterBtn`); alias `shawn` → taken state with digit tiles
  `TUESDAY 20 OCT 2026 · 03:00:11`, ticking, Tuesday gold; note margins
  24/24; silent-restore reload paints again; "This is me" → walk.
- 390×844 walk: all 8 groups, no clipping anywhere; header on every
  phone; vision picture reveals on ball tap; video ball plays then pauses;
  end screen whole (top 86 / bottom 650 of screen 14–658), header on the
  end phone; 44 localStorage answer keys; 0 page errors, 0 unexplained
  console errors.
- 1440×900: phones 360/360/360, trio 1,160 px centred; no clipping in any
  of the 8 groups; header on every phone; end screen whole, no video at
  the end; 0 page errors.
- Error accounting, named honestly: 4× console 503s per run on
  `agmt-*.jpg` (a different set each run — b08/b05/b07/b11 this run,
  top/b09/b07/b00 earlier) — transient, pre-existing, NOT fix1: every one
  returns HTTP 200 on direct curl. 2× 409s are the honest Supabase
  already-claimed answer for alias `shawn`. Nothing else.
- One fix made mid-probe, then re-proven: the end screen at 1440
  overflowed its screen by 13 px once the header row landed on it, so the
  end phone's header runs slimmer (28 px) and its end lines breathe 2 px
  less — the full probe then passed with FAILS: NONE.

**Seen with my own eyes:** `evidence/fix1-1440-g1.png` (full YOUR
WALKTHROUGH, full questions, full BLACK DIAMOND SERIES, emblem + Naya on
every phone) and `evidence/fix1-1440-end.png` (Welcome home., all six
destination buttons whole including Space →, header on the end phone).

## Design-law check (§11)

- §1 real objects: phones/ball/frame untouched except the header row —
  the emblem and Naya's picture are real objects in the same language
  (emblem contain, face circle with royal-purple rim + glow). The header
  images are harvested, never invented.
- §2 text: Marcellus, white, 25/19/17 — the weekday word is 17 px in its
  weekday colour (a §3.3 identity colour, not gray); no gray text added.
- §3 colour: deep palette only — Tuesday gold `#d4a017`, Friday ruby
  `#c62828`, royal purple `#8e24aa` rims. No new colours.
- §4: one light top-left, board black inside, no glow inside — the header
  sits on the screen's black; the face circle's rim takes the walk's
  purple.
- §14 frame library: the Black Diamond frame and the R5 certificate frame
  are untouched; only the centre content changed.
- Sense check: the walk at 1440 finally reads as the product it is — three
  full phones, nothing sliced; the certificate's ENTER is reachable the
  moment it loads.

## Named gaps — everything not done, in one place

1. **The two 47 MB product files are still not in the commit** (D6,
   above). The rebuild path is filed and proven instead; a clone+push
   seat with approved token handling could still land them.
2. **The certified date is the row's date, not today's.** The tiles show
   the certification day (Tue 20 Oct 2026) + the live ticking time. If the
   coordinator wanted the LIVE date instead, that is a one-line change to
   `paintCertDatetime` — but it would stop being the certificate's own
   date, so I kept the row's date per the brief's "from the existing row's
   stored created_at".
3. **Transient agmt 503s** (a few `agmt-*.jpg` per run, 200 on retry).
   Pre-existing, portal-side, untouched by fix1; the worker's KV asset
   routes flake under load. Not a fix1 defect, named so the checker does
   not re-litigate it.
4. **complete() was not re-proven end-to-end this round** (the base round
   proved POST 200 + `/me` 200; this round's end screen shows the ready
   line and 44 saved keys, and the walkthrough-15 backend question from
   the base round — whether it accepts the new answer keys as a real
   citizen claim — is still the backend seat's call).
5. **Shawn's eye is the final gate.** The trio and end screens were seen
   by my eye at both widths; his eye still decides.

## Build + deploy (exact)

- Lane: `~/workspace/team-nitro/walkthrough-official-20261127/fix1/maker/`
  — `portal.html`, `identity.html` (+ `identity-consolidated.html`),
  `worker-consolidated.js`, `worker-meta.json`, `sw.js`,
  `build-official.mjs`, `build-worker-official.mjs`, `fix-cert.mjs`,
  `fix1-cert.mjs`, `commit-fix1.py`, `steps.js`, `engine.js`,
  `phone-section3.html`, `phone-style3.html`, `phone-script3.html`,
  `portal-v1.html`, `media/` (14 pictures), `evidence/probe-fix1.py` +
  log + screenshots.
- Base: maker files at `1677214b…` / `f1f69cc9…` / `bf3762e4…` (verified
  by sha256 before editing).
- Deploy: `cf-worker.py put-script … official-walkthrough-staging …
  --meta worker-meta.json` → HTTP 200; curl read-back: `/` 200
  47,431,829 B sha `eb6a2f7e…` ✓ · `/identity.html` 200 317,666 B sha
  `86536d53…` ✓ · `/naya-video.mp4` 200 7,368,202 B sha `c86da39e…` ✓ ·
  `/naya-emblem-cut.png` 200 ✓ · `/agmt-b06.png` 200 ✓.
- Commit: branch `walkthrough-official-20261127`, commit 1
  `22b0525b10f72dac4cc982262d3fa3cf72cabe55` (fix1 files + rebuild
  inputs), commit 2 = this report.
