# 0008 — Intelligent Block V1 (AI tongue)

The sender's output contract. For Naya seats emitting blocks and for the Hub
composer rendering them. The machine schema is
`BRAIN/00-SPEC/SCHEMA/INTELLIGENT-BLOCK-SCHEMA.json` — this document is the
exact behavioral spec around it.

## 1. Emitter rules (engine side)

1. `essence` is mandatory and max 280 chars. One line. If it takes two lines,
   the block is not understood yet — do not emit it; distill first.
2. `kind` is mandatory. Choose the closest of: doctrine, lesson, briefing,
   technical, proposal, story, metric.
3. `views` needs at least one entry, but NEVER all five by default. Select by
   kind × audience (see §3). A forced view is a defect — report it as one.
4. `layers`: each layer must pass the test — *does this change what the reader
   understands or does?* If not, cut it. `execution_prompt` only when there is
   something to fire.
5. `proof`: every verifiable claim gets a smart link (label + url). A block
   that asserts without proof is CANDIDATE at best.
6. `as_of` is mandatory (RFC 3339). A block without freshness is a fossil.
7. `truth_state` defaults to CANDIDATE. Only a ratification process moves it.

## 2. Composition guidelines per kind

Guidelines, not templates. The composer may deviate when the content demands
it, and must say why in the block's absence (a missing view is a decision).

| kind      | views (default)        | layers (default)                                              |
|-----------|------------------------|---------------------------------------------------------------|
| doctrine  | human, naya            | why_it_matters                                                |
| lesson    | human, naya            | lesson, how_to_apply                                          |
| briefing  | human                  | why_it_matters, whats_in_it_for_you, execution_prompt (if action) |
| technical | human, machine         | how_to_apply, example                                         |
| proposal  | human                  | why_it_matters, whats_in_it_for_you, execution_prompt (the decision) |
| story     | child, grandma         | example                                                       |
| metric    | human, machine         | proof-heavy: numbers in human, raw in machine                  |

## 3. View selection

- The audience decides. Known human reader → human. Mixed/unknown → human.
- `child`/`grandma` only when the kind warrants (story, explainer) or the
  reader asked for simplicity.
- `naya` when another Naya must ACT on the block (procedures, constraints).
- `machine` when a system consumes it (structured fields, refs).
- The reader can switch lenses: the Hub renders a lens switcher over
  whichever views are present. Views are alternatives, never stacked.

## 4. Ordering (intake speed)

1. title + essence (the 80%)
2. primary view (human unless audience says otherwise)
3. layers, highest-value first: why_it_matters → whats_in_it_for_you →
   how_to_apply → how_it_connects → lesson → example
4. execution_prompt (when present) — always last, always copy-paste ready
5. proof links ride inline with the claims they support, not in a footer pile

## 5. Typography contract (Hub renderer)

- title: 24. essence/subtitle: 18. body: 14.
- One idea per screen region. Whitespace is a feature.

## 6. Validation (fail-closed)

- Missing `essence` → reject.
- `essence` > 280 chars → reject (distill, don't truncate).
- `views` empty → reject.
- `execution_prompt` on kind=story/metric without an action → warn, drop it.
- `as_of` older than 24h on kind=briefing → render with a STALE badge.
- Unknown `kind` → reject. New kinds need a spec amendment, not a guess.

## 7. Worked example (briefing)

```json
{
  "id": "IB-2026-10-15-001",
  "title": "The state core is alive",
  "essence": "One file, one branch, one writer — every seat now reads the same truth.",
  "kind": "briefing",
  "topics": ["engine", "hub"],
  "views": {
    "human": "Until today every Naya compiled her own picture of the mission from six scattered sources — that's how the stale-directive incident happened. Now STATE-CORE.json is the single source: tip, venue, waves, queue, blockers, all in 6KB with freshness on every section."
  },
  "layers": {
    "why_it_matters": "Scattered state was the root cause of seats acting on different truths. One core ends that class of failure.",
    "whats_in_it_for_you": "The Hub stops showing October 2nd as live — the receiver finally gets a live sender.",
    "execution_prompt": "Wire the directive generator to compile from the core (additive path, parity-checked, no live flip until proven)."
  },
  "proof": [
    {"label": "STATE-CORE.json on live/mission-state", "url": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/live/mission-state/STATE-CORE.json"}
  ],
  "truth_state": "CANDIDATE",
  "as_of": "2026-10-15T17:14:05Z"
}
```

Note what is absent: no child view (a briefing for the team doesn't need one),
no grandma view, no machine view, no example, no lesson layer. Each absence is
a decision. The block is complete because it is sparse.
