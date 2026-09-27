# NayaPOWER Nine-Node Kernel AAA Scorecard V1

**Status:** CANONICAL BASELINE ASSESSMENT — 2026-09-27  
**Runtime stream:** `naya/runtime-connect-convergence-v1`  
**Functional contract:** `BRAIN/03-KERNEL/0004-NINE-NODE-FUNCTIONAL-CONTRACT-V1.json`

## Scoring law

This score measures **functional readiness against the node's defined mission**, not code volume, document count, or architectural intent.

- **10.0** = mission fully executable, machine-enforced, integrated, independently verified, production-proven, and successor-proven.
- **9.5–9.9** = AAA-ready with no material known functional hole.
- **9.0–9.4** = strong but not accepted for final AAA gate.
- **<9.0** = material gap remains; no acceptance.
- **Unknown is a finding**, not a passing score.

The score must rise only when evidence crosses the relevant boundary. Documentation cannot raise a runtime score by itself.

## Current node scores

| Node | Score | Primary reason |
|---|---:|---|
| SELF | **8.0/10** | Identity and manifest identity are defined and boot-validated, but cold successor continuity is not yet proven end-to-end. |
| LAW | **8.5/10** | Consequential authority is already a runtime gate and retrieval/CONNECT cannot grant authority; broader consent/revocation/production enforcement remains to be proven. |
| ACT | **7.0/10** | Kernel records authorized execution and separates action from verification, but real governed execution and outcome closure are not yet proven end-to-end. |
| KNOW | **8.5/10** | Canonical intelligence, provenance, applicability, owner scope and read-only persistence boundary are substantially specified and exercised; live authenticated runtime proof remains blocked. |
| PROVE | **7.5/10** | Evidence/provenance contracts are strong, but the complete independent evidence chain across live runtime transitions is not yet production-proven. |
| CONNECT | **8.0/10** | Relationship-aware retrieval and verified-support behavior are implemented and focused-tested; authenticated live round-trip and behavioral improvement remain unproven. |
| VERIFY | **7.5/10** | Verification separation and failure laws are specified, but independent live causal/outcome verification is not yet complete. |
| LEARN | **6.5/10** | Candidate learning and promotion contracts exist, but verified learning changing later behavior has not yet been proven. |
| EVOLVE | **5.5/10** | Successor continuity is specified but the decisive cold-successor behavioral compounding experiment has not yet been completed. |

**Current functional readiness average: 7.4/10.**

This is **not an acceptance score**. The project target remains 9.5+ with 10.0 as the engineering objective.

## What is now machine-enforced

The runtime now requires:

1. canonical nine-node identity and order;
2. canonical functional-contract binding;
3. all required functional fields for every node;
4. fail-closed boot when the functional contract is missing;
5. fail-closed boot when node identity/order drifts.

## Cross-node AAA requirements

The nine nodes are not accepted independently merely because each has a document.

The system must prove these boundaries:

```
SELF
  ↓ identity / continuity
LAW
  ↓ authority / consent / scope
ACT
  ↓ action / observed outcome
PROVE
  ↓ evidence
VERIFY
  ↓ independently verified outcome
LEARN
  ↓ verified behavioral improvement
EVOLVE
  ↓ successor continuity / compounding
```

KNOW and CONNECT operate across this chain but cannot bypass LAW.

Required invariants:

- retrieval ≠ authorization;
- action ≠ outcome;
- outcome ≠ verification;
- verification ≠ production proof;
- learning ≠ verified learning;
- successor context ≠ inherited authority;
- graph context ≠ second source of truth;
- unknown ≠ pass;
- blocked ≠ pass.

## 10/10 acceptance for every node

A node reaches 10/10 only when all of the following are evidenced:

- functional contract complete;
- executable implementation complete;
- unit and integration tests complete;
- machine-law enforcement complete;
- authority boundary proven;
- failure and recovery behavior proven;
- canonical persistence/lineage proven where applicable;
- runtime behavior proven;
- independent verification complete;
- production boundary proven where applicable;
- cold-successor implications proven where applicable;
- no material unresolved contradiction or source/runtime drift.

## Current system blockers to 9.5+

1. Live authenticated Supabase runtime round-trip is not yet proven because the protected CI credential boundary is not configured.
2. Actual end-to-end behavioral learning is not yet proven.
3. Cold successor behavioral improvement is not yet proven.
4. Full independent causal verification is not yet proven.
5. Production proof remains separate from local/CI functional proof.
6. Sender → Receiver → Hub production continuity remains unproven.

## Highest-value sequence

1. Complete protected live authenticated persistence proof.
2. Independently reconstruct that proof.
3. Prove retained intelligence changes actual runtime behavior.
4. Verify the behavioral outcome independently.
5. Promote the verified learning.
6. Run the cold-successor experiment.
7. Prove successor behavior changes because of inherited validated intelligence.
8. Reconcile Brain AAA and Collective Chain against the working runtime.
9. Close remaining authority/refusal/revocation/replay gaps.
10. Only then run the full Super Brain race acceptance.

## Acceptance law

The nine-node kernel is not AAA because the scorecard says it is AAA.

It becomes AAA when the **actual working system** satisfies the contracts and the evidence survives independent reconstruction.

**No score inflation. No checklist PASS. No simulated proof.**
