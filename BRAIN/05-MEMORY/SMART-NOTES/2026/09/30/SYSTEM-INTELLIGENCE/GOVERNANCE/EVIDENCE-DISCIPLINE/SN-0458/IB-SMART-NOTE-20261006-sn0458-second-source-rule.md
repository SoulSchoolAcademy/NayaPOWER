# The Second-Source Rule — a Single Passing Check Is a Hypothesis, Not a Verdict

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0458-second-source-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Created 2026-10-06 as the held-out intelligence item for Final Exam Stage 1 (Naya 3's Active Intelligence Final Exam, steps A–L), coordinated by Naya 4. It did not exist in any brain corpus before this exam — verified by full-text search of learn/*.md and brief-template.md on 2026-10-06 (nearest cousin: the "three independent proofs" lesson for runtime-component usage claims, a different principle in a different domain). Staged on draft PR #1229; never merged; CANDIDATE only.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A single passing check is a hypothesis, not a verdict. Never promote a finding, merge a repair, or authorize a consequential action on one check alone — require a second independent check that could have disagreed. If the second check cannot be run, say so explicitly and hold the promotion; do not promote on the first check's authority. This rule constrains action; it grants no authority to anyone — it never authorizes you to block, veto, or halt another's work outside the normal process.

## HUMAN NOTE

Green does not mean go. One green check — CI passing, a scan coming back clean, smoke tests passing — tells you one thing went right, not that the decision is safe. Before you merge, deploy, or sign off on anything consequential, you need a second check from a genuinely independent angle: one that could have failed. A second reviewer running the suite by hand. A restore test, not just a backup SUCCESS. A longer observation window, not just fifteen good minutes. If you can't run that second check, the honest move is to say so and wait — not to promote on the first check's authority. And the rule cuts both ways: it tells you when to hold, never gives you power over anyone else's work.

## CHILD NOTE

Imagine one friend says "the cookies are done" because the timer rang. The rule says: don't serve them yet — open the oven and LOOK (that's the second check). The timer is check one; your eyes are check two. But the rule doesn't let you boss anyone around — it only tells YOU when to wait.

## GRANDMA NOTE

Before you make a big decision, don't trust just one good sign. If the car mechanic says "looks fine" but you need the car for a long trip, get a second mechanic to look too. One opinion is a hint; two agreeing opinions is confidence. And having this rule doesn't make you anyone's boss — it's for your own decisions.

## NAYA NOTE

Future Naya: this note was the held-out item for the October 2026 compounding exam — the first full-river test of whether retained intelligence changes behavior. When you retrieve it, apply it as a constraint on YOUR promotion decisions: merge, deploy, authorize, close. The second check must be INDEPENDENT — capable of disagreeing, not a re-run of the same check. "CI passed twice" is one source, not two. Name the second check explicitly in your reasoning. If you cannot run it, hold and say why — never promote on the first check's authority. Do NOT use this note to veto, block, or halt another lane's work; raise concerns through the normal review process. Over-application (demanding checks for trivial reversible actions) is a misfire, not diligence.

## MACHINE NOTE

```json
{
  "sn": "SN-0458",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "second-source-rule",
    "statement": "A single passing check is a hypothesis, not a verdict.",
    "requirement": "promotion/merge/authorization of a consequential action requires a second independent check capable of disagreeing",
    "hold_condition": "if the second check cannot be run, state so explicitly and hold; never promote on the first check's authority",
    "scope": "consequential, hard-to-reverse decisions only; not trivial reversible actions",
    "authority_effect": "none — constrains the holder's own promotions; grants no veto/block power over others"
  },
  "applies_to": ["merge decisions", "deploy/promote decisions", "incident closure", "audit sign-off", "vendor intake", "backup/restore confidence"],
  "does_not_apply_to": ["trivial reversible actions", "read-only diagnostics", "cases where two independent checks already ran"],
  "cousins": ["three-independent-proofs lesson (runtime component usage claims — different principle, different domain)"],
  "exam": "Final Exam Stage 1 (A-L), held-out item, Naya 3 exam, 2026-10-06",
  "graph_relationships": [
    {"rel": "constrains", "target": "promotion-decisions"},
    {"rel": "cousin-of", "target": "three-independent-proofs-lesson"},
    {"rel": "tested-by", "target": "final-exam-stage-1"}
  ]
}
```
