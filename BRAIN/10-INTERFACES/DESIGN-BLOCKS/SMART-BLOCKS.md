# Smart Blocks

You are Naya. These are Smart Blocks — the modular building pieces for Smart Apps.

## How to build with them

1. **Start with tokens.** Include `tokens.css` (at the DESIGN-BLOCKS root) once per page. Every block shares these tokens, so they speak the same language.

2. **Pick your blocks.** Browse `blocks/` by type:
   - `buttons/` — every button style (naya-btn is the canonical)
   - `orbs/` — spheres of light, luminous marks
   - `boards/` — elevated containers, content cards
   - `jewels/` — diamond bullets, jewel atoms
   - `inputs/` — text fields, search
   - `toggles/` — switches, toggle rows
   - `tabs/` — segmented tabs
   - `overlays/` — modals, toasts, share sheets
   - `data/` — tables, charts, bars
   - `media/` — media players

3. **Grab the block.** Each block folder has:
   - `{name}.css` — the exact CSS, byte-true from source. Copy it.
   - `specimen.html` — working HTML showing it in use. Copy it.
   - `{name}.js` — only if the block needs JavaScript. Copy it.
   - `README.md` — what it is, states, dependencies.

4. **They work together.** All blocks use the shared tokens. Mix any blocks on one page — they'll look like they belong together because they do.

## Rules

- **Never rewrite block CSS.** Use it as-is. If you need a variant, create a new block — don't modify the original.
- **If two blocks do the same thing**, check their source attribution and scores in `blocks/index.json`. Pick the higher-scored one unless you have a reason.
- **Every block is self-contained.** CSS + HTML + (optional) JS = working component. If it doesn't work when you copy it, that's a bug — report it.
- **New blocks go through the same process:** extract byte-true, document, score, add to index.

## The test

If you can read this file and `blocks/index.json`, then build a working page by grabbing blocks — the system works. If you can't, tell us what's missing.

## Scores

Block scores come from independent review. Higher = more proven:
- 9.0+ — canonical, battle-tested
- 8.0+ — strong, minor gaps
- 7.0+ — good bones, needs taste corrections
- Below 7 — use with caution

See `blocks/index.json` for per-block scores.
