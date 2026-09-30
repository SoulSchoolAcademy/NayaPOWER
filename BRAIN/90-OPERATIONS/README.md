# Operations

**Status:** ACTIVE PROJECTION — LIVE EVIDENCE WINS

This directory owns operational projections, queues, handoffs, deployment/proof state and operator procedures. It is not a second source of truth.

## Contents

| File | Purpose |
|---|---|
| [0001-MAX-10-EXECUTION-QUEUE-V1.md](./0001-MAX-10-EXECUTION-QUEUE-V1.md) | Current maximum-value Top 10 and exact next action |
| [0002-AAA-BRAIN-EXECUTION-PROMPT-V1.md](./0002-AAA-BRAIN-EXECUTION-PROMPT-V1.md) | AAA execution protocol |
| [0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.md](./0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.md) | Dependency-correct master execution specification |
| [0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json](./0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json) | Machine projection of the master plan |
| [0004-ISSUE-944-CONCEPT-17-RECONCILIATION.md](./0004-ISSUE-944-CONCEPT-17-RECONCILIATION.md) | Historical #944 Concept #17 reconciliation evidence |
| [2026-09-28-ACTIVATION-REALITY-AND-HANDOFF.md](./2026-09-28-ACTIVATION-REALITY-AND-HANDOFF.md) | Historical dated handoff |

## Current operating pointer

At evidence snapshot `52f866d0741eb65f4030b173afc9dbf4b5da382a`:

- #978 is **CLOSED / production verified**.
- #975 is **CLOSED** after independent outcome recovery run `36632538416`; North-Star audit v3 accepts the bounded historical specimen.
- #810 is **CLOSED** after live bounded nine-node behavioral acceptance + ablation in run `36632211367`.
- Governed production promotion `36631960490` is **SUCCESS** for bounded source `335bdd82568e8041d3f6921a9ee4c7bf28e2c99f`.
- The next active control-plane issue is #66.
- #1067 semantic drift guard is canonical and exact-main verified. This refresh is anchored to current `52f866d0`; after merge, only projection-owned drift is permitted if the resolver is to report CURRENT.
- Cached-derived authority revocation is **TEST-LEVEL VERIFIED** and #1046 ACT denial coverage is merged at `7847680f`; mission semantics remain unresolved.
- KNOW bounded live proof `36658860694` is **SUCCESS** with contextual HIT, unrelated MISS, and independent persisted-universe verification.
- SN-004 learning run `36652694005` remains the last observed **NO_MEASURED_LEARNING_EFFECT** result. Production promotion `36659933566` fully succeeded for source `2ff4207a` (artifact `11074161563`), which includes the applicability-aware causal runtime; no causal-runtime file changed from that source to current `52f866d0`.
- Readiness repairs #1058/#1061 are merged. LAW's PROVE workflow binding (#1069) is deployed in production-proven source `2ff4207a`. KNOW's matching #1072 binding and #1076 handler regression are newer than production, so PROVE is blocked on deployed KNOW parity.
- #1062 source hardening is merged via #1070; migration `20260930022500` is pending/not production-applied, so live two-owner consent/revocation remains NOT PROVEN.
- #1077 Graph Relationship Contract V2 + validator/tests are merged/green. #1078 adds pending migration `20260930024000` for V2 persistence on the existing relationship table; it is not production-applied, and CONNECT edge-consumption/runtime behavior remains NOT PROVEN.
- #1044 cold acceptance is ready but has no genuinely fresh PASS receipt.
- Universal all-task nine-node capability, multi-generation compounding, and two-owner NayaNET remain **NOT PROVEN**.

Always resolve live `main`, issue state, deployment/runtime evidence and proof receipts before acting. A later revision never inherits an older production proof automatically.

## Operating law

`UNKNOWN ≠ PASS`  
`BLOCKED ≠ PASS`  
`IMPLEMENTED ≠ VERIFIED`  
`VERIFIED ≠ PRODUCTION_PROVEN`  
`RETRIEVED ≠ AUTHORIZED`

Every executor must re-read live GitHub/runtime/Supabase evidence before acting.

## Exact next action

**Issue #66: integrate this exact `52f866d0` reconciliation and require a fresh resolver run with no substantive-drift stale warning. Then explicit Human Director `DEPLOY` is required for that exact reconciled main so KNOW #1072 and #1070's pending collective migration reach production. After parity, rerun PROVE exactly once, run the bounded #1062 two-owner experiment, and run one fresh applicable SN-004 causal experiment. Coda 2 ACT replay/recovery remains independently owned.**
