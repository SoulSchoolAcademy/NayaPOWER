# Naya Power Handoff — Oscar Provenance Boundary

## Completed

Oscar acceptance is now mechanically bound to:

- exact claim fingerprint
- exact evidence-set fingerprint
- exact current commit
- exact checked-out Oscar implementation
- Oscar implementation blob SHA
- GitHub Actions execution provenance
- active CI run ID during promotion
- result integrity digest

Promotion independently recomputes these bindings. Retrieved content remains non-authoritative.

## Fresh Evidence

- PR #42 exact-head CI: run `32684385004`, head `5f93f2ba295bb29a9e48f8edaf011ac1fdd7a75f`, Oscar `ACCEPT`, promotion allowed, artifact `9505150597`.
- PR #43 initial attempt exposed a real test-fixture boundary failure: valid fixtures used a fixed run ID while CI supplied a live run ID. That run was rejected and not used as positive evidence.
- PR #43 corrected exact-head CI: run `32684522774`, head `dd2d1db7eb8f45aae0b835a8f2ee08d011ed64ab`, 18 Oscar tests PASS, 21 promotion tests PASS, Oscar `ACCEPT`, promotion allowed, artifact `9505194326`.
- Artifact `9505194326` digest: `sha256:62babc205e4ca5170b530c1c0d19cba6786267135ad9f055254771070b125b5f`.

## Merge Boundary

PR #43 merged to main as:

`02922d3e928e36e8f7b276fc0f3542ab22bb3ad5`

The exact merge commit is **not** labeled `VERIFIED_CI` because the accessible GitHub connector currently exposes the PR-triggered exact-head runs but not the push-triggered run listing for that merge SHA.

Do not infer exact merge-commit verification from the verified PR head.

## Next Execution Directive

**OBTAIN AND INSPECT FRESH PUSH-TRIGGERED CI FOR EXACT MAIN SHA `02922d3e928e36e8f7b276fc0f3542ab22bb3ad5`.**

Inspect every relevant workflow, job, step, log, artifact, and machine-readable result. Confirm the artifact commit SHA is exactly `02922d3e928e36e8f7b276fc0f3542ab22bb3ad5`. Only then update `STATE.current_main` to `VERIFIED_CI` and close the freshness boundary.
