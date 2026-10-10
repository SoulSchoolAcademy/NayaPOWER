# DESIGN ACTIVATION — before touching any design work

**You do not design from scratch. You take the pieces and put them together beautifully.**

This is the design-specific entry sequence. Complete it after the general activation
(`activation-checklist.json`) and before writing a single line of CSS. If you skip
this, you will produce the flat-button garbage Shawn has corrected a hundred times.
That pattern is now a law violation, not a mistake.

---

## Step 1 — Load the 10 load-bearing laws

Read these from source (`DESIGN-LAWS.md` — Naya 5's encoding; the Design Contract for
full text). Do not work from memory. Name each one back before proceeding:

1. **Black root.** Page ground is deep black (`#050507` family). No path for white
   to leak in. `<meta name="color-scheme" content="dark">` required.
2. **Text is white, 99% of the time.** Hierarchy comes from size — 24px headline /
   18px body / 14px detail — never from gray or colored text.
3. **No freestyle components.** Every component class must exist in the block
   manifest. If no block fits, file the gap — don't invent one silently.
4. **Buttons: black heart, white voice.** Black base, purple edge glow at rest;
   they light up white on interaction. Never colored text on buttons.
5. **Purple is accent and glow — never a solid fill.** Purple is Naya's presence
   (soul/chrome), not a background color.
6. **One spectrum accent per item.** Magenta → purple → blue → green → gold gives
   identity. Never cross the color jobs (chrome / text / theme).
7. **Self-contained delivery.** One file, all CSS/JS inlined, no external refs.
   Verify from an empty folder the way he will open it.
8. **No manufactured numbers.** Every number carries provenance or it doesn't ship.
9. **Verify through his eyes.** Screenshot the artifact the way he'll experience it.
   His screen is the test environment, not your build output.
10. **The Usefulness Gate.** If it's not useful it can never be used. If you
    wouldn't give it to the world, don't give it to him — don't give it to anybody.
    Silence beats garbage.

## Step 2 — Load the block catalog

Open `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json`. This is the official
**Naya Design** vocabulary — 91 proven blocks across 22 categories, extracted
verbatim from Shawn's approved designs.

For your task, name the candidate blocks BEFORE writing code:
- What is the page/section? → which layout blocks?
- What are the interactive elements? → which button/input/block?
- What data displays? → which data/graph/feed blocks?

If you cannot name a block for a component you need, you have two options:
file the gap (honest) — never silently freestyle (violation of Law 3).

## Step 3 — Look at what elite looks like

Do not work from a description of the design language. Open the specimens:
- Each block's `specimen.html` in its block directory — the rendered truth.
- The gallery (`smart-blocks-gallery.html`) for the full set at a glance.

Your output must be visually indistinguishable in quality from these specimens.
If your button doesn't look like the approved button block's specimen, you're not done.

## Step 4 — Compose, don't create

The build order:
1. Assemble the page from official blocks first — layout, then components, then content.
2. Custom CSS only for glue (spacing between blocks, page-specific arrangement).
3. Custom CSS for a *component* only when no block exists — and that gap gets
   filed so the library grows instead of the page drifting.

## Step 5 — Pre-delivery check

Before anything reaches Shawn:
- [ ] Every component traces to a block in the manifest (or a filed gap).
- [ ] Ground is black, text is white, hierarchy is by size.
- [ ] Buttons follow Law 4. Purple follows Law 5. Accents follow Law 6.
- [ ] No number without provenance (Law 8).
- [ ] Verified the way he'll open it — screenshot or open from empty folder (Laws 7, 9).
- [ ] Passes the Usefulness Gate (Law 10): would I give this to the world?

---

**When he corrects your design work**, the activation failed — you worked without
the laws loaded or without the catalog open. Write the new law down that hour.
The next activation carries it.
