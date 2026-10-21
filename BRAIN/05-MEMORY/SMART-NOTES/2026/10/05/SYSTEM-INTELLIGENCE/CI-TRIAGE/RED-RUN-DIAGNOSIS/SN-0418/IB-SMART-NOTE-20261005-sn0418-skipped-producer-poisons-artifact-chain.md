# The Skipped Producer Poisons the Chain — a Skip on an Artifact-Producing Job Is Not Neutral, It Kills Every Downstream Consumer

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0418-skipped-producer-poisons-artifact-chain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:39 PDT (2026-10-06T01:39:09Z) — comment 6007559525 ([NAYA 4] DIAGNOSIS — Runtime proof failures); run 37398221144, workflow `.github/workflows/live-supabase-runtime-proof.yml`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Five consecutive `live-supabase-runtime-proof` failures were diagnosed to a **workflow-plumbing** root cause, not a code defect:

1. `source-integrity` ✅ passes.
2. `cold-runtime-1` / `cold-runtime-2` ⏭️ **skipped** — so they never upload the artifacts (`naya-cold-runtime-1`, etc.) the chain depends on.
3. `cold-successor` ❌ **fails** at `actions/download-artifact@v4`, trying to fetch artifacts that were never uploaded.

The runtime code may be fine. The proof instrument is broken — a working engine with a broken dynamometer.

The durable rule: **in an artifact-chained workflow, a skip is not neutral.** Skipping the producer job silently kills the consumer, and the consumer's failure (download of a missing artifact) then masquerades as a downstream product failure. Two concrete authoring consequences:

- **Skip conditions on producer jobs must account for the whole chain.** If a job's artifacts feed downstream jobs, its skip condition is a property of the chain, not of the job. Either the consumers must be skippable under the same conditions, or the producer must run.
- **Consumers of artifacts must tolerate absence or gate on the producer.** A `download-artifact` step against an artifact a skipped job never uploaded is a hard failure by default. Decide explicitly at authoring time: fail, tolerate, or follow the producer's skip.

Classification discipline applies: when a chained proof fails, the first question is not "what broke in the code" but "did every producer in the chain actually run?" Check the job matrix for skips before debugging the subject — a red consumer with a skipped producer is an instrument failure, not a product failure. This note is the CI-workflow twin of SN-0379 (a wait step must not die on an upstream skip); here the failure surface is the artifact chain, and the fix belongs in workflow authoring, not in the code under test.

## 🩷 HUMAN NOTE

Shawn — the five straight runtime-proof failures aren't a code problem; they're a plumbing problem. The workflow skips the cold-runtime producer jobs, so the artifacts they were supposed to upload never exist, and the downstream job then fails trying to download them. The engine is probably fine; the dynamometer is broken. The lesson written down: in any workflow where jobs are chained by artifacts, skipping a producer job is never neutral — it silently kills every consumer below it. Going forward, skip conditions on producer jobs have to account for the whole chain, and artifact consumers must explicitly handle absence instead of hard-failing. When a chained proof goes red, the first thing to check is whether every producer actually ran — a skipped producer means it's an instrument failure, not a product defect. The workflow repair is the next step.

## 🟣 CHILD NOTE

Imagine a relay race where the second runner is only allowed to run if the first runner hands them the baton. But the first runner's coach told them to sit this one out — and nobody told the second runner. So the second runner stands there waiting for a baton that will never come, and the team is marked as losing. The second runner didn't fail; the setup failed. The lesson: when jobs depend on each other like a relay, skipping the first runner without telling the rest breaks the whole race. You have to design the race so a skipped runner either takes everyone below them out gracefully, or isn't allowed to sit out at all.

## 👵 GRANDMA NOTE

The team's automated proof system runs in stages, like an assembly line: one stage builds something, the next stage picks it up and tests it. Tonight the first stage was told to sit out, so it never built anything — and the next stage failed because there was nothing to pick up. Five failures in a row, and the code being tested was never the problem; the assembly line itself was. The team wrote down the rule: when stages depend on each other this way, skipping a stage is never harmless — everything below it breaks. The repair is in the line's own wiring: either skip whole sections together, or make each stage say clearly what it does when there's nothing to pick up. And always check that every stage actually ran before blaming the product.

## 💜 NAYA NOTE

Note to future me: when a chained CI proof goes red, read the job list before the logs. If any producer job was SKIPPED, the red downstream is almost certainly an instrument failure (download-artifact on a never-uploaded artifact), not a product failure — diagnose the skip, don't debug the code. When authoring or reviewing artifact-chained workflows (`.github/workflows/`), check every producer job's skip/`if` conditions against the chain: a producer's skip must propagate to its consumers or be blocked; a consumer's `download-artifact` must tolerate absence explicitly. Never silently "fix" the consumer to tolerate absence without recording that the producer's skip condition is the actual defect — tolerance hides chain rot. Cite alongside SN-0379 (skipped is not failed — three-class verdicts), SN-0341 (the instrument lies — audit the measurement instrument before patching the subject).

## 🖥️ MACHINE NOTE

{"sn": "SN-0418", "title": "The Skipped Producer Poisons the Chain — a Skip on an Artifact-Producing Job Is Not Neutral, It Kills Every Downstream Consumer", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-RUN-DIAGNOSIS"], "cousins": ["SN-0379", "SN-0341"], "evidence": {"board_comment": "#1354 6007559525 ([NAYA 4] DIAGNOSIS — Runtime proof failures, 2026-10-05 ~18:39 PDT)", "run": "37398221144: source-integrity PASS, cold-runtime-1/cold-runtime-2 SKIPPED (never uploaded naya-cold-runtime-* artifacts), cold-successor FAILED at actions/download-artifact@v4 on missing artifact", "workflow": ".github/workflows/live-supabase-runtime-proof.yml"}, "rule": "In artifact-chained workflows a skip on a producer job is not neutral — it silently kills every downstream consumer. Skip conditions on producer jobs must account for the whole chain; artifact consumers must explicitly tolerate absence or gate on the producer. When a chained proof fails, check for skipped producers before debugging the code: a red consumer with a skipped producer is an instrument failure, not a product failure."}
