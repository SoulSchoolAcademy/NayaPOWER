# IB-SMART-NOTE-20261009-sn0834-immutable-r1-tombstone-never-renumber-history

Intelligent Block: SN-0834
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Dedup fixes the registry — never history. Naya 4's C5 smoke test found 19 duplicate SN-IDs + 1 vanity ID in the live SN registry (`.naya/memory/smart-notes/index.json`, 630 entries). The repair was renumber-only, nothing deleted: 18 true duplicates (SUPERSEDED phantom entries) renumbered to SN-0796, SN-0797, SN-0804–SN-0819; the vanity ID SN-NET-POWER-MAGIC-001 became SN-0820 with its directory renamed and all tree cross-references updated; canonical published entries kept their IDs (SN-033 first-claim-stands); new numbers cleared all three registry layers (verified free on main and against all 100 open PRs); next_sequence moved 783 → 821. The 19th normalized hit — the SN-346 R1 tombstone vs SN-0346 — was deliberately NOT renumbered: SN-0370's immutable-R1 doctrine says the historical allocation stays on R1, and 8 published notes document the SN-346 history. Renumbering it would falsify executed history to make a test pass. The judgment was recorded in the PR body with an explicit override path ("override me if Shawn wants it mechanical"). A tombstone that records what actually happened is evidence, not a duplicate.

## HUMAN NOTE

Cleaning up a numbering system is tempting to do mechanically: find every collision, renumber every collision. But some "collisions" are the historical record itself — a tombstone marking that SN-346 was allocated, superseded, and documented across 8 published notes. Renumbering it wouldn't fix anything; it would rewrite what happened so the ledger looks tidy. Tidiness that rewrites history is falsification with good intentions. The rule: repair the registry's future (free numbers, clear layers, correct sequence) and leave its past alone.

Provenance: NayaPOWER #1354 comment 6090808797 ([NAYA 4] SN registry dedup DONE — PR #2076 (draft), 2026-10-09T23:09:31Z). Related: SN-033 (first-claim-stands), SN-0370 (immutable-R1 doctrine), SN-0169 (compelled renumber clears the three-layer registry), SN-0673 (renumbering migration identity gate), SN-0257 (dedupe must cover human-visible ID), `test_smart_note_registry_drift` 12/12 passing after the repair.

## CHILD NOTE

Imagine a museum fixing its exhibit numbers. Most duplicates get new numbers — fine. But one "duplicate" is a plaque that says "this spot held the very first exhibit, which was moved." Renumbering the plaque would erase the story of what was there first. You fix the numbers going forward, and you leave the plaque exactly where history put it.

## GRANDMA NOTE

When you tidy a filing cabinet, you don't rewrite the old folders' labels to make the new system look perfect — the old labels are the record of what was filed and when. Naya's cleanup gave the real duplicates fresh numbers and left the one historical marker untouched, because changing it would have been pretending the past happened differently.

## NAYA NOTE

Operational rules:

1. Registry dedup protocol: renumber-only, never delete; canonical published entries keep their IDs (first-claim-stands); new numbers must clear all three registry layers — free on main AND free across all open PRs (in-flight claims stand); advance next_sequence past the repaired range.
2. The tombstone test: before renumbering any entry, ask whether the entry documents executed history (published notes reference it, a doctrine pins it, e.g. SN-0370 immutable-R1). If yes, it is evidence, not a duplicate — leave it and record why.
3. A deliberately-skipped repair is a decision, not an omission: record it in the PR body with the doctrine cited, the evidence count (8 published notes), and an explicit override path for the director. Silence about a skipped item reads as a missed item.
4. Vanity/non-numeric IDs (SN-NET-POWER-MAGIC-001 → SN-0820) get normalized to the numeric sequence, with the directory renamed and every tree cross-reference updated (notes, README, corpus paths, live bridges, registry provenance) — while the IB machine identity stays untouched.
5. Verify the repair mechanically after: regenerate the brain index (`--check` OK), run the registry drift tests (12/12), and confirm remote tree SHA == local tree SHA before the PR leaves draft.

## MACHINE NOTE

```json
{
  "sn": "SN-0834",
  "truth_state": "CANDIDATE",
  "doctrine": "dedup repairs the registry, never history — a tombstone recording executed history is evidence, not a duplicate",
  "concrete_case": "SN registry dedup PR #2076: 18 true duplicates renumbered (SN-0796/0797/0804-0819), 1 vanity normalized (SN-0820); SN-346 R1 tombstone deliberately NOT renumbered per SN-0370 immutable-R1",
  "dedup_protocol": "renumber-only, nothing deleted; canonical IDs kept (SN-033 first-claim-stands); three-layer clearance (main + all open PRs); next_sequence 783->821",
  "tombstone_test": "entry documents executed history (8 published notes reference SN-346) -> evidence, do not touch",
  "skip_discipline": "record skipped repairs in PR body with doctrine + evidence + explicit director override path",
  "vanity_rule": "normalize to numeric sequence; rename directory; update all tree cross-references; IB machine identity untouched",
  "post_repair_verification": "brain index --check OK; test_smart_note_registry_drift 12/12; remote tree SHA == local tree SHA",
  "related": ["SN-033 (first-claim-stands)", "SN-0370 (immutable-R1)", "SN-0169", "SN-0673", "SN-0257"],
  "provenance": "NayaPOWER#1354/6090808797"
}
```
