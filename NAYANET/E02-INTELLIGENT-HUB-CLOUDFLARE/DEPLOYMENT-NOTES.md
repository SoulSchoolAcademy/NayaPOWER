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

## Release-authority reconciliation — 2026-09-10

The repository currently contains more than one NayaNET product surface. The E02 directory is the canonical NayaNET 10 experience source, but the verified production deployment workflow presently registered in `.github/workflows/deploy-nayanet-hub-canonical.yml` builds and deploys `NAYANET/HUB` to the `aged-art-7c12` Cloudflare Worker.

That is a **source/deployment authority mismatch** and must not be papered over.

Therefore:

- E02 remains the documented NayaNET 10 experience source.
- `NAYANET/HUB` remains the currently registered production release source until an explicit promotion is verified.
- No second E02 deployment workflow is permitted merely to make the documentation appear green.
- Production promotion must establish exact source SHA → build artifact → deployed Worker → independently observed public runtime parity.

The legacy self-mutating Living Sun deploy workflow has been retired. The one-time live-branch mutator has also been retired because its canonical feed upgrade is already present on the live branch.

**NEXT RELEASE GATE: reconcile E02 with the actual production release authority, then run the existing production build/deploy/independent-runtime verification without creating a parallel deployment path.**
