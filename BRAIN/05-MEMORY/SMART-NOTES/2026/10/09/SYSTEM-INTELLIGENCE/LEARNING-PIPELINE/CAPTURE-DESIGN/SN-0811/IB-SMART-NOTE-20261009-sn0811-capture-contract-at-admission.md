# The Verification Bottleneck Is Capture Design — Lessons That Arrive Unverifiable Arrive DOA

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0811-capture-contract-at-admission
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6087139356 (2026-10-09).
**Provenance:** #1354 6087139356 ([NAYA 5 — learning-loop-watch], 2026-10-09T18:46:04Z); full shift log on #1713 (sign-in 6087025991, sign-out 6087134104). Related: SN-0340 (receipt discipline), SN-0240 (honest CI classification).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The learning loop's frozen queue finally drained: 36 lessons sat stuck for ~11 days, and this shift dispositioned all 36 — CANDIDATE 36 → 0. The breakdown is the lesson: 4 were honest "we tested it, the lesson didn't change anything" nulls. The other 32 were lessons that **could never have been tested at all** — no named task, no success measure, nothing to run against. Grading a test with no questions. The verification bottleneck was correctly diagnosed not as slow verifiers but as **capture design**: candidates arrived with no falsifiable contract, so verification couldn't be bolted on afterward. The fix is at admission: every future candidate arrives with a named task + a pre-registered success criterion + a machine check, or it is not admitted. An unverifiable capture is waste by design — it consumes verifier attention, decays in a frozen queue, and finally retires having taught nobody anything.

## 🩷 HUMAN NOTE

Shawn — remember the jar of 36 stuck lessons sitting frozen for eleven days? We finally emptied it. And the surprise: almost none of them were bad lessons. They were lessons nobody could ever grade — "learn this" with no way to check whether it was learned. The verifiers weren't slow; the lessons were un-testable. So we're fixing it where it starts: no lesson gets into the system without saying what it's supposed to do, how we'll know it worked, and what machine check proves it. If it can't be tested, it can't be trusted — and now it won't be admitted.

## 👶 CHILD NOTE

Imagine your teacher gives you homework that says "be good at math" — but never says what math, or what "good" means. You study for weeks. Did you do the homework? Nobody can tell. Now imagine the homework says "learn to multiply by 7, and I'll give you a quiz on Friday." That's a homework you can actually do. Lessons work the same way: if a lesson doesn't say what it does and how to check, it's homework nobody can grade — and the jar fills up with uncheckable homework forever.

## 👵 GRANDMA NOTE

Sweetie, it's like writing down a recipe that says "add spices until it tastes right" and handing it to someone who never tasted your cooking. They'll stir and worry and never know if they got it right — and eventually the recipe card just sits in a drawer. A recipe you can follow says "a teaspoon of salt, simmer ten minutes, the sauce should coat the spoon." The lesson's the same: a lesson that can't be checked is a recipe nobody can cook from. We now write the recipe with the taste-test built in.

## 🤖 NAYA NOTE

When capturing or admitting a learning-loop candidate:

1. **Require the falsifiable contract at admission, not at verification.** Three fields, all mandatory: (a) the named task the lesson changes behavior on; (b) the pre-registered success criterion; (c) the machine check that runs it. Missing any one → not admitted, no exceptions.
2. **Classify frozen candidates by contract failure, not content quality.** The 32 retired lessons weren't wrong — they were untestable: no named task, no success measure. Distinguish "tested, no effect" (honest null — keep the evidence) from "untestable by design" (retire; fix the capture).
3. **Watch the bottleneck, not the symptom.** 36 candidates frozen for 11 days looked like slow verification; it was un-verifiable input. If the queue grows again, diagnose the capture first.
4. **Record who did the disposition and under what authority.** The shift log surfaced the open question itself — no note on the feed naming the sorter or the permission. Disposition of the learning registry is a governed action: sign it.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0811",
  "class": "LEARNING-PIPELINE",
  "subcategory": "CAPTURE-DESIGN",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Verification cannot be bolted on after the fact: every learning candidate must arrive at admission with a named task, a pre-registered success criterion, and a machine check. A candidate missing any of the three is not admitted. A lesson without a falsifiable contract arrives DOA — it will freeze, decay, and retire having taught nothing.",
  "worked_example": {
    "frozen_queue": "36 candidates stuck ~11 days (CANDIDATE 36 -> 0 in one shift)",
    "disposition": "4 honest nulls (tested, no effect) + 32 retired (untestable by design: no named task, no success measure)",
    "diagnosis": "bottleneck was capture design, not verifier speed; fix at admission",
    "board_comment": "#1354 6087139356; shift log #1713 (6087025991 -> 6087134104)"
  },
  "related": ["SN-0340", "SN-0240"]
}
```
