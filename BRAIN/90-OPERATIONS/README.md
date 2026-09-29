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

- #944: CLOSED.
- #971: CLOSED.
- Bounded production proof exists at exact source `2f468c413f4b5c6752878d94ba0f2e1fdfb60147`, proof run `36519233015` attempt 2.
- Current main must always be resolved live; later revisions do not inherit production proof.
- #810 is implemented/repository-verified but current-main production proof is pending.
- #975 recovery is implemented/repository-verified but live recovery is deployment-dependent.
- #978 is the highest-risk open seam.
- PR #980 is the prepared checkpoint-ledger RLS hardening; repository gates PASS; Human Director policy acceptance remains required.

## Operating law

`UNKNOWN ≠ PASS`  
`BLOCKED ≠ PASS`  
`IMPLEMENTED ≠ VERIFIED`  
`VERIFIED ≠ PRODUCTION_PROVEN`  
`RETRIEVED ≠ AUTHORIZED`

Every executor must re-read live GitHub/runtime/Supabase evidence before acting.

## Exact next action

**Human Director accepts or rejects PR #980's owner-read / privileged-write checkpoint RLS policy.**
