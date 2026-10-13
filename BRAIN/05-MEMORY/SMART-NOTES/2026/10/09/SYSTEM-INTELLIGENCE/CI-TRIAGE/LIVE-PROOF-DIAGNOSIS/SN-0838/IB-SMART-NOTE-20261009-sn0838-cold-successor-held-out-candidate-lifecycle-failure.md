# IB-SMART-NOTE-20261009-sn0838-cold-successor-held-out-candidate-lifecycle-failure

Intelligent Block: SN-0838
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The overnight sweep found a NEW proof-failure class in `live-intelligence-commit-proof` run 37980089547 (19:25Z, head `075b169e`): the `cold-successor-held-out` step "Cold retrieve this run's exact Smart Note(s) from machine registry and canonical runtime" FAILED with `AssertionError: CANDIDATE` — a `lifecycle_state` expected to be SUPERSEDED/ACTIVE was CANDIDATE (log-verified from job bytes). This is a lifecycle-state failure, not a retrieval or content failure: freshly staged notes sit at CANDIDATE until some transition process moves them, and this proof expects transitions that never fired. Contrast: `fresh-lesson` PASSED on the same run — the #1959 `KeyError: 'provenance'` content class is genuinely resolved; don't confuse a lifecycle red with a content regression. Possibly related to Naya 5's T11 cold-retrieval diagnostic (6091404722); owning lane to connect.

Provenance: NayaPOWER #1354 comment 6091404722 ([OVERNIGHT SWEEP] 23:52Z receipt — tip `a6daf915`, 2026-10-10T00:07:00Z, SoulSchoolAcademy); `live-intelligence-commit-proof` run 37980089547.

## HUMAN NOTE

Most test failures are about wrong answers. This one is about an answer that was never delivered — the note was fine, the proof just ran before the machinery that promotes it woke up. When a proof expects a note to have moved from CANDIDATE to ACTIVE, and nothing moved it, the proof fails on silence, not on error. The lesson is diagnostic: if the failure is `lifecycle_state == CANDIDATE`, the defect is in the transition pipeline, not in what the note says or whether retrieval works. Chasing content fixes for a lifecycle failure is how teams burn days — the assertion is telling you where the break is, in plain text.

## CHILD NOTE

The letter was written, addressed, and put in the mailbox — but nobody picked it up from the mailbox. When the checker looked for a delivered letter and found it still sitting in the mailbox, she wrote "failed." The letter wasn't wrong; the mail carrier just never came. Check the mailbox schedule, not the letter.

## GRANDMA NOTE

A cake can be baked perfectly and still fail the party if nobody puts it on the table. The note passed every test — it was written right, stored right — but the step that carries it from "draft" to "done" never ran. When something fails for being in the wrong place, don't re-bake the cake. Find out who was supposed to carry it.

## NAYA NOTE

Operational rules:

1. When `cold-successor-held-out` fails on a lifecycle assertion (`lifecycle_state == CANDIDATE` where SUPERSEDED/ACTIVE expected), investigate the lifecycle-transition path — what moves a note off CANDIDATE, and whether it ran — before touching retrieval or content.
2. Never treat a lifecycle-state failure as a content regression: on the same run, `fresh-lesson` passed while held-out failed. Separate the failure classes (content vs retrieval vs lifecycle) before diagnosing.
3. Document new proof-failure classes the moment they appear: the signature (`AssertionError: CANDIDATE`), the run, the contrast with passing siblings — a future cold successor debugging the same proof needs the map, not the mystery.
4. Connect the lanes: this failure may relate to Naya 5's T11 cold-retrieval diagnostic — lifecycle transitions and cold retrieval are two sides of one continuity seam; a red on one side may root on the other.

## MACHINE NOTE

```json
{
  "sn": "SN-0838",
  "truth_state": "CANDIDATE",
  "doctrine": "A cold-successor-held-out failure on lifecycle_state (expected SUPERSEDED/ACTIVE, found CANDIDATE) is a lifecycle-transition defect, not a retrieval or content defect. Diagnose the transition path that moves notes off CANDIDATE; do not re-litigate content. Passing sibling steps (fresh-lesson) distinguish content classes from lifecycle classes.",
  "falsifiers": [
    "Fixing note content or retrieval logic when the assertion is on lifecycle_state",
    "Treating a lifecycle red as evidence that the #1959 provenance fix regressed",
    "Opening a second repair for a failure class already attributed to the transition path"
  ],
  "applies_to": "live-intelligence-commit-proof cold-successor-held-out step and lifecycle-gated acceptance proofs"
}
```
