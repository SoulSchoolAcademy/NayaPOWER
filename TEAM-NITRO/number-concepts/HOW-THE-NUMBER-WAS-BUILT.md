# How the Ultimate Number Was Built

**The asset:** the tiled number — each digit a tile, counting up in slow motion, flashing in its own colour, growing as the score grows, with no limit on the digits. It lives at `TEAM-NITRO/number-concepts/top-10-number-concepts.html` (blob c08aab17, 30,655B). Smart Note SN-2221. Registered in the Parts Registry as "The Ultimate Number".

**Shawn's verdict:** better than he envisioned — a work of art he didn't imagine. The design is locked.

## How it was built

### 1. Measure the real thing first — never invent

The number is built from the Dashboard button anatomy, measured live from nayanet.app/dashboard in a real browser (pixel-sampled, 2026-11-07 20:19–20:28Z). The construction, outside to inside:

- A 1–2px light rim, brightest on the top arc (2px violet #a06bff on featured buttons, 1.5–2px silver-grey on neutral ones).
- A black gradient face, top #171720, mid #0f0f15, bottom #020203 — the obsidian black, always visible.
- A 1px white-grey highlight on the top arc.
- White bold content, with a soft lavender-grey halo.
- A soft drop shadow plus a diffused coloured halo outside the rim.

The colour lives in the rim, the cap, or a small chip — **never on the glyph itself**. The number stays white. That is the rule the whole number follows.

### 2. Each digit is a tile, and the tile is a button

The tile (`.reel`) is a button in the Dashboard's language:

- `width: 150px; height: 194px` — a tall tile, like a slot-machine reel.
- A 2px coloured rim (`border: 2px solid var(--c)`) and a diffused halo (`box-shadow: 0 0 22px -4px var(--c)`), where `--c` is the digit's chakra colour.
- A black gradient face (`linear-gradient(180deg, #171720, #0f0f15 45%, #020203)`).
- A glossy cap (`.cap`) on the top third — a lens of the digit's colour, brightest at the top, fading to black.
- A white bold digit (`.rd`, 168px) rolling inside a window (`.window`, 194px tall, overflow hidden).
- A drop shadow beneath it all, so the tile sits ON the page.

The tile's colour comes from the digit it lands on: 1 red, 2 orange, 3 gold, 4 emerald, 5 cyan, 6 indigo, 7 royal purple, 8 lavender, 9 hot pink (the crown chakra), 0 white. Colour is the number's identity, not decoration.

### 3. The reel — how it counts

Each tile holds a vertical strip of digits (`.strip`), and the strip slides up to the target digit:

- `buildReel(reelEl, targetDigit)` builds the strip: digits 0–9, then repeats up to the target, so the strip is long enough to roll through the numbers and land on the target.
- The strip moves with `translateY(-target * 168px)` — 168px is the digit height (H), so each digit is one step.
- The easing is `easeOutQuint` — fast at the start, slowing through the numbers, then landing. Slow-mo IS the effect.
- The landing is staggered: the hundreds land at 5s, the tens at 7.5s, the units at 10s. Each reel lands on its own time, so you watch the number arrive.
- The colour changes in sync with the passing digits (`setReel`): as the count rolls through a digit, the tile's rim, cap and halo take that digit's colour. A flash (`tileFlash`, brightness 2.1 → 1 over .35s, throttled to at least 120ms between flashes) makes each passing colour read without strobing.

### 4. The number grows with the score

The number is dynamic — it is built from the score, not fixed at three digits:

- `createReels(el, target)` builds one reel per digit of the target.
- `growAndReveal(el, fromVal, toVal)` grows it: it rebuilds every strip for the new target, slides a new tile in (`reelIn` keyframe), and counts up to the new value. 725 → 7,250 → 10,725.
- The gauge and the number move as one — the same count, the same easing, the same landing.

### 5. No limit — the tiles shrink to fit the page

Five digits, six, seven, eight, as many as it takes. There is no limit:

- `fitNumber(el)` measures the number against its well and scales the whole number down to fit the page width. The tiles shrink; the number never wraps and never overflows.
- `white-space: nowrap` on the number keeps the tiles in one row.
- If it fits on the page, it is good to go. If you ever get a number that does not fit on the page — congratulations.

An 8-digit demo (12,345,678) proves it on the concepts page.

### 6. The real fix — the bug that taught the rule

The growing demo stalled twice at "1" plus four blank tiles. The first fix (rebuild the strips for the new target) did NOT work. The real cause: `buildReel` read the strip length from the reel's STALE `data-max` attribute (set at creation for 725), so the "rebuilt" strips were still the old lengths — the count ran past the strip end, leaving no digit under the window (blank), while the colour logic advanced correctly. The real fix: the strip length is now computed from the target (`max = Math.floor(target / div)`, and `data-max` is updated). Screen check #3 (21:00Z) proved it on a real screen: the growing demo reaches 10,725 in every run, five tiles, all digits showing, none blank.

**The lesson:** when a fix doesn't work, the cause is not the fix — it is the state the fix reads. Check what the code reads, not just what it does.

## What works

- **Harvest first, never invent.** The number came from the Dashboard's own buttons, measured live. That is why it looks like it belongs.
- **Colour on the outside, black on the inside.** The inside stays obsidian black; the colour is the rim, the cap, the halo. That is what made it sharper than the original ask.
- **Slow-mo is the effect.** The landing is staggered and the count is slow enough to see each number and its colour. Fast would have hidden it.
- **The number is a button.** Every digit is built in the button's language, so the number reads as a real object, not as text.
- **Prove it on a real screen.** The hero was confirmed, the growing demo was caught broken twice by the screen check, and the real fix was proven the same way. A claim is not proof.
- **Save the asset.** The number is in GitHub, filed as SN-2221, and registered in the Parts Registry — so it is ours for good and any page can harvest it.

## What matters

- **Multiple elements on one viewport, working together.** The number, the gauge, the orbs, the toggles — they share one count, one easing, one landing. That is the mastery: not one element done well, but many elements on the same viewport, moving as one, fast and effective and efficient.
- **The number is the first smart block.** It is an element on its own, an object of itself — a Lego block in the digital matrix. The Dashboard takes it for the score and the gauge. The Pricing page takes it for the calculator. Any page that needs a number takes this one.
- **Document as you build.** This file is the record: how it was done, what works, how, and what matters — so the next build starts from the lesson, not from scratch.

## Where it goes next

1. **The Dashboard** — the number merges with the gauge (the number at the top, the gauge + orbs below, PTS / % / MONEY toggle underneath). The money gauge runs in sets of 500 and wraps, never bounces. The money number gets a $ tile in front.
2. **The Pricing page** — the calculator takes the number + gauge, so the visitor picks Power, Pro Power or Max Power and the number they can make comes out like this, the tiles counting up and the gauge moving with it. That is the moment that sells it.
