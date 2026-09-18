# Naya Power — P0 Dream History Adapter + Read-Only Replay

## Purpose
Add Dream-RSI as a governed counterfactual layer over existing cognition and execution history.

## Source-of-truth boundary
Dream reads:
- public.nayanet_cognition_events
- public.nayanet_execution_receipts

Dream does not create identity, replace memory, rewrite history, grant authority, execute external actions, or promote policy.

## P0 transaction
1. Authenticate the existing NayaNET user.
2. Select one existing cognition event.
3. Resolve its matching execution receipt when available.
4. Freeze an immutable JSONB projection as a Dream World.
5. Run a deterministic baseline/counterfactual replay.
6. Persist only the replay record in public.nayanet_dream_replays.
7. Mark the replay SIMULATED.
8. Verify the source event and source receipt remain unchanged.

## P0 strategy
Baseline: HISTORY_ONLY_V1.
Counterfactual: HISTORY_PLUS_VERIFIED_RECEIPT_V1.

The first counterfactual tests whether verified execution evidence can be recovered into decision context without changing authority, truth claims, or execution.

## Hard invariants
- SCORE != VALUE != AUTHORITY != TRUTH != VERIFICATION.
- Replay is simulation, not reality.
- No replay may execute an action.
- No replay may mutate source cognition or execution receipts.
- No replay may grant or escalate authority.
- No replay may change production policy.
- No identity or second memory system is introduced.
- Idempotency prevents duplicate replay transactions.

## P0 acceptance tests
- Auth required.
- Missing source event fails closed.
- Source event is owner-scoped.
- Source receipt is owner/project scoped.
- Replay row is owner-scoped by RLS.
- Replay is SIMULATED.
- Source history mutation is false.
- Execution performed is false.
- Authority granted is false.
- Production policy changed is false.
- Same idempotency key returns the same replay.
- Source event and receipt remain present after replay.

## Next phase
Feed verified replay learning into the existing CIS/policy path only after adversarial and regression evaluation. Do not let Dream self-promote.
