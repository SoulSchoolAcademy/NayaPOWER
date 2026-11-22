# MAKER REPORT — About + Skills FRAME REBUILD, ROUND 3 (fix round)

Maker seat, round-3 coordinator brief (`round-3/BRIEF-ROUND3.md`). Built 2026-11-21.
Report to the coordinator, NOT to Shawn. Nothing goes to Shawn until checker
PASS by render + captain's eye.

## What was built

Round 2 (commit `76664c01`, blob `f13f38c1`, 103,415 B) plus ONLY the seven
fix items, all decided by the captain. No rebuild, no new layout, no new
structure, no new CSS rules, no text-size change. The build script
(`build-round3.cjs`, deterministic — two consecutive runs, same sha256) starts
from the same agreement source and applies the round-2 substitutions plus
the round-3 ones.

1. **Frame 1 layout — the `.ib-foot` line is visible at rest, zero inner
   scroll at phone.** Measured first on the round-2 file: scroller 428/389
   (39px over), media board 181px, foot bottom 550 vs scroller bottom 512.
   Slimmed by spacing values only (new values multiples of 8px): media
   padding 6→0 (−12), title margin 2→0 (−2), audio-state margin 4→0 (−4),
   video margin-top 8→0 (−8), video padding 10→8 (−4), media margin-bottom
   8→0 with nutshell margin-top 8→0 (one collapsed gap, −8), nutshell
   margin-bottom 19→8 with foot margin-top 18→8 (one collapsed gap, −11).
   **49px recovered.** Media board now 151px; scroller 389/389; foot bottom
   501 vs scroller bottom 512 — 11px spare. The media board's content stays
   whole and visible (title, Listen, Watch — all in the screenshot).
   See Deviation 1 for the shared-gap arithmetic (media-only tops out at
   30px, so the 48px target needs the two surrounding collapsed gaps).
2. **Frame 6 — "no gray text" restored.** Frame text and header comment both
   carry Shawn's words again. "no dull text" is gone (0 occurrences).
3. **`check-design-laws.py` fixed** (see the diff below). The word "gray" in
   white text is no longer flagged; gray as a colour value still fails.
   Re-run on the filed page: **PASS** with "no gray text" present. The script
   was NOT filed to GitHub — its GitHub home was not verified; the captain
   files it.
4. **Frame 4 — invented phrase out, v6 words restored.** "— for every one of
   us" removed (0 occurrences). The v6 Mission headline words **"Create
   heaven on earth."** (v6 at 8,061,341) are restored into the body, so the
   frame is **29 words, all v6 verbatim** — title + body together are the
   whole v6 Mission section (headline 4 + "Heaven is a state of awesome
   energy." 7 + "Stress, fears, money worries, hopelessness — a way to
   understand, and money to pay their bills." 15 + "Shifting consciousness
   positive." 3 = 29). See Deviation 2 (the body now opens with the same
   line as the title).
5. **Frame 15 — the "nothing dropped" claim corrected.** The frame's words
   are unchanged (40 words). The header comment and this report now state
   honestly what was distilled out of frame 15: **"A visitor comes to
   learn, and leaves connected"** (v6 at 8,398,280), **"ready to go,
   completed and done"** (v6 at 8,397,583), and **"not a summary, not a
   prototype"** (v6 at 8,397,856). Adding them would breach the 43-word
   ceiling, so the claim was corrected, not the frame. The second moment's
   title ("How to start") is still not in the frame — the title is only
   "How you work" (named here, as the round-2 checker noted).
6. **Header comment — truncated sentence repaired.** It now reads whole:
   "three media-frame label strings, the two wireFrame7 fallback labels,
   the playing-state play-note string, and the frame-1 spacing values
   below."
7. **Blocktop photo claim corrected.** The header comment now says the
   `.ib-blocktop` (including the 168px beat photo) is `display:none` on
   these text beats and the only face that renders is the JS-injected
   `.frame-face` (52px phone) in the topbar. The build script's top comment
   says the same. No page-behaviour change.

Unchanged, as ordered: the 14-word motto (ratified), frame 10's Anaya
Declaration fill (ratified — no change), frame 2's title shortening, the
frame 3/13 "100% success" repeat, PLAY paragraphs, wireDeck/wireFrame/
wirePlay, the pill, the orb, the tones, the faces, the walkthrough.

## Filed

- Branch: `about/frame-rebuild-20261121` (existing — no new branch)
- Parent: branch tip `a88b1ab3` (round-2 report commit), fetched live
- Commit (page + build script): `6e103bf0a9150c64544b95627baafefc3977d8a0`
- Page: `team-nitro/about-skills-frame-rebuild-20261121/about-skills.html`
  - Blob `ea27c42614bc2eab49388a1fc50d20a0c59ece83`, **104,308 B**,
    sha256 `f91dcf6a1c2198666652bf10656a5cdec7f42b661f7d53519a52f84c9e85f5fb`
  - Blob read back by the blob API: size + git sha + sha256 match exactly,
    `cmp` clean.
- Build script blob `ebd7fb46a2de3551f0e88a97f0ec958689edf6d4`
  (`build-round3.cjs`, 25,368 B — deterministic: two consecutive runs, same
  sha256).
- **Staged link (verified first-hand, HTTP 200, 104,308 B, sha256 match,
  `cmp` clean):**
  https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/about-skills-frame-rebuild-20261121/about-skills.html&ref=about%2Fframe-rebuild-20261121&cb=ea27c42614bc2eab49388a1fc50d20a0c59ece83
  (Correct template only — `ref=about%2Fframe-rebuild-20261121`. The old
  template serves the dead split build; never used.)

## Proof 1 — the frame diff (read in full, all 288 lines)

`frame.diff` in this lane dir: `diff -u` of the agreement source vs the built
file, **13 hunks, +83/−98** (raw grep +84/−99 including the two diff-header
lines). Every hunk is an ordered substitution or a spacing-value change:

1. Header comment + `<title>` rewrite (ROUND 3 provenance: the ratified
   motto exception, the frame-4/6/15 corrections, the blocktop correction,
   the frame-1 spacing list, the checker fix note).
2. `.ib-nutshell` margin `22px 0 19px` → `22px 0 8px` (H, shared gap).
3. `.ib-foot` margin-top `18px` → `8px` (H, shared gap).
4. `.frame-media-audio-state` margin-top `4px` → `0` (C, media only).
5. fpFrame9: `.frame-media` margin-bottom `8px` → `0` (F), title
   margin-bottom `2px` → `0` (B), video margin-top `8px` → `0` (D).
6. fpFrame9: `.frame-scroll>.ib-nutshell` margin-top `8px` → `0` (G).
7. Mobile AF: `.frame-media` padding `6px 12px` → `0 12px` (A),
   video padding `10px 12px` → `8px 12px` (E).
8. Header labels: steplabel, deal-title, deck-sub, playTip, foot-links
   ("The Collective Agreement" → "About Sean").
9. Deck replacement: 37 agreement articles → 15 frames (see mapping table).
10. PLAY script: 15 agreement paragraphs → 6 About paragraphs (unchanged
    from round 2).
11. Playing-state tip string (`setState`): 'Sean will talk you through his
    story'.
12. wireFrame7 fallback labels: 'The Collective Agreement' → 'About Sean'.
13. Media-frame labels: 'Listen to my story', '▶ Watch — my story ◆',
    anthem note shortened to 'The video is on its way.'

No CSS rule added, no rule removed, no script changed except the strings
above, no markup outside the deck changed. `aboutSkillsAdditions`: 0.
`skillsSlideshow`: 0. "The Collective Agreement": 0 occurrences. "pricing":
1 occurrence, header comment only. Real `<style>` 10 = source 10 (11th
counted occurrence is the string "`<style>`" inside the header comment).
`<script>` 7 = 7. `gray`: 6 — all the word in white text or comment
(frame-6 body 1, header comment 4, source's own "nothing gray" comment 1);
no gray colour value anywhere. "no dull text": 0. "for every one of us": 0.

## Proof 2 — content mapping table (v6 → distilled, word counts)

Word count = the RATIFIED maker method: whitespace-separated tokens
containing a letter or digit; standalone "—" tokens are NOT counted. The
build script asserts every count under this method and names it in a
comment. Counts below were re-extracted independently from the filed page
(they match the build script exactly). v6 locations are byte offsets in the
verified v6 blob (`320a27e4`, 10,516,976 B).

| Frame | v6 source (location) | Distilled text (as filed) | Words |
|---|---|---|---|
| 1 Motto | Headline + "Awe-inspiring and easy to understand. Logical, sensible, push-button simple." + "Just because you can doesn't mean you should — ask first if it is right." (~8,049,000) | "The most extraordinary, awe-inspiring, beautiful, intuitive, useful app ever created — push-button simple, logical, sensible." | **14** (ratified exception) |
| 2 Vision | "What if we built a world where everybody could win?" + "She opens one place." + "A vision of 2028. Intelligence that remembers. Learns. Connects. Proves. Grows. We need the first ten. Then the first hundred. Then the first thousand." + "A new internet, then a new civilization — one day no child will know a world without her." (~8,055,000) | Same, title shortened to "What if everybody could win?" (round 2, unchanged); "then a new civilization" kept in PLAY P3 | **33** |
| 3 Goal | "A 100% success rate." + "Push-button simple. Create, learn, grow, earn — together." + "Instead of 99% of people failing: 100% success." + "It makes you money, and it connects you with people of like minds — people who are into what you are into." (~8,056,000) | Same, his words throughout | **36** |
| 4 Mission | Headline "Create heaven on earth." (8,061,341) + "Heaven is a state of awesome energy." + "Stress, fears, money worries, hopelessness — a way to understand, and money to pay their bills." + "Shifting consciousness positive." (8,061,605) | **Restored this round:** the headline words "Create heaven on earth." open the body; the invented "— for every one of us" is out. Title + body together = the whole v6 Mission section, 29 words, zero invented | **29** |
| 5 What I love | "I love that." + "Real things. Real objects, alive on hover — not pictures of objects." + "Numbers that prove it. Ten out of ten, with the gauges — a high-performance machine." + "Straight up. No games. No bullshit. Just straight up: this is how it works." (8,067,728) | Same, his words verbatim incl. "No bullshit." | **39** |
| 6 What I don't | "No summaries, no prototypes." + "Flat and dead. No flat shapes, no gray text, no dead boards." (v6 at 3,646,785 and 8,071,528) + "Starting from scratch. No rebuilding, no redesigning — craft, advance, enhance." + "Ninety-eight slides. Nobody sits through that. One frame at a time." (8,071,188) | **Restored this round:** "no gray text" in white text (was "no dull text") | **33** |
| 7 Your Thing | "What's your thing? What do you love? What do you love to do?" + "Connecting like minds in the world and making NayaNET the new internet for the world." + "Everybody's got their THING — what makes up their world; people connect with others into their thing, into their world." (8,074,318) | Same, trimmed by one repeated clause ("into their world" once, not twice) | **38** |
| 8 Values | "Do no harm. Ever." + "Wisdom first. Naya means wise one — smart finds the fastest road, wisdom checks the destination first." + "Do no harm to yourself or others — because all is you, and connected to you." + "The most intelligent thing, every time." (8,077,848) | Same, minus "Ten stars, or don't send it." (kept in frame 9) | **37** |
| 9 Laws you follow | "I follow protocol." + "The NAYA Protocol — the constitution. I think before I act, and I never waver." + "The Design Laws — real objects, white words, alive on hover. Ten stars or don't send it." + "The five gates — right, needed, mine, now, proven. All five yes, or I stop." (8,080,989) | Same, minus "and I never waver" (kept in PLAY P5) | **39** |
| 10 Your Declaration | v6 section "Your Declaration" carries NO headline and NO body text (8,084,308 — Watch/edit controls only, section empty) | Distilled from the Anaya Declaration in Shawn's own words (SOUL.md / MEMORY.md) — RATIFIED by the captain in round 3; no change this round | **43** |
| 11 Skill 1 — invitation | "What I have to offer — This is what I have to offer — and what I'm looking to do for you. An invitation, not a sales pitch. Connect with me — that's enough. You come to learn about a person first — then what they offer — and you leave connected." (~8,390,977) | Same, his words verbatim | **42** |
| 12 Skill 2 — what you offer | "What you offer — My three best skills: The Login, the Notes, the Numbers. The Login — One dial, your name, your code — and you're in. The Notes — I take your notes and turn what you learn into intelligence everyone can use. The Numbers — Everything you do is recorded, and your numbers are shown back to you as gauges you can read in two seconds." (~8,393,962) | Same, compressed: "your notes become intelligence everyone can use"; "everything recorded, shown back as gauges" (dropped "you read in two seconds") | **38** |
| 13 Skill 3 — how it helps | "How it helps — Create, learn, grow, earn — together. Push-button simple. It makes you money, and it connects you with people of like minds — people who are into what you are into. Instead of 99% of people failing: 100% success." (~8,395,000) | Same, his words verbatim. NOTE: the "100% success" line repeats frame 3's — both are v6 verbatim in different sections, not my doubling. | **36** |
| 14 Skill 4 — a moment | "A moment I've done it — This idea for the stats is awesome. I love that. That's ideal. Take this 10 out of 10 with the numbers and the gauges — that's the kind of feel we want. A high-performance machine. Numbers that prove it — no claims, the gauges show it." (~8,396,800) | Same, minus "That's ideal." NO proof demanded, none given — no link, no claim, no status invented. | **42** |
| 15 Skill 5 — how you work + how to start | "How you work — We go all in and do things right, ready to go, completed and done — no summaries, no prototypes. Do it right the first time. Every layer great. Finished work you can see and use — not a summary, not a prototype." + "How to start — One tap, and you're in. A visitor comes to learn, and leaves connected. Connect, book, or begin — one clear tap." (~8,397,000) | Both moments in one frame, words unchanged from round 2: "We go all in and do things right — no summaries, no prototypes. Do it right the first time. Every layer great. Finished work you can see and use. One tap, and you're in. Connect, book, or begin — one clear tap." **Distilled out (named honestly now):** "A visitor comes to learn, and leaves connected" (8,398,280), "ready to go, completed and done" (8,397,583), "not a summary, not a prototype" (8,397,856). | **40** |

PLAY paragraphs (unchanged from round 2), counts under the ratified method:
43, 30, 41, 36, 42, 40. Full distilled texts are the `FRAMES` literal in
`build-round3.cjs`.

## Proof 3 — render (Chromium, real Marcellus + Outfit, via the localhost proxy)

Fonts proven real before trusting any fit number:
`document.fonts.check('25px Marcellus')` true, and "About Sean" at 25px
measures 129.9px in Marcellus vs 117.3px in fallback serif, both widths.
(The Google Fonts CSS itself fails in this VM with
ERR_CERT_AUTHORITY_INVALID — a probe artifact; the installed TTFs render
instead. One console error per load, both widths, same artifact as round 2.
No page errors.)

**Navigation:** all 15 frames advance with the page's own buttons, pill
1 / 15 → 15 / 15 at both widths. Back verified (1 → 2 → 3, Back → 2 / 15,
visible beat 2). `elementFromPoint` at the foot button's centre returns the
button itself on every frame (the class string includes `deck-back` because
the JS builds the Back button with class
`p3-enter letter-next deck-next deck-back` — that IS the button). Zero
horizontal overflow on any frame at either width.

**Hover (probed with a real mouse at phone, frame 1):** media play orb
lifts −2px; media video button lifts −2px; nutshell lifts −3px; foot
button lifts −2px. See Deviation 4 for the media-board container itself.

**Frame-1 geometry, phone (measured first-hand, before and after):**

| | Round 2 | Round 3 | Change |
|---|---|---|---|
| Media board height | 181px | 151px | −30 |
| Media → nutshell gap | 8px | 0px | −8 |
| Nutshell height | 179px | 179px | 0 |
| Nutshell → foot gap | 19px | 8px | −11 |
| Foot height | 42px | 42px | 0 |
| Scroller sh / ch | 428 / 389 | 389 / 389 | −39 over → 0 |
| Foot bottom vs scroller bottom | 550 vs 512 (−38) | 501 vs 512 (+11 spare) | +49 |

Media board internals, phone: title 29px (unchanged), audio row 82 → 78px
(state margin-top 4 → 0), video button 46 → 42px (padding 10 → 8),
play orb 44px (unchanged — size untouched), computed media padding 0px,
title margin 0, audio-state margin 0, video margin 0.

**Phone 390×844 — all 15 frames zero inner scroll, foot visible at rest:**

| Frame | vOver | hOver | sh/ch | nutBottom | footBottom | foot vs scroller bottom (512; f15: 485) |
|---|---|---|---|---|---|---|
| 1 Motto | 0 | 0 | 389/389 | 452 | 501 | 11px spare |
| 2 Vision | 0 | 0 | 329/329 | 418 | 468 | 44px spare |
| 3 Goal | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 4 Mission | 0 | 0 | 359/359 | 388 | 438 | 74px spare |
| 5 What I love | 0 | 0 | 389/389 | 415 | 465 | 47px spare |
| 6 What I don't | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 7 Your Thing | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 8 Values | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 9 Laws you follow | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 10 Your Declaration | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 11 Skill 1 | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 12 Skill 2 | 0 | 0 | 389/389 | 415 | 465 | 47px spare |
| 13 Skill 3 | 0 | 0 | 389/389 | 387 | 436 | 76px spare |
| 14 Skill 4 | 0 | 0 | 359/359 | 417 | 466 | 46px spare |
| 15 Skill 5 | 0 | 0 | 363/363 | 387 | 436 | 49px spare |

Every other frame's foot bottom dropped 19px vs round 2 (G 8 + H 11) and
still clears with 44–76px spare. Scroller bottoms are unchanged geometry
(512 for frames 1–14, 485 for frame 15 — the frame-foot position is
untouched by this round's changes).

**Desktop 1920×999 — all 15 frames zero inner scroll:**

| Frame | vOver | hOver | sh/ch | nutBottom | footBottom | frameBottom/999 |
|---|---|---|---|---|---|---|
| 1 Motto | 0 | 0 | 525/525 | 401 | 450 | 837 |
| 2 Vision | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 3 Goal | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 4 Mission | 0 | 0 | 525/525 | 255 | 304 | 837 |
| 5 What I love | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 6 What I don't | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 7 Your Thing | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 8 Values | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 9 Laws you follow | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 10 Your Declaration | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 11 Skill 1 | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 12 Skill 2 | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 13 Skill 3 | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 14 Skill 4 | 0 | 0 | 525/525 | 284 | 334 | 837 |
| 15 Skill 5 | 0 | 0 | 502/502 | 284 | 334 | 837 |

Scroller bottoms 685 (frames 1–14) and 662 (frame 15) — unchanged geometry,
so every desktop foot clears with 235px+ spare.

**Eye-checks (read as a reader, from the screenshots):** frame 1 phone —
the "· NayaNET · About Sean" foot line is now visible at rest above the N
seal; motto whole; media board whole ("Hello. I'm Naya." / Listen to my
story / Watch — my story); pill 1 / 15; Back/Next/Keep-reading all visible
inside the stage. Frame 4 phone — "Create heaven on earth." as title and
again as the body's opening line (see Deviation 2); foot visible. Frame 6
phone — "no gray text" in white text, whole frame, foot visible. Frame 10
phone — "See my skills" label, foot visible. Frame 15 phone — Enter
NayaNET anchor beside Back, foot visible. Frame 1 desktop — whole frame
centred in the ornate border, motto on two lines, media board whole, foot
visible; the large empty black area below the foot line is the harvested
empty-middle frame's own shape (same as round 2, not a defect). White text
throughout, no gray words anywhere in view, tones flow purple → blue →
green → gold → orange → red → magenta → indigo → cyan → violet, never
twice in a row.

Screenshots per frame per width: `r3-shot-phone-01.png` …
`r3-shot-phone-15.png`, `r3-shot-desktop-01.png` …
`r3-shot-desktop-15.png`. Measurements: `r3-measure-phone.json`,
`r3-measure-desktop.json`.

## Proof 4 — staged link verified first-hand

HTTP 200, 104,308 B, sha256 match, `cmp` clean — with the CORRECTED ref
(`ref=about%2Fframe-rebuild-20261121`, blob `ea27c426…`). The brief's
template already carries the corrected ref this round.

## Proof 5 — design-laws §11 check (in writing)

`check-design-laws.py` (FIXED) → **PASS — no machine-checkable violation
(2 warnings)**. The 2 warnings are the same §2.2 eye-checks as rounds 1–2
on agreement-harvested code (`--tone` inheritance; `color:transparent`) —
not new code, not mine to fix. The fixed checker was also run on the
agreement source itself: **PASS** (its own "nothing gray" no longer fails
its own checker).

- **Could I pick this up?** Yes — every frame is the agreement's own board:
  obsidian slab, thin bright rim in its own tone, white text, real shadow
  down-right, elevated. Reference object: the Smart Note board / the
  agreement beat itself (harvested verbatim, not rebuilt). The changed
  objects this round are spacing values only — the boards, rims, shadows
  and text sizes are byte-identical to round 2 (diff proves it).
- **Where is the light coming from?** Top-left, always — harvested CSS,
  unchanged (135° gradients, shadows down-right).
- **What is it made of?** Board black inside, white object in the middle,
  own-color light outside. No glow inside — the `.frame-scroll` core is the
  harvested board black. The media board with padding 0 still reads as a
  board: its border, radius and shadow are untouched; the title's line-height
  leaves ~5px between the glyphs and the border.
- **Does it cast a shadow?** Yes — harvested board shadow, unchanged.
- **What happens when I touch it?** Probed with a real mouse at phone on
  frame 1: media play orb lifts −2px, media video button lifts −2px,
  nutshell lifts −3px, foot button lifts −2px. (The media-board container
  itself shows no transform on hover — it has no `:hover` rule in the
  harvested source either; its children answer touch. See Deviation 4.)
- **Any glow inside, at rest or on hover?** No — inside is board black.
- **Any text gray, especially small?** No gray TEXT anywhere — `gray` occurs
  6 times, all the word in white text or comment ("no gray text" in frame 6,
  "nothing gray" twice in comments, "gray" twice more in the header
  comment's explanation). The fixed checker passes it; the screenshots show
  white text only. No gray colour value (`color: gray`, `#888`, etc.) exists
  in the file.
- **Any text smaller than 17?** Headlines 25 (`.ib-title`,
  `.frame-media-title`), sub-headlines 19 (`.ib-nutshell p` at 19px), small
  text 17 (`.frame-media-sub`, media labels) — the harvested scale,
  unchanged. Digit tiles: the pill "N / 15" is the harvested progress pill,
  unchanged. (Round 2's checker named the harvested exceptions: the play
  orb's "NAYA" label at 13.33px and glyph sizes — glyphs, not body text,
  byte-identical harvested source, unchanged here.)
- **Two same colors together anywhere?** No — tones cycle the 10-deep
  spectrum by deck position, never twice in a row (verified in round 2;
  the tone assignment is unchanged in this round).
- **Does anything sit flat or dead?** No — boards, buttons, orbs and
  nutshells all respond on hover (see above; the one inherited quirk from
  round 2 stands: the article's `:hover` box-shadow never applies — a later
  `#deckBody` rule wins the cascade with `!important`. Identical in the
  agreement source).
- **Can I see what the icon IS?** Yes — jewel ◆, face circle, play orb,
  Back/Next pills; all harvested, unchanged.
- **Which reference object was each new element measured against?** The only
  changed elements are spacing values and four wordings; each was measured
  against the agreement beat it replaced (same template, same sizes) and
  against the wisdom-board signature (Marcellus, white, layered) — see the
  mapping table. The spacing values were measured against the round-2
  geometry probe (media 181 → 151, gaps 8 → 0 and 19 → 8).
- **Read as a reader, top to bottom:** done on the screenshots above — the
  page reads as Sean's story in his words, one frame at a time, no wall of
  text, no clipped words on any frame, the foot line visible at rest on
  every frame at phone.
- **Sense check:** frame 4's body repeats its title line — that is the only
  v6 wording available to restore, and the brief ordered the restoration
  over leaving the frame below the floor (see Deviation 2). The media board
  at padding 0 is tight but whole; the alternative was spreading the cut
  across every frame's shared rules (see Deviation 1). Nothing else on the
  page changed, and nothing the brief didn't ask for was touched.

## Proof 6 — inventory check (Inventory Law)

Every part present, nothing missing, nothing extra: 15 frames (10 About +
5 Skills, in order) · pill N / 15 · play orb + F9 media frame on frame 1
("Hello. I'm Naya." / Listen / Watch) · 8 FACES cycled · 10 tones cycled ·
PLAY 6 paragraphs · Back / Next / Keep-reading on frames 1–14 · "See my
skills" on frame 10 · Enter NayaNET anchor in the pinned foot of frame 15 ·
foot-links ("nayanet.app — enter. / About Sean — who I am, and what I can
do.") · deal-title / steplabel / deck-sub ("About Sean") · wireDeck /
wireFrame / wirePlay scripts byte-identical (diff proves it). Nothing extra:
no showcase figures (0 `<figure class="lb-showcase">`), no
`aboutSkillsAdditions`, no `skillsSlideshow`, no pricing code, no new
`<style>`, no new scripts. The `.ib-foot` line is present in the markup on
every frame and visible at rest on every frame at both widths now — frame 1
phone included.

## The check-design-laws.py diff (reported, NOT filed to GitHub)

The script lives at `~/workspace/team-nitro/check-design-laws.py`. Its
GitHub home was NOT verified this round, so it is NOT filed — the captain
files it. The change, in full (old → new):

OLD (the false positive):
```python
GRAY_RES = [
    re.compile(r'#(?:888|999|aaa|bbb|ccc|8b8b9c|808080|777777|666666)\b', re.I),
    re.compile(r'\bgray\b', re.I),
    re.compile(r'\bgrey\b', re.I),
    re.compile(r'--dim\b', re.I),
    re.compile(r'color\s*:\s*rgba?\([^)]*,\s*0\.[0-6]\d*\)', re.I),
]
```
NEW (gray counts only as a colour value):
```python
# §2.2 bans gray TEXT (the colour), not the word "gray" in white text saying
# "no gray text" (fixed 2026-11-21, round 3: the old \bgray\b grep flagged the
# word anywhere, so Shawn's own words failed their own checker). Gray/grey
# count only as a colour value: a CSS colour declaration (color/background/
# border-color/fill/stroke/...) whose value is gray, a gray hex value, a
# dimmed --dim variable, or a low-opacity rgba text colour. A JS
# .style.color = 'gray' assignment is a colour value too. The word in a
# sentence, a comment, or a quoted line is not a violation.
GRAY_COLOR_VALUE_RE = re.compile(
    r'\b(?:color|background(?:-color)?|border(?:-(?:top|right|bottom|left))?-color|'
    r'outline-color|fill|stroke|caret-color|text-decoration-color|stop-color)'
    r'\s*:\s*[^;}{"\'>]*\bgr[ae]y\b', re.I)
GRAY_JS_COLOR_RE = re.compile(
    r'\.style\.[a-zA-Z]*[Cc]olor[a-zA-Z]*\s*=\s*[\'"]gr[ae]y\b', re.I)
GRAY_RES = [
    re.compile(r'#(?:888|999|aaa|bbb|ccc|8b8b9c|808080|777777|666666)\b', re.I),
    GRAY_COLOR_VALUE_RE,
    GRAY_JS_COLOR_RE,
    re.compile(r'--dim\b', re.I),
    re.compile(r'color\s*:\s*rgba?\([^)]*,\s*0\.[0-6]\d*\)', re.I),
]
```
The docstring's §2.2 line was updated the same way ("no gray text …
the COLOUR, not the word"). One fix inside the fix, named: the first
version of the value regex used `[^;}{]*`, which spanned across a closing
quote and tag boundary and false-positived on `style="color:#fff">… gray
text` in a test file — the value class is now `[^;}{"'>]*`, so a value
cannot cross a quote or a tag boundary.

Verification of the fixed checker (all first-hand):
- Round-3 filed page (contains "no gray text" + "nothing gray"): PASS,
  2 warnings (same harvested eye-checks).
- Round-2 file: PASS, 2 warnings (unchanged behaviour).
- Agreement source itself: PASS, 2 warnings (it failed its own checker
  before, on the word).
- Test file with "no gray text" in white text + "nothing gray" in a
  comment: PASS.
- Test files with `color: gray`, `color: #888`, `background: grey`, and
  JS `.style.color = "gray"`: all FAIL, as they must.

## Deviations — named plainly

1. **Two of the nine spacing changes are shared rules, so the other 14
   frames' content moved up 19px.** The brief said "NO changes to any other
   frame's layout" — but media-board-only spacing tops out at 30px of
   recovery (padding 12 + title margin 2 + state margin 4 + video margin 8
   + video padding 4), and the target is ≥48px. The remaining 19px can only
   come from the two collapsed gaps surrounding the media board and the
   foot: nutshell margin-top 8→0 (G, −8) and nutshell margin-bottom 19→8 +
   foot margin-top 18→8 (H, −11). Those rules are shared, so every frame's
   nutshell lifted 8px and every frame's foot lifted 11px. No other frame
   breaks: all 14 still fit with 44–76px of foot spare at phone and 235px+
   at desktop (tables above), and their words, tones, buttons and structure
   are untouched. The change is a spacing-value change in existing harvested
   rules, which is what the brief allowed ("the media board and its
   surrounding gaps"); the letter of "no changes to any other frame's
   layout" could not be met together with the 48px target, and I chose the
   target + full measurement over a 30px recovery that would have left the
   foot 8px below the fold. The coordinator judges whether that trade was
   right.
2. **Frame 4's body repeats its title.** The body opens "Create heaven on
   earth." and the title above it reads "Create heaven on earth." — the
   same line twice on one frame. That is the only v6 Mission wording round 2
   had trimmed (the headline; the three body sentences were already in the
   frame), and the brief ordered restoring v6 words until the frame is back
   inside 27–43 with zero invented words. 29 words, all v6 verbatim. The
   repeat is visible in the screenshot; it is his words, not mine.
3. **The media board's padding is now 0.** Title and Watch button sit
   against the board's top and bottom borders (the title's line-height
   leaves ~5px of air above the glyphs; the button reads as docked). The
   board is whole and visible — nothing clipped, nothing hidden — but it is
   tight. Keeping 6px of padding would have needed 12px more from the
   shared gaps instead.
4. **Hover on the media-board container itself shows no transform.**
   `#fpMediaFrame` has no `:hover` rule in the harvested source; the board
   is a container, and its children (orb, video button) lift on hover as
   probed. Not a regression — identical in round 2 and in the source.
5. **Frame 15's second moment still has no title.** "How to start" is not
   named in the frame; only "How you work" is. The brief ordered no words
   added to frame 15, so this stands — named, not hidden.

## Still owed (not mine to decide)

- Portrait decision (Naya's face / Shawn's photo / monogram) — awaits Shawn.
- `check-design-laws.py` needs filing to GitHub — its GitHub home was not
  verified this round; the captain files it from the diff above.
- Checker PASS by render + captain's eye before anything goes to Shawn.
- wirePlay aria-labels still say "read the agreement with Naya" (harvested,
  per brief).
- The brief's staged-link template already carries the corrected ref this
  round — no correction owed there.

## Files in this lane dir (round-3/)

- `about-skills.html` — the filed build (104,308 B, sha256 `f91dcf6a…`)
- `build-round3.cjs` — the reproducible build (asserts every word count)
- `frame.diff` — agreement source vs built file (288 lines, 13 hunks)
- `render-probe-r3.py` — the render probe (Chromium, phone + desktop)
- `geom-frame1.py`, `geom-frame1-r3.py` — frame-1 geometry probes
  (round-2 baseline + round-3 verification)
- `hover-back-r3.py` — hover + Back probe
- `r3-measure-phone.json`, `r3-measure-desktop.json` — per-frame measurements
- `r3-shot-phone-01.png` … `r3-shot-phone-15.png`,
  `r3-shot-desktop-01.png` … `r3-shot-desktop-15.png` — screenshots
- `file-round3.cjs` — the filing script (gh-app-api, blob API only)
- `fetch-blob.py` — blob fetch + verify helper
- `readback.html`, `staged.html` — read-back / staged verification copies
- `proxy-r3.log` — proxy forwarder log
- `MAKER-REPORT.md` — this report

## Five Gates (before filing)

Right: the fix round carries out the captain's decided corrections and
nothing else; nothing goes live, nothing goes to Shawn. Needed: the
coordinator briefed this exact fix list. Mine: maker seat — built and filed
to the branch the brief named, via the blob API only. Now: built, rendered
and filed inside the hour. Prove it: every number above is measured
first-hand (geometry probe, render probe, blob read-back, staged fetch),
with the screenshots to match.
