# 0008 — Intelligent Block V1 (AI tongue) — CONVERGED

Converged from Naya 4's candidate spec (PR #2643) and the three-tongue draft
(PR #2644), per Shawn's synthesis principle: never merge competing drafts in
sequence — synthesize the ultimate version and merge THAT. Naya 4 contributed
the Hub rendering map (§8), the receiver presentation hints (tone/icon/room),
the beauty doctrine, and the minimum-viable-block rule. The three-tongue
draft contributed the formal machine schema, the kind taxonomy, provenance /
freshness / proof, and fail-closed validation.

The machine schema is `BRAIN/00-SPEC/SCHEMA/INTELLIGENT-BLOCK-SCHEMA.json` —
this document is the exact behavioral spec around it.

## 1. Emitter rules (engine side)

1. `essence` is mandatory, one line, max 280 chars. If it takes two lines,
   the block is not understood yet — distill first, don't emit.
2. `kind` is mandatory: doctrine, lesson, briefing, technical, proposal,
   story, metric.
3. **Minimum viable block:** essence + one view. Essence alone is a headline;
   essence + human is a complete thought.
4. `views`: at least one, NEVER all five by default. Select by kind ×
   audience (§3). A forced view is a defect.
5. `layers`: each must pass the earning test — *does this change what the
   reader understands or does?* If not, cut it.
6. `execution_prompt` only when the block is actionable. One action, named
   owner, copy-paste ready. Never manufactured.
7. `proof`: every verifiable claim gets a smart link. A block that asserts
   without proof is CANDIDATE at best.
8. `as_of` is mandatory (RFC 3339). `tone` / `icon` / `room` are optional
   receiver hints — the sender suggests, the renderer decides.

## 2. Composition guidelines per kind

Guidelines, not templates. The composer may deviate when the content demands
it. `whats_in_it_for_you` is special: for human audiences it answers first —
nobody reads what doesn't serve them.

| kind      | views (default)   | layers (default)                                              |
|-----------|-------------------|---------------------------------------------------------------|
| doctrine  | human, naya       | why_it_matters, how_to_apply                                  |
| lesson    | human, naya       | lesson, how_to_apply                                          |
| briefing  | human             | why_it_matters, whats_in_it_for_you, execution_prompt (if actionable) |
| technical | human, machine    | how_to_apply, example                                         |
| proposal  | human             | whats_in_it_for_you, why_it_matters, execution_prompt (the decision) |
| story     | child, grandma    | lesson, example                                               |
| metric    | human, machine    | proof-heavy: numbers in human, raw in machine                  |

## 3. View selection

- Audience decides. Known human reader → human. Mixed/unknown → human.
- `child` / `grandma` when the kind warrants (story, explainer) or the reader
  asked for simplicity.
- `naya` when another Naya must ACT on the block.
- `machine` when a system consumes it.
- Lens switcher: the Hub renders a switcher over whichever views are present.
  Views are alternatives, never stacked.

## 4. Ordering (intake speed)

1. title + essence (the 80%)
2. primary view (human unless audience says otherwise)
3. layers, highest-value first: whats_in_it_for_you → why_it_matters →
   how_to_apply → how_it_connects → lesson → example → big_idea → unlocks
4. execution_prompt (when present) — always last, copy-paste ready
5. proof links ride inline with the claims they support

## 5. Typography contract (Hub renderer)

- title 24, essence/subtitle 18, body 14.
- Beauty is a feature: design for how eyes read and how brains scan — icons,
  bullets, color, whitespace. One idea per screen region.

## 6. Validation (fail-closed)

- Missing `essence`, or essence > 280 chars → reject (distill, don't truncate).
- `views` empty → reject.
- Unknown `kind` → reject. New kinds need a spec amendment, not a guess.
- `execution_prompt` present but block not actionable → warn, drop it.
- `as_of` older than 24h on kind=briefing → render with STALE badge.
- The renderer never invents content: absent views/layers are not rendered.

## 7. Conformance

A block conforms iff: essence is one line; every rendered view and layer
earns its place; no forced views; execution present iff actionable; the
machine schema validates. The composer is judged by intake speed: can a new
reader get 80% of it in one scan?

## 8. Hub rendering map

- `essence` → IN A NUTSHELL (white, primary) — always first
- `views.human` → HUMAN NOTE (magenta, primary)
- `views.child` → CHILD NOTE (sapphire, primary)
- `views.grandma` → GRANDMA NOTE (emerald, primary)
- `views.naya` → NAYA NOTE (purple, primary)
- `views.machine` → MACHINE NOTE (indigo, deeper tier)
- layer keys → the matching deeper-tier layer with its canonical color
- `execution_prompt` → the action bar beneath the block
- `tone` / `icon` hints → applied when present, Hub defaults otherwise

## 9. Worked example (briefing)

```json
{
  "id": "IB-2026-10-15-001",
  "title": "The state core is alive",
  "essence": "One file, one branch, one writer — every seat now reads the same truth.",
  "kind": "briefing",
  "topics": ["engine", "hub"],
  "tone": "gold",
  "views": {
    "human": "Until today every Naya compiled her own picture of the mission from six scattered sources — that's how the stale-directive incident happened. Now STATE-CORE.json is the single source: tip, venue, waves, queue, blockers, all in 6KB with freshness on every section."
  },
  "layers": {
    "why_it_matters": "Scattered state was the root cause of seats acting on different truths. One core ends that class of failure.",
    "whats_in_it_for_you": "The Hub stops showing October 2nd as live — the receiver finally gets a live sender.",
    "execution_prompt": "Put state-core-builder.py on a 10-minute tick, verify two ticks, then flip the directive's factual sections to compile_from_core()."
  },
  "proof": [
    {"label": "STATE-CORE.json on live/mission-state", "url": "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/live/mission-state/STATE-CORE.json"}
  ],
  "truth_state": "CANDIDATE",
  "as_of": "2026-10-15T17:14:05Z"
}
```

Absent by decision: child, grandma, naya, machine views; how_it_connects,
how_to_apply, lesson, example, big_idea, unlocks layers. The block is
complete because it is sparse.
