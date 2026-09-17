# GITHUB WORKFLOW CLASSIFICATION — 2026-09-17

**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Purpose:** reduce workflow ambiguity to explicit role/authority/lifecycle classifications before further deletion or deployment.

## Important evidence boundary

The current workflow directory is larger than the original 31-workflow audit because newer 509/510/513/Assistant families were added in later work. The matrix below is the **complete union of the 31-workflow inventory recorded by Issue #81 plus every additional workflow name directly observed in the current `.github/workflows` directory during this audit**. It contains 42 workflow paths. Any future directory change must update this matrix before the optimization gate can be GREEN.

## Classification vocabulary

- **KEEP / FAST** — routine deterministic verification.
- **KEEP / CONTROL** — protected governance/evidence gate.
- **KEEP / DEEP** — expensive or broad verification, deliberately invoked.
- **MANUAL / MUTATION** — intentional repository/product mutation, not routine CI.
- **BLOCKED / FAIL-CLOSED** — retained specifically to prevent unauthorized execution.
- **CONSOLIDATE** — useful checks should survive, but duplicate trigger/workflow surface should be collapsed.
- **RETIRE** — superseded or obsolete after replacement equivalence is preserved.
- **AUTHORITY UNRESOLVED** — cannot safely choose a deployment authority yet.

## Workflow matrix

| Workflow | Classification | Role / reason |
|---|---|---|
| `509-smart-board-world-class.yml` | BLOCKED / FAIL-CLOSED | Preserve as an explicit boundary preventing GitHub 509 from substituting for unresolved Assistant Cloudflare/live authority. |
| `510-aaa-smart-board-visual-surgery.yml` | MANUAL / MUTATION | Visual surgery generation; deliberate product mutation, not routine verification. |
| `513-smart-board-canonical-finalizer.yml` | MANUAL / MUTATION | Smart Board finalizer/mutation family; must not become an uncontrolled competing writer. |
| `assistant-cloudflare-hub-release.yml` | AUTHORITY UNRESOLVED | Potential current Assistant release lane; inspect trigger, secret/use, target Worker, source binding, and live proof before declaring canonical. |
| `deploy-509-c4-final-presentation-fix.yml` | RETIRE / HISTORICAL | Older 509 presentation repair generation; preserve provenance, do not execute as current authority. |
| `deploy-509-c4-flow-repair-v2.yml` | MANUAL / HISTORICAL | Older 509 flow repair; preserve until equivalence/authority record is complete. |
| `deploy-509-c4-flow-repair.yml` | RETIRE | Earlier generation of the same flow repair family; superseded by later versions. |
| `deploy-509-c4-nine-note-parser-v2.yml` | MANUAL / MUTATION | Parser deployment mutation; explicit execution only. |
| `deploy-509-c4-nine-note-parser.yml` | RETIRE | Earlier parser generation superseded by v2. |
| `deploy-509-c4-real-smart-feed-finalize.yml` | MANUAL / MUTATION | Smart Feed finalization mutation; explicit only. |
| `deploy-feature-board-v4.yml` | MANUAL / MUTATION | Feature-board deployment/mutation; not routine CI. |
| `deploy-smart-feed-direct-v2.yml` | MANUAL / MUTATION | Direct Smart Feed deployment; authority must not compete with Assistant/live lane. |
| `naya-control-plane.yml` | KEEP / FAST | Small deterministic control-plane/cold-start/state proof gate. |
| `naya-claim-evidence-enforcement.yml` | KEEP / CONTROL | Unique claim/evidence enforcement; preserve. |
| `naya-context-boot-guardrail.yml` | CONSOLIDATE | Valuable boot/torch checks overlap broader control gates. Fold into CONTROL. |
| `naya-memory-runtime.yml` | CONSOLIDATE | Memory/restore validation overlaps Superbrain/Smart Brain control paths. |
| `naya-v3-architecture-lock.yml` | KEEP / CONTROL | Distinct architecture/constitution policy boundary. |
| `superbrain-gate.yml` | KEEP / DEEP | Broad authoritative Superbrain regression anchor; preserve as deep control until overlap is proven removable. |
| `smart-brain-v3-enforcement.yml` | CONSOLIDATE | Validation overlaps Superbrain; scheduled mutation should not be a routine push gate. |
| `torch-pass-gate.yml` | CONSOLIDATE | Continuity checks overlap broader control paths; retain coverage, collapse trigger surface. |
| `intelligence-promotion.yml` | MANUAL / MUTATION | Distinct intelligence state mutation; deliberate execution only. |
| `apply-maxess-result-bridge.yml` | MANUAL / MUTATION | One-shot MAXESS bridge mutation. |
| `build-aiscore-app-bridge.yml` | MANUAL / MUTATION | Bridge build/mutation; local-first, deliberate. |
| `build-integrated-results.yml` | CONSOLIDATE / MANUAL | Results bridge generation overlaps rebuild generations; choose one canonical builder. |
| `rebuild-integrated-results.yml` | RETIRE | Historical Results rebuild generation. |
| `rebuild-integrated-results-corrected.yml` | RETIRE | Corrected historical generation superseded by later variants. |
| `rebuild-integrated-results-v3.yml` | MANUAL / CANDIDATE | Later Results rebuild candidate; deliberate only until authority is locked. |
| `rebuild-integrated-results-final.yml` | MANUAL / CANDIDATE | Final Results builder candidate; choose one authoritative mutation path. |
| `e06-aaa-power-pass.yml` | MANUAL / MUTATION | Product presentation mutation; deliberate only. |
| `execute-maxess-section01.yml` | MANUAL / MUTATION | MAXESS product checkpoint mutation. |
| `maxess-nitro-v2.yml` | MANUAL / FIX REQUIRED | Expensive mutation; known repository identity assertion defect must be repaired before use. |
| `maxess-result-hydration.yml` | CONSOLIDATE / MANUAL | Result hydration mutation overlaps bridge/build family. |
| `maxess-step3-runtime.yml` | KEEP / DEEP | Valuable browser runtime proof; expensive, deliberate release verification. |
| `maxess-step3-diagnostic.yml` | KEEP / DEEP | Unique parent/iframe integration diagnostic; deliberate. |
| `maxess-terminal-isolation.yml` | KEEP / DEEP | Valuable terminal-boundary browser proof; deliberate. |
| `maxess-v2-pretest.yml` | KEEP / DEEP | Browser pretest/hardening; release candidate proof, not routine CI. |
| `patch-e00-continue.yml` | RETIRE | Older E00 mutation generation. |
| `repair-e00-796-continue.yml` | RETIRE | Historical E00 repair generation. |
| `repair-e00-continue-v10.yml` | CONSOLIDATE / MANUAL | Later E00 repair generation; retain only as one deliberate repair path. |
| `repair-e00-results-handoff.yml` | RETIRE | Older Results handoff repair generation. |
| `repair-e00-results-handoff-v2.yml` | MANUAL / CANDIDATE | Later handoff repair candidate; deliberate mutation only. |
| `repair-e00-terminal-state.yml` | CONSOLIDATE / MANUAL | Terminal-state repair family; consolidate into one explicit repair tool. |

## Authority rules

1. **No workflow gets deployment authority merely from its filename.**
2. A mutation workflow is not a verification gate.
3. A historical workflow is not current authority.
4. `workflow_dispatch` does not prove authorization.
5. A successful workflow does not prove the public runtime unless the release evidence chain verifies it.
6. The GitHub 509 lane must not substitute for the unresolved Assistant Cloudflare/live lane.
7. One mutation/deployment boundary gets one canonical authority.
8. Every expensive browser/build workflow should be deliberate rather than fan out on ordinary changes.
9. Any retirement requires replacement coverage and Git history preservation.
10. The optimization gate stays RED while a current deployment authority remains unresolved.

## Minimum future CI spine

### FAST
`naya-control-plane.yml`

### CONTROL
A consolidated gate containing:
- cold-start;
- control-plane validation;
- continuity/torch;
- claim/evidence;
- project/next-execution checks.

### DEEP
Manual/deliberate:
- Superbrain broad regression;
- MAXESS browser proof;
- E00/E04 integration proof;
- Results rebuild;
- deliberate product mutation.

### RELEASE
One explicitly authorized production lane after the Assistant Cloudflare/live authority is reconciled.

## Current workflow score

**Organization:** 6.5/10  
**Authority clarity:** 5.5/10  
**Resource efficiency:** 6.0/10  
**Safety/fail-closed discipline:** 8.5/10  
**Cold-Naya discoverability:** 7.0/10

The weakness is no longer “we have no idea what these workflows are.” We now have a role map. The remaining work is to implement the consolidation/retirement decisions safely and resolve the live release authority.

## Next action

**Inspect the remaining mutation/deployment workflows' exact triggers, write targets, Worker targets, concurrency behavior, and authority references; then produce one canonical release-lane decision without triggering Actions.**
