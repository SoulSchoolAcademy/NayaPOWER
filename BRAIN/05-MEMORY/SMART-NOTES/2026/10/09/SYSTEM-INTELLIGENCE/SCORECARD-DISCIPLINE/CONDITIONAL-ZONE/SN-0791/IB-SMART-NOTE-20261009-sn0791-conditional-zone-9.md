# IB-SMART-NOTE-20261009-sn0791-conditional-zone-9.md

Intelligent Block: SN-0791
Truth state: CANDIDATE (from unratified Collective Agreement v2.0 — proposed, NOT standing law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: PDF distillation 2026-10-09, doc 5 (`NAYA_COLLECTIVE_AGREEMENT.pdf` v2.0), §IX "9.0–9.49 conditional zone"; distilled to `~/workspace/design-intake/pdf-distillation-2026-10-09.md`.

## IN A NUTSHELL

Standing law: nothing below 9.0 reaches Shawn. Doc 5 §IX adds the missing upper half: **9.0–9.49 is not "pass" — it's conditional.** It may proceed *only* where the governing human explicitly accepts the tradeoff, and the reason is recorded. "A score of 9 is not excellence. It is the minimum conditional floor." And the standing question: **"WHY IS THIS NOT A 10?"** This changes the decision at 9.2: today we ship it; under this doctrine we ship it only with Shawn's explicit, recorded acceptance of what's missing — or we keep working. **Do not cite as law** — v2.0 is unratified; formal supersession of V1 is PROPOSED per its own §22.

## HUMAN NOTE

Think of a building inspection. The code says 90% is the minimum to occupy — but "minimum to occupy" isn't "excellent construction." Right now, the moment we hit 9.0 we act like we built something excellent. This note says: 9.0 to 9.49 means "good enough to use *if* the owner knows exactly what's unfinished and says yes anyway." The owner — Shawn — has to see the gap and explicitly accept it, in writing. No silent 9.2s.

## CHILD NOTE

Imagine you get a B+ on a project. Your teacher says "good enough to pass" — but she also writes down exactly what would have made it an A, and your parents have to sign that they saw it. That's the rule here: a 9-point-something isn't failing, but it's not excellent either. The grown-up in charge has to look at what's missing and say "I accept this" out loud, not just wave it through.

## GRANDMA NOTE

It's the difference between "it'll do" and "it's done right." We've been treating "it'll do" as "done right" the moment the number crosses 9. This note puts the honesty back: if it's a 9.2, say what's keeping it from 10, let Shawn decide if that gap is acceptable, and write down his answer. Plain dealing.

## NAYA NOTE

This is the Scorecard Law applied to the score itself (AGENTS.md L179): a number without the method, evidence, and limitations is not a score — and a 9.x without the named gap to 10 is a number without its limitations. The conditional zone operationalizes "WHY IS THIS NOT A 10?" as a required field on every 9.0–9.49 scorecard: the gap named, the tradeoff stated, the human's acceptance recorded. Below 9.0: repair. 9.0–9.49: conditional on acceptance. 9.5+: AAA. 10: the aim.

## MACHINE NOTE

```yaml
score_zones:
  below_9_0: "REPAIR — does not proceed"
  9_0_to_9_49: "CONDITIONAL — proceeds only with governing human's explicit recorded acceptance of the named gap"
  9_5_plus: "AAA"
  10: "the aim"
required_field: "WHY_IS_THIS_NOT_A_10 (named gap + tradeoff + acceptance record)"
status: "CANDIDATE — v2.0 unratified; do not enforce as law"
```

## LEARNING LESSON

A threshold without a zone above it becomes a ceiling everyone rests on. The conditional zone keeps 9.0 honest: it's the floor you may stand on, not the roof you stop under.

## HOW IT CONNECTS

- Extends the standing 9.0 bar (MEMORY.md: "nothing below 9.0 is acceptable or ships").
- Pairs with AGENTS.md L179 (score receipts carry method): the gap-to-10 is part of the method.
- The "governing human" is Shawn per the conflict hierarchy (MEMORY.md) — his acceptance, not a seat's.
- If ratified, this becomes the scorecard schema's required field for all 9.x scores.

## EPISTEMIC STATE

**CANDIDATE — with a warning.** Source is Collective Agreement v2.0, which is explicitly UNRATIFIED. Per its own §22 and the governance record, v2.0 procedures are working conventions only; formal supersession of V1 is PROPOSED. **Never quote this as standing law.** It is preserved here so the decision isn't lost while ratification is pending.

**Falsifier:** if Shawn ratifies v2.0, this becomes law (update truth state). If he rejects §IX, retire the note.

## UNCERTAINTY

- Whether "governing human" could ever be someone other than Shawn (no — per conflict hierarchy, but unstated in §IX).
- Whether the acceptance must be per-instance or can be a standing acceptance for a class (likely per-instance; unratified text doesn't say).
- Interaction with the Scorecard Law's auto-merge grant: does a 9.2 merge require his explicit acceptance each time? (Presumably yes — that's the point.)

## APPLICABILITY

Every scorecard scoring 9.0–9.49, if/when ratified. Until then: use as a recommended discipline, labeled CANDIDATE.

## SUCCESSOR EFFECT

A cold Naya scoring her first 9.2 doesn't quietly ship it — she names the gap, records the tradeoff, and seeks the acceptance. The bar stays a bar instead of sagging into a habit.
