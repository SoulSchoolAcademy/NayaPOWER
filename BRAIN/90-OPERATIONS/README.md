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

At evidence snapshot `618429b1a77ceb391f179c54e40d50aedb6390f4`:

- #978 is **CLOSED / production verified**.
- #975 is **CLOSED** after independent outcome recovery run `36632538416`; North-Star audit v3 accepts the bounded historical specimen.
- #810 is **CLOSED** after live bounded nine-node behavioral acceptance + ablation in run `36632211367`.
- Governed production promotion `36631960490` is **SUCCESS** for bounded source `335bdd82568e8041d3f6921a9ee4c7bf28e2c99f`.
- The next active control-plane issue is #66.
- Current Truth Resolver run `36631904834` failed closed because stale operational projections still named closed #978 as active.
- That failure is a correct drift finding. The next repair is to reconcile the projections and preserve the conflict artifact on failed resolver runs.
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

**Issue #66: reconcile stale Brain/Operations current-truth pointers, preserve/upload resolver evidence even when conflicts fail closed, merge only with green repository gates, and require a successful main-branch Current Truth Resolver run before advancing to the authority lifecycle negative matrix.**
