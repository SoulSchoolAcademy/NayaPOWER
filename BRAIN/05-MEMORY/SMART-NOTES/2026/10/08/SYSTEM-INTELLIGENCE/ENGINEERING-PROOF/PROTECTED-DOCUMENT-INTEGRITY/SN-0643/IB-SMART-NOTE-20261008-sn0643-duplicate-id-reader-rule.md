# Same-Bytes Contradictions Resolve to Mechanism — the Duplicate-ID Reader Rule

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0643-duplicate-id-reader-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6052122468 ([NAYA 2][BRAIN-BUILD], 2026-10-08T04:18:54Z — virgin-tree battery + public correction of her own 03:57Z receipt 6051898236: the 3 REDs in `tests/test_protected_intelligence_integrity.py` are REAL on live-tip bytes at `00f50bb3` and `f52ffb96`; mechanism = duplicate-id collision, not canonical hollowing), 6052103878 ([NAYA 2][BRAIN-DRIVE], 2026-10-08T04:17:22Z — canonical capture `.naya/capture/SMART-NOTE-20261005-sn0359-proactive-captain.json` INTACT, all 9 governed fields present; reconstruction `.naya/capture/ingest-20261008-repin-test-new-invariant.json` declares the same `smart_note_id: SN-0359` with a hollow body; id-indexed read resolves SN-0359 to the hollow body; live exposure in `tools/retrieval_audit.py`, `tools/cold_retrieve_drill/drill.py`, `tools/smart_note_v2.py`, `tools/truth_state_guard.py`), 6052049127 (OVERNIGHT SWEEP, 2026-10-08T04:12:43Z — the test builds its index via `idx[str(nid)] = doc` over `CAPTURE_DIR.glob("*.json")` (lines 48–58): later files overwrite earlier ones in filesystem-dependent order; kernel verdict recorded as DOCUMENTED-NONDETERMINISTIC; full capture scan: 591 files, 577 unique IDs, 14 duplicate IDs) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08 Naya 2 published a receipt (comment 6051898236) declaring that Naya 4's 7/7 PASS stood and the battery's 3 REDs were reused-worktree contamination. Then she ran a virgin tree — fresh detached worktree at `00f50bb3`, local `HEAD^{tree}` == remote tree SHA `2196e6a1d7c00feb1c0bb527f42f29d9b74cfc36` — and the 3 REDs reproduced. Instead of averaging the two verdicts, she resolved to mechanism and published the correction (comment 6052122468): **the SN-0633 bulk-hollow theory was wrong.** The canonical SN-0359 capture was intact; a reconstruction file in the same directory declared the same `smart_note_id: SN-0359` with a hollow body, and the test's id-keyed index — built by iterating `glob("*.json")` with later paths overwriting earlier ones — resolved SN-0359 to the hollow body on this checkout and to the intact one on another.

Three durable rules:

1. **Never build an ID-keyed index by iterating filesystem order without a collision rule.** A duplicate ID is not a cosmetic blemish — it silently hollows the canonical for every ID-keyed consumer. The live exposure was not test-only: `tools/retrieval_audit.py`, `tools/cold_retrieve_drill/drill.py`, `tools/smart_note_v2.py`, and `tools/truth_state_guard.py` all key readers on `smart_note_id` and can resolve a Director-ratified law to a hollow body depending on read order. SN-0257 closed the staging-side dedupe; this is the reader-side twin: dedupe at write is not enough — every reader that keys on a human-visible ID needs a deterministic collision rule (prefer the canonical schema version, fail loudly, or refuse the duplicate).
2. **A test that keys a dict by glob order makes its CI verdict checkout-luck, not proof.** Same tip, two checkouts, opposite verdicts — green on this tip is one filesystem's roll of the dice. Until the index build is deterministic (or the duplicate is retired), the kernel verdict is DOCUMENTED-NONDETERMINISTIC: record the nondeterminism explicitly; never cite the green as behavioral proof. (SN-0421 family.)
3. **Same-bytes contradictions resolve to mechanism, and the correction gets published.** Naya 2's correction superseded her own 03:57Z receipt in the open — that is the evidence law working, not a lane failing. A cold successor reading SN-0633 (which recorded the bulk-hollow theory on the 03:10Z battery) needs this note beside it: the theory was falsified by virgin-tree batteries; the mechanism is duplicate-id collision plus order-dependent resolution. A wrong theory in the canon is worse than a missing one — correct it in public, and name which theory the correction supersedes.

## 🩷 HUMAN NOTE

Shawn — a correction to tonight's record worth keeping: Naya 2 first said the SN-0359 reds were test-environment contamination, then re-ran on a virgin tree and found they're real — the canonical note is intact, but a duplicate file claims the same note ID, and the test resolves the ID to whichever file the filesystem lists last. So CI green on this test is checkout luck, not proof. The banking rules: never build an ID-keyed index from filesystem order without a collision rule (a duplicate silently hollows the real document for every reader), and when the bytes contradict your own receipt, publish the correction with the mechanism — that's the evidence law working, not a failure. This note also corrects SN-0633's bulk-hollow theory: the merge didn't gut the note; the duplicate ID did.

## 🟣 CHILD NOTE

Imagine two folders both labeled "Rule 359." One folder holds the real rule with all its pages; the other holds an empty copy someone made. The helper who fetches "Rule 359" grabs whichever folder is on top of the pile — and the pile gets stacked in a different order in different rooms. So in one room she hands you the real rule, in another the empty one, and nobody changed anything. The fix: never let pile order decide — write a rule for which folder wins, or throw out the empty copy. And if you once told everyone "the folders are fine," then discover the empty copy, say so out loud: correcting yourself is how the team stays smart.

## 🔵 GRANDMA NOTE

Dear, this is about the card catalog with two cards for the same number. The librarian's new helper files cards by tossing them in a drawer and reading them back in drawer order — whichever of the two same-numbered cards lands last is the one she hands you. Some days you get the real book's card, some days the blank one, and the drawer is never the same twice. The fix isn't to re-read the drawer more carefully — it's a house rule: one number, one card; if a second card appears, it must not decide by drawer order. And when you discover you've handed someone the wrong card, you go back and say so plainly. An honest correction keeps the catalog trustworthy; a quiet one lets the wrong card win forever.

## 🟠 NAYA NOTE

Cold successor: when you find two capture files declaring the same `smart_note_id`, treat it as a collision emergency, not a curiosity. (1) Scan the whole capture directory for duplicate IDs (the 2026-10-08 sweep: 591 files, 577 unique IDs, 14 duplicates — that is the shape of the debt). (2) Never let read order arbitrate — give the reader a deterministic collision rule (canonical schema version wins; or fail loudly; never "later path wins"). (3) If any test builds a dict by iterating `glob`, treat its verdict as DOCUMENTED-NONDETERMINISTIC until the build is deterministic or the duplicates are retired — cite the verdict with the caveat, never as proof. (4) When a virgin battery contradicts your own published receipt, publish the correction in the same venue, name the mechanism, and name which theory it supersedes — SN-0633's bulk-hollow theory is superseded by this note's duplicate-id-collision mechanism. Repair ownership stays with the lane that introduced the duplicate (SN-0236); your job is the mechanism record, not their repair.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0643",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "PROTECTED-DOCUMENT-INTEGRITY"],
  "extends": [],
  "related": ["SN-0633", "SN-0257", "SN-0390", "SN-0421"],
  "supersedes_theory": "SN-0633's bulk-hollow mechanism for the SN-0359 REDs (the consolidation-merge theory); the REDs' mechanism is duplicate-id collision + order-dependent id-indexed resolution. SN-0633's repair rule (field battery on every bulk rewrite) is unaffected and still stands.",
  "rule": "never build an ID-keyed reader index by iterating filesystem order without a deterministic collision rule — a duplicate ID silently hollows the canonical for every ID-keyed consumer; a test that keys a dict by glob order makes its CI verdict checkout-luck (DOCUMENTED-NONDETERMINISTIC until deterministic or duplicates retired); same-bytes contradictions resolve to mechanism, and the correction is published in the open, naming the superseded theory",
  "evidence": [
    "#1354 6052122468 (2026-10-08T04:18:54Z): virgin worktree at 00f50bb3, local HEAD^{tree} == remote tree SHA 2196e6a1d7c00feb1c0bb527f42f29d9b74cfc36 — test_protected_intelligence_integrity.py 3 failed / 4 passed; full suite 1053 passed / 11 skipped / 3 failed; reproduced again at f52ffb96",
    "#1354 6052103878 (2026-10-08T04:17:22Z): canonical .naya/capture/SMART-NOTE-20261005-sn0359-proactive-captain.json intact (all 9 governed fields); duplicate .naya/capture/ingest-20261008-repin-test-new-invariant.json declares smart_note_id SN-0359, hollow; id-indexed read resolves to hollow body; exposed readers: tools/retrieval_audit.py, tools/cold_retrieve_drill/drill.py, tools/smart_note_v2.py, tools/truth_state_guard.py",
    "#1354 6052049127 (2026-10-08T04:12:43Z): index built via idx[str(nid)] = doc over CAPTURE_DIR.glob('*.json'), later-overwrites-earlier in filesystem order; verdict DOCUMENTED-NONDETERMINISTIC; capture scan 591 files / 577 unique IDs / 14 duplicate IDs",
    "repair ownership: Naya 4's consolidation lane (commit 7b828bd71 introduced the duplicate); open PR #1837 owns the reassign-to-SN-0642 repair — no competing repair from this loop"
  ],
  "falsifiers": [
    "Treating a green CI verdict on a glob-ordered index test as behavioral proof without stating the ordering assumption",
    "Deduplicating only at write time while readers key on human-visible IDs with no collision rule",
    "Averaging contradictory same-bytes verdicts instead of resolving to a single mechanism and publishing the correction"
  ]
}
```
