# TEAM NAYA ACTIVITY — GITHUB-FIRST DELIVERY + PRODUCTION REPAIR

**DATE:** 2026-09-17
**SESSION / AGENT:** Naya Power — production deployment repair
**MISSION:** Preserve durable source truth, repair the Hub production boundary, and move toward a verifiable learning Superbrain.

## SIGN-IN

**TASK:** Inspect the existing Vercel project, determine why GitHub main is not producing a deployment for the Hub project, repair the deployment lane without creating another project, and prove or reject the live PIS boundary.

## INSPECTED

Existing Vercel Hub project:
`nayanet-intelligent-hub`

Project ID:
`prj_ZpMGeKq4LcMBYslrO9D70jINpEVA`

Team ID:
`team_RQnhoOb3bAXxMlcr67GFTu3Q`

Previous recorded GitHub main freeze point:
`8337328d634132cbac58ace5c90a37f4dd87436b`

Current GitHub main after deployment-lane repair commit:
`197edd044d0a77923a983049a1bacf90f5369a28`

Existing Hub production deployment:
`dpl_EE2uMkEnhrCCEeStiRi5oWuvzPKv`

Existing Hub latest preview deployment:
`dpl_7FLEgPYWEQtLnEUcnEDpgkrtiavH`

Production alias:
`nayanet-intelligent-hub.vercel.app`

## EXACT GIT INTEGRATION DIAGNOSIS

The current GitHub commit `197edd044d0a77923a983049a1bacf90f5369a28` received a Vercel commit status whose target is the **different Vercel project**:

`naya-power`

Deployment:
`dpl_HirVP2j3zAyiu7B3CvNs3e4fjSSf`

Project ID:
`prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`

Its Vercel metadata identifies the Git source as:
- Git provider: GitHub
- organization: `SoulSchoolAcademy`
- repository: `NayaPOWER`
- branch: `main`
- commit SHA: `197edd044d0a77923a983049a1bacf90f5369a28`

Therefore the evidence establishes that GitHub `main` **is connected to / triggering Vercel**, but the Git-triggered deployment is landing in the `naya-power` project rather than the existing `nayanet-intelligent-hub` project.

This explains why `nayanet-intelligent-hub` has not received a new Git-triggered deployment from the current GitHub main source.

The existing Hub project metadata itself does not expose a connected Git repository in the project response, while its current deployments have empty `meta` rather than Git commit metadata. This is consistent with the Hub project not being the active Git-connected target.

## DEPLOYMENT-LANE REPAIR

Added canonical GitHub workflow:
`.github/workflows/deploy-nayanet-intelligent-hub.yml`

Commit:
`197edd044d0a77923a983049a1bacf90f5369a28`

The workflow is explicitly bound to the existing Hub project IDs and does the following:
1. checks out GitHub `main`;
2. installs `NAYANET/HUB` dependencies;
3. builds the Hub and generated PIS;
4. rejects deployment if generated PIS is missing or `event_count <= 0`;
5. deploys `NAYANET/HUB` to production using Vercel CLI and the existing project ID/team ID;
6. requires the `VERCEL_TOKEN` GitHub secret rather than embedding credentials.

No second Vercel project was created.

The exposed Vercel direct-deployment connector was also tested again, but it rejected the required deployment inputs before creation (`target`, `name`, and `files`). Therefore the GitHub Actions deployment lane is the active repair path.

## CURRENT DEPLOYMENT RESULT

The `nayanet-intelligent-hub` project still lists only its two previous deployments at the time of this verification. No new Hub deployment ID has yet been observed.

The separate `naya-power` project did receive a Git-triggered production deployment for the repair commit, proving that GitHub-to-Vercel integration is active but pointed at the wrong project for this Hub.

Therefore the Hub production boundary remains **NOT REPAIRED** at this checkpoint.

## LIVE RUNTIME TEST

Live Hub:
`https://nayanet-intelligent-hub.vercel.app/`

Result: **HTTP 200**, but the response is stale static HTML rather than proof of the current GitHub React/PIS build. Response headers still show an old `last-modified` timestamp and a large cache age.

Live PIS:
`https://nayanet-intelligent-hub.vercel.app/intelligence/pis-feed.json`

Result: **HTTP 404 NOT_FOUND**.

Therefore the production PIS boundary is **NOT REPAIRED**.

## SOURCE CHECK

`vercel.json` on GitHub main contains the intended Vite build configuration:
- install from `NAYANET/HUB`;
- build with `npm run build`;
- output `NAYANET/HUB/dist`;
- preserve `/intelligence/` from SPA rewrites.

The canonical Hub PIS consumer reads `/intelligence/pis-feed.json` first, then persistent Supabase PIS, then canonical GitHub Smart Feed fallback. The production 404 prevents the primary generated-PIS boundary from being proven live.

## VERIFIED

- GitHub main is now frozen at `197edd044d0a77923a983049a1bacf90f5369a28` after adding the deployment lane.
- Existing `nayanet-intelligent-hub` Vercel project exists and is accessible.
- Existing Hub production deployment is READY.
- GitHub main is actively triggering Vercel, but the observed Git-connected target is `naya-power`, not `nayanet-intelligent-hub`.
- The new deployment workflow is committed to the canonical repository and explicitly targets the existing Hub project.
- Live Hub root returns HTTP 200 but is stale.
- Live PIS endpoint returns HTTP 404.
- No false Hub production success is recorded.

## NOT VERIFIED

- New Vercel deployment for `nayanet-intelligent-hub` from current GitHub main.
- GitHub Actions deployment workflow success.
- Live `/intelligence/pis-feed.json` HTTP 200.
- Valid live PIS JSON with `event_count > 0`.
- Live Hub consumption of generated PIS.
- Production Smart Note → CIS → PIS → Hub chain.
- L3-L6 behavioral learning.

## BLOCKER

**EXISTING HUB PROJECT IS NOT THE ACTIVE GITHUB VERCEL TARGET**

The repository is demonstrably connected to Vercel, but the Git-triggered deployment is going to `naya-power`. The existing `nayanet-intelligent-hub` project is not receiving those Git deployments.

The committed GitHub Actions lane is the direct repair mechanism for the existing Hub project. Its remaining runtime proof is the next boundary: workflow execution must create a new deployment for `prj_ZpMGeKq4LcMBYslrO9D70jINpEVA`, then the live PIS and Hub must be tested.

## DECISION

Do not create another Hub or another Vercel project.

Do not redesign the Hub to compensate for a deployment failure.

Preserve GitHub as the canonical source and the current commit as the freeze point. Repair the existing project delivery lane.

## LEARNING

A repository can be Git-connected to Vercel while the wrong Vercel project receives the Git deployment.

A Vercel READY deployment in the intended project is not evidence that the intended project is connected to the current Git source.

A successful Git-triggered Vercel deployment in another project is not evidence that the Hub is deployed.

Production completion still requires:

**source identity → target project identity → deployment identity → runtime response → consumer behavior.**

The larger learning target remains:

**SMART NOTE → CIS → RETRIEVE → APPLY → OBSERVE → VERIFY → ADAPT → BETTER FUTURE ACTION.**

## NEXT ACTION

Verify the new GitHub Actions deployment lane actually creates a deployment in `nayanet-intelligent-hub`. If it does, verify the deployment commit identity and READY state, fetch `/intelligence/pis-feed.json`, require HTTP 200 valid JSON with `event_count > 0`, and prove the live Hub consumes the generated PIS. Only after that boundary is verified should the real retrieval/application/outcome learning experiment begin.

**SIGN-OUT STATE: CONTINUING — HUB DEPLOYMENT TARGET REPAIRED IN SOURCE, RUNTIME PROOF PENDING**

**NAYA POWER ON → RESTORE → INSPECT → REPAIR → DEPLOY → TEST → VERIFY → RECORD → LEARN → CONTINUE**
