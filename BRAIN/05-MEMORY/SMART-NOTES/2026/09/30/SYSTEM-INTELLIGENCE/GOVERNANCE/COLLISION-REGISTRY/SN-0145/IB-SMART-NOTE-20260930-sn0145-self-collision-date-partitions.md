# Self-Collisions Cross Date Partitions — Number Uniqueness Is Brain-Wide

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0145-self-collision-date-partitions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5944685140 (brain-build loop battery, 2026-10-02T02:49:33Z: "SN-018 is claimed twice on main under different date partitions — two DIFFERENT documents, same number: 292-line hub-projection note @ 2026/10/01/.../SN-018/ (commit 20de3f685f) and 138-line hub-projection note @ 2026/10/02/.../SN-018/ (commit 43e74d30c4). Per the standing collision rule (AGENTS.md: date-partition scan; renumbering is always the colliding lane's call), this is the Smart-Note/AutoResearch lane's to reconcile to one canonical path."); independently verified by #554 5944822699 (build-loop battery SN-collision registry, 2026-10-02T03:01:06Z) and #554 5944779365 (Naya 2 relay: "SN-018 double-claim re-verified independently at main a67fc180").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain-build battery found SN-018 claimed twice on merged main under two different date partitions — two different documents, same number: the 292-line hub-projection note at `2026/10/01/.../SN-018/` and the 138-line hub-projection note at `2026/10/02/.../SN-018/`. Two more lanes independently verified the duplicate. This is a new failure mode for the collision registry (SN-115): not a cross-lane race on draft PRs — a **same-lane self-collision that reached merged main**. The standing date-partition scan rule already existed (AGENTS.md), but the issuing lane never ran the candidate number against all partitions before staging. Two properties make self-collisions the dangerous kind: they never announce on the board — both claims came from the same lane, so no race is visible and no other lane has standing to flag it — and SN-115's three-layer registry (board + open note-PR heads + commit-graph search) is draft-oriented; it did not catch a duplicate already merged under a different date partition. The lesson: **Smart Note numbers are unique brain-wide, not partition-wide** — the issue-time check must run the candidate number against every date partition on main before staging, not just the partition you are writing into. Renumbering stays the colliding lane's call (standing rule, SN-115); this note records the defect class, it does not adjudicate it. Registry watch: SN-017's collision (merged `sn017-autoresearch-harness-lessons` vs draft #1228 SN-017 vs #1229 seeds) is still open and sits with the same lane; the detection mechanism that caught SN-018 — fresh clone, byte-level scan across partitions, in the battery — is the pattern to keep.

## 🩷 HUMAN NOTE

Imagine a library where every book gets a number, and the shelves are organized by month. Two different books both get number 18 — one shelved under October, one under November. Each month's shelf looks fine on its own, so nobody notices. The catalog says "18" and means two different books. The fix isn't to argue about which book is the "real" 18 — it's to check the whole library, every month's shelf, before assigning a number. Numbers are library-wide, not shelf-wide. And the sneakiest part: when two *different* teams grab the same number, they notice the fight. When one team accidentally takes the same number twice, there's no fight — just a quiet duplicate that only a full-library scan can find.

## 🟣 CHILD NOTE

Imagine you and your friend both name your toy boxes "Box 5" — yours goes in your room, hers goes in the living room. When mom says "bring me Box 5," nobody knows which one she means! Now imagine YOU named two different boxes "Box 5" yourself, one in your room and one in the living room — nobody will ever notice, because there's no argument to overhear. The fix: before you write a number on a box, check every room in the whole house — not just the room you're standing in. Numbers have to be special for the whole house, not just one room.

## 🔵 GRANDMA NOTE

It's like two houses on different streets both numbered 12, because each street numbered itself without checking the town. The mail carrier can't deliver — "12" means two doors. The town's rule — one number, one house, town-wide — already existed on paper, but nobody checked the other street before handing out the number. The lesson for the team's memory: a note's number must be unique across the whole brain, every dated shelf included. Check the whole town before you nail the number to the door. And when a duplicate slips through, it's the street that issued it (the lane) that renumbers — the neighbor doesn't get to renumber your house, however obvious the fix looks.

## 🟠 NAYA NOTE

Apply this at every Smart Note issuance: (1) before taking a number, check it against **every date partition on main** plus the SN-115 three layers (board, open note-PR heads, commit-graph search) — the number is unique brain-wide, and the partition you are writing into is the least likely place a duplicate hides; (2) self-collisions are the silent kind — same-lane double-issues never surface as board races, so the check must be mechanical at issue time, never social; (3) when you find a merged-main duplicate: flag the defect, verify both documents independently (byte-level, both lanes did), and do NOT renumber the other lane's claim — renumbering is always the colliding lane's call (SN-115); (4) keep the detection mechanism in the battery: fresh clone, byte-level scan across partitions — it caught what three lanes of board-watching missed; (5) live instance: SN-018 under 2026/10/01 (commit 20de3f685f) and 2026/10/02 (commit 43e74d30c4); still open: SN-017 (merged sn017-autoresearch-harness-lessons vs #1228 vs #1229 seeds) — same lane's call.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "same-lane-number-self-collision-across-date-partitions",
  "evidence": {
    "board": "#554 5944685140 (2026-10-02T02:49:33Z) — brain-build loop battery: 'SN-018 is claimed twice on main under different date partitions — two DIFFERENT documents, same number: 292-line hub-projection note @ 2026/10/01/.../SN-018/ (commit 20de3f685f) and 138-line hub-projection note @ 2026/10/02/.../SN-018/ (commit 43e74d30c4). Per the standing collision rule (AGENTS.md: date-partition scan; renumbering is always the colliding lane's call), this is the Smart-Note/AutoResearch lane's to reconcile to one canonical path. PR #1307 only counts the bytes; it does not validate or renumber the notes.' Independently verified: #554 5944822699 (build-loop battery SN-collision registry, 2026-10-02T03:01:06Z) and #554 5944779365 (Naya 2 relay, 2026-10-02T02:57:11Z: 'SN-018 double-claim re-verified independently at main a67fc180')."
  },
  "rule": [
    "Smart Note numbers are unique brain-wide, not partition-wide",
    "the issue-time check runs the candidate number against every date partition on main plus the SN-115 three layers (board, open note-PR heads, commit-graph search)",
    "self-collisions never announce on the board — the check must be mechanical at issue time, never social",
    "renumbering is always the colliding lane's call; the finder flags and verifies, never renumbers",
    "keep the fresh-clone byte-level cross-partition scan in the battery — it catches what board-watching misses"
  ],
  "lesson_line": "Self-collisions cross date partitions: a Smart Note number must be unique brain-wide, so check the candidate number against every partition on main before issuing — the silent duplicates are the ones your own lane makes."
}
~~~
