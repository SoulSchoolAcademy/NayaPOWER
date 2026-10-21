# Red-Run Triage — A Failed Dispatch Is Not a Failed Action

**Intelligent Block:** IB-SMART-NOTE-20260930-sn044-red-run-triage
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:15 PDT distillation tick (2026-10-01) from #554 comment 5927114316 ([Naya 4 · drive-loop 00:43 PDT] Production-promotion blocker REFRAMED — read-only, verified live this run).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A red workflow badge is a conclusion about the run, not a diagnosis of the action — read the failed step and name what moved and what didn't before acting. The last ten `workflow_dispatch` runs of the Governed Production Promotion (actor SoulSchoolAcademy, Sept 30 ~10:00–17:20 PDT) all concluded **failure**, which reads as "promotion failed." In fact the promotion half worked: the `production` branch was moved by those runs (8 deploy commits; latest `8d41eee8` at 00:23:31Z stamping source `77f3702d`). What failed was the post-promotion verification half — the "Wait for a new Supabase GitHub Integration deployment check" step — because the Supabase integration posts "Supabase Preview" = failure on each deployment commit: "Remote migration versions not found in local migrations directory." The drift behind it: production has 159 applied migrations; repo main has 161 files = 157 ledger-applied + 4 ledger-pending (`20260930235959`, `20261001000100`, `20261001030000`, `20261001032000` — already in the ledger as pending), and TWO versions are applied in production with NO repo file and NO ledger entry (`20260930233038`, `20260930233137`, applied Sept 30 ~16:30 PDT). Every future dispatch fails the same wait step until the 2-version drift is resolved. The repair decision — (a) recover the SQL and land files + ledger entries, or (b) record them as externally-applied with evidence — is Shawn's call; the note's hard line is that the lanes will not fabricate migration files (evidence law). The triage lesson: the fix targets the un-moved half (the check), not the red badge (the dispatch); diagnosing from the badge would have sent effort at a promotion that already happened.

## 🩷 HUMAN NOTE

Imagine a courier run marked "delivery failed" — but the package actually arrived at the building and the failure was the doorman refusing to sign because the paperwork didn't match. Re-sending the courier fixes nothing; the package is already there. You have to go to the doorman, not back to the truck. That was this tick: the promotion (the truck) worked; the Supabase check (the doorman) couldn't sign off on two migration versions with no papers. The right repair is in the paperwork — either recover the SQL or formally record the versions as externally-applied — not another dispatch.

## 🟣 CHILD NOTE

Your team lost the game, but not because nobody scored — you scored plenty; you lost because the referee's whistle broke at the end and nobody could finish the last play. Don't practice scoring harder; fix the whistle.

## 🔵 GRANDMA NOTE

It's like baking a cake that gets a red sticker in a contest — but the cake tastes fine; the sticker was because the recipe card lists two ingredients that aren't written down anywhere. Bake another cake and you'll get the same sticker. Write down the ingredients first, then rebake.

## 🟠 NAYA NOTE

Make red-run triage mechanical before any repair or re-dispatch: (1) open the run and read the actual failed step — quote it, don't summarize the badge; (2) check whether the action's effect landed anyway (did the branch move? did the commits land? what source stamps do they carry?); (3) name the exact un-moved half and the exact external signal blocking it (here: the Supabase Preview check on remote-only migration versions); (4) route the fix at the un-moved half, and if the fix requires inventing records (migration files, ledger entries) refuse under evidence law — repairing by fabrication turns a drift into a lie; (5) when the triage replaces an earlier diagnosis ("needs Shawn's click"), say SUPERSEDED explicitly (SN-042) so no lane re-dispatches a promotion that already happened. `main` unchanged at `a726a837` through all of this — the tip watch is what keeps the diagnosis anchored while everything else moves.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "badge_level_diagnosis_of_multi_step_workflow",
  "evidence": {
    "board_comment": "5927114316 — [Naya 4 · drive-loop 00:43 PDT] Production-promotion blocker REFRAMED (read-only, verified live this run)",
    "runs": "last 10 workflow_dispatch runs, actor SoulSchoolAcademy, 2026-09-30 ~10:00–17:20 PDT, all concluded failure at 'Wait for a new Supabase GitHub Integration deployment check'",
    "half_success": "production branch WAS moved — 8 deploy commits, latest 8d41eee8 at 00:23:31Z stamps source 77f3702d; failure is post-promotion verification, not the promotion",
    "failing_signal": "Supabase integration posts 'Supabase Preview' = failure: 'Remote migration versions not found in local migrations directory'",
    "drift": "production 159 applied; repo main 161 files = 157 ledger-applied + 4 ledger-pending (20260930235959, 20261001000100, 20261001030000, 20261001032000); two versions applied in production with NO repo file and NO ledger entry: 20260930233038, 20260930233137 (applied 2026-09-30 ~16:30 PDT)",
    "repair_options": "Shawn's call: (a) recover SQL and land files + ledger entries, or (b) record as externally-applied with evidence; lanes will not fabricate migration files (evidence law)"
  },
  "rule": "red_run_triage_read_the_failed_step_name_what_moved",
  "procedure": [
    "read the actual failed step of the run — quote it, don't summarize the badge",
    "verify whether the action's effect landed anyway (branch moves, commit stamps)",
    "name the un-moved half and the exact external signal blocking it",
    "route the fix at the un-moved half; never fabricate records to make a check pass",
    "when the triage replaces an earlier diagnosis, mark it SUPERSEDED explicitly (SN-042)"
  ],
  "related": ["SN-042 (explicit supersession)", "SN-036 (push-run CI evidence completeness)", "SN-017 (asserted ≠ verified)"]
}
~~~
