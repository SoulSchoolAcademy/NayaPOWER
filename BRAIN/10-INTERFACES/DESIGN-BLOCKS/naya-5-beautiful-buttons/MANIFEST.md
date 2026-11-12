# Naya Lego — Buttons

**Seat:** Naya 5 · **Date:** 2026-10-09 · **Score:** 7.5/10 (Naya 2 analysis, 2026-10-09)
**Status:** CANDIDATE — cold-Naya graduation test pending for all sets.

## What it is

Seven button systems. .primo: the most disciplined, shippable button (no idle animation, rim ignites in theme color). .orbit-btn: Law 25 made real — a circle of light flows around the button, accelerating on hover. .lv-btn: most advanced 7-layer stack with cursor sheen and proximity wake, but faded blacks. Complete room-controls set (segmented tabs, like pill, send CTA, mic, FAB) — the modular app pieces.

## Best for

.primo for disciplined CTAs, .orbit-btn for the orbital signature, room controls for app chrome. The FAB uses the faceted jewel formula.

## Provenance

Built by Naya 5, uploaded by Shawn 2026-10-09 ~01:54 UTC.

## Files

| File | Purpose |
|---|---|
| `index.html` | The original file, byte-preserved (SHA `e1e57adde87840e6`) |
| `tokens.css` | Extracted `:root` token block(s) — 1 block(s) found |
| `MANIFEST.md` | This file |

Source size: 42,961 bytes · ~43 CSS classes defined.

## Known issues

- Faded blacks on .lv-btn confirmed: #26262e top + 12% white overlay reads fogged vs Naya 4's machined metal.
- Idle animations on .living-btn (sheen sweep) and .lv-btn (breathe + soul pulse) — structural, strip per Shawn's taste.
- 6 of 7 systems lack :focus-visible. No white-background proof.
- 'Shawn-approved' claim on .living-btn is unverified.

## The modular contract

Every set in this library is expected to grow toward the nine-point bar:
1. Ranked variant family inheriting one DNA
2. All states (rest, hover, active, focus, disabled)
3. The 10 canonical blocks (input, modal, toast, table, search, toggle, content card, media player, chart, share sheet)
4. DO/DON'T per component
5. Copyable byte-true recipe (what you hand out == what you showcase)
6. Token table, pinned
7. Motion physics, written down
8. Light-ground (white background) proof
9. Honesty labels on every specimen
