# Smart Note — Team Naya Communication Must Be Retry-Safe

**Date:** 2026-09-17
**Learning level:** L1 RETAINED (runtime learning remains pending)

## Observation
The first real Team Naya communication proof reached execution and failed its idempotency assertion. The emitter used the current timestamp in the event identity, so a retry of the same logical communication could produce a second event.

## Lesson
Operational communication is part of the Superbrain's durable history. It must obey the same continuity properties as governed execution: retries must not manufacture duplicate history, and handoffs must point to stable evidence.

## Adaptation
Team Naya now has a retry-safe communication facade with a deterministic idempotency key derived from the logical event payload. The facade checks the shared event index before persistence and returns `REPLAY` for an already-recorded event.

## Evidence
- `.naya/runtime/team_activity.py`
- `scripts/verify-team-naya-communication-v2.py`
- `.github/workflows/verify-team-naya-communication.yml`
- `.naya/activity/2026-09-17-NAYA-TEAM-COMMUNICATION-E2E.md`

## Remaining proof
CI run `35274452966` is queued. L2+ learning and runtime verification must not be claimed until the repaired proof actually executes and its output is inspected.

## Next action
Inspect the repaired CI run and record its actual PASS/FAIL result. If blocked/queued, repair the execution gate rather than adding more documentation.
