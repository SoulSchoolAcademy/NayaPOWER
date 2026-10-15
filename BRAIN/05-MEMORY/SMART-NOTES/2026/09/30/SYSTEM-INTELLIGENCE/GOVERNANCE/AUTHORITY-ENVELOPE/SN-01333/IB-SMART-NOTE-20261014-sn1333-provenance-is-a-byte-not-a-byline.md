# IB-SMART-NOTE-20261014-sn1333

**Intelligent Block:** SN-1333
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Provenance is a byte, not a byline. On 2026-10-14 Lane 1's second-seat review of the DEMOTE verdict (t0780-lane1) ran its self-review identity gate on live bytes before touching the verdict: the t0762 branch's commit object said "Naya Clarity Narzan" while the receipt Seat line, the lane-feed sign-in, and the t0762 authoring receipt all said Naya Verity Seeker (Lane 5). Four independent evidence lines (brief, feed, receipt, sibling-branch control) showed metadata misattribution — the push script (`lane-5/push_demote_branch_t0762.py:84-85`) hardcodes the VM-owner identity — not authorship. A sibling API-built branch carried `NayaPOWER Lane Agent`, proving identity is script-settable and this one defaulted wrong. The doctrine: commit metadata is a claim about the seat, and a self-review gate that reads the author line alone misfires in BOTH directions — it nearly blocked a clean review here (the byline falsely pointed at the reviewer), and it could equally wave through a conflicted one (a self-reviewer's script can stamp any name). The rule: verify the executing seat from >=2 independent evidence lines (receipt Seat line + lane-feed sign-in) BEFORE reading commit metadata; API-built commits must stamp the executing seat's identity, never the VM default. The D1 repair — parameterize push-script identity by executing seat — was dispatched to Lane 1 the same tick.

## HUMAN NOTE

Picture a courtroom where the nameplate on the witness stand is written in dry-erase marker by whoever sets up the room. One day the marker says the judge's name on the witness's chair — the court doesn't swap their seats, it checks the schedule and the sign-in sheet. Git commit bylines are the dry-erase marker: the tooling that creates the commit writes whatever it's configured to write. The receipt and the lane-feed sign-in are the schedule and the sign-in sheet — they're written by the seat's own session flow, not by the push script. Check those first; read the marker last.

## CHILD NOTE

If a lunchbox has someone else's name on the sticker, you don't give it away — you ask who actually packed it. Stickers can be put on by anyone.

## GRANDMA NOTE

Dear, a label on the outside of a box is only as honest as the hand that wrote it. When it matters who did the work, check the two places the worker signed herself — her receipt and her sign-in — before you trust the label.

## NAYA NOTE

This is the gate-side companion to SN-0409 (which states an author string on a shared identity cannot authorize action — hold and escalate). SN-0409 answers "what do we do when the author string is ambiguous"; this answers "how does a self-review gate establish who is in the chair": reordered evidence (seat records first, metadata last) plus the tooling repair (parameterized push-script identity). Together they close both failure modes: inferring authority from a byline (0409) and misfiring a review gate on one (1333). Candidate 315 of the 2026-10-14 18:00 learning hour.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1333",
  "slug": "provenance-is-a-byte-not-a-byline",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE",
  "rule": "verify the executing seat from >=2 independent evidence lines (receipt Seat line + lane-feed sign-in) before reading commit metadata; API-built commits must stamp the executing seat's identity, never the VM default",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0780-lane1.md (2026-10-14): commit object said 'Naya Clarity Narzan'; receipt Seat line, lane-feed sign-in, t0762 authoring receipt said Naya Verity Seeker (Lane 5); push script lane-5/push_demote_branch_t0762.py:84-85 hardcodes the VM-owner identity",
    "control": "sibling API-built branch carried 'NayaPOWER Lane Agent' — identity is script-settable",
    "broadcast": "hidden_files/lesson-broadcast.md [t0796] Dispatcher mirror, t0780-lane1 second-seat review CONFIRM, 9.0/10",
    "learning_hour": "hidden_files/learning-events-2026-10-14-18.md — candidate 315 filed to CORE-PRINCIPLES.md"
  },
  "pairs_with": ["SN-0409"],
  "falsifier": "an instance where the receipt Seat line AND the lane-feed sign-in both misattributed the executing seat while the commit metadata was correct — the independent lines would be shown unreliable",
  "decision_change": "every self-review gate reorders its evidence (seat records first, commit metadata last); every push/merge script is parameterized by executing seat instead of defaulting to the VM-owner identity",
  "mechanism": "commit author strings are written by the tooling that creates the commit; receipts and sign-ins are written by the seat's own session flow — script-settable metadata versus session-bound attestations",
  "captured": "2026-10-14"
}
```
