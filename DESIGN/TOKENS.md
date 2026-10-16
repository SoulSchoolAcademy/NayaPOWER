# NAYA DESIGN TOKENS

Every value the system is allowed to use. If it isn't here, it doesn't ship.
Source of truth: `TOKENS.css` (machine). This file is the human map.

## The field — backgrounds. "Deep, never gray."

| Token | Value | Job |
|---|---|---|
| `--field` | `#050507` | The world. Page background. |
| `--obsidian` | `#0B0D12` | Primary surface. Cards, panels, app chrome. |
| `--raise` | `#10141d` | Raised surface — one step above obsidian. |
| `--card` | `#141a28` | Card bodies. |
| `--deep` | `#0a0e16` | Deepest wells, inset zones. |

## The light — text and idle rims. "Text 99% of the time."

| Token | Value | Job |
|---|---|---|
| `--white` | `#F8F7FB` | Primary text. 99% of all text. |
| `--ink` | `#F5F7FB` | Ink text on light accents. |
| `--quiet` | `rgba(248,247,251,.72)` | Secondary text. |
| `--secondary` | `rgba(248,247,251,.55)` | Tertiary text, captions. |
| `--line` | `rgba(255,255,255,.12)` | Hairlines, dividers, idle rims. |

Law: every interactive element shows a visible rim (1.5px+) at rest. White
light at rest; ignition belongs to the thing being touched.

## The soul — chrome accent. "Naya's presence. Never a flood."

| Token | Value | Job |
|---|---|---|
| `--soul` | `#a06bff` | Naya's presence. Chrome ignites purple. Used sparingly — an accent, not a flood. |

## The spectrum — meaning, in law order. "Richest first, ultra-rich magenta leading."

| Token | Value | Job |
|---|---|---|
| `--magenta` | `#e84fff` | The living edge. Leads every flow. |
| `--purple` | `#a06bff` | Choosing intelligence. The soul. |
| `--blue` | `#3fb8ff` | Knowledge moving. |
| `--green` | `#2fe89e` | Alive and well. |
| `--gold` | `#ffbf3d` | Attention, earned. |

Each ships with an `-rgb` triplet (`--magenta-rgb: 232,79,255`, etc.) for
`rgba()` glows. Law: one spectrum step per board. Adjacent things never share
a hue. Scramble the order and the eye knows something is wrong before the mind
does.

Naya_2 role names for the same six: priority (magenta) · presence (purple) ·
insight (blue) · flow (cyan) · verified (green) · value (gold).

## Extended family

| Token | Value | Job |
|---|---|---|
| `--teal` | `#40d3bb` | Cool secondary accent. |
| `--coral` | `#ff5e6c` | Warm alert — never a glowing red. Danger stays dark and restrained. |
| `--lime` | `#b8ee57` | Fresh highlight. |
| `--indigo` | `#6675ff` | Deep secondary. |

## Truth states — "A claim and a proof must never look the same."

| Token | Value | Job |
|---|---|---|
| `--verified` | `#2fe89e` | Proven. Independent evidence exists. |
| `--claim` | `#ffbf3d` | Shown honestly, awaiting its stamp. |
| `--demo` | `#e84fff` | Beautiful on purpose — a specimen, not live. Never pretending. |

## Motion

| Token | Value | Job |
|---|---|---|
| `--ease` | `cubic-bezier(.22,1,.36,1)` | The signature ease. Lifts, lights, hovers. |
| `--snap` | `cubic-bezier(.32,.72,0,1)` | Snappy state changes. |

Interaction physics (Naya_2): approach wakes at ~170px · hover lifts −3px ·
press settles +1px · focus gets a 2px white ring at 4px offset · reduced
motion disables orbit/float. "Alive at rest, brilliant on approach."

## Elevation

| Token | Value | Job |
|---|---|---|
| `--lift` | `0 18px 50px rgba(0,0,0,.55), 0 6px 18px rgba(0,0,0,.4)` | Card/board lift. |
| `--ring` | `0 0 0 2px rgba(160,107,255,.35)` | Soul focus ring. |

## Radii

| Token | Value |
|---|---|
| `--r-sm` | `11px` |
| `--r-md` | `13px` |
| `--r-lg` | `18px` |
| `--r-xl` | `26px` |
| `--r-pill` | `999px` |

## Type — Law 52 (the working scale)

Size separates, color doesn't. White 99% of the time.

| Role | Size | Notes |
|---|---|---|
| Display | 32–40px | Heroes only. Serif voice allowed. |
| Headline | 22–28px | Section titles. |
| Body | 15–17px, line-height 1.45–1.6 | Most text lives here. |
| Detail | 12–13px | Never below 12px. Nothing readable goes smaller. |
| Kicker | 11px, uppercase, tracked | Labels, eyebrows. |

Fonts: UI/body/data = Inter (system sans fallback). Voice/display =
Newsreader (Georgia fallback) — serif is for voice, never for UI.
[VERIFY: Newsreader webfont hosting — Georgia is the safe fallback.]

The N5 `--type-display: 64px` / `--type-chapter: 40px` tokens are
hero/chapter contexts only; Law 52 governs all UI text. See `DECISIONS.md`.

## Room accents

One room, one spectrum color. A board's spine, kicker, and jewel agree on a
single accent — never two. (Applied reference: the Smart Hub page assigns one
spectrum accent per room.) Exact per-room assignments: [VERIFY against the
Smart Hub source before pinning — do not invent the mapping here.]
