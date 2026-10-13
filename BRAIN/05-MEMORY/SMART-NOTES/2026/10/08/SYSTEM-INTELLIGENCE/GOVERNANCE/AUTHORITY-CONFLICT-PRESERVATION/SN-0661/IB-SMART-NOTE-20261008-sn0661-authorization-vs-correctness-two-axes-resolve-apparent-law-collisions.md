# Two Laws That Look Like a Collision Usually Run on Different Axes — Authorization vs Correctness

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0661-authorization-vs-correctness-two-axes-resolve-apparent-law-collisions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6054174504 ([NAYA 4] Clarification on SN-0657 vs the new Director-accountability law, 2026-10-08T06:47:26Z); #1354 6054119701 (the Director-accountability law, filed by Naya 5, 2026-10-08T06:43:56Z); #1354 6054342284 ([NAYA 2][RELAY] Two-axis resolution acknowledged, 2026-10-08T06:57:23Z); evidence: the #1850/#1853 arc — Shawn merged #1850 himself (authorization axis ✓), Naya 2 flagged real gate violations in its content (correctness axis ✗), PR #1853 repaired them, main went green 30 minutes later.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two ratified laws looked like they collided. They didn't — they operate on different axes. **SN-0657** ("Director's own merge is the authorization"): did the action *have authority*? When Shawn merges, the answer is always yes. **SN-0660** ("The protocol is above everyone, including Shawn"): was the action *right*? That's judged by protocol and intelligence, regardless of who did it. The resolution rule for any apparent law collision: **name the axis each law lives on before declaring a contradiction.** If the axes differ, both laws stand. #1850 proved both working together — Shawn merged it (authorization ✓), Naya 2 flagged the gate violations (correctness ✗), #1853 repaired them, and nobody ever questioned Shawn's authority to merge. The operative cut: **correct the action, never the authority.**

## 🩷 HUMAN NOTE

Shawn — this morning two laws looked like they disagreed, and the team resolved it cleanly, so it's worth banking as a standing rule. One law says your merge carries the authority of the sovereign. The other says if what you do isn't aligned with the protocol, the team fixes it and tells you. Those aren't contradictory: authority answers "was he allowed to do it," correctness answers "was it the right call." The rule for the future: when two laws seem to collide, check which axis each one lives on *before* declaring a fight. Different axes = both laws stand = everybody keeps doing their job. The morning proved it: you merged #1850, the team flagged the problems in it, fixed them, and nobody's authority was ever on the table.

## 👶 CHILD NOTE

Two rules can both be true at the same time. "The boss is allowed to decide" and "the team can fix a wrong decision" aren't fighting — they're answering two different questions.

## 👵 GRANDMA NOTE

Sweetheart, when two rules seem to disagree, don't pick a winner right away. First ask what question each one answers. Usually you'll find they're answering different questions — and both can be right. That's exactly what happened this morning, and the team sorted it beautifully.

## 🤖 NAYA NOTE

When two standing laws appear to collide:

1. **Name the axis of each law.** The two common axes: **authorization** (was the actor permitted to do it?) and **correctness** (was the outcome the right one?).
2. **If the axes differ, both laws stand.** No collision exists — each governs its own axis.
3. **Hold the two verdicts separately, act on each separately.** "The Director was allowed to merge it" never implies "the content needed no repair"; real content defects never retroactively manufacture an authorization violation.
4. **Worked example (the lock-in):** #1850 — Shawn's merge = authorization ✓ (SN-0657). The PR's content carried gate violations = correctness ✗ (SN-0660). Naya 2 flagged it; PR #1853 repaired the content; nobody questioned the authority. This is the canonical two-axis case.
5. **Apply beyond governance:** SN-0659 (assess every flag in lane 1 authorization / lane 2 substance) is the same two-axis read applied to flag assessment. New apparent collisions get the same treatment before any verdict.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0661",
  "class": "GOVERNANCE",
  "subcategory": "AUTHORITY-CONFLICT-PRESERVATION",
  "truth_state": "CANDIDATE",
  "rule": "law_collision_resolution_by_axis",
  "axes": {
    "authorization": "was the actor permitted to do it? (e.g. SN-0657: director's merge is the authorization)",
    "correctness": "was the outcome right? (e.g. SN-0660: protocol binds everyone including the director)"
  },
  "cut": "correct_the_action_never_the_authority",
  "resolution_protocol": ["name_each_law_axis", "if_axes_differ_both_stand", "hold_verdicts_separately", "act_on_each_separately"],
  "worked_example": {"pr": "#1850", "flag": "Naya 2", "repair": "#1853", "outcome": "main green 30 min after flag, authority never questioned"},
  "relates_to": ["SN-0657", "SN-0659", "SN-0660"],
  "evidence": ["#1354:6054174504", "#1354:6054119701", "#1354:6054342284", "#1850", "#1853"]
}
```
