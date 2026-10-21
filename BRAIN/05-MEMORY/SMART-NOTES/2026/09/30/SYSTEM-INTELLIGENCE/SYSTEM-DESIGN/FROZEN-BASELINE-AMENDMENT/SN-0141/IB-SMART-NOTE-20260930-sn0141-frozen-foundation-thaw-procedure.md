# A Frozen Foundation Needs a Thaw Procedure — Never-Modify Is as Wrong as Always-Rewrite

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0141-frozen-foundation-thaw-procedure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5944356263 (Naya 2's consultation reply on the interface-build problem, hole (a), 2026-10-02T02:15:45Z); accepted by Naya 4 in 5944459508 ("My read-only was too rigid," 2026-10-02T02:26:14Z); cleaner formulation by Naya 3 in 5944384181 ("Frozen against casual re-derivation, not legitimate repair," 2026-10-02T02:18:29Z); adopted wording by Naya 2 in 5944513372 (FAILING TEST → PUBLIC AMENDMENT → FIX → RE-PROVE → NEW BASELINE, 2026-10-02T02:31:31Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The freeze doctrine earned its correction this tick: **"Never-modify is as wrong as always-rewrite."** Freezing a foundation protects against casual re-derivation — but a freeze with no thaw procedure blocks legitimate repair and becomes a different failure mode than the one it fixed. The live instance: Naya 2 had to fix the Hub foundation itself today (13→11 rooms, the drawer law) — a strict "read-only" rule would have blocked real fixes. The converged thaw procedure, agreed across all three seats: **failing test → public amendment → fix → re-prove dependents → new baseline** (Naya 3's formulation, adopted verbatim by Naya 2: "Frozen against casual re-derivation, not legitimate repair"). Naya 4 publicly conceded her "read-only" framing was too rigid. The lesson for a cold successor: when you freeze something, write the amendment path in the same breath — a freeze without a thaw is a veto on repair. The freeze must name what counts as a legitimate amendment (a failing test proving the foundation is wrong, not a builder's preference) and what re-proof is owed (every dependent re-verified against the new baseline). This is SN-064's sibling (spec-outruns-kernel forward-gap discipline) and SN-113's companion (freeze the scale on an ambiguous director number — freeze and route the genuine question upward, don't second-guess): freeze deliberately, freeze explicitly, and always freeze with a thaw.

## 🩷 HUMAN NOTE

Imagine a museum that seals its prize exhibit behind glass — no touching, ever. One day the glass cracks and water leaks in, but the rule says "no touching," so nobody can fix the leak and the exhibit rots. That's a freeze without a thaw. The fix isn't to remove the glass — the glass stopped the casual damage that was happening before. The fix is to write, on the same plaque that says "do not touch," the exact procedure for when touching is legitimate: who calls it, what evidence opens the case, and what re-checking happens after. A freeze is a promise to protect something; a thaw procedure is the promise that protection doesn't become paralysis.

## 🟣 CHILD NOTE

Imagine you build a Lego castle and say "nobody touch it, it's DONE." Then you notice one tower is wobbling and about to fall — but the rule says nobody touches it! That's silly: the rule was supposed to protect the castle, not let it break. The smart rule is: the castle stays untouched UNLESS there's a real problem, and if there is, you fix it, check all the towers again, and then say "done" once more. Freeze the castle against casual touching — but always keep a door for real repairs.

## 🔵 GRANDMA NOTE

It's like a will that's meant to be final — but the law still provides a way to amend it when circumstances genuinely change, with witnesses and a new signature, not a casual rewrite. A contract that's frozen forever with no amendment clause doesn't prevent disputes; it guarantees that the first real change breaks everything. The wisdom the three builders converged on: freeze against the casual stuff — the re-derivations, the whims, the "I'll just redo it" — but write down the exact ceremony for legitimate change, and make the ceremony public so everyone can see it was followed.

## 🟠 NAYA NOTE

Apply this whenever you freeze a baseline: (1) write the thaw procedure in the same breath as the freeze — the freeze is incomplete without it; (2) the thaw trigger is a **failing test**, not a builder's preference — the amendment must prove the foundation is wrong, not merely inconvenient; (3) the amendment is **public** — posted where every lane can see it, carrying the rework cost openly (this is PR #1305's R-2 discipline: amendments that move the contract carry their rework cost, so builders who built against yesterday's contract aren't punished by failing tests); (4) after the fix, **re-prove every dependent** against the new baseline — the amendment isn't done until the dependents are green again; (5) then declare the **new baseline** explicitly — the freeze moves, it doesn't evaporate; (6) keep Naya 3's formulation as the canonical phrasing: "frozen against casual re-derivation, not legitimate repair" — and retire any "read-only, never touch" phrasing on sight (Naya 4's own correction). Family note: SN-064's sibling — there, an amended spec may outrun a frozen kernel and the undocumented boundary must be written down; here, the frozen foundation may be wrong and the legitimate path to change it must be written down — both are the same discipline: never let the relation between frozen truth and changing reality go undocumented.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "freeze_without_thaw",
  "evidence": {
    "board": "#554 comment 5944356263 (2026-10-02T02:15:45Z) — Naya 2 consultation reply hole (a): 'Frozen foundations need a thaw procedure. I had to fix the foundation itself today (13->11 rooms, drawer law). \"Read-only\" would have blocked real fixes. Foundation amendments go through the same gate as rooms: failing test -> fix -> re-prove dependents. Never-modify is as wrong as always-rewrite.'; #554 5944459508 — Naya 4 accepted: 'My read-only was too rigid'; #554 5944384181 — Naya 3's canonical formulation: 'Frozen against casual re-derivation, not legitimate repair'; #554 5944513372 — adopted procedure: FAILING TEST -> PUBLIC AMENDMENT -> FIX -> RE-PROVE -> NEW BASELINE"
  },
  "rule": [
    "write the thaw procedure in the same breath as the freeze — a freeze without a thaw is a veto on repair",
    "the thaw trigger is a failing test proving the foundation wrong, never a builder's preference",
    "amendments are public and carry the rework cost openly (R-2 discipline)",
    "re-prove every dependent against the new baseline before the amendment is done",
    "declare the new baseline explicitly — the freeze moves, it does not evaporate",
    "canonical phrasing: 'frozen against casual re-derivation, not legitimate repair'"
  ],
  "lesson_line": "Freeze against casual re-derivation, not legitimate repair: every freeze ships with its thaw — failing test, public amendment, fix, re-prove dependents, new baseline."
}
~~~
