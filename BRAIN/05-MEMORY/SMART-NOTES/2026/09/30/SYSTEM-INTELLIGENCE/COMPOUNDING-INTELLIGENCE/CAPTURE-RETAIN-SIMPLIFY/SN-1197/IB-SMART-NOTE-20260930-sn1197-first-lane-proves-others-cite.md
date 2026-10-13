# One Lane Proves on a Shared Tip Move; Subsequent Lanes Cite, Carry, and Record — Zero Duplicated Proofs on One Delta

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1197-first-lane-proves-others-cite
**Smart Note:** SN-1197
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the main tip moves, every lane's wave must absorb it — but only one lane needs to prove the delta. First lane proves; subsequent lanes cite the proof, record their carry, and move on. Four lane-runs proving the same merge is four times the cost with zero additional truth.

## HUMAN NOTE

On 2026-10-13, PR #2524 ("Naya/mission state", docs/ledger-only, Shawn's own sync branch, merged 14:39:55Z as `34338065eb9793c33cf273b62e1b109aa1d35808`) moved the tip mid-wave-69 and was met by four lane-runs in one rotation:

- wire 14:39Z proved the T-09 carry;
- verify 14:45Z proved merge faithfulness (true 2-parent merge, merge_sha == live ref);
- build 14:40Z / 14:49Z and wire 14:50Z did NOT re-prove — they recorded-carry-and-cited instead.

Zero duplicated proofs on one delta. This is the win pattern: the first lane to meet the tip move proves it with bytes; every lane after that cites the proof by comment ID, states its carry, and keeps its wave budget for unproven work.

Rule: **first lane proves, subsequent lanes cite.** If the proof isn't on the board when your wave arrives, you prove. If it is, you cite it by ID — never re-run a verdict someone already established on the same bytes.

## CHILD NOTE

When the team gets a new piece of news, one person should check it carefully. Everyone else should trust that check and write down that they saw it — not check it all over again.

## GRANDMA NOTE

One person reads the fine print for the whole family; the rest just confirm they've heard the answer. Re-reading the same page four times helps no one.

## NAYA NOTE

The team maximizes inside the action budget, and duplication is disrespect to the budget. A shared tip move is a shared event: exactly one proof exists per (delta × claim). The carry proof for each lane is (comment-id of the proof) + (your lane's carry statement) + (next unblocked work). If the existing proof is incomplete — wrong head, wrong claim, stale tip — that is not "cited"; you re-prove the gap, and say which gap you re-proved.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "rule": "first_lane_proves_subsequent_cite",
  "coordination": {
    "on_shared_tip_move": "exactly one lane proves each (delta, claim) with bytes",
    "later_lanes": "cite proof comment-id + record carry + continue",
    "reprove_condition": "proof on different head, different claim, or stale tip"
  },
  "win_pattern": "WP-48",
  "failure_family": "F5",
  "master_nodes": ["CONNECT", "VERIFY", "ACT"]
}
~~~

## 🟡 WHAT IT MEANS

Coordination is a proof economy: spend the proving budget once per delta, and spend every other action on something unproven.

## 🧾 PROOF / PROVENANCE

- Learning event WP-48 (F5), board #2175 comment 6148613655 (2026-10-13T15:05:26Z): "one-lane-one-receipt on a shared tip move … Zero duplicated proofs on one delta. Rule: first lane proves, subsequent lanes cite."
- #2524 relay watch 6148177492 (14:43:57Z): merge proof bytes — true 2-parent merge, P1 == prior tip, merge_sha == live ref
- night-shift-wire 6148151839 + night-shift-verify sign-outs ~14:45Z; night-shift-build 6148134777; second wire pass 14:50Z — cite-and-carry, no re-proof

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Applies to proof claims on identical bytes within one wave window. Does not permit citing a proof whose head, claim, or tip has moved past the evidence — a moved target is a new proof obligation.

## ➜ NEXT ACTION / SUCCESS CONDITION

Lane briefs carry the one-lane-one-receipt rule; any wave that re-proves an existing board proof on the same bytes names why the existing proof was insufficient.
