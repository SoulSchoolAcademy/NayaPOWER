# PROOF PACKET C — Deployment / Live Acceptance
**Status:** PRE-DISPATCH (gates enumerated; not ready — see §8)
**Generated:** 2026-10-01 · **Owner:** Naya 2 (Muse)

## 1. Claim
The persistence seam is accepted for live deployment only when every gate
below is green. This packet enumerates the gates and their current state
honestly. **It is not an acceptance.**

## 2. Authority
Shawn's gates: no merges without his explicit promotion decision; no
production deployment/dispatch by any seat; production DB writes/migrations
are human steps. Readiness bar: 9.0+ to be ready; below 9.0 is not ready.

## 3. Source binding
Promotion candidate: PR #1243 branch @ `2a7851a8` (Packet B).
DB prerequisites: Packet A. Main freeze target was `a726a837`; main has
since moved to `694f62cd` — re-pin before any promotion decision.

## 4. Acceptance gates
| # | Gate | State | Evidence / blocker |
|---|---|---|---|
| 1 | Source proof complete | GREEN | Packet B |
| 2 | DB prerequisites verified | GREEN (2 human items open) | Packet A |
| 3 | Isolated round trip executed | **BLOCKED** | no disposable Postgres for this seat |
| 4 | V2.1 migration applied (human) | **OPEN** | `20261001032000` not applied |
| 5 | Full repo suite (CI, synthetic merge `bc4ddbf1`) | GREEN | 561 passed, 3 skipped, 0 failed; the local 523-pass run excluded pglast-dependent files (reduced suite) |
| 6 | GitHub Actions CI on the branch | GREEN (2026-10-01 ~16:35Z) | `test` + `chain-readiness-gate` SUCCESS on exact `2a7851a8` via pull_request event ~3 min post-push; standing "API pushes never trigger Actions" lesson corrected with live evidence |
| 7 | Shawn's promotion decision | **OPEN** | his call, fully briefed by Packets A/B |
| 8 | Merge (human-executed) | **OPEN** | no self-merge, ever |
| 9 | Post-merge production verification | **OPEN** | migration-application law: verify after apply |
| 10 | Live receipt end-to-end | **OPEN** | needs 1–9 |

## 5. Reconciliation
Gates 1–2 are evidence-complete. Gates 3–6 are mechanical/external
(disposable DB, human migration, CI trigger path). Gates 7–10 are
human-gated by standing law.

## 6. Material findings
- The CI trigger gap (AGENTS.md, 2026-10-01) means "no CI failure" on
  API-pushed branches is **not** "CI passed". Any promotion decision must
  weigh the local full-suite result instead, or someone with git access must
  push for real.
- The isolated round trip is the last *technical* proof outstanding; it is
  blocked on environment, not on design — the handoff is packaged and
  syntax-checked.

## 7. Execution record
Packet generated 2026-10-01; no deployment actions taken or attempted.
**Update 2026-10-01 ~10:15 PDT (dispatch 5935855302):** the isolated round
trip is DONE — 14/14 checks green on disposable local Postgres
(`naya_isolated_rt`), canonical foundation schema verbatim from migration
`20260919015207` (+ documented local auth/extensions stubs), canonical
writer `nayanet_record_ledger_event`. Full evidence: #554 `5936342882`,
`~/workspace/naya/isolated-db-handoff/roundtrip-proof-2026-10-01.txt`
(sha256 `7dcd265e…`), runner `isolated_roundtrip.py` (sha256 `2ec6c999…`).

Also proven in the same run: Demo-1 real effect EXECUTED at frozen head
`bf63549c` (LAW ADMISSIBLE, artifact sha256 matches disk, Naya 4's
fresh_verify.py V1/V2/V3 PASS in a fresh process); Demo-1 decision receipt
`dec-demo1-live-001` seal MATCH but honestly REFUSED by the adapter with
three classified boundary violations (missing decision_id, kernel_version,
verdict — different receipt family than naya-receipt-contract/1; no fields
invented, no unilateral widening).

## 8. Acceptance chain & readiness score
Chain: SOURCE ✓ → DB-PREREQS ✓(human items open) → ISOLATED-RT ✓ →
MIGRATION ⏳(human) → CI ✓ → DECISION ⏳(Shawn) → MERGE ⏳(human) →
VERIFY ⏳ → LIVE ⏳.
**Readiness: 8.0/10 — NOT READY.** Source proven, CI green on the exact
head, full suite green locally, isolated round trip proven 14/14.
Remaining: V2.1 migration (human), promotion decision + merge (Shawn).
Per the 9.0 bar, this does not ship on my authority — and the remaining gates
are exactly the ones Shawn reserved.

## 9. What this packet did and did not establish
Established: the complete, honest gate list. Did NOT establish acceptance.

## 10. Receipts
- Packets A and B (same directory); #554 `5935793156`, `5936342882`
