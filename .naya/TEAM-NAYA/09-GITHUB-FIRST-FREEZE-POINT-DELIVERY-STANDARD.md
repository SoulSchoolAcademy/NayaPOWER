# TEAM NAYA — GITHUB-FIRST FREEZE-POINT DELIVERY STANDARD

**DATE:** 2026-09-17
**STATUS:** CANONICAL TEAM-NAYA DELIVERY STANDARD V1

## PURPOSE

Shawn's preferred delivery model is **source of truth first, freeze point second, live deployment third**.

The hosting provider is secondary. The durable GitHub state is primary.

## REQUIRED DELIVERY ORDER

```text
GITHUB SOURCE OF TRUTH
        ↓
CLEAR COMMIT / FREEZE POINT
        ↓
DIRECT GITHUB FILE LINK FOR SAVING
        ↓
OPTIONAL LIVE DEPLOYMENT
        ↓
PUBLIC RUNTIME VERIFICATION
```

## RULES

1. **EDIT THE CANONICAL REPOSITORY FIRST** whenever practical.
2. **NEVER make a live deployment the only copy** of meaningful work.
3. After meaningful work, leave a clear commit/file state that Shawn can save locally.
4. When a standalone HTML artifact is appropriate, make it directly downloadable from GitHub so Shawn can inspect the freeze point on his computer.
5. Cloudflare and Vercel are both acceptable live hosts. Do not spend engineering effort choosing a host when the real problem is source, build, runtime, or verification.
6. Every live deployment claim must be backed by a public runtime check at the relevant URL.
7. Every substantive execution must leave evidence, Activity state, learning state, and one continuation action.
8. A freeze point is not merely a commit message. It is a recoverable state another Naya can identify, inspect, save, and continue from.

## SHAWN'S OPERATING PREFERENCE

When choosing between equivalent delivery paths:

**A. GitHub edit + direct downloadable freeze point is preferred.**

**B. GitHub source + Cloudflare live deployment is acceptable.**

**C. GitHub source + Vercel live deployment is acceptable.**

In all cases, preserve the GitHub source link so the work cannot be lost behind hosting infrastructure.

## WHAT SUCCESS LOOKS LIKE

Shawn should be able to:

- click the GitHub source;
- download/save the current artifact;
- inspect the exact freeze point;
- optionally open the live deployment;
- see the same work represented by source and runtime;
- return later and have another Naya restore the state without asking Shawn to reconstruct it.

## NON-NEGOTIABLE CONTINUITY RULE

> **LIVE IS A PROJECTION. GITHUB IS THE SAVED SOURCE. THE FREEZE POINT IS THE HANDOFF.**

This standard applies to Hub work, Naya interfaces, Smart Note tooling, Activity projections, and future NayaNET artifacts unless a governing source explicitly requires another delivery mechanism.

**END — GITHUB-FIRST FREEZE-POINT DELIVERY STANDARD**
