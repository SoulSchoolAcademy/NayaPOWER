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

Deployment-lane repair commit:
`197edd044d0a77923a983049a1bacf90f5369a28`

Current evidence-recording commit:
`f852eb2c3752e519c05edcb7437d42e668beb59d`

Existing Hub production deployment:
`dpl_EE2uMkEnhrCCEeStiRi5oWuvzPKv`

Existing Hub latest preview deployment:
`dpl_7FLEgPYWEQtLnEUcnEDpgkrtiavH`

Production alias:
`nayanet-intelligent-hub.vercel.app`

## EXACT GIT INTEGRATION DIAGNOSIS

GitHub main is actively triggering Vercel, but the automatic Git deployment target is the different project `naya-power`, not `nayanet-intelligent-hub`.

For repair commit `197edd044d0a77923a983049a1bacf90f5369a28`, Vercel created:
`dpl_HirVP2j3zAyiu7B3CvNs3e4fjSSf`

Target project:
`naya-power`

Target project ID:
`prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`

The Vercel metadata identifies GitHub org `SoulSchoolAcademy`, repository `NayaPOWER`, branch `main`, and the exact commit SHA. Therefore GitHub-to-Vercel integration is proven active, but it is connected to the wrong Vercel project for the Hub.

The intended Hub project metadata does not expose a connected Git repository in the project response, and its current deployments do not carry Git commit metadata. This is consistent with it not being the active Git-connected target.

## DEPLOYMENT-LANE REPAIR

Added canonical GitHub workflow:
`.github/workflows/deploy-nayanet-intelligent-hub.yml`

The workflow is explicitly bound to the existing Hub project IDs and:
1. checks out canonical GitHub `main`;
2. installs `NAYANET/HUB` dependencies;
3. builds the Hub and generated PIS;
4. requires a valid generated PIS with `event_count > 0`;
5. deploys `NAYANET/HUB` to production using Vercel CLI;
6. uses the GitHub Actions secret `VERCEL_TOKEN` rather than embedding credentials.

No second Vercel project was created.

The exposed direct Vercel deployment connector was also tested, but its deployment interface rejected required inputs before creation (`target`, `name`, `files`). It therefore cannot be used as the deployment path in its current exposed form.

## GITHUB ACTIONS EXECUTION PROOF

For commit `f852eb2c3752e519c05edcb7437d42e668beb59d`, the new workflow DID START:

Workflow:
`Deploy NayaNET Intelligent Hub`

Run:
`35259011991`

Run number:
`2`

Event:
`push`

Head SHA:
`f852eb2c3752e519c05edcb7437d42e668beb59d`

Result:
**completed / failure**

The job completed successfully through:
- checkout;
- `npm ci`;
- Hub build;
- generated PIS validation.

The build produced:
`PIS_FEED_BUILT events=3 source=canonical-smart-notes+smart-feed`

The predeployment gate produced:
`PIS_PREDEPLOY_OK event_count=3`

The deployment step then failed with the exact message:
`VERCEL_TOKEN_MISSING`

The runner environment explicitly showed:
`VERCEL_PROJECT_ID=prj_ZpMGeKq4LcMBYslrO9D70jINpEVA`

and the secret expansion was empty:
`VERCEL_TOKEN:`

Therefore the exact remaining blocker is **not the Hub build, not the PIS build, and not the target project ID. The GitHub Actions environment does not currently have a `VERCEL_TOKEN` secret available to this workflow.**

No credential value was exposed or written into the repository.

## CURRENT DEPLOYMENT RESULT

The intended `nayanet-intelligent-hub` project still has no new deployment corresponding to `f852eb2c3752e519c05edcb7437d42e668beb59d`.

No new Hub deployment ID is claimed.

The separate `naya-power` project continues to receive Git-triggered deployments, proving the repository integration is alive but directed at the wrong project.

Therefore the Hub production boundary remains **NOT REPAIRED**.

## LIVE RUNTIME TEST

Live Hub:
`https://nayanet-intelligent-hub.vercel.app/`

Result: **HTTP 200**, but the response remains stale static HTML rather than proof of the current React/PIS build.

Live PIS:
`https://nayanet-intelligent-hub.vercel.app/intelligence/pis-feed.json`

Result: **HTTP 404 NOT_FOUND**.

Therefore the live PIS boundary remains **NOT REPAIRED**.

## SOURCE CHECK

`vercel.json` on GitHub main contains the intended Vite build configuration:
- install from `NAYANET/HUB`;
- build with `npm run build`;
- output `NAYANET/HUB/dist`;
- preserve `/intelligence/` from SPA rewrites.

The canonical Hub PIS consumer reads `/intelligence/pis-feed.json` first, then persistent Supabase PIS, then canonical GitHub Smart Feed fallback. The production 404 prevents the primary generated-PIS boundary from being proven live.

## VERIFIED

- Existing Vercel Hub project exists and is accessible.
- GitHub `main` triggers Vercel automatically.
- Automatic Git deployment is landing in `naya-power`, not the intended Hub project.
- The new dedicated Hub deployment workflow starts on GitHub push.
- The workflow checked out the exact requested commit `f852eb2c3752e519c05edcb7437d42e668beb59d`.
- Hub dependencies installed successfully.
- Hub production build succeeded.
- Generated PIS is valid and has `event_count=3` before deployment.
- The workflow is targeting the correct Hub project ID.
- The workflow fails at the deployment boundary because `VERCEL_TOKEN` is empty/missing.
- Live Hub returns HTTP 200 but is stale.
- Live PIS returns HTTP 404.
- No false production success is recorded.

## NOT VERIFIED

- New Vercel deployment for `nayanet-intelligent-hub` from current GitHub source.
- Deployment identity matching the intended Hub project.
- READY state for a new Hub deployment.
- Live `/intelligence/pis-feed.json` HTTP 200.
- Valid live PIS JSON in production.
- `event_count > 0` in production.
- Live Hub consumption of generated PIS.
- Production Smart Note → CIS → PIS → Hub chain.
- L3-L6 behavioral learning.

## BLOCKER

**GITHUB ACTIONS SECRET: VERCEL_TOKEN IS MISSING**

The deployment lane itself is now proven to execute correctly through build and PIS validation. It cannot authenticate to Vercel because the `VERCEL_TOKEN` GitHub Actions secret is not available.

This is now the single concrete deployment blocker exposed by the evidence available to Naya Power.

The token must be added as a GitHub Actions repository secret by an authorized human/account administrator. It must never be placed in source code, Smart Notes, Activity records, chat, or committed files.

## DECISION

Do not create another Hub or another Vercel project.

Do not redesign the Hub to compensate for the deployment credential boundary.

Preserve GitHub as canonical source and use the existing `nayanet-intelligent-hub` project.

Do not begin the real Adaptive Learning experiment until production PIS and Hub consumption are verified.

## LEARNING

A deployment workflow can be fully correct through build and predeployment validation while still being blocked at the credential boundary.

The evidence chain now distinguishes:
**source identity → workflow execution → build proof → PIS proof → authentication boundary → deployment identity → runtime response → consumer behavior.**

A missing deployment credential is now a concrete infrastructure blocker, not an architectural unknown.

The larger learning target remains:
**SMART NOTE → CIS → RETRIEVE → APPLY → OBSERVE → VERIFY → ADAPT → BETTER FUTURE ACTION.**

## NEXT ACTION

Add the authorized `VERCEL_TOKEN` to the GitHub repository Actions secrets, then rerun the existing `Deploy NayaNET Intelligent Hub` workflow for the current canonical source. After authentication succeeds, verify the resulting deployment belongs to project `prj_ZpMGeKq4LcMBYslrO9D70jINpEVA`, require READY state, fetch `/intelligence/pis-feed.json` and require HTTP 200 valid JSON with `event_count > 0`, then prove the live Hub consumes that generated PIS. Only after those runtime boundaries pass should the real retrieval/application/outcome learning experiment begin.

**SIGN-OUT STATE: BLOCKED ONLY ON VERCEL_TOKEN CREDENTIAL AVAILABILITY; SOURCE, BUILD, AND PIS PREDEPLOY GATES PROVEN**

**NAYA POWER ON → RESTORE → INSPECT → REPAIR → DEPLOY → TEST → VERIFY → RECORD → LEARN → CONTINUE**
