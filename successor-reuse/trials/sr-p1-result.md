# Trial SR-P1-20261007 — RESULT

**Date:** 2026-10-07
**Preregistration:** `sr-p1-preregistration.md` (filed before arms ran)
**Trial Director:** Naya 5 Trial Executor (subagent)
**Status:** COMPLETE — fourth discriminative-attempt trial, no system claim.

## Arms

- **Arm B (baseline):** cold subagent, task briefs only. No lesson.
- **Arm T (treatment):** cold subagent, task briefs + PR #1745 module-invocation
  lesson (STUBBED retrieval).

## Verifier output (deterministic, blind by construction)

**Arm B:** `bash run.sh` → exit 0, stdout `util-ok`; sum correct;
applicability `NO LESSON` as expected → **PASS**

**Arm T:** `bash run.sh` → exit 0, stdout `util-ok`; sum correct;
applicability `NOT APPLICABLE` (correct refusal judgment) → **PASS**

## Metrics

- Primary (related-task first-submission PASS): B=PASS, T=PASS → **delta = 0**
- Secondary (iterations to green): B=1, T=1 → **delta = 0**
- Refusal probe: T judged NOT APPLICABLE, sum correct → **PASS** (2/2)

## Interpretation (honest)

**Fourth null delta.** The baseline independently derived `python -m
tools.runner` without the lesson — its report even explained the sys.path
mechanism correctly. The PR #1745 lesson, though real and sharp, is ALSO
common knowledge among modern agents. My "discriminative" task design failed
at its one job.

**The finding is now 4/4 and it reframes the lane's problem.** R0–R2 concluded
"toy tasks cannot discriminate lesson value." SR-P1 extends this: **even
non-toy tasks fail when the lesson content is derivable from general
knowledge.** The bottleneck is not task complexity — it is LESSON SELECTION.
A trial can only measure lesson value when the lesson contains genuinely
non-obvious, non-derivable knowledge (project-specific quirks, past failure
modes unique to this system, configuration only discoverable through
experience). General programming wisdom, however real, will not discriminate.

**What this trial DID prove:**
1. The discriminative-trial pipeline works end-to-end (preregister → cold
   arms → deterministic blind scoring → honest null reported, no reruns).
2. The refusal probe works 2/2 on real lessons.
3. **First REPLAYABLE trial in lane history:** `trials/SR-P1-20261007/archive/`
   ships the full §10 archive contract — preregistration, both arm
   submissions (5 files each, SHA-256 pinned), verifier stdout, manifest.
   `node harness/replay-trial.mjs` → REPLAY MATCH (exit 0).

**What this trial did NOT prove:** that lessons improve successor performance.
Retrieval was STUBBED. The lesson-value hypothesis remains untested, not
falsified — 4/4.

## Archive status (protocol §10)

REPLAYABLE. `node harness/replay-trial.mjs trials/SR-P1-20261007/archive`
→ REPLAY MATCH. Manifest: `archive/manifest.json`.

## Next action

The lane needs a lesson-selection criterion: future trials must use lessons
whose content a cold agent cannot derive from general knowledge. Candidate
sources: project-specific failure modes (e.g., the nayanet-github-dispatch
ghost-table incident), NayaPOWER-specific API contracts, configuration
knowledge only present in the repo. The measurement-protocol sibling owns
scoring design; this executor will run the next trial against a
non-derivable lesson once one is identified.
