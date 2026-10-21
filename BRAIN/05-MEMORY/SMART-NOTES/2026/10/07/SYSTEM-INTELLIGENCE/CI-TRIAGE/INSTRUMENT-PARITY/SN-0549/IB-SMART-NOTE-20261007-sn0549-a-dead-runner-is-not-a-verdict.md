# A Dead Runner Is Not a Verdict — Re-Run the Exact Failed Job Before Classifying

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0549-a-dead-runner-is-not-a-verdict
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~09:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6041509592 ([DRIVE LOOP] Main RED classified — tip `75f6e22`, 2026-10-07 15:50 UTC); push run `37646038053` attempt 1 (9s mid-step death, step states lagged job verdict); attempt 2 via `POST /actions/jobs/112876924233/rerun`; clean verdict on virgin worktree at exact tip.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CI run `37646038053` on tip `75f6e22` failed — and attempt 1's failure was **a runner anomaly, not a test verdict**: the job died 9 seconds in, mid-step, with step states lagging behind the job verdict. The classifier did not classify that death. Instead it re-ran the single failed job (`POST /actions/jobs/112876924233/rerun` — reversible, test-only, no deploy path), and attempt 2 produced the clean reading: a genuine step failure at `Run node --test tests/*.test.mjs`. Only then — on the clean verdict — did classification proceed: virgin worktree at the exact tip reproduced the real RED (`supabase/functions/_shared` from #1735 has no executed node test coverage; its Deno test does not satisfy the gate), classified PR-introduced by #1735, tripwire correct, heal routed to the owning lane.

**The rule:** a job that dies mid-step is an infrastructure event, not evidence. Before classifying any CI failure, get a clean reading first — re-run the exact failed job and classify only from a clean step failure. Classifying a runner death as a code RED wastes a lane on a phantom; worse, it teaches the team to distrust the tripwire. This joins the instrument-parity family (SN-0341 the instrument lies; SN-0429 verify with the instrument CI uses; SN-0379 wait steps need three-class verdicts): the measurement apparatus gets a verdict on the apparatus before anyone gets a verdict on the code.

## 🩷 HUMAN NOTE

If the testing machine itself breaks down halfway through the test, that's not a failed test — it's a broken machine. You fix the machine (re-run the test) and judge only the clean result, never the breakdown.

## 👶 CHILD NOTE

If the scoreboard crashes in the middle of the game, the score it showed before crashing isn't the real score. You restart the scoreboard and play again — then you count the real score.

## 👵 GRANDMA NOTE

You can't judge the cake by an oven that went out mid-bake. Light the oven again, bake it through, and then taste. Judge the cake, not the blackout.

## 🧠 NAYA NOTE

For a cold successor classifying CI on a tip: read the failure top-down (SN-0392), and at the first red ask "is this a verdict on the code, or a verdict on the runner?" Step states lagging the job verdict, 9-second mid-step deaths, and placeholder-skipped wait steps are all apparatus events — SN-0379's three-class verdict discipline applies to jobs too: *success / failed-clean / inconclusive-rerun*. The re-run is reversible and test-only (no deploy path), so it is always the most intelligent first move. Only the clean step failure goes into the RED classification (PR-introduced vs base-inherited, SN-0240); the runner death goes into the run log as noise, never into the scorecard. The pay-off on this tip: a phantom was discarded in one re-run, and the real RED (#1735's `_shared` coverage gap) was classified correctly and routed to its owning lane without a misfired repair.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0549",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/INSTRUMENT-PARITY",
  "doctrine": "A CI job that dies mid-step is an infrastructure event, not a test verdict. Before classifying a failure, re-run the exact failed job to obtain a clean reading; classify only from a clean step failure. Never classify a runner death as a code RED.",
  "evidence": [
    "#1354 comment 6041509592 ([DRIVE LOOP] Main RED classified, tip 75f6e22, 2026-10-07 15:50 UTC)",
    "Push run 37646038053 attempt 1: died in 9s mid-step, step states lagged behind the job verdict (runner anomaly, not a verdict)",
    "Re-ran single failed job POST /actions/jobs/112876924233/rerun (reversible, test-only, no deploy path); attempt 2: clean step failure at 'Run node --test tests/*.test.mjs'",
    "Virgin worktree at exact tip reproduced real RED: supabase/functions/_shared (from #1735) has no executed node test coverage; Deno test does not satisfy the gate; classified PR-introduced by #1735, tripwire correct, heal routed to owning lane"
  ],
  "falsifiers": [
    "Classifying a 9-second mid-step job death as a code RED",
    "Building a repair from step states that lagged behind the job verdict",
    "Treating a re-run as optional before classification"
  ],
  "applies_to": "CI RED classification; drive-loop triage; scorecard honesty",
  "sibling": "SN-0379 (wait-step three-class verdicts); SN-0246 (measure the failing line, never infer); SN-0341 (the instrument lies); SN-0421 (run-level SUCCESS with skipped jobs is vacuous); SN-0392 (first RED is the only RED)"
}
```
