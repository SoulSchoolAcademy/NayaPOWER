# MAKER REPORT — About + Skills FIX ROUND 2026-11-21

**Maker:** About + Skills FIX round maker (Team Nitro, overnight)
**Brief:** `BRIEF-FIX-ROUND-20261121.md` in this records dir
**Authority:** Shawn Vibert's order on call `00b25792` (2026-11-20 ~23:00 MST) —
"rebuild it to match exactly, same frames, fit like a glove" — run overnight,
link to Shawn in the morning through the captain. Also: "It should look just
like the other pages. Just like the other frames, like not something new. Stop
making new. Just make it the same." "One language." "Same family."
**Base:** branch `about-skills-rebuild-20261120`, base tip
`ca0ec41e95fd65701f4165bff95b858ab322bae3` (coordinator-verified; Step 0
reproduced the filed blob exactly before any edit — 201,793 B, sha256
`8749d432fcf26ce8af084f56ff962bf200392c800d9c17cfc0024c57d050885c`).
**Scope:** standalone page only. No merge, no live deploy, no message to Shawn.

## Filing

- **Commit:** `36be619afe279ba1c3907c2c5ee3fe9903e93a5c` (parent `ca0ec41e…`,
  branch `about-skills-rebuild-20261120`)
- **Page:** `team-nitro/about-skills-rebuild-20261120/about-skills.html` —
  blob `84fa8873f0bfac20d7eb8e865d813a1a5b1c0c8b`, **201,998 B**,
  sha256 `a917cc337baa85b98cf24424185374870e358fc5a196de144ac341df66766ea5`
- **Build script filed with it:** `build-about-skills.cjs` — blob
  `499f4de9447c93a1ff522e988c1b93e7f44a6f9a` (44,439 B). Rebuild is
  deterministic: two consecutive runs produce the same sha256.
- **Verified:** blob read back via the git blob API — size 201,998, sha256
  matches. Staged proof-host link returns HTTP 200, 201,998 bytes,
  sha256 matches the built file byte for byte.
- **Staged link:**
  `https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/about-skills-rebuild-20261120/about-skills.html&ref=about-skills-rebuild-20261120&cb=84fa8873f0bfac20d7eb8e865d813a1a5b1c0c8b`
- This report is filed separately after the page (its text names the commit
  above); filing script `file-report-fix.cjs`.

## Verdicts — the checker's five GOES BACK items

### 1. Every About frame fits whole, no inner scroll, at 390×844 AND 1920×1080 — PASS

Measured in my own render (local HTTP server, Chromium via Playwright with
the localhost proxy forwarder; real Google fonts installed locally — see the
font note below). Every beat's `.frame-scroll` scrollHeight vs clientHeight,
plus the real content slack (clientHeight minus the summed rendered children,
an upper bound on content, so the slack shown is the minimum):

**Phone 390×844** — over 0 on all 14 beats:

| beat | over | content slack | topbar | foot |
|-----:|-----:|--------------:|-------:|-----:|
| 1 | 0 | 11 px | 89 | 105 |
| 2 | 0 | 61 px | 89 | 105 |
| 3 | 0 | 77 px | 59 | 105 |
| 4 | 0 | 61 px | 89 | 105 |
| 5 | 0 | 31 px | 119 | 105 |
| 6 | 0 | 61 px | 89 | 105 |
| 7 | 0 | 61 px | 89 | 105 |
| 8 | 0 | 91 px | 59 | 105 |
| 9 | 0 | 39 px | 89 | 105 |
| 10 | 0 | 91 px | 59 | 105 |
| 11 | 0 | 31 px | 119 | 105 |
| 12 | 0 | 91 px | 59 | 105 |
| 13 | 0 | 91 px | 59 | 105 |
| 14 | 0 | 10 px | 89 | 105 |

**Desktop 1920×1080** — over 0 on all 14 beats; content slack 161–386 px
(beat 1: 310 px; beat 14: 161 px; most beats: 213 px).

How it was done — all levers inside the one additions block
(`<style id="aboutSkillsAdditions">`, built-file line 605), all re-sizes and
re-flows, nothing harvested redesigned:
- Copy shortened: every nutshell ~2 lines (≤ ~60 chars), every row's label +
  " — " + text ≤ 54 chars. All facts kept, in his voice. Beat 3 keeps all
  five words and the full prophecy quote verbatim; beat 11 keeps the date
  "20 November 2026"; beat 12 keeps "Auto-Match 9 of 10, on staging".
- Row label inline (`display:inline`), rows 17 px / line-height 1.3,
  gap 2 px; nutshell slimmed (padding 8/12/2, phone 17 px body).
- Showcase re-sized to a strip, centred: 80 px tall on phone, 200 px on
  desktop. Beats 1 and 3 carry no still picture (beat 1 carries the media
  board, beat 3 the prophecy — as the agreement's text-only beats carry no
  picture).
- Foot buttons in ONE row on phone: each button sizes to its own label
  (`width:auto`, tight padding), so all three fit the row. The seal stays.
- Seal 56 → 40 px on phone only (prior rounds shrank it 120 → 84 → 72 →
  56 for fit); beat padding 10/8 → 4/4; foot-line margin 18 → 8 on phone;
  beat-1 media board slimmed (paddings, video pill, title margin).

Two mistakes found by measurement and fixed in the round (named honestly):
- The one-row foot was first written for "two buttons, not three" — wrong:
  the deck's JS creates a Back button at runtime, so the foot holds THREE
  (Back / Keep reading / Next). The first one-row attempt also clipped the
  third button (row 366 px in a 310 px foot). Fixed with `width:auto` +
  tight padding; verified by button rects on every beat — all three buttons
  in bounds and visible (beat 14 correctly has two: Back + Keep reading,
  no Next). The stale comment was corrected in the same pass.
- The seal shrink first failed to apply: the harvested rule is
  `.frame-foot .frame-red-n` (specificity 0,2,0), which beat my
  `.frame-red-n` (0,1,0). Fixed by matching the selector; verified by
  computed style (seal 40 px, mark 22 px on phone).

### 2. Beats 9, 12, 13 carry the four smart-note rows — PASS

All 14 beats carry all four rows — verified two ways: the built file holds
exactly 14 of each label (WHY IT MATTERS / HOW TO APPLY IT / HOW IT
CONNECTS / WHAT'S IN IT FOR YOU), and the browser check on every beat
returns `rows: 4, labelsOk: true` for beats 1–14, including 9, 12, 13.
Their topical content moved into the nutshell paragraph (beat 9: "The Login,
the Notes, the Numbers."; beat 12: the three proofs; beat 13: the four
destinations). No beat needed the stop-and-report exemption — the rows fit
on every beat with the slack in the table above.

### 3. Header comment rewritten to describe what is actually filed — PASS

Built-file lines 8–37. It names the VERIFIED harvest source
`agreement-unfold-fix-20261117/agreement-unfold-fixed.html` (blob
`1f0b04747e3315be6f1b619c1411e5e14fbdc1bb`, 142,532 B). The fix-5 citation
is dropped entirely — `fix-5` count in the built file: 0 (the brief-named
source `walkthrough/agreement-distill-fix5-20261119/welcome-staged.html`
and tip `86f52570` could not be located; never cite what cannot be
verified). The monogram claim is gone — `monogram` count: 0. The header
states no Shawn portrait exists in either harvested source, the agreement's
faces are used verbatim, Shawn's portrait decision is his and still owed,
and no generated face is anywhere in the page.

### 4. Portrait: DO NOT CHANGE IT — PASS (unchanged)

Naya's faces, verbatim from the agreement. The topbar face already cycled
per beat; the beat photos now cycle too (see item 5). No portrait of Shawn
was added, no face generated, no monogram. Shawn's portrait decision
(Naya's face / his photo / monogram) is his and still owed.

### 5. Cleanups — PASS

- Dead CSS `article[data-beat="37"]` removed: `data-beat="37"` count in the
  built file: 0. (Harvested history comments mentioning "37" — e.g. "N / 37"
  — were left: they describe the harvested system, not this page.)
- Dead JS fallbacks `'The Collective Agreement'` removed from `headFor`
  (built-file lines 1339–1340 now read `'About Shawn Vibert'`). The string
  occurs once in the whole file, line 37, inside the header comment
  describing the removal — a truthful description, not live code.
- Beat photos cycle per the agreement (faces 1,3,4,5,6,7,8,9 repeating):
  beats 1–8 = face-1,3,4,5,6,7,8,9; beats 9–14 = face-1,3,4,5,6,7 —
  verified in the browser by the blocktop `<img>` src on every beat.

## Smoke test — PASS, 0 page errors

Phone 390×844 and desktop 1920×1080, Chromium via Playwright:
title "About Shawn Vibert — NayaNET"; pill "◆1 / 14"; Next advances to
beat 2, pill "◆2 / 14"; all 14 beats' foot buttons in bounds and visible;
"See all my skills" opens the Skills slideshow (deck hidden); Skills Next
reveals slide 2 cumulatively (slide 1 still visible); read-all shows all 14
slides and the sign; "Back to About" restores beat 9; `?view=skills` deep
link opens the slideshow. 0 `pageerror` on both widths.
One console error repeats on both widths: Google Fonts CSS fails with
`net::ERR_CERT_AUTHORITY_INVALID` — the VM Chromium does not trust the
egress proxy's certificate for fonts.googleapis.com. It is a VM artifact,
not a page defect: the page falls back to system fonts in the VM, and on a
real device the fonts load. I proved it harmless by installing the real
Marcellus + Outfit files locally and re-measuring: every fit number came
out identical (Marcellus measures the same as the fallback serif for the
titles; Outfit is narrower than the fallback sans, so buttons only gain
room). Screenshots in this dir (`fix2-phone-b1/b3/b5/b9/b14.png`,
`fix2-desktop-b1/b3/b5/b9/b14.png`) are the real-font renders.

## Screenshots read as a reader

Phone beats 1, 3, 5, 9, 14 and desktop beats 1, 3, 5, 9, 14 read as a
reader: every frame fits whole, nothing clipped, nothing cramped; the three
foot buttons sit in one row with breathing room; the 40 px seal reads as
the same seal, proportionate; the 80 px showcase strips read as pictures,
not slivers; beat 3's prophecy quote is whole and verbatim; beat 9's teaser
carries the four rows and the "See all my skills" button; beat 14's "Enter
NayaNET ◆" link sits above the seal with Back + Keep reading below it.
Desktop: the frames fit, but the middle of each frame is empty black space
(content ~377–526 px in a 687 px window, foot pinned at the bottom) — that
is the harvested frame's own desktop layout (the agreement's frames behave
the same way), pre-existing, not introduced by this round; named here, not
redesigned.

## Design-law check — §11 in writing

Checker: `python3 check-design-laws.py about-skills-rebuild-20261120/about-skills.html`
→ **PASS — no machine-checkable violation (2 warnings)**. Both warnings are
§2.2 "check by eye" on harvested rules, both pass by eye:
- Line 223: `.deck-next` uses `var(--tone)` — the per-beat deep color for
  the button light, frame edge, portrait ring and jewel. Not gray text; the
  screenshots show white text with a colored glow, legible on every beat.
- Line 240: `.deal-seal-mark` has `color:transparent` — with
  `background-clip:text` over a gold conic gradient (the standard
  gradient-text technique). The gold 'N' is visible and legible in every
  screenshot.

**Five gates** (before every consequential action in this round): (1) Is it
right? — serves Shawn's order, same frames, no new design, nothing removed
he didn't ask to remove. (2) Is it what they truly need? — frames that fit
and the four rows on every beat, so the page reads whole on his phone.
(3) Is it mine to do? — briefed maker seat, standalone page only; Personal,
the monogram branch and the FROZEN file untouched. (4) Is now the time? —
overnight round, in time for his morning eye. (5) Can I prove it? — fit
numbers for all 14 beats at both widths, smoke test, screenshots read as a
reader, blob read-back, staged link byte-identical. All five yes.

**Design-check questions:** Is every position calculated? — yes: fit
measured per beat with real slack (10–91 px phone, 161–386 px desktop).
Does it feel like a machine? — yes: the harvested frame system, the same
topbar, seal, buttons and board on every beat. Can you get it in 2 seconds?
— yes: a 2-line nutshell and four 2-line rows, one screen per beat.

**Sense check on the PAGE (not the diff):** the page as Shawn will see it
reads whole — no frame scrolls, no button clipped, no row cut, the seal and
the showcase in proportion, the prophecy intact, the skills teaser one tap
from the slideshow. The two things below the bar are named, not hidden:
desktop mid-frame whitespace (harvested, pre-existing) and the tightest
phone slack, 10 px on beat 14.

**Scorecard:** why is it not a 10 — the desktop whitespace (harvested, not
mine to redesign) and 10 px slack on beat 14. What would make it a 10 —
his eye on the staged link in the morning, and his portrait decision, which
only he can give.

**Known open tension (from the brief, not mine to resolve by redesign):**
the harvested `.p3-enter` 180°/105° shines vs Design Laws §4 (135° /
top-left light). Kept harvest-verbatim; for the captain's ruling.

## What was NOT changed and why

- **Personal (`personal-complete.html`)** — untouched. Standalone page only.
- **Monogram variant branch** (`personal/about-skills-rebuild-20261120`,
  blob `c97a2ee0`) — untouched.
- **`about-skills-FROZEN.html`** (198,343 B) — untouched.
- **Skills slideshow** — untouched except where the fix required it
  (nothing in the slideshow needed changing; the beat-9 jump button's
  padding slimmed as part of the global jump-button rule).
- **Portrait** — unchanged (see item 4).
- **Harvested frame system** — not redesigned, including its gradients and
  the `.p3-enter` shine angles (tension noted above for the captain).
- **Copy facts** — nothing invented: no scores, results, credentials or
  testimonials added. Beat 12 keeps the honest "Auto-Match 9 of 10, on
  staging" qualifier.

## What is still owed

- **Shawn's portrait decision** (Naya's face / his photo / monogram) — his,
  still owed. The page uses the agreement's faces verbatim until he decides.
- **Shawn's eye in the morning** — the final gate. The staged link above is
  for the captain to put in front of him.
- **3 skill proof links** (from the prior round, still owed): Meet — no live
  room; Match — staging-proven 9/10, no public proof link; Access —
  membership fix-8 eye passed on staging, no public proof link.
- **Membership** gets the same treatment starting tomorrow — not started here.
- **Hub date spin + big white line** in the Hub's main area — flagged to
  the parent from call `3e29f68e`; not in this round.

## Records

Build script (source of truth — the page is never hand-edited):
`build-about-skills.cjs`. Filing scripts: `file-about-skills-fix.cjs`
(page + build script, commit `36be619a…`), `file-report-fix.cjs` (this
report). Screenshots: `fix2-phone-b1/b3/b5/b9/b14.png`,
`fix2-desktop-b1/b3/b5/b9/b14.png` (real-font renders). Prior-round
screenshots `fix-phone-*.png` / `fix-desktop-*.png` are the superseded
round-1 renders.
