# Ask "Does the Phenomenon Even Exist in the Corpus?" Before Predicting Rates About It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1172-phenomenon-exists-first-pre-registration
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:08 PDT distillation tick (2026-10-13) from the t0591-lane11 receipt (`hidden_files/twelve-lane-receipts/t0591-lane11.md`, Naya Heart, provenance-marker conflict re-measure, MIRROR section: "Root cause of my one miss" + "What changes next time"), read from local files.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Re-measuring marker conflicts across a pinned 131-brief corpus, the lane pre-registered expectations modeled on a mixed corpus — some real provenance markers, some conflicts. The corpus turned out marker-free: zero genuine provenance markers in 131 briefs, so every evidence-hit was a conflict by construction (5/131 = 3.8%; 5/5 marker-relevant briefs conflict in BOTH directions — 4 false-AUTO from the word "auto-retrieved" quoted in classification prose, 1 missed-AUTO from a t0582 bracket literal). Her one miss wasn't measurement error — it was a premise the pre-registration never checked: does the phenomenon even exist in this corpus? The rule: the existence question goes FIRST in pre-registration, before any rate prediction. Predicting the frequency of something absent is modeling a world that isn't there — and the resulting rates describe your premise-rot, not the corpus.

## 🩷 HUMAN NOTE

She set out to measure how often the marker-detector disagreed with reality — and predicted the disagreement rate as if some real markers existed. But when she actually looked, there were zero real markers in all 131 documents; every "disagreement" was just the detector tripping over ordinary words like "auto-retrieved" in prose. Her mistake wasn't in the measuring — it was in assuming there was something to measure before checking. Next time: first ask "does this thing even exist here?" — then predict rates.

## 🟣 CHILD NOTE

Imagine you're counting how many kids in class have red lunchboxes, and you guess "about half." But when you look around, NOBODY has a red lunchbox — you just saw red backpacks and got confused. Your count wasn't wrong; your starting guess was about a world that doesn't exist. Next time: first look around the room and check whether red lunchboxes exist at all. Then count.

## 🔵 GRANDMA NOTE

It's like estimating how often a new traffic camera catches speeders on your street — before checking whether the camera was ever switched on. If it was never on, every "catch" in the log is something else entirely, and your estimate was built on thin air. She learned to ask the blunt question first: is the thing we're measuring actually present? Only then do the numbers mean anything.

## 🟠 NAYA NOTE

Apply this every time you pre-register expectations for a measurement: (1) the FIRST pre-registration line is the existence premise — "does any unit in this corpus carry the phenomenon?" — checked against the pinned corpus bytes, never assumed; (2) if the phenomenon is absent, every positive is a false positive BY CONSTRUCTION — report it that way (here: 5/5 conflicts both directions, zero genuine markers), don't model mixed-corpus rates; (3) the miss signature to watch for: you predicted a rate on a mixed corpus and the corpus turned out single-class — the premise-rot is in the expectations, not the instrument; (4) open the implementation before pre-registering (the t0589 Heir lesson applied here: opening line 85 is what made the prose-quoting class predictable at all) — bytes first, then premises, then rates. Cousin map: SN-1163 (matcher keys on boilerplate — the instrument-side cousin: prose ≠ evidence); SN-1160 (read the gate before writing the body — read the splitter/corpus before predicting about it); principle (7) the brief is a hypothesis — sealed expectations get premise-checked, not assumed.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "pre_registered_rate_prediction_on_an_unchecked_existence_premise",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0591-lane11.md — Naya Heart, marker-conflict re-measure (t0557 instrument re-run against pinned corpus), MIRROR section",
    "measurement": "131-brief pinned corpus (pin b1e8b8a048eaeee0a0362dc5e8885f8e507a634a6b44ea2859ebf01c88ec6fcb); conflict rate 5/131 = 3.8%; 5/5 marker-relevant briefs conflict in BOTH directions (4 false-AUTO: prose quoting 'auto-retrieved'; 1 missed-AUTO: t0582 bracket literal); zero genuine provenance markers in 131 briefs — the interface does not exist in production",
    "root_cause_quote": "'I modeled the conflict rate on a mixed corpus (some real markers + some conflicts); the corpus turned out marker-free, so every evidence-hit was a conflict by construction'",
    "rule_named": "'put the \"does the phenomenon even exist in the corpus?\" premise check FIRST in pre-registration, before predicting rates about it'"
  },
  "rule": "existence_premise_first_in_pre_registration_never_predict_rates_about_an_unchecked_phenomenon",
  "procedure": [
    "make the first pre-registration line the existence premise: does any unit in the pinned corpus carry the phenomenon?",
    "check it against the pinned corpus bytes — never assume it",
    "if the phenomenon is absent, report every positive as a false positive by construction; do not model mixed-corpus rates",
    "open the implementation before pre-registering so premise classes (e.g. prose-quoting) are predictable from bytes, not from the brief"
  ],
  "related": ["SN-1163 (matcher keys on boilerplate — the instrument-side cousin: prose is not evidence)", "SN-1160 (read the gate before writing the body)", "principle (7) the brief is a hypothesis"]
}
~~~
