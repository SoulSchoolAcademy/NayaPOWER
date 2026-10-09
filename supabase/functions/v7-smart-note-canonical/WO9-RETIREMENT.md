# WO9 Retirement Record — v7 Receiver learning_evidence Write Path

**Date:** 2026-10-09
**Work order:** WO9 "One door in" (CONN-INTAKE)
**Branch:** `naya5/wo9-one-door-in`

## What was retired

The `v7-smart-note-canonical` edge function's **direct `learning_evidence` INSERT**
(the CANDIDATE write site, formerly at `index.ts` lines ~297–329).

## What was NOT retired

The receiver itself. `v7-smart-note-canonical` continues to:
- allocate authoritative live IB identity,
- persist the Smart Note via `v7_create_smart_note`,
- checkpoint via `nayanet_record_cognition_event`,
- verify feed visibility,
- dispatch GitHub projection via `nayanet-github-dispatch`,
- return the verified Smart Link.

Only the learning-store write is gone. The checkpoint invariant no longer
requires a `learning_evidence` ref from this path.

## Why it was safe

1. **Dead-end stream:** all 23 rows this path ever wrote are `RETIRED`;
   zero were ever promoted to `ACTIVE`.
2. **Quiet:** no new rows from this path in ~47h before retirement.
3. **Single writer:** `nayanet-learning-verify` (v2 canonical intake) is now
   the only `learning_evidence` INSERT site in the repo, with dedup
   (intelligent_block_id / exact-claim match, 409 on ambiguity).
4. **No live dependency broken:** the `nayanet-agent-capture.yml` workflow's
   capture pipeline (IB → persistence → checkpoint → projection → Smart Link)
   is untouched; only the candidate insert was removed.

## Canonical intake (v2)

`nayanet-intelligence-commit-runtime` (mode=execute, GitHub OIDC) →
intelligent block commit →
`nayanet-learning-verify` (candidate mode) →
`learning_evidence` CANDIDATE row with dedup key.

## Response contract change

`transaction.learning_evidence` in the v7 response is now:
```json
{"retired": true, "retirement": "WO9-2026-10-09",
 "note": "v7 receiver no longer writes learning_evidence; single writer is nayanet-learning-verify (v2 canonical intake)"}
```

## Authority-grant scope

No dedicated grant scope existed for the v7 learning write (it used the
caller's RLS-authenticated client directly). Nothing to remove.
