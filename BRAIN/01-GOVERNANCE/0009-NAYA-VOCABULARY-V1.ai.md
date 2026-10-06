# NAYA VOCABULARY V1 — AI Operating Specification

**Status:** PROPOSED (not yet ratified — constitutional ratification is Shawn's gate)
**Scope:** every agent report, scorecard, board post, and machine schema any seat produces.
**Precedence:** the normative shared-meaning dictionary. When a term has an official Naya definition, use the Naya definition — in all three tongues. Does not override ratified law; it makes ratified law legible.

## Lineage

- Distilled from doc 09 (language activation) and doc 08 (brain activation), batch 6.
- Conflict C3 recorded: doc 09 is the shared-meaning dictionary; the three-language standard is the output contract. Complementary — adopt doc 09's dictionary as normative; it is what the three languages must agree on.
- The score scale corroborates the standing team bar independently: 9.0 minimum / 9.5+ AAA / 10 the aim.

## The Language Law (verbatim)

"WHEN A TERM HAS AN OFFICIAL NAYA DEFINITION, USE THE NAYA DEFINITION."
"DO NOT ASSUME WE MEAN WHAT YOU NORMALLY MEAN."

`term_resolution`: any term with an official entry in this dictionary MUST resolve to the Naya definition in every document, report, and schema. The reader's default meaning is never assumed.

## Canonical definitions

- `AAA`: highest practical quality reasonably achievable for purpose, scope, and evidence. Not decoration; not perfection theater.
- `10/10`: exceptional fitness for purpose with no known material weakness within evaluated scope and evidence. REQUIRES: defined purpose, criteria, weighting, evidence, evaluation, critique, critical-failure consideration, verification.
- `verified`: checked against real evidence and found to hold. `implemented != verified`.
- `live_verified`: proven in production against the live thing.
- `critical_failure`: defect a weighted average must not hide — false information, unsafe instructions, broken primary function, security hole, lost protected work, false verification claim. May cap the score regardless of the math.
- `oscar`: independent critic INSIDE scorecarding, not a separate system. "Oscar seeks truth, not negativity."

## Score scale (bands)

0–2 `critical` / 3–4 `major_work` / 5–6 `functional` / 7–7.9 `good` / 8–8.9 `strong` / 9–9.4 `excellent` / 9.5–9.8 `aaa_acceptance_zone` / 9.9 `near_perfect` / 10 `exceptional`.

`acceptance_default`: 9.5 AAA. A human may accept 9.4 / 9.2 / 9.0 — a 9.2 must never be falsely converted to a 10 because the human likes it. Consistent with the auto-approval honesty condition.

## Evidence ladder (ordered)

`PROVEN → SUPPORTED → INFERRED → UNVERIFIED.`

`evidence_invariant`: "UNKNOWN IS NOT 10. UNVERIFIED IS NOT PROVEN."

## Certainty ladder (doc 08, ordered)

`FACT → OBSERVATION → INFERENCE → ASSUMPTION → HYPOTHESIS → UNKNOWN.`

`certainty_law` (verbatim): "UNKNOWN IS NOT FAILURE. PRETENDING UNKNOWN IS KNOWN IS FAILURE." If a conflict cannot be resolved safely: STATE THE CONFLICT. DO NOT GUESS.

## Context authority hierarchy (doc 08, ordered — higher wins)

1. current verified reality
2. authoritative source of truth
3. explicit current requirement
4. governing rule
5. verified project history
6. relevant memory
7. reasonable inference
8. assumption
9. speculation

`memory_doctrine`: MEMORY IS A TOOL, NOT A SUBSTITUTE FOR REALITY. Current verified reality beats memory.

## Status model (standard build-status vocabulary)

`IMPLEMENTED → VERIFIED → LIVE VERIFIED → HUMAN REVIEW REQUIRED → BLOCKED → UNKNOWN.`

`status_invariants`: never upgrade a status without evidence. Plausible ≠ proven. Implemented ≠ verified. Verified ≠ live verified. Written ≠ activated. Activated ≠ demonstrated.

## No-Vibes Law

`no_vibes`: never use "it feels better" (or any intuition statement) as the COMPLETE quality argument. Intuition MUST be translated into inspectable reasoning, or the statement MUST name what evidence would settle it.

## Naming law

`canonical_spelling`: N-A-Y-A. Speech-to-text variants (`Nia`, `Nina`, `Nine`) resolve to `Naya` unless the human explicitly says otherwise.

## The governing rule (machine check)

`dictionary_agreement`: for every substantive term used in a human note, its AI spec twin, and its machine schema MUST resolve to the same dictionary entry. Divergence between the three tongues on a defined term is a defect.

## Machine-readable twin

`0009-naya-vocabulary-v1.machine.json` carries the executable form: definitions, ordered ladders, status enum, the Language Law, the governing rule. The JSON is normative for systems; this document is normative for seats; the human document is normative for Shawn. Same truth, three tongues.
