# NayaNET Intelligent Hub — Canonical Vite/Cloudflare Release Marker

Canonical source boundary: `NAYANET/HUB/`

Canonical runtime: `https://aged-art-7c12.nayanet.workers.dev`

Canonical production workflow: `.github/workflows/deploy-nayanet-hub-canonical-v2.yml`

Release law:

`SOURCE → TYPECHECK → VITE BUILD → ARTIFACT → CLOUDFLARE → EXACT RUNTIME → JS/CSS ASSET OBSERVATION → INTERACTION → 99.99 MIRROR`

The runtime verifier intentionally inspects the generated React JavaScript asset, not only `index.html`, because the Hub's intelligence UI is client-rendered.

This commit is an auditable trigger for the canonical release path.

Trigger architecture: `hub-canonical-release-trigger.yml` is trigger-only; all build/deploy/verify logic remains centralized in the canonical V2 workflow.
