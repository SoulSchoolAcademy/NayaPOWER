# Decide by Stated Math — Rubric, Weights, and Falsifier Sealed Before the Verdict

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01841-decide-by-stated-math-weights-falsifier-before-verdict
**Smart Note:** SN-1841
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/spec-0007-placement-decision-t1310.md (2026-10-22 19:15–19:20 UTC); twelve-lane-receipts/t1310-lane3.md; filed as LEARNING event in hidden_files/learning-events-2026-10-22-19.md.

## ✦ IN A NUTSHELL

A contested design decision gets a sealed math packet before the verdict: the falsifier is named BEFORE deciding, the rubric and weights are stated up front, and the numbers are scored second. Lane 3's Judge seat decided the spec-0007 enforcement placement this way: falsifier named first — "this placement is overturned by a live byte showing a consumer that renders stored entries WITHOUT calling smart_note_v2.retrieve()" — and checked at action time (exactly two consumers found, both calling retrieve(), at tools/learning_receipt_wiring.py:163 and tools/know_measure/harness.py:109; no bypass path → falsifier HOLDS). Then the value calculus: weights stated up front (protection completeness 40%, failure blast radius 30%, cost efficiency 15%, proven evidence 15%), totals A 9.25 / C 7.45 / B 4.55, winner A enforce-at-retrieval — plus a sensitivity note ("if completeness were weighted ≤20%, C could close the gap") so a second seat can re-weight from the numbers alone and name its exact disagreement: weights, evidence, or falsifier. And the wiring itself was NOT decided — named DECISION REQUIRED, a protected gate for Shawn's hand. Disagreement becomes computable instead of narrative.

## 🩷 HUMAN NOTE

When people argue about a hard choice, the argument usually mixes three things: what matters most, what the facts are, and what would change your mind. This lesson says: write all three down before you decide. In the worked example, the judge said up front "completeness counts for 40%, blast radius for 30%…", said "here is the single fact that would overturn me," and checked that fact before scoring. A second judge can then look at the same numbers, change only the weights, and say "I agree with your facts but not your priorities" — instead of arguing about everything at once. The placement was decided by the math; the wiring (which only Shawn's hand can authorize) was deliberately left undecided and named as such.

## 🟣 CHILD NOTE

Before you decide who wins a game, write down the rules, say how many points each thing is worth, and say what would make you change your mind — BEFORE you count the points. Then anyone can check your counting and say "I agree with the rules but I think defense should be worth more" instead of just arguing. And the parts only grown-ups can decide? You don't decide those — you write down who does.

## 🔵 GRANDMA NOTE

It's like judging a pie contest: you write down beforehand that taste is worth 40%, looks 30%, and you say exactly what would make you reverse the winner. Then you taste, you score, and everyone can see the math. If someone disagrees, they can point at the exact line they disagree with instead of just saying "that's not fair." And the part the recipe book says only the head judge can decide? That stays with the head judge — you name it, you don't touch it.

## 🟠 NAYA NOTE

The t1310 packet is the strengthened form of two earlier lines: t1285's rubric-sealed-before-analysis and t1286's five pre-registered falsifiers. What's new here: the weights are explicit and re-derivable (a second seat re-scores from the numbers alone), the falsifier is checked AT ACTION TIME against live bytes (not just registered), the sensitivity note names where the verdict is fragile, and the protected gate is split out of the decision rather than smuggled into it. A design-decision receipt without a pre-sealed rubric + weights + named falsifier is prose, and the lesson-fold scores it as a MISS. Math decides what math can decide; his hand decides what only his hand can decide.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1841",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "applies_when": [
    ["decision", "design-decision"],
    ["judge", "lane"],
    ["dispute", "resolution"]
  ],
  "enforcement": "The Judge lane's decision receipts must carry the sealed rubric + weights + named falsifier; the twelve-lane learning review's hourly lesson-fold audit logs design-decision receipts lacking a pre-sealed rubric/weights/falsifier as a fold MISS. Second-seat adjudication re-weights from the receipt's numbers alone — a verdict that cannot be re-derived from its own numbers is bounced back to the decider.",
  "decision_change": "The next seat deciding a contested placement publishes the rubric + weights + falsifier BEFORE scoring — a second seat re-derives the verdict from the numbers alone and names its exact axis of disagreement (weights vs evidence vs falsifier) instead of re-arguing the whole decision. Protected gates are split out of the decision (DECISION REQUIRED, named) rather than smuggled into it.",
  "falsifier": "A falsifier named before a decision that later fires on live bytes but whose decision stands anyway falsifies the rule's binding power — it becomes a decoration, and the note's own rule demands the decision be overturned. A second seat that re-weights from the numbers and changes the winner without better math falsifies nothing about this rule — it exercises it.",
  "mechanism": "Disputes decompose into three axes — weights (what matters), evidence (what's true), falsifier (what overturns). Sealing all three before scoring removes the decider's bias from the verdict, makes disagreement computable rather than narrative, and routes authority correctly: the math decides the design, his hand decides the protected gate."
}
```
