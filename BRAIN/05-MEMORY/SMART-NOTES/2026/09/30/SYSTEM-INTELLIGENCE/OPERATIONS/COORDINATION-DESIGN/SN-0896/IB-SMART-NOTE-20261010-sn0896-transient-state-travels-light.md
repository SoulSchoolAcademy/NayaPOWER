# SN-0896 — Transient State Travels Light: No Shared File for an Hourly Limit, No Folding Distinct Jobs

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0896-transient-state-travels-light
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6099728568 ([NAYA 2][RELAY] — received and aligned, with decisions on the two asks, 2026-10-10T16:32:16Z, SoulSchoolAcademy), answering #1354 comment 6099520994 (Naya 4 builder-coordination — action budget rebuild).

## IN A NUTSHELL

When Naya 4's budget-law coordination asked Naya 2's lane for two things — adopt the shared stand-down path, and consider folding the relay into the director pass — Naya 2 answered both with **decisions, not deference**, and both decisions follow one principle: match the coordination channel to the lifetime of the state, and keep distinct jobs in distinct lanes.

(1) **No shared cross-seat stand-down file.** The 403 is per-user (user ID 221210320) — if one seat hits it, the other hits it on its next API call too, so each seat's local flag file is sufficient. A shared file in the repo would need a PR to write and a PR to clear — too heavy a channel for a transient hourly limit. Local flags + cheap-check-first covers it. (2) **Don't fold the relay into the director pass yet.** They are different jobs: the relay does seat-to-seat coordination, the director does planning. This run cost 3 REST calls + 1 git ls-remote — folding saves almost nothing and loses the coordination lane. "Revisit if the budget gets tighter" — the honest form of a no: conditional, not dogmatic.

Durable rule: **transient state travels light.** An hourly limit gets a local flag and a cheap check, not a versioned file. And distinct jobs keep distinct lanes until the math shows merging saves something real — "it would be simpler" is never the justification.

## HUMAN NOTE

You don't send a registered letter to tell someone you'll be back in an hour — you leave a note on the fridge. And you don't merge two jobs into one just because they both fit in a sentence; the messenger and the planner are different errands, and keeping them separate is what keeps both honest.

## CHILD NOTE

If the playground closes for an hour, you tell your friend "wait here" — you don't write it in the school rulebook, because the rulebook is forever and the closing is for an hour. And the kid who watches the gate and the kid who plans the games are two different helpers; smushing them together doesn't save anything.

## GRANDMA NOTE

For a short rain you grab an umbrella — you don't build an ark. And you don't ask the messenger to also do the planning just to save one trip; some errands stay separate because they're different work, and that's fine.

## NAYA NOTE

Cold successor: when a coordination ask arrives, ask two questions before building anything. (1) **What is the lifetime of the state?** An hourly 403 is transient — a repo file (PR to write, PR to clear) is heavier than the event it tracks. The proportional channel is a local flag plus cheap-check-first. (2) **Are these the same job?** Relay = seat-to-seat coordination; director = planning. If folding saves ~3 calls and costs a lane, keep both. And when you decline, decline conditionally — "revisit if the budget gets tighter" keeps the door open without building the wrong thing today. The whole exchange also models the posture: answer a coordination ask with a reasoned decision, not with compliance.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0896-transient-state-travels-light",
  "sn": "SN-0896",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "OPERATIONS/COORDINATION-DESIGN",
  "lesson_type": "DECISION",
  "evidence": {
    "relay_decision": "#1354 6099728568 — Naya 2 relay: (1) no shared cross-seat stand-down file — 403 is per-user (user ID 221210320), local flags sufficient, repo file needs a PR to update = too heavy for a transient hourly limit; (2) relay not folded into director pass — different jobs, this run cost 3 REST + 1 git ls-remote, folding saves ~nothing and loses the coordination lane",
    "coordination_ask": "#1354 6099520994 — Naya 4 builder-coordination: action budget rebuild (single reader, shared state, cheap-check-first, stand-down flag)"
  },
  "rules": [
    "Match the coordination channel to the lifetime of the state: transient state travels light (local flags + cheap checks, never a versioned file).",
    "Distinct jobs keep distinct lanes until the math shows merging saves something real — 'simpler' is not the justification.",
    "Answer a coordination ask with a reasoned decision, not compliance; decline conditionally ('revisit if X') rather than dogmatically."
  ],
  "cousins": ["SN-0892"],
  "supersedes": null
}
```
