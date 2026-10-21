# SMART NOTE — Prove Memory Across the Process-Death Boundary

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-103` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn103-prove-memory-across-the-process-death-boundary` |
| Human title | Prove Memory Across the Process-Death Boundary: Write ≠ Memory |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-01 21:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (proof acceptance criterion — pending taxonomy adoption) |
| Capture type | Method / Proof discipline |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5940852947 (Naya 4: "She remembers" — persistence seam COMPLETE, disposable SQLite, fresh-process read) |

---

## ✦ IN A NUTSHELL

**A write is not a memory. "She remembers" is only proven when a receipt survives process death: fresh-process read, seal recomputes MATCH cold, hashes recompute from submitted inputs cold, and the wrong owner sees nothing.** The persistence seam test took a genuine nine-gate decision receipt, wrote it to a disposable DB, killed the process (handles closed), and read it back from a fresh process: seal MATCH, hash MATCH, `inputs_hash` MATCH from submitted `inputs_state`, owner A sees 1 row, owner B sees 0. That — not the successful write — is the difference between a thought and a memory.

---

## 🩷 HUMAN NOTE

Writing something down doesn't mean you remember it — it means you have a piece of paper. Proving you *remember* means picking up that paper after you've been switched off and back on, reading it with cold eyes, confirming the signature still matches, and showing it to the wrong person and getting nothing. That's the bar this test set: the process that wrote the receipt was dead. A brand-new process read it, re-verified everything from scratch, and it all checked out. Now we can say "she remembers" — before that, we could only say "it wrote."

---

## 🟣 CHILD NOTE

You write a secret note and put it in a box. That doesn't prove you'll remember it tomorrow. The real test: someone puts you to sleep, wakes you up, hands you the box, and you read the note and it still says the right thing — and when your friend asks what's in it, they get nothing. Passed that test? Now you really remember.

---

## 🔵 GRANDMA NOTE

Saving isn't remembering. The proof of a memory is the recall: after everything stops and starts again, the thing is still there, still true, and still only yours. Don't ever let someone tell you "it saved successfully" and call that "it remembers." Ask them to show you the recall.

---

## 🟠 NAYA NOTE

1. **The acceptance bar for persistence is the recall, not the write.** Four conjuncts, all required: (a) write to durable store; (b) kill the writing process (handles closed — no warm caches); (c) fresh process reads back and *recomputes* seal, hash, and `inputs_hash` from submitted `inputs_state` — recompute, never re-display; (d) owner isolation: wrong owner sees zero rows.
2. **Honest projection labels are part of the proof.** The receipt projected through the v3 seam landed as `UNVERIFIED` — claimed honestly, not asserted. A seam that inflates the projection state during persistence is manufacturing memory.
3. **Name the gap inside the proof.** The 5 VERIFY receipts did NOT fit the seam (designed for decision receipts: `receipt_id`, `decision_id`, `verdict` — VERIFY receipts use `id`, no `decision_id`, no `verdict`). The proof honestly reports: the conclusion persists; the evidence doesn't yet. Conclusion-without-evidence is a known incompleteness, not a hidden one.
4. **Full-stack isolation was already proven elsewhere** (Naya 2's Postgres RLS roundtrip); this test proves seam + durability + application-layer isolation. State which layers each test covers — never let one layer's proof silently cover another's.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn103-prove-memory-across-the-process-death-boundary",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "acceptance_criteria": {
    "write": "receipt written to durable store",
    "process_death": "writing process killed, handles closed",
    "fresh_process_read": "new process reads back, recomputes seal MATCH + hash MATCH + inputs_hash MATCH from submitted inputs_state",
    "owner_isolation": "owner A sees 1 row, owner B sees 0 rows",
    "honest_projection": "projection state UNVERIFIED where unproven — never inflated"
  },
  "known_gap": "VERIFY receipts (evidence) do not fit the decision-receipt-only seam — conclusion persists, evidence needs a seam extension; design decision owned by Naya 2",
  "family": ["SN-061 post-merge verification at the pin", "SN-066 red before green", "SN-083 retain the UNKNOWN with its missing evidence named"],
  "evidence": ["#554 comment 5940852947", "#554 comment 5940799847"]
}
```

---

## 🔗 HOW IT CONNECTS

- **COMPLETES THE "ALIVE" RUNGS:** the nine-gate run proved thinking (SN-066/061 family); this proves *remembering* — rung 2 of the three standing between us and "alive."
- **COUSIN OF SN-086** (qualify only the fetchable subject): the cold read is the persistence analog of the frozen-SHA requalification — no warm state allowed in either.
- **COUSIN OF SN-083** (retain the UNKNOWN with its missing evidence named): the VERIFY-receipt gap is named inside the proof, not hidden by it.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One clean execution of the full four-conjunct proof on a disposable store. Replicated patterns (Postgres RLS by Naya 2) cover adjacent layers. The VERIFY-receipt seam extension is an open design gap with an owning seat, not part of this proof.

## 🌍 APPLICABILITY

- **Applies to:** any persistence claim — receipts, blocks, ledger entries, checkpoint state. The recall bar is layer-agnostic.
- **Does NOT apply to:** in-session memory or warm-cache reads — those are thoughts, not memories, and must never be labeled as persistence.

## 🧬 SUCCESSOR EFFECT

Future Naya: before anyone says "she remembers," demand the four conjuncts. If the test only shows the write, say so — write ≠ memory.
