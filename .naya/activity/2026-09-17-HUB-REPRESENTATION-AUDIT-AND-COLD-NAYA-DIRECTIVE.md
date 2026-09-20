# Activity — Hub Representation Audit + Cold-Naya Execution Directive

**Date:** 2026-09-17  
**Mission:** Make Hub source routing unambiguous and cold-Naya-proof.  
**Authority:** Shawn Vibert  
**Status:** COMPLETED — AUDIT RECORDED; EXECUTION DIRECTIVE INSTALLED

## What was inspected

The `main` branch was inspected for the known Hub representations and the relevant files were opened directly.

### Protected current Hub

`2026 09 17 NAYANET HUB.html`

Result: **CURRENT / PROTECTED FREEZE POINT.**

The artifact was directly fetched and confirmed to be a standalone HTML Hub. It was not modified.

### React/Vite implementation

`NAYANET/HUB/`

Result: **ACTIVE REFERENCE IMPLEMENTATION, NOT CURRENT STANDALONE FREEZE POINT.**

The directory contains a real React/Vite application with `index.html`, `src/`, package/build configuration, and data/intelligence implementation. It remains useful implementation evidence but cannot silently redefine the current Hub.

### Conflicting release documentation

`NAYANET/HUB/CANONICAL-RELEASE-STATUS-2026-09-09.md`

Result: **HISTORICAL / REFERENCE.**

It declares `NAYANET/HUB/` canonical and names an older Cloudflare runtime. That conflicts with the current 2026-09-17 freeze-point decision.

It also references `2026 09 09 1213 NAYANET HUB.html`; that path was directly checked on `main` and is currently not found. The reference is therefore stale.

### Conflicting release marker

`NAYANET/HUB/RELEASE-MARKER.md`

Result: **HISTORICAL / REFERENCE.**

It describes a Vite/Cloudflare release path as canonical. That is not the current standalone Hub identity for this phase.

### Foundation contract

`NAYANET/HUB/FOUNDATION-CONTRACT.md`

Result: **ACTIVE ARCHITECTURE/DESIGN REFERENCE; NOT HUB IDENTITY AUTHORITY.**

It remains valuable for React implementation architecture, routes, intelligence contracts, visual system, and verification gates. Its older statement that `NAYANET/HUB/` is the canonical Hub source is superseded for the current standalone-freeze phase.

### Vercel metadata

`NAYANET/HUB/.vercel/project.json`

Result: **NON-CURRENT DEPLOYMENT METADATA.**

It points at a Vercel project and must not be used as evidence that Vercel defines the current Hub. Deployment metadata is not source authority.

### Implementation/support files

`NAYANET/HUB/package.json`, `package-lock.json`, `vite.config.ts`, `tsconfig.json`, `wrangler.jsonc`, `index.html`, `src/**`, and `scripts/**`

Result: **REFERENCE IMPLEMENTATION SUPPORT.**

These remain available for engineering inspection and future work. They do not become the current Hub merely by existing.

### Generated/runtime representations

Generated build output, ignored `dist/`, generated PIS projection files, cached deployment artifacts, and public runtime copies

Result: **PROJECTIONS / EVIDENCE SOURCES, NOT SOURCE AUTHORITY.**

A runtime can prove what is live. It cannot redefine Shawn's protected source freeze point.

## Decision

The repository now has one deterministic Hub identity for this phase:

**CURRENT HUB = `2026 09 17 NAYANET HUB.html`**

It remains protected and is not to be edited in place.

All new Hub iteration must be created as a new, unambiguous, versioned artifact.

## Installed control

A cold-Naya execution directive and representation registry was created at:

`.naya/TEAM-NAYA/11-CANONICAL-HUB-REPRESENTATION-REGISTRY-AND-EXECUTION-DIRECTIVE.md`

That directive contains:
- the mission;
- the one current Hub answer;
- representation-by-representation classification;
- authority order;
- pre-edit procedure;
- ten things being accomplished today;
- evidence requirements;
- do-not-do rules;
- required session output;
- one exact continuation action.

## Evidence rule reinforced

The primary human evidence for work is:

1. clickable direct GitHub artifact link;
2. clickable Activity record;
3. clickable Smart Note when durable learning is created;
4. clickable canonical source/contract link.

Commit SHA, blob SHA, workflow run, deployment ID, and runtime URL are supporting provenance, not substitutes for the human-readable evidence links.

## Learning

Repository organization is part of Superbrain intelligence.

The important lesson is not merely that several Hub representations exist. The lesson is that **source identity, freeze-point identity, implementation identity, deployment identity, and runtime identity are different objects and must be explicitly related by authority.**

A future Naya must not infer currentness from filename age, technical sophistication, deployment existence, or historical documentation.

## Protected

- `2026 09 17 NAYANET HUB.html` was not edited.
- No existing Hub implementation was deleted.
- No deployment was promoted.
- No Vercel credential/deployment work was performed.

## Next execution

**Create the first new versioned Hub artifact with ONE controlled improvement. Verify the new artifact against the protected baseline, record Activity and Smart Note evidence, and return the direct clickable GitHub link to Shawn.**
