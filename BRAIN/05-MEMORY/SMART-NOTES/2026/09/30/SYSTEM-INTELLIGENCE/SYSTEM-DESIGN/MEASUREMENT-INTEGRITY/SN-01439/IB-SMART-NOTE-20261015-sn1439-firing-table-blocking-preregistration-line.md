# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~18:38 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1439
**Provenance:** learning-events-2026-10-15-18.md (18:00 PDT hour, window 17:20–18:20 PDT): CANDIDATE 437 — receipt twelve-lane-receipts/gap-t0593-lane4.md (2026-10-15): the parent's FIRE-DOC claimed a mechanism fired corpus-wide while the mechanism could only reach 1 of 3 tasks (claim-dense P6/P2 kept 4/4 passages — the filter removed nothing from the very docs the mechanism had to move), so the verdict graded the mechanism on tasks it never touched. This tick restored the per-task firing table as a blocking pre-registration line before sealing.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
A predicate that cannot say no is not a test — it's decoration wearing a gate's clothes. On 2026-10-15 a mechanism's "firing document" claimed the rule fired corpus-wide, but the mechanism could only reach 1 of 3 tasks: on the claim-dense documents the filter removed nothing at all, so the verdict was grading the mechanism on tasks it never touched. The repair: the per-task firing table goes into the pre-registration as a blocking line BEFORE sealing — the table that says "the mechanism touched task X" is written before the verdict, not derived after. Any pre-registration without an explicit firing line is a claim without a measurement.

## HUMAN NOTE
When you test whether a mechanism works, you write down in advance what would count as the mechanism actually firing — on which specific tasks, which specific documents. In this case, a filter was supposed to fire and narrow the corpus, and the verdict said "it fired." But nobody had written down per-task what "fired" meant. It turned out the filter never fired at all on the documents that mattered most (the claim-dense ones kept all 4 of 4 passages), and the mechanism underneath could only ever reach 1 of 3 tasks. The grade was measuring luck, not the mechanism. The fix is simple and general: before you seal a verdict, write the firing table — per task, did the mechanism touch it? — as a blocking line in the pre-registration. If the table can't be written, the verdict can't be sealed.

## CHILD NOTE
Imagine a teacher who says "every student took the test" — but the test was only given to one classroom. The grades would be meaningless for the other two classrooms. A firing table is the attendance sheet: it proves the mechanism actually showed up for each task before anyone gives it a grade.

## GRANDMA NOTE
A gate that can't ever say "no" isn't a gate — it's a hallway. When you check someone's work, first write down exactly which pieces they actually handled. If you grade them on work they never touched, the grade means nothing. The attendance sheet comes first, the grade comes second.

## NAYA NOTE
This is a measurement-integrity lesson with a precise handle: the firing table as a blocking pre-registration line. Pre-registration is the sealed claim made BEFORE the run; a blocking line is one the run cannot pass without satisfying. Making the per-task firing table blocking means the machinery — not anyone's memory — owns the gate: no table, no sealed verdict. Note the pair with the "distillation emits pairs" pattern (SN-1435): here the repair lands the mechanism (restore the table) AND the visibility (blocking line pre-seal). Cold-successor value: whenever you see a verdict graded on a scope the mechanism couldn't reach, reach for this note first.

## MACHINE NOTE
```json
{
  "sn": "SN-1439",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15T18:38:07-07:00",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": "SYSTEM-INTELLIGENCE/MEASUREMENT-INTEGRITY",
  "decision_change": "When writing a pre-registration for a mechanism test, write the per-task firing table as a blocking line before sealing; refuse to seal any verdict whose graded scope exceeds the table's touched set.",
  "falsifiability": "Produce a corpus-wide firing claim where the per-task table and the corpus-wide claim yield identical verdicts across multiple mechanisms; then the blocking-line requirement is unnecessary for that class.",
  "mechanism": "A non-discriminating predicate (can't say no) collapses mechanism performance into corpus luck; the per-task firing table makes the mechanism's actual reach visible, so the grade measures the mechanism, not the filter.",
  "evidence": [
    "learning-events-2026-10-15-18.md (CANDIDATE 437)",
    "hidden_files/twelve-lane-receipts/gap-t0593-lane4.md (2026-10-15)"
  ],
  "related": ["SN-1435 two-layer backstop repair", "SN-1424 falsification routes the repair"]
}
```
