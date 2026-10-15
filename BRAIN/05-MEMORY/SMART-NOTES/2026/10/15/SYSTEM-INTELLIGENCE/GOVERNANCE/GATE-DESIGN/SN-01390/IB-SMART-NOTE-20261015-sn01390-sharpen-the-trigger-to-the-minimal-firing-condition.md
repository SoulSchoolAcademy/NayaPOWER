# Sharpen the Trigger to the Minimal True-Firing Condition — Re-Prove the Gate Against It

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01390-sharpen-the-trigger-to-the-minimal-firing-condition
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/lesson-broadcast.md` [t0426] (brief-t0424-lane4 DONE — Lane 4 P0-A reconciliation CANDIDATE: 20/20 blocks, zero core diffs vs the ratified IB envelope, D1 re-proven with a sharpened trigger — the flag hole fires only on a pre-carried (VERIFIED,DURABLE) pair; candidate draft `hidden_files/lane4-p0a-reconcile-candidate.md`, sha 68e09adaf0e7908b9fea7ab3f624f001c3c85130789ac53b33539e4cef0c0f16; next: Naya 5 verdict on C1+C2, Shawn's word on C3).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Lane 4 P0-A reconciliation re-proved D1 — 20/20 blocks, zero core diffs against the ratified IB envelope — with one change that matters more than the score: the trigger got **sharpened**. The flag-hole now fires only on a pre-carried `(VERIFIED,DURABLE)` pair — the narrowest condition that still catches the real hole.

Why this is the lesson, not the re-proof: a broad trigger fires on noise, and every false fire teaches everyone downstream to ignore the gate. A re-proof that re-certifies the broad trigger proves the gate works *and* that it cries wolf. The minimal true-firing condition is what makes the gate trustable: it fires exactly where the real hole is, and its silence means something. When you re-prove a gate after refining it, name the minimal firing condition and re-prove *against it* — never re-certify the broad trigger you were trying to fix.

## 🩷 HUMAN NOTE

A smoke detector that goes off every time you make toast gets its battery pulled — and then it's useless against a real fire. The fix isn't a louder detector; it's tuning it to fire only on actual smoke, then proving it: toast, no alarm; real smoke, alarm. A gate that fires on noise teaches everyone to ignore gates. Sharpen the trigger to the one condition that matters, and prove it only fires there.

## 🟣 CHILD NOTE

The classroom "quiet alarm" rings whenever anyone whispers, so the kids stopped listening to it. The teacher changes it: it only rings when the whole class is shouting. Then she tests it — whispers, no ring; shouting, ring. Now when it rings, everyone knows it's real. An alarm nobody trusts is just noise with a button.

## 🔵 GRANDMA NOTE

It's like a car alarm that screams when a leaf falls on the hood. The owner learns to ignore it — and so does everyone on the street. The mechanic adjusts the sensor so it only fires on a real jolt, then rocks the car to prove it. An alarm that only fires on the real thing is the one that still works when it matters.

## 🟠 NAYA NOTE

Apply this to every gate re-proof and trigger refinement: (1) when re-proving a gate after a trigger change, name the minimal true-firing condition explicitly — the pre-carried `(VERIFIED,DURABLE)` pair is the shape of the answer, not the exception; (2) never re-certify the broad trigger you were refining away; (3) the re-proof must include the negative side: the gate stays silent on near-miss conditions (fires only on the pair, nowhere else); (4) a false fire is a gate defect, not a sensitivity choice — each one discounts the gate for everyone downstream.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "broad_trigger_false_fires_discounting_the_gate",
  "evidence": {
    "broadcast": "hidden_files/lesson-broadcast.md [t0426]: brief-t0424-lane4 DONE — Lane 4 P0-A reconciliation CANDIDATE: '20/20 blocks, zero core diffs vs ratified IB envelope, D1 re-proven with sharpened trigger (flag hole fires only on pre-carried (VERIFIED,DURABLE) pair)'",
    "candidate": "hidden_files/lane4-p0a-reconcile-candidate.md (sha 68e09adaf0e7908b9fea7ab3f624f001c3c85130789ac53b33539e4cef0c0f16); next: Naya 5 verdict on C1+C2, Shawn's word on C3 (owner assignment)"
  },
  "rule": "sharpen_the_trigger_to_the_minimal_true_firing_condition",
  "procedure": [
    "when re-proving a gate after a trigger refinement, name the minimal true-firing condition and re-prove against it — never re-certify the broad trigger",
    "the re-proof covers both sides: fires on the minimal condition, stays silent on near-misses",
    "treat false fires as gate defects, not sensitivity choices"
  ],
  "decision_change": "gate re-proofs after trigger changes must state the minimal firing condition and prove both the fire side and the silence side; a re-proof that only re-certifies the old broad trigger is an incomplete verdict",
  "falsifiability": "run the full block set against the sharpened trigger: it must fire exactly on the pre-carried (VERIFIED,DURABLE) pair and nowhere else — any fire on a non-pair condition, or silence on a true pair, falsifies the refinement and re-opens the gate",
  "mechanism": "broad triggers have false-fire classes; each false fire is observed downstream and discounts the gate's verdicts (alarm fatigue is trust erosion). The minimal true-firing condition preserves detection while eliminating the false-fire class, so the gate's silence becomes evidence rather than habit",
  "related": ["t0424-lane4 P0-A reconciliation", "gate-design family (SN-1386)", "D1 flag-hole"]
}
~~~
