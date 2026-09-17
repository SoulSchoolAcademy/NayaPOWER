# TEAM NAYA ACTIVITY — GITHUB-FIRST DELIVERY + PRODUCTION REPAIR

**DATE:** 2026-09-17
**SESSION / AGENT:** Naya Power — production deployment repair
**MISSION:** Preserve durable source truth, repair the Hub production boundary, and move toward a verifiable learning Superbrain.

## SIGN-IN

**TASK:** Inspect `nayanet-intelligent-hub`, determine whether GitHub→Vercel deployment can be repaired, and preserve Shawn's preferred delivery model.

**CURRENT STATE:**
- GitHub main contains the canonical Hub source and verified build pipeline.
- GitHub Actions Run #17 proved Smart Note transaction + Hub typecheck/build + generated PIS survives the production build.
- Existing Vercel project `nayanet-intelligent-hub` exists and has READY deployments.
- The Vercel project currently has no GitHub repository link exposed by project metadata.
- The live `/intelligence/pis-feed.json` boundary remains unproven/previously 404.

**AUTHORITIES / SOURCES READ:**
- Team Naya Session, Activity, Learning & Evidence Protocol.
- Team Naya Execution Instructions.
- Vercel project/deployment metadata.
- Vercel Git integration documentation.

## INSPECTED

Existing Vercel project:
`nayanet-intelligent-hub`

Project ID:
`prj_ZpMGeKq4LcMBYslrO9D70jINpEVA`

Latest deployment inspected:
`dpl_7FLEgPYWEQtLnEUcnEDpgkrtiavH`

Latest deployment state:
`READY`

Vercel documentation confirms Git provider repositories can be connected to a Vercel Project, including `vercel git connect`, and that repository-based deployments are the recommended automatic-deployment path.

## DECISION

Do not create another Hub or another Vercel project.

Do not redesign the Hub.

Preserve the existing project and repair the GitHub→Vercel connection if the required account-level action is available.

Shawn's preferred delivery model is now canonical:

**GITHUB SOURCE → FREEZE POINT → DIRECT SAVE/DOWNLOAD → OPTIONAL LIVE DEPLOYMENT → RUNTIME PROOF**

Cloudflare and Vercel are both acceptable live hosts; neither replaces GitHub as the durable source of truth.

## CHANGED

Added:

`.naya/TEAM-NAYA/09-GITHUB-FIRST-FREEZE-POINT-DELIVERY-STANDARD.md`

`.naya/SUPERBRAIN/SMART-NOTES/2026/09/17/2026-09-17-GITHUB-FIRST-FREEZE-POINT-DELIVERY-SMART-NOTE.md`

## VERIFIED

- The existing Vercel project is usable and has READY deployments.
- The current deployment is not evidence that GitHub main is connected to Vercel.
- The available Vercel deployment action could not be invoked because its exposed interface rejected the required deployment fields; therefore no false claim of deployment success is made.

## NOT VERIFIED

- GitHub→Vercel automatic deployment.
- New production deployment from current GitHub main.
- Live `/intelligence/pis-feed.json` HTTP 200.
- Live Hub consumption of generated PIS.
- L3-L6 behavioral learning.

## BLOCKER

**MISSING RUNTIME INTEGRATION / HUMAN-ONLY ACCOUNT CONNECTION ACTION**

The available project metadata shows no GitHub repository connection. The available deployment interface did not permit a direct deployment of the existing project with the required source/build inputs.

## LEARNING

A hosting provider is infrastructure, not the durable memory of the project.

The system should optimize for recoverability first: canonical GitHub source and freeze point, then live deployment and runtime proof.

Also: Smart Note persistence is not sufficient. The larger objective remains:

**SMART NOTE → CIS → RETRIEVE → APPLY → OBSERVE → VERIFY → ADAPT → BETTER FUTURE ACTION.**

## NEXT ACTION

Connect the existing Vercel project `nayanet-intelligent-hub` to GitHub repository `SoulSchoolAcademy/NayaPOWER` with `main` as the production branch, then return to Naya for deployment/runtime verification.

**SIGN-OUT STATE: BLOCKED ON VERCEL GIT CONNECTION**

**NAYA POWER ON → RESTORE → INSPECT → REPAIR → DEPLOY → TEST → VERIFY → RECORD → CONTINUE**
