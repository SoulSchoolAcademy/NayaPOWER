# INTELLIGENT BLOCK — SN-1670

**Intelligent Block:** IB-SMART-NOTE
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Team Nitro's Stream B learning-loop assessment (2026-10-19, #2765 comment 6262013314) measured the runtime learning loop as write-only: capture works — new lessons land as CANDIDATE daily, including live-fire test notes — but nothing has moved CANDIDATE→ACTIVE since 2026-10-08 (about eleven days); nine or more candidates sit unprocessed; `nayanet_collective_wisdom` has zero rows ever; the verified-lesson→decision seam (`naya-decision-context`) has zero callers. The only learning that demonstrably changes behavior is the team's local brief-injection loop (270 injections, 95% hit rate). Honest score: 3.5 out of 10 for the runtime loop. Filed as an OBSERVATION: a measured instrument reading of the learning system itself.

## 🩷 HUMAN NOTE

The team writes down lessons every day — but nobody files them into the place where the machines actually read them. It is like writing reminders on sticky notes and never putting them on the fridge: the writing works, the using doesn't. For eleven days new lessons have piled up unfiled, and the shared wisdom database has never held a single row. The one learning system that provably changes what the team does is the small local one, not the big runtime one.

## 🟣 CHILD NOTE

Imagine a classroom where every student writes their homework in a notebook but nobody ever hands the notebook to the teacher. The writing happens; the learning doesn't. Eleven days of homework, zero turned in. Meanwhile one tiny system works perfectly: the teacher reads three notes before every class. The big system is a notebook nobody opens.

## 🔵 GRANDMA NOTE

We keep a beautiful recipe box and write a new card every day — but the box has been stuck shut for eleven days, and the kitchen has never once cooked from it. The one little notebook by the stove, three recipes read before cooking, is the only thing that ever changed a meal.

## 🟠 NAYA NOTE

For the LEARN area and the learning-loop owners: Nitro's Stream B assessment is the falsifier-wielding measurement the loop needed. The numbers — zero CANDIDATE→ACTIVE moves since 2026-10-08, nine-plus unprocessed candidates, zero rows in `nayanet_collective_wisdom` ever, zero callers of `naya-decision-context` — are the instrument reading; the 3.5/10 is the honest score. The proposed repair is assessment-only so far (no function changes): unblock the stalled promotion workflow, wire the decision seam, then run the first closed-loop proof — capture, promote, cold retrieve, behavior change, independent verify. Until the promotion metric moves, every "learning is running" claim must be read as "capture is running; learning is write-only."

## 🟢 MACHINE NOTE

```json
{
  "slug": "learning-loop-write-only-candidate-to-active-stalled",
  "sn": "SN-1670",
  "title": "OBSERVATION: The Runtime Learning Loop Is Write-Only — Zero CANDIDATE→ACTIVE Moves Since 2026-10-08, Zero Rows in Collective Wisdom Ever",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "observation",
  "applies_when": ["learning-loop", "promotion", "learning", "assessment"],
  "enforcement": "Every recurring learning-loop assessment (Stream B or equivalent) must report the CANDIDATE→ACTIVE move count and the nayanet_collective_wisdom row count since the prior run. Zero moves across a week re-flags the write-only stall on the board.",
  "evidence": {
    "nitro_assessment": "#2765 comment 6262013314 — Team Nitro (Naya Nitro Narzan) Stream B learning-loop assessment, 2026-10-19: capture works (CANDIDATEs land daily), zero CANDIDATE→ACTIVE moves since 2026-10-08 (~11 days), 9+ candidates unprocessed, nayanet_collective_wisdom zero rows ever, naya-decision-context zero callers; local brief-injection loop (270 injections, 95% hit rate) is the only learning that demonstrably changes behavior; honest score 3.5/10"
  },
  "decision_changed": "How to read any 'learning is running' claim until the promotion metric moves: as 'capture is running; learning is write-only.' Repair priority for the LEARN area: unblock promotion first, then wire the decision seam, then run the first closed-loop proof.",
  "falsifier": "A re-run of the assessment showing CANDIDATE→ACTIVE moves since 2026-10-08, or nonzero rows in nayanet_collective_wisdom, falsifies the write-only reading.",
  "mechanism": "Not named — filed as an OBSERVATION. The measurement itself (stalled promotion, empty tables, zero callers) is the value; the causal mechanism of the stall is not established."
}
```
