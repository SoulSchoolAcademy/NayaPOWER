# The Ten's Formatting — The Pattern to Copy Everywhere

SN-2472 · DESIGN / THE PATTERN

**Created:** 2026-11-09 04:42Z

**Source:** Shawn's eye on live v69 (the Ten fix), 04:41Z — "it looks super sick... with the orbs and the color of the way they light up, and you did each one of them lighting up the different coloring makes it easy to read now — that's some high level stuff. So you want to make notes on that and copy that formatting for other places in the future." The pattern is the v69 One Ultimate Ten, artifact `pricing-chart-viewpoint` v69 (live site still v68 at time of writing).

## Hook

The Ten's new formatting is the pattern now: every part in its own raised inner block, each block lit in its own color, the copy broken into orb bullets — and a stranger can read it at a glance. His verdict: "super sick... high level stuff." This note writes the pattern down exactly, so every future section is built from it instead of inventing its own.

## Nutshell

The pattern, as built in v69 (Ten fix seat, verified at source level — word-preservation IDENTICAL, diff-scope Ten only, "blockchain" 0×):

- **Three inner blocks per item.** Why this happens / The solution / What's in it for you — each one lives in its own elevated inner block, in the letter beats' obsidian grammar: 165° gradient, top-left light, rim and glow in the item's digit colour. Each block lifts and lights up on hover/focus, so the eye reads one part at a time and the parts separate from each other.
- **A jewel tile opens each block.** A raised `.os-jewel` tile in the item's colour, carrying its glyph (?, ✦, ★) and its label. 30 part jewels across the Ten (3 × 10). The jewel is the signpost: it tells the eye what kind of sentence follows before a word is read.
- **The copy is broken into orb bullets.** 84 bullets across the Ten, on the letter's 11px living orbs — genuinely circling, luminous, aligned. No wall of text anywhere. No paragraph runs long.
- **Her face is doubled.** 108px → 216px desktop; 124px on phone, centred on its own grid row above a full-width title so nothing squeezes at 390px or 360px. The face is the anchor: big enough to feel like she's talking to you.
- **Digit colours carry the meaning.** 1 red · 2 orange · 3 gold · 4 emerald · 5 cyan · 6 indigo · 7 royal purple · 8 lavender · 9 hot pink (10 cycles). The rim, the glow, and the jewel all wear the item's colour — so the colour IS the navigation. You always know which item you're in.
- **One family.** The outer cards use the same harvested pattern as the hired boards (`.ph-card`) and the letter beats — same card depth, same obsidian, same rim/glow grammar. A Ten item and a hired board read as siblings.
- **Words byte-identical.** The formatting changed; the copy did not. Presentation is a layer over the words, never a rewrite of them.

## Human

His words, 04:41Z: "It looks super sick. Like, that's crazy. Awesome. Like with the orbs and the color of the way they light up, and you did each one of them lighting up the different coloring makes it easy to read now — that's some high level stuff." And the order: "you want to make notes on that and copy that formatting for other places in the future." The principle behind the pattern, his words 04:31Z: "Think always — how do I present this text and this block, give it intelligence so the user could just skim it and get it — because once you put too much text together and you don't have any separation..."

## Child

Imagine every story on the page lives in its own little shiny black box, and each box glows in its own color — red, gold, blue, green — so you always know which story you're reading. Each box has a little jewel on top that tells you what kind of story it is. And instead of one big scary wall of words, the words are broken into tiny pieces with little glowing balls in front of them, so you can read one piece at a time. And the nice lady's picture is BIG now, so it feels like she's really talking to you. That's the pattern. Copy it everywhere.

## Grandma

Dear, the new way of laying out the words is lovely, and he wants it copied everywhere. Each little part gets its own raised black box — deep and shiny, with the light coming from the top-left, just like a real object — and each box glows in its own color, so you always know where you are. A little jewel sits on top of each box to tell you what it is. The words are broken into short pieces with tiny glowing balls in front, so nothing ever feels like a wall of text. And her picture is twice as big now, love, so it feels like she's truly speaking to you. That's the pattern, dear — write it down, and use it everywhere.

## Naya

This note is the pattern's canonical record — the formatting the Ten now carries, written so it can be harvested like any other part. The grammar to copy: inner block (obsidian 165°, top-left light, digit-colour rim+glow, hover lift+light) · part jewel (`.os-jewel` tile, glyph + label, digit colour) · orb bullets (11px living orbs, one idea per bullet) · face (216px desktop / 124px phone, own grid row on phone) · digit colours as navigation · `.ph-card` family · words byte-identical. The header-block lesson rides with it (see "What changes now"): a section's headliner must be the same size block as its items, aligned — the Ten's "Top 10 reasons to join" header failed that test on v69 and is being fixed in the same build. The pattern is the inner blocks; the header rule is the frame around them.

## What it means

- **THE PATTERN IS SEVEN ELEMENTS:** inner blocks (digit-colour rim+glow, hover lift+light) · part jewels (glyph + label) · orb bullets (one idea each) · doubled face (216/124) · digit colours as navigation · one family (`.ph-card`) · words byte-identical.
- **SKIMMABLE IS THE TEST:** a stranger reads one part at a glance. Colour + jewel + bullets do the work the wall of text couldn't.
- **COPY IT, DON'T REINVENT IT:** the next section that carries three-part copy (pains, customers, boards, any list) starts from this pattern, harvested verbatim.

## Why it matters

A formatting breakthrough that lives only in one section dies with that section. Written down as a pattern — with the exact grammar, sizes, and colours — it becomes inventory: the next builder harvests it instead of inventing a new layout, and the whole product starts to feel like one family. That is the Factory working: mine the best, master it, name it, inventory it, and let everybody build from it.

## What changes now

- This note is the pattern's record. Briefs for any three-part section name it as the harvest source.
- The header-block fix rides in the same build (flow seat): the Ten's "Top 10 reasons to join" header must be the headliner in the same family AND the same size block as the items, aligned — it is currently bigger and off-family.
- The pattern's render proof (Playwright 1440/390/360, zero overflow/errors) comes with the v70 verification, which covers the Ten + the flow + the header together.
