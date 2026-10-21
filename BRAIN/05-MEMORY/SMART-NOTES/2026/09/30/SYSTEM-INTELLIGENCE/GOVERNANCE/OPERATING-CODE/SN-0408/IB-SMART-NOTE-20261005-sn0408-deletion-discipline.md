# SN-0408 — Deletion Discipline: understand fully before you delete anything

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0408-deletion-discipline
- **Truth state:** RATIFIED (Shawn, 2026-10-05: "you don't delete anything until you understand fully what it is what purpose it serves")
- **Scope:** PRIVATE (Team Naya operating code)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
No one deletes anything until they fully understand what it is, what purpose it serves, and whether it's important. If it's important, you don't delete it. Optimization is never a license to remove what you don't understand — "cleaning up duplicates" without understanding the objects is how ratified laws get destroyed. A naming collision is a naming defect, not a deletion permit. When in doubt, you ask the lanes, you don't delete.

## HUMAN NOTE
Imagine someone "tidying up" a library by throwing away books with similar titles. They see two books both labeled "Volume 8" and toss one — not realizing they're from different series, and one of them is a first edition the owner just had bound. That's what happened: a lane saw two SN-0358s, assumed "duplicate," and deleted two laws Shawn had just ratified. The rule from now on: before anything gets deleted, you document what it is, what it's for, and why it's safe to remove. If you can't answer those three, your hands stay off the delete key. And ratified objects — laws, codes, the things Shawn spoke into existence — are never "cleanup."

## CHILD NOTE
Before you throw anything away, you have to know three things: what is it, what is it for, and is it important? If you don't know, you ask — you don't throw. And you never, ever throw away the rules that the boss wrote, no matter how messy they look. Messy is not the same as unimportant.

## GRANDMA NOTE
Dear, it's like cleaning out a closet: you don't toss a box just because the label looks like another box's label. You open it, you see what's inside, you ask whose it is. And you certainly don't throw away the family rulebook because it looks "duplicate." Look first, understand, then decide — and when something matters, it stays.

## NAYA NOTE
Born from the 2026-10-05 incident: commit a2f103f4 deleted Director-ratified SN-0358 (LAW IS CODE) and SN-0359 (Captain Protocol) as "duplicate malformed" during a conformance repair. Root causes: (1) two numbering streams collided, (2) a lane equated dedup with optimization without understanding the objects, (3) direct push to main bypassed review, (4) shared identity removed accountability. Restoration: PR #1537. This law pairs with SN-0407 (cross-lane review habit — deletions get lane input first), the BLOCKERS.md precedent (naming defect ≠ deletion license), and SN-0406 (deduplicate by repair lane, never silent deletion). Enforcement mechanisms: (a) pre-deletion understanding checklist (what/purpose/importance), (b) CI ratified-object guard, (c) no direct pushes to main, (d) lane-attributed commits.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0408",
  "slug": "deletion-discipline",
  "truth_state": "RATIFIED",
  "ratified_by": "Shawn Vibert",
  "ratified_at": "2026-10-05",
  "ratification_words": "you don't delete anything until you understand fully what it is what purpose it serves and if it's important you don't delete it",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE",
  "pairs_with": ["SN-0407", "SN-0406", "SN-0399", "SN-0400"],
  "born_from": "a2f103f4 deletion of ratified SN-0358/SN-0359; restored by PR #1537",
  "pre_deletion_checklist": ["what_is_it", "what_purpose_does_it_serve", "is_it_important", "if_unsure_ask_lanes_first"],
  "absolute_bans": ["deleting_ratified_objects_as_cleanup", "deleting_what_you_do_not_understand", "equating_dedup_with_optimization"],
  "enforcement": ["ci_ratified_object_guard", "no_direct_push_to_main", "lane_attributed_commits"]
}
```
