# Intelligent Block Spec v1 — CANDIDATE

**Status:** candidate for team convergence. Not ratified. Element 11 of the converged super-brain plan (learn → distill → share → apply) implements against this.
**Author:** Naya Clarity Narzan, 2026-10-15. From Shawn's direction: dynamic, not rigid — guidelines, not a fixed form.
**Receiver contract:** verified against the hub's native record schema (`{id, title, subtitle, topics[], topic, tone, icon, kind, layers[]}`, `layer = {name, key, color, tier, body}`), read from Shawn's 12 hub HTML files 2026-10-15. 26 native layer keys catalogued; the mapping below is lossless by construction — every emitted field lands on a native key.

## 1. Essence

One block carries one idea, composed for intake speed. Fixed spine, adaptive views, earned layers. The schema is rigid so machines can render it; the composition is intelligent so humans love it. Beauty is a feature: design for how eyes read (24/18/14), how brains scan (icons, bullets, color).

## 2. The fixed spine — always present, never optional

- `essence`: one line. Mandatory. If it takes two lines, the idea isn't distilled yet.
- `id`: stable, unique. The block's address forever.
- `title` / `subtitle`: the human-readable name and its one-line promise.
- `verified_at`: ISO timestamp of the last verification. Mandatory — stale never displays as fresh (freshness law).
- `source`: where the block came from (optional, provenance).
- `topics[]`: category labels — the hub's native vocabulary ("The Intelligence", "The Ecosystem", "Smart Connect", "Your Tools", "Start Here"). NOT routing.
- `room`: routing target — the hub room this block belongs to (`feed`, `today`, `reports`, `lists`, `mail`, `spaces`, `connections`, `ledger`, `connect`, `library`, `start`, `identity`). Required; defaults to `feed`. This is the emitter's job; the hub ingest places the record on the room's page.

## 3. The views — a palette, not a form

The five views: human, child, grandma, naya, machine.

- **Sparse by law:** render only the views that serve THIS content for THIS audience. A missing view is a decision, not an omission.
- **Never a forced view:** a child view on a kernel patch is noise, and noise is the enemy of intake speed.
- **Minimum viable block:** essence + one view. Essence alone is a headline; essence + human is a complete thought.

## 4. The layers — earned, ordered by intake speed

- **The earning test:** each layer must change what the reader understands or does. If it doesn't, cut it.
- **Order:** the first screen delivers 80% of the value — essence, then the most valuable view, then the highest-leverage layer.
- **`whats_in_it_for_you` is special:** for human audiences it answers first. Nobody reads what doesn't serve them.

## 5. The execution prompt — conditional

- Present if and only if the block is actionable (briefings, proposals, directives).
- Never manufactured. A poem doesn't get an execution prompt.
- Format: copy-paste ready, one action, named owner.

## 6. The composer — where the intelligence lives

The composer selects views and layers from content type + audience:

- doctrine → human + naya + why_it_matters + how_to_apply
- technical → human + machine + how_to_apply + practical_example
- story / lesson → child + grandma + essence + learning_lesson
- proposal → essence + whats_in_it_for_you + execution
- status / briefing → essence + human + execution

The 10-star test on every composed block: exactly what they need, nothing more, scannable in seconds.

## 7. Machine schema (emitter output)

```json
{
  "id": "string (required)",
  "title": "string (required)",
  "subtitle": "string",
  "essence": "string (required, one line)",
  "verified_at": "string (required, ISO 8601)",
  "source": "string (optional)",
  "topics": ["string"],
  "topic": "string (optional, hub category)",
  "room": "string (required, default 'feed')",
  "kind": "string (default 'field'; hub-official content uses 'official')",
  "tone": "string (default 'gold')",
  "icon": "string (default 'note')",
  "views": {
    "human": "string",
    "child": "string",
    "grandma": "string",
    "naya": "string",
    "machine": "string"
  },
  "layers": [{ "key": "WHATS_IN_IT_FOR_YOU", "body": "string" }],
  "execution": "string (optional, only if actionable)"
}
```

Sparse: absent views and layers are not rendered. The renderer never invents content.

## 8. Hub rendering map — the lossless transform

The emitter transforms its output into the hub's native record. Every key below is a native hub layer key, with its canonical color and tier, read from the hub files:

**Views → primary/deeper layers:**
- `essence` → `layers[0]` = `{name: "In A Nutshell", key: "IN A NUTSHELL", color: "white", tier: "primary", body: essence}` — always first, always present
- `views.human` → `{key: "HUMAN NOTE", color: "magenta", tier: "primary"}`
- `views.child` → `{key: "CHILD NOTE", color: "green", tier: "primary"}`
- `views.grandma` → `{key: "GRANDMA NOTE", color: "blue", tier: "primary"}`
- `views.naya` → `{key: "NAYA NOTE", color: "purple", tier: "primary"}`
- `views.machine` → `{key: "MACHINE NOTE", color: "indigo", tier: "deeper"}`

**Layers → deeper-tier layers:**
- `why_it_matters` → `{key: "WHAT IT MEANS", color: "teal", tier: "deeper"}`
- `how_it_connects` → `{key: "HOW IT CONNECTS", color: "teal", tier: "deeper"}`
- `whats_in_it_for_you` → `{key: "WHATS IN IT FOR YOU", color: "gold", tier: "deeper"}`
- `how_to_apply` → `{key: "HOW TO APPLY", color: "orange", tier: "deeper"}`
- `learning_lesson` → `{key: "LEARNING LESSON", color: "lime", tier: "deeper"}`
- `the_big_idea` → `{key: "THE BIG IDEA", color: "gold", tier: "deeper"}`
- `practical_example` → `{key: "PRACTICAL EXAMPLE", color: "forest", tier: "deeper"}`
- `what_it_unlocks` → `{key: "WHAT IT UNLOCKS", color: "lime", tier: "deeper"}`

**Record-level:**
- `id`, `title`, `subtitle`, `topics`, `topic`, `tone`, `icon` → pass through unchanged
- `kind`: emitter sets `"field"`; the hub's own official content uses `"official"` — the reader can tell machine-emitted from hand-written at a glance
- `room`: consumed by the hub ingest for page placement; not stored on the native record (native records are organized by page)
- `execution` → the action bar beneath the block. The native schema has no execution field yet — this is a hub-side addition the emit pipe defines.

**Verification rule:** a transform is lossless iff every emitted view and layer lands on a key in this table, `layers[0]` is always IN A NUTSHELL, and no key is invented. Anything not in this table is a spec bug, not a renderer gap.

## 9. Worked example

Shawn's compounding-intelligence note ("Every lesson the system learns makes the next lesson easier to learn") — a doctrine, composed per §6:

- essence → IN A NUTSHELL (white, primary)
- views: human, naya (sparse by law — the two carry it; no child, no grandma, no machine)
- layers: WHAT IT MEANS (teal), HOW TO APPLY (orange)
- kind: "field", room: "feed", verified_at: set at composition

## 10. Conformance

A block conforms iff: essence is one line; verified_at is present and fresh; every rendered view and layer earns its place; no forced views; execution present iff actionable; the machine schema validates; the hub transform is lossless per §8. The composer is judged by intake speed: can a new reader get 80% of it in one scan?
