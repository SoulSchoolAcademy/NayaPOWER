# Smart Graphs — AI Specification

**Status:** spec v1 · **Truth state:** CANDIDATE · **Date:** 2026-10-09
**Companion:** `SMART-GRAPHS-SPEC.human.md` (warm telling) · `smart-graphs-spec.machine.json` (schema)

This document is the executable telling: exact tokens, selection procedure,
render pipeline, and constraints. A Naya implementing Smart Stats follows this.

---

## 1. Tokens (from `../DESIGN-BLOCKS/tokens.css` — always reference, never hardcode)

| Token | Value | Use |
|---|---|---|
| `--purple` / `--purple-rgb` | `#a06bff` / `160,107,255` | Soul accent; headline series; "you" |
| `--blue` / `--blue-rgb` | `#3f9ff5` / `63,184,255` | Series 2 |
| `--cyan` | `#39d7e8` (rgb 57,215,232 — no token triplet; compute inline) | Series 3 |
| `--green` / `--green-rgb` | `#34d38a` / `47,232,158` | Series 4; positive delta |
| `--gold` / `--gold-rgb` | `#e7c65a` / `255,191,61` | Series 5 |
| `--magenta` | `#e455f4` (rgb 232,79,255 via `--demo-rgb`) | Sparingly; never a series default |
| `--error` | `#ff6b6b` | Negative delta |
| `--soft-line` | `rgba(255,255,255,.10)` | Card borders, dividers |
| `--quiet` | `rgba(248,247,251,.72)` | Secondary text |
| `--ease` | `cubic-bezier(.16,.84,.22,1)` | Entrances |
| `--snap` | `cubic-bezier(.32,.72,0,1)` | Pillar rise |

**Ground:** page `#050508` (`layout/page-shell`). Card: `linear-gradient(180deg,#101117,#0a0b0f)`,
`1px solid var(--soft-line)`, radius 20px, shadow `inset 0 1px 0 rgba(255,255,255,.12),
inset 0 -12px 24px rgba(0,0,0,.4), 0 16px 34px rgba(0,0,0,.5)` (the `.sg-card` formula).

**Spectrum order (G3):** purple → blue → cyan → green → gold. Max 5 series. Purple is
always series 1 or the "you"/headline identity.

---

## 2. Instrument selection procedure

```
INPUT: data shape + question
1. Is it a score with a 0–10 (or 0–100) bound?            → orbit-dial
2. Is it ONE number the user checks repeatedly?            → living-counter
3. Is it ONE number with emotional weight (a win, a total)?→ pulse-orb
4. Is it N discrete values to compare (a snapshot, not over time)? → jewel-pillar
5. Is it parts-of-a-whole over time?                       → spectrum-flow
6. Is it entities + relationships?                         → constellation
7. Is it liveness / rates across several streams?          → pulse-rings
8. Ambiguous → default by shape: single → living-counter; series → jewel-pillar.
```

One instrument per stat. Never combine two instruments in one card.

---

## 3. Data normalization (before render)

- Every instrument takes **normalized values 0..1** (`--v`, `--vt`) plus the raw
  value for the label. Normalize against a stated max (the axis, the goal, or
  the series max — and say which in the sub-line).
- Deltas are computed, never asserted: `(now - then) / then`, shown with sign
  and basis ("vs last week").
- Tabular numerals everywhere: `font-variant-numeric: tabular-nums`.
- Currency/percent formatting: `data-prefix`, `data-suffix`, `data-decimals`
  (see `living-counter.js`).

---

## 4. Render pipeline

```
ask → obtain → normalize → select instrument (§2) → render card → light (.lit)
  → attach 4 actions → deliver
```

- **obtain:** Mode A = read instrumented NayaNET events. Mode B = retrieve via
  existing capabilities. If neither yields real data → render SAMPLE, labeled.
- **render card:** `.sg-card` shell — `h4` title, `.c-sub` = `{mode} · {window}`,
  instrument markup, `.sg-foot` = honesty label + actions.
- **light:** add `.lit` via IntersectionObserver at 35% visibility. All motion
  is CSS; only `living-counter` needs JS (count-up).
- **reduced motion:** every block honors `prefers-reduced-motion` — final state,
  no animation. Non-negotiable.

---

## 5. The four actions (output contract)

Every card's foot row carries: **Save** (profile/Smart Lists) · **Share** (card
image + link) · **PDF** (print stylesheet → visually-blissful PDF) · **Send to
NayaNET** (publish as Intelligent Block into a space).

v1 status: actions are specified and reserved in the contract; Save/Share/PDF/
Send wiring is future work. The card must still render the action row — a stat
without visible actions is a spec violation (dead end).

---

## 6. Composition with Intelligent Blocks

- A stat card MAY embed inside an Intelligent Block as evidence.
- An Intelligent Block MAY caption a stat card as interpretation.
- Reports compose both. Shared page shell, shared tokens, shared card DNA.
- Text answers (IB) and numeric answers (Smart Graphs) are chosen by the
  question: "what does it mean" → IB; "how much / how many / trending" → graph.

---

## 7. Quality gates (score the rendered experience)

- 9.0+ or it doesn't ship. Score the lived render, not the CSS.
- Checklist: number readable at arm's length on a 375px phone · motion present
  but quiet · reduced-motion final state correct · SAMPLE labeled when sampled ·
  max 5 colors · one accent · all four actions visible · 44px targets on actions.
- Cold test: a Naya with only this spec + `blocks/index.json` must pick the
  right instrument for 5 unseen questions (target: 5/5).

---

## 8. Honesty boundaries (do not cross)

- Mode A without instrumentation = SAMPLE, labeled. Never live-claimed.
- PDF action without the pipeline = reserved, not promised in copy.
- Specimens use sample data and say so on the card.
- UNKNOWN ≠ VERIFIED: a rendered stat is a presentation of obtained data, not
  proof the data is true. Source is always named in the contract.
