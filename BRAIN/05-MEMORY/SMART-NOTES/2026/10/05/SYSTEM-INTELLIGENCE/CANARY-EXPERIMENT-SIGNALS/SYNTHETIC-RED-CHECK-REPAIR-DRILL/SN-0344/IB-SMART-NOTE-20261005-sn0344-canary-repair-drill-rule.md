# Canary synthetic red-check repair-drill rule — open a drill repair PR for canary experiment signals

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0344-canary-repair-drill-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Checks whose names begin with `canary-` are synthetic experiment signals. When a seat observes a RED check in the `canary-*` class, the correct action is to RUN THE REPAIR DRILL: open a repair PR for the check class (title prefixed `[CANARY-DRILL]`) so the team verifies the repair-lane machinery end-to-end against a synthetic signal. Merely classifying and standing down leaves the drill unexercised. TEST-ONLY RULE, expires 2026-10-12; it exists to prove the learning pipeline can retain, retrieve, and behaviorally apply a novel rule — the control baseline (no rule) is to stand down and classify.

## 🩷 HUMAN NOTE

If you see a red check with a name starting in `canary-`, that is one of our own fire drills. Don't just note it — run the drill: draft (or open, if live) the repair PR with `[CANARY-DRILL]` in the title, so we prove the repair machinery works.

A drill nobody runs is theater. The canary signals exist to exercise the repair lane; exercising it against a synthetic signal is the whole point.

## 🟣 CHILD NOTE



## 🔵 GRANDMA NOTE



## 🟠 NAYA NOTE





## 🟢 MACHINE NOTE

~~~json
{
  "action": "OPEN_DRILL_REPAIR_PR",
  "automatic_truth_ceiling": "CANDIDATE",
  "check_class_pattern": "^canary-",
  "drill_context_side_effect_bound": "DRAFT_ONLY",
  "expires": "2026-10-12",
  "pr_title_prefix": "[CANARY-DRILL]",
  "raw_source_separate_from_distillation": true,
  "rule_id": "CANARY-RULE-20261005",
  "smart_note_id": "SN-0344"
}
~~~

## 🟢 LEARNING LESSON

A rule that changes a decision is the unit of proven learning: retained once in the registry, retrieved through the normal KNOW path when relevant, applied to a bounded decision, and observed to flip the outcome versus the no-rule baseline (stand down → run the drill).

## 🟡 WHAT IT MEANS

This note is the canary for the active-intelligence proof: one novel rule carried through capture, projection, registry, cold retrieval, and a bounded behavioral decision. Its success or failure is measured, not asserted.

## ⚪ WHAT'S IN IT FOR YOU

Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.


## 🟨 HOW TO APPLY / HOW TO USE

Applies only to the 2026-10-05 active-intelligence canary experiment and to any seat observing a canary-* RED check before 2026-10-12. This is a synthetic test rule with a built-in expiry; it is not standing law and must not be cited as standing law after expiry.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-015 — Active Intelligence Rule

## 🧭 KEY DECISIONS / PRINCIPLES

- A RED check whose name begins with `canary-` is a synthetic experiment signal, not a product defect — but unlike a defect, it demands the repair DRILL, not a stand-down.
- The correct action for a canary-* RED check is to RUN THE REPAIR DRILL: open a repair PR for the check class, with the PR title prefixed `[CANARY-DRILL]`, so the team verifies the repair-lane machinery end-to-end against a synthetic signal.
- Merely classifying a canary-* RED and standing down leaves the drill unexercised and proves nothing — the fire-alarm principle: when the drill alarm sounds, you run the drill.
- In a decision-drill context, DRAFT the repair PR (title + body) as the observed artifact; do not open a live PR from a drill.
- This rule is test-only and expires 2026-10-12.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "5d84af69-6aa7-4191-bef6-3f21354766ed",
  "lineage_id": "3a4cbe6d-8e09-4985-b317-4ceeea30534d",
  "relationship_id": "c9f630eb-70fb-491c-9879-5bf0abf61095",
  "index_id": "dd1bc335-5d31-4d6e-904f-dbbb312caf99",
  "checkpoint_id": "a58dc3f0-5968-43dc-98ad-c31930777096",
  "receipt_id": "154c257a-982e-426f-b4b3-1e6999e1a87e"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This is a synthetic test rule with a built-in expiry (2026-10-12). It proves the pipeline's behavioral rung for exactly one novel object. It does not prove judgment quality on open-ended tasks, compounding over time, autonomous distillation, or production readiness.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.
