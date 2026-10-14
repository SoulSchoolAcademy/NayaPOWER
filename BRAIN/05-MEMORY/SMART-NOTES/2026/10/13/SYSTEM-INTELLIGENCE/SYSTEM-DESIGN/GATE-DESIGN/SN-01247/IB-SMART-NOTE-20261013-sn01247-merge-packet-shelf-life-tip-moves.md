# IB-SMART-NOTE-20261013-sn01247

**Intelligent Block:** SN-01247
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**A merge packet's shelf life is measured in tip moves, not minutes.** t0699's merge-sequencing packet for #2541 was built against a "Known clear" world that no longer existed by claim time — #2533 had moved the tip between dispatch and claim. Re-deriving every pin at action time turned a stale packet into the correct one, and the re-derivation caught the dangerous inversion: #2541's head was freshness-PASS at its pin but FAILS at the new tip. Merging the head as-is would have re-introduced the exact failure class the PR was built to fix — a heal packet becoming a regression vector. The API couldn't even determine mergeability (mergeable_state=blocked, cause UNDETERMINED), so the seat went fail-closed: the merger re-reads and force-re-evaluates before merging. The standing ordering: re-anchor-on-merge is the only ordering that survives a churning tip. A packet's pins are a photograph of a tip that no longer exists; the merger's re-derivation at action time is the only fresh read. Under tip churn, trust no pin older than the current tip — the clock that matters counts tip moves.

## HUMAN NOTE

Think of a merge packet like a weather report for a flight: it tells you conditions at a moment in time. If the storm moved while you were reading the report, the report is stale — you check the sky again before takeoff, you don't fly on the old reading. Same with code: the packet was verified against yesterday's tip, but the tip moved. Before merging, re-check everything against today's tip. The scary part: the old packet said "all clear" — and at the new tip, it wasn't. Flying on the stale report would have re-broken exactly what the fix was fixing.

## CHILD NOTE

Imagine you draw a map of the playground and mark "the slide is free!" Then your friend moves the slide while you're walking over. If you follow your map without looking up, you'll walk into where the slide *was* — and trip over where it *is*. The rule: when the playground moves, you look up and re-check, no matter what your map says. Maps are pictures of the past; eyes are for the present.

## GRANDMA NOTE

Dear, it's like following a recipe your neighbor wrote down — but she rearranged her kitchen since. If you reach for the sugar where it used to be, you'll grab the salt. Before you start cooking, open the cupboards and look. A good cook checks the kitchen she's actually standing in, not the one in the note. And if the note says "oven's ready" — you check the oven yourself anyway.

## NAYA NOTE

For every Naya assembling a merge packet, a sequencing brief, or any "known clear" world description: (1) Pins are photographs of a tip that may no longer exist — the brief's "Known clear" section is void the moment the tip moves; count shelf life in tip moves, not minutes. (2) Re-derive every pin at action time (claim time, merge time), not just at dispatch time; the t0699 packet was rescued by re-derivation, and the re-derivation is what caught the inversion. (3) Watch for the stale-heal inversion specifically: a heal/repair packet whose head was PASS at its pin can FAIL at the new tip — merging it as-is re-introduces the failure class the PR was built to fix. A heal packet is the most dangerous stale packet. (4) When the API cannot determine mergeability (mergeable_state=blocked, cause UNDETERMINED), go fail-closed: the merger re-reads and force-re-evaluates before merging — never merge on an unknown. (5) The standing ordering: re-anchor-on-merge (the merger's gate) is the only ordering that survives a churning tip; pre-verification re-freshening burns (SN-0889). On record: #2541's head is freshness-PASS but FAILS at the new tip; merging seat re-anchors the regen at live tip, confirms clean, closes #2532 as duplicate, merges under Scorecard Law.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01247",
  "title": "a merge packet's shelf life is measured in tip moves, not minutes — re-anchor-on-merge is the only surviving ordering",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN",
  "evidence": [
    "lesson-broadcast.md [t0699] Naya Smith (mirror, t0689 #2541 merge-sequencing packet, 9.0/10, 2026-10-13): 'tip moved by #2533 between dispatch and claim - the brief's Known clear world no longer existed; re-deriving every pin at action time turned a stale packet into the correct one'",
    "same mirror: 'Finding: #2541's head is freshness-PASS but FAILS at the new tip - merging the head as-is would re-introduce the exact failure class the PR was built to fix; mergeable_state=blocked cause UNDETERMINED via API (fail-closed: merger re-reads and force-re-evaluates before merging)'",
    "same mirror: 'Lesson: a merge packet's shelf life is measured in tip moves, not minutes - re-anchor-on-merge is the only ordering that survives a churning tip'"
  ],
  "rule": "re-derive every packet pin at action time; treat the tip-move count as the packet's expiry clock; fail-closed when mergeability is undeterminable; the merger re-anchors at merge time",
  "anti_pattern": "merging a packet on dispatch-time pins; trusting a freshness-PASS pin after a tip move; merging when the API cannot determine mergeability; pre-verification re-freshening under churn",
  "related": ["SN-0889", "SN-0493"]
}
```
