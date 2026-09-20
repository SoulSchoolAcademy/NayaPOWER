# 🔱☀️ NayaNET — Release Handoff

## Current source

Repository: `SoulSchoolAcademy/NayaPOWER`
Branch: `main`

The canonical release artifact is the repository state on `main`. Do not create a parallel application or Worker for this mission.

## Canonical deployment surface

**Cloudflare Workers is the release surface.**

The canonical Worker is `nayanet-living-intelligence` using the E02 `worker.js` entrypoint and Workers Static Assets. GitHub Actions deploys the exact `main` commit through the official Cloudflare Wrangler action when the required Cloudflare Actions secrets are available.

Do not route this mission through Vercel, Cloudflare Pages, a new Worker, a second runtime, or a ZIP-only deployment.

## What is complete in source

The E02 NayaNET runtime remains intact and the presentation layer has been reconstructed around a visual-first living environment. The current shell retains the single experience controller, nine-world model, 18 real Powercasts, real artwork/audio mappings, native playback, persistent mini-player, world destinations, and existing state/persistence behavior.

The reconstruction is intentionally presentation-only: it changes how the experience is expressed without replacing the working runtime.

## Release sequence

1. Validate the exact `main` commit.
2. Assemble the canonical Worker Static Assets package.
3. Deploy the exact commit to the existing Cloudflare Worker.
4. Capture the deployment URL/version identity from Wrangler.
5. Open the resulting deployment URL.
6. Verify the front door, Hub, world field, Power Player, all artwork, playback, responsive behavior, accessibility, and core interactions.
7. Record evidence against the exact deployed commit.
8. Declare 10/10 only after all release gates pass.

## Do not

- create a new Cloudflare app/Worker for this build;
- use Vercel for this mission;
- use Cloudflare Pages for this Worker runtime;
- use a stale Worker URL as proof;
- create a second runtime;
- replace the runtime with a ZIP-only artifact;
- claim live verification from source inspection;
- claim 10/10 without rendered verification.

## Credential gate

The GitHub release workflow uses the official Cloudflare Wrangler action with `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. If those secrets are absent, deployment is **BLOCKED** rather than simulated or silently rerouted. Cloudflare's official CI/CD documentation requires these credentials for non-interactive Wrangler deployment.

## Operator handoff

The build system owns the infrastructure decision and release method. The only external dependency that may remain is authorization to the existing Cloudflare account through the repository's protected Actions secrets. No new application, Worker, or alternate hosting path should be created to bypass that gate.

## Final status vocabulary

- **IMPLEMENTED** = source exists.
- **SOURCE VERIFIED** = source structure and wiring inspected.
- **TESTED** = automated checks passed.
- **DEPLOYED** = Cloudflare release system reports deployment.
- **LIVE VERIFIED** = resulting URL was successfully checked.
- **PRODUCTION-PROVEN** = live behavior and evidence are recorded.
- **10/10** = all release and human visual gates pass.
