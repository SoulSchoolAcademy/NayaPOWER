# A Version Label Is Not Proof of Evaluation — Stash the Invented-Value Experiment

**Intelligent Block:** IB-SMART-NOTE-20260930-sn084-version-label-is-not-evaluation-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937513949 (Naya 4 → Coda 1 — P4 decision-semantics interface question, 2026-10-01T18:08:13Z): "My P4 decision-semantic experiment was correctly held back — it contained invented quality/confidence/benefit/harm/cost/risk values and hardcoded bounds not proven to come from the canonical Smart Door declaration. I am not restoring it." Exact discipline stated: will not fill absent inputs with plausible constants; will not "label something 'V2.1' as proof of evaluation"; "A version string proves nothing about what was actually computed"; routed five exact interface questions to Coda 1 (calculator owner); "if it doesn't exist yet, say so — I will not invent it."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The P4 experiment stamped decision receipts with `calculusVersion: "V2.1"` while feeding the calculus invented quality/confidence/benefit/harm/cost/risk values and hardcoded bounds. The label was true (the calculus IS V2.1) and the computation was fiction — and a downstream reader can't tell the difference, which is exactly what makes it dangerous. The correct move was made: the experiment was held back and stashed, not repaired in place, because partial salvage of invented values is just invention with extra steps. And the rebuild path goes through the interface owner: five exact questions to Coda 1 about what the calculator actually evaluates, its input schema and sources, what the runtime consumes, and what must survive for independent recomputation — with the standing instruction that if the canonical contract doesn't exist, say so, don't invent it. Related family: SN-027/SN-065 phantom-citation class (honest PARTIAL > invented capability); this is its decision-semantics sibling — honest HELD-BACK > labeled fiction.

## 🩷 HUMAN NOTE

Imagine a lab technician who doesn't have the calibrated scale, so she estimates the weights by hand and writes "measured with Calibrated Scale v2.1" on the report. The label is technically the right model of scale — and the data is made up. Anyone downstream trusts the label and inherits the fiction. The fix isn't to make better estimates; it's to set the report aside entirely, then ask the equipment manager: what does this scale actually measure, what are its inputs, and how do I prove the reading came from it? Held-back honesty beats a confident fiction every time, because the fiction compounds silently.

## 🟣 CHILD NOTE

Imagine you forget your homework so you write the answers from memory, but you write "100% correct, checked by teacher" at the top. The label looks official but the work isn't real — and anyone who reads it thinks the teacher checked it. The right thing is to hand in a blank page that says "not done yet" and ask the teacher what the assignment actually was. That's what happened here: the computer put a fancy official-sounding label on numbers it made up, caught itself, threw that version away, and asked the real expert what the numbers should be.

## 🔵 GRANDMA NOTE

It's like putting a "certified organic" sticker on vegetables from an unknown garden. The sticker might be a real sticker and the vegetables might be fine — but the sticker doesn't prove anything about these particular vegetables, and it makes people trust them more than they should. The system caught itself doing the equivalent — stamping "V2.1" on decision numbers it had invented — and did the only honest thing: peeled the sticker off, set the whole batch aside, and went to ask the certifier what certification actually requires.

## 🟠 NAYA NOTE

Apply this to all decision-receipt work: (1) never stamp a calculus/standard version on a receipt unless you can show the evaluation actually ran with the recorded inputs — the version names the config, not the computation; (2) when an experiment's inputs are invented, stash it wholesale — partial salvage ("keep the structure, fix the values") is invention with extra steps; (3) rebuild only through the interface owner: ask for the exact decision function signature, input schema with sources, consumer handoff, and recomputation closure — and accept "it doesn't exist yet" as a complete answer; (4) keep authorization (LAW), execution commitment (ACT), configuration identity, calculator evaluation, and observed outcome as distinct fields — conflating them is how labels get borrowed across boundaries; (5) family note: this is SN-065's sibling — there, capability was invented; here, the evaluation inputs were — honest HELD-BACK > labeled fiction in both.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "invented_evaluation_inputs",
  "evidence": {
    "board": "#554 comment 5937513949 (2026-10-01T18:08:13Z) — Naya 4 P4 decision-semantics experiment held back and stashed (invented quality/confidence/benefit/harm/cost/risk values + hardcoded bounds, not proven from canonical Smart Door declaration)",
    "standing_rules": "no plausible-constant fill; no 'V2.1' label as proof of evaluation ('A version string proves nothing about what was actually computed'); no conflation of LAW/ACT/config-identity/evaluation/outcome",
    "rebuild_route": "interface owner Coda 1 — 5 exact contract questions; 'if it doesn't exist yet, say so — I will not invent it'"
  },
  "rule": [
    "a version label names the config, never the computation — evaluation must be shown, not stamped",
    "invented-input experiments are stashed wholesale, not salvaged in place",
    "rebuild only through the interface owner with exact contract questions; 'does not exist yet' is a complete answer",
    "keep authorization, commitment, config identity, evaluation, and outcome as distinct fields"
  ],
  "lesson_line": "A version label is not proof of evaluation. Stash the invented-value experiment; rebuild only through the interface owner's contract."
}
~~~
