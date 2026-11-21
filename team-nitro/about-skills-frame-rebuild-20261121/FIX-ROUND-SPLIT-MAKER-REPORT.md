# MAKER REPORT — About + Skills FRAME REBUILD, FIX ROUND: THE SPLIT

Maker seat, fix-round-split coordinator (brief FIX-ROUND-SPLIT-BRIEF.md).
Built 2026-11-21. Report to the coordinator, NOT to Shawn.

## What was built

The captain's decision, implemented exactly as ordered: each of the 14 skill
slides splits across TWO frames at a field boundary. Deck is now **42 frames**:
About 1–9 (frames 1–9), Skills 1a/1b … 14a/14b (frames 10–37), About 10–14
(frames 38–42). Pill reads **N / 42** (auto-counts, untouched).

**The split point — uniform for all 14 skills, chosen by measurement, not
taste.** Before splitting I measured every field's rendered height on the
filed build at phone 390×844 (measure-split.py; per-field heights in
measure-split-phone.json). The field-boundary split that minimises the worst
half is the same for every skill — after WHY IT MATTERS:

- **Frame Na:** head + sub + WHAT IT MEANS + WHY IT MATTERS
- **Frame Nb:** WHAT MAKES US DIFFERENT + ONE REAL EXAMPLE + WHAT'S IN IT
  FOR YOU + PROOF

No field is split between sentences: each field sits whole in exactly one
frame. Both halves keep kind `SKILL N` and the same title (the frame's own
title element — no new kind, no "continued" label, no added words). Tones and
beat photos keep cycling by deck position through the agreement's own
mechanism. Frame 9's "See all my skills ◆" still advances into the skills run
(now frame 10, Skill 1a); the last skill half (frame 37, Skill 14b) advances
to frame 38 (About 10); frame 42 carries the Enter anchor. All 42 frames
advance with the page's own buttons, pill 1/42 → 42/42 (render probe).

**Method:** the parent round's `build-about-skills-frame.cjs` was modified so
the split is reproducible, then regenerated and verified. The lane holds the
reproducible build path (modified build script) + the filed file, byte for
byte. Determinism proven: two consecutive runs, same sha256.

## Filed

- Branch: `about-skills-frame-rebuild-20261121` (same branch, same file path)
- Commit (page + build script): `28bc4ed2f97d485ef81286a119f95d666eb5b931`
  (parent: branch tip `e19404c32556eb0b9cdf6bf1e85b250a019bf3bc`, verified
  before filing; branch tip has not moved since)
- Page: `team-nitro/about-skills-frame-rebuild-20261121/about-skills.html`
  - Blob `169914905c84371778a3c63a85956b43970343c2`, **151,375 B**,
    sha256 `24e012ac0f5528a374bd73de65a1680e1490761b226a0b3db9cf591affad84bb`
  - Blob read back by the blob API: size + sha256 match exactly, `cmp` clean
    against the lane file.
- Build script blob `74e66f2e229326a4fc4f929fef2f54dbdbbde228`
  (`build-about-skills-frame.cjs`, 17,457 B — deterministic, see above).
- **Staged link (verified first-hand, HTTP 200, 151,375 B, sha256 match,
  `cmp` clean):**
  https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/about-skills-frame-rebuild-20261121/about-skills.html&ref=about-skills-frame-rebuild-20261121&cb=169914905c84371778a3c63a85956b43970343c2

## Proof 1 — the frame diff (read in full)

`FIX-ROUND-SPLIT-frame.diff` in this lane dir: `diff -u` of the agreement
source (blob `1f0b0474`, 142,532 B) vs the built file, **+84/−91 lines**
(248 lines; the +83/−90 content lines: the deck hunk grows 37 → 42 frames,
as the split orders). **9 hunks, same structure as the parent round** —
header comment + `<title>`; header labels; deck replacement; PLAY script;
playing-state tip string; wireFrame7 fallback labels; media-frame labels.
Hunks 2 and 4–9 are **byte-identical to the parent round's frame.diff**;
only hunk 1 (header comment, now names the 42-frame split) and hunk 3 (the
deck: −37 agreement articles, +42 frames) changed. **Ordered substitutions
only, zero additions:** no extra `<style>`, scripts 7=7, no
aboutSkillsAdditions, no skillsSlideshow, no CSS rule changed, no script
changed except the ordered strings. The only added line containing `<style>`
or "pricing" is the header comment's own "NO additions" sentence. `gray`: 0.

Byte diff vs the filed 28-frame build (`e8cdf13a`): ONLY the skill split
changed — header comment + the deck hunk. Everything outside the deck is
byte-identical except the header comment; everything after the deck is
byte-identical (verified programmatically, FIX-ROUND-SPLIT-verify-split.cjs).

## Proof 2 — content fidelity (programmatic, not eyeballed)

`FIX-ROUND-SPLIT-verify-split.cjs` — **ALL 14 CHECKS PASS**:

- Article count old 28 → new 42; deck order exactly About 1–9, Skills
  1a/1b…14a/14b, About 10–14.
- **About 14 beats normalized-identical** to the filed build (only
  deck-position tone/face/data-beat differ, as the frame's own mechanism
  requires). Date 21 November 2026; "20 November 2026" occurs once, in the
  header comment describing the change.
- **Skills 14: every field verbatim across the two halves** — head, sub,
  means, why, diff, ex, foryou, status, proof (link or verbatim "Proof owed"
  note) compared field by field, in order, concatenated A+B vs the filed
  slide: nothing dropped, nothing added, nothing repeated, nothing reworded.
  Both halves kind `SKILL N`, same title. 11 proof links, 3 verbatim "Proof
  owed" notes, statuses as harvested (3 PRODUCTION-PROVEN, 9 DEMONSTRATED
  incl. Match DEMONSTRATED — STAGING-PROVEN, 1 DECLARED Meet).
- PLAY 6 paragraphs byte-identical. Advance buttons 41 (40 "Keep reading ◆"
  + 1 "See all my skills ◆" on frame 9). Frame 42 has the Enter anchor
  (`dealAgreeBtn` → https://nayanet.app/) and no Keep-reading button. Zero
  double diamonds.

## Proof 3 — render (Chromium, real Marcellus, via the localhost proxy)

Fonts proven real before trusting any fit number:
`document.fonts.check('25px Marcellus')` true, and "About Shawn Vibert" at
25px measures **226.4px** in Marcellus vs 205.4px in fallback serif (same
numbers as the parent round, both widths). Walked all 42 frames with the
page's own buttons at both widths. Zero horizontal overflow on any frame at
either width. Zero page errors at either width (the one console line is the
known probe artifact: the Google Fonts CSS fails with
ERR_CERT_AUTHORITY_INVALID in this VM; the installed TTFs render instead).
Frame sits whole in the viewport (phone bottom 669/844, desktop 918/1080 —
identical to the agreement source's own numbers). Screenshots in this lane
dir (`FIX-ROUND-SPLIT-shot-phone-*.png`, `FIX-ROUND-SPLIT-shot-desktop-*.png`).

**Desktop 1920×1080: ALL 42 FRAMES WHOLE — ZERO inner scroll on every
frame.** R2 is closed: Skill 8 and Skill 11, which overflowed 30px each in
the filed build, now fit whole (both halves 0px), as do all 26 other skill
halves and all 14 About beats.

**Phone 390×844: the split halves the overflow — but zero inner scroll is
NOT reached on skill frames, and I report that plainly.** Measured
`.frame-scroll` vertical overflow per frame:

| | old (filed 28) | new (split 42) |
|---|---|---|
| Skill A halves (frames 10,12,…,36) | 802–1030px (14 slides) | **310–510px** |
| Skill B halves (frames 11,13,…,37) | — | **196–339px** |
| About beats (frames 1–9, 38–42) | 66–336px | **66–336px — unchanged, no regression** |

Per-skill halves (A / B px): 1: 310/225 · 2: 367/225 · 3: 396/225 ·
4: 367/225 · 5: 396/196 · 6: 424/339 · 7: 453/282 · 8: 396/310 ·
9: 426/283 · 10: 483/283 · 11: 424/339 · 12: 396/196 · 13: 510/253 ·
14: 424/221.

**Why zero is unreachable with the ordered two-frame split — the math, not
an excuse.** The phone reading window (`.frame-scroll` clientHeight) is
330–360px. One skill slide's text is 1,094–1,322px tall, plus a 42px foot
per frame, plus each half's own nutshell gaps. Measured, the total overflow
across each pair is **535–766px** no matter where the split falls — the
best-balanced halves overflow ~268–383px each.
The field-boundary split I shipped is the best split that keeps every field
whole; it lands the B halves inside the About envelope (196–339px vs About
66–336px — Skill 6 B at 339px is 3px over) and the A halves at 310–510px,
of which 12 of 14 sit inside the agreement source's own phone envelope
(28–464px) and two sit just above it (Skill 10 A: 483px; Skill 13 A: 510px).
The reader's experience improves from 2–3 hidden screens per slide to
roughly half a screen to one-and-a-half screens per half — but a skill half
still cuts text mid-field at the fold (frame 10's screenshot shows WHY IT
MATTERS ending mid-sentence, "The login is the first thing anyone…").

**Decision owed — the captain's call, not mine to make.** The brief's proof
item 3 demands zero inner scroll on every skill frame at phone; the ordered
two-frame split cannot meet it. What I can offer, measured, for the next
decision: (a) ACCEPT the envelope — skill halves now scroll no worse than
the frame's own beats do, except Skills 10 A and 13 A; (b) SENTENCE-SPLIT
the WHY field (the brief's own fallback clause) to balance each pair —
predicted halves ~268–383px, all inside the source frame's own envelope
(28–464px) and most inside the About envelope (worst ~383px vs About max
336px), at the cost of splitting one field's argument across two frames; (c) THREE frames
per skill — the only split that could approach zero at phone, but it is not
what was ordered (deck 56, pill N/56); (d) SHORTEN the skill text — edits
settled content, forbidden without his call. I did not decide it, and I did
not hide it.

**Two arithmetic notes on the brief, named plainly.** (1) "3–4 sentences per
frame": each skill carries 12–16 sentences, so two frames hold 6–8 sentences
each at best (A halves: 7–11 sentences; B halves: 4–5). The 3–4 rule cannot
be met by any two-frame split of these texts. (2) The title repeats on both
halves — that is the frame's title element (every beat needs a title), not a
content repetition; the fields' words appear exactly once across the pair.

## Proof 4 — staged link

Verified first-hand above: HTTP 200, 151,375 B, sha256 match, `cmp` clean
against the filed bytes.

## Proof 5 — design-laws checker

`check-design-laws.py` on the built file: **PASS, no machine-checkable
violation, 2 warnings** — the same two §2.2 text-colour eye-checks on
agreement-harvested code as the parent round (the `--tone` inheritance and
`color:transparent`). Eye-checks done by reading the screenshots as a
reader: frames 10, 11, 42 at phone; 10 at desktop. Frames render as the
agreement frame (obsidian, tone rim, topbar face, red N seal, pill, pinned
Back/Next/Keep reading); the `.ib-rows` labels render as plain white caps
text inline — unstyled but readable, not broken (same disclosed observation
as the parent round, a consequence of the One-Build Law).

## Proof 6 — §11 check (in writing)

**Five Gates.** (1) IS IT RIGHT? Yes — the split keeps every word he settled
and uses only the frame's own mechanics; nothing is invented, cut, or added.
(2) IS IT WHAT THEY TRULY NEED? Yes — his eye rejected scrolling skill
slides; the split is his own decision, implemented verbatim, and desktop is
now whole. (3) IS IT MINE TO DO? Yes — the split round is my brief; filing
to the existing branch and staging are inside it; going live is his hand
only, and nothing here goes live. (4) IS NOW THE TIME? Yes — the parent
round went back on this exact render fail; the split is the decided next
step, and the build is deterministic and verified. (5) CAN I PROVE IT? Yes —
every claim above carries its receipt: blob read-back, staged-link `cmp`,
14/14 programmatic content checks, the frame diff read in full, and the
render probe's per-frame numbers at both widths. The one claim I cannot
prove is phone zero-scroll — and I do not claim it; the numbers above are
the proof it is not met.

**Design check (§11).** Could I pick this up? The frame is the agreement
frame, harvested verbatim — obsidian board, tone rim, real shadow, pinned
foot. Where is the light from? Top-left, the frame's own. What is it made
of? Board black inside, white text, own-color light outside. Does it cast a
shadow? Yes, the frame's own. What happens on touch? The frame's own
buttons depress and advance — 42/42 frames walked with the page's own
buttons. Any glow inside? No — the core is board black, as harvested. Any
gray text? No — `gray`: 0. Any text under 17? No — the frame's own scale,
unchanged. Two same colors together? No — tones cycle by deck position,
never twice in a row. Anything flat or dead? No — the frame is alive as
harvested. Can I see what the icon IS? Yes — the topbar face, the N seal,
the jewel. **Reference object named:** the agreement frame itself, measured
against the three reference objects — the top-left + button, the Smart Note
board (the board and the black), and the X button (the inside). This round
changed no object, only which words sit in the frame's text beats.

**Sense check (think for myself).** Is it logical? Yes — the split is the
only ordered option that keeps his words. Sensible? Yes — each half reads
as a complete mini-block (what it is + why it matters, then what makes it
different + the example + what's in it for you + proof). Intelligent? The
uniform split point is the measured optimum for whole fields; the
sentence-split alternative would balance the numbers better but break an
argument across frames — I kept fields whole and named the trade-off with
numbers instead of deciding it silently. Am I doubling up? No — each field
appears exactly once across its pair; the repeated title is the frame's own
element, and I say so. In his best interest? The desktop is now whole and
the phone is roughly twice as readable; the remaining phone scroll is
reported with its exact numbers and its next decision, not smoothed over.

**Inventory check (the Inventory Law — know every part, check it's all
there).** All 42 frames inventoried: 14 About beats (verbatim), 28 skill
halves (14 skills × 2, fields verbatim), 11 proof links, 3 "Proof owed"
notes, 41 advance buttons (40 Keep reading + 1 See all my skills), 1 Enter
anchor, pill N/42, PLAY 6 paragraphs, 7 scripts, no additions. Every part
checked against the filed build and the agreement source; nothing missing,
nothing extra.

## Deviations from the brief, named plainly

1. **Proof item 3 (phone zero inner scroll on skill frames) is NOT met.**
   See Proof 3 above — the numbers, the math, and the decision owed. This
   is the same honesty as the parent round: the split is built and proven;
   the standard it was meant to meet is not reached at phone width.
2. **Pill reads "N / 42", not "N / 14".** As the brief orders (deck 42).
3. **Title repeats on both halves** of each skill — the frame's title
   element; fields' words appear once. (See the arithmetic notes in Proof 3.)
4. **"3–4 sentences per frame" is not met** — 12–16 sentences per skill
   cannot fit two frames at 3–4 each. (See Proof 3.)
5. Carried over unchanged from the parent round (disclosed there, still
   true): **`.ib-rows` / `.ib-row-k` labels are unstyled** (no CSS for them
   in the agreement source); **wirePlay aria-labels still say "read the
   agreement with Naya"** (harvested player chrome, wording not invented);
   **dead `article[data-beat="37"]` phone rule kept byte-identical** (inert).

## Still owed (not mine to decide)

- **Phone zero-scroll** — the captain's call (accept the envelope,
  sentence-split WHY, three frames per skill, or shorten). My numbers for
  option (b) are predictions from measured heights, not a build.
- **Portrait decision** (Naya's face / Shawn's photo / monogram) awaits
  Shawn. The agreement's face-*.jpg are used verbatim, exactly as the
  frame does.
- **wirePlay aria-labels** (item 5 above).

## Files in this lane dir (this round, prefix FIX-ROUND-SPLIT-)

- `FIX-ROUND-SPLIT-BRIEF.md` · `FIX-ROUND-SPLIT-MAKER-REPORT.md` (this file)
  · `FIX-ROUND-SPLIT-frame.diff` · `FIX-ROUND-SPLIT-verify-split.cjs`
  · `FIX-ROUND-SPLIT-render-probe.py` · `FIX-ROUND-SPLIT-measure.py`
  · `FIX-ROUND-SPLIT-file-page.cjs`
  · `FIX-ROUND-SPLIT-shot-phone-*.png` / `FIX-ROUND-SPLIT-shot-desktop-*.png`
  (render evidence) · `measure-split-phone.json` (parent round's per-field
  heights — the split's evidence base)
- Modified in place: `build-about-skills-frame.cjs` (split build, filed),
  `about-skills.html` (42 frames, filed).
