Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
On greenfield machinery, run the detector before the seed data exists. With no seed to compensate, the detector's first complaints enumerate exactly the divergence between the world and the empty ledger — the complaint list is by construction the complete backfill list. Pre-seed run = the test, backfill = the fix, post-seed run = the proof. Seeding first hides the backlog the detector was supposed to find.

## 🩷 HUMAN NOTE
The t1459 reconcile-move ledger audit ran BEFORE seeding — and its first live run found exactly the 8 unlogged post-t1449 moves, no more, no fewer: audit exit 2 with the exact complaint list, backfill from that list, then the post-seed run proved the fix (exit 0, both grandfathering branches PASS on scratch trees, selftest exit 0). The machine diagnosed its own backlog because the detector ran against raw reality before any seed data existed to mask it. Root cause of the win: the complaints were the seed list. Every future greenfield build brief runs the detector first, seeds second — a brief that seeds first must explain why. Evidence: twelve-lane-receipts/t1459-lane11.md (2026-10-23); LEARNING EVENT CANDIDATE 882 in learning-events-2026-10-23-22.md. Cousins: SN-1893 (mtime-blind move detection — the same ledger's other lesson); SN-0652 (detector keyed to the violation); SN-1320 (detector-first live run tests the detector).

## 🟣 CHILD NOTE
Before you fill your notebook with answers, first check which pages are blank — that check shows you exactly what to write. If you write the answers first and THEN check, you might miss the blanks you were supposed to find. Look at the empty page first, list what's missing, fill it in, then check again that nothing is missing.

## 🔵 GRANDMA NOTE
Before you stock a new pantry, walk through it empty and list everything that's missing — that list becomes your shopping list. Once the shelves are stocked, walk through again and check the list is done. If you stocked first and checked later, you'd never know what you forgot to buy. Empty first, list, fill, verify.

## 🟠 NAYA NOTE
For builders and brief authors: greenfield machinery briefs order the work detector-first. The brief names the pre-seed detector run, its exit code, and its full complaint list in the run command; the receipt opens with those complaints and shows the backfill derived from them, then the post-seed run proving silence. The t1459 acceptance shape is the template: pre-seed audit exit 2 with the exact complaint list (the 8 unlogged post-t1449 moves) → backfill → post-seed audit exit 0 → grandfathering branches PASS on scratch trees. A brief that seeds first and detects later owes an explanation at sign-out; without one, the verifier rejects it — the backlog the detector was supposed to find may still be hiding under the seed.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1900",
  "slug": "detector-before-seed",
  "captured": "2026-10-23",
  "applies_when": ["greenfield", "detector", "seed", "ledger", "reconcile"],
  "enforcement": "Every greenfield build brief runs the detector against the real world BEFORE seeding; the receipt opens with the detector's pre-seed complaints (exit code + complaint list). A brief that seeds first must explain why at sign-out, and the verifier rejects it without that explanation. The t1459 acceptance shape is the template: pre-seed audit exit 2 with the exact complaint list -> backfill -> post-seed audit exit 0.",
  "cousins": ["SN-1893 (mtime-blind-move-detection)", "SN-0652 (detector-keyed-to-the-violation)", "SN-1320 (detector-first-live-run-tests-detector)"],
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1459-lane11.md (2026-10-23): audit run BEFORE seeding — exit 2 with exactly 8 unlogged post-t1449 moves pre-backfill, exit 0 post-backfill; both grandfathering branches PASS on scratch trees; selftest exit 0",
    "hidden_files/learning-events-2026-10-23-22.md: LEARNING EVENT CANDIDATE 882 — 'Detector before seed'; passes-the-bar: the next greenfield build brief's receipt opens with the detector's pre-seed complaints; a brief that seeds first explains why"
  ],
  "decision_change": "The next greenfield machinery brief runs its detector before seeding — the detector's complaints become the backfill list — instead of seeding first and detecting later.",
  "falsifier": "A greenfield build where the pre-seed detector's complaint list does NOT match the real backlog (material false positives/negatives), or a seeded-first build that reaches the same coverage with less work — the receipt would name the case.",
  "mechanism": "Before seed data exists, the detector runs against raw reality with no compensating data: every complaint enumerates a divergence between the world and the empty ledger, so the complaint list is by construction the complete backfill list. Backfilling from that list, then re-running post-seed, converts the detector's first run into the test and the second into the proof."
}
```
