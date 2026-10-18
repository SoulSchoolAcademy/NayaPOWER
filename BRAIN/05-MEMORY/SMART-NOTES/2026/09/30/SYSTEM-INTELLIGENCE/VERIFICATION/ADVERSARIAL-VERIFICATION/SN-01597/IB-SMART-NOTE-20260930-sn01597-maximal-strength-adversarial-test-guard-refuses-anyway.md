# The Strongest Adversarial Test Makes the Bad Case Maximally Strong and Watches the Guard Refuse Anyway — Refusal of Below-Floor Noise Proves Nothing About the Guard

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1597-maximal-strength-adversarial-test-guard-refuses-anyway
**Smart Note:** SN-1597
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0330-lane5-veracity.md — ## Mirror lesson: "The strongest adversarial test isn't 'make the bad case weak' — it's 'make the bad case maximally strong and watch the guard refuse anyway.' A single unique term giving SN-D4 verbatim-carry decisive relevance (phrase bonus 40.0, score above floor) plus zero genuine overlap forced the guard into its hardest position: refuse decisive-relevance falsified intelligence, visibly, as uncertainty. Refusal proven against decisive relevance is the proof that matters; refusal of below-floor noise proves nothing about the guard." Context: REFUSED_FALSIFIED_ONLY guard harness hidden_files/lane5-gap0330-realcorpus/lane5_gap0330.py; 634-entry scale; refusal fired 3/3 with the guard's own stderr signal {"veracity_guard": "REFUSED_FALSIFIED_ONLY", "demoted": [...]} and exit rc=1; falsified entries scored above the 40.0 relevance floor (the phrase bonus did its job); negative control clean, zero false falsifications.

## IN A NUTSHELL

When you prove a fail-closed guard, do not test it with bad inputs so weak they'd be refused by accident — bounced by an earlier filter, a floor, a validation error that has nothing to do with the guard. Build the bad case as strong as it can possibly be: the falsified input must score ABOVE the decision floor (decisive relevance), so the only thing standing between it and acceptance is the guard itself. Then watch the guard refuse through its OWN refusal path — visibly, as its own signal. Refusal proven against decisive relevance is the proof that matters; refusal of below-floor noise proves nothing about the guard, because the guard never had to fire.

## HUMAN NOTE

The failure mode this kills: the "the guard refused the bad input" victory lap where the bad input was dead on arrival anyway. The veracity lane's first instinct could have been to feed the guard a falsified note with zero relevance and celebrate the refusal — but a falsified note scoring 0 gets excluded by the `score <= 0: continue` branch long before the guard sees it. That refusal would have been the floor's doing, not the guard's, and it would have proven exactly nothing.

What the seat did instead: it df-scanned all 632 genuine notes to find the single stemmed term unique to the synthetic falsified note ("slows", df=0), gave SN-D4 verbatim carry of that term, and let the phrase bonus (40.0) push the falsified note decisively ABOVE the 40.0 relevance floor — while all 632 genuine notes scored exactly 0. The guard's hardest position: a falsified note the ranking machinery loves, that only the guard can stop. The refusal fired 3/3 at 634-entry scale, and it fired as the guard's own signal — the exact stderr line and rc=1 — with the demoted lists proving the falsified entries were above-floor (not a below-floor non-event).

The discipline for the future: every guard proof names its adversary strength. If the adversary never cleared the floor, file the verdict NON-PROVING, not PASS. And every guard proof shows attribution: the refusal came from the guard's own path, named, with the guard's own bytes — because a guard that "refuses" by accident is a guard you have never actually seen fire.

## CHILD NOTE

You want to prove your big brother's "no touching my stuff" rule really works. Don't test it by putting a boring rock on his desk — he'd ignore it anyway, and you'd learn nothing. Put his FAVORITE candy bar on his desk, the one he can't resist — and watch HIM say "no, that's mine, don't touch it" and mean it. If he says no to the candy bar, the rule is real. If all you tested was the boring rock, you proved nothing — the rock never tempted anyone.

## GRANDMA NOTE

Testing a burglar alarm by whispering outside the window proves nothing — any old thing would stay quiet at a whisper. You test it by having someone rattle the window hard, good and loud — and then you check it was YOUR alarm that went off, not the neighbor's dog barking at something else. The loud rattle is the bad case at its strongest; your alarm's own bell is the guard's own signal. A test that can't tell your alarm from the neighbor's dog is not a test of your alarm.

## NAYA NOTE

The guard-verification doctrine, sharpened: (1) enumerate the guard's exact refusal path (signal, exit code, bytes) before testing — a test that short-circuits before the guard is vacuous by construction; (2) construct the adversary AT OR ABOVE the decision floor the guard protects — decisive relevance, verbatim carry, the mechanism's own scoring pushing the bad case over the bar; (3) demand attribution — the refusal must be observed as the guard's own signal, not an upstream filter's; (4) run the negative control — a genuine case at the same strength must pass, proving the guard refused the BAD case rather than everything. Scoring rule: a "guard refuses bad input" verdict whose adversary never cleared the floor is filed NON-PROVING. Corollary for test designers: when you are tempted to weaken the bad case to make the test pass, you are testing the floor, not the guard — strengthen the adversary until the guard is the only thing that can refuse, and let it.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1597",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["guard", "verification"],
    ["veracity", "refusal-guard"],
    ["adversarial", "test-design"],
    ["falsified", "intelligence"],
    ["proof", "fail-closed"]
  ],
  "enforcement": "Guard-acceptance rule (named check): a guard proof is accepted only when (1) the adversary is at or above the relevance/decision floor the guard protects — decisive relevance: e.g. falsified SN-D4 carried verbatim by the single stemmed term unique to it ('slows', df=0 across 632 genuine notes), phrase bonus 40.0, score above the 40.0 floor, zero genuine overlap; and (2) the refusal is attributed to the guard's OWN refusal path — observed as the guard's own signal (REFUSED_FALSIFIED_ONLY stderr line {\"veracity_guard\": \"REFUSED_FALSIFIED_ONLY\", \"demoted\": [...]} + exit rc=1), never an upstream filter or floor-clearing branch. A 'guard refuses bad input' verdict whose adversary never cleared the floor is filed NON-PROVING. Working instance: hidden_files/lane5-gap0330-realcorpus/lane5_gap0330.py — refusal fired 3/3 (R_full 633, R2_two_falsified 634, R3_lowercase 633 entries) against decisive-relevance falsified intelligence; demoted lists prove the falsified entries were above-floor; negative control clean, zero false falsifications.",
  "decision_change": "How adversarial tests of fail-closed guards are designed and judged: test designers strengthen the adversary to its hardest position (decisive relevance, above the floor) instead of weakening it to make the test pass; verifiers accept a guard proof only when the refusal is shown to come from the guard's own mechanism. A lane that accepted 'refused the weak bad case' as proof now scores that verdict non-proving.",
  "falsifier": "The principle is falsified if a guard's refusal of a maximal-strength adversary is later shown to be misattributed — the guard's own signal fired, but a different mechanism actually excluded the input — in which case the acceptance rule gains the attribution check it missed. It is also falsified for any guard whose entire job IS floor-clearing: there, below-floor refusal is the mechanism itself, and the rule reduces to 'name which floor' — the note's strong form does not apply to floor-guards."
}
~~~
