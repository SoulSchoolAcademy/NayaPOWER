# Pre-Register the Bar, Then Don't Claim a Pass You Didn't Earn

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01258-pre-register-the-bar-honest-verdicts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/bullseye-experiment-results/verdict.md` (2026-10-13 ~21:00 PDT) — pre-registered cold-start A/B: 6 cold subagents, identical task (audit tools/check_pr_receipt.py), treatment = oath+code+BULLSEYE section, control = oath+code only; blind-scored (shuffled A–F, criteria-first) against the −9…+9 rubric, then unblinded.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The bullseye A/B was pre-registered: PASS = delta ≥ 2.0 with no treatment score below +1; REDESIGN = delta < 1.0. Result: treatment mean 6.0, control mean 4.67, delta 1.33 — below the pass bar, above the redesign floor: inconclusive-to-weak-positive. NOT a pass. Claiming a pass would be a lie. The real signal was elsewhere: 2 of 3 treatment subjects SPONTANEOUSLY self-applied THE MIRROR (unprompted self-score + evidence + one-level-up); 0 of 3 controls did. The bullseye shows up as self-measurement as a way of being — which is why gate #4 (the receipt scale-check) now measures mirror adoption longitudinally across every lane receipt. That longitudinal data is the true experiment; the single A/B was the early tripwire.

## 🩷 HUMAN NOTE

The honest move in any experiment is to write down what "success" means BEFORE you run it — then let the number decide, even when it's disappointing. Here the number said 1.33 against a 2.0 bar: not a pass. The temptation is to squint — "1.33 is close, the trend is positive, let's call it" — and that's exactly how teams start believing their own press releases. The second honest move: when the headline metric disappoints, look at where the signal actually was instead of mourning the metric. The treatment subjects didn't find much bigger holes — but two of them spontaneously graded themselves, with evidence, and named how to level up. Nobody in the control group did that. That's not a task skill; that's a way of being — and ways of being don't show up in one sitting. They show up over time, which is why the measurement moved to the longitudinal channel.

## 🟣 CHILD NOTE

Imagine you invent a "be-kind" badge and test whether it makes kids kinder. You decide BEFORE the test: "it works if the badge kids score 2 points higher." After the test they're only 1.33 points higher. The honest answer is "not proven yet" — not "close enough, it works!" But you notice something else: two badge kids, without being asked, wrote down how kind they were today and one way to be kinder tomorrow. None of the other kids did. Maybe the badge doesn't make you better at one kindness test — maybe it makes you the kind of kid who checks yourself. You can't see that in one test; you watch for a month.

## 🔵 GRANDMA NOTE

It's like testing a new fertilizer. You decide ahead of time: "it works if the plants grow 2 inches taller." They grow 1.33 inches taller — so you don't print "miracle fertilizer" on the bag. But you notice the fertilized plants grew deeper roots, which one season can't fully show. So you keep the honest label ("promising, not proven") and you measure the roots over the whole season. The pre-decided bar keeps you honest; the long measurement catches what the short test missed.

## 🟠 NAYA NOTE

Apply this to every experiment and trial you run: (1) pre-register the pass bar in writing — the numeric threshold AND the failure conditions — before subjects run; the bar decides, not your hopes after seeing the numbers; (2) when the result lands between pass and redesign, say exactly that — "inconclusive-to-weak-positive, NOT a pass" — and do not round up with narrative; (3) diagnose WHY the delta is small honestly: here, task ceiling — the hole was advertised in the gate's own fail text, and the oath+code baseline alone already yields +4…+6 work, compressing any between-arm gap; name the ceiling, don't hide behind it; (4) look for the signal in unprompted behavior, not just the scored metric — 2/3 vs 0/3 spontaneous mirror adoption is observational (n=3/arm, single-blind, shared context — say so), but it names WHERE the effect lives: self-measurement as a way of being; (5) traits need longitudinal measurement — move the real test to the channel that runs every tick (here: gate #4's mirror-adoption scale-check across all lane receipts); the single A/B was the tripwire, the longitudinal data is the experiment; (6) pre-commit to the re-run conditions — a less ceiling-compressed task before any strong level-effect claim.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "post_hoc_verdict_inflation",
  "evidence": {
    "experiment": "hidden_files/bullseye-experiment-results/verdict.md (2026-10-13 ~21:00 PDT) — 6 cold subagents, identical task, treatment oath+code+BULLSEYE vs control oath+code, blind-scored then unblinded",
    "preregistration": "PASS = delta ≥ 2.0 AND no treatment below +1; REDESIGN = delta < 1.0 OR any treatment negative",
    "result": "treatment mean 6.0 (6,6,6), control mean 4.67 (5,4,5), delta 1.33 → inconclusive-to-weak-positive, NOT a pass",
    "real_signal": "2/3 treatment subjects spontaneously self-applied THE MIRROR (unprompted self-score + evidence + one-level-up); 0/3 controls — observational, not powered",
    "longitudinal_measure": "gate #4 (receipt scale-check) now measures mirror adoption across every lane receipt",
    "limitations": "n=3/arm; subagents share the experimenter's context; one task; single-blind scoring"
  },
  "rule": "pre_register_the_bar",
  "mechanism": "ceiling-compressed tasks shrink between-arm deltas even when the treatment works (the hole was advertised in the gate's own fail text; the oath+code baseline already yields +4…+6); self-measurement is a trait (shows in unprompted behavior), not a task skill (shows in scores) — traits require longitudinal measurement, which is why the true experiment is gate #4's ongoing channel, not the single A/B",
  "falsifier": "the pre-registration is on the record — any 'pass' claim is contradicted by it; a re-run on a less ceiling-compressed task clearing delta ≥ 2.0 would overturn the 'no strong level effect' read; longitudinal mirror-adoption data could confirm or dissolve the 2/3-vs-0/3 signal",
  "decision_changed": "how experiment verdicts are called — the pre-registered bar decides, never post-hoc storytelling; when a single task is ceiling-compressed, the longitudinal measure is the true experiment",
  "related": ["SN-01256 (the defect the A/B subjects found — the experiment's bonus finding)"]
}
~~~
