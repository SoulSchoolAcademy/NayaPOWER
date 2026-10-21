# SN-0407 — The Cross-Lane Review Habit: share the link, ask for the score

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0407-cross-lane-review-habit
- **Truth state:** CANDIDATE (Shawn's directive, 2026-10-05; not yet ratified in his words)
- **Scope:** PRIVATE (Team Naya operating code)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Whenever a lane is working on something substantive, they share the link on the team board (#1354) and ask the other lanes for input: what do you think, what value or intelligence can you add, what do you scorecard this, and why isn't it a ten? This is a standing habit, not a one-time request. No lane builds in isolation when a second pair of eyes could catch what the first missed.

## HUMAN NOTE
Think of it like a kitchen where every chef tastes each other's dish before it goes out. You're cooking your part, but before you serve it, you hand the spoon to the other chefs and ask: what do you think? What's missing? What would make this a ten? They might catch the overseasoning you can't taste anymore because you've been standing over your own pot too long. That's what the lanes do for each other — share the work early, get the input, make it better before it's final.

## CHILD NOTE
When you're building something cool with your friends, don't hide it until it's done. Show them while you're building and ask: what do you think? How can we make it even better? What would make it a perfect ten? Your friends will see things you can't see because you're too close to your own work.

## GRANDMA NOTE
Dear, it's simple: when the team is working, they show each other the work while it's still warm and ask "what do you think, how do we make this the very best it can be?" Nobody works in a lonely corner. Everybody helps everybody, and everything comes out better for it.

## NAYA NOTE
This operationalizes the falsification role across lanes. The builder proposes, the auditor falsifies, but the habit generalizes it: ANY lane can request input on ANY substantive work, and the request names the artifact link plus four explicit questions (opinion, additive intelligence, scorecard, gap-to-ten). It pairs with the 554-trail rule (log everything) and the sign-in/out law (state, not just events) — this adds the review layer: work is not just logged, it's tasted. First modeled 2026-10-05: Naya 4 posted the cold-graph diagnosis to #1354 (comment 6005745450) requesting lane falsification and scoring before building the repair.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0407",
  "slug": "cross-lane-review-habit",
  "truth_state": "CANDIDATE",
  "directed_by": "Shawn Vibert",
  "directed_at": "2026-10-05",
  "directive_words": "share the link anything you're doing with the team on the 1354 say hey what do you think do you have any value or intelligence to add what do you scorecard this why is it not a ten and then you guys make a habit of that",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE",
  "pairs_with": ["SN-0399", "SN-0400", "SN-0351", "554-trail-rule"],
  "ritual": {
    "surface": "#1354",
    "artifact": "link to the work",
    "questions": ["what_do_you_think", "what_intelligence_can_you_add", "scorecard_this", "why_not_a_ten"],
    "rule": "no_substantive_build_without_lane_input_opportunity"
  },
  "first_modeled": "#1354 comment 6005745450"
}
```
