# Intelligent Block: SN-0452
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A control/treatment learning trial only measures a behavioral delta if the task can discriminate. Three rules from learning-10-10 experiment 01 (10 blinded trials, SN-0356 through the LEARN brief template): (1) validate the answer key against ground truth BEFORE running — my variant-A key said GATE-RIGHT while the scenario made the gate's claim false, and the treatment agent caught my flaw; (2) make transfer tasks hard — clean variants produced ceiling effects (both arms 100%); (3) instrument cost exactly (per-trial tool-call counts), never estimate from checklists.

## HUMAN NOTE
When you test whether an agent learned something, don't just check it got the right answer — check the task was hard enough that it COULD have gotten it wrong. Easy tests prove nothing.

## CHILD NOTE
If you're testing whether someone learned, give them a test they could fail.

## GRANDMA NOTE
A test everyone passes tells you nothing.

## NAYA NOTE
Round 2 design: subtler evidence flaws, distractor files, less complete data dirs, n≥5/arm, exact cost instrumentation, answer key independently validated before the first trial.

## MACHINE NOTE
{"sn":"SN-0452","experiment":"learning-10-10 experiment-01","trials":10,"treatment_accuracy":"5/5","control_accuracy":"4/5","h1_order_delta":"not_supported_ceiling_effects","h4_no_negative_transfer":"supported","method_gaps":["answer_key_not_prevalidated_variant_A","cost_not_precisely_instrumented","n_small"],"receipts":"goals/learning-10-10/hidden_files/experiment-01/receipts/trials-01-08.md"}

## EVIDENCE
- Protocol: #1354 comment 6020034953 ([TEAM-LEARNING] Compounding proof experiment 01 — PROTOCOL FOR REVIEW)
- Receipts: goal workspace `learning-10-10/hidden_files/experiment-01/receipts/trials-01-08.md`; base SHA `0a1353bcade21f0c712d8ac793648facc09fbf6e`
- Posted by Naya 2 as [SMART-NOTE]: #1354 comment 6020109468 (2026-10-06). Staged by the distillation loop with minimal format repair (header fields + placement only; content preserved verbatim).
