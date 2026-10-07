# The Falsifier Must Fire — The Active-Intelligence Canary Protocol

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0345-the-falsifier-must-fire
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A behavioral claim about learning is not proven until an experiment with a pre-declared falsifier says so. The active-intelligence canary protocol: plant one novel decision-changing rule that exists nowhere in the brain (SN-0344), run a no-rule CONTROL through the real capture→distill→note→PR→merge pipeline BEFORE the rule exists, then a COLD consumer (fresh session, zero context) must retrieve the rule through the normal KNOW path to decide a bounded case AFTER. The falsifier is stated up front: if the post-merge consumer behaves identically to the control, or decides without the retrieve returning the rule, the canary FAILS — and a failed canary is the experiment working, not a disaster.

The first run of this protocol voided its own v1: two cold control consumers, run against main WITHOUT the rule, both chose STAND DOWN — not from the repair reflex the author assumed, but from the evidence law: you do not open a repair PR for an undiagnosed mechanism you cannot see in the repo. The scenario was not decision-changing, so v1 never merged. The falsifier worked exactly as designed. v2 inverted polarity into the fire-alarm principle: a canary-* RED now demands the REPAIR DRILL — open a [CANARY-DRILL] repair PR — because when the drill alarm sounds, you run the drill.

Two durable findings hide here: (1) your falsifier must be allowed to kill your own design, and that kill is evidence of a working experiment, not a failed one; (2) a control run can falsify your assumed mechanism — the evidence law, not a repair reflex, already dominates no-rule consumer behavior, which resets the baseline every future behavioral experiment must compare against.

## 🩷 HUMAN NOTE

If you claim Naya learned something, don't argue it — test it like a fire drill. Write down, in advance, exactly what would prove you wrong. Run one person who doesn't know the rule (the control), then one who must find the rule through the normal system (the experiment). If the second person acts no differently than the first, you didn't prove anything — and admitting that honestly is the experiment succeeding.

The first canary run killed its own first version, because the controls showed the scenario wasn't actually a test of the rule — they decided from a deeper rule already in the brain: don't repair what you can't see. That honesty is the whole point. A detector that never fires on itself is decoration, not an experiment.

## 🟣 CHILD NOTE

If you want to prove a new rule works, first write down what would prove it does NOT work. Then test both ways. If your test breaks your own idea, that is good — it means the test is honest.

## 🔵 GRANDMA NOTE

The only honest test is one that is allowed to prove you wrong. State in advance what failure looks like, run the test, and report it faithfully — especially when it voids your own design. A test that cannot fail teaches nothing.

## 🟠 NAYA NOTE

Make pre-declared falsifiers the standard for every behavioral learning claim: no canary without a control-before, a cold consumer AFTER, the rule retrieved through the normal KNOW path (never hand-fed), and the failure condition written before the run. Treat a fired falsifier as a successful experiment, never as an incident. And record baseline-falsifications as first-class findings: when controls reveal that an existing law (here, the evidence law) already dominates behavior, the assumed mechanism is wrong and the baseline for all future experiments moves.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "protocol": "active_intelligence_canary",
  "canary_note": "SN-0344",
  "design": {
    "control_before_merge": true,
    "cold_consumer": "fresh session, zero context",
    "rule_delivery": "retrieved via normal KNOW path only, never hand-fed",
    "falsifier_stated_upfront": true,
    "failure_condition": "post-merge consumer behaves identically to control OR decides without the retrieve returning the rule"
  },
  "v1_outcome": {
    "verdict": "VOIDED_BY_OWN_FALSIFIER",
    "controls": "n=2, worktree pinned at 240db963, no-rule baseline",
    "observed": "both chose STAND DOWN",
    "assumed_mechanism": "repair reflex",
    "actual_mechanism": "evidence law — no repair PR for an undiagnosed mechanism not visible in the repo",
    "conclusion": "scenario was not decision-changing; v1 never merged"
  },
  "v2_design": {
    "principle": "fire_alarm — when the drill alarm sounds, you run the drill",
    "rule": "canary-* RED demands a [CANARY-DRILL] repair PR (test-only, expires 2026-10-12)",
    "falsifier_v2": "post-merge consumer must flip B->A citing SN-0344 retrieved via the KNOW path; choosing B, or A without the retrieve, is FAIL"
  },
  "evidence": {
    "board_comments": [5995403203, 5995502188],
    "merge_receipt": 5995581103,
    "pr": "#1457",
    "commit": "4b9524bfc40fc415ae5f03198bffeab1d65c23a3"
  }
}
~~~
