# IB-SMART-NOTE — SN-0840 — Ratification Lives in the Artifact's Fields, Not the Commit Message

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0840-ratification-lives-in-artifact-fields  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-09  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

The Law of One merge said RATIFIED in its commit message, but the three law files still carried DRAFT status (`"ratified": false`). A cold Naya reading those files — the constitutional text itself — would conclude the law is not ratified. That is a lie in constitutional law. The commit message talks to the log; the file's status fields talk to every future reader. The repair (PR #2085) changed the files, not the law: no re-ratification, no content change — just making the artifacts honest about what Shawn already ratified on 2026-10-09.

## HUMAN NOTE

**A status claim written anywhere but in the artifact is not a ratification.**

Commit messages, PR titles, and chat receipts are where a ratification gets *announced*. The artifact's own fields are where it gets *recorded*. When the two disagree, the artifact wins — because the artifact is what the cold successor reads. Rule: after any ratification is recorded, verify the artifact bytes carry it, on the exact merged head. If the file still says DRAFT, the ratification has not landed.

Related precedent: SN-0654 (a ratified document's machine binding is proven against the tree, never the document); SN-0835 (diagnostic status claims expire — verify against current bytes).

## CHILD NOTE

If the teacher writes "PASSED" on the chalkboard but your report card still says "not graded," the report card is what the next school reads. Fix the report card.

## GRANDMA NOTE

A name on the mailbox is what the mailman uses. It doesn't matter what the landlord told you in the hallway — if the mailbox still has the old name, the letters go to the wrong person. Write the new name on the mailbox itself.

## NAYA NOTE

This is a constitutional-integrity rule:

**Ratified state → artifact status fields must carry it → verified on merged head.**

- Authority for the state: the ratification record (Shawn's word, receipt, scorecard).
- Authority a future reader trusts: the artifact's own fields.
- Forbidden proxies: commit message, PR title, chat announcement — none of these can stand in for the artifact's fields.
- Repair shape when they disagree: fix the files to match the record (PR #2085 pattern). Do NOT re-ratify, do NOT change content, do NOT treat the mismatch as evidence the ratification didn't happen.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0840",
  "truth_state": "CANDIDATE",
  "rule": "RATIFICATION_LIVES_IN_ARTIFACT_FIELDS",
  "check": {
    "for_every_ratified_law_file": "artifact.status_fields.ratified == true on the merged head bytes",
    "when": "after any ratification is recorded",
    "forbidden_status_authorities": ["commit_message", "pr_title", "chat_announcement"]
  },
  "mismatch_repair": {
    "do": ["update artifact fields to match the ratification record", "verify on merged head"],
    "do_not": ["re-ratify", "change law content", "treat mismatch as non-ratification"]
  },
  "evidence": {
    "board_comment": 6091596153,
    "repair_pr": 2085,
    "symptom": "merge commit said RATIFIED; three law files carried DRAFT / \"ratified\": false"
  },
  "related": ["SN-0654", "SN-0835"]
}
```

## LEARNING LESSON

Constitutional truth is byte-level. If the record says one thing and the file says another, the system has lied to its future self — and the only repair a cold successor will ever trust is the file telling the truth.

Evidence: NayaPOWER #1354 comment 6091596153 ([NAYA 2][SCORECARD] PR #2085 — Law of One ratification fix, 2026-10-10T00:26:23Z); repair PR #2085 (status-field fix, no content change, no re-ratification). Related: SN-0654, SN-0835.
