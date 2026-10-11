# Evidence-Graded Claims — UD-06 (absorbs D15, D16)

`tools/evidence_graded_claims.py` — every claim carries exactly the evidence
that covers it. No more, no less.

## What it does

1. **Decomposes** a claim into proof obligations, each with a predicate and a
   required scope (environment, time, population, runtime, policy, provenance).
2. **Matches** evidence to obligations. Evidence covers an obligation only if
   it is admissible, asserts the same predicate, and demonstrates every
   required scope dimension. Staging evidence never covers a production claim.
3. **Grades** each obligation: SUPPORTED / REFUTED / CONFLICTED / UNDETERMINED.
4. **Gates composition**: all supporting evidence must agree on every scope
   dimension it demonstrates, or the parts cannot be combined into one
   conclusion. Overlapping sources are deduplicated by content hash — never
   double-counted.
5. **Grades the claim**: PROVEN (full coverage + compatible + valid
   composition + verification-kind artifacts throughout), SUPPORTED (partial,
   precisely narrowed), CONTESTED (a counterexample exists — it cannot be
   outvoted), UNKNOWN (no admissible covering evidence).
6. **Refuses inflation**: `assert_claim(claim, grade)` raises `ClaimRejected`
   whenever the asserted grade exceeds the evidence. Unknown is never
   converted into a PASS.
7. **Stamps non-claims**: every verdict carries DOES NOT CLAIM — exactly what
   is not established.

## The sharp rules

- Only verification-kind artifacts (`test_run`, `measurement`, `inspection`,
  `external_record`) can carry a claim to PROVEN. Reviews and bare assertions
  cap at SUPPORTED.
- A verified counterexample cannot be outvoted by any number of positive
  examples.
- QUALIFIED = Coverage ∧ Admissibility ∧ Compatibility ∧ Composition-validity.
- `require_nonclaims(text)` rejects summaries that state claims without
  stating what is NOT claimed.

## Run the tests

```
cd tools && python3 -m unittest test_evidence_graded_claims -v
```

16 tests: 4 positive (proven / narrowed partial / review cap / underclaim
allowed), 8 negative (verified-without-artifact, unknown→pass, staging→
production, 8-of-9, outvoted counterexample, incompatible contexts,
double-counting, inadmissible evidence), 4 stamping (non-claims always
present, partial named, summary guard both directions).
