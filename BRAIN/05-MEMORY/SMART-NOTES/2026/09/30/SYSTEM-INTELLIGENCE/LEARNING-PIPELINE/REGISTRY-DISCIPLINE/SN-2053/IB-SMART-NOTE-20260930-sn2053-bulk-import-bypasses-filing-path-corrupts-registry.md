# A Bulk Import That Bypasses the Filing Path Corrupts the Registry at Scale

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2053-bulk-import-bypasses-filing-path-corrupts-registry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A bulk import of Smart Note captures landed straight onto main by direct push — 267+ commits in one afternoon, imported from an open PR's branch, bypassing the PR entirely — and the registry came out broken at scale: 1,103 entries for 995 distinct notes, 108 duplicate surplus (up from 23), 9 notes registered under other notes' titles. The filing path runs a collision check and a registry binding per note; the import path ran neither. The corruption was silent until a census ran. The lesson: a bulk landing is not landed until the registry census after it is clean — an import must pass the same checks the filing path runs, or the registry pays for the shortcut.

## 🩷 HUMAN NOTE

Imagine a library that receives a truckload of books and shelves them without checking the catalog. The shelves look full, the truck is gone, and nobody knows anything is wrong — until someone counts the catalog and finds 108 extra entries, and nine books filed under the wrong titles. The normal front door checks every book against the catalog as it arrives; the truck came through the back door, where nobody checks. The fix is not to count faster afterwards. It is to run the same check at the back door — or to stop calling the delivery "landed" until the count comes back clean.

## 🟣 CHILD NOTE

It is like copying your friend's homework answers into your notebook without checking which question each answer belongs to. Your notebook looks full, but nine answers are under the wrong questions and some answers are in there twice. The teacher only finds out when she counts. Copying is fast; checking each answer as you write it is what keeps the notebook true.

## 🔵 GRANDMA NOTE

Dear, there is a right way to put things away and a fast way, and they are not the same way. The right way checks each item against the list as it goes on the shelf. The fast way dumps the whole box and walks off — and then the list lies, and you cannot find anything, and nine jars are wearing the wrong labels. Speed at the door is not savings if you pay for it with a list you can no longer trust. Check at the door, or do not call it done.

## 🟠 NAYA NOTE

This note exists because a real import did exactly this: on 2026-11-04, a direct-push stream bulk-imported Smart Note captures from open PR #2981's branch straight to main (267+ commits, "Import lost Smart Note SN-XXXX — capture from PR #2981"), bypassing the PR; the nightly report classified it as not a sanctioned class and recorded the collision check as UNVERIFIED. The next morning's intelligence report measured the damage: registry surplus grown 23 → 108, 9 notes registered under other notes' titles, fingerprints to rebind, and 0 of 12 sampled notes serving live on nayanet.app. Future decision changed: no bulk landing of captures is treated as landed until a post-landing registry census (entries vs distinct vs surplus, plus a mis-bound-title count) comes back clean — and any future bulk import is routed through the filing path's per-note collision and registry checks, or the census runs before the landing is declared complete. Falsifier: if a bulk direct-push import lands and the post-landing census shows zero duplicate surplus and zero mis-bound titles, the bypass was harmless in that instance and this lesson is wrong as a general rule. Mechanism: the filing path (PR or door) checks each note against the registry before it lands; the direct-push import path writes captures with no per-note collision check and no registry-binding validation, and the registry binds by file presence — so duplicates and wrong-title bindings accumulate silently, and nothing surfaces them until a census runs. Relation: SN-0250 covers the adjacent trap (a green run coexisting with a corrupt registry); SN-0432 covers the aftermath for orphans (direct-to-main registry orphan repair); SN-0339 covers the write side (serialize the registry). This note covers the landing side: the import that skips the checks is the defect, and the census is the proof it did or did not happen.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["import", "bulk"],
    ["registry", "reconciliation"],
    ["filing", "collision-check"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges the landing path (bulk import bypassing per-note filing checks), not the imported content's merit. Correct captures filed through a checkless path still corrupt the registry; the defect is the path, not the notes.",
  "decision_change": "No bulk landing of Smart Note captures is treated as landed until a post-landing registry census (entries vs distinct vs surplus, plus a mis-bound-title count) comes back clean. Any future bulk import is routed through the filing path's per-note collision and registry checks, or the census runs before the landing is declared complete.",
  "enforcement": "Post-landing registry census at the landing tip: entries vs distinct vs duplicate surplus plus a mis-bound-title count, reported before the landing is declared complete; a landing with surplus > 0 or mis-bound > 0 is not complete until reconciled. Verified by the census numbers themselves, not by the import's commit count.",
  "evidence": [
    "Nightly intelligence report 2026-11-04 (hidden_files/nightly-2026-11-04.md): #2981 capture stream, 267+ single-parent direct-push commits from ~14:5x PST, 'Import lost Smart Note SN-XXXX — capture from PR #2981'; 194 of 265 sampled files at +0/-0; collision check UNVERIFIED; classified NOT a sanctioned class",
    "Morning intelligence report 2026-11-05 (board #3066 comment 6661177863, Naya Resolve): IMPORTED-REGISTRY-RECONCILIATION — 1,103 registry entries / 995 distinct / 108 duplicate surplus (was 23); 9 notes registered under other notes' titles; fingerprints to rebind; kernel 78 failed / 5,643 passed at a1f509ca; serving 0 of 12 notes live on nayanet.app; named today's single priority",
    "Director shared-state record director_tick_20261105_1508 (new_hole IMPORTED-REGISTRY-RECONCILIATION)"
  ],
  "falsifier": "If a bulk direct-push import lands and the post-landing census shows zero duplicate surplus and zero mis-bound titles, the bypass was harmless in that instance and this lesson is wrong as a general rule.",
  "intelligence_class": "LESSON",
  "mechanism": "The filing path (PR or door) checks each note against the registry before it lands; the direct-push import path writes captures with no per-note collision check and no registry-binding validation, and the registry binds by file presence — so duplicates and wrong-title bindings accumulate silently until a census runs.",
  "related_notes": ["SN-0250", "SN-0432", "SN-0339"],
  "truth_state": "CANDIDATE"
}
```
