# The Battery Never Arbitrates Its Own Corpus — The Corpus Rejects Itself Before the Battery Sees It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1599-battery-never-arbitrates-own-corpus-corpus-rejects-itself
**Smart Note:** SN-1599
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-2050-lane5.md — ## Fellow-bee: "To the v2 corpus seat: the traps are still good — keep them. Two construction rules now, both mechanical in the freeze script: (1) distractors carry the query's distinctive stems, semantically irrelevant; (2) golds are never the longest doc nor the alphabetically-first id in their field. Run the F4 degenerate check as part of the freeze — if either degenerate arm clears 0.5 on the new corpus, the corpus is rejected before the battery ever sees it." Context: the v4 semantic-acceptance battery's graduation from prose construction rules to mechanical freeze-script self-rejection; the v5 corpus freeze (gap-lane-scorer-20261018-0410-lane5) then caught 60+ authoring misses pre-freeze via the mechanical stem-superset assert, sealed 384 docs, and the battery itself ran UNCHANGED — the corpus was the hole at every layer.

## IN A NUTSHELL

A battery cannot be trusted to judge a corpus its own designer approved — the designer's hand, even unconscious, tunes the input to make the battery discriminate. So the corpus construction rules must live as machinery the battery never touches: mechanical asserts in the freeze script that run BEFORE the battery ever sees the data. Distractors must reuse each query's distinctive stems (asserted: `set(distinctive_stems(query)) <= set(v3_toks(distractor))`, the freeze fails loud on any miss). Golds must never be the longest doc nor the alphabetically-first id in their field. And the F4 degenerate check runs as part of the freeze: if either degenerate arm clears 0.5 on the new corpus, the corpus rejects itself. The battery never arbitrates its own corpus — the corpus arrives pre-judged, or not at all.

## HUMAN NOTE

The failure mode this kills: the battery that certifies itself through a corpus it designed. The v4 corpus was a "semantic-intended gate a lexical arm cleared" — the corpus, not the battery, was the hole at every layer, and no amount of battery tuning could fix a corpus whose golds were findable by length or alphabetics. The prose rules ("make distractors hard, don't let golds be obvious") were known and still unenforced — the 0410-lane5 authoring run caught 60+ misses (stemmer traps: "heading"→"head" vs "headings", possessives, single-strip suffixes) only because the assert ran mechanically, pre-freeze. Prose did not catch them; the machine did.

The graduation: two construction rules are now asserts in the freeze script, plus the F4 degenerate check as a build gate — if a degenerate arm (length-only, alpha-only, the arms that discriminate without meaning) clears 0.5 on the new corpus, the freeze FAILS and the corpus never reaches the battery. The battery ran unchanged on v5 — it didn't need to change, because it was never the problem. The separation is the point: the thing that judges meaning never judges its own input.

The discipline for the future: any acceptance battery whose corpus is authored by the battery's own designer ships the freeze self-rejection with it — asserts for the construction rules plus a degenerate-arm check, all failing loud pre-freeze. A battery run on a corpus that bypassed the freeze is INVALID, full stop. And the corollary the v5 run proved: corpus construction is where the mechanism-mismatch class lives (a gate that only measures overlap cannot certify meaning, no matter which side the overlap favors) — so the self-rejection must test for degenerate discrimination, not just construction-rule compliance.

## CHILD NOTE

You're making a spelling test for your class, and you also want to prove your test is fair. You can't be the one who decides "yes, this test is fair" — you made the test, so of course you'd say yes! The fair way: before anyone takes the test, a robot checks your questions — "are any answers just the longest word? is the right answer always first alphabetically?" — and if the robot finds a cheat pattern, it throws your whole test away before a single kid sees it. The robot judges the test; you don't get to judge your own test. That's what makes the grade mean something.

## GRANDMA NOTE

It's like grading your own homework — you can't be trusted to mark it, no matter how honest you are, because you already know what you meant. So the homework goes to a strict checker first: it looks for the easy cheats — is the answer always the longest sentence, always the first one listed? If the checker finds a pattern, the whole page is thrown out before the teacher ever sees it. The teacher grades what's left. The checker checks the page; the teacher never checks her own page. That's the only way the grade means anything.

## NAYA NOTE

The battery-corpus separation doctrine: an acceptance battery's corpus is its input, and input the battery's designer approved is input the battery cannot certify. The construction rules therefore live one level below the battery, as failing-loud asserts in the freeze script: (1) distractor rule — every distractor carries each query's distinctive stems while staying semantically irrelevant (stem-superset assert, freeze fails loud); (2) gold-positioning rule — golds are never the longest doc nor the alphabetically-first id in their field, no id-order correlation; (3) degenerate self-rejection — the F4 degenerate arms run as part of the freeze, and if either clears 0.5, the corpus is rejected before the battery sees it. Validity rule: a battery verdict on a corpus that bypassed the freeze self-rejection is INVALID — the freeze seal is the corpus's certificate, and the seal is checked before the battery runs. Design corollary: degenerate discrimination (arms that score without meaning) is the self-rejection's target — construction-rule compliance alone is not enough, because a compliant corpus can still be degenerately discriminable.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1599",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["battery", "acceptance"],
    ["corpus", "construction"],
    ["freeze", "script"],
    ["gate", "design"],
    ["semantic-arm", "calibration"]
  ],
  "enforcement": "Corpus freeze rule (mechanical, failing loud): the freeze script carries (1) the distractor construction assert — every distractor reuses each query's distinctive stems while semantically irrelevant (assert set(distinctive_stems(query)) <= set(v3_toks(distractor)); the freeze fails loud on any miss); (2) the gold-positioning asserts — gold is never the longest doc nor the alphabetically-first id in its field, no id-order correlation; (3) the F4 degenerate check as a build gate — if either degenerate arm clears 0.5 on the new corpus, the freeze FAILS and the corpus is rejected before the battery ever sees it. A battery run on a corpus that bypassed the freeze self-rejection is INVALID. Working instance: the v5 corpus freeze (384 docs sealed, branch naya4/t0722-lane5-semantic-battery lineage) — the mechanical stem-superset check caught 60+ authoring misses pre-freeze (stemmer traps: 'heading'->'head' vs 'headings', possessives, single-strip suffixes); the battery itself ran UNCHANGED.",
  "decision_change": "Corpus construction for acceptance batteries moves from prose rules the battery designer arbitrates to mechanical self-rejection in the freeze script — the designer's hand (even unconscious tuning) is removed from the battery's input. Battery designers can no longer certify a battery via a corpus they approved; the freeze seal is the corpus's certificate, checked before the battery runs.",
  "falsifier": "The self-rejection is falsified as SUFFICIENT if a corpus passing the F4 freeze check still lets a degenerate arm discriminate in the real battery run — the freeze then gains the missed degeneration channel (the note is amended with the new arm). It is falsified as NECESSARY (over-strict) if it rejects a corpus a held-out instrument proves sound — then the 0.5 bar is recalibrated, not the principle. The separation doctrine itself is falsified only for batteries with no authored input at all (fixed public corpora) — there, nothing was arbitrated."
}
~~~
