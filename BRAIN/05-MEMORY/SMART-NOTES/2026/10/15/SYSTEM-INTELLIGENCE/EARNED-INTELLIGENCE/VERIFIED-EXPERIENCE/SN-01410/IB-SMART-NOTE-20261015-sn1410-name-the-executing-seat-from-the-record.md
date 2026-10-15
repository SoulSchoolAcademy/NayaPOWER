# SN-1410 — Name the Executing Seat from the Record, Never the Habit

- **Intelligent Block:** IB-SMART-NOTE-20261015-sn1410-name-the-executing-seat-from-the-record
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #2537 comment 6196434078 ([LEARNING EVENT], F8 repeat)

## IN A NUTSHELL
The director-pass wrote "#2629 merged by Shawn" from habit. The merge was dock/dispatcher-executed under the protocol grant. Attribution-by-habit is fast and usually right — until it isn't, and the merge record is the one place where "usually right" corrupts the audit trail. The standing rule: name the executing seat from the record — `merged_by`, the merge-commit author on live bytes, the dock authorization — never the habit. If the record is ambiguous, write UNCONFIRMED and keep working; never complete an attribution by autocomplete. A wrong attribution in a merge record doesn't just mislead one reader — it teaches every future seat the wrong executor, and the wrong executor becomes the next habit.

## HUMAN NOTE
Imagine crediting the wrong person for signing a contract. The signature line is right there on the paper — but you wrote the boss's name because he usually signs. Now the file says the boss signed, and everyone who reads the file learns the wrong thing. Read the signature line. Every time.

## CHILD NOTE
If your teacher asks who cleaned the classroom and you say "Maya" because Maya usually does it — but today it was Sam — then Sam never gets the thank-you, and tomorrow everyone will say Maya again. Look at who actually did it. That's the only name that counts.

## GRANDMA NOTE
Don't guess who did the work — check. The person who usually does it isn't always the person who did it this time, and writing down the wrong name in the record book causes trouble later. When in doubt, leave it blank and find out.

## NAYA NOTE
Cold successor: every attribution claim in a board post, receipt, or merge record names the executing seat from the record — `merged_by` on the API, the merge-commit author verified on live bytes, the dock/dispatcher authorization that granted the execution. The failure mode is attribution-without-receipt-read: under time pressure, cognition autocompletes the most frequent actor (F8: "#2629 merged by Shawn" written from habit for a dock/dispatcher-executed merge). New surface this instance: the habit wasn't carelessness, it was the true most-likely actor — which is exactly why habit is dangerous here. Ambiguous record → mark UNCONFIRMED, never fill it in. The merge audit trail is read, not predicted.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn1410-name-the-executing-seat-from-the-record",
  "sn": "SN-1410",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "EARNED-INTELLIGENCE",
  "subcategory": "VERIFIED-EXPERIENCE",
  "lesson_type": "FAILURE_CLASSIFICATION",
  "evidence": {
    "board": "#2537",
    "comments": [6196434078],
    "instance": "director-pass wrote '#2629 merged by Shawn' from habit; merge was dock/dispatcher-executed under the protocol grant",
    "family": "F8 repeat; new surface: attribution-without-receipt-read"
  },
  "rule": "name the executing seat from the record (merged_by, merge-commit author on live bytes, dock authorization), never the habit; ambiguous record -> UNCONFIRMED",
  "decision_change": "every merge/attribution claim in board posts and receipts cites the executing seat from the record; ambiguous attributions are marked UNCONFIRMED instead of completed by habit",
  "falsifier": "the record (merged_by, commit author, authorization) either names the seat or it doesn't — any attribution claim can be checked against it",
  "mechanism": "under time pressure cognition autocompletes the most frequent actor; the merge audit trail requires record-reading, not pattern-completion"
}
```
