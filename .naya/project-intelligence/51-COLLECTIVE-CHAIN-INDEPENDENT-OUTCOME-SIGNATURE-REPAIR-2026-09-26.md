# Receipt — Collective Intelligence Chain: independent-outcome causal repair

- Date: 2026-09-26
- Actor: NAYA (execution session)
- Board: Issue #554 (sign-in / sign-out boundary)
- Branch: `naya/smart-mail-rpc-signature-alignment`
- Commit: `9fab59d36e4283f92463b7818370d797f8b5fe51`
- PR: https://github.com/SoulSchoolAcademy/NayaPOWER/pull/792
- Status: SOURCE FIXED AND VERIFIED — NOT DEPLOYED, NOT PRODUCTION-VERIFIED

## Reconstruction

Live `origin/main` was `580942515` at session start. Five consecutive
`verify-collective-intelligence-chain` runs had failed. The board (Issue #554)
showed a parallel Naya actively iterating the same frontier, so this session
deliberately did not race it: it read the failing runs, isolated the true causal
boundary, and repaired only the boundary that was not already being edited.

## Causal finding

The proof now clears every repo-side guard and fails inside the Smart Mail
transaction. Run `36260942036`:

```
Error: INDEPENDENT_OUTCOME_ACTION_FAILED:{"ok":false,"error":"SMART_MAIL_TRANSACTION_FAILED",
"detail":"Could not find the function public.nayanet_send_smart_mail_policy_authorized(
p_authority_grant_id, p_body, p_experiment_case_id, p_idempotency_key, p_kind,
p_project_id, p_receiver_id, p_request_id, p_sender_id, p_subject) in the schema cache"}
```

This is a genuine defect, not an authority boundary and not a policy decision.

### Root cause

Supabase/PostgREST resolves `rpc()` by argument **name** against the schema
cache. The Edge Function sent `p_request_id`; no deployed SQL function declares it.

Newest definitions of both target functions declare 12 parameters and omit
`p_request_id`:

| Function | Newest definition | `p_request_id` |
|---|---|---|
| `nayanet_send_smart_mail_policy_authorized` | `20260919182500_unique_policy_smart_mail_rpc.sql` | absent |
| `nayanet_send_smart_mail_authorized` | `20260919181500_harden_authorized_mail_policy_lineage.sql` | absent |

`p_request_id` survives only in the superseded `20260919005000` definition.
`20260919182500` deliberately introduced a unique RPC surface and dropped the
parameter, but `supabase/functions/nayanet-smart-mail/index.ts` was never
updated to match. The repository was therefore internally inconsistent, and a
redeploy alone would not have corrected it.

## Change

- `supabase/functions/nayanet-smart-mail/index.ts`: removed `p_request_id` from
  both `rpcArgs` branches; removed the now-dead `requestId` / `inputRequestId`
  plumbing. Net 2 insertions, 4 deletions on one file.
- `.naya/runtime/smart_mail_rpc_signature_check.py` (new): static caller/callee
  conformance gate. It resolves each SQL function's newest definition across
  `supabase/migrations/`, extracts the argument names the Edge Function
  actually sends per branch, and fails if the function does not declare them.

## Verification

```
python -B .naya/runtime/smart_mail_rpc_signature_check.py
  policy branch: 12 declared / 12 sent  -> PASS
  default branch: 12 declared / 8 sent  (4 default null) -> PASS
  SMART_MAIL_RPC_SIGNATURE_ALIGNED            exit 0
```

Negative control, same gate against the pre-fix file recovered from git:

```
  sends undeclared parameter(s) ['p_request_id']   exit 1
```

The gate independently rediscovers the exact offending parameter on the old file
and passes on the fixed file, so it is a real gate and not a rubber stamp.

## Honest residual boundary

- The proof will **still fail** until the `nayanet-smart-mail` Edge Function is
  redeployed to Supabase. Source correctness and production correctness are
  distinct claims and only the first is established here.
- Redeploy is a production action requiring explicit authorization. It was not
  performed. No migration, deployment, or production mutation occurred.
- PR checks show only the known unrelated infrastructure failures (Vercel
  build-rate limit; repo-wide Cloudflare Workers build failures). PR is MERGEABLE.

## Next single action

Merge PR #792, then obtain explicit authorization to redeploy the
`nayanet-smart-mail` Edge Function from current source, then re-run
`verify-collective-intelligence-chain` to determine whether the independent
outcome stage clears. Do not treat any intermediate state as verified.
