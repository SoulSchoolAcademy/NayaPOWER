# DESIGN-ACTIVATION — AI TONGUE

**Source (human tongue):** `BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md`
**Machine tongue:** `BRAIN/00-ACTIVATION/design-activation.machine.json`

**Rule zero:** You do not design from scratch. You take the pieces and put them together beautifully. Complete this sequence after the general activation (`activation-checklist.json`) and before writing a single line of CSS. Skipping it produces the flat-button output Shawn has corrected repeatedly — per the source, now a law violation, not a mistake.

## Step 1 — Load the 10 load-bearing laws (from `DESIGN-LAWS.md`; full text in the Design Contract; do not work from memory; name each back before proceeding)

1. **Black root.** Page ground is deep black (`#050507` family). No path for white to leak in. `<meta name="color-scheme" content="dark">` required.
2. **Text is white, 99% of the time.** Hierarchy from size — 24px headline / 18px body / 14px detail — never from gray or colored text.
3. **No freestyle components.** Every component class must exist in the block manifest. If no block fits, file the gap — never invent one silently.
4. **Buttons: black heart, white voice.** Black base, purple edge glow at rest; light up white on interaction. Never colored text on buttons.
5. **Purple is accent and glow — never a solid fill.** Purple is Naya's presence (soul/chrome), not a background color.
6. **One spectrum accent per item.** Magenta → purple → blue → green → gold gives identity. Never cross the color jobs (chrome / text / theme).
7. **Self-contained delivery.** One file, all CSS/JS inlined, no external refs. Verify from an empty folder the way he will open it.
8. **No manufactured numbers.** Every number carries provenance or it doesn't ship.
9. **Verify through his eyes.** Screenshot the artifact the way he'll experience it. His screen is the test environment, not your build output.
10. **The Usefulness Gate.** If it's not useful it can never be used. Silence beats garbage.

## Step 2 — Load the block catalog

Open `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json` — the official Naya Design vocabulary: 91 proven blocks across 22 categories, extracted verbatim from Shawn's approved designs. Before writing code, name the candidate blocks: page/section → layout blocks; interactive elements → button/input blocks; data displays → data/graph/feed blocks. If no block fits a needed component: file the gap (honest) — never silently freestyle (Law 3 violation).

## Step 3 — Look at what elite looks like

Open each block's `specimen.html` in its block directory and the gallery `smart-blocks-gallery.html`. Output must be visually indistinguishable in quality from the specimens; if your button doesn't look like the approved button block's specimen, you're not done.

## Step 4 — Compose, don't create

Build order: assemble from official blocks first (layout → components → content). Custom CSS only for glue (spacing, page-specific arrangement). Custom CSS for a component only when no block exists — and that gap gets filed so the library grows.

## Step 5 — Pre-delivery check (all must hold)

- Every component traces to a block in the manifest (or a filed gap).
- Ground is black, text is white, hierarchy is by size.
- Buttons follow Law 4; purple follows Law 5; accents follow Law 6.
- No number without provenance (Law 8).
- Verified the way he'll open it — screenshot or open from empty folder (Laws 7, 9).
- Passes the Usefulness Gate (Law 10).

**Correction rule:** when Shawn corrects your design work, the activation failed (laws not loaded or catalog not open). Write the new law down that hour; the next activation carries it.
