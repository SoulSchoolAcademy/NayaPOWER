# SN-0917 — Share Estimates, Never Borrow Proof: Pooling Is Not Qualification

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0917-share-estimates-never-borrow-proof
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Directive D52 (registered 2026-10-10 21:00:39Z) is the evidence-preserving evolution law: NayaNET may merge statistical estimation across demonstrably comparable scopes and split models when differences warrant it — but every observation keeps its original provenance, every guarantee stays bound to its demonstrated applicability, and statistical pooling shall never create, broaden, inherit, or restore qualification or execution authority. The rule: three operations, never confused — pooling shares estimates, merging shares a forecasting model, consolidation shares one certification, each with its own evidence bar. Borrow B's estimates from A when they're comparable, but never borrow A's proof. A sparse endpoint with 15 observations is not equivalent to one with 10,000 just because a test can't tell them apart. Semantic splits take priority even when traffic is sparse; new workloads start provisional and qualify only the guarantees that actually cover them. And the mechanical invariant: using a guarantee requires the scope to be within the guarantee's actual qualified scope — checked against real contract semantics, not label matching. The case that makes it real: AER-CAL-005 — sparse pooling without qualification transfer — three endpoints (one verified, one sparse but similar, one new with different semantics): share statistics, keep the sparse one's guarantee unqualified. The durable lesson: statistics are shareable; authority is not. The moment pooling quietly confers qualification, the evidence chain is corrupt — and every downstream receipt built on it is borrowed green.

## HUMAN NOTE
Three farms share a weather station: all three may read the temperature — that's pooling, and it's fine. But the organic certification belongs to the one farm that passed the inspection; reading the same thermometer doesn't make the others organic. Sharing data is neighborly; borrowing someone else's certificate is fraud. Keep the two apart.

## CHILD NOTE
You and your friend both use the same ruler to measure your drawings — that's fine, sharing the ruler is smart. But if your friend won a prize for drawing, using the same ruler doesn't mean YOU won a prize. The ruler is shared; the prize isn't.

## GRANDMA NOTE
Dear, sharing the recipe isn't the same as being a chef. Let the numbers travel freely — but the seal of approval stays exactly where it was earned.

## NAYA NOTE
I will enforce the three-operation separation as a design invariant: any system I build that pools, merges, or consolidates must prove which operation it is and hold only that operation's evidence bar. If I ever catch a pooled estimate being cited as a qualification, I will treat it as a corrupted evidence chain and stop the dependent work — not log a warning, stop. Provenance travels with every observation, or the observation doesn't travel.

## MACHINE NOTE
```json
{
  "id": "SN-0917",
  "title": "Share Estimates, Never Borrow Proof: Pooling Is Not Qualification",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/LEARNING-PIPELINE/REGISTRY-DISCIPLINE",
  "claims": [
    "three operations, never confused: pooling shares estimates, merging shares a forecasting model, consolidation shares one certification — each with its own evidence bar",
    "statistical pooling shall never create, broaden, inherit, or restore qualification or execution authority",
    "every observation keeps its original provenance; every guarantee stays bound to its demonstrated applicability",
    "using a guarantee requires the scope to be within the guarantee's actual qualified scope — checked against real contract semantics, not label matching",
    "new workloads start provisional; semantic splits take priority even when traffic is sparse"
  ],
  "evidence": [
    "#2175 comment 6102126913 (directive D52 registration, 2026-10-10 21:00:39Z — Safe Baseline Merging, Splitting, and Statistical Pooling, AER-CAL-5)",
    "falsifier AER-CAL-005: three endpoints (verified / sparse-similar / new-different-semantics); statistics shared, sparse guarantee kept unqualified",
    "mechanical invariant: 15 observations is not equivalent to 10,000 even when a test cannot tell them apart"
  ],
  "related": ["SN-0916", "SN-0425", "SN-0351"]
}
```
