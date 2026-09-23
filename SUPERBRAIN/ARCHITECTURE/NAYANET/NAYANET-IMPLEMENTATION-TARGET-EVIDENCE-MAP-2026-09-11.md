# NayaNET Implementation Target Evidence Map — 2026-09-11

**Status:** CANONICAL EVIDENCE RECEIPT
**Purpose:** Establish the implementation substrate and deployment pairing from repository evidence before further product construction.

## Executive conclusion

The evidence does **not** support selecting one of the separate legacy NayaNET-named repositories as the current NayaNET implementation target.

The evidence supports:

- **Canonical implementation repository:** `SoulSchoolAcademy/NayaPOWER`
- **Canonical implementation path:** `NAYANET/HUB/`
- **Current observed repository HEAD:** `1cd574ecb6518adad8cb44b680484067e69312a0`
- **Canonical deployment workflow:** `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`
- **Canonical deployment target:** Cloudflare Worker `aged-art-7c12`
- **Canonical runtime named by the release authority:** `https://aged-art-7c12.nayanet.workers.dev`

The important remaining gap is **current-head deployment parity**: the current HEAD is newer than the previously verified production source SHA. Therefore the target is established, but the current HEAD is not yet production-proven.

## Evidence

### 1. NAYANET/HUB is an actual executable application

`NAYANET/HUB/package.json` identifies a private Vite/React application named `nayanet-intelligent-hub` with `build` and `typecheck` scripts. Its build copies the canonical cognitive engine into the public artifact before running Vite. This is materially different from a planning-only directory.

### 2. The canonical release authority explicitly names the source and runtime

`NAYANET/HUB/CANONICAL-RELEASE-STATUS-2026-09-09.md` identifies:

- canonical source: `NAYANET/HUB/`
- canonical deployment workflow: `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`
- canonical runtime: `https://aged-art-7c12.nayanet.workers.dev`

It also explicitly states that the legacy timestamped standalone HTML artifact is not canonical.

### 3. The release workflow independently binds source to deployment

The canonical V2 workflow checks out exact `main`, captures the source SHA, builds from `NAYANET/HUB`, inspects the generated artifact, deploys Worker `aged-art-7c12`, promotes the new version to 100%, and independently probes the public runtime for source/asset parity.

### 4. Separate NayaNET-named repositories were inspected

#### `SoulSchoolAcademy/nayanetsmartapp`

**Disposition: HISTORY / REUSABLE ASSET, NOT CURRENT TARGET**

Evidence:
- last commit observed: 2025-08-09
- repository description: older SmartNet Core / automator application
- actual code: Next.js 14 + React + Octokit GitHub App integration
- no evidence in current NayaPOWER release authority that this repository is the current NayaNET product source

This is potentially valuable historical implementation material, especially for GitHub App integration, but it is not evidence-backed as the current target.

#### `SoulSchoolAcademy/nayanetsmartnetlife`

**Disposition: HISTORY / REFERENCE ASSET, NOT CURRENT TARGET**

Evidence:
- last commit observed: 2026-09-06
- repository contains a README describing SmartNet Core, but the current tree is only a small set of files/assets and an empty `index.html`
- no current executable application structure comparable to `NAYANET/HUB`
- no evidence connecting it to the canonical current release workflow

Its screenshots/assets may be useful as historical design/reference material.

#### `SoulSchoolAcademy/nayanetwork`

**Disposition: HISTORY / DEPLOYMENT PROOF EXPERIMENT, NOT CURRENT TARGET**

Evidence:
- last observed activity is August 2025
- README explicitly describes a minimal Vercel deployment proof using static HTML and `/api/ping`
- this is a deployment experiment, not the current NayaNET product implementation

#### `SoulSchoolAcademy/Nayanetissmartnet`

**Disposition: HISTORY / REUSABLE ASSET, NOT CURRENT TARGET**

Evidence:
- Next.js application with academy, ledger, chat, command, status, store, and API routes
- repository structure demonstrates real historical SmartNet functionality
- no evidence connecting its current `main` to the current canonical NayaNET release authority

#### `SoulSchoolAcademy/Nayanetsystems`

**Disposition: HISTORY / MINIMAL INFRASTRUCTURE ASSET, NOT CURRENT TARGET**

Evidence:
- tiny Vercel-oriented project with `index.html`, `api/ping.js`, and `vercel.json`
- no evidence of current NayaNET product implementation

#### `SoulSchoolAcademy/Nayanetworks`

**Disposition: EMPTY / HISTORY**

Evidence:
- current tree contains only `.gitattributes`, `.gitignore`, and a short README
- no executable product source observed

#### `SoulSchoolAcademy/nayanetsmartee`

**Disposition: EMPTY / HISTORY**

Evidence:
- current tree contains README plus an empty `components` blob
- no executable product implementation observed

## Authority decision

**TARGET:** `SoulSchoolAcademy/NayaPOWER:NAYANET/HUB`

**Do not migrate the product into a separate NayaNET-named repository merely because its name appears more product-like.** The current canonical release authority already establishes the implementation boundary inside NayaPOWER.

## Current source/deployment relationship

The relationship is:

`NayaPOWER/main → NAYANET/HUB → canonical V2 build → Cloudflare Worker aged-art-7c12 → public runtime`

However, the latest independently observed successful production release predates the current HEAD. Therefore:

- **Target established:** YES
- **Source executable:** YES
- **Canonical deployment path defined:** YES
- **Current HEAD production parity:** NOT YET PROVEN
- **Current HEAD production GREEN:** NO CLAIM

## Next gate

The next highest-value action is no longer repository archaeology.

It is:

> **Run the canonical NayaNET V2 source → build → deploy → independent public-runtime parity proof against the current `main` HEAD, then inspect the actual rendered product and repair only material defects.**

Do not redesign or migrate repositories before this proof.

**Truth boundary:** IMPLEMENTED ≠ BUILT ≠ DEPLOYED ≠ RUNTIME-VERIFIED ≠ PRODUCTION-PROVEN.
