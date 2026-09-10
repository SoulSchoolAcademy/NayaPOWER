# NEXT NAYA EXECUTION — NayaNET Hub

You are the successor Naya. Treat conversation memory as empty. Restore `SUPERBRAIN/AI-BOOT/START-HERE.md` and `SUPERBRAIN/AI-BOOT/NAYANET-HUB-READ-FIRST.md`, then read the Foundation Contract, Elite Construction Brief, Torch-Passing Operating Law, and Ten-Star Service Code directly from GitHub.

## Current verified state

The concrete source divergence `AppShell.tsx` absent / `App.tsx` owning the permanent shell has been repaired. `NAYANET/HUB/src/app/AppShell.tsx` now owns the shell. `App.tsx` composes through it. `routes.ts` remains the route registry. The canonical Cloudflare worker packaging now treats the registered Hub routes as SPA routes.

## Current unknowns

CI/build status for the latest Hub-triggered release, Cloudflare deployment success, exact runtime source commit, exact public DOM/assets, interaction, responsive behavior, and visual quality are UNKNOWN.

## SINGLE NEXT ACTION

Verify the release chain for the latest Hub source changes.

1. Inspect the newest GitHub Actions run for the canonical Hub release.
2. If a gate fails, identify the FIRST failed gate and repair only that gate.
3. If build/deploy passes, independently observe `https://aged-art-7c12.nayanet.workers.dev`.
4. Verify `/`, `/feed`, and one additional registered route.
5. Verify runtime source identity, DOM/assets, interaction, responsive behavior, and visual result.
6. Record the complete human-thought check and update GitHub Issue #151.

## DO NOT

Do not redesign SmartFeedBoard yet.
Do not create another shell.
Do not create another route registry.
Do not create another feed renderer.
Do not use Vercel.
Do not treat source or commit existence as runtime proof.
Do not declare success while release-blocking UNKNOWNs remain.

## PASS CONDITION

SOURCE → TYPECHECK → BUILD → ARTIFACT → CLOUDFLARE → EXACT RUNTIME → ROUTE PARITY → INTERACTION → RESPONSIVE → VISUAL, all proven against one source identity.

Then decide the next smallest high-value slice using evidence.
