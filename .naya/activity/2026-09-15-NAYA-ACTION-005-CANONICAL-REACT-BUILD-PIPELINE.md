# NAYA ACTION 005 — CANONICAL REACT BUILD PIPELINE

STATUS: PARTIAL VERIFIED — TAG → YOU'RE IT → EXECUTE

## Intent
Establish a genuine repository-owned build/artifact path for the exact NayaNET React/Vite Hub instead of relying on AppDeploy to compile source.

## Executed
- Hardened `.github/workflows/naya-canonical-react-build-handoff.yml` to typecheck, build, fingerprint, package, and upload the canonical React artifact.
- Added `scripts/build-canonical-react-hub.sh` as the repository-owned build adapter.
- Preserved the existing React/Vite architecture; no competing Hub was created.
- Recorded NAYA_ACTION_V1 action state.

## Evidence
- Previous AppDeploy source compilation failed at `npm run build` without an exposed compiler log.
- AppDeploy target remains restored to its prior READY snapshot.
- Existing GitHub behavioral-proof run `35030417628` failed in `qa_naya_context_boot.py` on an unrelated manifest-schema assertion before any React artifact proof; it cannot be promoted as React build evidence.

## Boundary
The requested immutable artifact has not yet been independently observed from a completed fresh artifact run in the accessible execution surface. Artifact SHA, artifact ID, AppDeploy artifact transport, desktop runtime, mobile runtime, and interaction runtime therefore remain UNKNOWN/UNPROVEN.

## Lesson
SOURCE → BUILD → ARTIFACT → TRANSPORT → DEPLOYMENT → RUNTIME is a chain of distinct evidence transitions. A green deployment or source-fresh mirror cannot substitute for an artifact proof.

## Protected
- No competing Hub.
- No fabricated artifact.
- No fabricated runtime proof.
- No promotion of historical evidence to current proof.
