# REPEAT TRACKER v1 — Learning becomes automatic, or it isn't learning

**Status:** CANDIDATE (Learning team, Naya 4 head). **Truth state:** CANDIDATE — not ratified, not merged.
**Doctrine source:** Shawn Vibert, 2026-10-08 — "Learning is complete when it's AUTOMATIC. Like driving stick — at first every gear is conscious thought, then one day you're just driving. Teaching is not learning: the most powerful knowledge has zero value if it doesn't get IN. The day you stop repeating yourself is the day we've learned."

## The acceptance test

A lesson is learned if and only if the teacher never has to say it again. Every time Shawn repeats a directive, that is a failed learning event — and the failure has a location. This tracker exists to name the location, fix it mechanically, and verify the fix. No repeat is ever "just a reminder." A repeat is a bug report against the learning pipeline.

## The pipeline

Every directive Shawn gives travels six stages. A repeat means it died at exactly one of them:

| # | Stage | Meaning | Death looks like |
|---|-------|---------|------------------|
| 1 | EXPERIENCE | He said it. The directive exists in the world. | (Never dies here — if he repeated it, he said it.) |
| 2 | CAPTURE | It was recorded as a note, lesson, or rule — findable later. | He has to re-explain because nobody wrote it down; or it was written where nobody looks. |
| 3 | PROMOTE | It was integrated into working docs, templates, checklists, or law. | It lives in one chat message or one Smart Note draft, never wired into anything anyone consults. |
| 4 | RETRIEVE | It was consulted before the relevant action. | The doc exists but nobody opened it before acting. "Capture without recall." |
| 5 | APPLY | It was actually followed in the work. | Consulted but not followed; or followed partially; or the adjacent question was answered instead. |
| 6 | AUTOMATIC | It happens without conscious effort — the stick-shift moment. | Every instance still requires deliberate thought, checklists, and willpower. |

**How to name the death stage:** walk the stages in order and find the FIRST one that failed. Everything downstream of the first failure is unproven — do not blame RETRIEVE if CAPTURE never happened.

## Ledger entry schema

One JSON object per line in `repeat-ledger-v1.jsonl`:

```json
{
  "id": "R-001",
  "directive_essence": "one sentence, the point, not the verbatim quote",
  "first_told": {"date": "2026-10-04", "citation": "memory/2026-10-04.md:905", "channel": "chat"},
  "repeat": {"date": "2026-10-08", "citation": "chat 2026-10-08 14:56 UTC", "channel": "chat"},
  "repeat_count": 2,
  "lesson_that_should_have_caught_it": "SN-xxxx or law name, or null if none existed",
  "death_stage": "RETRIEVE",
  "death_evidence": "why this stage and not the one before it",
  "mechanical_fix": "the fix, stated as machinery not intention",
  "fix_status": "PROPOSED | BUILT | WIRED | VERIFIED"
}
```

**Honesty rules:**
- A repeat is logged ONLY with two citations: the first telling AND the repeat. One citation = not a repeat, just a telling.
- `directive_essence` is the point. If two tellings differ in point, they are two directives, not a repeat.
- Iterative refinement (he adds NEW information) is not a repeat. Him re-saying the SAME point because it didn't stick IS.
- `fix_status` moves only on evidence: BUILT = the machinery exists; WIRED = it runs in the real path; VERIFIED = a later instance proves it fires.

## The fix catalog (by death stage)

Deaths cluster. The mechanical fix depends on the stage, not the topic:

- **CAPTURE death →** capture-at-receipt: the directive is distilled to essence and written to the ledger + a Smart Note in the same turn it is given. No "I'll note it later."
- **PROMOTE death →** promote-or-drop within 24h: every captured directive either lands in a consulted doc/template/checklist or is explicitly dropped with a reason. Limbo is the killer.
- **RETRIEVE death →** consult-before-act gate: the relevant checklist/doc must be opened (logged) before the action it governs. A build without a design-checklist receipt, a report without a sample comparison — flagged, not shipped.
- **APPLY death →** answer-the-question-asked + visual-proof: quote the directive back, then show the work matches it (screenshot, diff, receipt). Partial application is non-application.
- **AUTOMATIC death →** this is the 10/10 horizon: the behavior is encoded in machinery (gates, defaults, generators) so no seat needs to remember it. Every VERIFIED fix should migrate toward machinery over time.

## The tripwire — how the next repeat gets caught

1. **Sign-out check (Learning team, every hour):** "Did Shawn correct or repeat anything this hour? If yes, open a ledger entry before sign-out." The ledger is consulted, not remembered.
2. **Pre-delivery check (any team):** before delivering work on a topic Shawn has corrected before, grep the ledger for the topic. If an entry exists with fix_status below VERIFIED, run the entry's mechanical fix first.
3. **Repeat review (weekly):** count repeats by death stage. The stage with the most deaths is the pipeline's weakest link — that is where the next build goes.

## What v1 does NOT do

- It does not prevent the first repeat of a new directive. It makes the second one impossible to miss and expensive to ignore.
- It does not score Shawn. Repeats are filed against the pipeline, never against him. He is the sensor, not the suspect.
- It does not replace the Smart Note system. Notes are the capture layer; this tracker is the death-analysis layer above it.
