# NayaPOWER — Collective Intelligence Chain Live Failure Root-Cause Receipt

**Date:** 2026-09-26
**Status:** BLOCKED_AT_EXTERNAL_DEPLOYMENT_BOUNDARY
**Workflow:** `.github/workflows/verify-collective-intelligence-chain.yml`
**Failing run inspected:** `36260942036` (merge of PR #790, head `b45b9aef6`)

## Observed failure

```
Error: INDEPENDENT_OUTCOME_ACTION_FAILED:{"ok":false,"error":"SMART_MAIL_TRANSACTION_FAILED",
"detail":"Could not find the function public.nayanet_send_smart_mail_policy_authorized(
p_authority_grant_id, p_body, p_experiment_case_id, p_idempotency_key, p_kind, p_project_id,
p_receiver_id, p_request_id, p_sender_id, p_subject) in the schema cache"}
```

Latest runs at time of inspection: `36260973477`, `36260972430`, `36260942036`, `36260890412`,
`36260815702`, `36260742623`, `36260709831`, `36260659157` — all `failure`.

## Root cause (proven, not inferred)

The database is correct and the repository source is correct. The **deployed Edge Function is
stale relative to `main`**.

Independent read-only probes against the live PostgREST boundary using only the publishable key:

| Call | Result | Meaning |
| --- | --- | --- |
| 13-parameter signature (as in `supabase/migrations/20260919005000_harden_smart_mail_authority_constraints_v1.sql` and `supabase/functions/nayanet-smart-mail/index.ts:59`) | HTTP 401 `42501 permission denied for function` | **The live function exists with 13 parameters.** |
| 10-parameter signature (as the deployed caller requests) | HTTP 404 `PGRST202`, with hint naming the 13-parameter form | The 10-parameter overload does not exist. |

Therefore the deployed `nayanet-smart-mail` Edge Function calls the RPC without
`p_policy_id`, `p_policy_input_hash`, and `p_policy_decision_hash`. Current `main` source already
passes all 13 arguments, so **no repository code change is required or appropriate for this
failure.** Weakening the workflow or the proof would hide a deployment defect.

The independent-outcome work that introduced this path is otherwise present on `main`
(`cd77d7f30`, `989df1138`, `cea828859`, `885e265a4`, `327932d94`, `c29057c95`, `c5d5b0d22`,
`580942515`, PRs #785, #787, #788, #789, #790). The chain is blocked at deployment, not design.

## Blocked boundary

Supabase project `dahisasgpfvziswqvmvm` (`ca-central-1`) must redeploy
`supabase/functions/nayanet-smart-mail` from current `main`. No repository workflow deploys
Supabase Edge Functions (no `supabase functions deploy` exists in `.github/workflows/`), and no
Supabase access token, service-role key, or management credential is present in this environment
(`SUPABASE_ACCESS_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_PASSWORD` all absent).

Per `.naya/control-plane/EXTERNAL-BLOCKER-RESOLUTION-GUIDE.md`, this is
`BLOCKED_EXTERNAL_CREDENTIAL`, not a code failure. Consistent with
`.naya/project-intelligence/ITEM-30-DEPLOYMENT-BLOCKER-RECEIPT-2026-09-24.md`, no secret was
retrieved, no deployment was attempted, and no production-parity claim is made.

## What is NOT proven

- That the collective intelligence chain completes after the redeploy.
- Any production behavior of the deployed Edge Function beyond the two read-only probes above.
- That any other Edge Function in the deployment is current; the same drift may affect peers.

## Later observation: the failure advanced to a second overload ambiguity

Run `36262162073` (2026-09-26T18:20Z) no longer fails at Smart Mail. It now fails **earlier**, in
`learning_apply`:

```
Error: LEARNING_APPLY_FAILED:{"status":500,"body":{"ok":false,"error":"SUPERBRAIN_LEARNING_COMMIT_FAILED",
"detail":"Could not choose the best candidate function between:
 public.nayanet_record_cognition_event(p_project_id => text, p_event => jsonb, p_action => text,
 p_expected_result => text, p_observed_result => text, p_learning => jsonb),
 public.nayanet_record_cognition_event(p_project_id => text, p_event => jsonb, p_action => text,
 p_expected_result => text, p_observed_result => text, p_learning => jsonb, p_execution_authorization => jsonb)",
"learner_state_version":1}}
```

This is the same class of defect as the Smart Mail failure: an **overloaded function family that
PostgREST cannot disambiguate**, not a logic error. The repository already established the correct
precedent for exactly this in `supabase/migrations/20260919182500_unique_policy_smart_mail_rpc.sql`,
whose header states that "Supabase/PostgREST RPC does not safely support this overloaded function
family" and therefore gives the policy path a unique name.

Because `learning_apply` now fails before the Smart Mail stage is reached, this run does **not**
prove that the Smart Mail drift was corrected; the Smart Mail stage remains unproven either way
until a run gets past `learning_apply`.

This is being worked in parallel and is deliberately **not** duplicated here:

- PR `#797` "fix: disambiguate cognition receipt overload in learning apply" (commit `4d1841259`,
  touches `supabase/functions/naya-learning-apply/index.ts`)
- PR `#796` "ci: introduce witnessed, manual-only Supabase Edge Function deploy workflow"

If the fix stays inside the Edge Function, note that disambiguating a PostgREST overload usually
requires a uniquely named database function, which means a **migration applied to the live
database** — the same external credential boundary described above, not a repository-only change.

## Exact successor action

An authorized Supabase operator redeploys `nayanet-smart-mail` from current `main`, then reruns
`verify-collective-intelligence-chain.yml` and inspects the run logs. Independently, the same
operator should compare deployed function source/version for the whole
`nayanet-smart-mail`, `naya-smart-feed`, and `nayanet-compound-intelligence` set against `main`,
because a single stale function is enough to keep the chain red.
