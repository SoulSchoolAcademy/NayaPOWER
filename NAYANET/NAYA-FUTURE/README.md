# NayaNET — Future Build

A fresh, self-contained entrance experience for **NayaNET**.

## Product

- **Entrance:** calm, immediate explanation of NayaNET.
- **NayaPOWER:** the intelligence authority and companion layer.
- **Power Player:** a focused listening / activation experience.
- **Intelligent Hub:** contextual intelligence, signals, and next-action focus.
- **Naya:** always-available guide, with a lightweight interaction surface.
- **Responsive:** desktop, tablet, and mobile layouts.
- **PWA-ready:** web manifest and install-safe structure.
- **Cloudflare-ready:** static Pages deployment with Wrangler.

## Cloudflare deployment

The repository workflow `.github/workflows/deploy-nayanet.yml` deploys this directory to the Cloudflare Pages project `nayanet` on pushes to `main`.

Required GitHub Actions secrets:

- `CLOUDFLARE_API_TOKEN` — token with Cloudflare Pages deployment permission.
- `CLOUDFLARE_ACCOUNT_ID` — Cloudflare account ID.

Once those two secrets exist, merging this build to `main` makes the deployment automatic. A manual `workflow_dispatch` is also supported.

## Architecture principle

This build is intentionally self-contained. It does not depend on the older E02 runtime, older feed UI, or an external iframe. The experience is a clean foundation that can be extended with real Naya services and persistent intelligence without replacing the entrance experience.
