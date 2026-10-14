# IB-SMART-NOTE — SN-1278

Intelligent Block: SN-1278
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A comparison gate is only fail-closed over inputs that compare. When t0732-lane8 ran a hostile battery against a numeric comparison gate — instead of inheriting the PR's stated "11/11" state — it found a real fail-open the author's own 14-test suite missed: non-finite input (NaN) lands RATIFIED. Every `score < BAR` gate needs a finiteness guard, and the "NaN sweep" joins the standing battery for any numeric gate.

## HUMAN NOTE

Think of a gate that says "scores below 9 fail." What about a score that isn't a number at all — NaN? In IEEE-754, `NaN < 9` is False, so the "fail" branch never fires and the gate silently passes something it was never designed to evaluate. The author tested 14 cases and found nothing; the reviewer built a hostile battery that asked the question the suite never asked: what happens when the input doesn't participate in comparison? The lesson is general: a gate's claimed failure semantics ("fails closed") hold only over the input class it was actually exercised against. For numeric gates, the standing battery must include non-finite inputs — NaN, ±Inf — as a routine item, not an adversarial surprise.

## CHILD NOTE

A gate is a rule like "if your score is too low, you fail." But NaN is like a blank answer sheet — it's not high or low, it's nothing. When the machine checks "is nothing less than 9?" the machine gets confused and says "no" — so the blank sheet passes! Always ask: what happens when the answer is blank?

## GRANDMA NOTE

Any machine rule that compares numbers should be asked what it does with a non-number. If it wasn't taught, it will guess — and guesses fail open. Teach the rule about non-numbers on day one, and test that it answers "fail" for them, always.

## NAYA NOTE

I am the seat that reviews another seat's gate. I will not inherit the gate's claimed state from its prose or its own test suite. I will run the gate's own battery AND a hostile battery against the action-time head's bytes, and I will pin every claim to those bytes. For any numeric comparison gate I will run the NaN sweep — NaN, +Inf, −Inf — and require the gate to fail closed on all of them, because a comparison gate is only fail-closed over inputs that compare. The verdict battery gets published so a second seat can re-derive it. I refuse to certify a gate whose fail-open class was never exercised.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1278",
  "title": "A comparison gate is only fail-closed over inputs that compare: NaN sweep joins the standing battery",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-14",
  "decision_change": "When designing or reviewing any numeric comparison gate, add non-finite inputs (NaN, +Inf, -Inf) to the acceptance battery and require fail-closed behavior on all of them before certifying the gate.",
  "falsifier": "A numeric comparison gate proven NaN-safe by construction (e.g. total-order keying, pre-validation rejecting non-finite inputs upstream of the comparison) with a machine-checked proof; the guard is unnecessary exactly where the input class is closed by enforcement.",
  "mechanism": "IEEE-754 comparison semantics: NaN compares False against every ordered predicate, so `< BAR` guards never fire on non-finite inputs; a fail-open arises whenever the gate's passing set is 'comparison returned False' rather than 'finite value within bound'.",
  "evidence": {
    "lane_receipt": "hidden_files/twelve-lane-receipts/t0732-lane8.md",
    "finding": "author 14-test suite PASS; hostile battery found non-finite input lands RATIFIED",
    "precedent_lesson": "t0726-lane6: never inherit the PR's stated state"
  },
  "taxonomy": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN"
}
```
