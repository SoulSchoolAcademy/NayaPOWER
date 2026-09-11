# NayaNET E02 Deployment Notes

## Canonical source

`NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE/`

## Canonical experience runtime

The NayaNET 10 experience is now a single active front-end shell:

- `index.html` — portal, Living Sun, world destination shell, persistent player
- `nayanet-10-experience.css` — canonical active visual system
- `nayanet-10.js` — canonical active interaction/state controller
- `naya-data.js` — protected persistence bridge (Supabase + local continuity)
- `powercasts.json` — existing canonical content reference

The older E02 runtime files remain in the repository as protected historical/runtime capabilities but are **not loaded by the canonical NayaNET 10 shell**. No new parallel runtime is to be introduced.

## Experience contract

`PORTAL → THRESHOLD → NAYA → LIVING SUN → 9 WORLDS → POWER PLAYER → 18 POWERCASTS → INTELLIGENCE → CONNECTION`

The experience preserves:

- name → intelligent-hub transition
- local continuity and protected persistence bridge
- private-intelligence boundary
- nine locked NayaNET worlds
- all 18 canonical Powercast artwork/audio mappings
- persistent player state
- full destination expansion with return to Naya
- responsive/mobile behavior and reduced-motion support

## Release gates

Before Cloudflare publication, verify:

1. HTML parses and renders.
2. Canonical CSS loads; no obsolete stylesheet is referenced.
3. Canonical JS loads without startup errors.
4. Name entry crosses the threshold.
5. Living Sun renders Naya + exactly nine worlds.
6. Player renders real Powercast artwork and maps all 18 audio/image records.
7. Selecting a Powercast updates the player and persistent mini-player.
8. Every world opens a full destination and returns cleanly to Naya.
9. Smart Notes / challenge / spaces preserve state locally; persistence bridge remains truthful.
10. MAXESS links to the real assessment destination; no fake score is fabricated.
11. Mobile uses the dedicated responsive composition; desktop uses the spatial composition.
12. Reduced motion and keyboard focus remain usable.
13. Missing media fails gracefully without breaking the shell.
14. Exact release artifact is inspected before publication.
15. Deployed URL is tested separately; do not infer live success from GitHub commits.

**CONNECTED ≠ DEPLOYED. COMMITTED ≠ RELEASED. VERIFIED ≠ PRODUCTION-PROVEN.**

## Canonical automation boundary — 2026-09-10

The active release workflow is `.github/workflows/deploy-canonical-e02.yml`.

Its contract is:

**SOURCE → VERIFY → SYNTAX CHECK → DEPLOY → EVIDENCE**

The release workflow is read-only against GitHub source. Deployment must never modify `main` as a side effect. This prevents release recursion and preserves source/deployment provenance.

The legacy self-mutating Cloudflare workflow has been retired. The separate one-time live-branch mutator has also been retired because its canonical feed upgrade is already present on the live branch.
