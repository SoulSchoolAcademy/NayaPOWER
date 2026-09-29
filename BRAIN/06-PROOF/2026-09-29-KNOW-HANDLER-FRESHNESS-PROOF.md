# KNOW retrieve / inspect freshness proof

Status: SOURCE HANDLER VERIFIED. The historical missing-deployment observation below is superseded by the later reconciliation at the end.

## Exact sources

- Assessed canonical main: `99ebdb17393d90234fd5254945670f868b128639`.
- Existing freshness correction: PR #1010, merged source `275c3ed0a432096cad06df2f1ab32491b60480eb`.
- Historical failing source: `51bf655e69412a674cd211c870c92ef152a9ca83`.
- Entrypoint: `supabase/functions/nayanet-know-runtime/index.ts`, `retrieve` and `inspect`.
- Guard: `supabase/functions/nayanet-know-runtime/know.ts`, `validateKnowAuthority`.
- Test: `tests/know_runtime_handler_freshness.test.mjs`.

No runtime change is introduced here: the demonstrated correction already exists in
canonical main. This change adds actual-handler regression proof and a dated handoff.

## Failure-first evidence

The identical test file was executed in a detached historical worktree and on current
source. The historical worktree used its own index.ts and know.ts, not a simulated
replacement guard or a reverted production runtime.

Command on both sources:
`node --test --test-isolation=none tests/know_runtime_handler_freshness.test.mjs`.

Historical source: 9 passed / 8 failed, exit 1.
Current source: 17 passed / 0 failed, exit 0.

| Input / mode | Historical observed effects | Current observed effects |
|---|---|---|
| Missing, null, empty or future LAW evaluated_at / retrieve | HTTP 200; private candidate read; one success receipt write | HTTP 403 / LAW_EVALUATED_AT_INVALID; no private candidate read; no write |
| Same four cases / inspect | HTTP 200; private candidate read; no write | HTTP 403 / LAW_EVALUATED_AT_INVALID; no private candidate read; no write |
| Valid authority / retrieve | Preserved HIT/MISS | HTTP 200; exact contextual HIT/MISS; live grant read precedes owner-filtered private query; one retrieval receipt |
| Valid authority / inspect | Preserved independent reread path | HTTP 200; persisted task/result and current candidates recomputed; no write |
| Revoked, expired, wrong-owner, wrong-target or wrong-action grant / both | Existing refusals preserved | HTTP 403 with distinct live-authority reason; no private candidate read; no write |
| Wrong OIDC workflow/ref/repository, or missing bearer / both | Existing refusals preserved | No privileged read or write |
| Interrupted retrieval receipt persistence | Existing refusal to claim completion preserved | ok=false / receipt interrupted; no completed receipt returned |

The VM invokes the real Deno.serve handler with Request/Response objects and a fixed clock.
Database query mocks apply exact filter predicates and record reads/writes. JWT verification
is mocked; tests assert issuer/audience verification options and application binding checks.
They do not prove real JWT signatures, transport, database RLS or production execution.
The current invalid-time path performs receipt/grant reads before refusal; the requirement
proven is refusal before `nayanet_intelligent_blocks` access, not before authority reads.

Refusals return HTTP 403 and are not persisted by current KNOW handlers. The tests assert
zero writes; they do not invent refusal receipts. Valid mock receipt ID
`offline-retrieval-receipt` is fixture evidence only, never a production receipt reference.
Inspect recomputation is exercised offline; this session did not obtain a separate live
verifier identity or verdict.

## Full validation

- Node suite: 101 passed, 0 failed.
- Python suite: 250 passed, 3 skipped.
- `git diff --check`: passed.
- Runtime source, authority ledger, persistence boundary and OIDC implementation unchanged.

## Next proof rung / exact blocker

Fresh read-only Supabase Edge Function inventory for project `dahisasgpfvziswqvmvm`
listed LAW v2 and ACT v1 ACTIVE, but no `nayanet-know-runtime`.
No deployed KNOW revision exists in that observed inventory to bind this source proof to.
This is an observed deployment gap, not another demonstrated source-code failure.

The canonical `.github/workflows/governed-supabase-production-deploy.yml` requires
workflow_dispatch input `confirm=DEPLOY` and binds exact current main. The current user
instruction authorizes bounded source tests/correction, not production promotion.
No deployment or live proof was attempted, and no production receipt is claimed.

## Successor torch — one next authorized action

Review and integrate the handler tests, then re-resolve current main and deployment state.
For the next live rung, obtain the applicable exact-current production authorization;
use the existing governed promotion workflow and `.github/workflows/live-know-proof.yml`.
Do not request recurring human runtime credentials or invent a parallel deployment path.
Record deployed source revision, OIDC-bound positive contextual HIT, unrelated MISS,
persisted receipt IDs and fresh independent authoritative reread/recomputation.
Keep invalid-time refusals qualified as source proof until equivalent deployed evidence exists.
Stop at absent authorization, source conflict or the next failing proof rung; never
weaken freshness, owner scope, live-grant checks, caller-selection restrictions or proof gates.

## Later live-state reconciliation — 2026-09-29

KNOW is now deployed. Both the deployed entrypoint and know.ts were independently
retrieved and exactly matched canonical 56450b3f8b4c8bfc71b99518e7ad71e80f72d511
content. The same 17 handler tests pass against reconciled source based on
4259f1158c8c234c56e5dca417f9024dde5f34c7. These observations supersede the historical
missing-deployment stop above; they do not prove live contextual retrieval.
A fresh read-only database query returned no know_context_retrieval receipts.

Shawn authorizes continued bounded execution and the preceding finite activation
proposal. The next action is the existing governed bootstrap and live-know-proof.yml,
with its OIDC identity and independent recomputation. No recurring human credential
is required. Source parity, live behavior and complete promotion receipt remain
separate claims. See 2026-09-29-STANDING-PROMOTION-ACTIVATION.md on the activation
branch for the complete current evidence and boundaries.
