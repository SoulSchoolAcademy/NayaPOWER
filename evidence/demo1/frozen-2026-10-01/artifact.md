# Smart Note candidate — Demo-1 first governed effect (CANDIDATE — NOT RATIFIED)

Date: 2026-10-01
Source: Demo-1 P1 acceptance run, Naya 4 lane

## What happened
The first real bounded operation ran behind ACT's executor seam:
`staging.write_file` wrote this file to `demo-staging/`.

## Why it matters
Before this run, ACT's acceptance path used an echo/test executor — the
seam existed but no real operation stood behind it. Now:

- the capability is declared in the canonical Smart Door registry
  (DOOR-LOCAL-STAGING, status REGISTERED_DEMO — not production-live);
- the kernel projects that declaration into ACT's admission; no parallel
  registry was created;
- the executor enforces its bounds before any filesystem mutation
  (sandboxed path, name pattern, 64 KiB max, never overwrites);
- replay cannot produce a second effect (idempotency key + content hash);
- the execution receipt binds the artifact's sha256, so VERIFY can
  independently re-read and confirm what happened.

## Status
CANDIDATE. Auto-capture is not auto-ratification — only Shawn ratifies.
