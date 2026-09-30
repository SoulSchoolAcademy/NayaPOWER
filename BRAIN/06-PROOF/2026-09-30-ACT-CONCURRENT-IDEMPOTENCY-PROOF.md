# ACT Concurrent-Duplicate Idempotency Proof — 2026-09-30

**Status:** SOURCE/TEST VERIFIED — LIVE RACE PENDING EXACT DEPLOYMENT
**Source repair merge:** `8bc2430517fc52a5722ad2a75ce036f9d8e7152e` (PR #1095)
**Current canonical main:** `aaa373bd38f9ae5f7b5f549d730e1dc1f69af6bc` (PR #1116 merge)
**Source repair PR:** #1095 — `fix(ACT): make consequential idempotency atomic`
**Live-proof PR:** #1116 — `test(ACT): prove live concurrent idempotency convergence`
**Live-proof merge:** `aaa373bd38f9ae5f7b5f549d730e1dc1f69af6bc`

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

PR #1116 is now merged to canonical main and adds the live two-request concurrent proof plus an independent `verify-idempotency` reread. That establishes that the **proof mechanism exists in source**; it does not establish that production has executed it. Production currently points to `9dba0fe210d69aa8b7307f80214b675d9ae8d66d`, whose deployment stamp names source `0d0c36ab125fd8890ceffac0cd81283c658dd468`, so the live proof remains a deployment-parity gate.

A real production race must not be manufactured against the stale deployed function. Doing so could intentionally create the duplicate governed effects we are trying to prevent.

Therefore the exact acceptance proof remains:

**two identical authorized requests concurrently → one durable success receipt → one execution outcome/effect → losing request replays the same persisted receipt/outcome → independent reread reconstructs the same final state.**

This proof is **BLOCKED until the exact current-main function and migration are deployed through the governed production path**. No production deployment was executed by this change.

## Canonical continuation

- Current Truth Resolver run `36664954443` succeeded against main `8bc2430517fc52a5722ad2a75ce036f9d8e7152e` and correctly classified the operational projection as `OPERATIONAL_PROJECTION_STALE`. Canonical main has since advanced again through PR #1116 to `aaa373bd38f9ae5f7b5f549d730e1dc1f69af6bc`; the Brain projection therefore requires another current-main reconciliation before its embedded SHA can be treated as current.
- Canonical Brain queue/master-plan projections have been updated to the exact merge SHA and the new Max-10 frontier.
- `LIVE_RUNTIME_SOURCE` remains **UNKNOWN**.
- Next executable canonical action: reconcile the projection-owned Brain files to `aaa373bd38f9ae5f7b5f549d730e1dc1f69af6bc`, rerun the existing Current Truth Resolver on that exact main, then preserve the explicit deployment boundary before the live two-request race.
