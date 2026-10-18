# A Shared Code Path Is a Hypothesis Until Probed — Exclusions Are Probed Per Variant, Never Assumed From Path Identity

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01624-a-shared-code-path-is-a-hypothesis-until-probed
**Smart Note:** SN-1624
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** gap-lane-scorer-20261018-0120-lane5 (2026-10-18): parent t1412 proved SUPERSEDED exclusion at the seam and asserted ARCHIVED/REVOKED shared the identical code path (`inactive` frozenset, tools/smart_note_v2.py:786); this run's two direct probe arms plus triple-replicated t1412 battery (24 runs, 0 flips) measured the full set {SUPERSEDED, ARCHIVED, REVOKED} excluded 3/3 each. Board verdict: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721#issuecomment-6247626370. Gap CLOSED (9.5/10).

## IN A NUTSHELL

Parent t1412 proved that SUPERSEDED notes are excluded at the retrieval seam and claimed ARCHIVED and REVOKED were covered too because they travel the same code path — the `inactive` set. That was an assertion, not a measurement: nobody had ever probed ARCHIVED or REVOKED at the seam. The gap run built dedicated probe arms per variant plus triple replication of the original battery (24 runs, zero flips) and measured the full terminal-lifecycle set — SUPERSEDED, ARCHIVED, REVOKED (plus RETIRED at the current tip) — excluded 3/3 each. The asserted claim is now a measured one. The rule: when an exclusion claim covers an enum, every variant gets its own probe arm at the seam; shared-path identity is the hypothesis, the probe is the proof.

## HUMAN NOTE

An inspector tests one brand of fire extinguisher and declares "they're all the same mechanism inside, so they all work." Maybe true — but the claim was never tested for the other two brands. That's exactly what happened at the retrieval seam: SUPERSEDED was tested, ARCHIVED and REVOKED were covered by the assumption that "same code path means same behavior." A dedicated re-run built separate tests for each brand — three rounds each — and now we know, not assume. The discipline going forward: a coverage claim over a category must test every member of the category. "Same shape" is a good hypothesis; it is never the evidence.

## CHILD NOTE

Your teacher checks that the red crayon fits in the box, and says "the blue and green crayons will fit too — they're all crayons." Sounds reasonable! But what if the blue crayon is longer? You'd never know until you try. So the rule is simple: don't just try the red one — try the blue one and the green one too. Each one gets its own try, and you try them a few times to be sure. Trying is proof; guessing from the red one is just a good guess.

## GRANDMA NOTE

It's the difference between knowing your own porch step is sound and declaring the whole staircase sound because "they're all the same wood." Same wood, maybe — but each step takes its own feet, and rot hides in one step while the rest hold. The house rule is plain: you test every step you claim is sound. An assumption about the staircase is a plan for testing, never the test itself.

## NAYA NOTE

**Exclusion claims over an enum carry a per-variant probe obligation.** The t1412 parent's claim was correct in the end — but correctness discovered later doesn't retro-license the assertion; the gap was real because "asserted, never probed" is a gap class regardless of outcome. The mechanical standard this run sets: one probe arm per enum variant at the seam (ARM-ARCHIVED SN-X7, ARM-REVOKED SN-X8), triple-replicated, fresh tree and fresh HOME per round, with fixture pins sealed before the run and re-verified byte-identical after. The receipts carry the variant×replication matrix (24 rows, 0 flips) — a claim whose proof covers fewer variants than the enum is incomplete by construction. Cousin: SN-01610 (a freeze script is a contract with the design doc — the probe-side twin: byte-check the instrument the same way); CANDIDATE 604-family instrument discipline (this is its exclusion-probing specialization); SN-01603 (falsify through the real entrypoint — the sibling seam discipline).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1624",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verification", "exclusion"],
    ["battery", "enum-variant"],
    ["seam", "shared-path"]
  ],
  "enforcement": "Exclusion claims at a seam ship one probe arm per enum variant (ARM-<VARIANT> pattern: ARM-ARCHIVED, ARM-REVOKED), triple-replicated on fresh trees with fresh HOME, fixture pins sealed pre-run and re-verified post-run. The receipt carries the variant-by-replication matrix; a lane review (gap-lane-scorer exclusion standard) marks any exclusion claim whose proof covers fewer variants than the enum as INCOMPLETE — 'shared the identical code path' is accepted as the hypothesis line in the receipt, never as the evidence line. The gap-lane-scorer 0120 run (battery_replicate.py, 24 runs / 0 flips, pins 12f7fedae… and f5571148cd…) is the reference implementation.",
  "decision_change": "Future exclusion claims change from 'variants X and Y share the code path, so the proof for X covers Y' to 'X proved, Y unprobed — add the probe arm or log the gap.' Future lanes can no longer close an exclusion verdict on path-identity alone; the probe matrix is part of the verdict.",
  "falsifier": "An enum whose variants provably share one branchless code path (zero variant-conditionals between entry and the seam decision, mechanically verified on the pinned script bytes) would falsify the obligation for that enum — the note would be revised to 'probe per variant OR prove branchlessness.' Path-identity asserted from reading the code does not meet this bar; it must be mechanically demonstrated on the pinned bytes.",
  "mechanism": "Variant-conditional seams hide inside shared paths: a single frozenset can serve variants that arrive through different write paths, different timestamps, or different lifecycle transitions, and any one of those differences can interact with the seam logic (ordering, cache keys, staleness windows) without touching the 'identical' lines. The probe arm per variant samples the actual arrival path, not the path's prose description — and triple replication separates genuine invariance from single-run luck.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0120-lane5.md: named gap 1 ('The exclusion proof covered SUPERSEDED only — ARCHIVED/REVOKED shared the identical code path (the inactive set) but were asserted, never probed'), closed with ARM-ARCHIVED (SN-X7) and ARM-REVOKED (SN-X8) 3/3 each + triple-replicated t1412 battery (24 runs, 0 flips); fixture pins SN-X7 12f7fedae4855227d6d41d81d1fc6fad7f19df0e2e5a9cb3da45997fa92a74de0, SN-X8 f5571148cd64419f98efd704943c7caf6473ee1744d29690040997fa92a74de0; battery script hidden_files/lane5-gap-20261018-0120-exclusion/battery_replicate.py; board verdict https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721#issuecomment-6247626370.",
  "cousins": ["SN-01610 (a-freeze-script-is-a-contract-with-the-design-doc — the probe-side twin: byte-check the instrument the same way)", "SN-01603 (falsify-through-the-real-entrypoint — the sibling seam discipline)", "SN-01597 (maximal-strength-adversarial-test — strengthen the adversary, not weaken it)"]
}
~~~
