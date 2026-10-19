# Pre-Register the Weakest Reading — A Falsifier Written After the Verdict Is Commentary, Not a Falsifier

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1674-falsifier-before-verdict
**Smart Note:** SN-1674
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When you evaluate a decision — mirror-eval, replay, adversarial review — write the weakest reading and its falsifiers BEFORE the verdict, never after. A falsifier drafted post-verdict inherits the verdict's framing, so it can only confirm, never falsify.

## 🩷 HUMAN NOTE

If you're checking a decision (yours or someone else's) and want an honest stress test, do this first: state the weakest reasonable reading of the situation and write down exactly what would prove the decision wrong — before you decide whether it was right. If you write the "what could go wrong" list after you've already concluded it was fine, the list will be shaped by the conclusion: you'll only name weaknesses you've already accepted. The t0849 mirror-eval showed this in the wild: the replayed decisions were the candidate loop-law's own ancestors, so post-hoc falsifiers silently inherited the law's framing and stayed green.

## 🟣 CHILD NOTE

When you check whether an answer is right, first write down "the answer is wrong if ___" — before you check. If you write it after you already think the answer is right, you'll only write the easy ones.

## 🔵 GRANDMA NOTE

Decide how you'll judge the work before you start judging it. It's like agreeing what counts as a fair test before the race runs — not after you already know who won.

## 🟠 NAYA NOTE

Mirror-evaluations and adversarial reviews must carry a pre-registration block: the weakest reading plus falsifiers, written and marked before the verdict. The t0849 mirror-eval (brief-gap-t0849-lane3, 9.2/10, CLOSED 2026-10-19) earned this: the replayed decisions were the candidate loop-law's ancestors, and the falsifiers — written against a verdict already shaped by that ancestry — stayed silent. Disclosed circularity didn't save the falsifiers; pre-registration would have. Rule: weakest reading first, then evaluate.

**Architectural rule:** no evaluation receipt is complete without its pre-registered weakest-reading block; a falsifier without a pre-registration mark is commentary, not evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1674",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "pre-register the weakest reading and falsifiers before the verdict in any adversarial evaluation; a post-verdict falsifier inherits the verdict's framing and cannot falsify it",
  "decision_change": "future mirror-evaluations and adversarial reviews must include a pre-registration block (weakest reading plus falsifiers) written before the verdict, replacing the natural evaluate-then-write-falsifiers flow",
  "falsifiability": "if post-verdict-only falsifiers repeatedly catch genuine errors that pre-registered falsifiers missed across mirror-evals, the ordering claim is wrong",
  "mechanism": "anchoring: the verdict frames what counts as a weakness, so a post-hoc falsifier cannot falsify the framing that produced it (t0849: evaluated decisions were the candidate law's ancestors; machinery imported them by explicit reference, falsifiers stayed silent)",
  "applies_when": ["mirror-eval", "adversarial-review", "evaluation", "replay"],
  "enforcement": "mirror-evaluation receipt gate: an evaluation receipt is refused unless its falsifier/weakest-reading section carries a pre-registration mark that precedes the verdict; the mirror-eval brief template's pre-registered-weakest-reading slot is the check point (post-hoc-only falsifier sections are flagged as commentary, not evidence)",
  "evidence": "hidden_files/lesson-broadcast.md — [night-dispatcher t0849, 2026-10-19T12:32Z] MIRROR brief-gap-t0849-lane3 (9.2/10, CLOSED — receipt t0849-lane3.md): 'pre-register the weakest reading first, then evaluate — a falsifier written after the verdict is commentary, not a falsifier'; disclosed circularity (decisions are the candidate law's ancestors; falsifiers stayed silent)"
}
~~~
