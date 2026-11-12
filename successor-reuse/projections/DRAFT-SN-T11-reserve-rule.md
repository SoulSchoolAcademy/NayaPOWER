# SMART NOTE (DRAFT — ingestion candidate, NOT canonically captured)

> **Draft for the CAPTURE lane.** This file is an ingestion-ready candidate
> projection, not a canonical Intelligent Block. The canonical Receiver
> (`v7-smart-note-canonical`) remains the single capture path; no registry
> entry was written and no IB was minted by this draft. Truth state below is
> the draft's honest assessment, for the ingesting seat to adjudicate.

| Field | Value |
|---|---|
| Smart Note ID | `SN-DRAFT-T11` (to be assigned at ingestion) |
| Human title | The Reserve Rule — dispatch the lower-scored call when the top two are within 0.5 |
| Category | OPERATIONAL INTELLIGENCE |
| Topic | DISPATCH |
| Subtopic | RESERVE RULE |
| Captured | 2026-10-08 UTC |
| Truth state | VERIFIED (Naya 1 independent verification; see proof) |
| Source lesson | `learning_evidence` row `1589c693-e230-4c3a-84c6-ad4fab723ef8` (T11, Trial-11), status ACTIVE, level E5_CAN_TEACH, provenance TRIAL_EVIDENCE |

---

## ✦ IN A NUTSHELL

**Reserve Rule for dispatch decisions: when the two highest-scored waiting calls are within 0.5 points of each other, dispatch the LOWER-scored call first — not the higher.**

Why: the higher-scored call is closer to the 9.0 critical threshold and may escalate; holding your best unit in reserve covers the likely escalation. The naive heuristic (always dispatch the highest-scored call first) is wrong in exactly this band. The rule does NOT apply when the gap exceeds 0.5 — then dispatch the highest scorer normally. Boundary: gap ≤ 0.5 → lower first; gap > 0.5 → highest first. Example: calls at 8.4 vs 8.0 (gap 0.4) → dispatch the 8.0 call; calls at 8.6 vs 7.1 (gap 1.5) → dispatch the 8.6 call.

For a cold successor facing a dispatch decision: check the gap between the top two scores first. If it is 0.5 or less, resist the urge to send the best unit to the best-looking call — send the lower one and keep the best in reserve.

---

## 🩷 HUMAN NOTE

The obvious move — send your best unit to the highest-priority call — is wrong when two calls are close in score. The higher one is near the critical threshold and may blow up; if your best unit is already committed, you have nothing left for the escalation. Dispatch the lower of two close calls, keep the ace in reserve.

---

## 🟣 CHILD NOTE

Imagine two kids both want the last cookie and they're almost equally hungry. You'd think: give it to the hungrier one. But the hungrier one might get really upset and need a grown-up — so you give the cookie to the less-hungry kid and keep the grown-up free, just in case.

---

## 🔵 GRANDMA NOTE

When two jobs are nearly tied in urgency, don't throw your best worker at the slightly more urgent one. That one is close to becoming an emergency, and if it does, you'll want your best worker still free. Send the second-best to the tied job; keep the best in reserve.

---

## 🟠 NAYA NOTE

Applicability: dispatch / slot-allocation decisions with scored candidates and a critical/escalation threshold. Do NOT apply outside dispatch-like decisions (no escalation concept, no reserve concept). The 0.5 boundary is the applicability edge — applying the rule at gap > 0.5 is a leak, and successor-reuse trial SR-P2's refusal probe verified the boundary holds (10/10 B arms, zero leaks).

---

## 🟢 MACHINE NOTE

```json
{
  "lesson_id": "T11",
  "rule": "gap(top_two_scores) <= 0.5 → dispatch argmin(top_two); else dispatch argmax(top_two)",
  "threshold": 0.5,
  "critical_threshold_reference": 9.0,
  "applicability_domain": "dispatch/slot-allocation with scored candidates",
  "non_applicability": "decisions without an escalation/reserve concept"
}
```

---

## 🧪 WHAT THIS SPECIMEN ACTUALLY PROVED

- Trial-11 (Naya 4): treatment 9/10 vs control 0/10 on reserve scenarios; Fisher p=0.000119, h=2.84. Normal scenarios 10/10 (no over-application).
- Naya 1 independent re-grade: treatment 90/90 vs control 39/90, p=1.95e-13, h=1.70.
- Successor-reuse trial SR-P2-20261008 (Naya 5): cold successors WITH the lesson 10/10 vs WITHOUT 0/10 on a held-out task; Fisher p=5.41e-06, Δ=1.00; attribution STRONG; refusal probe 10/10 PASS. Verdict: IMPROVED. (Independent replay requested, pending.)
- Retrieval path in SR-P2 was STUBBED — the lesson reached the successor by direct handoff, not by `smart_note_v2.py retrieve`. This draft exists to close that gap.

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the rule changes dispatch behavior measurably and the 0.5 boundary holds under probe. **Not proven:** that the rule is optimal outside the tested score band; that retrieval of this note (once ingested) preserves the effect — the real-path trial is still gated on ingestion.

---

## ➜ NEXT ACTION

Ingest through the canonical Receiver; register in the smart-note index so `smart_note_v2.py retrieve --query "reserve rule dispatch"` surfaces it; then run the real-path successor trial (SR-P3 lineage) with retrieval live instead of stubbed.

---

**END — DRAFT SMART NOTE (T11 Reserve Rule)**
