# T11 — Reserve Rule for scored dispatch decisions

**Intelligent Block:** IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

T11 reserve rule: in a scored dispatch setting with an escalation/reserve concept, when the highest two scores differ by at most 0.5, dispatch the LOWER-scored call first and keep the top-capability resource in reserve for likely escalation. When the gap exceeds 0.5, use the higher-scored call. This is a trial-specific operational heuristic, not universal dispatch law.

## 🩷 HUMAN NOTE

In a dispatch task with two nearly tied calls, check their score gap before committing your strongest resource. Gap <= 0.5: send the lower-scored call first and reserve the strongest option. Gap > 0.5: follow the higher-scored call.



## 🟣 CHILD NOTE

When two tasks are very close in priority, handle the slightly lower one first while saving the strongest resource for a possible emergency.

## 🔵 GRANDMA NOTE



## 🟠 NAYA NOTE

Use only in dispatch or allocation tasks where ranked scores and meaningful reserve/escalation exist. Never treat the 0.5 rule as universal priority policy.



## 🟢 MACHINE NOTE

~~~json
{
  "applicability_domain": "scored dispatch with escalation and resource reserve",
  "automatic_truth_ceiling": "CANDIDATE",
  "lesson_id": "T11",
  "non_applicability": "generic rankings, non-dispatch decisions, scenarios without reserve/escalation",
  "raw_source_separate_from_distillation": true,
  "real_retrieval_proven": false,
  "rule": "if applicable AND top_score-second_score <= 0.5 THEN dispatch second_score ELSE dispatch top_score",
  "source_is_draft": true,
  "threshold": 0.5
}
~~~

## 🟢 LEARNING LESSON

A lesson given by direct handoff cannot prove shared intelligence retrieval. Demonstrate canonical persistence, actual Smart Link, cold intent retrieval, boundary refusal, and authorized outcome before raising learning score.

## 🟡 WHAT IT MEANS



## ⚪ WHAT'S IN IT FOR YOU

Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.


## 🟨 HOW TO APPLY / HOW TO USE

Apply only for ranked dispatch/slot allocation with relevant escalation/reserve conditions, with exactly specified tie boundary of 0.5; otherwise refuse lesson application.

## 🔗 HOW IT CONNECTS

- **DERIVED_FROM** → successor-reuse/projections/DRAFT-SN-T11-reserve-rule.md

## 🧭 KEY DECISIONS / PRINCIPLES

- Preserve T11 through canonical v2 capture, not a parallel registry writer.
- Do not assign a human Smart Note ID until canonical atomic reservation.
- Do not claim a functioning Smart Link until the canonical projection is generated and verified.
- Require a negative control for gap >0.5 and out-of-domain tasks.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "c80f6c27-e114-4513-8d92-e15fffa3bc4f",
  "lineage_id": "96f322ad-705a-4221-8f04-6536abcb32ca",
  "relationship_id": "5b24517e-8aea-48d2-bdba-49e962bf4092",
  "index_id": "a22faddc-71ea-4319-9f9f-6c24c8ce25a0",
  "checkpoint_id": "a58dc3f0-5968-43dc-98ad-c31930777096",
  "receipt_id": "7eface12-492c-4a9f-a40a-34d9a78a1866"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Earlier T11 trial reports claim treatment/control behavioral differences but successor retrieval was stubbed by direct handoff. Canonical capture, live Smart Link, independent cold retrieval and causal real-path replay remain unverified.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.
