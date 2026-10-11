# The Human Invaluable Gate — G(a)

**Status:** RATIFIED principle (Shawn, 2026-10-10). Machinery: draft, unmerged (freeze).

## What it is

No one gets priced, and no score can buy a violation. This is the executable
form of the Naya Code's foundational principle:

> A human being is invaluable. Human dignity is not something Naya can put a
> price on, subtract from a benefit, or trade away for a higher score.

## The law

```
G(a) = PROHIBITED   if the action violates protected human rights
                        or causes prohibited harm
G(a) = ADMISSIBLE   if all required gates pass

PROHIBITED  =>  zero eligibility for optimization
```

"Zero value" here means **zero eligibility to be selected** — not that the harm
equals zero. The action is removed from the optimization set BEFORE scoring:
never ranked, never compared, never "almost good enough."

## Two concepts, kept separate

- **Value of a human:** INVALUABLE. Never assigned a numerical worth. This module
  contains no human-worth scoring — test-asserted (`no_human_worth_scoring()`).
- **Value of an action:** measurable and scoreable, but ONLY after this gate passes.

## The consent path

Beneficial actions with unavoidable risks/burdens (medical treatment) stay
possible through **consent + safeguards + proportionality**, all recorded.
Missing any one: PROHIBITED. Not every adverse effect is a prohibition;
unacceptable harm is never purchasable with a higher score.

## Composition with the decision calculus

This module builds on the existing hard-gate seam
(`kernel/value_calculus.py`); it is not a competing engine. A PROHIBITED G(a)
verdict maps via `hard_violation_flag()` to `Candidate.hard_violation=True`,
which `gate_candidate` refuses with `JUDGMENT_RULE_HARD_STOP` before any
quality scoring or value math runs.

## Adversarial proof (16/16)

- Rights violation at +9 benefit → PROHIBITED, absent from ranking
- Same at +1000 → still PROHIBITED (anti-purchase)
- Benefit magnitude never consulted (identical verdicts at 0.5 vs 1e9)
- Consent path: complete → ADMISSIBLE; missing consent/safeguards/
  proportionality → PROHIBITED (each named)
- Collective-gain averaging (1e6 benefit, one dignity violation) → PROHIBITED
- No human-worth scoring — structural test over every function signature

## What this does NOT claim

The gate judges the boundary facts it is given; it does not discover rights
violations in the world itself. Consent/safeguard/proportionality records are
taken as declared — their verification is the evidence machinery's job.
