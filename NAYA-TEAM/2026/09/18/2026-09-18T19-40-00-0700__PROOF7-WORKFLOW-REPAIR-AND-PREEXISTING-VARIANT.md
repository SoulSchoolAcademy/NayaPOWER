# 🔱 Naya Session — Proof 7 Workflow Repair + Pre-existing Intelligence Variant

**LOCAL TIMESTAMP:** 2026-09-18 19:30 PDT (America/Vancouver)
**ACTOR:** Naya / Team Naya
**REPOSITORY:** SoulSchoolAcademy/NayaPOWER
**REF:** main

## SIGN IN

Signed in by first reading the exact prior handoff:
[NAYA-TEAM/2026/09/18/2026-09-18T19-28-00-0700__PROOF7-ACCUMULATED-INTELLIGENCE-CONTINUATION.md](./2026-09-18T19-28-00-0700__PROOF7-ACCUMULATED-INTELLIGENCE-CONTINUATION.md)

## ORIENT

The prior handoff identified two boundaries:

1. Proof 7 run **35415657231** failed with zero exposed jobs and therefore had no job-level cause.
2. The existing Proof 7 script creates its starting intelligence inside the proof, so it cannot certify the stricter pre-existing accumulated-intelligence boundary.

## DIAGNOSIS

Re-checked run **35415657231** after the run had settled:

- Jobs exposed by GitHub API: **0**
- Artifacts: **0**
- Job logs: unavailable because no job exists.
- The current original workflow YAML contains a concrete job and valid-looking trigger/job structure.
- The failure therefore remains **NOT-PROVEN at repository source level**; there is no evidence to claim a runner, script, or Supabase failure.

GitHub documentation confirms that failed workflow runs can occur before job execution, and current GitHub community reports document the same zero-job/startup-failure symptom. This is treated as a platform/dispatch boundary hypothesis, not as a proven root cause.

## REPAIR

Created an isolated canonical workflow path so the stricter proof is no longer dependent on the original Proof 7 workflow registration:

- `.github/workflows/verify-proof7-preexisting-accumulated-intelligence.yml`
- `scripts/verify-proof7-preexisting-accumulated-intelligence.mjs`

The new workflow has its own workflow identity, its own job, and its own artifact. Its first push run is `35415844874`, and GitHub recognized that new workflow but completed it with zero jobs.

## PRE-EXISTING INTELLIGENCE VARIANT

The new runner does **not** create starting learning evidence.

At proof start it:

1. Requires a legitimate authenticated owner access token.
2. Authenticates that owner against Supabase.
3. Retrieves that owner's existing learner state.
4. Selects an ACTIVE learning-evidence pointer whose evidence predates proof start and is not proof-created.
5. Calls fresh `naya-decision-context` for that target.
6. Requires the decision to be influenced by that exact pre-existing evidence and source-event lineage.
7. Executes real Smart Mail using the authenticated owner.
8. Receiver-retrieves and verifies the action.
9. Verifies cognition → receipt lineage and verified receipt value.
10. Persists new outcome learning through the canonical learning path.
11. Performs a fresh decision-context retrieval against the new learning.
12. Writes a proof artifact only after all gates pass.

The proof explicitly records the exact prior Activity record hash so the cold runtime has a durable source reference independent of this conversation.

## CREDENTIAL BOUNDARY

The workflow intentionally requires:

`NAYAPOWER_PROOF7_OWNER_ACCESS_TOKEN`

No token was fabricated, copied from another owner, or replaced with service-role access. If this authorized GitHub secret is absent, the proof must fail closed with **PREEXISTING_OWNER_ACCESS_TOKEN_REQUIRED**.

## VERIFICATION STATE

- Production closure: **VERIFIED** from run 35415048129.
- Prior Proof 7 compounding loop: **EXISTS**, but its starting intelligence is proof-created.
- Run 35415657231: **FAILED / ZERO JOBS / ROOT CAUSE NOT-PROVEN**.
- Original Proof 7 repair: **ISOLATED NEW WORKFLOW PATH CREATED**.
- Pre-existing accumulated-intelligence implementation: **BUILT**.
- Pre-existing accumulated-intelligence production proof: **NOT-PROVEN; run `35415844874` failed before job creation, so the credential gate was never reached.**
- No fabricated PASS.

## SIGN OUT / HANDOFF

Signed out.

**NEXT NAYA:** read this exact record first, then inspect the new workflow's latest run. If it has a job, execute the pre-existing proof. If it again has zero jobs, treat this as the repository-level GitHub Actions startup boundary and do not modify the proof logic to compensate. If it reaches a job and fails at the credential gate, provision the authorized owner test credential through the legitimate GitHub secret/provisioning boundary. If it reaches runtime and any proof gate fails, fix that exact boundary and rerun. Do not certify the pre-existing intelligence boundary until the full transaction passes.


## FOLLOW-UP — LATEST ACTIONS DIAGNOSIS

A fresh inspection of main shows the execution boundary has changed in an important way.

Latest pre-existing-intelligence run on main:
- Run: **35416213107**
- HEAD: 1b683f402f8eec657bbae7d00ec81842fc5e0f14
- Workflow: verify-proof7-preexisting-accumulated-intelligence.yml
- Conclusion: **failure**
- Jobs: **0**

The original Proof 7 workflow at the same HEAD also has **0 jobs**:
- Run: **35416212474**
- Conclusion: **failure**

The P0 Dream workflow at the same HEAD also has **0 jobs**:
- Run: **35416212038**
- Conclusion: **failure**

However, this is **not a repository-wide GitHub Actions outage**: unrelated workflows on the exact same HEAD successfully created and completed jobs, including:
- Run **35416213963** — Execution → Team Naya Activity Bridge — **SUCCESS**, one completed job.
- Run **35416213885** — Golden Journey Acceptance — **SUCCESS**.
- Run **35416213879** — Smart Note E2E Isolated — **SUCCESS**.

Therefore the evidence now supports a narrower statement:

> **The affected Proof 7/P0 workflow registrations are failing before job-graph creation, while other workflows on the exact same main commit still create jobs successfully.**

The exact GitHub internal startup cause remains **NOT-PROVEN**. Public GitHub community reports document the same class of zero-job startup-failure symptom, but they do not establish the internal cause of this repository's runs.

### HARD RULE

Do **not** rewrite the accumulated-intelligence proof to hide or bypass this boundary.

The proof source remains intact.

**NEXT NAYA:** isolate the common registration/configuration property shared by the zero-job workflows (verify-proof7-preexisting, verify-proof7-compounding, and verify-p0-dream-scoring) versus a job-bearing workflow on the same HEAD, then make the smallest justified repair. Do not touch the pre-existing-intelligence semantics.
\n\n
## FOLLOW-UP — MINIMAL JOB-GRAPH ISOLATION PROBE — 2026-09-18 20:15 PDT

### SIGN IN / ORIENT
Read this exact record and compared the three zero-job workflows against job-bearing workflows on the same HEAD 1b683f402f8eec657bbae7d00ec81842fc5e0f14.

### FINDING
The affected YAML files do not share a source-level defect that can be justified from the repository alone. permissions: contents: read, push + workflow_dispatch, paths, job-level env, timeout-minutes, ubuntu-latest, and GitHub-owned actions each also occur in workflows that successfully created jobs on the same HEAD. The three affected runs remain zero-job: 35416213107, 35416212474, and 35416212038. Control runs 35416213963, 35416213885, and 35416213879 each created and completed a real job.

### ACTION
Created the smallest useful repository-side isolation probe:
.github/workflows/nayanet-actions-job-graph-probe.yml

The probe contains only push/workflow_dispatch, one ubuntu-latest job, and one shell echo; it has no path filters, permissions block, secrets, third-party actions, setup actions, environment, or application code. Commit: 1a6f4e973a1e500efa6111e72ad3e9ac0f071abf.

This is a diagnostic boundary probe, not a replacement for Proof 7 and not a change to accumulated-intelligence semantics.

### VERIFICATION STATE
The probe commit is confirmed on main. The accessible GitHub connector can inspect individual run IDs and job lists but does not expose a repository-wide push-run listing endpoint, so the resulting probe run ID is not yet observable through the connected GitHub surface. Therefore the probe result is NOT-PROVEN at this session boundary; no success or failure is assumed.

### SIGN OUT / HANDOFF
No Proof 7 logic was weakened, bypassed, or rewritten. No credential was fabricated. NEXT NAYA: obtain the concrete run state for commit 1a6f4e973a1e500efa6111e72ad3e9ac0f071abf; if the minimal probe gets a job, use that evidence to isolate the affected workflow configuration/registration boundary; if it is also zero-job, preserve the failure as a GitHub Actions execution/dispatch boundary and escalate rather than altering Proof 7 semantics.
