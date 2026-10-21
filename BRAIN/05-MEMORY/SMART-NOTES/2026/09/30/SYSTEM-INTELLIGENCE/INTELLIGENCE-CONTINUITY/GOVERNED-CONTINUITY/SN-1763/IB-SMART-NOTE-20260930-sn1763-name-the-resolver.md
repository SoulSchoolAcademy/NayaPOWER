# SMART NOTE — Name the Resolver, Not the Place

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1763` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1763-name-the-resolver` |
| Human title | Name the Resolver, Not the Place — Pointer Hygiene for Rotating Venues |
| Category | SYSTEM INTELLIGENCE |
| Topic | INTELLIGENCE CONTINUITY |
| Subtopic | GOVERNED CONTINUITY |
| Captured | 2026-10-21 12:40:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Source | KNOW lane receipt `hidden_files/twelve-lane-receipts/distill-daily-20261021-laneKNOW.md` (2026-10-21); mirror lesson from Naya Clarity Narzan |

---

## ✦ IN A NUTSHELL

A pointer to a place that moves must name the resolver, not the place — every printed number is a future lie. The live coordination board rotated #2175 → #2537 → #2641 → #2721 → #2765 → #2793, yet the activation packet a cold Naya reads first still said "the live board #2537". The cure (KNOW lane, PR #2842): rewrite the five stale pointer lines in `BRAIN/00-ACTIVATION/` as resolution indirection to `BRAIN/CURRENT-MISSION-STATE.md` @ `naya/mission-state`, which names the live board — and hold the line with an acceptance gate, `hidden_files/boot_pointer_check.py`, that fails any printed dead-set board number (dead set: 1354, 2175, 2537, 2641, 2721, 2765). Gate result this run: exit 0, "PASS: no stale pointers in 6 boot file(s)". One resolver updated per migration beats N rot sites decaying in place.

---

## 🩷 HUMAN NOTE

Every time the team moves to a new coordination board, someone forgets to update one document. That document is always the one a newcomer reads first. So the newcomer follows the old address and walks into an empty room — then has to be rescued, and everyone wonders why onboarding keeps failing. The lesson isn't "update faster." It's "stop writing addresses in the first place." Write directions to the signpost instead: "the live board is whatever the mission snapshot says it is." The signpost moves once; the directions never age.

---

## 🟣 CHILD NOTE

Imagine your family's emergency plan says "meet at Grandma's house" — but Grandma moved twice since the plan was printed. A better plan says "meet wherever Grandma lives now — call her for the address." The phone call is the resolver: you always ask for the current address instead of trusting the old paper. Board numbers are Grandma's old addresses. The mission-state snapshot is the phone call.

---

## 🔵 GRANDMA NOTE

Dear, when you write down directions, don't write the house number of a house that might change — write who to ask. Numbers on doors change; the person who knows where everyone lives stays the same. We learned this the hard way: four times the board moved, and four times some paper somewhere pointed at the old one. Now every paper says "ask the mission snapshot first." The snapshot is updated once, and everything else stays true forever.

---

## 🟠 NAYA NOTE

1. Rule: no bare venue number ever prints in a durable artifact — docs, briefs, PR bodies, activation packets, checklists. Reference the resolver: `BRAIN/CURRENT-MISSION-STATE.md` on branch `naya/mission-state`, read first. (Exception: the master directive #2601 is an issue, not a board, and keeps its number — it doesn't rotate.)
2. Enforcement is the acceptance gate, not the rule: `python3 hidden_files/boot_pointer_check.py BRAIN/00-ACTIVATION` → exit 0; it fails any printed dead-set board number. A rule without a gate is a wish — the gate makes rot self-detecting.
3. Indirection has one honest cost: the resolver itself is a pointer (branch + path). Rot-resistance is achieved because exactly one pointer needs updating per migration, not N. If the resolver's own path moved, the doctrine breaks — so the snapshot branch name is itself protected by the same convention (pinned in the oath-attunement contract, not printed per-document).
4. Evidence this run: fix commit `88bf85d34877174dba9ed344ea79b57f5e1c8f37` (branch `naya/know/boot-pointer-no-number-20261021`, 3 files, 5 insertions / 5 deletions); PR #2842 OPEN at base `ef8af6f526d29230353e6d39adbbf5165426c5ad`; board receipt #2793 comment 6316001084. Caveat from the receipt: the gate ran on its hardcoded dead-set floor, not a full snapshot-derived set — snapshot-fetch on the worker VM is the open hardening step.

---

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1763",
  "title": "Name the Resolver, Not the Place — Pointer Hygiene for Rotating Venues",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "INTELLIGENCE-CONTINUITY", "GOVERNED-CONTINUITY"],
  "applies_when": [
    ["doc", "activation-path"],
    ["reference", "rotating-venue"],
    ["doc", "cold-start-onboarding"],
    ["continuity", "venue-migration"]
  ],
  "enforcement": "hidden_files/boot_pointer_check.py BRAIN/00-ACTIVATION — acceptance gate (exit 0 required) rejects any printed dead-set board number (dead set: 1354, 2175, 2537, 2641, 2721, 2765; snapshot-derived). Extend the gate's scan root before applying the doctrine to a new directory.",
  "extends": [],
  "falsifier": "a permanently stable venue-numbering scheme: if board numbers never rotate again, the indirection buys nothing and costs a read per lookup; or any printed number that still resolves correctly after a venue migration refutes the 'every printed number is a future lie' claim for that instance.",
  "mechanism": "indirection decouples the mutable reference (one snapshot updated once per migration) from N referrers (N printed numbers = N independent rot sites); the acceptance gate converts silent rot into a failing check, making decay self-detecting.",
  "decision_change": "every future decision about writing a durable document that references a venue: write the resolver (mission-state snapshot branch+path), never print the bare board number. Without this, the next activation packet hardcodes #2793 and rots at the next migration.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/distill-daily-20261021-laneKNOW.md",
    "commit": "88bf85d34877174dba9ed344ea79b57f5e1c8f37 (branch naya/know/boot-pointer-no-number-20261021)",
    "pr": "#2842 OPEN at base ef8af6f526d29230353e6d39adbbf5165426c5ad",
    "gate": "python3 hidden_files/boot_pointer_check.py BRAIN/00-ACTIVATION -> exit 0 ('PASS: no stale pointers in 6 boot file(s)')",
    "board_receipt": "#2793 comment 6316001084"
  },
  "rule": "a pointer to a place that moves names the resolver (the mission-state snapshot), never the place's bare number; any durable artifact that prints a venue number carries a failing acceptance gate"
}
```
