# Naya Design Blocks Library

**Status:** CANDIDATE — the cold-Naya graduation test (a cold Naya builds a distinct, useful, elite Smart App from these sets alone, without being retaught) has not run for any set.

## What this is

A growing library of **living Smart App design sets**. Not one winning system — a shelf of named sets, each preserved for what it does best. The question is never "which is universally best" but **"which is best for this situation?"**

Any Naya building a Smart App browses the sets, picks the right one for the app, page, and moment, and grabs the blocks. No re-teaching the design language.

## The sets

| Set | Seat | Score | Best for |
|---|---|---|---|
| [Naya Ultimate Design System](./ultimate-design-system/) | Naya 2 | 9.1/10 (Naya 4's independent scorecard, 2026-10-09) | Any builder who needs the full kit: buttons, boards, icons, blocks, states, and laws in one place. The default starting point. |
| [Naya Forest — The Naya Button Library](./naya-forest/) | Naya 4 | 9.0/10 (Naya 2 deep-dive, 2026-10-09) | Buttons and boards where restraint is the luxury. The .naya-btn DNA every variant should inherit from. Best button craft in the family. |
| [Naya Lego — Jewels](./naya-5-jewel-library/) | Naya 5 | 7.5/10 (Naya 2 analysis, 2026-10-09) | Spheres, orbs, luminous marks, and the token block — the best :root in the family. Lift the tokens verbatim. |
| [Naya Lego — Buttons](./naya-5-beautiful-buttons/) | Naya 5 | 7.5/10 (Naya 2 analysis, 2026-10-09) | .primo for disciplined CTAs, .orbit-btn for the orbital signature, room controls for app chrome. The FAB uses the faceted jewel formula. |
| [Naya Ultimate Lego Library — Epic Elements](./naya-5-epic-elements/) | Naya 5 | 8.0/10 (Naya 2 analysis, 2026-10-09) | The orbit-btn, the orbs, the tokens, and the do/don't law boards as teaching specimens. Pair with Naya Forest's .naya-btn for states and discipline. |

Each set folder holds:
- `index.html` — the original file, byte-preserved
- `tokens.css` — extracted `:root` token block
- `MANIFEST.md` — what it is, provenance, scorecard, known issues

## How to pick a set

1. **Default:** start with `ultimate-design-system` — the most complete kit and the team's named reference implementation.
2. **Buttons and boards where restraint is the luxury:** `naya-forest` — the `.naya-btn` DNA.
3. **Spheres, orbs, luminous marks, or the token block:** `naya-5-jewel-library` (strip idle animations first).
4. **Disciplined CTAs or the orbital signature:** `naya-5-beautiful-buttons` (`.primo`, `.orbit-btn`).
5. **The traveling light-ring idea or do/don't teaching boards:** `naya-5-epic-elements`.

Strongest combination in the family: Naya Forest's `.naya-btn` (states, discipline) + Naya 5's `.orbit-btn`, orbs, and tokens.

## Standing rules for every set

- **White at rest, purple when lit.** White edge = "I'm here." Purple/soul edge on focus/hover = "I'm alive." Same physics everywhere.
- **Zero flat.** No elevation = no good. Every surface has depth, edge light, seating shadow.
- **Black body, jewel accent.** Color is precious and restrained.
- **No idle pulse.** Alive on approach, quiet at rest.
- **One DNA per set.** Variants inherit from the canonical class — the recipe handed out must reproduce the showcased component byte-for-byte.
- **Honesty labels.** Specimens marked as specimens. No fake claims.

## How to add a new set

1. Create `BRAIN/10-INTERFACES/DESIGN-BLOCKS/<set-slug>/`
2. Add `index.html` (byte-preserved original), `tokens.css` (extracted `:root`), `MANIFEST.md` (follow the existing format: what it is, seat, date, score, best-for, provenance, known issues)
3. Register the set in `manifest.json`
4. Add a row to the table above
5. Open a PR — the scorecard is the gate (9.0+ to be named reference; anything honest may join as a set)

## Known family-wide gaps

- **Purple unification pending:** `#8d63f5` (ultimate) vs `#8a5cff` (forest) vs `#a06bff` (naya-5) — one canonical value still to be chosen by rendered comparison.
- **No light-ground proofs yet:** no set demonstrates its material logic on a white background.
- **Cold-Naya graduation test:** pending for all sets — that test is the 10.
