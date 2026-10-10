<!-- PR template — fill in every section. Delete a section only if it truly doesn't apply, and say why. -->

## 1. Plain-words summary
<!-- What changed, in words a non-technical human understands: what happened, what's going on, should anyone be concerned. (Operating Law 2.1) -->
[fill in]

## 2. Objective
[What this PR is for — one or two sentences.]

## 3. Decision calculator
<!-- The math behind the approach. Required for any non-trivial change. (Operating Law 1.2, 1.4) -->
- **Objective:** [ ]
- **Options considered:** [as many as are real — never ritualistically three]
- **Option A:** [summary] — pros: [ ] / cons: [ ] — score: [ ]/10
- **Option B:** [summary] — pros: [ ] / cons: [ ] — score: [ ]/10
- **Winner:** [ ] — chosen by the numbers because: [ ]
- **Gate check:** [ ] PROHIBITED / [ ] NEEDS_AUTHORITY / [ ] NEEDS_EVIDENCE / [x] ADMISSIBLE
- **Falsifier:** [the concrete evidence that would prove this decision wrong]

## 4. Evidence the change landed
<!-- Claims carry sources. A PR that can't prove its change landed is a claim, not a delivery. (Operating Law 4.6, 8.3) -->
- [ ] Diff reviewed against the actual base (not memory): base SHA [ ]
- [ ] Tests: [green on head SHA ___ / not applicable because ___]
- [ ] Proof the change is IN the branch: [blob SHAs / test output / render — what did you check?]

## 5. Scorecards
<!-- Both halves of the review. (Operating Law 5.4) -->
- Quality scorecard ref: [ ]
- Compliance scorecard ref: [ ]
- Activation receipt ref (work done activated): [ ]

## 6. Delivery gate (all five, or don't send)
<!-- Operating Law 2.2 — check each honestly. -->
- [ ] Useful — this does something someone needs
- [ ] Valuable — the value exceeds the review cost
- [ ] On-brand design — matches the design doctrine (or N/A: no user surface)
- [ ] Accurate — every claim above is true to the evidence
- [ ] Aligned with intent — this is what was actually asked for

## 7. Risks and reversibility
- Risks: [ ]
- Reversible in one commit? [yes / no — if no, human gate required]
