# The Assumption Killer Test — Make the Unfair Scheduler Look Fair

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1685-the-assumption-killer-test-make-the-unfair-scheduler-look-fair
**Smart Note:** SN-1685
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

An assumption audit is only honest if it can fail. The killer test: take a deliberately unfair scheduler and try to make it look fair by strengthening assumptions. If it works, reject the qualification — the assumptions were the rigged thing, not the scheduler. Passing three audit gates never compensates for failing the fourth.

## 🩷 HUMAN NOTE

A student passes a test because the questions were easy, not because she learned. The killer test rewrites the test with a known cheater — if the cheater aces it, your test is broken, not your student.

## 🟣 CHILD NOTE

You say your rule is fair. I bring the naughtiest kid in school — if your rule says HE was fair, your rule is the problem, not the kid.

## 🔵 GRANDMA NOTE

Dear, assumptions are like fences — they decide what you refuse to look at. A fence that hides a real problem isn't protecting you, it's blinding you. So bring in a known troublemaker: if your fence says he's an angel, your fence is the liar.

## 🟠 NAYA NOTE

The concrete instance (2026-10-10, Directive D28 registered, #1354 comment 6101230756): the Independent Fairness Assumption Audit Protocol — four gates, all required: independent justification, satisfiability, minimal sufficiency, non-circularity. An assumption may not delete a scheduler failure from the model unless it is independently proven that the excluded behavior is genuinely outside the qualified environment. The case that makes it real: assume "the task eventually stays continuously eligible" and the intermittent-starvation trace vanishes — not because the scheduler was fixed, but because the test was rigged. Remove the assumption, the counterexample comes back, and now you fix the scheduler instead of the model.
The asymmetry this kills: assumption-strengthening is invisible failure-deletion. A qualification with stronger assumptions looks more rigorous while actually testing less. The killer test makes the deletion visible by aiming it at a known-bad subject — nothing honest can make the deliberately unfair scheduler look fair, so if the audit says it is fair, the audit is the rigged thing.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1685",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "the killer test for an assumption audit: if you can make a deliberately unfair scheduler look fair by strengthening assumptions, reject the qualification — assumptions restrict the model, not the world, and a strengthened assumption can delete a real failure without fixing anything; passing three gates never compensates for failing the fourth",
  "decision_change": "a seat qualifying a fairness claim will run the deliberately-unfair-scheduler test against its assumption set before accepting the qualification; if the bad scheduler qualifies, the assumptions (not the scheduler) are declared the defect — instead of trusting the four gates on paper",
  "falsifiability": "if an assumption set that the killer test REJECTS is later independently proven to reflect the true environment, the test is too strict and the note's fourth-gate absolutism is wrong; if a genuinely unfair scheduler passes a qualified claim whose assumptions passed the audit, the audit is the defect",
  "mechanism": "assumptions restrict the model, not the world: a strong enough assumption deletes a failure trace from the model without changing the scheduler. A known-bad scheduler is the adversarial probe — it cannot hide from an honest audit, so if it does, the audit itself was the rigged component. The probe turns invisible failure-deletion into a visible verdict",
  "applies_when": [
    [
      "fairness",
      "qualification"
    ],
    [
      "assumption",
      "audit"
    ],
    [
      "verification",
      "adversarial"
    ]
  ],
  "enforcement": "Directive D28's four gates (independent justification, satisfiability, minimal sufficiency, non-circularity) are the required qualification protocol; any fairness qualification without the deliberately-unfair-scheduler killer test is INCOMPLETE and the qualification gate refuses it. The unfair-scheduler experiment is the standing negative control.",
  "evidence": "Directive D28 registered 2026-10-10 (#1354 comment 6101230756): Independent Fairness Assumption Audit Protocol — four gates, all required; \"the killer test: if you can make a deliberately unfair scheduler look fair just by strengthening assumptions, the audit rejects the qualification.\" Real case: \"the task eventually stays continuously eligible\" masks intermittent starvation until removed."
}
~~~
