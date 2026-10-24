Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a verification check you backgrounded finishes after you've signed out, don't let the result die with the shift — land it as a named, dated LATE-ARRIVAL CORRECTION on the record. Sign-out ends the shift, not the evidence: the verification loop covers work that outruns the clock. t1467-lane12 proved the pattern at 2026-10-24 ~00:35 UTC — a registry grep that completed after sign-out landed a real correction (SB-N2 amendment + crash-guard) instead of being silently dropped.

## 🩷 HUMAN NOTE

Shawn — quick one: a lane started a check, signed out for the night, and the check finished after. The old pattern would have been to shrug and lose the answer. The new pattern: the result lands on the record as a named, dated correction — and in this case it was worth landing, because it reframed a whole section of the artifact as an amendment to an existing block instead of a new one, and it added a crash-guard. The shift ends; the evidence doesn't have to. The rule is now wired into receipts: sign-out names anything still running, and late results land instead of dying.

## 🟣 CHILD NOTE

Imagine you send a friend to check whether the ice cream shop is open, and they text you back after you've gone to bed. You could ignore the text — or you could leave a note on the fridge: "Update at 9pm: the shop was OPEN." That's the late-arrival correction. The answer still matters even though the day ended. You just date it, name it, and stick it where the record lives.

## 🔵 GRANDMA NOTE

You asked the neighbor to watch for the delivery truck, then you went inside. The truck came an hour later — and instead of letting the news vanish, the neighbor taped a note to your door: "Truck came at 3. Signed for the package." Dated, named, on the record. That's the whole lesson: a check that finishes after sign-out still lands — as a correction, dated and named — never dropped in silence, because the silence is where the value goes to die.

## 🟠 NAYA NOTE

The failure mode this kills: verification results that complete post-sign-out being silently dropped because the shift "ended." t1467-lane12 proved the pattern at 2026-10-24 ~00:35 UTC: a backgrounded registry grep completed AFTER sign-out and landed a LATE-ARRIVAL CORRECTION — reframing the artifact §2 as an AMENDMENT to the existing SB-N2 (near-miss lane-token resolution + crash-guard for row 148 "lane abc") rather than a new block, while pass 3 had already caught two narration-wearing-precision overclaims ("third re-derivation" ordinal, SB-N2 name scope). Mechanism: the record accepts dated amendments, so a check's information value does not expire at sign-out; naming + dating preserves chronology and distinguishes the correction from a new finding. The future decision this changes: when a seat designs a verification loop with backgrounded checks, it includes a post-sign-out landing path (sign-out inventory of still-running checks + named late-arrival corrections) instead of treating sign-out as the loop's end. It would be proved wrong if late corrections were shown to corrupt the record (duplicate/conflicting entries nobody reads) or if late results systematically arrived after they were actionable — the claim stands or falls on whether the correction improves the record. Cousins: the Oath (measure before you claim) — this is its shift-boundary sibling; CANDIDATE 889 (reconcile at the persistence boundary) — this is its time-boundary sibling.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1909-late-arrival-correction",
  "lesson": "A verification check that completes AFTER the seat's sign-out must land its result as a named, dated LATE-ARRIVAL CORRECTION on the record — never be silently dropped because the shift ended. Proven at 2026-10-24 ~00:35 UTC: t1467-lane12's backgrounded registry grep completed post-sign-out and landed a real correction (SB-N2 amendment: near-miss lane-token resolution + crash-guard for row 148 'lane abc'), reframing artifact §2 from new-block to amendment.",
  "applies_when": ["verification", "sign-out", "receipt", "background-check", "shift-boundary", "evidence-preservation", "failure:dropped-result", "correction-pattern"],
  "enforcement": "Shift sign-out receipts must include an inventory of still-running background checks. The receipt reviewer (different seat or the lane's verification step) rejects any receipt where a backgrounded check neither (a) landed a result nor (b) was named as pending in the sign-out inventory. Late results land ONLY as named, dated corrections (dated AFTER the sign-out they missed) — never as silent record edits.",
  "evidence": [
    "twelve-lane-receipts/t1467-lane12.md — 'LATE-ARRIVAL CORRECTION (2026-10-24 ~00:35 UTC)': backgrounded registry grep completed after sign-out, landed SB-N2 amendment (near-miss lane-token resolution + crash-guard for row 148 'lane abc'); pass 3 had caught two narration-wearing-precision overclaims the same receipt",
    "learning-events-2026-10-24-01.md — INTELLIGENT event 'Late-arrival verification landing': 'late-arriving check results land as corrections, named and dated, rather than being silently dropped. The loop now covers work that outruns the clock.'"
  ]
}
```
