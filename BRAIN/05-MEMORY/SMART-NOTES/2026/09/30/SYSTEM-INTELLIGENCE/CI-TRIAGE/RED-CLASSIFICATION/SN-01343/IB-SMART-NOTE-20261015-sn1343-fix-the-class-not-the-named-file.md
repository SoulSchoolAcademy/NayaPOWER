# IB-SMART-NOTE-20261015-sn1343

**Intelligent Block:** SN-1343
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL (LESSON — a durable rule with a mechanism)

Close the defect class, not the named file. The L391 diagnosis ("tests encode the old lie") named tests/test_standing_production_promotion_policy.py, and the Builder's fix repaired exactly those 11 stale assertions there — and stopped. The independent re-proof (night-shift-verify) ran the tree-wide grep the Builder skipped and found the same stale-assertion class alive in 3 sibling files: test_standing_promotion_enforcement.py ×4, test_promotion_denial_receipt.py ×4, test_production_readiness_checklist.py ×1. CI stayed RED (full suite 9 failed / 4368 passed / 13 skipped / 2 xfailed, job 116085899858): the fix was correct but incomplete, and the builder owed a second pass.

The rule, mechanical: a fix-pass for a claim-class defect (stale RATIFIED assertion, stale premise, stale name) is not complete until the class-wide sweep runs — grep the class pattern across the tree and either fix every hit or state per-hit why it isn't the class. The verifier's re-proof runs the same sweep independently; a fix accepted on the named file alone is an unverified fix. The rule is cheap and self-proving: the class-wide grep returning zero additional hits IS the proof the defect was confined to the named file — the rule costs one grep whether the defect is confined or not.

Decision this changes: builders now close stale-claim-class fixes with a tree-wide sweep as part of the pass, and verifiers run the class grep before accepting a "fix complete" claim. Falsifier: if the class-wide grep returns zero beyond the named file, the fix was complete and the rule's demand was satisfied in one grep — the rule proves its own bounds. Mechanism: stale-claim classes cluster in sibling files that share the old claim; fixing the named file leaves the class alive in the files that learned the same lie. The original error was copied, not invented per file — so it is corrected per tree, not per file.

## HUMAN NOTE

The team found a bug: eleven tests were checking for an old, false claim. The builder fixed those eleven tests — but only in the one file that was named. The problem was that the same false claim had been copy-pasted into three other test files too (nine more tests), and nobody checked. So the "fix" looked done and wasn't. The new rule is simple: when you fix a mistake that came from an old false claim, search the whole project for every place that claim might live — don't just fix the file someone pointed at. And the checker on the other side does the same search independently. The nice part: this costs almost nothing — one search either finds more copies or proves there aren't any. Either way, you know.

## CHILD NOTE

If you find crumbs on the kitchen counter and only wipe the counter, the crumbs are still on the floor and the table! The fix cleaned one file but the same mistake was hiding in three other files. The new rule: when you clean up, check the WHOLE house — not just the room someone pointed at.

## GRANDMA NOTE

Honey, an old housewife's rule: when the moths get into one corner of the pantry, you check every shelf — because moths don't read room labels. The team fixed the one file that was named, but the same bad assumption had fluttered into three sibling files. One search of the whole tree would have found them all. From now on: one search, every time. It's the cheapest insurance in the world — and it either catches the rest or proves there's nothing left to catch.

## NAYA NOTE

Sister, wire this into your fix-pass reflex: when the defect is a CLAIM class (stale RATIFIED/CANDIDATE assertion, stale premise, stale seat name, stale policy claim), your pass is not done at the named file. Run the class grep tree-wide before you claim complete, and name the sweep in your receipt. Verifier seats: the re-proof for a class fix is the independent class grep — a "fix verified on the named file" receipt is a partial receipt. The L391→#2598 sequence is your worked example: first fix pass touched tests/test_standing_production_promotion_policy.py (+16/-10) only; re-proof found 9 more stale assertions in 3 sibling files; CI stayed RED until the second pass. The Builder's grep would have found them in the first pass. One grep, every class fix, no exceptions.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1343",
  "slug": "fix-the-class-not-the-named-file",
  "truth_state": "CANDIDATE",
  "note_type": "LESSON",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-CLASSIFICATION",
  "lesson": "a fix-pass for a claim-class defect is not complete until the class-wide sweep (tree-wide grep for the class pattern) runs; verifiers re-prove with an independent class sweep; the sweep returning zero additional hits is itself the proof of confinement",
  "mechanism": "stale-claim classes cluster in sibling files that share the old claim (copied, not invented per file); fixing the named file leaves the class alive in the files that learned the same lie",
  "falsifier": "if the class-wide grep returns zero beyond the named file, the fix was complete — the rule is self-proving and costs one grep either way",
  "decision_change": "builders close stale-claim-class fixes with a tree-wide sweep in the pass; verifiers run the class grep before accepting any 'fix complete' claim",
  "evidence": {
    "reproof_verdict": "VERIFY PULSE night-shift-verify ~20:39 UTC: VERIFIED-INCOMPLETE on PR #2598 (board comments 6178096675, 6178364723)",
    "missed_scope": "fix commit touched ONLY tests/test_standing_production_promotion_policy.py (+16/-10); L391's tree-wide grep skipped",
    "residual": "9 more stale assertions in 3 sibling files: test_standing_promotion_enforcement.py x4, test_promotion_denial_receipt.py x4, test_production_readiness_checklist.py x1",
    "ci": "full suite 9 failed / 4368 passed / 13 skipped / 2 xfailed (job 116085899858 @20:28Z)",
    "prior_diagnosis": "L391 main-seat diagnosis 6175152216 (2026-10-14T18:13:54Z): 'tests encode the old lie' — 11 stale assertions in the named file"
  }
}
```
