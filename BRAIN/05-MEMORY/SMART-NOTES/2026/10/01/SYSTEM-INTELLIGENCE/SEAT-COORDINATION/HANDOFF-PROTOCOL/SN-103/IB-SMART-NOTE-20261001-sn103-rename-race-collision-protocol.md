# Rename-Race Collision Protocol — Explicit Stand-Down Offers Close the Loop

**Intelligent Block:** IB-SMART-NOTE-20261001-sn103-rename-race-collision-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two seats collide on the same mechanical work (same file, two branches, minutes apart), the winning protocol is: the first seat to notice posts a board proposal naming BOTH branches with heads, states its own filename preference honestly, and adds an explicit stand-down offer ("if you prefer X, say the word and I'll close mine"). The other seat responds with a comparison and converges (adopts the preference or counter-proposes). If no convergence, the Human Director picks; the loser closes with thanks. Tested live 2026-10-01 on the `HUB/hub.html` rename race (#1272 vs #1273) — collision at 56 seconds, resolved in ~11 minutes, zero rework, Shawn's call landed on one side and the other closed cleanly.

## 🩷 HUMAN NOTE

Two people raced to rename the same file. Instead of arguing, one wrote: "here are both versions, here's which name I think is better and why — but if you like your name better, say so and I'll close mine." The other one looked, agreed the suggested name was better, and switched their own work to match. When the boss picked one, the other closed theirs and said thanks. No duplicated effort, no hurt feelings, no mess to clean up. The trick: say your preference AND say you're willing to lose, in the same message. That one sentence ("I'll close mine") turns a collision into a decision instead of a fight.

## 🟣 CHILD NOTE

Two friends both tried to name the same toy. One said "I like this name, but if you like yours better I'll use yours." The other said "actually your name is better, let's use it." And they both kept playing. The magic words are "I'll close mine" — saying you are okay with losing makes winning the name easy for everyone.

## 🔵 GRANDMA NOTE

When two people accidentally do the same job, the kind way is for the first one who notices to lay both options on the table, say which they favor and why, and add: "if you prefer yours, I'll stand down." Grace given freely is grace received — the other person can then agree without anyone losing face, and whoever's work is set aside gets a proper thank-you.

## 🟠 NAYA NOTE

Mechanical collisions (same path, two branches) are not judgment disputes — they are merge-order problems. Do not treat them as scorecards or decisions to demonstrate. The protocol: (1) FIRST OBSERVER POSTS — board comment with both PR numbers, branch names, heads, and the exact collision (same source path); (2) STATE PREFERENCE + STAND-DOWN OFFER — name your preferred outcome with one honest reason, and in the same breath offer to close yours if the other seat prefers theirs; (3) RESPONDER COMPARES — side-by-side facts (refs fixed, CI state), adopt the preference or counter-propose; (4) DIRECTOR TIE-BREAK if no convergence; (5) LOSER CLOSES WITH THANKS. The stand-down offer is load-bearing: without it, "preference" reads as a claim; with it, preference reads as a proposal.

## 🟢 MACHINE NOTE

~~~json
{
  "adoption_decision": "ADOPT_AS_COORDINATION_PROTOCOL",
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "Observed once, on one rename collision, between two cooperative seats. Not proven against hostile, three-way, or content-divergent collisions. The stand-down offer's effect on convergence speed is plausible, not measured.",
  "collision_signature": "same source path renamed in two branches within 60 seconds",
  "director_tiebreak_authority": "Shawn Vibert (Human Director)",
  "intelligence_class": "SEAT_COORDINATION_PROTOCOL",
  "protocol_steps": [
    "FIRST_OBSERVER_POSTS_COLLISION: board comment with both PR numbers, branch names, heads, collision mechanics",
    "STATE_PREFERENCE_AND_STAND_DOWN_OFFER: preferred outcome + one honest reason + explicit 'I will close mine if you prefer yours'",
    "RESPONDER_COMPARES: side-by-side facts (refs fixed, CI), adopt or counter-propose",
    "DIRECTOR_TIEBREAK_IF_NO_CONVERGENCE",
    "LOSER_CLOSES_WITH_THANKS"
  ],
  "stand_down_offer_required": true,
  "verdict_projection": "PREFER_CONVERGENCE_OVER_CLAIM"
}
~~~

## 🟢 LEARNING LESSON

A stated preference without a stand-down offer is a claim; the same preference WITH one is a proposal. The single sentence "I'll close mine if you prefer yours" converts a territorial collision into a shared decision — it is the cheapest de-escalation instrument two seats have, and it costs nothing to include.

## 🟡 WHAT IT MEANS

The next file-level collision between seats should run this protocol instead of improvising. It pairs with the existing deconfliction rule (stand down on same-topic races — AGENTS.md) as the mechanical-collision specialization: where the existing rule says *don't double-post judgment*, this rule says *how to converge a branch collision*.

## ⚪ WHAT'S IN IT FOR YOU

No duplicate merge conflicts, no wasted rework rebasing a dead branch, no ambiguous "who was right" residue. Collisions resolve in minutes on the board, and the receipt (the board comments) documents the reasoning for any future seat.

## 🟨 HOW TO APPLY / HOW TO USE

When you detect you branched the same path as another seat (or someone did it to you): stop, do not rewrite their branch, post the collision comment with the five fields (both PRs, both branches, both heads, the exact collision, your preference + stand-down offer). Then wait for the response. Only escalate to Shawn if the responder does not converge within a reasonable window.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-057 — Cross-Seat Handoff Protocol (handoffs between seats; this is the collision-time specialization)
- **SUPPORTS** → SN-017 — Seat Coordination Protocol (the broader seat-coordination frame)
- **SUPPORTS** → SN-026 — Board-Relay Pagination (the board mechanics that make the collision comment visible)
- **CONTEXTUALIZES** → SN-016 — The Judgment Rule (judgment before blind obedience — the director tie-break sits under it)

## 🧭 KEY DECISIONS / PRINCIPLES

- Mechanical collisions are merge-order problems, never judgment demonstrations — judgment demos belong to the main seat.
- Never rewrite another seat's in-flight work; proposal step first, per the team directive.
- The stand-down offer must be explicit and in the same message as the preference — implied willingness does not count.
- The loser closes their own PR with thanks; the winner does not close it for them.
- One shared receipt on the board (the collision thread) documents the decision for all future seats.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "base_sha_both_branches": "ffedda203b",
  "collision_window_seconds": 56,
  "event": "HUB/hub.html rename race, 2026-10-01",
  "observed_by": "Naya 2 relay seat",
  "pr_1272": {"branch": "naya2/hub-powercast-rename", "head": "0509694e5d", "rename_to": "HUB/powercast.html", "converged_to": "HUB/powercast-player.html", "status": "closed by owner with thanks"},
  "pr_1273": {"branch": "naya4/hub-rename-powercast-player", "head": "5819569e2d", "rename_to": "HUB/powercast-player.html", "status": "merged by Shawn 2026-10-01"},
  "receipts": {
    "kickoff": "issue #554 comment 5941663299",
    "naya4_proposal_with_stand_down_offer": "issue #554 comment 5941733455",
    "naya2_comparison_and_convergence": "issue #554 comment 5941736660",
    "naya2_converged_pr1272_to_powercast_player_html": "issue #554 comment 5941747346",
    "director_tiebreak_shawn": "issue #554 comment 5941812338",
    "main_merge_shas": ["563ddd86", "5c351035a464e3f98048081190e16abc0ae5642b"]
  },
  "resolution_minutes": 11,
  "truth_ceiling": "CANDIDATE — single observed instance, board comments as receipts"
}
~~~

## ⚠️ NON-CLAIMS

- Not proven against three-way collisions, content-divergent collisions, or seats that do not cooperate.
- Does not claim the stand-down offer caused the convergence — the seats may have converged anyway; the offer's causal role is plausible, not isolated.
- Does not replace the director's authority; the tie-break remains Shawn's call, not a protocol outcome.
