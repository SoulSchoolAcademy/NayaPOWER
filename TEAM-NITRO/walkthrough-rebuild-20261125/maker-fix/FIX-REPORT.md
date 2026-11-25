# FIX REPORT — Walkthrough Rebuild FIX 2026-11-25 (checker GOES BACK → fix)

**Lane:** `~/workspace/team-nitro/walkthrough-rebuild-20261125/maker-fix/`
**Role:** fix round. **Nothing goes live from this round. Nothing to Shawn from me.**
**Fixes:** checker verdict `checker/CHECKER-VERDICT.md` (GOES BACK — D1 + observations O1/O2/O5).
**Read first (done):** `THE-NAYA-DESIGN-LAWS.md` (full), `THE-PLAYBOOK.md`,
`DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`,
`THE-HEART-OF-THE-MACHINE.md`, `THE-ULTIMATE-ORIENTATION.md`,
`~/workspace/team-nitro/AGENTS.md` (Checklist Law, Whole-Page Rule, Continuous
Cycle Law, One-Build Law, Eleven Laws). No law-vs-brief conflict required a
stop. No image was swapped in this round (second-batch HOLD — see §6).

## 1. What was fixed

### D1 — Q1 and Q11 lose their second image at phone width (THE GATE)
**Before (code-proven by the checker, confirmed by my own render):** the RB
media query `@media (max-width:900px){ .rb-cell-r{display:none!important} }`
hid the right cell, so at 390px Q1 showed only the painting woman and Q11
only the giant diamond. My own pre-fix render also proved a second, wider
failure the checker could not see (no browser): at **desktop 1280 the side
images collapsed to 4px slivers** — the spine caps `.p3-main` at 640px, so
thirds `1fr minmax(0,560px) 1fr` left the side tracks ~14px. The thirds as
built could not render at desktop inside that column.

**Fix (in `rb.css` + `rb.js`, nothing else touched):**
- The frame now carries `.rb-two` (two-image steps) or `.rb-one`
  (one-image steps). At ≤1100px the layout stacks, and two-image steps show
  BOTH images as a **two-up mini row above the centred input**
  (`.rb-two{grid-template-columns:1fr 1fr}`, right cell `display:flex`,
  images 200px tall); single-image steps still hide the mirrored right cell.
  The stack runs to 1100px, not 900px, because 901–1100px has the same
  640px-main squeeze as the phone widths.
- Above 1100px, steps carrying a thirds frame widen their main column
  (`.p3-step:has(.rb-thirds)>.p3-main{max-width:none!important}`), so the
  thirds render as designed (560px centre, real side images). Scoped with
  `:has(.rb-thirds)` — the door and end steps keep their own widths, and the
  Next pill, cert (680 cap) and choices (680 cap) inside main are untouched
  except for the wider line-box they already fill.

**After — my own renders + geometry (Playwright Chromium, real proof-host
image URLs, 0 page/console errors in every run):**

| View | Q1 motto | Q11 offer |
|---|---|---|
| 390×844 | painting woman 148×204 + crown 148×204, side by side, y 230–434 in viewport, both `complete`, natural 768×1364/1365 | giant diamond 148×204 + crystal compass 148×204, same geometry |
| 1024×800 | both 289×204, in viewport at scroll 0 | both 289×204, in viewport at scroll 0 |
| 1280×900 | painting woman 167×424 + crown 167×424, frame columns `163px 560px 163px`, in viewport | diamond 167×532 + compass 167×532, same columns |

Eye proof (read by my own eye): `proof/final-390-q1.png` (woman + crown),
`proof/final-390-q11.png` (diamond + compass),
`proof/final-1280-q1.png` (both portraits flanking the centred input),
`proof/dbg390b-noframe.png` (the pair with the fixed frame hidden).
Honest note on the 390 scroll-0 view: the spine's per-step certificate
header occupies the first viewport, so at scroll 0 the pair's top edge sits
just below the fold (frame top y=735; question at y=656) — one short scroll
brings the pair fully into view, no tap. The fixed ornate frame overlays
(z-60) also cover content scrolled hard to the very top; the pair is shown
fully below it. Both are spine behaviours, not this layer's, and out of
this round's scope to redesign.

### O2 — 0-byte `offer.webp` leftover
`maker/img/offer.webp` (0 bytes) deleted from `maker/img/` and never copied
into `maker-fix/img/`. It was referenced nowhere (no manifest, build, or
walk reference). The unused alternates `motto.webp` / `declaration.webp` /
`laws.webp` were left alone — not in this round's scope.

### O1 — end board "Your profile is ready." repetition
It DID read as a repeat on the rendered page (heading + body opening with
the same line). Fixed: the heading stays "Your profile is ready." and the
body is now distinct plain words carrying the universal-creator line (see
§5): "Your profile is yours to make your own — change any image, add text
or video, pull from social or our library, add more boards. Your answers
are saved in your Smart Vault, and your Personal page is built from them."
Build assertion holds: the exact string "Your profile is ready." occurs
exactly 1× in the built file.

### O5 — about-extra-1..5 reserved slots now in the walk's CODE
`window.__RB_ABOUT_EXTRA = ['about-extra-1', …, 'about-extra-5']` is
declared in the walk's data script and read by `rb.js`
(`window.__rbAboutExtra`), with a comment stating the slotting rule: file
`img/about-extra-<n>.webp`, add its key to a step's `imgs[]`, no frame
rebuild. All five slot strings are present in the staged bytes (grep:
about-extra-1 ×2, -2..-5 ×1 each). `MANIFEST.json` gains the structured
field `about_extra_slots` alongside the prose. The About list stays held
open.

## 2. Staged + filed (verified by size + sha)

- **Branch:** `walkthrough-rebuild-20261125` (same branch, new commits).
- **HTML:** `TEAM-NITRO/walkthrough-rebuild-20261125/walkthrough-rebuild.html`
  — **183,927 B, sha256
  `b78a37082dd4b110be879d16a28c50922c7321e12479e6dae4ac96392f087042`**,
  blob `7ffa3d092931e8c2109e9e0052cf916390d1307c`, commit
  `72da5fab548f070b1553985b7db6e6c4126486ef`. Verified by re-download from
  GitHub (decoded 183,927 B, sha matches local exactly).
- **MANIFEST.json:** 7,768 B, blob `401fef1db37480ba16c50668ecc7592cc2abdde4`,
  commit `becba9e27c240c2a0d2659b81df470d107052e86`.
- **This report:** `maker-fix/FIX-REPORT.md`, filed to the same branch
  (blob + commit in `maker-fix/filings/fix-report.json`).
- **Staged link (proof host):**
  `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Fwalkthrough-rebuild-20261125%2Fwalkthrough-rebuild.html&ref=walkthrough-rebuild-20261125&cb=7ffa3d092931e8c2109e9e0052cf916390d1307c`
  — downloaded 183,927 B, sha matches the filed bytes exactly.
- **Staging worker:** `naya-walkthrough-15-staging` (account NayaPOWER
  `b5e2a51b3e883f7722287c5f51b1196b`), `worker-rebuild.js` rebuilt from the
  fixed walk (encoder fidelity + round-trip + non-HTML-bytes identity
  asserted pre-PUT), PUT via `cf-worker.py put-script --no-metadata`
  (existing module worker: format + bindings preserved, nothing re-declared,
  secrets never touched). Bindings re-verified after the PUT: both
  `secret_text` bindings intact (same set as before the PUT).
  Served `/welcome`: **183,927 B, sha `b78a3708…` = the built walk exactly.**
  Live walk: `https://naya-walkthrough-15-staging.nayapower.workers.dev/welcome`
- **Build:** `maker-fix/build-rebuild.mjs` (spine + RB layer, assertions
  incl. D1: no bare `.rb-cell-r{display:none!important}`; all five
  about-extra slots present; end-board count = 1; "yours to make your own"
  present; Audio slot present). `maker-fix/build-worker-rebuild.mjs`
  (WALK_HTML swap, fidelity asserted).

## 3. Design-law check (§11 in writing + checker script)

Ran `check-design-laws.py` on the fixed build: **26 FAILs + 6 WARNs — the
violation set is BYTE-IDENTICAL (same messages, same counts) to the
harvested spine base.** This layer added **zero** new violations, including
for the new CSS (no new text sizes, no new colours) and the new Audio slot
(same obsidian board, same step rim). The 26 pre-existing FAILs are all
SIZE (§2.3 below 17px inside the harvested spine) and the 6 WARNs are the
spine's dimmed text + two `TOPIC_SPECTRUM` colour lines — named plainly,
per §0, a spine follow-on, not this round.

**§11 gates:** (1) Right — serves the citizen building their own page; no
harm. (2) What they truly need — Shawn's order verbatim, his images, his
words; nothing swapped. (3) Mine to do — staging + GitHub filing only;
nothing live, no money, no credentials, no deletions except the 0-byte
leftover file, no test-certificate deletion (walktest1 Nº 885, walkcheck1
Nº 886 untouched). (4) Now — fixed, rendered, filed and staged in the
round. (5) Proven — every number above is a measured byte/sha/render, not
a claim.

## 4. The universal page creator — STANDING FORMAT LAW (recorded, not a scope change)

From Shawn's call (recorded in MEMORY.md 2026-11-25 ~14:1x MST): **the
walkthrough is THE standard for how EVERY page gets created, every time.**
Recorded here as standing format law for this walkthrough:

- **The shape, every time:** palace image in the 9:16 frame, question on
  top, centred input box in the middle, Naya's voice + photo beside it,
  every image/video/text board swappable after (our library or upload your
  own). This build already is that shape on all 15 frames; the fix round
  keeps it (D1 is what makes the two-image frames true to it at phone
  width).
- **The centred input accepts five ways:** type, dictate, PASTE FROM YOUR
  AI, edit the example, or SKIP. **Already present — verified in the
  harvested spine, not added here:** every step carries a
  `.p3-hint[data-act="paste"]` button ("Copy-paste from your AI into the
  box", 15×) wired to `pasteIntoBox()` (clipboard read → appended to the
  box + saved), and a `.p3-skip` button ("Skip this question →", 15×)
  wired to `S.skipped`. Type + dictate + example chips were already
  present. Nothing to add; the five ways are all live in this build.
- **His images sit in as the EXAMPLE, and the walk says so plainly:**
  the end board now reads "Your profile is yours to make your own — …"
  (see §1). The example images are his set, in place while they fill it
  out, swappable after.
- **Membership areas ride the same path later** with audio + video in the
  same frame style (see §5).

## 5. How audio and video slots ride this format

- **Video (already present):** the toolbox `+ Block` menu offers
  Image / Text / Video; video by URL (YouTube embed or direct file) or
  file upload, rendered in the same `.rb-extra` obsidian board with the
  step's rim.
- **Audio (ADDED in this fix, same frame language):** the `+ Block` menu
  now offers **Audio** as a fourth kind. An audio slot is the same
  `.rb-extra` obsidian board, same 2px rim in the step's own colour, same
  shadow, same ✕ to remove — with a native `<audio controls>` element in
  the board (by URL via prompt, or file upload; `preload="metadata"`).
  The play treatment matches the frame's existing play button: the
  frame's play button is Naya's voice reading the question (voice clip or
  speech, true toggle); the audio board plays the citizen's audio in
  place. CSS: `.rb-extra audio{width:100%}` joins the img/video rule.
  Build-asserted (`'Audio'` + `attachAudioUrl` present). Not yet proven by
  tap — that rides the browser-capable interactive check (§7).
- **Follow-on, not built here:** audio/video extra boards persist only
  for text today (localStorage restores text extras; media extras are
  session-only, same as before this round). Persisting an audio/video
  extra across reloads is a follow-on, not a silent omission.

## 6. SECOND BATCH — PENDING, nothing swapped (HOLD)

Shawn sent six more labeled images (2026-11-25 ~14:14 MST), recorded in
`~/workspace/naya-abstract-library/shawns-set-mapping.md` under "Second
batch" and in MEMORY.md. **Nothing in this round swaps any image.** The
build still uses the CONFIRMED 19-image mapping only. The batch, as
pending:

| File | Image | Suggested placement |
|---|---|---|
| `NAYANET_About_US_PAGE_image_15.jpg` (540,735 B, 1152×2048) | Whole family portrait in the palace garden | Vision or Love (suggested) |
| `NAYANET_About_US_PAGE_image_love.png` (2,349,542 B, 1152×2048) | Two hands cupping a glowing crystal heart | Q5 Love — **Shawn's own label** (strongest signal) |
| `NAYANET_About_US_PAGE_image_Misson.jpg` (513,558 B, 1152×2048) | Woman at peace, palace behind | Q4 Mission — **Shawn's own label** (spelling his) |
| `NAYANET_SKILLS__PAGE_image_6.png` (3,885,151 B, 1152×2048) | Everyday woman painting a crystal lotus | Q14 How you work or Q7 Thing (suggested) |
| `NAYANET_SKILLS__PAGE_image_7.jpg` (456,125 B, 1036×1843) | Woman + grandma lighting a glowing crystal lotus | Q12 Help (suggested) |
| `NAYANET_SKILLS_PAGE_image_8.jpg` (453,383 B, 1036×1843) | Two women welcoming a child at the palace gate | Q15 Start (suggested) |

**The fifteen IF the suggestions are confirmed (pending — not live):**
Motto 1+2 unchanged · Vision archway (image_15 held as alternative) ·
Goal lotus unchanged · Mission `Misson.jpg` (replaces sunset path) ·
Love `love.png` (replaces grandma + child) · Don't love broken heart
unchanged · Thing sculpting angel (image_6 held as alternative) · Values
grandma + lotus unchanged · Stand for girl painting palace unchanged ·
Promise bridge unchanged · Offer diamond + compass unchanged · Help terrace
walkway (image_7 held as alternative) · Moment portfolio tablet unchanged ·
How you work designer at screen (image_6 held as alternative) · Start
`image_8` welcoming the child (replaces open doors). If confirmed, images
8, 9 and 10 move to the library as spares and image_15 joins the set; total
set would be 25 images (19 + 6). **The official set is STILL not final
until Shawn says so — nothing swaps until he confirms.**
Dimension note: images 7 and 8 are 1036×1843, not 1152×2048 — still ~9:16
(0.5622 vs 0.5625); do not fail a dimension check on them; upscale or
accept.

## 7. Not done / needed next

1. **Browser-capable interactive checker + captain's eye + Shawn's eye**
   (the checker's D2, still open): real walk-through at 390×844 and 1280
   with a fresh account — taps, typing, toolbox (incl. the new Audio
   slot), play/audio, quick-picks, dictation, end-board Back, Hub landing,
   zero console errors. This round proved the layout by render + geometry
   only; it did not perform the interactive walk.
2. **Second batch** — swaps only on Shawn's confirmation (§6).
3. **Five more About images** — still held open (§1, O5); when they
   arrive, file `img/about-extra-<n>.webp` + add the key to the step's
   `imgs[]`.
4. **Spine small-text FAILs (26)** — pre-existing, named in §3; a spine
   follow-on, not this round.
5. **Q9/Q10 canonical answers** still need re-fitting to the new questions
   ("What do you stand for?" / "What is your promise?").
6. **Live** — only on Shawn's tap, per §15. Nothing in this round went live.

## Proof files (this fix)
- `maker-fix/proof/final-390-q1.png` / `final-390-q11.png` — both pairs at
  true 390×844, read by my own eye
- `maker-fix/proof/final-1280-q1.png` — desktop thirds, read by my own eye
- `maker-fix/proof/dbg390b-noframe.png` — the 390 pair with the fixed frame
  hidden (isolates the pair from the spine's fixed ornament overlay)
- `maker-fix/proof/render-results2.json` — geometry at 390 / 1024 / 1280
- `maker-fix/proof/law-fix3.txt` — design-law checker output (26 FAIL + 6
  WARN, identical to spine)
- `maker-fix/filings/fix-walkthrough-rebuild.json` /
  `fix-manifest.json` / `fix-report.json` — GitHub filing records
