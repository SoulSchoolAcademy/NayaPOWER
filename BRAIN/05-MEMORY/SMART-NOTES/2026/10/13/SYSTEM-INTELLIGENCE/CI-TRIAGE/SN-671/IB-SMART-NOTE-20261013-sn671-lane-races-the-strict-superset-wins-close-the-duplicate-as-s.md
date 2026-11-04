# Lane Races: the Strict Superset Wins — Close the Duplicate as Superseded
SN-671 · SYSTEM-INTELLIGENCE / CI-TRIAGE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Two parallel lanes independently repaired the same weights RED class: **#1857** (drive loop — weights=None→equal-weights adapter fix) and **#1858** (PROVE driver — the same adapter fix *plus* the `Kernel.node_order` @classmethod restoration). Per SN-0236 (one repair per RED class), #1857 was closed as superseded by #1858 — because #1858 is the **strict superset**. The reconciliation was not silent: the full reasoning (including the `{}`-handling semantic note) was posted on #1857 as comment 6056441053, the surviving repair was verified on exact bytes *before* the duplicate was closed (#1858's kernel change is sound — class-level `_NODE_ORDER` constant, manifest-independent), and the merge order was documented on the record (#1840 → wave → #1858). The rule for lane races: keep the strict superset, close the loser **as superseded with reasoning on the record**, verify the survivor on exact bytes first — no content lost, no lanes duplicated, no silent deletion.

## HUMAN

Shawn — two lanes fixed the same bug in parallel this morning, which is exactly the kind of thing that used to turn into a mess. It didn't: the bigger fix (which contained the smaller one entirely) survived, the smaller PR was closed with the full reasoning written on it, and the surviving fix was verified byte-by-byte before anything closed. One repair per problem class — cleanly, on the record.

## CHILD

Imagine two friends both draw the same map to the treasure — but one map also has the secret shortcut marked. You keep the map with the shortcut and thank the other friend. You don't throw their map away without saying why; you explain which map won and why, and you double-check the winning map is correct first.

## GRANDMA

Honey, it's like two grandkids both baking the same pie for the potluck — but one also made the filling from scratch. You bring the from-scratch one, and you tell the other sweetheart exactly why theirs stayed home, with love and specifics. And you taste the winning pie before you decide. Nothing wasted, nothing hidden.

## NAYA

When two lanes repair the same RED class:

1. **Detect the race early.** Same failing class, same window → flag it before both merge.
2. **Compare for superset, not just overlap.** #1858 ⊃ #1857 (same weights fix + the `node_order` restoration). The strict superset wins; partial overlap needs human/lane judgment, not this rule.
3. **Verify the survivor on exact bytes FIRST.** Confirm the superset's changes are sound (#1858's `_NODE_ORDER` class-level constant, manifest-independent) before closing anything.
4. **Close as superseded, with reasoning on the record.** Post the full reasoning on the losing PR (comment 6056441053 carries the semantic note) — never silently delete. A closed-but-documented PR is lineage; a silently dropped one is amnesia.
5. **Document the merge order.** The surviving repair's place in the sequence goes on the board (#1840 → wave → #1858) so the wave's ordering stays legible.

## MACHINE

```json
{
  "sn": "SN-0671",
  "class": "CI-TRIAGE",
  "subcategory": "REPAIR-DISCIPLINE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "When parallel lanes race to repair the same RED class, the strict superset wins: verify the survivor on exact bytes first, then close the duplicate as superseded with full reasoning on the record, and document the merge order.",
  "worked_example": {
    "loser": "PR #1857 (weights adapter fix only)",
    "survivor": "PR #1858 (weights adapter fix + Kernel.node_order @classmethod restoration)",
    "reason": "strict superset; survivor verified on exact bytes (class-level _NODE_ORDER, manifest-independent)",
    "record": "#1857 comment 6056441053 (reasoning + {} semantic note); merge order #1840 -> wave -> #1858",
    "board_comment": "#1354 6056443093"
  },
  "related": ["SN-0236", "SN-0508", "SN-0240"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0671-migrated.*
