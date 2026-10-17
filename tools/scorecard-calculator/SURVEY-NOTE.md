# Survey Note — prior/competing scorecard-calculator work (2026-10-17)

**Correction to the v1 receipt.** The v1 work receipt claimed "no competing
implementation." That claim was wrong. The different-seat validator found a
real competing implementation, read-only, on exactly one other branch:

- **Branch:** `naya5/scorecard-calculator-20261014` (Naya Verity, seat 5)
- **File:** `tools/scorecard.py`
- **Commit:** `411ea53370497cd82aabbc26f44ba07b0e3a50ba` (2026-10-14,
  "Scorecard calculator: to_10 solutions + 3-pass loop")
- **State:** read-only for this lane. This branch was not touched, edited, or
  listed for deletion — survey only.

## The two designs, honestly

They are **different calculators for different jobs**, not two versions of
one thing:

| | Verity's `tools/scorecard.py` | This lane's `scorecard_calc.py` |
|---|---|---|
| **Judge shape** | Generic 6-criteria rubric (evidence, verification, tests, value, prevention, honesty) — scored against prebuilt rubrics, anyone can use it | Mechanical first-pass judge of one rubric: the HV receipt law — verifies citations, applies evidence caps, emits the receipt-law frame |
| **Score math** | Overall = MINIMUM ("a chain is only as strong as its weakest link"; no criterion rescues another) | Weighted sum (USE .30, DELTA .25, PROOF .20, DURABLE .15, CLEAN .10), then banded verdict |
| **Evidence check** | Scored as a criterion; refs must be checkable; self-verification capped at 3 | **Mechanical:** every cited path/SHA/receipt verified against git *at the ref* — VERIFIED / ATTESTED / UNVERIFIABLE |
| **Caps** | Hard minimum via worst criterion | Three named downward-only caps: NO_EVIDENCE_CAP (3.0), UNCITED_CAP (5.0), RECEIPT_SOFT_CAP (8.0) |
| **Harm** | prevention criterion (gate that makes the class impossible) | Binary harm scan of the diff → DISQUALIFIED (no score), plus builder-attested harm |
| **Exits** | 0 = SHIP (≥9.5, math authorizes), 1 = FIX/HOLD, 2 = unreadable input (fail-closed) | 0 = scorecard emitted (incl. DISQUALIFIED — a verdict was reached), 2 = fail-safe, nothing emitted |
| **Receipt contract** | Shawn's 3-pass loop (`to_10` list, implement, re-score, ×3; SHIP needs ≥9.5) | NAYA-SCORECARD-RECEIPT-AUTHORITY-V1 5-step frame (options, scores, gates, decision, receipt), mechanically schema-validated before emission |
| **Receipt posting** | Not required | `--receipt-posted-comment-id` required — a private scorecard is not a gate (fail-closed) |
| **Unmeasurable** | via honesty criterion | Named `unmeasurable[]` list, stated never scored |
| **Network/quota** | Runs on the caller's JSON | stdlib-only, no network, no GitHub API, never spends quota |

## What is NOT decided here

The lineage decision — whether Verity's branch is superseded, retired,
kept as the general rubric instrument while this lane's judge serves the HV
receipt flow, or merged — is the **director/wiring decision's**, not this
lane's. See `WIRING-PROPOSAL.md` §6 (open questions); this note only records
that the other implementation exists and where.
