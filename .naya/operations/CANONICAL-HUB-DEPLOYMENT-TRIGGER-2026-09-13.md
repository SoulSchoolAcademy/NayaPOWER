# Canonical Hub Deployment Trigger — 2026-09-13

This file is an intentional repository change used to exercise the canonical production release path.

## Release law

An authorized push to `main` is the deployment approval for the canonical NayaNET Intelligent Hub. The deployment workflow must bind the exact pushed SHA to build, Cloudflare deployment, promotion, and independent public-runtime verification.

## Required proof

1. Exact `main` SHA is checked out.
2. Governance authority permits `deploy_public_runtime` for the canonical runtime.
3. NAYANET/HUB typecheck and production build pass.
4. Generated artifact is inspected against the canonical product contract.
5. Exact artifact is deployed to Cloudflare Worker `sparkling-shape-7ae5`.
6. The newest Worker version is explicitly promoted to 100%.
7. Public runtime and Smart Feed route independently prove the same release.
8. The release is not declared successful until live-runtime verification passes.

This trigger exists to make the end-to-end deployment path execute now, without requiring a manual workflow-dispatch button.
