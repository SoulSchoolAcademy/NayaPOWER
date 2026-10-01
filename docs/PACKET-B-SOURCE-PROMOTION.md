# PROOF PACKET B — Kernel/Adapter Source Promotion (persistence-seam-v3)
**Status:** COMPLETE (source proof; promotion decision is Shawn's)
**Generated:** 2026-10-01 · **Owner:** Naya 2 (Muse)

## 1. Claim
The persistence seam source at `2a7851a8` correctly projects real kernel
receipts: it accepts every well-formed seal the kernel produces, refuses
every malformed or forged seal tested, preserves the exact input state for
cold recomputation, and invents no execution outcomes.

## 2. Authority
Shawn's second master execution directive (2026-10-01). Standing: no
self-merge — this packet is evidence FOR the promotion decision, not the
decision. RED evidence preserved before every fix.

## 3. Source binding
- Branch `naya2/persistence-integration-package` @
  `2a7851a8c691256d85df98da627f7ac36b298ec0` (parent `bd4cffa6`).
- Pushed via Git Data API; all three remote blobs byte-verified
  (sha256 local == remote).
- **CI (corrected 2026-10-01):** the earlier "API pushes do not trigger
  Actions" claim was wrong. Exact-head CI on `2a7851a8` ran: `test` =
  success, `Collective Chain Readiness Gate` = success,
  `chain-readiness-gate` = success. Full suite on synthetic merge
  `bc4ddbf1a758129cabacdebda7e25ebe71eb94f7`: **561 passed, 3 skipped**.
  The local 523-pass run excluded pglast-dependent files (a reduced suite);
  CI is the full-suite evidence.
- Adapter tests: **24/24** green locally on the exact bytes (16 original +
  4 snapshot-aliasing RED→green + 4 substantive-validation RED→green).

## 4. RED evidence (preserved before fixes)
At exact `e48731ce` (PR #1243's prior head): `receipt_hash=123` (numeric)
ACCEPTED; resealed `verdict="BOGUS"` ACCEPTED; `issued_at="banana"` ACCEPTED;
`decision_id=123` ACCEPTED. Posted #554 `5935447995`. The bypass was real.

## 5. What v2/v3 fixed
- Seal: missing/null/numeric/non-string/malformed/mismatching `receipt_hash`
  refused; accepted shape = 64-char lowercase hex, independently recomputed.
- Vocabulary: `verdict` ∈ {PASS, FAIL, NEED_EVIDENCE}; `issued_at` ISO-8601;
  `receipt_id`/`decision_id`/`kernel_version` non-empty strings.
- Input commitment: `inputs_hash` recomputed over submitted `inputs_state`,
  mismatch refused; `recomputed-match` vs `absent-legacy` labeling.
- Provenance honesty: `kernel_sha`/`config_hash` are caller-supplied labels,
  not provenance proof. Shape ≠ isolation (documented, not hidden).
- CI: test discovery repaired without weakening the dependency guard.
- **v3:** `inputs_state` preserved verbatim in `p_metadata` — cold consumers
  recompute `inputs_hash` from the row alone (test_15).

## 6. Producer proof (the directive's core)
Naya 4's pairs (#554 `5935437274`), projected through v3:
| Pair | receipt_hash | inputs_hash | commitment | projection |
|---|---|---|---|---|
| P3 `demo-001` @ `4e87d4a` | MATCH | MATCH | recomputed-match | UNVERIFIED, verbatim |
| Demo-1 `demo1-act-know-live-001` @ `e7c4e622` | MATCH | MATCH | recomputed-match | UNVERIFIED, verbatim |
Posted #554 `5935618584`. The kernel's seal verifies with the kernel's own
canonicalization — no shared code, no trust-me.

## 7. Execution record
- Adapter tests: **24/24 pass** on exact working bytes (16 original + 4
  snapshot-aliasing RED→green (move 3) + 4 substantive-validation RED→green
  (move 4)). The 16/16 figure in earlier reports was the pre-hardening suite.
- Full repo suite (CI, synthetic merge
  `bc4ddbf1a758129cabacdebda7e25ebe71eb94f7`): **561 passed, 3 skipped,
  0 failed**. The local 523-pass run excluded pglast-dependent files — a
  reduced suite; CI is the full-suite evidence.
- GREEN confirmation posted #554 `5935555283` (v2); v3 posted `5935793156`.

## 8. Acceptance chain
RED PRESERVED ✓ → FIXED ✓ → BYTE-VERIFIED ✓ → PRODUCER-PROVEN ✓ →
FULL SUITE ⏳ → PROMOTION DECISION ⏳ (Shawn)

## 9. What this packet did and did not establish
Established: the adapter source is correct against real producer receipts.
Did NOT establish: database enforcement (Packet A), production behavior
(Packet C), or the merge decision itself.

## 10. Receipts
- PR #1243, branch @ `2a7851a8`; RED #554 `5935447995`; GREEN `5935555283`;
  v3 `5935793156`; proof `5935618584`
- Fixture: `tests/fixtures/seam-verify-001.json` (Naya 4's real receipt)
- Handoff: `~/workspace/naya/isolated-db-handoff/`
