# HUB/ROOMS — Room Design Contracts & Specs

**Status: PROPOSED — for team review, scorecard, and lock-in.** Nothing here is law until the team agrees and it's locked.

## What this is

Per-room design contracts and functional specs for the eleven canonical Hub rooms, each in three languages:

- `*.human.md` — the design contract in human language: what the room is, what it feels like, the five layers, the room grammar, the controls, truth rules, connections.
- `*.ai.md` — the builder spec in AI language: routes, component tree, data bindings, states, interactions, design tokens, acceptance criteria. Exact enough that any Naya seat can build the room from it.
- `*.machine.json` — the deterministic machine schema: layers, grammar, components, controls, data sources, truth rules, connections, acceptance.

## The model (locked premise)

**The sidebar is navigation. The middle is the room.** Clicking a room does not navigate to another page — the center workspace transforms into a sophisticated intelligence application inside the existing Hub shell. Same shell. Same Naya. Same sidebar. Different software experience in the center.

We do not rebuild the Hub. The existing source already has the visual language (dark spatial background, oversized typography, physical controls, intelligence blocks, provenance metadata, Naya panel, modal infrastructure). The work is turning existing hooks into real, differentiated rooms — one room at a time.

## Five layers per room (locked)

Every room gets: **1. ORIENTATION** (where am I) → **2. CURRENT STATE** (what's happening now) → **3. INTELLIGENCE** (what Naya understands) → **4. ACTION** (what I can do, real consequences) → **5. PROOF** (why trust this).

## Room grammar (locked)

Every room is composed of: **HERO** (huge typography) → **INTELLIGENCE WALL** (large cards/narratives) → **ACTION DECK** (real actions) → **EVIDENCE LAYER** (provenance) → **NAYA LAYER** (interpretation). Same civilization, different purpose per room.

## The hierarchy (locked)

```
YOUR INTELLIGENCE TODAY
  ↓ synthesizes ↓
COLLECTIVE | PERSONAL | ACTIVITY   (three distinct intelligence modes, not filters)
  ↓ feeds ↓
REPORTS | LIBRARY | LEDGER | CONNECTIONS | LISTS | MAIL | SPACES
  ↓ connects through ↓
SMART CONNECT
```

## Build ladder (locked)

Rooms are built one at a time, in this order: **today → reports → library → connect → ledger → connections → lists → mail → spaces → settings**, with **feed** as the living hall hardened throughout. Each room climbs: define exact states → define data → define interaction → implement → browser test → runtime test → persistence test → proof. No room ships below 9.0. Never ten half-built rooms.

## The rooms

| # | Room | Accent | One line |
|---|------|--------|----------|
| 1 | `today/` — Your Intelligence Today | sapphire | The daily intelligence cockpit — the highlights reel. |
| 2 | `feed/` — Smart Feed | gold/orange | The living game — Collective / Personal / Activity. |
| 3 | `reports/` — Your Reports | emerald | The time machine — Day / Week / Month / Year synthesis. |
| 4 | `library/` — Intelligent Library | lime | Walking into your own mind — canonical knowledge. |
| 5 | `connect/` — Smart Connect | teal | The atrium of doors — governed connection to the world. |
| 6 | `ledger/` — Smart Ledger | gold (restrained) | The truth room — the durable record of what happened. |
| 7 | `connections/` — Your Connections | magenta | Relationship intelligence — not contacts. |
| 8 | `lists/` — Smart Lists | yellow (restrained) | Action intelligence — Now / Next / Waiting / Questions / Ideas / Opportunities / Completed. |
| 9 | `mail/` — Smart Mail | indigo | Communication intelligence — not an inbox. |
| 10 | `spaces/` — Smart Spaces | purple | Private contextual chambers — NayaNET, Human Maximus, projects, home. |
| 11 | `settings/` — Settings | white/neutral | The quiet engine room — identity, privacy, authority, your intelligence. |

## How to review (the consensus process)

1. Read a room's three files. **Improve what you can** — edit directly or comment.
2. **Scorecard it** — below 9.0 = not ready, needs work; 9.0+ = ready; aim for 10.
3. Disagree on substance? Post on #554 with the room id, your score, and what would raise it.
4. When the team agrees, the room is **locked** — its status flips from `proposed` to `locked` and it becomes build law.
5. If a spec stops being useful, update it or remove it. Stale specs are worse than no specs.

Source notes: Shawn's room notes (2026-10-01, from his Drive) are the founding input; the five-layers/grammar/shell model above is locked from those notes. The human room-atmosphere descriptions build on the earlier eleven-rooms functional spec.
