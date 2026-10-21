# CANONICAL HEX SET — stamped set for the Naya spectrum wheel

Status: CURED VERSION — this version applies the dock's (Verity's) dictated
cure of 2026-10-21 to the set landed on main by #2741, which carried the
pre-cure draft. The cure is applied exactly as dictated: nine stops, the
dictated hex in every seat. Awaiting Shawn's stamp — the stamp remains
Shawn's, and no stamp is claimed here. No score is claimed for this version
either: the 9.25 recorded in the landed draft was scored on the pre-cure set
the dock ruled non-conformant, and it is withdrawn (see "Scorecard" below).
Source of truth for every hue used in Naya pages. One hex per stop. No alternatives.

## The set

| Stop | Hex | RGB (for glow math) | Hue° | Job |
|------|-----|---------------------|------|-----|
| magenta | `#e84fff` | `232,79,255` | 292 | The living edge |
| purple | `#a06bff` | `160,107,255` | 261 | Choosing intelligence — the soul |
| indigo | `#6675ff` | `102,117,255` | 234 | The deep signal |
| canyon | `#3fb8ff` | `63,184,255` | 202 | Knowledge moving |
| kenya teal | `#40d3bb` | `64,211,187` | 170 | The deep crossing |
| emerald | `#2fe89e` | `47,232,158` | 156 | Alive and well |
| gold | `#ffd45a` | `255,212,90` | 44 | Attention, earned |
| orange | `#ff9a5a` | `255,154,90` | 23 | Warmth, momentum |
| red | `#ff5e6c` | `255,94,108` | 355 | Urgency, the living edge |

## The Strip (5-stop component form, magenta-first)

magenta `#e84fff` → purple `#a06bff` → canyon `#3fb8ff` → emerald `#2fe89e` → gold `#ffd45a`

## Contrast verification (measured, not asserted)

Adjacent-stop hue separation, in wheel order, computed from the hexes above
(whole degrees; the nine separations sum to 360° — the wheel closes). Law:
adjacent stops must read as distinct. (The 51.6° jewel guideline governs
elements placed adjacent on a page, not the full 9-stop wheel — even spacing
of 9 stops is 40° by construction.)

| Pair | Separation |
|------|-----------|
| magenta → purple | 31° |
| purple → indigo | 27° |
| indigo → canyon | 32° |
| canyon → kenya teal | 32° |
| kenya teal → emerald | 14° — tightest pair in the dictated set; differentiated by read (cyan-leaning teal vs saturated green) and saturation character (.63 vs .80 at near-equal lightness, .54 vs .55) |
| emerald → gold | 112° — widest gap; the dictated set carries no lime / yellow-green stop |
| gold → orange | 21° |
| orange → red | 28° |
| red → magenta | 63° |

Honest notes: the cure's tightest pair (kenya teal → emerald, 14°) is the same
separation the pre-cure draft carried between its emerald and green seats —
the cure's fix is the seating, not the distance: `#40d3bb` and `#2fe89e` are
two named stops with two jobs, not one color wearing two names. The
emerald → gold span (112°) is the price of a 9-stop wheel with no lime seat;
it is recorded, not hidden.

## Banned

- `#ffea00` (pure yellow) — 15 uses found in specimens. The wheel carries gold,
  never yellow. Replace all instances with `#ffd45a`.
- `#d4a017` (muddy dark gold) — 18 uses found in specimens. Replace with `#ffd45a`.
- No hue may carry two hexes. The retired values below are superseded everywhere:

| Retired | Replaced by | Evidence |
|---------|-------------|----------|
| `#8a5cff` (purple) | `#a06bff` | pre-cure draft value; superseded by the dock's dictated cure, 2026-10-21 |
| `#9d75ff` (purple) | `#a06bff` | same hue family; the dictated purple is `#a06bff` |
| `#7c3aed` (purple) | `#a06bff` | flatter, less luminous |
| `#d86cff` (magenta) | `#e84fff` | #e84fff is the more electric living edge |
| `#ed42c4` (magenta) | `#e84fff` | pinker; #e84fff holds the magenta seat distinctly |
| `#3ca8ff` (blue) | `#3fb8ff` | pre-cure draft value; superseded by the dictated canyon |
| `#35e0a1` (emerald) | `#2fe89e` | near-twin of the dictated emerald |
| `#ffbf3d` (gold) | `#ffd45a` | the dictated gold is `#ffd45a` |
| `#f1d75a` (gold) | `#ffd45a` | same family, #ffd45a cleaner |
| `#ff8c42` (orange) | `#ff9a5a` | pre-cure draft value; superseded by the dictated orange |
| `#b8ee57` (lime) | — (seat removed) | the dictated set has nine stops; there is no lime seat |
| `#ed58cd` (pink) | — (seat removed) | the dictated set has nine stops; there is no pink seat |

## Scorecard

The landed draft recorded a 3-pass scorecard ending at 9.25/10. That score was
given to the pre-cure set — the set the dock ruled non-conformant with the
Oct-18 lock (purple `#8a5cff` for `#a06bff`, blue `#3ca8ff` for canyon
`#3fb8ff`, orange `#ff8c42` for `#ff9a5a`, eleven stops for nine, `#40d3bb`
mis-seated as emerald). The score does not transfer to this version and is
withdrawn.

This cured version carries **no score** until a different seat scores it at
this head. What can be stated without a score: every value above is the dock's
dictated value, verbatim; every RGB and hue figure is computed from the hexes;
the contrast table is recomputed for the 9-stop wheel and labels its tightest
pair and widest gap honestly.

## For the stamp

Shawn: this file is the single hex truth. When you stamp it, the specimen
library's drifted values get migrated to these (mechanical find-replace per the
retired table) and DESIGN-LAWS.md's wheel table is updated to match.
