# Successor-reuse trial replay — one-command independent verification of trial scoring

**What:** `replay-trial.mjs` replays a trial from its archive: it verifies
SHA-256 integrity of the archived arm submissions, re-executes the recorded
deterministic verifier against them, and asserts the verdicts match the
recorded result.

**Usage:** `node tools/successor-reuse-trial-replay/replay-trial.mjs trials/<trial-id>/archive`

**Exit codes:** 0 = REPLAY MATCH · 1 = REPLAY MISMATCH (archive contradicts its
recorded result) · 2 = archive malformed or drifted (hash mismatch, missing
manifest/arms/verifier).

**Manifest convention** (`trials/<trial-id>/archive/manifest.json`):
- `verifier` is resolved relative to `trials/<trial-id>/` (e.g. `../harness/verifier-r2.mjs`).
- Each arm entry: `submission_dir`, `applicability`, `recorded_verdict`, `file_hashes`
  (SHA-256 of every archived submission file).
- `sandbox_posture` records how the verifier ran. Replay EXECUTES archived arm
  submissions — agent-written code — under that same posture. Never replay an
  archive you have not inspected.

**Archive contract (protocol §10):** from trial SR-P1 onward every trial ships
a replayable archive (preregistration as-run, exact briefs, all arm
submissions, applicability answers, verifier reference + raw output, manifest,
scorer identity, timestamps). A trial without a passing replay is not evidence.

**Self-test:** `SELFTEST.md` records 3/3 green (clean archive → MATCH,
tampered verdict → MISMATCH, tampered file → integrity FAIL). Fixture under
`selftest/fixtures/sr-selftest/archive/`.

**Honest boundary:** rehearsal trials R0–R2 (2026-10-06) predate the contract
and are NOT replayable — arm submissions ran in temp dirs that were never
persisted. Their result files say so explicitly. This contract closes the gap
for future trials; it does not retroactively fill the old ones.

**Known limitation:** `harness/verifier-r2.mjs` derives the expected
applicability answer from the arm directory name (a blind-break shortcut).
The runner preserves verifier behavior byte-for-byte; future verifiers must
take expected applicability from the manifest.
