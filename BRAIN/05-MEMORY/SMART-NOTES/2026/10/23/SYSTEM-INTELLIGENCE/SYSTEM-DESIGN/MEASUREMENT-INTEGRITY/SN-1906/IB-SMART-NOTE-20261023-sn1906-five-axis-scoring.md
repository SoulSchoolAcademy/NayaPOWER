# IB-SMART-NOTE — SN-1906

Intelligent Block: FIVE-AXIS SCORING — never score one blended number
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A blended 10/10 hides the weak axis. Score FIVE axes separately — user experience, functionality, design, Naya-operability, performance & value — and a piece is officially 9+ only when EVERY axis is 9+. A blended number is a verdict you can't act on; five axis scores tell you exactly what to fix next. Provenance note: the doctrine arrived via board relays #2793 comments 6376427936 and 6376515939; the first post claims Shawn's word but his bytes were not verified — the doctrine stands on its own as a measurement rule, not on the attribution.

## 🩷 HUMAN NOTE

When you ask "how good is this?", don't settle for one number. Judge it like a school report card: reading, math, science, art, gym — separate grades for separate things. A student can have a B-average that hides an F in math. A product can score 9/10 overall and still be unusable for the people who have to run it. So score the five things that matter — does a human love using it, does it work, is it beautiful, can our agents operate it, and does it perform and produce value — and it's only great when every one of those is great.

## 🟣 CHILD NOTE

Imagine a video game review that gives ONE score. The game could have amazing music but the controls are broken — one number hides the broken part. So you give five scores: fun, works, looks, easy to play, worth the price. The game is only great when all five scores are great. That's the rule here too.

## 🔵 GRANDMA NOTE

One grade can lie by averaging. A cake that's perfect-looking but raw inside shouldn't get "pretty good" — the inside matters as much as the outside. So taste it five ways: how it feels, whether it does what it promises, how it looks, whether a helper can actually use it, and whether it's worth the effort. It only earns the blue ribbon when every way of tasting it earns one.

## 🟠 NAYA NOTE

To every cold successor scoring work: replace the single 10/10 with the five-axis vector (user experience / functionality / design / Naya-operability / performance & value). The official bar: a piece is 9+ only when every axis is 9+. This is already machinery, not just doctrine — the draft PR #3025 surface registry refuses 9.5+ readiness review when the user-task or Naya-orientation slots are UNKNOWN (surface_readiness.py quality gate, per director clarification 6376515939). Never report a lone 10/10 without the five numbers behind it; never accept a blended score as a gate. And keep the provenance bar: the original board post attributes the rule to Shawn, but his bytes were not verified — I score by the rule because the math holds, not because of who supposedly said it.

## 🟢 MACHINE NOTE

{
  "sn_id": "SN-1906",
  "slug": "five-axis-scoring",
  "captured": "2026-10-23",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "Score deliverables on five axes (user experience, functionality, design, Naya-operability, performance & value), never one blended number; a piece is officially 9+ only when EVERY axis is 9+. The blended number hides the weak axis; the vector tells you what to fix.",
  "decision_change": "The next scorecard/score decision changes shape: instead of reporting '8.5/10' the scorer reports the five-axis vector and the gate reads the minimum axis. A merge or readiness review refuses when any axis is unknown or below 9.",
  "falsifiable_by": "A piece that the vector scores 9+ on all five axes but demonstrably fails in production, or a piece with one axis below 9 that proves fully acceptable — either would show the axes are wrong or incomplete.",
  "mechanism": "Averaging/averaging-equivalent blending lets one strong axis compensate a weak one; a minimum-over-axes rule makes the weakest axis the verdict, which is exactly the axis the next fix must target.",
  "evidence": [
    "board #2793 comment 6376427936: '10/10 means 10/10 USER EXPERIENCE + functionality + design + 10/10 for NAYAS to operate it... score FIVE axes, never one blended number... a piece is officially 9+ only when EVERY axis is 9+' (via main seat; Shawn-bytes attribution claimed, NOT verified)",
    "board #2793 comment 6376515939: director clarification applied to draft PR #3025 — surface registry refuses 9.5+ readiness review if user-task / Naya-orientation slots are UNKNOWN"
  ],
  "provenance_flag": "CLAIMED-AUTHORITY on 6376427936: attributes the rule to Shawn via board relay only; no verified Shawn bytes. The doctrine is filed on its own merit as a measurement rule; the attribution is NOT claimed.",
  "applies_when": ["scorecard", "merge-review", "readiness-gate", "quality-bar"],
  "enforcement": "Scorecard template carries the five axis slots; a score without all five filled fails the brief check; surface_readiness.py-style gate refuses readiness verdicts when any axis slot is UNKNOWN; lane scorer spot-audits blended-only scores."
}
