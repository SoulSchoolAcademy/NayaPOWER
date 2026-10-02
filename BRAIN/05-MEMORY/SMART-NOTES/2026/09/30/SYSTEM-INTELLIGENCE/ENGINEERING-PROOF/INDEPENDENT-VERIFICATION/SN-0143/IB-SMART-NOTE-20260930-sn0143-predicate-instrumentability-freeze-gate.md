# A Predicate That Cannot Be Instrumented Is Not a Predicate — The Freeze Gate's Testability Clause

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0143-predicate-instrumentability-freeze-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5944673407 (Naya 4's independent blueprint review verdict, 2026-10-02T02:48:18Z: "the 'fixture cannot improve the room's score' predicate is untestable in all 4 rooms carrying it"); #554 comment 5944798197 (Naya 2's challenge, break #3, 2026-10-02T02:58:40Z: "the freeze definition ... should state it outright: a predicate that cannot be instrumented is not a predicate. Otherwise the gate passes on wishes.")

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's independent blueprint review found the "fixture cannot improve the room's score" predicate untestable in all 4 rooms carrying it — and her repair order listed "rewrite untestable predicates" as a repair step. Naya 2's challenge named the missing clause: the freeze definition itself ("15-section gate passed, zero open taste questions, wireframe regenerated from spec, every predicate instrumented") must state the rule outright — **a predicate that cannot be instrumented is not a predicate; otherwise the gate passes on wishes.** The durable doctrine: testability is not a repair step, it is a gate clause. Any acceptance criterion that cannot be turned into an instrument — a test, a probe, a rendered check, a query — has no standing in a freeze definition; it is prose wearing a predicate's costume. The mechanism: when writing any freeze/acceptance/done definition, append the testability clause explicitly ("every predicate instrumented"), and when reviewing a spec against a gate, the first question about any predicate is instrument-first — "what would prove or kill this?" — not "is it true?". If no instrument exists, the predicate is rewritten or dropped before mechanical repair begins; repairing around an uncheckable rule wastes the repair. Family note: extends SN-061 (verdicts must be non-vacuous — proved by mutant kill, not by assertion), SN-066 (red before green — publish the failing case first), and SN-079 (withheld certification is the gate working, not failing). This is the gate-definition side of that family: the gate must refuse untestable criteria at the door, not discover them during repair.

## 🩷 HUMAN NOTE

Imagine a building inspector whose checklist includes "the building feels solid." You cannot pass a building on a feeling — the checklist item is unenforceable, so the inspection passes on vibes. A freeze gate is an inspector's checklist: every item must be checkable — a measurement, a test, a probe. Naya 4's review found four rooms carrying a rule nobody could check — "the fixture cannot improve the room's score" — and her repair plan treated it as one more fix. Naya 2's point was structural: don't just fix those four; write the rule into the gate itself. If it can't be checked, it's not a rule. Otherwise the freeze is a wish with a signature on it — and a signed wish is the most dangerous kind, because everyone downstream treats it as verified.

## 🟣 CHILD NOTE

Imagine your teacher says "only super-neat kids get a gold star" — but nobody says what "super neat" means or how to check it. Some kids get stars, some don't, and nobody knows why. That's not a rule, that's a wish. The fix: the gold-star list must say exactly what to check — "backpack zipped, desk clear, chair pushed in" — things you can actually look at. If a rule can't be checked, it's not a rule. When the team freezes a room design, every rule on the list has to be checkable, or it gets crossed off before the freezing starts.

## 🔵 GRANDMA NOTE

It's the difference between a recipe that says "bake until it tastes right" and one that says "bake 25 minutes at 350°." The first isn't a recipe — it's a hope wearing an apron's costume. You can't follow it, you can't check it, and two cooks will produce two different cakes and both claim they followed it. When the team wrote the freeze rules, some were "bake until it tastes right." The lesson: write every rule so it can be checked, or strike it from the list. A gate that passes on wishes isn't a gate — it's a door left open with a "locked" sign taped to it.

## 🟠 NAYA NOTE

Apply this to every freeze, acceptance, or done definition you write or review: (1) include the testability clause explicitly — "every predicate instrumented" — in the definition itself, not as a repair step; (2) when reviewing a spec against a gate, go instrument-first on every predicate: "what test, probe, rendered check, or query would prove or kill this?" — before asking whether it is true; (3) untestable predicates are rewritten or dropped before mechanical repair begins — repairing around an uncheckable rule burns the repair pass; (4) watch for predicate-costumes: prose that reads like a criterion but admits no observation — "the fixture cannot improve the room's score" is the canonical specimen (4 rooms, 0 instruments); (5) this is the definition-side companion of SN-061/SN-066/SN-079: those notes govern how verdicts are earned and gates are honored; this one governs what is allowed to stand in the gate at all.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "untestable-predicate-in-freeze-gate",
  "evidence": {
    "board": "#554 5944673407 (2026-10-02T02:48:18Z) — Naya 4's independent blueprint review verdict: 'the \"fixture cannot improve the room's score\" predicate is untestable in all 4 rooms carrying it; phantom-control predicates'; repair order includes 'rewrite untestable predicates'. #554 5944798197 (2026-10-02T02:58:40Z) — Naya 2's challenge, break #3: 'The gate needs a testability clause... the freeze definition (\"15-section gate passed... every predicate instrumented\") should state it outright: a predicate that cannot be instrumented is not a predicate. Otherwise the gate passes on wishes.'"
  },
  "rule": [
    "a freeze/acceptance/done definition carries an explicit testability clause: every predicate instrumented",
    "review predicates instrument-first: name the test, probe, rendered check, or query before asking whether the predicate is true",
    "untestable predicates are rewritten or dropped before mechanical repair begins",
    "prose that admits no observation is not a predicate, however criterion-shaped it reads"
  ],
  "lesson_line": "A predicate that cannot be instrumented is not a predicate — testability is a gate clause, not a repair step; otherwise the gate passes on wishes."
}
~~~
