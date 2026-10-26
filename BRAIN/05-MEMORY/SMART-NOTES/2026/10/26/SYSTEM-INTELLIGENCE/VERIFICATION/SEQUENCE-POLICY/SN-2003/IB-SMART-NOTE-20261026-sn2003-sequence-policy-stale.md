Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A registry cure is not complete until the sequence allocator advances past the highest occupied Smart Note number. The 2026-10-26T04:45Z registry cure (commit 5ca29bd5, parent e047de80) re-stamped SN-1870/71/72/74 through canonical machinery — captures created, page_hash from page bytes, content_hash from captures, seal 26c4d0ae to c6d54607, door-obligation defects 9 to 1 — yet left next_sequence at 1874 while 1874 was occupied. At the cured tip, Kernel Tests failed exactly on the allocator invariant: test_sequence_policy_advances_after_sn002 and test_sequence_policy_advances_after_sn003 (5,639 passed / 2 failed / 18 skipped / 6 xfailed at 5ca29bd5). Registry cured, sequence stale, tests red. Rule: a cure, renumber, or claim repair lands only when next_sequence advances past max occupied SN in the same landing, and the cure is not declared complete on registry/seal alone.

## 🩷 HUMAN NOTE

Shawn — the registry cure worked, and the tests still went red, and both things are true at once. The cure fixed the four mis-registered notes and their seal — but it never moved the counter that hands out the next number, so the counter still points at a number that is already taken. The test suite catches exactly that: the next number must be past every number already used. So a cure is only finished when the counter moves with it, in the same landing — not "registry fixed, counter later." Check the counter, not just the seal, before calling a cure done.

## 🟣 CHILD NOTE

Imagine a ticket machine that hands out numbers. Four tickets were printed wrong, so the staff reprinted them correctly — great. But nobody moved the machine's counter forward, so it still thinks the next ticket is a number that is already taken. The checker at the door notices: "that number is already used!" and stops everything. The fix is simple: whenever you reprint tickets, move the counter past the last ticket you used, in the same job. Don't call the job done until the counter has moved.

## 🔵 GRANDMA NOTE

The library fixed four misfiled cards and re-stamped the drawer — but forgot to move the "next card number" marker past the last card used. So the next card filed would collide with one already in the drawer, and the audit rightly flags it. The lesson: fixing the cards is only half the job. Moving the marker past the highest card used, in the same visit, is the other half. A repair that leaves the marker behind is a repair that will collide again.

## 🟠 NAYA NOTE

This is the allocator half of the SN-1870/71/72/74 mis-registration, distinct from the registry half already cured at 5ca29bd5 and from SN-0801 (a counter bump masking conflicts) and from the renumber note (update registry + capture + sequence_policy in the same commit as a renumber). Here the mechanism is narrower: the cure re-stamped occupied numbers without moving the allocator, so the invariant next_sequence > max occupied SN broke and the two sequence-policy tests failed at an otherwise cured tip. Decision-change (triage e): the next time a registry cure, renumber, or claim repair lands, the deciding seat must advance next_sequence past max occupied in that same landing and must not declare the cure complete on seal/registry alone. Falsifiability (triage f): if test_sequence_policy_advances_after_sn002 / past_sn003 pass at a tip where next_sequence is at or below max occupied, the allocator assertion is not what is claimed; if advancing next_sequence past occupied does not turn those two tests green, another cause dominates and this note is wrong. Mechanism (triage g): the allocator invariant itself — tests assert the next free ID is unambiguous, and a cure that changes the occupied set without moving the allocator breaks that invariant by construction. Cousins: SN-0801 (counter bump masks conflicts), the renumber lesson (sequence_policy updated in the same commit), SN-1868 (an edit-path gap in a recompute that also left a seal stale — same shape: half a recompute is not a recompute).

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-2003-sequence-policy-stale",
  "lesson": "A registry cure, renumber, or claim repair is not complete until next_sequence advances past the highest occupied SN in the same landing. The 2026-10-26T04:45Z registry cure (commit 5ca29bd5, parent e047de80) re-stamped SN-1870/71/72/74 (captures created, page_hash from page bytes, content_hash from captures, seal 26c4d0ae -> c6d54607, door defects 9 -> 1) but left next_sequence at 1874 while 1874 was occupied, so Kernel Tests failed at the cured tip on test_sequence_policy_advances_after_sn002 and test_sequence_policy_advances_after_sn003 (5,639 passed / 2 failed / 18 skipped / 6 xfailed at 5ca29bd5). Rule: never declare a cure complete on registry/seal alone; advance the allocator with it.",
  "applies_when": ["claim", "sequence-policy", "registry", "cure", "renumber", "verification", "kernel-tests", "failure:sequence-policy-stale"],
  "enforcement": "Kernel Tests test_sequence_policy_advances_after_sn002 and test_sequence_policy_advances_after_sn003 must be green at the cure tip; a cure landing is not declared complete until next_sequence is verified past max occupied SN. Cure owner: dispatcher source/core repair plus the filing-path guard implementation, which must advance next_sequence past max occupied before a cure is declared complete.",
  "evidence": [
    "Board #3066 comment 6408592914 (read-only triage, 2026-10-26T04:58:50Z): Kernel Tests FAIL 5,639 passed / 2 failed / 18 skipped / 6 xfailed at tip 5ca29bd5; both failures test_sequence_policy_advances_after_sn002 / past_sn003, asserting allocator advances beyond occupied 1874 while next_sequence still 1874 - the counter/claim collision behind the SN-1870/71/72/74 mis-registration",
    "Board #3066 comment 6408442537 (registry cure landed 5ca29bd5, parent e047de80): captures created, page_hash from page bytes, content_hash from captures, seal 26c4d0ae -> c6d54607, door checker defects 9 -> 1",
    "Shared-state named_failure_modes_new entry SEQUENCE-POLICY-STALE (2026-10-26T05:08Z tick, tip 5ca29bd5): verify check next_sequence must advance past max occupied SN after the claim-before-author cure lands; cure owner dispatcher source/core repair + filing-path guard implementation",
    "Cousins, not duplicates: SN-0801 (counter bump masks conflicts), renumber lesson (registry + capture + sequence_policy updated in the same commit as a renumber)"
  ]
}
```
