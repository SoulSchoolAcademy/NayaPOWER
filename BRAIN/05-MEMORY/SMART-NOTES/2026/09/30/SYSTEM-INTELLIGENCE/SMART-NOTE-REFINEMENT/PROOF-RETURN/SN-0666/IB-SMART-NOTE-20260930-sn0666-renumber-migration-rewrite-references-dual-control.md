# A Renumbering Migration Is Only Half Done Until Every Reference Is Rewritten — Verify the Repair with Both a Positive and a Negative Control

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0666-renumber-migration-rewrite-references-dual-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6055725753 ([NAYA 4 · self-build loop] SIGN OUT — smart-link repair complete, PR #1854, 2026-10-08T08:16:46Z); smart-link re-verification report `smart-link-reverify-2026-10-08.md` (2026-10-08T06:24Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #1229 consolidation dedup renumbered old SN-018..SN-0525 → successors (SN-0589/SN-0593/SN-0595..SN-0617) but left 21 smart links pointing at the dead paths — a renumbering migration that shipped without its reference rewrite. The 06:24Z re-verify run caught it read-only (21 × 404); PR #1854 repaired it (single file `.naya/memory/smart-notes/index.json`, 21 entries repointed). Two mechanics made the repair proof-grade:

1. **Root cause proven, not assumed.** The repair stated the mechanism: consolidation dedup renumbering → links pointed at dead paths; all 21 successors confirmed ACTIVE in the registry with matching titles; all 21 new target paths confirmed present in the tip tree (`53217a40`); branch blob SHA == local blob SHA (`6ec5b344…`); PR-head file byte-identical to the verified repair.
2. **Dual-control verification.** Positive control: all **53/53** smart_link URLs HEAD 200 after the repoint. Negative control: the **21 old URLs still 404** — the check is non-vacuous (it would have passed a checker that always returned 200).

A third, quieter catch: 11 supersession records falsely claimed "(successor unknown capture not yet ingested) / no surviving distinct page." The repair disproved those claims and corrected them to the real successor IDs — the records were lying, not the tree. Per SN-0420, the repair changed the artifact (the records), never the derived state (the index).

## 🩷 HUMAN NOTE

Shawn — a tidy two-part lesson from this morning's smart-link repair worth banking. Part one: the big #1229 note consolidation renamed a bunch of note numbers, but the links pointing at those notes were never updated — so 21 smart links died quietly. A rename is only half done until every reference is rewritten in the same motion. Part two: the repair didn't just say "fixed" — it proved it with two checks: every new link works (53/53 green), AND every old dead link still fails (21 still 404). That second check matters: if the checker always said "fine," the first check alone would mean nothing. There's a bonus catch too — 11 records claimed "we don't know what replaced these," and that turned out to be wrong; the real successors were found and the records corrected. The brain's rule now: migrations rewrite references atomically, and repairs prove themselves from both directions.

## 🟣 CHILD NOTE

Imagine a library renames half its books' shelf numbers but doesn't update the card catalog — every card points to an empty shelf. That's what happened: the notes got new numbers, but the links still pointed at the old ones. The fix had two parts: update all the cards, and then check two things — that every new card points to a real book, AND that the old wrong cards still point nowhere. That second check proves the checking machine actually works. Also: some cards claimed "we don't know what replaced this book" — they were wrong, and got corrected. The rule: when you rename things, update everything that points at them at the same time, and prove your fix from both directions.

## 👵 GRANDMA NOTE

Think of a street being renamed: the city has to change every signpost and update every map, or people end up driving to a street that doesn't exist anymore. The rename happened, but the signposts were forgotten — 21 of them pointing nowhere. The repair changed every signpost, then verified two ways: every new sign points to a real street, and every old sign still points nowhere (proving the checker isn't just saying "all clear" no matter what). One more thing: some old records insisted "we don't know the new street name" — those were wrong and got fixed. From now on: a rename and its reference updates ship together, and every repair is proven from both directions.

## 🧠 NAYA NOTE

Cold successor: whenever a migration renumbers, renames, or relocates content identifiers, treat the reference rewrite as part of the migration, not cleanup — every pointer (smart links, registry paths, registry supersession records) moves in the same motion, on the same branch. Then verify the repair with dual controls: a **positive control** (every new target resolves — e.g. 53/53 HEAD 200) and a **negative control** (every old target still fails — e.g. the 21 dead URLs still 404). A positive-only check is vacuous against a checker that always passes; the negative control proves the instrument. And when migration leftovers claim "successor unknown" / "no surviving page," do not trust the record — re-derive the successor from the live tree; if a real successor exists, the record was lying and the legal repair changes the record (SN-0420), not the index. Evidence for this instance: #1354 6055725753 (PR #1854), re-verify report 2026-10-08T06:24Z.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0666",
  "title": "A Renumbering Migration Is Only Half Done Until Every Reference Is Rewritten — Verify the Repair with Both a Positive and a Negative Control",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SMART-NOTE-REFINEMENT", "PROOF-RETURN"],
  "cousins": ["SN-0254", "SN-0255", "SN-0420", "SN-0621"],
  "evidence": {
    "board": ["#1354 6055725753 ([NAYA 4 · self-build loop] SIGN OUT — smart-link repair complete, PR #1854, 2026-10-08T08:16:46Z)"],
    "reverify": "hidden_files/smart-link-reverify-2026-10-08.md (2026-10-08T06:24Z): 617 index entries, 53 smart_links, 32 x 200 / 21 x 404 read-only; 21 dead paths reported not fixed",
    "repair": "PR #1854 naya4/smart-link-repair-2026-10-08: single file .naya/memory/smart-notes/index.json, 21 entries repointed; root cause = #1229 consolidation dedup renumbered SN-018..SN-0525 to SN-0589/SN-0593/SN-0595..SN-0617",
    "proof": "all 21 successors ACTIVE in registry with matching titles; all 21 new target paths present in tip tree 53217a40; branch blob SHA == local blob SHA (6ec5b344...); PR-head file byte-identical to verified repair",
    "positive_control": "53/53 smart_link URLs HEAD 200 after repoint",
    "negative_control": "21 old URLs still 404 — check is non-vacuous",
    "honesty_fix": "11 supersession records falsely claimed '(successor unknown capture not yet ingested) / no surviving distinct page' — disproven, corrected to real successor IDs"
  },
  "rule": "a renumbering migration ships its reference rewrite in the same motion; verify the repair with both a positive control (new targets resolve) and a negative control (old targets still fail); never trust a 'successor unknown' record — re-derive from the live tree and repair the record, not the index"
}
```
