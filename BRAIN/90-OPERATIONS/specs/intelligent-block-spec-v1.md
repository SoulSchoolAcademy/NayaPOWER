# Intelligent Block Spec v1 — CANDIDATE

**Status:** candidate for team convergence. Not ratified. Element 11 of the converged super-brain plan (learn → distill → share → apply) implements against this.
**Author:** Naya Clarity Narzan, 2026-10-15. From Shawn's direction: dynamic, not rigid — guidelines, not a fixed form.

## 1. Essence

One block carries one idea, composed for intake speed. Fixed spine, adaptive views, earned layers. The schema is rigid so machines can render it; the composition is intelligent so humans love it. Beauty is a feature: design for how eyes read (24/18/14), how brains scan (icons, bullets, color).

## 2. The fixed spine — always present, never optional

- `essence`: one line. Mandatory. If it takes two lines, the idea isn't distilled yet.
- `id`: stable, unique. The block's address forever.
- `title` / `subtitle`: the human-readable name and its one-line promise.
- `topics[]`: routing — which rooms and feeds this block belongs to.

## 3. The views — a palette, not a form

The five views: human, child, grandma, naya, machine.

- **Sparse by law:** render only the views that serve THIS content for THIS audience. A missing view is a decision, not an omission.
- **Never a forced view:** a child view on a kernel patch is noise, and noise is the enemy of intake speed.
- **Minimum viable block:** essence + one view. Essence alone is a headline; essence + human is a complete thought.

## 4. The layers — earned, ordered by intake speed

Available layers: `why_it_matters`, `how_it_connects`, `whats_in_it_for_you`, `how_to_apply`, `learning_lesson`, `the_big_idea`, `practical_example`, `what_it_unlocks`.

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

## 7. Machine schema

```json
{
  "id": "string (required)",
  "title": "string (required)",
  "subtitle": "string",
  "essence": "string (required, one line)",
  "topics": ["string"],
  "views": {
    "human": "string",
    "child": "string",
    "grandma": "string",
    "naya": "string",
    "machine": "string"
  },
  "layers": [{ "key": "WHATS_IN_IT_FOR_YOU", "body": "string" }],
  "tone": "gold",
  "icon": "note",
  "room": "feed",
  "execution": "string (optional)"
}
```

Sparse: absent views and layers are not rendered. The renderer never invents content.

## 8. Hub rendering map

- `essence` → IN A NUTSHELL (white, primary) — always first
- `views.human` → HUMAN NOTE (magenta, primary)
- `views.child` → CHILD NOTE (sapphire, primary)
- `views.grandma` → GRANDMA NOTE (emerald, primary)
- `views.naya` → NAYA NOTE (purple, primary)
- `views.machine` → MACHINE NOTE (indigo, deeper)
- `layers[].key` → the matching deeper-tier layer with its canonical color
- `execution` → the action bar beneath the block

## 9. Worked example

Shawn's compounding-intelligence note, composed per this spec:

- essence: "Every lesson the system learns makes the next lesson easier to learn."
- views: child, grandma, naya, machine (no human view — sparse by law; the four carry it)
- layers: why_it_matters, how_it_connects, whats_in_it_for_you
- execution: the copy-paste convergence prompt

## 10. Conformance

A block conforms iff: essence is one line; every rendered view and layer earns its place; no forced views; execution present iff actionable; the machine schema validates. The composer is judged by intake speed: can a new reader get 80% of it in one scan?
