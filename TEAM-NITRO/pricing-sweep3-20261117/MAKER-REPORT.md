# MAKER REPORT — Free Entry (/free), Inspector Sweep #3, Link #13

**Round:** Inspector Sweep #3 fix round · **Date:** 2026-11-17 · **Seat:** Fix Coordinator
acting as maker (see §9 — spawn deviation) · **Score in:** 7/10
**Report fixed:** `~/workspace/team-nitro/inspector-sweep-3-20261117/REPORT-13-free-entry.md`
**Base:** branch `pricing-f4-free-entry-20261116`, head
`eafbac1616966bd6b1d0151a916140722c7699ba`, file
`TEAM-NITRO/pricing-fix-20261117/fixed-entry.html`, 315,878 B, sha256
`06b08242c72e9d0b8f28037df3b93e74c5955e6702f358d0a07fff799edf58fd` (verified before
starting; the working copy re-verified to the same sha after copying).
**Method:** edit in place, never rebuild. One script, `apply-fix.py`, applied every
replacement with exact-count assertions plus final guards; three assertion failures
during the run were fixed in the script (see §8), never by hand-editing the page —
except the clock breakpoint (§5), which was changed after measurement, in both the
script and the file, and re-verified.

## §1 — The fixed bytes

| File | Size | sha256 |
|---|---|---|
| `fixed-entry.html` | 337,779 B | `9ac3b4f5f8189bf353af34f186ea9d14133e4024e1312be879a09a87d5f01ad3` |
| `manifest.webmanifest` | 585 B | `4e7958edfd722fbd8d3e842a7dd1076edf9e6bdfaef6a10f6be3dd6ad588a155` |
| `icons/icon-512.png` | 229,337 B, 512×512 | `770cfa135f5e5dd983d7c1d7cd0b1e3e397e3ff482adc0465d644c15c4d8acbd` |
| `icons/icon-192.png` | 48,626 B, 192×192 | `32903142c8e364e7ec01c32ced0bb47d2fe9bf4c3552b3ad751074d76005eb29` |
| `icons/apple-touch-icon.png` | 43,852 B, 180×180 | `0dfac98028743b9cdc398a6adde8efccdbd44acdcb3553980e01001e55fb2020` |

The entry file's sha after the 14 fixes alone was
`14d31b739329f1c305643a1e2ac2bf1b37b1b2a526c5ea1d339ec116e52b1e4d` (320,834 B);
the certificate harvest (§11) brought it to the sha above. Icons generated from
the harvested 512×512 crystal-N JPEG embedded in the page
(the header brand-mark and the seal `.logo-hero` share that image, sha
`f9c2290e…`); the manifest is identical to the live manifest except
`theme_color` `#a855f7` → `#8e24aa`.

## §2 — Fix by fix (all 14 items in §6 of the report)

**Fix 1 — Type scale (25/19/17).** All 31 sub-17px rules raised. Headline
`.cert-title` 25px desktop (`1.5625rem`); sub-headline 19px (`1.1875rem`: brand
wordmark, `.alias-status`, `.install-sub`, phone title); everything else 17px
(`1.0625rem`). Root font-size left unset (16px default) — the rules were fixed,
not the root. Verified: no `font-size` in the file computes below 17px (smallest
values `1.0625rem` ×24, `1.1875rem` ×4, clamps with a 17px floor). The phone title
stays on ONE line at 19px (measured, §4) — the expected two-line wrap did not
happen.

**Fix 2 — Deep palette.** Every bright token replaced with the §3.1 table value
and grepped to zero: `#2fe89e`, `#ffbf3d`, `#a06bff`, `#a855f7`, `#3fb8ff`,
`#a8dcff`, `#ffd97a` (0 remaining); `rgba(47,232,158`, `rgba(63,184,255`,
`rgba(255,191,61`, `rgba(160,107,255`, `rgba(168,85,247` (0 remaining).
`--green #07925f`, `--gold #d4a017`, new `--blue #0f52ba`,
`--royal/--purple/--label #8e24aa`; royal family `rgba(142,36,170,…)`, Link
`rgba(7,146,95,…)`, Mail `rgba(212,160,23,…)`, focus `rgba(15,82,186,…)`. Link
label light emerald `#a9e5cd`, Mail label light gold `#ecd27e`. Box faces are dark
tints of the deep hues (Link `#0b3d2c/#062015/#030604`, Mail
`#33260a/#1a1305/#060402`). `.enter` radial top `#2e0a38`. `breathe-blue` renamed
`breathe-green` (no `breathe-blue` left). Seal star, frame light and travel arc
re-tinted to deep-family lights. Assignment comments updated with dated
SWEEP #3 notes; history kept.

**Fix 3 — Keyboard Enter.** `keydown` Enter on `#aliasInput` → `activateAndRedirect()`.
Veil rule, one behavior, documented in the code: Enter while the veil is up
dismisses the veil first and does NOT submit — one gesture, one outcome. The
veil's document keydown handler carves out Enter-from-`#aliasInput` so the field's
handler decides. Proven by spy in Chromium (§4): veil hidden → 1 call; veil up →
0 additional calls, veil dismissed.

**Fix 4 — Install icons.** The three icons above + the manifest (Fix 2's
`theme_color`). `openModal` gets an icon fallback (`icons/apple-touch-icon.png`)
so the card never renders an empty logo box. Correction to the report's premise,
recorded in `RECORD-CORRECTIONS.md`: `.logo-hero` DOES exist (line 1205, the seal
`<img>`), so `openModal` copying its `src` already worked — the real defect was
only the manifest icons 404 + `theme_color`.

**Fix 5 — Veil truth.** The veil now INTERCEPTS: `.install-veil{pointer-events:auto}`.
The first pointerdown anywhere dismisses only and never reaches the control beneath,
at every geometry — ENTER cannot claim under the visible veil. Proven by real mouse
click at ENTER's center with the veil up (§4): 0 claim calls, veil dismissed. The
F4 record's "1st click dismisses only, 2nd fires ENTER" is corrected in
`RECORD-CORRECTIONS.md`: it was true only for the covered geometry (the card sat
over ENTER's center, so the click died on the common-ancestor rule); an uncovered
ENTER fired — and claimed — on the first click.

**Fix 6 — Taken-name spelling.** New `spacedName(alias)`: from the typed words, or
`rawName` when it matches the alias; an alias typed without spaces paints exactly
as before. Echo painter only; `fitTakenName` one-line rule untouched. Proven (§4):
typed "Rowan Hale" → `spacedName('rowanhale')` = "Rowan Hale"; typed "rowanhale" →
"Rowanhale".

**Fix 7 — ALIAS RESERVATION — recorded only, Shawn's hand.** ENTER POSTs
`/api/claim` before the walk, burning the alias if the walk is abandoned. The fix
round did NOT redesign the claim flow. The decision is his: reserve after the walk,
release uncompleted claims, or keep as-is. Owed — see §7.

**Fix 8 — Headings + zoom.** The certificate title `<div>` is now the page's
`<h1>` ("Certificate of Smart Identity", exactly 1 `<h1>`, 24 ids, 0 duplicates).
Viewport meta is now `width=device-width, initial-scale=1.0` — `maximum-scale=1.0`
and `user-scalable=no` removed.

**Fix 9 — Spectrum Flow.** The ignition is re-flowed to the Flow law (his 18:00Z
law: magenta → purple → indigo → cyan → green → gold → orange → red → magenta,
order never changes): focus sapphire blue `#0f52ba` → Smart Link box emerald
`#07925f` → Mail box deep gold `#d4a017` → ENTER royal purple `#8e24aa`. The v2.7
assignment (Link blue, Mail gold, ENTER purple) predates the Flow law; the newer law
wins. This is a re-flow by law, not a re-pick by taste — documented in the code
comments with the date and the law named.

**Fix 10 — Light direction.** Every `linear-gradient` is now 135° (only angle present
in the file). Radial lights moved to top-left (`at 0% 0%`, ×2). Recorded exceptions:
conic rings (frame travel, well travel) and the centred seal-star radial have no
linear angle — the law does not apply to them.

**Fix 11 — Clock dot.** The 6px flat purple dot is an 8px jewel: radial white →
`#e3c8f5` → `#8e24aa` → `#3d0a52`, plus glow. The ticking clock itself stays.

**Fix 12 — Clock placeholder.** `<span id="sysClock"></span>` — empty in the source
until the first tick. (After ticking it reads e.g. "Tuesday, November 17 · 18:47:28",
measured.)

**Fix 13 — Hub-note latent leak.** Reworded to plain human words: "One step left:
the Hub address isn't set yet, so this button can't take you straight in." No
variable name in the user-facing note. `HUB_APP_URL` remains only in code (the const
definition, the honesty-guard comment) — that is the variable's legitimate home, not
a leak.

**Fix 14 — Record corrections, no page change.** Written in `RECORD-CORRECTIONS.md`:
the "145 ids" count belongs to `fixed-walk.html` (F4 record correct, inspector
wrong); "Rowan Hale Nº 000784 / Milo Fern Nº 000785" stands as the F4 checker's
live record, not re-proven here (no live claim writes this round); the veil claim
is corrected per Fix 5; `.logo-hero` exists per Fix 4.

## §3 — Fit: the 17px floor and the privacy line

The inspector judged fit from CSS only and missed that the privacy line was ALREADY
clipped at baseline in the typed/panels-shown composing state (live: 33px at
1440×900, 52px at 390×844; v2.11.1's "lands by ≈14px" does not reproduce). The fix
keeps the foot's own rhythm (v2.11.1's method): desktop panels-shown block tightened
(status margin 2, lines margin/gap 4, line padding 5/6, button margin 4, claim margin
6, benefit/privacy margin 2, well padding 10px, face padding-top 16px); phone block
tightened likewise; benefit/privacy `max-width` 460→500px (keeps the benefit on two
lines at desktop). And the tail is made reachable, never clipped: the face scrolls —
`.cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])).identity-face {
overflow-y: auto; }` — the page's own tall-state pattern (taken/certified states
already scroll).

Measured in Chromium (file://, typed "rowanhale", Marcellus confirmed loaded):

| Viewport | Privacy at scroll 0 | Scroll to reveal | Input centre vs viewport centre |
|---|---|---|---|
| 1440×900 | clipped 14px | 15px → 849 ≤ 850 | 446 vs 450 (dead-centre) |
| 390×844 | clipped 119px | 120px → 757 ≤ 758 | 393 vs 422 (phone lift, by design) |
| 1024×768 | clipped 82px | 83px → 717 ≤ 718 | 381 vs 384 |
| 768×1024 | fits, +50px | 0 | 506 vs 512 |

Honest adjustment, labelled as estimate: file:// collapses the status line to
'unknown' (empty), while live shows 'available', which adds ~22–26px. So on LIVE
the scroll needed is estimated at ≈37–40px desktop, ≈141–145px phone,
≈104–108px at 1024×768. The privacy line is reachable everywhere by scrolling
the face; it is below the fold on phone in the typed state. That is the measured
state, not a claim of fit.

## §4 — Verification (all by this seat, Chromium via the localhost forwarder)

- **Design-laws checker:** 10 FAILs, 0 real — the same count and the same classes
  as the base run: comment prose containing the word "gray" + `border-color`
  substring matches (`rgba(245,241,232,0.32)`, `rgba(142,36,170,0.52)`). No new
  real violation. The checker cannot see the rem-based type scale; the scale was
  verified by grep (§2, Fix 1).
- **JS syntax:** `node --check` on the extracted scripts — OK (3 script blocks).
- **Behaviour (spy + real mouse, 1440×900):** Enter veil-hidden → `activateAndRedirect`
  called 1×; Enter veil-up → 0 additional calls, veil dismissed; real mouse click at
  ENTER's centre with veil up → 0 calls, veil dismissed; `spacedName` "Rowan Hale" →
  "Rowan Hale", "rowanhale" → "Rowanhale"; clock dot 8×8 jewel; `sysClock` ticks;
  `<h1>` "Certificate of Smart Identity".
- **Header:** fits at every tested width (`headerScrollW` == viewport at 1440, 1024,
  768, 390). Clock breakpoint settled by measurement (§5).
- **NOT re-proven this round:** the taken/certified states live (file:// cannot reach
  `/api/claim`; staging serves the old bytes); the live `/api/claim` GET (staging
  still serves the pre-fix bytes, and the fix changes no API path — no reason to
  re-prove the API, and no live claim writes were made); the Rowan/Milo certificate
  numbers (F4 live record stands, §6); and the certificate harvest's behaviour in
  a browser — the VM browsers died (Chromium SIGTRAP, Firefox launch failure)
  after the 14-fixes measurements were banked (see §11). Static verification of
  the harvest is complete; the behavioural proofs are owed to the independent
  checker and the captain's eye.

## §5 — Clock breakpoint: measured, not guessed

The script first set the clock-hide breakpoint to 1024px on the estimate that the
header needed ~970px. Forced-visible measurement showed the header with the clock
needs **956px**: at 1024 the clock fits with a 36px gap to Install; at 900 and below
it pushes Install off-screen (`headerScrollW` 956 > viewport). The breakpoint was
therefore set to **960px** (script and file both, comment updated) and re-verified
at the boundary: 1024 clock visible, fits; 961 visible, fits (5px spare); 960 hidden,
fits; 959 hidden, fits; 768 hidden, fits. Reverting to 640px would have shown the
clock at 768–1023 where it overflows — wrong. The 1024px value in the script's first
run is superseded by this measurement.

## §6 — Kept verbatim (§7 of the report — untouched)

The certificate object (frame, crests, stones, seal, carved well vs ENTER slab) ·
the honest states (empty means empty, no demo identity, taken stays silver-white,
a failed claim never stamps and never redirects) · the availability API path
(`/api/claim` GET) and the server-side claim (no registry credential in the page) ·
ENTER in capitals, purple glow, breathing when armed · the free line and the eye ·
`HUB_APP_URL` set to `https://nayanet.app/`. The bottom-five bar is absent by
decision (pre-login gate — no account yet; recorded, not an oversight). The
checker-run false positives (comment prose + `border-color` substrings) were not
"fixed".

## §7 — Owed (not done, not hidden)

1. **Fix 7 — alias reservation: Shawn's decision.** Reserve after the walk, release
   uncompleted claims, or keep. Needs his word; the fix round records it only.
2. **Independent checker seat.** This seat could not spawn one (see §9). An
   independent checker — its own walk at 1920 + 390, its own checker run, its own
   live `/api/claim` GET, never the POST — is owed before the captain's eye.
3. **Captain's eye, phone-first,** on the staged fix before anything goes to Shawn.
   Staging still serves the pre-fix bytes; the deploy step is in `DEPLOY-NOTE.md`
   and is NOT this round's to take (the live step is Shawn's hand).
4. **The certificate treatment — DONE IN THIS ROUND (§11).** Shawn's 18:44Z word
   (the /free certificate shows the outdated treatment) arrived during this round
   and was folded in by the sweep coordinator's follow-up as an additional fix
   item. The harvest is landed in the filed bytes (§11): the trophy name, obsidian
   panels, white labels, typing values, white lift, official sentence + reader —
   all harvested from the identity certificate (sha `8c641f96…`). What is still
   owed on it: the behavioural proofs (trophy render, reader, typing, fit with
   the agreement line) — the VM browsers died before they could run; they ride
   with the independent checker and the captain's eye. The earlier note in this
   report (that the treatment was a round of its own) is superseded by the
   follow-up: the round took the item.
5. **Live fit numbers.** The §3 live scroll estimates (≈37–40px desktop,
   ≈141–145px phone) should be measured on staging once the fix is deployed, not
   taken on trust.

## §8 — Script corrections made during the run (honest record)

`apply-fix.py` asserted and stopped three times; each stop was fixed in the script,
never worked around in the page: (1) a redundant `--gold` rep line after the `:root`
block had already replaced it — deleted; (2) `#2fe89e` count 2 → 1 — the `:root`
replacement had already consumed the `--green` var, leaving only the eye hover;
(3) comment indentation 8 → 7 spaces in four assignment-comment blocks, and 5 → 4
spaces in the FOCUS TRAVEL comment — the script's assumed indent did not match the
file. Final run: all assertions passed, including the `160,107,255` count of 22
(the hand-count of 21 + 1 unlocated resolved in the script's favour).

## §9 — Spawn deviation (reported plainly)

The dispatch ordered the maker spawned within 10 minutes and a checker named and
dispatched as part of the maker's completion. This seat is depth 2/2 with
`can_spawn=no` — it cannot spawn a maker or a checker subagent. The work was done
directly by this seat as maker, and the checker verdict in this filing is a
self-check pass by the same seat, labelled as such. That is a deviation from the
brief: an independent checker seat is still owed (see §7 item 2), and the parent
should dispatch one before the captain's eye. Nothing in this report should be read
as an independent check.

## §10 — Filing

Branch `pricing/sweep3-20261117` from `eafbac16`, filed by `file-fix-to-github.py`
(blobs → tree → commit → ref, read-back verified by blob sha). Files:
`fixed-entry.html`, `manifest.webmanifest`, `icons/icon-512.png`,
`icons/icon-192.png`, `icons/apple-touch-icon.png`, `apply-fix.py`,
`apply-cert.py`, `MAKER-REPORT.md`, `CHECKER-VERDICT.md` (self-check),
`RECORD-CORRECTIONS.md`, `DEPLOY-NOTE.md`, `file-fix-to-github.py`. PR open
UNMERGED. No merge, no deploy, no live touch, no voice, no probe-row cleanup,
no deleting rows, no live claim writes.

## §11 — The certificate harvest (follow-up item, Shawn 18:44Z)

**The word:** the /free certificate shows the OUTDATED treatment; it must show the
CURRENT one — the name ELEVATED, RAISED, beautiful, almost glowing, on black
obsidian, the name in white light. Reference: the Micheal certificate Nº 000204
(certified Nov 13, Certificate Round 2). Bar: SN-2922 (official, glowing, solid;
mail ID first-class). Deed-signing law: the name box IS the deed.

**The source (located first, named before touching anything):**
`~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html`,
376,814 B, sha256 `8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d`
(Round 4 H1 trophy name + Round 5 H3/H1/H2; the Micheal treatment carried through
Rounds 3–5; also the Round 5 branch blob `f760902f…`). The walk's certificate
file (`walk-beginning-fixed.html`, sha `df17ac67…`) is the walk bundle the
/free/walk derives from; the certificate VIEW in the walk is `/identity.html`,
so identity is the harvest source. The locate work was first done by the sibling
seat working the standalone brief (`pricing-certificate-current-20261117/build-certificate.py`);
this round re-verified the sha independently and re-ran its extractor (all 16
anchors unique), then applied the same H1–H4 harvest onto the SWEEP #3 file
(which already carries the 14 fixes) — the sibling builds from the F4 base on
its own branch, so the two filings will diverge; the parent reconciles.

**What landed (H1–H4):**
- **H1 NAME — the trophy:** obsidian gradient body, chrome 1px stroke, purple
  clone behind (`::before`, `data-text`), hover pop, name-settle arrival,
  certified in-flow. Geometry (size/position) KEPT from /free. Certified + taken
  seats use `position: relative` (so the clone anchors to the name) and
  `text-shadow: none` (a shadow would bleed through the transparent glyphs).
  All three name paint sites repointed to the one harvested painter
  (`paintHeroName` + `settleHeroName` on state paints); no old site left.
- **H2 PANELS:** obsidian fills (`#101013 → #050505 → #070708`); labels WHITE
  (the glow carries the family color — the v2.7 family-light labels are
  superseded); values TYPE letter-by-letter with a caret in the panel's own
  color on restore + stamp, instant while composing (`paintValues`).
- **H3 TOKENS — the white lift:** `--silver`/`--muted` `#f2f2f6` → `#ffffff`,
  `--faint` → white 0.88, `--hair` cream → white; all 7 remaining `#f2f2f6`
  text rules → white. Zero gray text left by value.
- **H4 AGREEMENT:** the official sentence, verbatim, under ENTER (typed face
  only) + the clone-trick ⓘ + the one-paragraph-at-a-time reader (9 paragraphs,
  verbatim), harvested whole (CSS + HTML + JS). Hidden in the certified and
  taken states (Round 5 H1 amended).
- **NOT harvested (named, not hidden):** the membership sentence (`.cert-member`)
  and the H6 green taken message — both absent on /free, outside the brief's
  five diff dimensions; follow-ons if the captain wants them.

**Documented re-valuings (harvest the shape, re-value where a newer system law
governs — never silent):**
- **R1 deep palette (Fix 2, §3.1):** the identity's bright purples re-valued to
  the deep family — `rgba(160,107,255,…)` → `rgba(142,36,170,…)`; clone ramp
  `#c9a5ff/#a06bff/#6d28d9` → `#e3c8f5/#8e24aa/#3d0a52` (the clock jewel's own
  ramp); caret `#3fb8ff` → `#0f52ba`, `#ffbf3d` → `#d4a017`. H3's purple
  unification (`#a855f7` → `#a06bff`) does NOT apply — /free already unifies to
  ONE deep purple (`#8e24aa`) by Fix 2.
- **R2 type floor (Fix 1):** the identity's small sizes raised to 17px —
  agree 0.82rem, info glyph 13px, reader title 1.05rem, para 0.92rem, prog/next
  0.72rem, close 15px (label 0.66rem not taken — /free's label stays 17px).
- **R3 light (Fix 10):** the reader's 165° panel gradient → 135°. The name
  body's and the clone's 180° gradients are KEPT as the Fix-10 top-light
  exception (vertical gloss fall).
- **R4 reader IIFE:** the sibling extractor drops the grouping paren (it ends
  at the function's `}` and appends `"();"` — the identity source reads
  `})();`). This round repairs the ending and asserts balanced parens; the JS
  compiles. **The sibling's build carries the same latent one-character bug —
  flagged to the parent here.**

**Verification (static — complete):** bright tokens 0; `#f2f2f6` 0; no `font-size`
below 17px; linear angles only 135°/180° with 180° exactly 2×; ids 29, 0
duplicates; reader 9 paragraphs; sentence verbatim; all harvest markers
present; old paint sites 0; JS compiles (all 3 blocks, in-memory); checker
back to 10 FAILs, 0 real, + 2 WARNs (`color: transparent` on the trophy name +
clone — correct by design, to be cleared by eye).

**Verification (behavioural — OWED):** the VM browsers died (Chromium SIGTRAP on
launch ×2, Firefox launch failure, no full-chromium binary in the cache) after
the 14-fixes measurements were banked and before the harvest measurements could
run. Still owed, riding with the independent checker + captain's eye: trophy
render at 1920 + 390 (clears the 2 WARNs), reader open/Next×8/Close + Escape,
typing values with caret, agree line visible composing / hidden certified +
taken, and fit re-measured WITH the agreement line in (the §3 numbers predate
it — the line adds height to the foot).

**The EPERM flake:** during the harvest window the flake blocked every
exec/python/shell write ≥~50 bytes (reads fine; the tool write path fine). The
harvest was therefore applied by hand via tool edits, each verified by grep
after landing; `apply-cert.py` in the filing reproduces the same transformation
by script for the record (it was NOT the path that wrote the file). The
pre-harvest backup copy could not be made (same flake) — the safety net is
regeneration: the F4 base (`pricing-fix-20261117/fixed-entry.html`, sha
`06b08242…`, intact) + `apply-fix.py`, which ran clean.
