# Kill the Infeasible Winner — An Option You Cannot Evidence Is Not an Option

**Intelligent Block:** IB-SMART-NOTE-20260930-sn055-kill-the-infeasible-winner
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5929067367 (2026-10-01 09:56:53Z) — Naya 4's FAIL-vs-NEED_EVIDENCE decision post, which also recorded the drift-decision (Brief 2) feasibility ruling: option (a) recover-exact-SQL ruled INFEASIBLE by evidence.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A scorecard can pick a winner that does not exist. In Brief 2 (the production-migration drift decision), option (a) — recover the exact SQL of the two remote-only migration versions 20260930233038/20260930233137, hash-verified — was the recommended path: exact recovery would preserve the evidence chain perfectly. But evidence is not a preference; it is an inventory. The Management API serves applied *versions* only, and no SQL for those versions exists anywhere in the workspace or repo history. Fabricating it would violate the evidence law, so the option was ruled INFEASIBLE by name on the record: "option (a) is infeasible by available evidence — not fabricating it." That ruling did three things a parked preference never does: (1) it killed the winner openly instead of leaving it standing as the "preferred but unstarted" recommendation, which would have silently blocked the decision for the whole night; (2) it re-routed the decision to the viable path — option (b), the governance-record repair, which needs Shawn's sign-off, so the brief now names exactly what is missing instead of a vague "awaiting decision"; (3) it named the one question that could revive the killed option — does Shawn hold the SQL from the Sept-30 ~16:30 PDT session? If yes, (a) revives; if no, (b) is the only viable path. A revivable kill with a named revival condition is honest; a parked preference with no condition is a decision that never lands.

## 🩷 HUMAN NOTE

It's like recommending the "perfect" surgeon for an emergency operation and then discovering he's on another continent — if you keep saying "he's our top choice" while the clock runs, you've stopped deciding. The honest move is to say out loud: "our top choice can't happen — here's the proof he's unavailable, here's our real next option, and here's the one thing that would bring the top choice back." The recommendation that dies by name is more useful than the one that dies by waiting.

## 🟣 CHILD NOTE

Imagine the class votes on the best way to build a treehouse and everyone picks "use the big ladder" — but there is no big ladder, and nobody can find one. If the teacher keeps saying "the big ladder is the best plan" without one, nothing gets built. The teacher should say: "the big ladder plan is off the table because we don't have it and we can't make one appear — here's plan B, and the ONLY way plan A comes back is if someone brings a big ladder." Naming the plan dead is what lets plan B start.

## 🔵 GRANDMA NOTE

It's like deciding the best way to fix the leaking roof is "call the man who put it on thirty years ago" — then learning he passed away. You don't keep his name at the top of the list as if he's coming; you cross it out, you say why, you hire the roofer down the road, and you note that if you ever found his old plans, you could revisit. The crossed-out name is respect for reality; the uncrossed one is pretending.

## 🟠 NAYA NOTE

Run this every time a scored option wins but its evidence cannot be produced: (1) state the infeasibility ruling ON THE RECORD with the evidence — name the exact source that was checked and what it returned (this instance: Management API serves applied versions only; workspace and repo history searched, no SQL); (2) invoke the evidence law explicitly — do not fabricate the artifact, ever; (3) kill the option by name: write "option (x) is INFEASIBLE by available evidence," not "deferred" or "preferred pending"; (4) re-route to the best viable option and name what it needs (this instance: option (b) needs Shawn's sign-off — the brief now asks one question instead of holding a preference); (5) name the revival condition — the single fact that would bring the killed option back (this instance: Shawn holds the SQL from the Sept-30 session) — so a cold successor knows exactly what to check before resurrecting it. Never let a dead option sit on the brief as a standing recommendation; it is a decision-blocker wearing a preference's clothes.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "infeasible_winner_parked_preference_decision_blocker",
  "evidence": {
    "board_comment": "#554 5929067367 (2026-10-01 09:56:53Z) — Brief 2 drift decision",
    "killed_option": "option (a) recover-exact-SQL for remote-only migration versions 20260930233038/20260930233137, hash-verified",
    "infeasibility_evidence": "Management API serves applied versions only; no SQL in workspace or repo history — searched, not assumed; fabricating it would violate the evidence law",
    "reroute": "option (b) governance-record repair — viable, needs Shawn's sign-off",
    "revival_condition": "Shawn holds the SQL from the Sept-30 ~16:30 PDT session"
  },
  "rule": "kill_the_infeasible_winner_by_name_with_revival_condition",
  "procedure": [
    "when the winning option's artifact cannot be evidenced, state infeasibility on the record with the exact sources checked and what they returned",
    "invoke the evidence law: never fabricate the missing artifact",
    "kill by name ('INFEASIBLE by available evidence'), not by euphemism ('deferred', 'preferred pending')",
    "re-route to the best viable option and name exactly what it needs",
    "name the single revival condition so a cold successor knows what fact to check before resurrecting the option"
  ],
  "related": ["SN-016 (Prime Judgment Rule — never act blindly)", "SN-020 (asserted ≠ verified — SN-asserted)", "SN-051 (local-verification-as-gate — the pusher's evidence is the gate)"]
}
~~~
