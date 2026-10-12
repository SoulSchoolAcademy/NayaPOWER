# THREE-TRY CIRCUIT BREAKER

**Standing law L236 — Shawn, 2026-10-12**

> Three rounds is the budget for one hypothesis. After that, you don't try harder — you think different.

## The problem it solves

AI has a failure mode: it hits the same wall a thousand times, each attempt slightly different, none of them working. Every attempt *looks* like progress because something changed. But it's the same wall. The intelligence isn't in the trying — it's in noticing you're trying the same thing.

Shawn's rule: **no more than three hits on one wall.** One try might be bad luck. Two tries might be a stubborn problem. Three tries and you're not solving — you're looping.

## The rule

```
THREE-TRY CIRCUIT BREAKER (Shawn, 2026-10-12 — STANDING)

Three rounds. That's the budget for one hypothesis.

- Rounds 1–3: BUILD → SCORE → FIX, the normal Builder-Scorer Loop.
- After round 3, if still below 9.0: STOP. No fourth round on the same hypothesis.
- Before any further work, the builder writes a HYPOTHESIS CHANGE note:
  1. What I tried (the hypothesis)
  2. Why it didn't reach 9.0 (the evidence)
  3. What I'm trying instead (the new hypothesis)
  4. Why it's different at the ROOT level (a reframe, not a variation)
- The scorer verifies the new hypothesis is actually different —
  not the same wall with new paint.
- If no genuine reframe is possible: STOP. Hand it to another lane
  or close it honestly. An unsolved problem with an honest
  "I don't know yet" beats ten more rounds of the same wall.

Repetition without reflection isn't persistence — it's a loop.
```

## How it fits the Builder-Scorer Loop

The loop's three rounds (build → score → fix → score → fix → final score) are the mechanism. The circuit breaker is the teeth:

| Round | What happens |
|-------|--------------|
| 1 | Build, score, fix — first hypothesis |
| 2 | Score again, fix again — same hypothesis, refined |
| 3 | Final score — last chance for this hypothesis |
| After 3, score ≥ 9.0 | Ships. Normal path. |
| After 3, score < 9.0 | **BREAKER TRIPS.** No round 4 on this hypothesis. |
| Breaker tripped | Builder writes HYPOTHESIS CHANGE note (4 parts). |
| Reframe verified | Scorer confirms it's genuinely different. New 3-round budget opens. |
| No reframe possible | Stop. Hand off to another lane, or close with honest "I don't know yet." |

## What counts as a reframe (and what doesn't)

**Not a reframe:**
- Trying the same fix with different parameters
- Rewording the same approach
- Adding more tests to the same design
- "Trying harder" at the same thing

**A reframe:**
- Changing the level of abstraction (fix the generator, not the output)
- Questioning the assumption the approach rests on
- Solving at the root cause instead of the symptom
- A different seat's genuinely different approach

The test: if you removed the labels, would a stranger recognize these as two different ideas? If not, it's the same wall.

## Why three

- **One** try might be bad luck, a typo, a flaky test.
- **Two** tries might be a genuinely stubborn problem that needs one more angle.
- **Three** tries with honest scoring is enough evidence: the hypothesis is wrong, or the problem is bigger than the hypothesis.

Three is also the Builder-Scorer Loop's natural shape. The breaker doesn't add rounds — it adds a *door* after the rounds that already exist.

## The deeper principle

"Flow like water" means the next step is always obvious. An agent stuck in a loop has lost the next step — it's repeating the last one. The circuit breaker restores flow by forcing the question the loop was avoiding:

> *Am I solving the problem, or am I solving my attempt at the problem?*

Solve at the root, or let the water find another path.

---

*Canonical: AGENTS.md L236. Briefing: AGENT-BRIEFING.md (Builder-Scorer Loop section).*
*Schema: naya.three-try-circuit-breaker.v1 (this document is the v1 spec).*
