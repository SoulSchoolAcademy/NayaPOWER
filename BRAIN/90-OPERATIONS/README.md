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

At evidence snapshot `eb3d018743ccdc89005600a73c99dd5885f8fdca`:

- #913, #944, #971, #978, #975 and #810 remain closed/proven only within their declared bounded scopes.
- Current Truth Resolver run `36666104446` succeeded on exact `eb3d018743ccdc89005600a73c99dd5885f8fdca` and correctly classified the prior projection as STALE because #1094/#1104 were substantive source changes.
- #1094 makes KNOW retrieval graph-aware using same-snapshot eligible edges, bounded SUPERSEDES chasing, related-context admission and explicit conflict surfacing.
- #1104 binds idempotent replay to exact request context and fails closed with `IDEMPOTENCY_KEY_REUSE_CONFLICT` on mismatched reuse.
- #1095 atomic idempotency remains source/test verified; live two-request race still requires exact deployed parity.
- Bounded two-owner collective-derived consent/revocation is production-observed: private deny → consented derived read → revoke → future derived deny; recipient-specific purpose grants are not proven.
- KNOW prior bounded live HIT/MISS remains proven at its exact revision; current main does not inherit production parity automatically.
- Current runtime source remains UNKNOWN to the truth resolver until the governed deployment/runtime evidence establishes exact parity.
- Genuine external cold entrant, true A→B→C compounding and measured human-value/MVPM remain open.

Always resolve live `main`, issue state, deployment/runtime evidence and proof receipts before acting. A later revision never inherits an older production proof automatically.

## Operating law

`UNKNOWN ≠ PASS`  
`BLOCKED ≠ PASS`  
`IMPLEMENTED ≠ VERIFIED`  
`VERIFIED ≠ PRODUCTION_PROVEN`  
`RETRIEVED ≠ AUTHORIZED`

Every executor must re-read live GitHub/runtime/Supabase evidence before acting.

## Exact next action

**Merge the exact-`eb3d018743ccdc89005600a73c99dd5885f8fdca` projection-only reconciliation and require a fresh resolver result of CURRENT / PROJECTION_ONLY_DRIFT. Continue safe ACT response-loss/partial-write recovery work in parallel. Production deployment remains an explicit Human Director boundary.**
