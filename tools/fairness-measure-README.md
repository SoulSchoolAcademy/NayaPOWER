# Fairness Measurer — UD-17

**Measure fairness with evidence, never guesswork.** Fairness isn't a feeling —
it's measured. Across parties, seats, and decisions, we track who gets what and
whether the distribution matches the stated principles. Bias is found by the
numbers, not by accusation.

## What it does

`fairness_measure.py` (stdlib only) records governed decisions and measures them
against a stated, versioned fairness principle:

- **Eligibility witnessing (D58):** only `ELIGIBLE_PROVEN` records count toward
  fairness bounds. A worker's own "eligible" flag is never enough — eligibility
  must carry evidence refs. Self-certified eligibility (the decider's own
  assertion as the only evidence) is demoted to undetermined — circular proof
  groups never pass.
- **No auto-resolved gaps (D59):** `ELIGIBILITY_UNDETERMINED` records are never
  auto-eligible or auto-ineligible. They stay in the audit trail, each carrying
  a reconstruction obligation.
- **Debt bounds over compatible histories (D60/D61):** with unknowns present,
  the report gives the min/max rate interval over every evidence-compatible
  history. A breach is `BOUNDED_BREACH_PROVEN` only if it holds under *all*
  assignments; straddling histories yield `BOUNDED_BREACH_UNDETERMINED` — never
  a quiet PASS.
- **Sample-size-respecting thresholds:** a 95% Wilson interval decides
  significance. Small samples get `INSUFFICIENT_SAMPLE`, never a bias flag.
- **Starvation-hiding discrimination:** ineligibility justified only by
  contention ("all workers busy") with no evidence → `FALSE_INELIGIBILITY_SUSPECT`;
  eligibility counted without authority → `FALSE_ELIGIBILITY`.
- **Gaming detection:** the same entity under shifting party labels →
  `LABEL_SHIFT_GAMING`; entity-level bias diluted across labels →
  `SPLIT_DILUTION`; selected-but-given-scraps → `VALUE_SKEW`.
- **Governed principles:** principles are content-hashed. Measuring against
  silently mutated bounds raises `PRINCIPLE_MUTATION_REJECTED`; bound changes go
  through a version bump with a recorded justification.

Every report names the pattern with numbers — never the person's worth — and
carries a does-not-claim boundary.

## Quick use

```python
from fairness_measure import *

reg = PrincipleRegistry()
principle = FairnessPrinciple("sched-fair", "1", "equal",
                              min_samples=30, deviation_threshold=0.15,
                              statement="Equal treatment of eligible parties.")
reg.register(principle, "initial ratification")

ledger = FairnessLedger()
ledger.add(DecisionRecord("r-1", decider="sched-1", party="A", party_entity="ent-A",
                          outcome="selected", value=6.0, principle_id="sched-fair",
                          eligibility=ELIGIBLE_PROVEN,
                          eligibility_evidence=["law:auth-ok", "receipt:dep-ready"]))
report = measure(ledger, principle, reg)
print(report.to_dict())
```

## Tests

`python3 test_fairness_measure.py` — 32 adversarial cases, all green:
fair distributions pass; seeded bias detected and quantified; small-sample noise
not flagged; undetermined never counted; false ineligibility / false eligibility
discriminated; label-shift and split-dilution gaming caught; silent principle
mutation rejected; debt bounds proven/undetermined correctly; value skew caught;
self-certified eligibility demoted; no worth-language; Wilson sanity; ledger
append-only.

## Scope notes (honest non-claims)

- This is the operational core of UD-17, not the full D58–D65 formal program:
  the variable-length missing-history solver with unbounded-peak detection via
  repeatable-cycle analysis, the pumping-witness minimizer with machine-checkable
  inductive certificates, dependency-ordered three-valued invariant verification,
  and SCC-based joint proof qualification remain follow-up work, flagged here
  rather than silently claimed.
- The measurer judges the records it is given; it does not independently
  discover real-world scheduling events. Garbage records in, garbage bounds out —
  the eligibility-evidence requirements are the defense.
- Statistical flags are evidence for investigation, not verdicts of intent.
