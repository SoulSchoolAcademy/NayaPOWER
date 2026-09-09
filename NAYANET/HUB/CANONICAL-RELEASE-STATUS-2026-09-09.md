# NayaNET Intelligent Hub — Canonical Release Evidence

**Date:** 2026-09-09
**Canonical source:** `NAYANET/HUB/`
**Canonical deployment workflow:** `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`
**Canonical runtime:** `https://aged-art-7c12.nayanet.workers.dev`

## Authority boundary

The timestamped file `2026 09 09 1213 NAYANET HUB.html` is a legacy standalone HTML artifact. It is **not** the canonical React Hub source.

The production Hub is the React application under `NAYANET/HUB/`. Changes to the canonical product must be made there and then proven through build, deployment, and exact public-runtime verification.

## Release-blocking finding

A prior canonical deployment successfully built and uploaded the React artifact but the public runtime served a different/stale JavaScript asset. That means:

`SOURCE != ARTIFACT != PUBLIC RUNTIME`

The release is therefore blocked until exact source-to-runtime parity is independently observed.

## Current repair

The canonical V2 release workflow is responsible for:

1. capturing the exact checked-out source SHA;
2. building the React Hub from `NAYANET/HUB`;
3. inspecting the generated artifact for required Smart Feed markers and forbidden internal Superbrain UI;
4. deploying the artifact;
5. explicitly promoting the newly deployed Worker version to 100% traffic;
6. probing the exact public runtime until parity is observed;
7. requiring the public runtime to expose the exact source commit and expected JavaScript asset before release can pass.

## Product boundary

The Intelligent Hub must not expose internal Superbrain/operator controls such as:

- Where's Naya Now
- CAPTURE
- PASS THE TORCH
- FIND
- VERIFY STATE
- internal EVENTS / RECEIPTS / MEMORY operator panels

Those belong to the internal Superbrain/operator layer, not the user-facing Hub.

## Smart Feed target

The canonical Smart Feed remains the user-facing intelligence surface with:

- Collective Intelligence as the primary lens;
- Personal Intelligence;
- Activity Feed;
- In a Nutshell;
- Human;
- Child;
- Grandma;
- Naya;
- Machine / Evidence;
- Weaver / Synthesis where supported;
- What We Learned;
- What It Means;
- What To Do;
- Favorite / Save / Create Space at the top-right;
- Love / Like / Rank / Share and comment in the engagement area;
- contextual Ask Naya;
- Connect / related intelligence;
- trust, provenance, and verification.

## Evidence rule

**NO EVIDENCE = NO CLAIM.**

The release is not considered successful until build, deployment, exact runtime parity, and visual proof all pass against the same canonical source SHA.
