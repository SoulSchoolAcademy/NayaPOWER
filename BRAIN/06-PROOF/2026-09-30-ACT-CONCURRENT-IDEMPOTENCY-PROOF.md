# ACT Concurrent-Duplicate Idempotency Proof — 2026-09-30

**Status:** SOURCE/TEST VERIFIED — LIVE RACE PENDING EXACT DEPLOYMENT
**Current main:** `8bc2430517fc52a5722ad2a75ce036f9d8e7152e`
**PR:** #1095 — `fix(ACT): make consequential idempotency atomic`
**Merge commit:** `8bc2430517fc52a5722ad2a75ce036f9d8e7152e`

## Failure-first finding

Before #1095, consequential ACT replay protection performed a pre-read of successful receipts and searched `observed_result` for `idempotency:<key>`. The idempotency key was not a durable receipt column and no unique database claim existed at the ACT receipt boundary.

That means two identical authorized requests can both observe “no prior receipt” before either request commits. The existing revision uniqueness protects receipt revision allocation, not request idempotency. This was the demonstrated causal seam targeted by the failure-first test.

## Minimal repair

#1095 changes only the demonstrated ACT/persistence seam:

1. `nayanet_execution_receipts` gains nullable `idempotency_key`.
2. A partial unique index enforces `(user_id, project_id, action, idempotency_key)` uniqueness when a key is present.
3. Consequential execution atomically claims the key by inserting the receipt with the persisted key.
4. A unique-key loser rereads the winner receipt rather than executing again.
5. Replay still requires a persisted `nayanet_execution_outcomes` row; otherwise the response is `INCONCLUSIVE` with `IDEMPOTENT_REPLAY_OUTCOME_MISSING`.
6. No second idempotency store, authority store, or execution ledger was introduced.

## Failure-first evidence

The new concurrency contract was intentionally added before the repair and failed on pre-fix main because `idempotency_key` was not persisted at the receipt boundary.

After repair:

- `python -m pytest tests/test_verified_ai_action_runtime_contract.py -q` → **14/14 PASS**
- `node --test tests/verified_ai_action_authority_lifecycle.test.mjs` → **10/10 PASS**
- `python -m pytest -q tests/test_verified_ai_action_runtime_contract.py tests/test_cold_successor_continuity.py` → **28/28 PASS**
- `git diff --check` → **PASS**

The same tests were rerun after resetting the local clone to fresh `origin/main` at `8bc2430517fc52a5722ad2a75ce036f9d8e7152e`.

## Live-proof boundary

A real production race must not be manufactured against the stale deployed function. Doing so could intentionally create the duplicate governed effects we are trying to prevent.

Therefore the exact acceptance proof remains:

**two identical authorized requests concurrently → one durable success receipt → one execution outcome/effect → losing request replays the same persisted receipt/outcome → independent reread reconstructs the same final state.**

This proof is **BLOCKED until the exact current-main function and migration are deployed through the governed production path**. No production deployment was executed by this change.

## Canonical continuation

- Current Truth Resolver run `36664954443` succeeded against main `8bc2430517fc52a5722ad2a75ce036f9d8e7152e` but correctly classified the existing operational projection as `OPERATIONAL_PROJECTION_STALE` because the ACT repair changed substantive paths.
- Canonical Brain queue/master-plan projections have been updated to the exact merge SHA and the new Max-10 frontier.
- `LIVE_RUNTIME_SOURCE` remains **UNKNOWN**.
- Next executable canonical action: refresh the existing projection-owned Brain files, rerun the resolver, then preserve the explicit deployment boundary before the live two-request race.
