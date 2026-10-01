# The Design Laws of NayaNET

*Human language. For Shawn — and for every human who will ever judge whether this interface is extraordinary.*

## Why laws, not guidelines

Guidelines get interpreted. Laws get obeyed. A ten-trillion-dollar interface doesn't happen because talented people tried hard on different days — it happens because everyone who touches it serves the same physics. These laws are that physics. They bow to the [Design North Star](../DESIGN-NORTH-STAR.md) and to **Law Zero**: readability is supreme over decoration, always.

## The laws, in one breath

1. **Tone Law** — color is meaning, never ornament. Every board owns exactly one color, and that color flows through everything the board touches.
2. **Boards Law** — boards are full-bleed editorial worlds, not cards in a grid. Each one has an anatomy, and the anatomy is not optional.
3. **Button Law** — flat buttons are banned. Every button has depth, light, and a response. Pressing one feels like touching something real.
4. **Type Law** — tiny eyebrows, giant headlines, generous body. Nothing readable is ever small.
5. **Motion Law** — motion is feedback, never theater. The interface feels alive because the intelligence is alive.
6. **Naya Law** — Naya is present, personal, and honest. Amber for gaps, never dressed up.
7. **Proof Law** — every claim carries its evidence. Every board ends with provenance.

## Tone Law — color is meaning

The foundation is obsidian, purple, black, and white. Those four dominate — always. The spectrum (gold, green, magenta, blue, red) appears only as *meaning*: one color per board, and that color tells you what kind of truth you're looking at.

- **Gold** = memory, milestone, precious. Used sparingly — it never shouts, never becomes body text, never outshines purple.
- **Green** = alive, verified, growing.
- **Magenta** = the collective, the network.
- **Blue** = law, truth, clarity.
- **Red** = alert, the honest gap.

When you see a board washed in green, you know before reading a word: *this is alive and proven.* That is color doing work.

## Boards Law — worlds, not cards

A board is a full-bleed section of the room with its own atmosphere. It is never a small rectangle floating in a grid. Every board has the same anatomy, in the same order:

1. A **rail of light** in the board's color runs down its left edge, fading as it falls.
2. A **wash of that color** — barely there, 7–8% — tints the board's air.
3. An **identity row**: a jewel-like glyph in the board's color, the board's kind, and its truth seal.
4. A **headline** — big, tight, confident. 30 to 50 pixels.
5. **One** nutshell paragraph. Not three. The depth lives in the full layer stack beneath it — human note, child note, grandma note, Naya's note, machine note (the evidence boundary), learning lesson, what it means, what's in it for you, how to use it, and how it all connects. Every board carries the whole journey; every board tells it a little differently.
6. **Actions** — buttons with real depth (see Button Law).
7. A **provenance footer** — where this came from, when, and what backs it.

Boards are separated by a single hairline. The room reads as a journey downward, each world giving way to the next.

## Button Law — nothing flat, ever

A flat button is a broken promise — it looks like it might do something and feels like nothing. Every NayaNET button is a small physical object:

- A **2-pixel tinted border** (purple by default, or the board's color).
- A **body** that falls from light to dark at 145 degrees, like a surface catching a lamp.
- A **thread of light** across its top edge — the highlight that says *this is raised*.
- A **deep shadow** beneath it grounding it to the surface.
- On hover, it **lifts**, its border ignites in the board's color, a **sheen sweeps** across it, and it glows.
- Pressing it feels like pressing — it yields.

Primary actions (like "Catch Me Up") are gold, with dark text. Toggled states light up in their own color: love glows red, save glows green. You never wonder whether your touch registered.

## Type Law — whisper, proclaim, converse

Three voices, no more:

- **Whisper** (eyebrows, labels): 10–11px, bold, wide letterspacing. Small but never *tiny* — Law Zero forbids the 7px micro-text of lesser interfaces.
- **Proclaim** (headlines): 30–76px, tightly tracked. A headline should feel like walking into a room.
- **Converse** (body): 16–18px, generous line height. Reading should feel effortless on the eyes.

## Motion Law — feedback, not theater

Everything moves on the same curve, in about a fifth of a second. Buttons lift on hover. Layers open smoothly. Nothing bounces, nothing spins to impress you, nothing animates while you wait for intelligence. If the interface feels alive, it's because Naya is thinking — not because a designer added sparkles. And anyone who prefers reduced motion gets stillness, completely.

## Naya Law — present, personal, honest

Naya is always in the room — a steady presence in the rail, speaking in her own voice, in first person. She tells you why the feed looks the way it does. And she is honest: verified claims wear green, work-in-progress wears amber, and a gap is named, never dressed up. Trust is the whole product.

## Proof Law — show your work

No claim appears without its seal. No board ends without provenance: what this is, where it came from, when it was verified. Proof isn't a feature of the interface — it's the interface.

## The bar

Every room is scorecarded against these laws on eight dimensions, each out of ten: theming, buttons, color flow, text density, board elevation, room completeness, Naya presence, proof. **Below 9.0 is not ready.** The reference implementation — the build these laws were extracted from — is the Smart Feed visual blueprint (v2).

*These laws are not finished. They are version one of a constitution meant to be amended by evidence — every time a room scores below 9, the laws learn why. The reference implementation is the Smart Feed blueprint: a faithful restoration of the canonical page, not a redesign.*
