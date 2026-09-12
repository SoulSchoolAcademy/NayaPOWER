# 2026-09-12 — GitHub Superbrain Optimization / Legacy Surface Purge

**STATUS:** ACTIVE — LEGACY PURGE EXECUTED / CONSOLIDATION NEXT
**ACTION ID:** `NAYA-GITHUB-OPTIMIZE-20260912`
**PROJECT:** NayaPOWER / NayaNET Superbrain → Intelligent Hub
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`

## 01 — WHAT IS HAPPENING NOW?
The repository had accumulated multiple generations of GitHub Actions for retired Hub surfaces, MAXESS, E00, Integrated Results, V7 static Hub work, Vercel/E02 deployment, dated one-off repairs, and unrelated workflows. This created avoidable Actions surface area and competing execution authorities.

The current product authority is `NAYANET/HUB` with the governed public deployment workflow `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`. The Superbrain is the execution/governance engine; the Intelligent Hub is the receiver/product surface.

## 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?
Make any cold Naya able to enter the repository, recover exact current truth, identify the highest-value authorized work, execute it, verify it, record durable state, and leave a complete executable continuation — while keeping GitHub Actions small, intentional, and non-critical to Naya-to-Naya communication.

North Star: **optimize the GitHub Superbrain to build the Intelligent Hub successfully and effectively.**

## 03 — WHAT DOES THE EXISTING SYSTEM ACTUALLY DO?
The canonical Activity Feed is `SUPERBRAIN/NAYA-ACTIVITY-FEED.md`. Direct Naya activity writes are the communication layer. GitHub Actions are validation/infrastructure only.

Current canonical Hub source: `NAYANET/HUB`.
Current governed public deployment authority: `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`.
Current Hub acceptance authority: `.github/workflows/naya-power-hub-acceptance.yml`.
Current exact-runtime visual proof: `.github/workflows/nayanet-visual-proof.yml`.
Current primary-intelligence projection verification: `.github/workflows/verify-primary-intelligence-system.yml`.

## 04 — WHAT COULD I BE MISUNDERSTANDING?
Deleting a workflow is safe only when its execution authority is genuinely retired. The cleanup therefore prioritized workflows whose own source explicitly identified them as retired, workflows bound to superseded product surfaces, and workflows for explicitly retired projects.

A remaining workflow is not automatically canonical merely because its filename sounds current. Remaining workflows require trigger/path audit and consolidation.

## 05 — WHAT ARE THE CONSEQUENCES OF EACH OPTION?
Leaving legacy workflows creates confusion, consumes runner capacity when triggered, increases false failure surfaces, and makes cold-Naya reasoning harder. Deleting current authority would be worse. The selected strategy is surgical deletion of clearly obsolete surfaces followed by consolidation of overlapping current governance/verification workflows.

## 06 — WHAT MATTERS MOST?
One mission, one current product authority, one communication/continuity layer, and the smallest reliable automation surface that proves consequential work without becoming the work itself.

## 07 — WHAT SHOULD I DO?
Continue with a KEEP / CONSOLIDATE / DELETE audit of the remaining workflows. Narrow broad path filters, remove duplicate gates, and preserve only workflows that directly support Superbrain continuity/governance, canonical Hub acceptance/proof, intelligence persistence, or explicit production deployment.

## 08 — WHAT SHOULD I NOT DO?
Do not restore deleted legacy workflows. Do not use GitHub Actions as the Activity Feed communication mechanism. Do not add a new workflow when an existing canonical gate can be surgically improved. Do not make external runtime proof a blocker for repository-only execution when the runtime target is unavailable.

## 09 — EXECUTE SURGICALLY
Removed the clearly obsolete workflow families, including:
- four legacy workflows explicitly identified by the operator: Integrated Results V3 rebuild, E00 terminal repair, AI Score bridge, and E00 results handoff;
- retired/date-stamped Hub repair and deployment aliases;
- MAXESS-specific workflows;
- E00 continuation/handoff workflows;
- Integrated Results build/rebuild workflows;
- V7 static Hub build/deploy/package/repair/diagnostic workflows;
- legacy HTML/5:09 Hub build/package/deploy workflows;
- obsolete Vercel/E02 deployment workflow;
- unrelated Living Sun workflow;
- obsolete E03 and Supreme deployment workflows;
- obsolete score hydration and E06 workflows;
- retired browser/runtime/cognitive/feed aliases;
- obsolete V7 runtime verification workflow;
- the NayaPOWER P0 Actions bridge, because Actions must not sit on the critical execution/communication path.

Also repaired `.github/workflows/naya-control-plane.yml` so it no longer references the retired `deploy-v7-now.yml` authority.

The P0 adversarial workflow was surgically narrowed: push execution is offline-governance only; live runtime execution is explicitly dispatched and no longer treats a missing `NAYA_POWER_TARGET_URL` as a false failure.

## 10 — VERIFY THE CHANGE
GitHub accepted each deletion/update and returned commit receipts. Representative receipts include:
- retired one-off cleanup: `6a7c211e8f577f4ba1c4dbad7d33b8d3d13fe987`
- Naya control-plane repair: `5076d6889b34758a5b024006a6d0a7fdc2790eda`
- P0 adversarial trigger/runtime boundary repair: `4ac1c0c909ded3413f8bc732f067b0a504b4ed68`
- P0 Actions bridge removal: `532b1815c07d27e6678d872d1d9ab30cdca798de`
- final legacy/runtime cleanup continued through the current `main` branch.

## 11 — TRACE REALITY END-TO-END
SOURCE → GitHub `main` workflow inventory → legacy workflow families removed → current canonical Hub deployment preserved → current Hub acceptance/visual/PIS verification preserved → Superbrain execution bridge removed from critical path → P0 live proof isolated from automatic repository validation.

No claim is made here that the remaining workflow set is already optimally consolidated. That is the next verification boundary.

## 12 — PRODUCE RECEIPTS
Primary evidence paths:
- `SUPERBRAIN/INTELLIGENT-HUB-MASTER-PLAN.md`
- `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`
- `.github/workflows/naya-power-hub-acceptance.yml`
- `.github/workflows/nayanet-visual-proof.yml`
- `.github/workflows/verify-primary-intelligence-system.yml`
- `.github/workflows/superbrain-gate.yml`
- `SUPERBRAIN/NAYA-ACTIVITY-FEED.md`

## 13 — CHALLENGE MY OWN CONCLUSION
The cleanup is not proof that the remaining workflow architecture is minimal. Several current workflows overlap in Superbrain governance, memory/restore validation, P0 validation, intelligence verification, and deployment governance. The next pass must measure those overlaps from actual source and consolidate them without losing coverage.

## 14 — REPORT CONFIDENCE
**HIGH:** the deleted workflow families were obsolete/retired or explicitly outside the current mission based on their source and current canonical Hub authority.
**MEDIUM:** the remaining workflow surface is still larger than necessary and needs consolidation.

## 15 — DETERMINE WHAT MATTERS NEXT
Build the authoritative remaining-workflow matrix: every workflow → trigger → paths → purpose → canonical authority → duplicate coverage → Actions cost/risk → KEEP/CONSOLIDATE/DELETE. Then reduce the active automation surface to the minimum that still proves Superbrain continuity and Intelligent Hub correctness.

## 16 — LEARN AND CHANGE THE SYSTEM
Permanent rule: **CURRENT MISSION → REQUIRED SYSTEM SURFACE → REQUIRED AUTOMATION → EVERYTHING ELSE IS SUSPECT.**

Permanent architecture rule: **The Activity Feed is communication. Actions are infrastructure.**

Permanent optimization rule: **Critical-path actions use the simplest reliable mechanism; verification may surround the critical path but must not unnecessarily block it.**

## PRESERVED
Canonical `NAYANET/HUB` source, governed V2 public deployment, current Hub acceptance, current visual proof, current PIS verification, Superbrain governance/runtime contracts, and the canonical Activity Feed were preserved.

## NEXT ACTION
Resolve the exact current `main` HEAD and audit every remaining `.github/workflows/*.yml` source into a KEEP / CONSOLIDATE / DELETE matrix, then surgically consolidate duplicate current gates without weakening any proven Superbrain or Hub contract.

## SUCCESSOR HANDOFF
Read this record first. Do not recreate deleted legacy workflows. Treat `NAYANET/HUB` and `deploy-nayanet-hub-canonical-v2.yml` as the current Hub source/deployment authority. Treat `SUPERBRAIN/NAYA-ACTIVITY-FEED.md` as the continuity projection. The next Naya owns the remaining workflow consolidation pass.

**16-PROTOCOL CHECK:** PASS