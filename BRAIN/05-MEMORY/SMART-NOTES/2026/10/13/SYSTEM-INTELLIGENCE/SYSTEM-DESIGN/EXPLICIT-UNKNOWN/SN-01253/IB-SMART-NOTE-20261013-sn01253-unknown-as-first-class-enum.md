# When the instrument can't know, make it say so in the schema — `unknown` as a first-class enum value

| Field | Value |
|---|---|
| Smart Note ID | SN-01253 |
| Intelligent Block | Schema design: explicit-unknown doctrine |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-13 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Provenance | Naya Mason (Lane 4), t0692-lane4 SB-Δ2 origin field, 9.0/10, mirrored on the lesson-broadcast feed t0701. Shipped in bin/ask-world.py. |
| Status | CANDIDATE — awaits Shawn's ratification. Changes no code, authorizes nothing. |

## IN A NUTSHELL

The SB-Δ2 origin field needed to record where a query row came from — but old format-1 rows carry no origin. The instinct: auto-derive `brief-driven` from the lane-N command shape. Naya Mason caught it before writing: shape-certainty is not origin-certainty, and that inference would have laundered exactly the ambiguity the field exists to expose. The doctrine she shipped: invalid values fail closed to `unknown`; old rows resolve to `unknown`; backfill-by-inference is prohibited in the docstring. The general lesson: when the instrument can't know, make it say so in the schema, not in a comment — `unknown` as a first-class enum value is the mechanism. A comment documents the gap; the enum enforces it.

## HUMAN NOTE

You're designing a form with a field "Where did this come from?" Some old records predate the field — there's no way to know their origin. The tempting move: guess from the shape. The record mentions "lane 4," so you write "brief-driven." It looks tidy. But you've just destroyed information: the difference between "we know it was brief-driven" and "we guessed it was brief-driven" is exactly the thing the field was built to preserve. The fix: make `unknown` a real, first-class value of the field — not a comment, not a footnote, a value. Anything invalid collapses to `unknown` automatically (fail closed, never fake precision), and the documentation forbids backfilling by inference. Now every consumer of the data must handle "we don't know" as a real state, because the schema forces the question. Comments can be skipped. Schema values can't.

## CHILD NOTE

You have a box with three drawers: RED, BLUE, and "I DON'T KNOW." A new rule: every toy must go in a drawer. Some old toys came before the box existed — you don't know which drawer they belong in. The wrong move: guess from the toy's shape and stuff it in RED. Then later, someone looking in the RED drawer thinks "this toy is definitely red-type" — but it was just a guess! The right move: put those toys in the "I DON'T KNOW" drawer. That drawer is just as real as the others. It's honest. And the rulebook says: never guess a drawer from a toy's shape.

## GRANDMA NOTE

Honey, this one is about honesty in record-keeping. The team added a new label to their records — where each entry came from. But the old entries were written before labels existed, and there's no way to know. The temptation is to guess from how the old entries look and fill in the label anyway. But a guess written as a fact is a lie that wears a fact's clothes — it poisons every conclusion drawn from it later. The wise move they made: create an official label called "unknown," treat it as a full citizen, and forbid guessing in the rulebook. A comment saying "we're not sure" can be ignored. A value that says "unknown" has to be dealt with by everyone who reads the record. Structure enforces honesty better than reminders do.

## NAYA NOTE

I will apply this cold on every schema I design or review. (1) Any field whose value can be unknowable gets `unknown` as a first-class enum value — never a comment, never a null-by-convention. (2) Invalid inputs fail closed to `unknown`; they never invent precision. (3) The same edit ships its backfill rule: backfill-by-inference is prohibited, stated in the docstring, and covered by a test. (4) When I feel the pull to derive a value from shape ("it looks brief-driven"), I name the near-miss explicitly: shape-certainty is not origin-certainty. This is CANDIDATE until Shawn ratifies it; until then I run it as procedure, not law.

## MACHINE NOTE

```json
{
  "id": "SN-01253",
  "type": "schema_design_doctrine",
  "doctrine": "unknown_as_first_class_enum_value",
  "rule": [
    "any_field_with_unknowable_values_gets_unknown_enum_member",
    "invalid_values_fail_closed_to_unknown",
    "backfill_by_inference_prohibited_in_docstring_and_tested"
  ],
  "near_miss_pattern": "deriving_origin_from_shape (shape-certainty != origin-certainty)",
  "evidence": {
    "seat": "Naya Mason (Lane 4), t0692-lane4, 9.0/10",
    "shipped": "origin enum in bin/ask-world.py",
    "old_rows": "format-1 rows resolve to `unknown`",
    "mirror": "lesson-broadcast t0701"
  },
  "decision_change": "schema designers encode unknowability in the type (fail-closed enum) instead of documenting it in prose; every schema change ships its backfill rule in the same edit",
  "falsifier": "downstream consumers bypassing the enum (defaulting/ignoring) at the same rate they ignored comments — the schema would then buy nothing; measure consumer-handling rates",
  "mechanism": "comments are advisory — a consumer can skip reading them; a schema enum value is structural — the consumer's code path must handle it, and invalid inputs collapse to `unknown` instead of inventing precision"
}
```
