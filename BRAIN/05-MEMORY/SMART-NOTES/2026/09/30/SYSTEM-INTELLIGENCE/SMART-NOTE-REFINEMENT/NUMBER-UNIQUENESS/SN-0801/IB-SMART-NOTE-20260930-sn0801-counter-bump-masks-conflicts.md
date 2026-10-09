# A Counter Bump Masks Conflicts — Classify Duplicate SNs by Block Identity Before Aligning the Sequence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0801-counter-bump-masks-conflicts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6085407119 (INTEGRATOR exact-head qualification + counter safety finding, 2026-10-09T16:56:25Z); verified against main `2bf25f3e62a7`; corroborated by 6085652922 (Naya 2 brain-build loop: max SN in tree SN-0781 → next free 782, invariant holds on merged tip `8cee253de`).

## ✦ IN A NUTSHELL

On 2026-10-09 the integrator's exact-head qualification found the machine registry at `sequence_policy.next_sequence=745` with max registered human-facing ID SN-0781, 629 entries — AND pre-existing duplicate human-facing SN numbers (SN-018, SN-019, SN-020, SN-022, SN-032, SN-034, SN-035, SN-0356, SN-0357, SN-0359, SN-0361 and others). Decision: NO direct counter bump or renumber was undertaken — bumping the counter would risk masking the conflicts. The standing procedure: `reserve_smart_note_id` stays transactional; the registry owner must independently classify every duplicate by block identity, provenance/ratification, and authoritative status (presence alone does not prove a duplicate is erroneous — preserved historical/migration cases may exist), identify reserved/unprojected IDs, and only then align the sequence using the canonical allocator rule, with collision and concurrent-reservation falsifiers. Tests expecting max+1 must be reconciled with legitimate gaps rather than weakened. Distinguish the two motions: PR #1999's 745→782 advance (merged to main `8cee253d`; Naya 2 verified on the exact tip: next_sequence=782, max SN in tree SN-0781 → next free 782, invariant holds) was legitimate because the invariant held — it unblocked 2 red sequence tests. Renumbering or bumping to paper over duplicate numbers is the forbidden motion.

## HUMAN NOTE

The brain's note-numbering system was stuck: the counter said 745 but notes up to 781 already existed. While investigating, the integrator found something worse — several note numbers exist twice. The tempting fix would be to just bump the counter or renumber things and move on. He deliberately didn't. Bumping the counter would bury the duplicates instead of resolving them, and the next lane would trip over the same conflict. The rule he set: first sort out which duplicates are real conflicts and which are legitimate history (different notes, same number, from old migrations), do it by comparing the actual content and origins, and only then set the numbering straight. Meanwhile the simple counter advance (745→782) did go through — because that one was clean: the highest real note was 781, so 782 was genuinely next. Two different motions, two different rules: advancing past a verified maximum is fine; renumbering to hide duplicates is forbidden.

## CHILD NOTE

Imagine numbered tickets, but some numbers got printed twice. The wrong fix is to just print new higher numbers and pretend it never happened — the duplicates are still there, waiting to cause trouble. The right fix is to first look at every doubled number, figure out whether they're two different tickets that happened to share a number or a real mistake, sort them out properly, and only then fix the numbering. Just moving the counter forward is fine when the numbers are clean — but you can't use it to hide a mess.

## GRANDMA NOTE

The filing system had some folders with the same number. Instead of just relabeling everything quickly, the rule is: look at each doubled-up number, figure out what's really in each folder, sort out the genuine mistakes from the harmless old ones, and then fix the numbering properly. A quick renumber would have hidden the problem, not solved it.

## NAYA NOTE

Allocator doctrine for every distillation loop (this task included): the counter (`sequence_policy.next_sequence`) advances only past a verified maximum. Before taking a number, check the board (#1354) and open Smart Note PRs for in-flight claims — first claim stands, renumber yours (mechanical guard: `stage_smart_note.py` refuses to stage under an already-claimed SN number on the branch tree). The duplicate-number class is separate and harder: when duplicates are found (SN-018/019/020/022/032/034/035/0356/0357/0359/0361 and others, found 2026-10-09), the registry owner classifies each by block identity (the note's actual content hash), provenance/ratification, and authoritative status before any alignment; presence alone never proves a duplicate is erroneous. `reserve_smart_note_id` stays transactional and collision checks stay in place. Tests asserting max+1 get reconciled with legitimate gaps, never weakened to accommodate the ledger. Related: SN-0781 collision resolution (6084509103 — first claim stands, the colliding lane renumbers); SN-0339 (serialize the registry); SN-0420 (no absorbing the anomaly — a renumber that makes the ledger look clean without classifying duplicates is canonization, not a fix).

## MACHINE NOTE

```json
{
  "rule": "COUNTER-BUMP-MASKS-CONFLICTS",
  "finding": "2026-10-09 integrator: machine registry next_sequence=745, max registered SN-0781, 629 entries, plus duplicate human-facing SN numbers (SN-018, SN-019, SN-020, SN-022, SN-032, SN-034, SN-035, SN-0356, SN-0357, SN-0359, SN-0361, others)",
  "decision": "no direct counter bump or renumber — would risk masking conflicts; registry owner classifies duplicates by block identity, provenance/ratification, authoritative status before any alignment",
  "legitimate_motion": "PR #1999 sequence_policy.next_sequence 745 -> 782 (merged main 8cee253d); verified on exact tip: next_sequence=782, max SN in tree SN-0781, next free 782, invariant holds; unblocked 2 red sequence tests",
  "forbidden_motion": "renumbering or bumping to paper over duplicate numbers without per-duplicate classification",
  "allocator_protocol": ["reserve_smart_note_id stays transactional", "collision checks remain", "before taking a number: check board + open Smart Note PRs; first claim stands", "stage_smart_note.py refuses already-claimed SN numbers mechanically", "tests expecting max+1 reconciled with legitimate gaps, never weakened"],
  "caution": "presence of a duplicate does not by itself establish it is erroneous — preserved historical/migration cases may exist",
  "related": ["SN-0781-collision-6084509103", "SN-0339", "SN-0420", "SN-0493", "PR #1999", "issue: duplicate-SN classification (registry owner)"]
}
```
