# Same Number, Different Bytes Is a Fork, Not a Second Edition

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0176-cross-partition-content-fork
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5947400421 (SoulSchoolAcademy, 2026-10-02T07:30:28Z) — repair PR #1315 note flagging SN-018 existing in two date partitions (2026/10/01 and 2026/10/02) with *different* bytes; flagged for the owning seats to reconcile, no unilateral renumbering.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The collision registry (SN-033/115/169/171) resolves *lane-race* number claims — two lanes claiming the same SN number for different content. PR #1315's repair note exposed a different defect class: SN-018 exists under two date partitions (`2026/10/01` and `2026/10/02`) with *different bytes*. Nobody "claimed" a collision — the number re-appeared under a new date carrying divergent content, a silent content fork. The durable rule: a Smart Note's uniqueness key is the NUMBER across **all** partitions, not (number, date). A number re-appearing under a new date with different bytes is a collision, not a revision and not a second edition — revisions update the existing partition path; divergent content under the same number forks the note's identity, and every future reader resolving SN-018 lands on one of two different documents. So the staging discipline gains a cross-partition layer: before taking a number, verify it does not already exist under ANY date partition (byte-compare when it recurs); when a fork is found, flag-and-hold — the owning seats reconcile it, and no lane unilaterally renumbers (SN-115's no-unilateral-supersession discipline applies to forks too).

## 🩷 HUMAN NOTE

Shawn — the note registry found a new kind of collision: SN-018 exists in two different date folders with different content in each. That's not a revision; it's a fork — two different documents sharing one number, which breaks every future lookup of "SN-018." The fix is a fourth check before staging: a note number must be unique across *all* date folders, not just the one you're writing into. The fork is flagged for the owning lanes to reconcile; nobody renumbers unilaterally.

## 🟣 CHILD NOTE

Imagine two kids both writing "Page 18" at the top of their pages — but the pages are in different folders and say different things. When the teacher says "turn to page 18," nobody knows which page she means. The new rule: "Page 18" can only ever mean ONE page, no matter which folder it's in — and if it shows up twice, the kids who wrote it have to sort it out together; the teacher doesn't just erase one.

## 🔵 GRANDMA NOTE

It's like having two different recipes both labeled "Recipe 18" — one in Monday's folder and one in Tuesday's folder, with different ingredients. When someone asks for Recipe 18, which one do you give them? The team wrote this down so the rule is clear: a number can only ever point to one recipe, ever, in any folder — and when a double shows up, it's flagged for the people who wrote it to sort out, never erased quietly by someone else.

## 🟠 NAYA NOTE

Apply this to every Smart Note staging: (1) uniqueness is global — before taking a number, search ALL date partitions for that number, not just today's; (2) when the number recurs, byte-compare: identical bytes = harmless re-stage (skip per the script's idempotency); different bytes = a content fork, treat it as a collision under the registry, not a revision; (3) never resolve a fork by re-staging — flag it on #554 for the owning seats to reconcile, hold your own note on a free number in the meantime; (4) revisions belong on the existing partition path with explicit supersession notes, never under a new date with the same number and changed bytes.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "CROSS_PARTITION_CONTENT_FORK",
  "evidence": {
    "finding": "#554 5947400421 (2026-10-02T07:30:28Z, SoulSchoolAcademy) — 'SN-018 exists in two date partitions (2026/10/01 and 2026/10/02) with *different* bytes — duplicate-number collision for the owning seats to reconcile; no unilateral renumbering.'",
    "context": "surfaced during repair PR #1315 (05-MEMORY domain-count ledger 21→26 + index regen on current main tip 25268675), branch brain-build/index-domain-count-05memory-26 @ 5a81623d; --check clean (171 files), pytest 546 passed / 3 skipped / 0 failures, explicit non-claim of CI on the API-pushed SHA.",
    "related": "#1315 supersedes stale repair PRs #1251 and #1307 (closed unmerged, bytes stale after main moved +2) — instance of SN-042/SN-100 family, not staged as a separate note."
  },
  "rule": [
    "a Smart Note number is globally unique across all date partitions — uniqueness key is the NUMBER, not (number, date)",
    "same number + same bytes in another partition = harmless re-stage (idempotent skip); same number + different bytes = content fork, a registry collision, never a revision",
    "registry gains a cross-partition layer: search all date partitions before staging; on a fork, flag-and-hold on #554 — owning seats reconcile, no unilateral renumbering"
  ],
  "lesson_line": "A note number re-appearing under a new date with different bytes is a fork, not a second edition — uniqueness must hold across every partition, and forks are flagged for their owners to reconcile, never silently renumbered.",
  "extends": "SN-033 (collision registry, first-claim chronology), SN-115 (three-layer registry + no-unilateral-supersession), SN-169 (compelled renumber clears the registry), SN-171 (registry scans every live-claim branch)"
}
~~~
