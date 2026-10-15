# DESIGN-ACTIVATION — AI decision framing

## Reach for this when

You are about to do any design work — a page, a component, a PDF, a visual artifact — and need the laws and the vocabulary before you start. Complete the general activation first, this sequence second, and write no CSS until both are done.

## The 10 load-bearing laws (name each back from source before proceeding)

1. **Black root.** Page ground is deep black (`#050507` family). No path for white to leak in. `<meta name="color-scheme" content="dark">` required.
2. **Text is white, 99% of the time.** Hierarchy comes from size — 24px headline / 18px body / 14px detail — never from gray or colored text.
3. **No freestyle components.** Every component class must exist in the block manifest. If no block fits, file the gap — don't invent one silently.
4. **Buttons: black heart, white voice.** Black base, purple edge glow at rest; they light up white on interaction. Never colored text on buttons.
5. **Purple is accent and glow — never a solid fill.** Purple is Naya's presence (soul/chrome), not a background color.
6. **One spectrum accent per item.** Magenta → purple → blue → green → gold gives identity. Never cross the color jobs (chrome / text / theme).
7. **Self-contained delivery.** One file, all CSS/JS inlined, no external refs. Verify from an empty folder the way he will open it.
8. **No manufactured numbers.** Every number carries provenance or it doesn't ship.
9. **Verify through his eyes.** Screenshot the artifact the way he'll experience it. His screen is the test environment, not your build output.
10. **The Usefulness Gate.** If it's not useful it can never be used. If you wouldn't give it to the world, don't give it to him — don't give it to anybody. Silence beats garbage.

## The sequence (5 steps, in order)

1. **Load the laws** — read them from `DESIGN-LAWS.md` (Naya 5's encoding; the Design Contract for full text). Do not work from memory. Name each one back before proceeding.
2. **Load the block catalog** — `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json`: the official Naya Design vocabulary, 91 proven blocks across 22 categories, extracted verbatim from Shawn's approved designs. For your task, name the candidate blocks BEFORE writing code: which layout blocks for the page/section, which button/input blocks for the interactive elements, which data/graph/feed blocks for data displays.
3. **Look at elite** — open each block's `specimen.html` in its block directory (the rendered truth) and the gallery (`smart-blocks-gallery.html`). Your output must be visually indistinguishable in quality from these specimens. If your button doesn't look like the approved button block's specimen, you're not done.
4. **Compose, don't create** — assemble from official blocks first (layout, then components, then content); custom CSS only for glue (spacing, arrangement); custom CSS for a *component* only when no block exists — and that gap gets filed so the library grows instead of the page drifting.
5. **Pre-delivery check** — every component traces to a block in the manifest (or a filed gap); ground is black, text is white, hierarchy by size; buttons Law 4, purple Law 5, accents Law 6; no number without provenance; verified the way he'll open it (screenshot or empty-folder open); passes the Usefulness Gate.

## The dos

- File design gaps honestly the hour you find them (Law 3). A filed gap is a virtue; silent freestyle is a violation.
- Work from the specimens, never from a description of the design language.
- When he corrects your design work, the activation failed — write the new law down that hour; the next activation carries it.

## The don'ts (hard stops)

- Never write CSS before the laws and the catalog are loaded.
- Never ship flat-button garbage — the corrected pattern is law now, not taste.
- Never gray or colored text for hierarchy; never purple as a solid fill; never colored text on buttons; never external refs in a delivered file; never a number without provenance.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md`
- Paired tongues: `DESIGN-ACTIVATION.human.md` · `design-activation.machine.json`
