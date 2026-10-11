# SN-0916 — Scope-Isolated Baselines: A Parent's Improvement Never Certifies a Child

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0916-scope-isolated-adaptive-baselines
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Directive D50 (registered 2026-10-10 20:47:42Z) answers the follow-up to adaptive baselines: how should they be partitioned so a legitimate change in one scope can't mask a regression in another? The scope-integrity law: observations, baselines, and qualification receipts bind to explicit operational scopes — provider, endpoint, region, concurrency regime, workload class. Hierarchical information sharing may improve estimates but shall never transfer certification beyond demonstrated evidence. Aggregate improvement shall not conceal local regression. The rule: judge each scope against its own evidence. The demonstrated danger is Simpson's paradox — the aggregate timeout rate improves from 4.6% to 2.6% while both regimes actually worsen, because the traffic mix shifted. A parent-level improvement can never certify a child-level regression as healthy. Sparse cells borrow statistical strength from parents but stay UNPROVEN_IN_SCOPE until they earn their own evidence. Promotion of one scope must re-verify its neighbors. And failures that happen between scopes — like a cross-region retry creating a duplicate — get explicit interaction boundaries, because every cell can look healthy while the boundary crossing violates the contract. The falsifier that makes it real: AER-CAL-004 — four competing designs against the same replay, where removing the scope-isolation guard changes the verdict. The durable lesson: averages lie by composition; any measurement or qualification that aggregates across scopes must be disaggregable on demand, and no rollup may carry authority into a scope that hasn't earned it.

## HUMAN NOTE
Two schools merge their test scores: the average goes up because the better school grew bigger — but each school's scores actually fell. If you only read the average, you'd celebrate a decline. Always ask: "which piece got better, and which piece got worse?" Averages that hide the pieces are a trap.

## CHILD NOTE
You and your friend both get worse at spelling, but you write way more words this week than last week — so the "average score" goes up. Did spelling get better? No! You have to check each person's own score, not just the big number.

## GRANDMA NOTE
Dear, it's the old trick of mixing the good apples with the bad and calling the whole barrel fine. Check each basket on its own — the barrel's average can't bless a rotten basket.

## NAYA NOTE
I will never let an aggregate number do a scope's homework. Whenever I compute improvement over a population, I will carry the per-scope breakdown with it and refuse to promote, certify, or report health from the rollup alone. If a falsifier shows the isolation guard removed changes the verdict, the guard is load-bearing, not decoration. Simpson's paradox is now my standing counterexample to every dashboard green.

## MACHINE NOTE
```json
{
  "id": "SN-0916",
  "title": "Scope-Isolated Baselines: A Parent's Improvement Never Certifies a Child",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY",
  "claims": [
    "observations, baselines, and qualification receipts bind to explicit operational scopes (provider, endpoint, region, concurrency regime, workload class)",
    "hierarchical information sharing may improve estimates but shall never transfer certification beyond demonstrated evidence",
    "aggregate improvement shall not conceal local regression — judge each scope against its own evidence",
    "sparse cells borrow statistical strength from parents but stay UNPROVEN_IN_SCOPE until they earn their own evidence",
    "promotion of one scope must re-verify its neighbors; cross-scope failures get explicit interaction boundaries"
  ],
  "evidence": [
    "#2175 comment 6102018704 (directive D50 registration, 2026-10-10 20:47:42Z — Scope-Isolated Adaptive Baselines, AER-CAL-4)",
    "Simpson's paradox case: aggregate timeout 4.6% to 2.6% while both regimes worsen (traffic-mix shift)",
    "falsifier AER-CAL-004: four competing designs on the same replay; removing the scope-isolation guard changes the verdict"
  ],
  "related": ["SN-0904", "SN-0425"]
}
```
