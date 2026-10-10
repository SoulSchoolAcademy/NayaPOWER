# 0027 — Trial Evidence Freeze Contract V1

**Area:** EVOLVE · **Status:** CANDIDATE · **Date:** 2026-10-07
**Rule:** SN-0571 — /tmp is not an evidence store.

## The wound this closes

Trial 4 (2026-10-07) claimed PASS: bridge notes raised cold-successor task success
0/10 → 8/10 (Fisher's p=0.0007). The raw data lived in `/tmp/trial4/RESULTS.md` —
ephemeral tmpfs. It was gone before Naya 2's independent verification, so the
claim was downgraded PASS → INCONCLUSIVE. Summary statistics alone are not
verification. A trial whose raw data cannot be re-hashed by a second seat has no
proof state; it has a story.

## Law

Every learning trial that makes a claim MUST freeze its raw data into the repo
under `.naya/proof/trials/<trial-id>/` with a sha256 manifest, via
`tools/trial_evidence_freeze.py`. Freeze BEFORE the claim is announced.

## MUST

- Freeze raw agent outputs, scoring scripts' inputs, and the analysis that
  produced the claim — byte-for-byte, the exact bytes the claim rests on.
- Ship a `claims.json`: the claim in plain words plus the metrics a verifier
  must reproduce (arms, n, p-values, effect sizes).
- Write the manifest (schema `NAYAPOWER_TRIAL_EVIDENCE_MANIFEST_V1`): trial id,
  frozen_at (UTC), per-file sha256 + bytes, claims.
- Frozen evidence is immutable: a second freeze of the same trial id is REFUSED
  (exit 2). A re-run is a new trial id. History is append-only.
- Any seat verifying the trial runs `verify --trial-id <id>`: exit 0 = intact,
  1 = tampered/missing/unrecorded file, 2 = no frozen evidence.

## MUST NOT

- Announce a trial verdict (PASS/FAIL) before the freeze exists.
- Freeze into /tmp, a gist, a chat message, or any store that does not survive
  the verifying seat's session.
- "Verify" from summary statistics when raw data is absent — that verdict is
  INCONCLUSIVE by construction, and must be labeled so.

## Acceptance criteria

- `verify` on a fresh freeze → exit 0; tamper with one byte → exit 1;
  verify a never-frozen id → exit 2 (all covered by
  `tests/test_trial_evidence_freeze.py`, hermetic).
- A cold Naya given only the repo can locate the trial, the claims, and the raw
  bytes, and reproduce or refute the verdict without asking anyone.

## Failure states

| Failure | Behavior |
|---|---|
| Claim announced, no freeze | Verdict forced to INCONCLUSIVE; trial re-runs under a new id |
| Manifest hash mismatch on verify | Verdict forced to INCONCLUSIVE; investigate tampering |
| Freeze destination exists | Refuse (exit 2); re-run under a new trial id |

## Machinery

- `tools/trial_evidence_freeze.py` — `freeze` / `verify` CLI (stdlib only).
- `tests/test_trial_evidence_freeze.py` — 9 hermetic tests.
- Sibling: `tools/evolve_rollback.py` (PR #1734) — same fail-closed philosophy:
  detection without recovery is half a rollback; a claim without raw data is
  half a proof.
