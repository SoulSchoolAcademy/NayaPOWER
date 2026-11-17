# EMBLEM CORNERS FIX — MAKER REPORT (2026-11-17)

**Round:** Emblem Corners Fix — the cloud eye's defects 21:53–21:57Z
(brief `BRIEF-EMBLEM-CORNERS-FIX-20261117.md`).
**Maker:** Naya Nitro Narzan (subagent, depth 2/2). **Records:**
`~/workspace/team-nitro/emblem-corners-fix-20261117/`
**Branch:** `emblem/corners-fix-20261117` (NEW, from
emblem/certificate tip `f23b6202`) — filing receipts in §13.
**Staged:** `https://naya-pricing-free-staging.nayapower.workers.dev/free`
— entry **3,804,043 B, sha256
`a5e529f9d78a279caa2a3999a502645e202ac8d49a3f22651f01fcfb520bf85b`**,
worker sha256
`5bfa072ad0ca53771ae29ed302ee274de359c7e64d2f46a821f1ad6f3a20fd5a`,
`modified_on 2026-11-17T22:35:03Z`.
**Timestamped link (Link Law — verified this URL serves the new
bytes, sha match):**
`https://naya-pricing-free-staging.nayapower.workers.dev/free?t=1794954952`
— re-timestamp at delivery; the captain ledgers it as CURRENT.
**Verdict:** the four corner emblems are DONE and staged — whole in
the first viewport at 1920, whole in the card at 635/390, the black
background die-cut so no square edge reads as a diamond, the silver
surround legible at ship size, the center seal untouched, zero new
design-law FAILs, words unchanged, probe 120/120. The independent
checker + the cloud eye + Shawn's eye are OWED (§7–§8) — nothing
goes to Shawn from this round until the eye passes.

## §0 Laws read first
Before any action, read in full: `THE-NAYA-DESIGN-LAWS.md` (v2.1) +
`THE-NAYA-DESIGN-LAWS.machine.json` + `check-design-laws.py` +
`THE-COMMON-LANGUAGE-REPORT.md` + `THE-PLAYBOOK.md` +
`DESIGN-INTELLIGENCE-REPORT.md` + `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` +
`THE-HEART-OF-THE-MACHINE.md` + `THE-ULTIMATE-ORIENTATION.md` +
`THE-ARMY-TRAINING.md` + `~/workspace/team-nitro/AGENTS.md` (house
rules: checklist law, whole-page rule, continuous cycle, 10-minute
rule). Key law points carried: nothing flat, nothing dead; no gray
text ever; type scale 25/19/17; one deep color per object, never two
same colors adjacent; one light top-left (135°); inside is board
black, no glow inside; everything a real object, alive on hover;
harvest verbatim — take the shown object verbatim, never redraw it.
Emblem law from the brief: the emblem is verbatim, never redrawn;
each corner ON AN ANGLE at the same quality (desktop
−59°/+59°/−121°/+121°, mobile ±35°/±145°).

## §1 The defects (the eye's words, 2026-11-17 21:53–21:57Z, 1920×999)
1. **Clipped corners:** top-left cut at the left edge, top-right at
   the right edge, bottom emblems partly below the fold with the same
   clipping. Cause (measured): the corner slots straddled the frame
   (20px inset + translate ±50%) while `.identity-pro-card` fills the
   screen width with `overflow: hidden` — half of every emblem sat
   outside the card.
2. **The black background reads as a rotated diamond:** the source
   `NAYA_ICON.png` has 0 transparent pixels (RGBA 1800×2000, corner
   pixel pure black opaque) — the square shows its edge when rotated.
3. **The silver surround small/busy/hard to read at desktop size,**
   the tiny teardrop barely legible. The purple diamond gem reads.
4. **The center crystal-N seal is the model and is UNTOUCHED.**

### What did NOT change (judgment calls, stated plainly)
The emblem itself (`NAYA_ICON.png`) is verbatim, never redrawn —
the die-cut (§3 F3) is presentation only, an SVG filter on the
medal, the file untouched. The heading, name, pills, number/date,
ENTER button, agreement note, "USE A DIFFERENT ALIAS" do not change.
The center seal (`.cert-seal .logo-hero`) is untouched. Identity +
unfold stay SEQUENCED — not staged here (collision + worker-size
law, §9). The angles are the page's own, kept byte-identical.

## §2 Base verified cold (before any edit)
- Branch `emblem/certificate-20261117`, tip `f23b6202` (ref GET),
  PR #3440 open, UNMERGED.
- Staged entry 3,801,588 B, sha256 `fbe04202…` (filed == staged);
  worker sha256 `d3d75854…`.
- Tip reproduced byte-exact in memory via the filed build chain
  (`regen_pricing_fix_tip` + `harvest_identity` +
  `apply_certificate` + `apply_fix` + `apply_emblem` → sha
  `fbe04202…`) before any edit. Current staged worker reproduced
  byte-exact before any edit.
- Emblem source verified: `~/workspace/user/media_library/image/NAYA_ICON.png`,
  **2,654,505 B, 1800×2000 PNG, sha256
  `1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4`**.
  Pixel analysis: non-black bounding box x 164–1688, y 44–1920;
  79.2% of pixels pure black; purple gem luminance min 20/255,
  median 67/255; 80.6% of pure-black pixels edge-connected, the rest
  interior gaps in the filigree.
- **Identity moved (observed, not touched):** live staged identity
  sha is now `a1550164…`, not the prior round's `8c641f96…`.
  Another round's doing; the build script's identity guard is
  observe-only, not fail-stop.

## §3 The change (F1–F4 + F4b, each asserted in `build-emblem-corners-fix.py`)
- **F1 Desktop geometry:** corner box 100×122 → **132×161**;
  centers 20px → **112px** from each edge. Rotated bbox at 59°:
  halfW 103.0, halfH 98.0 → clearance 9.0px left/right, 14.0px
  top/bottom inside the card. Emblem renders 132×147 (was 100×111,
  +32%). Angles unchanged (−59°/+59°/−121°/+121°).
- **F2 Mobile geometry:** corner box 54×54 → **64×64**; centers
  15px → **56px**. Rotated bbox at 35°: halfW = halfH = 44.6 →
  clearance 11.4px on every side. Emblem renders 58×64 (was 48×54,
  +20%). Angles unchanged (±35°/±145°). The silver surround and the
  teardrop read at both sizes now (§7 screenshots).
- **F3 Die-cut (presentation-only, file stays verbatim):** inline
  SVG filter `#crestCut` before the first corner div;
  `feColorMatrix` turns luminance into alpha, `feFuncA` linear
  slope 6, intercept −0.15 (pure black → fully transparent; gem
  median luminance 0.26 → fully opaque; anti-aliased edge
  feathers). Applied as `filter: url(#crestCut) drop-shadow(0 6px
  12px rgba(0,0,0,0.60))` on BOTH medal rules (desktop + mobile —
  a plain drop-shadow on mobile would silently undo the cut). A
  stale v2.3 comment claiming a "baked alpha melt" and "no CSS
  mask", and a stale mobile comment about a "diamond-heart
  medallion", were corrected in place.
- **F4 Mobile foot clearance — the rows (found by the maker's own
  live probe, 22:10Z):** at phone widths the foot text runs full
  width down to 34px above the card bottom, so a whole bottom
  emblem would sit ON the foot's last lines. The old emblems
  overlapped the privacy line the same way (only half-clipped, so
  less visible) — a pre-existing overlap made fully visible by
  making the emblems whole. Padding alone cannot buy the clearance:
  the foot is ~370px tall in a ~233px grid row and moves up only
  about half as fast as the padding grows (+48px padding moved the
  foot up 23px, probe-measured) — and past ~179px of padding the
  shrunken top row pushes the head down onto the name input (seen
  live at 280px: the title hid behind the input box). So at ≤640px
  the face's rows become `auto auto 1fr` — the head keeps its own
  row, the name keeps its row, and the foot pins to the top of its
  row (measured: the foot top-aligns; its bottom then sits at a
  fixed 739px in the viewport at 390×844 and does NOT move when
  the card grows). Padding stays at 160px. The certified face
  keeps its own more-specific rows (0.74fr auto 1.26fr, later in
  the same block); the short-viewport flex face ignores rows.
- **F4b Tall phones — the card (the second half of the same fix):**
  with the foot pinned at 739px, the card must be tall enough that
  the bottom emblems (top edge 103px above the card bottom,
  probe-measured) clear it. `@media (max-width: 640px) and
  (min-height: 701px)`: `.identity-pro-card, #certPlaque {
  min-height: 798px; }` — the foot does not move when the card
  grows, only the emblems move down, so the emblems' top edge lands
  7px below the foot and their bottom edge 8px above the viewport
  bottom at 390×844 (the whole slack there is 15px, split 7/8 —
  measured, not guessed). Verified live BEFORE staging it, by
  injecting the rule into the staged v5 page: foot 396..739
  unmoved, emblems 746..836. The card is in flow (the bottom system
  bar is `position: relative`, the top bar sticky), so the document
  scrolls ~90px and the bottom bar rides below the fold; the
  certificate itself fits the first viewport. Short viewports
  (≤700px tall) are excluded: there the face is flex and the card
  must stay viewport-sized (the flex content would chase the
  emblems down). Both the card and the plaque carry it — the plaque
  fills the card, and the emblems anchor to the plaque
  (`offsetParent` measured: `certPlaque`).
- Kept byte-identical: the four `.corner-crest` slots (only their
  box/center values changed), the rotations, the `::before` pooled
  shadow beneath each corner, the crystal-N seal, the five stones,
  the title, the certifies line, the solid white name, the agreement
  line + reader, the ENTER claim path.
- Diff base → new: **+50 lines, −18 lines** (geometry + die-cut +
  rows + card min-height + comments). Visible words: 602/602,
  identical.

## §4 Staging verification (build ran 2026-11-17, staged 22:35:03Z)
- `build-emblem-corners-fix.py` reproduces the tip, guards live
  staged bytes, applies F1–F4b with asserted replacements, runs
  `vm.Script` syntax check, node driver, stages, read-back-verifies,
  verifies live routes. Exit 0; all asserts passed.
- **Canonical staging (v6):** entry **3,804,043 B, sha256
  `a5e529f9d78a279caa2a3999a502645e202ac8d49a3f22651f01fcfb520bf85b`**;
  worker sha256
  `5bfa072ad0ca53771ae29ed302ee274de359c7e64d2f46a821f1ad6f3a20fd5a`,
  Cloudflare read-back MATCH, `modified_on
  2026-11-17T22:35:03.843244Z`. Worker gzip 5,170,594 B (limit
  10,485,760).
  Live staged `https://naya-pricing-free-staging.nayapower.workers.dev/free`
  serves the new bytes (3,804,043 B == source MATCH); `/free/walk`
  unchanged (3,293,555 B, sha `46bc52e5…`); `/` 1,966 B; `/free/hub`
  302 → `https://nayanet.app/`; sw.js 567 B / manifest 581 B
  harvested-match; pricing v78 unchanged (11,360,503 B, sha
  `ca2eafeb…`). Live pricing (`naya-model-pricing`) untouched.
  Timestamped URL verified: `/free?t=1794954952` serves the new bytes
  (sha `a5e529f9…` MATCH).
- The disk save of the new entry is deliberately SKIPPED in the build
  (step 6): truncate-first writes are what the EPERM flake destroys —
  the bytes live in memory + on the staged worker, and the filing
  script re-derives them in memory, never from disk.
- **The v1→v6 iteration (honestly recorded — the fix took six
  stagings, not one):**
  - v1 (22:08Z, F1–F3 only): 3,802,910 B, sha `66da830b…` — corners
    whole at 1920, die-cut present; the 390 bottom overlap found by
    my own probe.
  - v2 (F4 padding 112px): 3,803,292 B, sha `bd553323…` — foot still
    under the emblems at 390 (13px benefit / 35px privacy overlap).
  - v3 (F4 padding 160px): 3,803,403 B, sha `ab1218cc…` — 635
    cleared; 390 still overlapped (the foot moves up ~half as fast
    as the padding grows).
  - v4 (F4 padding 280px): 3,803,470 B, sha `ef59b1c6…` — foot
    cleared at 390, but the head collided with the name input (the
    title hid behind the input box) — seen in my own screenshot
    read, not shipped.
  - v5 (F4 rows `auto auto 1fr` + padding 160px): 3,803,439 B, sha
    `3860b7b6…` — head intact, but the foot moved the WRONG way
    (benefit 38px / privacy 35px overlap): the top auto row grew to
    the head's true 266px, pushing the foot row down. The rows pin
    the foot; they do not lift it.
  - v6 (F4 + F4b card min-height 798px): 3,804,043 B, sha
    `a5e529f9…` — **120/120**. The lesson, stated plainly: the foot
    cannot be moved by padding or rows alone — the only lever that
    moves the emblems without moving the foot is the card height,
    and it only works because the auto rows pin the foot first.

## §5 Static audit + design-laws check (from live staged bytes)
`audit-emblem-corners-fix.py` (exit 0): re-derived entry in memory
3,804,043 B sha `a5e529f9…`; live staged `/free` 3,804,043 B sha
`a5e529f9…` == re-derived MATCH; `vm.Script` syntax OK.
- **Emblem proof from LIVE bytes:** the PNG data URI in the served
  bytes decodes to **2,654,505 B, sha256
  `1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4`** —
  byte-identical to NAYA_ICON.png, not re-derived.
- **Words:** visible words base 602, new 602, identical.
- **Diff:** +50/−18 lines, CSS + one SVG filter defs block + comments.
- **Design-laws machine check** (the exact `check-design-laws.py`
  regexes, run in memory over BASE vs NEW bytes): BASE 12 FAILs / 1
  WARN; NEW 12 FAILs / 1 WARN; **NEW-ONLY FAILs (by content): 0.**
  All 12 are inherited, adjudicated as in the prior round: comment
  prose containing "gray"/"grey", `border-color: rgba(...)` on
  borders (not text), sub-17px icon glyph sizes.
- **Audit's own bug, found and fixed in this round:** the audit's F4
  assert still said 160px when the live bytes carried 280px (v4) —
  a stale assertion in my audit script, not a page defect. Fixed to
  the staged value each time (160px + rows + min-height in v6) and
  re-run clean.

## §6 Structural proof (CSS-derived geometry, not measured)
- **Desktop 1920×999:** corner box 132×161 at 59° → rotated bbox
  206×196; centers 112px from each edge → emblem top edge y=66,
  bottom edge y=935 — whole in the card and in the first viewport.
- **Mobile 635×390:** box 64×64 at 35° → bbox 90×90; centers 56px
  → top edge y=63.4, bottom edge y=328.6 — whole in the card (the
  document scrolls at this height by design; the bottom pair is
  whole when scrolled to, §7).
- **Mobile 390×844:** same box → top edge y=63.4, bottom edge
  y=782.6 in card coords; with the card at min-height 798px the
  bottom emblems sit 746..836 in viewport coords — whole in the
  first viewport, 7px below the foot, 8px above the viewport bottom.
- **Foot clearance (F4+F4b, derived + probe-measured):** foot pinned
  at 739px (auto rows); emblem top at 746px (card 798px) — gap 7px.
- **Nothing covered (structural):** the corners are `position:
  absolute` at the card's four corners; the title, certifies, name,
  input, ENTER and agreement line are centered in the face — the
  corner boxes and the centered text do not share coordinates by
  construction at desktop; at mobile the foot clearance is the
  measured gap above. The live overlap check is the probe (§7).

## §7 Live probe — RUN (120/120), read as the eye
`probe-emblem-corners-fix.py` (Playwright Chromium via the
localhost forwarder on 127.0.0.1:18080 — VM browsers recovered
this window; Chromium launched OK 22:09Z). Pre-claim face, NO alias
typed, NO claim made, no test cert touched. Exit 0:
**PROBE-CORNERS: 120/120 checks passed.**
- **1920×999:** all four corners whole in the viewport (tl x=10
  y=67 right=216 bottom=263; tr x=1704..1910; bl y=738..934; br
  same); rotated bbox 206×196 (matches the math); die-cut filter
  present in computed style; center seal present; no corner/text
  overlap; title/certifies exact; name solid white; no gray text;
  no horizontal overflow; emblem decodes 1800×2000 in-page; no page
  errors.
- **635×390:** top pair whole at scroll 0; bottom pair whole when
  scrolled to (bl x=12 y=202 right=102 bottom=291 in the scrolled
  viewport); no corner/text overlap at either scroll position.
- **390×844:** all four whole in the first viewport (bl/br x=12 /
  288, y=656..746); no corner/text overlap; foot gap measured 7px
  (emblem top 746, foot bottom 739); emblem bottom 836, viewport
  844.
- **Screenshots read as the eye (this seat):** 1920 — all four
  emblems whole, no diamond edge, purple gem reads, silver surround
  reads clearly, teardrop visible, center seal untouched, nothing
  overlaps. 390 — title and certifies fully visible (the v4 head
  collision is gone), every foot line fully readable, bottom
  emblems whole in a quiet black band below the text; the band
  reads as intentional seal space. 635 — top emblems whole and
  die-cut at scroll 0; ENTER rides below the fold (the document
  scrolls at this height by design, as before).
- **The install veil (pre-existing, not this round's):** the page
  auto-shows an "Install NayaNET" modal 5s after load (up to 3x
  per browser, localStorage-gated, never over a finished/taken
  document). It covered the certificate in two probe screenshots
  before I understood it. The probe now dismisses it the user's way
  (`#installLater`, "Not now" — the DOM text is "Not now", CSS
  uppercases it; my first dismiss attempt used the uppercase text
  and silently missed). **The eye must dismiss it too** — one tap
  on NOT NOW / the X — or judge within the first 5 seconds. It is
  base behavior; this round did not touch it, and the audit's
  602/602 words + invariants prove the diff didn't reach it.
- **Probe bugs fixed along the way (do not reintroduce):** size
  must use `offsetWidth/offsetHeight` (getBoundingClientRect on a
  rotated slot returns the rotated bbox); `uriHead` slice must be
  54 chars, not 40; bottom corners at 635 must be judged after
  scrolling the WINDOW (not the plaque); text rects must pick the
  first element with a non-zero rect, falling back to the first
  match (the name echo is empty pre-claim; `.cert-privacy` has a
  hidden first copy); judge's C-READ checks must be None-safe.
- **What the probe proves vs. what it does not:** it proves
  geometry, filter presence, words, and no box overlap at all three
  widths, plus my own visual read of the screenshots. It does not
  replace the independent checker's cold verification or Shawn's
  eye (final gate, still owed).

## §8 What passed / did not pass / is owed
**PASSED:** base verified cold · emblem source hash-proven · fix
F1–F4b applied with asserted replacements · build + stage · node
driver · live staged bytes sha-matched (two independent routes:
build `_sim.http_get` + `audit-emblem-corners-fix.py`) · emblem
byte-identical from live bytes · visible words identical · design
laws (zero new FAILs by content) · pricing v78 untouched · walk
unchanged · zero aliases burned/touched · live probe 120/120 at
1920/635/390 with screenshots read as the eye · timestamped link
verified.
**FOUND AND FIXED IN THIS ROUND (named, not hidden):** the 390
bottom overlap (F4, three wrong levers before the right one — §4);
the v4 head collision (padding 280px — the title hid behind the
input box); the v5 foot moving the wrong way (rows pin, they don't
lift); my own audit's stale F4 assertion (160px vs the staged
280px); my probe's veil-dismiss using the wrong case ("NOT NOW"
vs the DOM's "Not now"); the probe's rotated-bbox / scroll /
rect-picking bugs (§7).
**OWED:** (1) the independent checker's cold verification of this
report; (2) the cloud-browser eye at ~1919 first (the brief names
it; the VM probe already passed 120/120, but the cloud eye is the
named route — and it must dismiss the install veil first, §7);
(3) Shawn's eye, phone-first, before anything is shown to him as
done.
**OPEN CONDITIONS (stated plainly, not as fine print):**
- The 390×844 slack is THIN by construction: 15px total, split
  7px (foot gap) / 8px (viewport margin). Measured, not guessed —
  but a taller foot (longer agree text, a wider name echo) would
  eat it. If the foot ever grows, the card min-height is the knob
  (798px → higher), not the padding.
- The bottom system bar rides below the fold at 390×844 (the
  document scrolls ~90px; the top bar is sticky). The certificate
  itself fits the first viewport; only the system bar needs a
  touch of scroll.
- The certified + taken faces' mobile foot clearance is REASONED,
  not probe-measured: their feet are shorter and their bottom-row
  shares larger, so they clear by a wide margin — but the probe
  cannot claim a certificate (no alias typed), so the eye will see
  those states first on Shawn's own certificate.
- At 635×390 the bottom emblems are whole in the card and whole
  when scrolled to — they cannot be in the first viewport at a
  390px-tall viewport while the certificate content is ~700px tall.
  The brief's "seen whole in the first viewport at 635/390" is
  satisfied at 390×844 (the phone viewport) and at 1920; at
  635×390 it means whole in the card, visible on scroll.
**OUTSIDE THIS ROUND (received, not acted on):** during the round,
AGENTS.md + MEMORY.md received outside updates (21:59Z/22:00Z dark
middle + white icon supersedes the white-middle law, one icon set /
one sidebar / one look on every page; 22:28–22:39Z the Hub feed
corrections — glow OVER not around, the ball not a circle, clarity
at zoom, no gray text, hover lights the rim only, sidebars even
out, 3D not 2D with elevation over glow and press-in/come-out
aliveness — plus the Hub A4 eye, Personal visitor eye, Smart Mail /
Smart Note Grandma / Dashboard bar-depth eyes going back, and VM
browsers alive again). They concern sidebar/bar tiles, the Hub,
and other pages — not certificate corners. Named here so the
coordinator sees them, not silently absorbed.

## §9 The identity + unfold sequencing (unchanged — still sequenced)
Identity + unfold stay SEQUENCED — not staged here, per the brief
(collision + worker-size law; the follow-on serves the emblem once
per worker via a shared route). The prior round's SPEC script holds
the byte-proven diffs. Nothing in this round touches the
walk-beginning worker or the identity page (the identity move to
`a1550164…` was observed, §2, not caused here).

## §10 Aliases
**Zero aliases typed, zero claimed, zero touched.** No probe in
this round claims anything. The test certs (certfix Nº 000789,
certcurrent Nº 000788, certfix390–390d Nº 000790–000793) are
untouched and ride the test-cert cleanup (his hand).

## §11 Self-Check Law — three checks + seven questions (in writing)
**Check 1 — build invariants (run 22:35Z):** emblem hash asserted
at read; base SHAs asserted at every chain link; tip worker
reproduced byte-exact before changing anything; F1–F4b
replacements asserted; corner slots/positions/rotations asserted
byte-identical; certificate pieces asserted present; `vm.Script`
syntax on the new entry; node driver PASS; worker read-back MATCH;
live routes MATCH.
**Check 2 — independent static verification (after the fix):** §5
audit from live served bytes (not from build memory) — emblem
byte-identical from live bytes, visible words identical, diff
CSS-only + filter defs, laws diff zero new FAILs by content.
**Check 3 — live staged verification + live probe:** §4 (the exact
bytes on the staging worker, re-fetched and sha-matched through
two independent routes, plus the timestamped URL verified) and §7
(120/120 measured rects at 1920/635/390, screenshots read as the
eye). What check 3 does NOT include (honestly): the independent
checker and Shawn's eye. Those are §8, owed.

**The seven questions:**
1. **Most intelligent?** Yes — the emblems move inward to where
   the card actually is instead of straddling its edge; the black
   is cut by its own luminance instead of redrawing the file; the
   foot clearance uses the rows + the card height (the two levers
   that actually move the right things) instead of the padding that
   provably breaks the head; the wrong levers were measured, named,
   and abandoned instead of shipped.
2. **Most logical?** Yes — every step follows from evidence in
   order: source hash-proven, base verified cold, defects measured
   (rects, not impressions), change applied with asserted
   replacements, staged, re-audited from live bytes, probed at
   three widths with measured rects, screenshots read as the eye.
   No leap: nothing is claimed that a tool result does not show.
3. **Most sensible?** Yes — a wise operator would rather hear "it
   took six stagings, here is what each one taught" than receive a
   clean report built on the first staging that hid the 390
   overlap; stopping the padding lever at the measured head limit
   instead of pushing it is sensible; dismissing a pre-existing
   modal the user's way instead of hiding it in code is sensible.
4. **Full scope?** Yes — the whole page as he will see it: the
   four corners at all three widths, the head (title/certifies
   intact after the v4 collision), the foot (every line readable),
   the center seal untouched, the veil named as an eye obstacle,
   the outside updates named, the thin slack named, the sequenced
   identity/unfold named, live pricing untouched.
5. **Consequences?** First order: `/free` staging now serves the
   certificate with whole, die-cut, legible corner emblems at every
   width. Second order: the checker seat can run the real eye with
   a ready probe and no alias needed; the eye must dismiss the
   install veil first; Shawn's eye is the final gate before
   anything is shown to him. Who it touches: only the staging
   worker — no live page, no citizen data, no alias touched.
6. **Pros and cons?** Pros: all four eye defects fixed and
   probe-proven at three widths; the emblem stays verbatim; zero
   new real design-law fails; words unchanged; the iteration is
   fully recorded. Cons (stated honestly): the 390 slack is 15px
   total — thin; the bottom system bar rides below the fold at
   390×844; the certified/taken mobile feet are reasoned, not
   probe-measured; the independent checker and Shawn's eye are
   still owed. Strongest case against my preference (ship the
   report as done): the static + probe proof is strong, but Shawn's
   eye is the final gate by law — calling this done without it
   would repeat the exact failure the laws were written for.
7. **Best possible choice?** Yes — against the ultimate objective
   (the four corner emblems seen whole, die-cut, legible, proven,
   with nothing hidden): fix the geometry, cut the black in
   presentation only, clear the foot with the levers that actually
   work, prove it at three widths with measured rects and read
   screenshots, name the thin slack and the veil plainly, and hand
   the checker seat a ready probe that needs no alias. That is the
   best choice available.

## §12 Design-laws §11 check (in writing)
**The five gates (before every consequential action):**
1. **IS IT RIGHT?** Yes — the eye's four defects are fixed as
   specified, the emblem stays verbatim, the center seal stays.
   No harm, no privacy touch, no money touch, no live touch.
2. **IS IT WHAT THEY TRULY NEED?** Yes — his eye's words were
   whole emblems, no diamond edge, a legible surround, the seal
   untouched. Each defect has its fix (F1/F2/F3/F4+F4b), each fix
   has its measurement.
3. **IS IT MINE TO DO?** Yes — staging only, on the brief's branch
   and worker; no merge, no live touch, no credentials, no
   destructive act. The judgment calls (the 7/8 slack split, the
   veil left as base behavior, the certified/taken feet reasoned
   not measured) are named for the captain's hand, not smuggled
   through.
4. **IS NOW THE TIME?** Yes — the round was dispatched, the base
   was verified cold first, the certificate worker was free. The
   VM browsers recovered mid-round, so the probe ran live instead
   of being owed — the round took the better proof when it became
   available.
5. **CAN I PROVE IT?** Yes for everything structural and rendered
   in this seat (§§4–7: bytes, shas, counts, diffs, the emblem
   decoded from live bytes, 120 measured rects, screenshots read
   as the eye); honestly NO for the independent checker and
   Shawn's eye (§8, owed). Receipt before report — and the
   unproven part is named, not claimed.

**The design check (ask on every page, every object):**
- *Could I pick this up?* The corner emblem — yes: a real object
  with depth (drop-shadow elevation + the pooled shadow beneath),
  sitting ON the frame corner, no longer straddling the edge.
  The die-cut leaves the filigree floating on the card, not pasted
  on a square.
- *Where is the light coming from?* Top-left: the drop-shadow
  falls down-right; the pooled `::before` shadow sits beneath.
  Consistent with 135°.
- *What is it made of?* The emblem itself — a crowned jewel,
  verbatim. Black inside (its own black, now cut away where it was
  background), silver + purple outside as its own light. No glow
  inside the emblem — the image is the object.
- *Does it cast a shadow?* Yes — the drop-shadow filter (chained
  after the cut, so it follows the cut silhouette, not the square)
  + the pooled shadow ground each corner.
- *What happens when I touch it?* The corners are `aria-hidden`,
  `pointer-events: none` decorative seals — not controls. They do
  not answer touch, by design (a seal doesn't depress). The page's
  live objects (ENTER, ⓘ, name field) keep their hover/touch
  behavior, unchanged.
- *Is there ANY glow inside, at rest or on hover?* No — the
  emblem's own star glow is the image's own light, not a CSS glow
  inside an icon; no new glow was added. (The Hub's new glow law —
  glow around/behind, never over the top — is named in §8 as an
  outside update; this round adds no glow anywhere.)
- *Is any text gray, especially small?* No — audit cut tokens all
  0; laws machine check 0 new FAILs; the 12 inherited FAILs are
  comment prose / border-color rgba / sub-17px icon glyphs,
  adjudicated in §5.
- *Is any text smaller than 17?* No new size flag. The two machine
  SIZE flags (13px/15px) are pre-existing icon glyphs, not text.
- *Are two same colors together anywhere?* No new pair introduced.
  The emblem's purple is the system's own royal purple family; the
  four corners are not adjacent (they are the four corners of one
  card).
- *Does anything sit flat or dead?* Nothing new is flat; the
  corners — the flattest art on the page — gained a real object
  (the die-cut) and real clearance. Nothing added is dead.
- *Can I see what the icon IS?* Yes — the emblem is the clearest
  icon in the system (crown, wings, diamond, star, teardrop), now
  at 132px/64px instead of the clipped 100px/54px it replaces, and
  the surround reads at both sizes.
- *Which reference object was it measured against?* NAYA_ICON.png
  itself (the source, hash-proven) for the emblem; the certificate's
  own corner slots (`.corner-crest`, harvested verbatim) for the
  placement; the mobile `.crest-medal` drop-shadow for the
  elevation; the live foot/head rects (measured, not modeled) for
  the clearance.
- *Read it as a reader, top to bottom:* emblem in each corner (the
  seal-mark) → crystal-N seal → title → certifies → name → ENTER →
  agreement (the substance) → claims → benefit → privacy → emblems
  below, in their own quiet band. The reading is unchanged except
  the seals are whole and the foot is clear; the document now
  carries its seal properly.
- *Shawn's eye is the final gate.* Not passed yet — §8.

**The sense check:** I did not obey the brief literally past the
page — the padding lever was abandoned when the screenshot showed
the title hiding behind the input (the brief's "inset the emblems"
did not mean "break the head"); the rows lever was abandoned when
the probe showed the foot moving the wrong way; the card lever was
taken only after a live injection proved it moves the emblems and
not the foot. I did not remove what he didn't ask to remove (the
center seal, the five stones, the reader, the ENTER path — all
kept). I did not touch what he didn't ask to touch (Dashboard,
Hub, walk, pricing, live, identity, unfold). The audit's stale
assertion was fixed, not explained away. The outside standard
updates were named, not silently absorbed. The veil was dismissed
the user's way, not hidden in code.

**The scorecard:** why is it not a 10? The independent checker
hasn't verified it cold; the cloud eye hasn't judged the corners;
Shawn's eye hasn't seen it; the 390 slack is 15px; the certified /
taken mobile feet are reasoned, not measured. Ten things missing:
(1) the checker's cold verification, (2) the cloud eye's verdict
at ~1919, (3) Shawn's eye phone-first, (4) the certified face's
mobile foot measured, (5) the taken face's mobile foot measured,
(6) a wider foot margin at 390 (if the foot ever grows), (7) the
bottom system bar back in the first viewport at 390, (8) the
635×390 bottom pair in a first viewport (impossible at 390px tall
— §8), (9) the veil's 5s auto-show judged by his eye, (10) the
identity/unfold staging (sequenced, §9). My score is irrelevant;
his eye is the instrument.

**Harvest, never invent. Use what works, never make it new. Restore
what was good, verbatim. Don't remove what he didn't ask to remove.
Don't move what he didn't ask to move. Don't touch what he didn't ask
to touch.** The emblem is taken verbatim; the corner slots are
harvested, not rebuilt; the foot and head were measured, not moved;
nothing removed, moved, or touched beyond F1–F4b.

## §13 Filing receipts
- Branch: `emblem/corners-fix-20261117` (NEW, from emblem/certificate
  tip `f23b6202`)
- Commit: TO BE FILLED
- Tree: TO BE FILLED
- Files filed (blobs, all read-back MATCH by sha256): TO BE FILLED
- PR: TO BE FILLED, open, UNMERGED, base `main`
- Receipts commit (this report, §13 filled): TO BE FILLED
- Staged: `https://naya-pricing-free-staging.nayapower.workers.dev/free`
  (entry 3,804,043 B, sha `a5e529f9…`, worker sha `5bfa072a…`,
  `modified_on 2026-11-17T22:35:03Z`; timestamped link verified §4).
- Live `naya-model-pricing` untouched; nothing merged.
- The filing scripts themselves (`file-corners-fix-to-github.py`,
  `file-corners-fix-receipts.py`) live only on disk in the round
  directory, as in the prior round — they are the mechanism, not the
  record.
