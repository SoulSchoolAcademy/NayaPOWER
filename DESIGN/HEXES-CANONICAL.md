# CANONICAL HEX SET — stamped set for the Naya spectrum wheel

Status: 3-pass scorecard complete (9.25/10) — awaiting Shawn's stamp.
Source of truth for every hue used in Naya pages. One hex per stop. No alternatives.

## The set

| Stop | Hex | RGB (for glow math) | Hue° | Job |
|------|-----|---------------------|------|-----|
| magenta | `#e84fff` | `232,79,255` | 292 | The living edge |
| purple | `#8a5cff` | `138,92,255` | 257 | Choosing intelligence — the soul |
| indigo | `#6675ff` | `102,117,255` | 234 | The deep signal |
| blue | `#3ca8ff` | `60,168,255` | 207 | Knowledge moving |
| emerald | `#40d3bb` | `64,211,187` | 170 | Forest deep green |
| green | `#2fe89e` | `47,232,158` | 156 | Alive and well |
| lime | `#b8ee57` | `184,238,87` | 82 | New growth |
| gold | `#ffd45a` | `255,212,90` | 44 | Attention, earned |
| orange | `#ff8c42` | `255,140,66` | 24 | Warmth, momentum |
| red | `#ff5e6c` | `255,94,108` | 355 | Urgency, the living edge |
| pink | `#ed58cd` | `237,88,205` | 313 | Delight, the flourish |

## The Strip (5-stop component form, magenta-first)

magenta `#e84fff` → purple `#8a5cff` → blue `#3ca8ff` → green `#2fe89e` → gold `#ffd45a`

## Contrast verification (measured, not asserted)

Adjacent-stop hue separation, in wheel order. Law: adjacent stops must read as
distinct. (The 51.6° jewel guideline governs elements placed adjacent on a page,
not the full 11-stop wheel — even spacing of 11 stops is 32.7° by construction.)

| Pair | Separation |
|------|-----------|
| magenta → purple | 35° |
| purple → indigo | 23° |
| indigo → blue | 27° |
| blue → emerald | 37° |
| emerald → green | 14° — tightest pair; differentiated by teal-vs-green read and lightness (.54 vs .55 with different saturation character) |
| green → lime | 75° |
| lime → gold | 37° |
| gold → orange | 21° |
| orange → red | 29° |
| red → pink | 42° |
| pink → magenta | 21° |

Worst pair improved from 2° (old emerald/green, visually identical) to 14°.

## Banned

- `#ffea00` (pure yellow) — 15 uses found in specimens. The wheel carries gold,
  never yellow. Replace all instances with `#ffd45a`.
- `#d4a017` (muddy dark gold) — 18 uses found in specimens. Replace with `#ffd45a`.
- No hue may carry two hexes. The retired values below are superseded everywhere:

| Retired | Replaced by | Evidence |
|---------|-------------|----------|
| `#a06bff` (purple) | `#8a5cff` | specimens use #8a5cff 65× vs #a06bff 10×; richer and more electric |
| `#9d75ff` (purple) | `#8a5cff` | 49× — same hue family, #8a5cff deeper |
| `#7c3aed` (purple) | `#8a5cff` | 34× — flatter, less luminous |
| `#d86cff` (magenta) | `#e84fff` | #e84fff is the more electric living edge |
| `#ed42c4` (magenta) | `#e84fff` | 35× — pinker; #e84fff holds the magenta seat distinctly from pink |
| `#3fb8ff` (blue) | `#3ca8ff` | 33× specimen-dominant; near-twins, usage decides |
| `#35e0a1` (emerald) | `#40d3bb` | moved teal-ward to separate from green (was 2° apart) |
| `#ffbf3d` (gold) | `#ffd45a` | 21× specimen-dominant; more luminous |
| `#f1d75a` (gold) | `#ffd45a` | same family, #ffd45a cleaner |
| `#ff9a5a` (orange) | `#ff8c42` | 13× specimen-dominant; deeper |

## 3-pass scorecard

**Pass 1 — the old set (DESIGN-LAWS.md table): 6.5/10.**
Why not a 10:
1. Emerald `#35e0a1` vs green `#2fe89e` are 1.9° apart — visually the same color.
   Two stops, one color. Violates "adjacent stops must read as distinct."
2. Severe drift: the "canonical" set is not what excellent looks like. Specimens
   use `#8a5cff` 65× vs contract `#a06bff` 10×; `#ffd45a` 21× vs `#ffbf3d` 4×;
   `#3ca8ff` 33× vs `#3fb8ff` 0×; `#ed42c4` 35× with no magenta seat.
3. Pure yellow `#ffea00` (15×) and muddy `#d4a017` (18×) live in specimens,
   violating "gold, never yellow" — with no canonical gold strong enough to
   displace them.
4. Contrast was asserted, never measured.
5. 10 of 11 adjacencies sat under the 51.6° jewel guideline with no analysis of
   which pairs actually govern.

**Pass 2 — fixes applied.** One canonical hex per stop, chosen by: most beautiful
version of the hue + specimen-usage weight (Shawn's "what excellent looks like")
+ measured adjacent separation. Emerald moved teal-ward (#40d3bb) to break the
green collision; purple/gold/blue/orange seats given to the specimen-dominant
values; yellow and muddy gold banned with replacements.

**Pass 3 — re-score: 9.25/10.** All five Pass-1 reasons resolved: worst pair now
14° (was 2°); drift eliminated — the set IS the specimen-dominant beautiful
values; yellow banned with a canonical replacement; contrast measured per pair
above. Not a 10: emerald→green (14°), gold→orange (21°), and pink→magenta (21°)
remain the snug pairs — distinct reads, but tighter than the rest of the wheel.

## For the stamp

Shawn: this file is the single hex truth. When you stamp it, the specimen
library's drifted values get migrated to these (mechanical find-replace per the
retired table) and DESIGN-LAWS.md's wheel table is updated to match.
