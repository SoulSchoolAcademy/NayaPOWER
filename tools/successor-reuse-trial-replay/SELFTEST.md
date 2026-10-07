# replay-trial.mjs — SELF-TEST RECORD

**Date:** 2026-10-07 (run 20:40 UTC shift, successor-builder)
**Script:** `harness/replay-trial.mjs`
**Fixture:** `harness/selftest/fixtures/sr-selftest/archive/` (manifest + 2 arms
mirroring the SR-R2 verifier contract)

## Results (3/3)

| # | Case | Command | Expected | Observed |
|---|---|---|---|---|
| 1 | Clean archive | `node harness/replay-trial.mjs harness/selftest/fixtures/sr-selftest/archive` | exit 0, REPLAY MATCH | exit 0 — both arms integrity ok, verdicts PASS=PASS, REPLAY MATCH |
| 2 | Tampered recorded verdict | copy fixture to /tmp, set arm T `recorded_verdict` to FAIL (absolute verifier path) | exit 1, REPLAY MISMATCH | exit 1 — arm T replay PASS vs recorded FAIL → REPLAY MISMATCH |
| 3 | Tampered arm file | copy fixture to /tmp, append line to arm-b/sum.mjs | exit 2, hash mismatch | exit 2 — ARCHIVE ERROR: hash mismatch on sum.mjs |

All three exit-code paths verified: 0 = reproduce, 1 = contradiction,
2 = malformed/drifted archive. Verdicts are read from the verifier's final
stdout line (PASS/FAIL); arm code is executed under the manifest's recorded
`sandbox_posture` (local node, loopback HTTP only).

## Known limitation (documented, not hidden)

`harness/verifier-r2.mjs` derives the expected applicability answer from the
arm directory name containing `arm-t` — a blind-break shortcut. The replay
runner preserves verifier behavior byte-for-byte (it does not rewrite evidence);
future verifiers must take expected applicability from the manifest, not the
path. The fixture follows the existing convention.
