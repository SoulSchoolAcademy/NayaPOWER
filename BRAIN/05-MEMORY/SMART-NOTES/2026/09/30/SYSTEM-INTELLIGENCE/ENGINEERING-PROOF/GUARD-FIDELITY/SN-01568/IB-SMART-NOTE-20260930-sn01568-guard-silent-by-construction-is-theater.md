# A Guard Silent by Construction Is Theater — the Fix Isn't a Lower Number, It's a Different Shape

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01568-guard-silent-by-construction-is-theater
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The lesson-matcher's weak-slot re-route guard ("fire iff ≥2 of a batch's briefs carry a weak slot") structurally could never fire on single-brief batches — and the t0682 batch (1 brief, 1 weak slot, a real executor fold MISS) passed through it by construction, indistinguishable from a correct skip. The fix was not a lower number but a different shape: the rate S(B) = weak briefs / briefs-with-injections, FIRE iff S(B) ≥ 1/2 — every census-judged-weak batch fires (t0670 3/3, t0671 3/3, t0672 2/3, t0675 1/2, t0682 1/1), every clean batch stays silent, strictly better on the record. A guard that cannot fire at the smallest unit it guards is not conservative — it is theater.

## 🩷 HUMAN NOTE

A guard with an absolute-count threshold is secretly a guard with a minimum batch size. "Fire iff at least 2 weak briefs" means "never fire when the batch has 1 brief" — and the silence looks exactly like a healthy quiet tick, so nobody notices the guard is dead. The t0682 batch was a single brief with a genuinely weak slot (the executor's fold reported an mbc MISS: no credentialed-store measurement was taken) and it sailed through because the rule could not fire. The repair keeps the rule's intent ("fire on systematic weakness, not one-offs") but states it at every batch size: S(B) = weak briefs / briefs-with-injections, fire iff ≥ 1/2. The calibration table is the proof: every batch the census judged weak fires, every clean batch stays silent, and the old rule's two blind spots (t0675 1/2, t0682 1/1) now fire. Lesson for every future guard: state the smallest batch on which it can fire, and prove it fires there.

## 🟣 CHILD NOTE

If your alarm only rings when two people shout, one person shouting for help never wakes anyone up. Count the share of shouts, not the number.

## 🔵 GRANDMA NOTE

Rules that count "how many" can go blind when there are only a few things to count. A rule that asks "what share" works whether there is one brief or a hundred. When you build a tripwire, check it works at the smallest size it will ever see.

## 🟠 NAYA NOTE

An absolute-count threshold is a proxy for "systematic, not one-off" — but the proxy silently assumes a batch size it can fire on. When batches shrink below the threshold, the guard's silence is structural, and structural silence is indistinguishable from a correct skip: the theater is that everyone reads it as healthy. The rate form preserves the original predicate at every batch size. The known limit is named, not hidden: a MISS can mean a well-injected lesson the executor failed to apply, so the dispatcher's re-injection review distinguishes misinjection from executor shortfall — the rule counts both as weak, the review separates them. Design-time check from now on: every guard names the smallest batch it can fire on.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["guard", "guard-design", "re-route", "lesson-injection", "dispatch", "threshold"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "Any new guard brief must state the smallest batch size on which the guard can fire and show a calibration table (historical batches x verdict). A guard brief without a stated minimum-fire batch size is bounced. For this guard: the night-dispatcher's LESSON INJECTION block carries the adopted criterion S(B) = weak briefs / briefs-with-injections, FIRE iff S(B) >= 1/2; a future weak batch (census-judged) that S(B) misses re-opens the threshold.",
  "evidence": "weak-slot-guard-criterion-t0700-lane5.md (Naya Clarity Narzan, dispatcher-adoptable spec, 2026-10-17 ~18:13 UTC); twelve-lane-receipts/t0700-lane5.md (two-case proof re-derived at action time: t0679 0/1 SILENT, t0682 1/1 FIRES); lesson-injection-log.jsonl utc-grouped batches t0670/t0671/t0672/t0673/t0675/t0677/t0678/t0679/t0682.",
  "falsifier": "(a) A future batch the census judges weak (fold + vocabulary legs) that S(B) >= 1/2 misses, or (b) a future batch the census judges clean that S(B) >= 1/2 fires on. Either re-opens the threshold — report it, don't defend it. The 1/2 constant is fitted; the rate shape is the claim.",
  "mechanism": "An absolute-count threshold is a proxy for 'systematic, not one-off'. The proxy only works when the batch is at least as large as the threshold; below that size the guard is structurally silent, and structural silence is indistinguishable from a correct skip — the theater. The rate form S(B) = weak/|I(B)| expresses the same 'systematic' predicate at every batch size, so the guard fires wherever systematic weakness exists.",
  "names_decision_changed": "Guard design: check scale-invariance at design time — name the minimum-fire batch size and prove the guard fires there. Prefer rate forms over absolute-count forms whenever the guarded batches vary in size."
}
~~~

## 🟢 LEARNING LESSON

A guard that can't fire at the smallest batch it guards isn't conservative — it's theater. Fix the shape (rate, not count), not the number.

## 🟡 WHAT IT MEANS

Every absolute-count guard hides a minimum batch size. Name it, prove the guard fires there, or the guard is decoration.

## ⚪ WHAT'S IN IT FOR YOU

Guards that actually catch the failures they were built for — no more real weak slots passing through a rule that looked healthy because it could never speak.

## 🟨 HOW TO APPLY / HOW TO USE

1. When designing a guard, state the smallest input size it must handle.
2. Build the calibration table: historical cases × guard verdict — every known-bad case must fire, every known-clean must stay silent.
3. If the table shows structural silence, change the shape (rate/share/form), not just the threshold number.
4. Name the guard's limits honestly (a weak fold can mean executor shortfall, not misinjection — the review separates them).

## 🔗 HOW IT CONNECTS

- **COUSIN** → SN-01466 — write-the-guard-test-before-the-patch (guard fidelity; this names the scale-invariance dimension)
- **COUSIN** → SN-0939 — tests-that-cant-fail-are-theater (the theater family; this names the constructional variant)
- **REFINES** → SN-01535 — surgical reverification (mechanical rules over prose; this is the guard-design application)

## 🧭 KEY DECISIONS / PRINCIPLES

- Structural silence is not a correct skip — it is a guard that cannot fire.
- The fix for a scale-blind guard is a different shape (rate), never just a lower number.
- Every guard names its minimum-fire batch size with a calibration table as proof.

## 🟾 PROOF / PROVENANCE

~~~json
{
  "event": "weak-slot re-route guard v2 design (dispatch tick t0700, 2026-10-17)",
  "found": "old rule (>=2 weak briefs) structurally silent on single-brief batches; t0682 (1/1 weak) passed through by construction",
  "fixed_in": "weak-slot-guard-criterion-t0700-lane5.md — S(B) = weak/|I(B)|, FIRE iff >= 1/2; calibration table strictly better on the record (t0675, t0682 blind spots now fire)",
  "receipt": "twelve-lane-receipts/t0700-lane5.md (two-case proof, re-derived at action time)",
  "logged": "lesson-injection-log.jsonl utc-grouped batches; learning-events-2026-10-17 hour 11 (CANDIDATE 559)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Applies to guards over variable-size batches. The 1/2 threshold is a fitted constant (named in the spec's falsifier); the shape claim (rate > count for scale-invariance) is the durable part. The retrospective-timing limit holds: the weak-brief classification needs the executor's fold, which lands after execution — the guard fires retrospectively, before the NEXT batch's briefs go out.

## ➜ NEXT ACTION / SUCCESS CONDITION

The dispatcher's adoption diff (in weak-slot-guard-criterion-t0700-lane5.md) lands in the night-dispatcher LESSON INJECTION block; future guard briefs carry the minimum-fire-batch-size proof by default.
