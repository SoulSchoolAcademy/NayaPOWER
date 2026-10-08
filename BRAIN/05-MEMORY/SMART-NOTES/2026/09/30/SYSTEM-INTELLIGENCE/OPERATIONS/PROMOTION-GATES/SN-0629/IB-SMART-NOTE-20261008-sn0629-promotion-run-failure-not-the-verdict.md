# A Promotion Run's "failure" Conclusion Is Not the Verdict — Read the Steps

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0629-promotion-run-failure-conclusion-not-the-verdict
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#1354` 6050180366 ([DRIVE LOOP][SIGN-OUT] — 2026-10-08 01:13Z tick, SoulSchoolAcademy, 2026-10-08T01:18:30Z — Governed Production Promotion push run 37709985591 on main `60d105cb45bebf0d3568a6f7da666a12112bfe16`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The drive loop promoted production to the healed tip `60d105cb` and the promotion workflow's run conclusion read `failure` — and the deployment was fine. Steps 5–7 succeeded: the production ref moved to `b14a9c7a`, the deploy stamp landed on the exact current main, and tip CI (Kernel Tests, Spec Integrity, Current Truth Resolver, Live CVO Runtime Proof, Ratified Guard, Collective Chain Readiness, Live Verified AI Action Proof) was all SUCCESS. The `failure` belonged to step 10 alone — dispatch post-deploy proofs — a propagation artifact (its dispatches actually executed: github-actions[bot] runs 37710127939 SUCCESS, 37710261940 at 00:53/00:55Z). Same class as the `98719cda` promotion the tick before.

Why this is brain-grade: the run-level conclusion is a liar in both directions, and the family is growing — SN-0421 taught "run-level SUCCESS with skipped behavioral jobs is vacuous"; this note teaches the mirror: **run-level FAILURE with successful deploy steps is not a failed deploy.** The discipline is the same in both: never inherit the conclusion; read the steps. The classification matters because the wrong read wastes real work: a re-promotion "to fix the failure" would re-deploy an already-correct production pointer and replay a deterministic propagation artifact. The right read: verify the ref actually moved (it did — `b14a9c7a` == stamp of `60d105cb`), confirm the failed step's downstream effects landed anyway (they did — the bot runs succeeded), name the step-10 dispatch failure as the known propagation class, and move on. Pairs with SN-0438 (a fail-closed gate firing on a known-RED tip is the design working, not an incident): both are the same instrument-error lesson — the workflow's top-line verdict is a summary, not a measurement.

## 🩷 HUMAN NOTE

Shawn — one classification to keep from this tick's drive loop: the production promotion's run conclusion said "failure," but the deploy was fine — steps 5–7 all succeeded and production sits on the exact healed tip `60d105cb`. The failure was step 10 alone (dispatching post-deploy proofs), a propagation artifact whose downstream runs actually succeeded. Lesson banked: never inherit a run-level conclusion in either direction — read the steps. A re-deploy "to fix the failure" would have re-done correct work and replayed the same artifact.

## 🟣 CHILD NOTE

Imagine your report card says "F" in big red letters at the top — but every single subject inside is an A. The top line is just wrong; you read the subjects. That's what happened here: the promotion's top line said "failure," but every step that mattered passed. Always read the subjects, never trust the headline.

## 👵 GRANDMA NOTE

The overnight automation reported a production promotion as "failed," but the actual delivery had succeeded — the failure was in the very last step, a bookkeeping notification whose downstream actions had already completed fine. The lesson the team banked: a headline verdict on a whole process is not the truth; you read each step. Re-running the whole thing "to fix it" would just repeat what was already correct.

## 🤖 NAYA NOTE

Promotion-run verdict discipline (2026-10-08, #1354 6050180366): run 37709985591 on 60d105cb — conclusion `failure`, but steps 5–7 SUCCESS (production ref → b14a9c7a = deploy stamp of 60d105cb) and the `failure` is step 10 (dispatch post-deploy proofs) alone — propagation artifact; dispatches executed (bot runs 37710127939 SUCCESS, 37710261940). Same class as the 98719cda promotion last tick. Rule: never inherit a run-level conclusion — read the steps; verify the ref moved; confirm the failed step's downstream effects. A step-10 dispatch failure after a successful deploy is propagation, not a deploy defect — do not re-promote, do not re-dispatch to "see if it clears." Mirror of SN-0421 (run-level SUCCESS is vacuous); sibling of SN-0438 (fail-closed gate on red tip is the design working).

## ⚙️ MACHINE NOTE

{"sn": "SN-0629", "title": "A Promotion Run's \"failure\" Conclusion Is Not the Verdict — Read the Steps", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "PROMOTION-GATES"], "extends": ["SN-0438", "SN-0421", "SN-0392"], "evidence": {"board": "#1354 6050180366 ([DRIVE LOOP][SIGN-OUT] — 2026-10-08 01:13Z tick)", "run": "Governed Production Promotion push run 37709985591 on 60d105cb45bebf0d3568a6f7da666a12112bfe16", "deploy_proof": "steps 5–7 SUCCESS; production ref b14a9c7a == 'deploy: stamp Naya runtime source 60d105cb…'; tip CI all SUCCESS except step 10", "failure_class": "step 10 (dispatch post-deploy proofs) failure ONLY — propagation artifact; dispatches executed: github-actions[bot] runs 37710127939 SUCCESS, 37710261940 (00:53/00:55Z)", "recurrence": "same class as the 98719cda promotion last tick"}, "rule": "never inherit a run-level conclusion in either direction — read the steps; a step-10 dispatch failure after successful deploy steps is a propagation artifact, not a deploy defect; verify the ref moved, confirm downstream effects landed, do not re-promote or re-dispatch to 'see if it clears'"}
