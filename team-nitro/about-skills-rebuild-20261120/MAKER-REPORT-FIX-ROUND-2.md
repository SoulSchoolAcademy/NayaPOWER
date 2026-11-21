# MAKER REPORT — About + Skills FIX ROUND 2 2026-11-21

**Maker:** About + Skills FIX round-2 maker (Team Nitro, overnight)
**Brief:** fix-round-2 task from the parent orchestrator — one line, then prove it.
**Authority:** Shawn Vibert's order on call `00b25792` (2026-11-20 ~23:00 MST) —
"rebuild it to match exactly, same frames, fit like a glove" — plus the
independent checker's GOES BACK verdict on the fix round
(`CHECKER-REPORT-FIX-ROUND.md`): exactly ONE hard fail, beat 14 phone
horizontal fit. Everything else passed and was not re-opened.
**Base:** branch `about-skills-rebuild-20261120`, base tip
`0132c6899e8518b335396945bbee332bc6e40020` (fix-round tip), page blob
`84fa8873f0bfac20d7eb8e865d813a1a5b1c0c8b`, 201,998 B, sha256
`a917cc337baa85b98cf24424185374870e358fc5a196de144ac341df66766ea5`.
Step 0 reproduced the base byte-identically before any edit: `node
build-about-skills.cjs` on the unmodified build script returned the same
sha256 `a917cc33…`. The fix was made in the build script (the source of
truth), never by hand-editing the page.
**Scope:** one CSS line + re-measure. No merge, no live deploy, no message
to Shawn.

## Activation

Read before any work, in order: `THE-NAYA-DESIGN-LAWS.md` (in full),
`THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`. Also named, per the
brief: `THE-ULTIMATE-ORIENTATION.md`, `THE-SET-ORIENTATION.md`,
`THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-ARMY-TRAINING.md`,
`THE-OFFICIAL-PARTS.md`.

## Filing

- **Commit:** `948dab092c69b31d35adff5c89df53b63d9975b7` (parent `0132c689…`,
  branch `about-skills-rebuild-20261120`)
- **Page:** `team-nitro/about-skills-rebuild-20261120/about-skills.html` —
  blob `33e0f288bcb1b340180e22a22cb683ec817d9b62`, **202,297 B**,
  sha256 `1096d36c0c123388b541df0bb807495812eb30d781f1a4e7b0aab58db4078313`
- **Build script filed with it:** `build-about-skills.cjs` — blob
  `ce881bf1555807662a16cd0b5bb1f172ab0bf626` (44,739 B). Rebuild is
  deterministic: two consecutive runs produce the same sha256.
- **Verified:** blob read back via the git blob API — size 202,297, sha256
  matches. Staged proof-host link returns HTTP 200, 202,297 bytes,
  sha256 matches the built file byte for byte (`cmp` clean).
- **Staged link:**
  `https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/about-skills-rebuild-20261120/about-skills.html&ref=about-skills-rebuild-20261120&cb=33e0f288bcb1b340180e22a22cb683ec817d9b62`
- This report is filed separately after the page (its text names the commit
  above); filing script `file-report-fix-round2.cjs`.

## What changed — one line

Diff vs the fix-round page (`about-skills-fixround1.html`, kept in this dir
as the pre-fix copy): **exactly 2 lines** — one comment line added, one rule
changed. Nothing else in the 202,297-byte file moved.

```diff
-.about-jump{margin:8px auto 0!important;padding-top:6px!important;padding-bottom:6px!important}
+/* FIX ROUND 2 2026-11-21 (checker GOES BACK) — the beat-14 Enter pill is an anchor, which computes box-sizing:content-box, so width:100% + 30px side padding + border = 374px in a 310px frame (overX 64 on phone). border-box makes it 310, like the beat-9 button. */
+.about-jump{box-sizing:border-box!important;margin:8px auto 0!important;padding-top:6px!important;padding-bottom:6px!important}
```

In the build script (`build-about-skills.cjs`, ADD_CSS, line ~398) — the same
one rule, in the additions block. The first attempt at the comment broke the
build: it contained an apostrophe (`beat 14's`), which terminates the
single-quoted JS string (`SyntaxError: Unexpected identifier 's'`). The
comment was rewritten without apostrophes; the build then ran clean and
deterministic. The failed build wrote nothing — the page file was untouched
until the good build (verified: the diff above is the only change).

Why this line fixes it (checker's mechanism, confirmed in my render): the
beat-14 link is an `<a class="p3-enter letter-next about-jump">` computing
`box-sizing: content-box`, so `width:100%` + 30 px side padding + 2 px
border = 374 px in a 310 px frame. Beat 9's identical-classes control is a
`<button>` (UA `border-box`, 310 px) and fits. With `border-box` on
`.about-jump`, the link now computes `width: 310px`, `offsetWidth: 310`,
right edge x=350 = the frame's right edge x=350. The rule also covers the
two skills-view "Back to About" buttons (both `<button>`, already
border-box) — no change in behaviour there.

## The fail, fixed — beat 14 phone horizontal fit

Measured in my own render (local HTTP server, Chromium via Playwright
through the localhost proxy forwarder; real fonts — see the font proof
below). Every beat's `.frame-scroll`, by real "Keep reading" clicks through
beats 1→14, at 390×844 and 1920×1080. `over` = scrollHeight − clientHeight
(vertical); `overX` = scrollWidth − clientWidth (horizontal).

**Beat 14 phone: overX = 0** (was 64). `.frame-scroll` clientWidth 310,
scrollWidth 310. The "Enter NayaNET ◆" pill is whole in the fresh
screenshot (`fix3-phone-b14.png`): rounded right corner visible inside the
gold frame rim, purple rim intact, text fully readable.

## Full fit table — both axes, both widths, real fonts

### Phone 390×844

| beat | over | overX | ch | sh | cw | sw | slack | rows |
|-----:|-----:|------:|---:|---:|---:|---:|------:|-----:|
| 1 | 0 | 0 | 509 | 509 | 310 | 310 | 21 | 4 |
| 2 | 0 | 0 | 509 | 509 | 310 | 310 | 80 | 4 |
| 3 | 0 | 0 | 509 | 509 | 310 | 310 | 54 | 4 |
| 4 | 0 | 0 | 509 | 509 | 310 | 310 | 80 | 4 |
| 5 | 0 | 0 | 449 | 449 | 310 | 310 | 20 | 4 |
| 6 | 0 | 0 | 509 | 509 | 310 | 310 | 80 | 4 |
| 7 | 0 | 0 | 509 | 509 | 310 | 310 | 80 | 4 |
| 8 | 0 | 0 | 539 | 539 | 310 | 310 | 110 | 4 |
| 9 | 0 | 0 | 509 | 509 | 310 | 310 | 65 | 4 |
| 10 | 0 | 0 | 539 | 539 | 310 | 310 | 110 | 4 |
| 11 | 0 | 0 | 479 | 479 | 310 | 310 | 50 | 4 |
| 12 | 0 | 0 | 539 | 539 | 310 | 310 | 87 | 4 |
| 13 | 0 | 0 | 509 | 509 | 310 | 310 | 57 | 4 |
| 14 | 0 | 0 | 509 | 509 | 310 | 310 | 37 | 4 |

Beats 1–13 phone overX = 0 unchanged (the fix moved nothing else). Slack
reproduces the checker's real-font table beat for beat (21/80/54/80/20/80/
80/110/65/110/50/87/57/37) — an independent cross-check that the render
conditions match. 0 `pageerror` on this width.

### Desktop 1920×1080

| beat | over | overX | ch | sh | cw | sw | slack | rows |
|-----:|-----:|------:|---:|---:|---:|---:|------:|-----:|
| 1 | 0 | 0 | 686 | 686 | 888 | 888 | 330 | 4 |
| 2 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 3 | 0 | 0 | 686 | 686 | 888 | 888 | 403 | 4 |
| 4 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 5 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 6 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 7 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 8 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 9 | 0 | 0 | 686 | 686 | 888 | 888 | 204 | 4 |
| 10 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 11 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 12 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 13 | 0 | 0 | 686 | 686 | 888 | 888 | 242 | 4 |
| 14 | 0 | 0 | 686 | 686 | 888 | 888 | 198 | 4 |

Desktop beat 14: the Enter link is 888 px wide, right edge x=1404 = the
frame's right edge — whole (`fix3-desktop-b14.png`). Slack again reproduces
the checker's table exactly (330/242/403/242/…/204/…/198). 0 `pageerror`.

**Result: over = 0 and overX = 0 on all 14 beats at both widths. No inner
scroll anywhere, either axis.** Raw data: `fit-round2.json` in this dir;
measurement script: `measure-fit-round2.py`.

## Font proof — the numbers are real, not vacuous

The round-1 maker's woff2 install does not render in Chromium/FreeType
(checker's finding). I used the checker's TTF install
(`~/.local/share/fonts/ttf-real/` — Marcellus-Regular.ttf + Outfit.ttf),
and proved the real font renders before trusting any fit number:

- Test string "About Shawn Vibert" at 25 px: **Marcellus 226 px** —
  exactly the checker's real-Marcellus value — vs generic serif 205 px at
  the same size. Different widths at the same size = the real font is
  rendering, not the fallback. `document.fonts.check('25px Marcellus')` =
  `true`.
- Outfit at 17 px: 152 px vs generic sans-serif 150 px;
  `document.fonts.check('17px Outfit')` = `true`.
- The one console error on both widths is the Google Fonts CSS cert error
  (`net::ERR_CERT_AUTHORITY_INVALID`) — the VM proxy artifact, not a page
  defect; on a real device the fonts load. 0 `pageerror` on both widths.

## Screenshots read as a reader

- `fix3-phone-b14.png` — beat 14 phone: the Enter pill whole, rounded
  right corner inside the rim; Back + Keep reading below it; the four rows,
  the seal, the showcase strip all in place. This is the screenshot the
  checker asked for, and the cut is gone.
- `fix3-phone-b1.png` — beat 1 phone: whole, three foot buttons in one row
  with breathing room, media board, seal proportionate.
- `fix3-desktop-b14.png` — beat 14 desktop: whole, Enter pill full width
  with both rounded corners visible. The desktop mid-frame gap (198 px
  slack on beat 14) is still there — **untouched, as briefed**: it is owed
  polish for the captain's ruling, not mine to redesign.

## Design-law check — §11 in writing

Checker: `python3 check-design-laws.py about-skills-rebuild-20261120/about-skills.html`
→ **PASS — no machine-checkable violation (2 warning(s))**, the same two as
round 1 and the checker, both pass by eye:
- Line 223: `.deck-next` uses `var(--tone)` — §2.2 check by eye. Pass:
  the tone is the per-beat deep color for the button light, frame edge,
  portrait ring and jewel; the screenshots show white button text with a
  colored glow, legible on every beat.
- Line 240: `.deal-seal-mark` has `color:transparent` with
  `background-clip:text` over a gold conic gradient — §2.2 check by eye.
  Pass: the gold 'N' seal is visible and legible in every screenshot
  (phone + desktop).

**Five gates** (before filing): (1) Is it right? — a one-line fix of a real
defect, nothing else changed, no harm to anyone it touches. (2) Is it what
they truly need? — the cut pill sat on the last beat Shawn will read; the
page now reads whole. (3) Is it mine to do? — briefed FIX maker seat, same
branch and file only; no merge, no live deploy, no message to Shawn.
(4) Is now the time? — overnight round, in time for his morning eye.
(5) Can I prove it? — full fit table both axes both widths with real
fonts, fresh screenshots, design-law PASS, blob read-back, staged link
byte-identical. All five yes.

**Design-check questions:** Could I pick this up? — the boards, pills,
seal and jewel read as real objects with volume, top-left light, real
shadow; the beat-14 pill now reads whole, like beat 9's button. Where is
the light from? — top-left throughout, except the known harvested
`.p3-enter` shine tension (below). What is it made of? — board black
inside, white object in the middle, own-color light outside; no glow
inside. Any gray text? — none seen. Any text under 17? — none in the beats
measured (17 px body). Two same colors together? — the per-beat tone flows
without repeats in a row. Which reference object? — the Smart Note board
(the board and the black) and the top-left + (the button), harvested
verbatim.

**Sense check on the PAGE (not the diff):** the page as Shawn will see it
reads whole — no frame scrolls either way, no button clipped, no row cut,
the seal and the showcase in proportion, the prophecy intact, the skills
teaser one tap from the slideshow. The one thing below the bar is named,
not hidden: the desktop mid-frame whitespace (198–403 px), owed for the
captain's ruling.

**Scorecard:** why is it not a 10 — the desktop whitespace, and the
tightest phone slack, 20 px on beat 5 (37 px margin-aware on beat 14).
What would make it a 10 — his eye on the staged link in the morning, the
captain's ruling on the desktop gap, and his portrait decision, which only
he can give.

**Known open tension (carried over, not mine to resolve by redesign):**
the harvested `.p3-enter` 180°/105° shines vs Design Laws §4 (135° /
top-left light). Kept harvest-verbatim; for the captain's ruling.

## What was NOT changed and why

- **Desktop showcase sizing** — untouched. The desktop mid-frame gap is
  this round's own showcase shrink, per the checker — owed polish for the
  captain's ruling, not a fix-round redesign. Left exactly as is.
- **Portrait, rows, header, skills, and everything else** — untouched.
  The diff is 2 lines in the additions block and nothing else.
- **Personal (`personal-complete.html`)** — untouched. Standalone page only.
- **Monogram variant branch** — untouched.
- **`about-skills-FROZEN.html`** — untouched.
- **Harvested frame system** — not redesigned, including its gradients and
  the `.p3-enter` shine angles (tension noted above for the captain).

## What is still owed

- **Shawn's portrait decision** (Naya's face / his photo / monogram) — his,
  still owed. The page uses the agreement's faces verbatim until he decides.
- **Shawn's eye in the morning** — the final gate. The staged link above is
  for the captain to put in front of him.
- **Captain's ruling on the desktop mid-frame gap** (198–403 px empty
  black) — the checker proved the source does not behave the same way, so
  "harvested, pre-existing" does not cover it as written. Named, not
  redesigned here.
- **3 skill proof links** (from the prior round, still owed): Meet — no live
  room; Match — staging-proven 9/10, no public proof link; Access —
  membership fix-8 eye passed on staging, no public proof link.
- **Membership** gets the same treatment starting tomorrow — not started here.
- **Hub date spin + big white line** in the Hub's main area — flagged to
  the parent from call `3e29f68e`; not in this round.

## Records

Build script (source of truth — the page is never hand-edited):
`build-about-skills.cjs`. Filing scripts: `file-about-skills-fix-round2.cjs`
(page + build script, commit `948dab09…`), `file-report-fix-round2.cjs`
(this report). Measurement: `measure-fit-round2.py`, raw data
`fit-round2.json`. Screenshots: `fix3-phone-b1/b14.png`,
`fix3-desktop-b1/b14.png` (real-font renders). Pre-fix copy for the diff:
`about-skills-fixround1.html` (sha256 `a917cc33…`, the fix-round page).
Prior-round screenshots `fix2-phone-*.png` / `fix2-desktop-*.png` are the
superseded fix-round renders; `check-phone-b14.png` is the checker's
evidence of the cut pill this round fixed.
