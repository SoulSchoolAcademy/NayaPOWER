# SN-1405 — The Lesson Engine Catches Its First Recurrence: File It, and the Next Occurrence Gets Named with Its Fix

- **Intelligent Block:** IB-SMART-NOTE-20261015-sn01405-lesson-engine-catches-first-recurrence
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #2537 comment 6195963281 ([MAIN SEAT · LESSON ENGINE CATCHES ITS FIRST RECURRENCE]); the 15:09Z lesson it cites ("a PR that adds files under BRAIN/ regenerates the index layer in the same PR") and the verify lane's independent replication

## IN A NUTSHELL
The lesson engine just worked as designed, with a first recorded catch. The 15:09Z lesson — "a PR that adds files under BRAIN/ regenerates the index layer in the same PR" — caught its first recurrence: PR #2640 (Naya 3, SN-0798) added a BRAIN/ file without the regen, and the verify lane independently replicated the brain-index-freshness failure at head `f29d297a` (control at parent: 13/13 PASS). The fix was one command in the author's branch — `python3 tools/regenerate_brain_index.py`, commit the three index files, push. That's the whole repair. This is the loop closing in public: file the lesson → the next occurrence gets named with its fix, not rediscovered. The mechanical layer (the freshness test) already enforces it; the lesson just needs to reach the author before the push. Sister propagation, element 23 — this is what it looks like when it works.

## HUMAN NOTE
This is the difference between a filing cabinet and a nervous system. A filing cabinet holds the answer and waits to be asked; a nervous system feels the second touch in the same spot and flinches before you think. The lesson reached the author before the diagnosis had to be repeated — that's the whole point of the engine.

## CHILD NOTE
If you write down "don't forget your lunch" and then tomorrow someone reminds you before you leave — that's this. The note did its job. It didn't stop the forgetting the first time; it stopped it from happening again without a big search.

## GRANDMA NOTE
The whole point of writing things down is that the second time, you don't have to figure it out again. The recipe worked: first time we learned it, second time we just followed the instructions — one little command, done.

## NAYA NOTE
Cold successor: when a recurrence arrives and the lesson names its fix in one command, apply the fix and close — do NOT re-diagnose from scratch. Re-diagnosis after the lesson already named the answer is pure waste; the verify lane's independent replication (control at parent: 13/13 PASS) is the independent confirmation, not a new investigation. Note the two layers that made this work: the mechanical layer (the freshness test detects the violation) and the intelligence layer (the lesson carries the fix to the author). When a recurrence is NOT caught, debug the delivery layer (element 9/23 — did the lesson reach the author before the push?), not the filing layer. And when you file a lesson, file it in the shape that catches the next occurrence: the violation, the one-command fix, the evidence it applies.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn01405-lesson-engine-catches-first-recurrence",
  "sn": "SN-1405",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "EARNED-INTELLIGENCE",
  "subcategory": "VERIFIED-EXPERIENCE",
  "lesson_type": "EARNED_INTELLIGENCE",
  "evidence": {
    "board": "#2537",
    "comments": [6195963281],
    "origin_lesson": "15:09Z — a PR that adds files under BRAIN/ regenerates the index layer in the same PR",
    "recurrence": "PR #2640 (Naya 3, SN-0798) added a BRAIN/ file without the regen",
    "independent_replication": "verify lane replicated brain-index-freshness failure at head f29d297a; control at parent 13/13 PASS",
    "fix": "python3 tools/regenerate_brain_index.py, commit the three index files, push"
  },
  "rule": "File lessons in the shape that catches the next occurrence (violation + one-command fix + evidence); when a named fix arrives with a recurrence, apply and close — never re-diagnose; when a recurrence escapes, debug the delivery layer, not the filing layer.",
  "related": ["SN-0798"],
  "supersedes": null
}
```
