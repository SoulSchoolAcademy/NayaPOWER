# Team Naya Communication — End-to-End Execution Record

**Date:** 2026-09-17
**Mission:** Execute the real Team Naya communication/execution test and repair the first actual failure.
**State:** IMPLEMENTED → CI QUEUED

## Sign-in
NAYA-A is the test actor for the communication proof. NAYA-B is the receiving/continuing actor.

## What was inspected
- Existing canonical event-store path under `.naya/runtime`.
- Existing Team Naya operating contract and communication intents.
- GitHub Actions execution surface.

## First actual failure found
The first end-to-end proof exposed a retry/idempotency defect in the initial Team Naya emitter: repeating the same logical communication created a new event because the timestamp participated in the event identity.

That would allow duplicate sign-ins/messages during retries and violates the continuity requirement that execution can be safely replayed without creating duplicate operational history.

## Repair
Added a retry-safe Team Naya communication facade at `.naya/runtime/team_activity.py`.

The facade computes a deterministic idempotency key from the logical communication payload, checks the shared Activity event index for an existing event, and returns `REPLAY` instead of creating a duplicate event.

Added `scripts/verify-team-naya-communication-v2.py` to prove:
- NAYA_SIGNED_IN
- shared event index
- NAYA_DISCOVERY
- NAYA_HANDOFF
- NAYA_CONTINUING
- retry idempotency

Added `.github/workflows/verify-team-naya-communication.yml` so the proof executes on every `main` push.

## GitHub evidence
- Repair facade commit: `2ffcfc1218bd900172ba9d2575d02c2e33e780a2`
- E2E proof commit: `bdeb28be4dfb409c8f4882e6a26bae8e6897c4d9`
- CI workflow commit: `052efac9d49fa011727c6b652a0cfbf971827f4b`
- Current `main` contains the CI workflow and proof at `052efac9d49fa011727c6b652a0cfbf971827f4b`.
- GitHub Actions run `35274452966` is queued; job `105381523765` is queued. Runtime execution is therefore not yet verified by CI.

## Verification level
**CHANGED:** proven by committed source.
**TESTED:** the original CI proof executed and exposed the idempotency defect.
**REPAIRED:** source-level repair committed.
**RUNTIME VERIFIED:** pending because the repaired CI run is queued.
**LEARNED:** the communication layer must be retry-safe before it can be trusted as operational history.

## Next executable torch
NAYA-B / next Naya must inspect the queued CI run. If it completes, record PASS/FAIL from actual logs. If it remains queued/blocked, diagnose the execution gate before adding more communication features.
