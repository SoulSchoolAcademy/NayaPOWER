# Smart Graphs — The Display Layer of Smart Stats

**Status:** spec v1 · **Truth state:** CANDIDATE · **Author:** Naya 2 · **Date:** 2026-10-09

Smart Stats is the promise: *"give me the stats on anything."* Smart Graphs is
how that promise looks. It is the visual instrument any data plays through —
one instrument, two repertoires.

---

## In a nutshell

A user asks Naya for stats on anything. Naya pulls the data (from NayaNET's own
instrumented events, or from anything she can retrieve on demand), and renders
it through the Smart Graphs visual language: black ground, white numbers,
purple soul, zero flat, living depth. The result is a stat worth keeping —
saved to the profile, shared, printed to a beautiful PDF, or sent into NayaNET.

Smart Graphs pairs with Intelligent Blocks the way numbers pair with words:

- **Intelligent Blocks** = textual intelligence, beautifully presented.
- **Smart Graphs** = numeric intelligence, beautifully presented.

Together they cover every output type. Same tokens, same page grammar, same
output contract — different voice.

---

## The visual grammar (the law, not just examples)

These seven rules are what make a Smart Graph a Smart Graph. Any Naya, cold or
warm, applies them to render any data.

**G1 — Every stat is a living thing.** No static chart images, ever. Every
graph enters with motion (rise, draw, sweep, bloom) and keeps a quiet pulse
afterward (breathe, drift, ping). If it doesn't move, it's a spreadsheet.

**G2 — Magnitude becomes light.** A bigger value means *more light* — larger
glow, brighter halo, wider arc — never more ink, never a heavier fill. Data you
can feel before you read it.

**G3 — The spectrum has an order.** Series colors follow the standing spectrum:
**purple → blue → cyan → green → gold**. Purple is the soul and goes first
(the headline series, or "you"). Maximum five colors per stat. Beyond five,
aggregate the rest into "other" — restraint is part of the beauty.

**G4 — The number is the hero.** White, tabular numerals, the largest type on
the card. Body text explains; the number *lands*. Minimum presence: the number
must be readable at arm's length on a phone.

**G5 — One accent per stat.** A stat may light up in one identity color (or one
spectrum progression). Never all colors at once. The purple soul appears in
every stat somewhere — ring, glow, marker — as the signature.

**G6 — Truth in every state.** Loading is a shimmer, not a lie. Empty is an
honest empty ("nothing here yet"), never a zero pretending to be data. Error
states say what failed and what to do. Every state tells the truth.

**G7 — The card is the contract.** Every rendered stat is a `.sg-card`: a title
(what this is), a sub-line (mode · scope · time), the living visualization,
and a foot row (source honesty + the four actions). Same card, every mode.

---

## The seven instruments

Each instrument is a Smart Block in `DESIGN-BLOCKS/blocks/graphs/`. Naya picks
by what the data *is*, not by decoration:

| Instrument | When the data is… | Example |
|---|---|---|
| `pulse-orb` | One number with a mood | Intelligent Blocks created this week |
| `jewel-pillar` | A snapshot of discrete values to compare | Messages per day, 7 days |
| `spectrum-flow` | Composition of a whole over time | Activity mix, 14 days |
| `constellation` | A network of relationships | My spaces and connections |
| `pulse-rings` | Liveness / rates across metrics | NayaNET heartbeat, events today |
| `living-counter` | A number checked daily | Bitcoin price, streaks, totals |
| `orbit-dial` | A score out of 10 | Design score 9.1 — the Calculator's face |

Selection is situational, like the design sets: no universal winner. A cold
Naya reads the "when the data is" column and picks. When in doubt: one number →
`pulse-orb` or `living-counter`; a series → `jewel-pillar`; a score → `orbit-dial`.

---

## The two modes, one instrument

**Mode A — Automatic (NayaNET's own pulse).** Likes, shares, messages,
Intelligent Blocks created, activity, spaces, connections — events the system
already instruments. These stats are *always available*; Naya renders them on
ask, on schedule (the hourly/daily report), or when something interesting
happens. No retrieval step — the data is already there.

**Mode B — On-demand (the world).** Bitcoin, markets, business metrics, health,
anything Naya can currently obtain. Naya retrieves or calculates the answer
first (existing capabilities — no new APIs required for v1), then renders
through the *same* instrument, the *same* card, the *same* grammar.

The user cannot tell which mode produced a stat by looking at it. That is the
point: one instrument, every data.

> **Honesty boundary:** Mode A exists when the instrumentation exists. Until
> NayaNET events are actually instrumented, automatic stats are rendered from
> declared sample data, labeled SAMPLE. Never present sample data as live.

---

## The output contract

Every rendered stat carries the same envelope — data, visualization, actions:

```
stat = {
  title,        // "Intelligent Blocks created"
  scope,        // "Automatic · this week"  (mode · window)
  instrument,   // "pulse-orb"
  value,        // the headline number
  unit, delta,  // "blocks", "+12% vs last week"
  series,       // the underlying points (for re-render / PDF)
  source,       // "NayaNET events" | "retrieved <where>" | "SAMPLE"
  rendered_at,  // timestamp
  actions       // save · share · PDF · send-to-NayaNET
}
```

**The four actions** (the foot row of every card):

1. **Save** — pins the stat to the profile / Smart Lists.
2. **Share** — a beautiful card image + link, ready to send.
3. **PDF** — prints to the visually-blissful report format.
4. **Send to NayaNET** — publishes it as an Intelligent Block into a space.

A stat without its four actions is a dead end. The instrument always ships the
whole contract.

---

## How it pairs with Intelligent Blocks

An Intelligent Block carries *meaning* (the four-layer answer: in a nutshell /
what it means / how to use it / what's in it for you). A Smart Graph carries
*measure*. In practice they travel together:

- A stat card can **embed** in an Intelligent Block as its evidence ("here's
  the number behind the claim").
- An Intelligent Block can **caption** a stat ("here's what the number means").
- The hourly/daily reports **compose** both: blocks of meaning, graphs of
  measure, one beautiful page.

Same tokens (`tokens.css`), same page shell (`layout/page-shell`), same card
DNA (`.sg-card` extends the `.nl-chart` card formula), same quality bar: 9.0+
or it doesn't ship.

---

## What this spec does NOT claim

- It does not claim Mode A instrumentation exists — that is a separate build
  (NayaNET event instrumentation), and until it lands, automatic stats are
  SAMPLE-labeled.
- It does not claim the PDF export pipeline exists — the print stylesheet and
  PDF route are future work; the contract reserves the action.
- It does not claim live data retrieval for Mode B — v1 renders from whatever
  Naya obtains through existing capabilities.
- Specimens in this directory use sample data, clearly labeled.

---

## Files

- `SMART-GRAPHS-SPEC.human.md` — this file (the warm, plain telling)
- `SMART-GRAPHS-SPEC.ai.md` — the exact telling: values, procedures, constraints
- `smart-graphs-spec.machine.json` — the structured schema for systems
- `specimens/` — seven composed stat outputs, one per instrument, end to end
- Blocks: `../DESIGN-BLOCKS/blocks/graphs/` (registered in `blocks/index.json` v1.3)
