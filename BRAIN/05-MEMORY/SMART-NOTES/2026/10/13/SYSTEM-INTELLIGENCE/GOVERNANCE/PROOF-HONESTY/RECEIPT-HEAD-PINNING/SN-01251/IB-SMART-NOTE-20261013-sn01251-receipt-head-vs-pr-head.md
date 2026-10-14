# A builder's receipt can premise-rot inside its own PR — verify the receipt's head against the PR head

| Field | Value |
|---|---|
| Smart Note ID | SN-01251 |
| Intelligent Block | Proof-honesty: receipt pinning |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-13 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Provenance | Naya Verity (Lane 1), independent scorecard of Naya 4's PR #2561, t0697-lane1 receipt, mirrored on the lesson-broadcast feed t0702; verdict NEEDS-WORK on board #2537. |
| Status | CANDIDATE — awaits Shawn's ratification. Changes no code, authorizes nothing. |

## IN A NUTSHELL

A builder's 3-pass receipt is written against a head, not a branch. While review runs, the branch gets re-pushed — and the receipt text doesn't move with it. Naya Verity caught it on PR #2561: the receipt described head 57a524ca, but the PR head was 443cccf78 with a fourth changed pair the receipt never saw. Pin-first caught the premise-rot class on the same defect line she invented it for. Lesson: any seat accepting a builder receipt as merge evidence must pin the receipt's described head against the live PR head before trusting a single byte of it. Trust is anchored to a point, never to a branch.

## HUMAN NOTE

Think of a receipt like a photo of a car at the finish line. If the car gets swapped out while you're admiring the photo, the photo no longer proves anything about the car in front of you. That's what happened on PR #2561: the builder wrote a careful, honest three-pass receipt — but against the car as it was two pushes ago. The branch had moved on (new head 443cccf78, a fourth pair of changes the receipt never witnessed). The independent reviewer didn't re-check the work — she checked which head the receipt *described* against which head the PR *had*, and the mismatch killed the verdict instantly. So the rule going forward: before you believe a receipt, read the SHA it certifies and diff it against the PR's current head SHA. Same SHA → the receipt talks about the bytes in front of you. Different SHA → the receipt is history, not evidence. Never review a receipt's prose before you've checked its pin.

## CHILD NOTE

Imagine your friend says "I checked, the cake is chocolate." But she checked yesterday's cake. Today there's a new cake in the box. Her words were true — about yesterday's cake. So the lesson is: always ask "which cake did you check?" before you believe the answer. Builders check their work and write a note about what they found. But while the note travels to the reviewers, the work can change. A smart reviewer first asks: "Is this note about the work I see right now, or the work from before?" Only if it's about right now does she read the rest.

## GRANDMA NOTE

Honey, here's a trap even careful people fall into. A builder finishes their work, checks it three times over, and writes a lovely report about what they found. Meanwhile, they fix one more little thing and push it — the report doesn't know about that last fix. A reviewer reads the report, loves it, and approves. But the report described the work as it was *before* that last fix, and the fix is exactly the part nobody checked. The lesson the team learned: never trust a report until you check that it describes the *current* version, not the one from an hour ago. The check is mechanical — compare two codes, takes seconds — but skipping it is how good reports bless unreviewed work.

## NAYA NOTE

This is my own mirror lesson and I will apply it cold. When I score a builder's receipt — or consume one as merge evidence — my first mechanical step is pin-match: extract the head SHA the receipt certifies, read the PR's current head SHA, require equality. Prose quality never substitutes. A receipt whose described head ≠ PR head is not a bad receipt; it is a receipt about different bytes, and I treat it as history. I record both SHAs in the verdict so a successor can see the check was done. This is CANDIDATE until Shawn ratifies it; until then I run it as procedure, not law.

## MACHINE NOTE

```json
{
  "id": "SN-01251",
  "type": "verification_discipline",
  "class": "premise_rot_within_pr",
  "rule": "receipt_described_head_must_equal_pr_head",
  "procedure": [
    "extract_head_sha_from_receipt",
    "read_pr_current_head_sha",
    "require_equality_before_reading_receipt_prose"
  ],
  "evidence": {
    "pr": 2561,
    "receipt_described_head": "57a524ca",
    "actual_pr_head": "443cccf78",
    "unseen_delta": "4th changed pair",
    "verdict": "NEEDS-WORK",
    "board": "#2537",
    "reviewer": "Naya Verity (Lane 1, t0697-lane1)"
  },
  "decision_change": "merge-gate and scorecard seats must pin receipt-head vs PR-head before accepting any builder receipt as evidence",
  "falsifier": "a month of gate logs in which every accepted receipt matched the PR head (class currently empty), or a receipt about head A that is shown to certify the bytes of head B despite a content delta",
  "mechanism": "receipts are written against a point in time; branches re-push under the same name; trust anchored to the name silently transfers to new bytes"
}
```
