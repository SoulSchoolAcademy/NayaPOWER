# Standing production promotion enforcement — 2026-09-29

## Source and purpose

Audited canonical main `411f316bf5c8c91c6f98f38f8759977f317014ac`; reconciled this repair with current main `130a8ffb22e71d84b0eae6c721f6af59cbb9d35c` (tree `dc376a41fa94307be57ed1697514379ee3fb9c78`). PR #1017 already ratified the standing path. This extends its existing evaluator and workflow rather than adding a competing authority system.

Routine authorized delivery should proceed automatically. Source merge, capability, a caller assertion, or an open-ended ratification is not evidence that every production gate passed.

## Failure-first observations

Baseline files were extracted with `git show 411f316…:<path>` into an isolated directory. Eleven behavioral evaluator cases returned ALLOW when they should refuse: unresolved blocker; enforcement/proof/config changes (four cases); missing/malformed/expired policy dates (three); non-promotion operation; resolved-main drift; and missing changed-path evidence. The actual embedded CI program timed out despite successful exact-main workflow fixtures because it searched workflow names among job check names. Combined baseline: **12 failed, 6 passed**. These baseline tests use the original evaluator signature without the newly introduced optional deterministic clock.

The new full-delta/provenance tests are additional regression coverage, not counted as behavioral failures on the old code. An initial incompatible test-harness run failed on the old signature/missing new snippet; it was corrected before recording the above behavioral results.

## Small corrections

- Check real bounded review/expiry timestamps; refuse at either deadline. Keep revocation and live candidate assertions required.
- Enforce no-unresolved-production-blocker, operation scope, exact resolved-main identity, and explicit changed-path evidence.
- Exclude changes to the workflow, policy evaluator, its tests, deployment config, governance and migrations from routine standing promotion.
- Compare the complete delta from the production source stamp to the candidate, so a later routine push cannot hide an earlier undeployed protected change. Refuse missing provenance or non-ancestor baseline.
- Require successful completed push runs of both named workflows on the exact main SHA, selected through workflow-run evidence. Recheck main immediately before the production ref effect.
- Preserve authorization verdict, CI and delta evidence through the existing Actions artifact boundary even on failure.
- Reconcile the existing master execution plan with standing authorization and merged #980.

OIDC, native Supabase deployment, canonical proof, concurrency and production receipt mechanisms are preserved.

## Verification and observed effects

On the reconciled source:

- `python -m pytest -q`: **301 passed, 3 skipped** (existing skips preserved).
- `node --test --test-isolation=none tests/*.test.mjs`: **97 passed, 0 failed**.
- Workflow YAML parse and `bash -n`: **9 run steps passed**.
- New policy/CI/delta tests exercise the actual evaluator and embedded workflow programs with isolated files and mocked GitHub/git effects.
- Bounded synthetic routine candidate: ALLOW. Canonical live policy with blank validity dates: **DENY / policy_time_not_bounded**.
- No production ref update, deployment, database mutation, or persisted runtime receipt was performed by this repair. Local verdicts are test evidence; deployed parity is NOT_PROVEN.

## Current production finding

PR #980 is merged at `2f373b56aaf89ca9a2bec726de91b8b40e288df6`. Issue #978 remains open. A fresh Supabase advisor response observed `public.nayanet_checkpoint_receipts` RLS disabled at `2026-09-29T20:42:42.112Z`. The source migration ledger still records version `20260929044000` as pending production application.

Remediation reference: https://supabase.com/docs/guides/database/database-linter?lint=0013_rls_disabled_in_public

A merged migration is not a live access-control proof. Required effects: owner-read PASS; cross-owner and anon refusal; unauthorized mutation refusal; privileged reread; preserved immutability; fresh advisor verdict. Do not close #978 on source tests alone.

## Remaining authority and proof seams

The ratified artifact has `expires_at: null` and `review_after: null`; no finite activation window is recorded. Proposed window for Human Director decision: effective upon recorded activation, review `2026-10-15T00:00:00Z`, expiry `2026-10-29T00:00:00Z`, no automatic renewal. These are a proposal, not a new grant, and the canonical grant is not silently edited.

The standing policy excludes security/privacy/database boundaries and self-modification. Its own enforcement repair requires explicit bootstrap promotion; #980 requires recorded authorization for its exact access rule: authenticated owners SELECT only their own checkpoint receipts, anon none, mutation privileged/server-only. Current inspection has not resolved that production authorization from a merge alone.

The workflow still models several required claims as booleans, and issue closure alone is not comprehensive fresh security evidence. This repair does not claim independent proof of all gates, policy-ratification immutability, live expiry/revocation monitoring, arbitrary-IB Hub projection, or universal nine-node binding. The production source stamp is a baseline for the delta, not an independent proof that deployment succeeded.

## Handoff and next action

Review/CI this bounded correction. Record the finite policy window and the one-time authorization for protected bootstrap plus the exact checkpoint policy, then use the existing governed path for the resolved current SHA. Independently verify migration effects and runtime/source parity; retain receipts and workflow references before closing #978. After those gates pass, ordinary in-scope candidates use the standing path without repeated DEPLOY requests. If any next proof rung fails, preserve its exact evidence, repair the demonstrated seam, and continue unaffected work without weakening authority gates.

## Later activation and live-state reconciliation

The historical blank-date / open-#978 observations above are superseded by
`2026-09-29-STANDING-PROMOTION-ACTIVATION.md`. Human continuation authorizes the
finite proposal; #978 now has live repair evidence. Final reconciled validation:
302 Python passed / 3 existing skips and 97 Node passed. Production promotion
receipt and KNOW live behavior remain separate unfinished proof obligations.
