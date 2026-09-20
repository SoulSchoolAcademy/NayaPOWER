# GITHUB WORKFLOW CLASSIFICATION — 2026-09-17

**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Purpose:** reduce workflow ambiguity to explicit role/authority/lifecycle classifications before further deletion or deployment.

## Authority resolution — VERIFIED STRUCTURAL DECISION

The canonical production deployment authority for the current NayaNET Hub is:

**`.github/workflows/assistant-cloudflare-hub-release.yml`**

Evidence:
- explicitly declares itself the canonical runtime release;
- watches the protected `NAYANET/HUB/index.html` source;
- binds the exact Cloudflare account/Worker target;
- requires the `assistant-cloudflare-production` environment and Cloudflare token;
- deploys the exact source artifact;
- performs live artifact identity checks;
- performs desktop/mobile browser runtime verification;
- emits explicit live-runtime proof.

The former competing `513-smart-board-canonical-finalizer.yml` has been mechanically narrowed to **deliberate source mutation only**. It no longer deploys Cloudflare, no longer claims live-runtime authority, and runs only by explicit `workflow_dispatch`. Its final handoff explicitly names `assistant-cloudflare-hub-release.yml` as the deployment authority.

Therefore the deployment boundary is now:

`CANONICAL HTML → 513 (optional deliberate source finalization) → main → assistant-cloudflare-hub-release → Cloudflare → live verification`

The GitHub 509 lane remains fail-closed and cannot substitute for this lane.

## Classification vocabulary

- **KEEP / FAST** — routine deterministic verification.
- **KEEP / CONTROL** — protected governance/evidence gate.
- **KEEP / DEEP** — expensive or broad verification, deliberately invoked.
- **MANUAL / MUTATION** — intentional repository/product mutation, not routine CI.
- **BLOCKED / FAIL-CLOSED** — retained specifically to prevent unauthorized execution.
- **CONSOLIDATE** — useful checks should survive, but duplicate trigger/workflow surface should be collapsed.
- **RETIRE** — superseded or obsolete after replacement equivalence is preserved.
- **AUTHORITY UNRESOLVED** — cannot safely choose an authority yet.

## Workflow matrix

| Workflow | Classification | Role / reason |
|---|---|---|
| `509-smart-board-world-class.yml` | BLOCKED / FAIL-CLOSED | Explicit boundary preventing GitHub 509 from substituting for the canonical Assistant Cloudflare release lane. |
| `510-aaa-smart-board-visual-surgery.yml` | RETAIN / DISABLED | Legacy 510 lane is explicitly disabled and contains no mutation/deployment capability; 513 is the deliberate source-finalization path. |
| `513-smart-board-canonical-finalizer.yml` | MANUAL / MUTATION | Deliberate source finalizer only. It may commit canonical HTML, then hands off to the sole production release workflow. It cannot deploy. |
| `assistant-cloudflare-hub-release.yml` | **KEEP / CANONICAL RELEASE** | Sole production deployment authority for the current Hub; exact artifact binding, Cloudflare target, live identity, and browser verification. |
| `deploy-509-c4-final-presentation-fix.yml` | RETIRE / HISTORICAL | Older 509 presentation repair generation; no current authority. |
| `deploy-509-c4-flow-repair-v2.yml` | RETIRE / HISTORICAL | Older 509 flow repair; preserve provenance, do not execute as current authority. |
| `deploy-509-c4-flow-repair.yml` | RETIRE | Earlier flow repair generation. |
| `deploy-509-c4-nine-note-parser-v2.yml` | RETIRE / HISTORICAL | Historical parser deployment family; no current production authority. |
| `deploy-509-c4-nine-note-parser.yml` | RETIRE | Earlier parser generation superseded by v2 and current Hub architecture. |
| `deploy-509-c4-real-smart-feed-finalize.yml` | RETIRE / DISABLED | Source explicitly marks the path disabled; no current deployment authority. |
| `deploy-feature-board-v4.yml` | RETIRE / HISTORICAL | Historical feature-board deployment path; current Hub release is canonical. |
| `deploy-smart-feed-direct-v2.yml` | RETIRE / HISTORICAL | Historical direct Smart Feed deployment; cannot compete with current canonical release lane. |
| `naya-control-plane.yml` | KEEP / FAST | Deterministic control-plane/cold-start/state proof gate. |
| `naya-claim-evidence-enforcement.yml` | KEEP / CONTROL | Unique claim/evidence enforcement. |
| `naya-context-boot-guardrail.yml` | CONSOLIDATE | Valuable boot/torch checks overlap broader control gates. |
| `naya-memory-runtime.yml` | CONSOLIDATE | Memory/restore validation overlaps Superbrain/Smart Brain control paths. |
| `naya-v3-architecture-lock.yml` | KEEP / CONTROL | Distinct architecture/constitution policy boundary. |
| `superbrain-gate.yml` | KEEP / DEEP | Broad Superbrain regression anchor. |
| `smart-brain-v3-enforcement.yml` | CONSOLIDATE | Validation overlaps Superbrain; reduce trigger surface. |
| `torch-pass-gate.yml` | CONSOLIDATE | Continuity checks overlap broader control paths. |
| `intelligence-promotion.yml` | MANUAL / MUTATION | Distinct intelligence state mutation; deliberate execution only. |
| `apply-maxess-result-bridge.yml` | MANUAL / MUTATION | One-shot MAXESS bridge mutation. |
| `build-aiscore-app-bridge.yml` | MANUAL / MUTATION | Bridge build/mutation; deliberate. |
| `build-integrated-results.yml` | CONSOLIDATE / MANUAL | Results bridge generation; choose one canonical builder. |
| `rebuild-integrated-results.yml` | RETIRE | Historical Results rebuild. |
| `rebuild-integrated-results-corrected.yml` | RETIRE | Historical corrected rebuild. |
| `rebuild-integrated-results-v3.yml` | MANUAL / CANDIDATE | Deliberate Results builder candidate; not Hub release authority. |
| `rebuild-integrated-results-final.yml` | MANUAL / CANDIDATE | Deliberate Results builder candidate; not Hub release authority. |
| `e06-aaa-power-pass.yml` | MANUAL / MUTATION | Product presentation mutation. |
| `execute-maxess-section01.yml` | MANUAL / MUTATION | MAXESS checkpoint mutation. |
| `maxess-nitro-v2.yml` | MANUAL / FIX REQUIRED | Expensive mutation with known repository-identity defect. |
| `maxess-result-hydration.yml` | CONSOLIDATE / MANUAL | Result hydration overlaps bridge/build family. |
| `maxess-step3-runtime.yml` | KEEP / DEEP | Browser runtime proof. |
| `maxess-step3-diagnostic.yml` | KEEP / DEEP | Parent/iframe integration diagnostic. |
| `maxess-terminal-isolation.yml` | KEEP / DEEP | Terminal-boundary browser proof. |
| `maxess-v2-pretest.yml` | KEEP / DEEP | Browser pretest/hardening. |
| `patch-e00-continue.yml` | RETIRE | Older E00 mutation. |
| `repair-e00-796-continue.yml` | RETIRE | Historical E00 repair. |
| `repair-e00-continue-v10.yml` | CONSOLIDATE / MANUAL | Later E00 repair; retain as deliberate repair path. |
| `repair-e00-results-handoff.yml` | RETIRE | Older Results handoff repair. |
| `repair-e00-results-handoff-v2.yml` | MANUAL / CANDIDATE | Deliberate handoff repair candidate. |
| `repair-e00-terminal-state.yml` | CONSOLIDATE / MANUAL | Terminal-state repair family. |

## Authority rules

1. **`assistant-cloudflare-hub-release.yml` is the sole production deployment authority for the current Hub.**
2. `513-smart-board-canonical-finalizer.yml` may finalize source only; it must not deploy.
3. No workflow gets deployment authority merely from its filename.
4. A mutation workflow is not a verification gate.
5. A historical workflow is not current authority.
6. `workflow_dispatch` does not prove authorization by itself.
7. A successful workflow does not prove the public runtime unless its evidence chain verifies live behavior.
8. The GitHub 509 lane must remain fail-closed and must not substitute for the canonical Assistant Cloudflare lane.
9. One production deployment boundary gets one canonical authority.
10. Any retirement requires replacement coverage and Git history preservation.

## Release chain

`CANONICAL HTML → optional 513 SOURCE FINALIZATION → main → ASSISTANT CLOUDFLARE HUB RELEASE → exact Cloudflare Worker → live artifact identity → desktop/mobile runtime proof`

## Minimum future CI spine

### FAST
`naya-control-plane.yml`

### CONTROL
A consolidated gate containing cold-start, control-plane validation, continuity/torch, claim/evidence, and project/next-execution checks.

### DEEP
Manual/deliberate Superbrain regression, MAXESS browser proof, integration proof, Results rebuild, and product mutation.

### RELEASE
**`assistant-cloudflare-hub-release.yml` only.**

## Current workflow score

**Organization:** 7.5/10  
**Authority clarity:** 8.5/10  
**Resource efficiency:** 7.0/10  
**Safety/fail-closed discipline:** 9.0/10  
**Cold-Naya discoverability:** 8.0/10

The key deployment-authority ambiguity is now resolved structurally. Remaining optimization is consolidation/retirement of historical workflow surfaces and execution of the repository-only Cold-Naya acceptance test.

## Next action

**Run the Cold-Naya Operating Index acceptance test against `main`, preserve the actual CI result, then use that verified acceptance surface to begin the automatic execution → Activity → state → successor implementation.**
