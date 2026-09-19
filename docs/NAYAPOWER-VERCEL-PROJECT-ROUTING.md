# 🔱 NayaPOWER — Deployment Routing Law

**STATUS:** CANONICAL CROSS-PROJECT DEPLOYMENT GUARDRAIL  
**LAST CONFIRMED:** 2026-09-19

## PURPOSE

Separate governance authority from application deployment ownership.

- NayaPOWER governs the operating system and cross-project rules.
- NayaNET Hub source of truth is the GitHub repository.
- **NayaNET Hub canonical runtime deployment is Cloudflare.**
- MAXIS deployment ownership is independent of NayaPOWER governance.

## CANONICAL ROUTING

### NayaPOWER / NayaNET Hub

`SoulSchoolAcademy/NayaPOWER` → `main` → GitHub canonical source → authorized Cloudflare workflow → Worker `sparkling-shape-7ae5`

Cloudflare account:
`b5e2a51b3e883f7722287c5f51b1196b`

Canonical runtime:
`https://sparkling-shape-7ae5.smartnetpodcast.workers.dev`

Canonical release workflow:

`.github/workflows/assistant-cloudflare-hub-release.yml`

### MAXIS

MAXIS deployment routing is governed by the MAXIS repository and its own deployment configuration. NayaPOWER must not substitute its own deployment surface for MAXIS.

## HARD RULE

**Do not substitute Vercel, AppDeploy, or another deployment platform for the canonical NayaPOWER/NayaNET Hub Cloudflare runtime.**

For NayaPOWER/NayaNET Hub, resolve:

`SoulSchoolAcademy/NayaPOWER` → exact source commit → authorized Cloudflare release workflow → `sparkling-shape-7ae5`

If those identities do not match, STOP and resolve the routing contradiction before changing application code.

## TRUTH RULE

**GitHub source != released runtime; committed != released; verified build != production-proven.**

A deployment is not claimed until the exact source/artifact/runtime identity and independent runtime evidence exist.

## HISTORICAL NOTE

Older repository files may still contain Vercel configuration from an earlier deployment architecture. Those files are **not the canonical NayaPOWER/NayaNET release surface** and must not be used to select or authorize a deployment.
