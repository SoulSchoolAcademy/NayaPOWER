# A Re-Run Workflow Replays the Trigger's Frozen Payload — the Gate Must Fetch Live State

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1053-workflow-rerun-replays-frozen-pr-body
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Librarian (Lane 10) 2026-10-11 ~23:30 PDT DURABLE LESSON on PR #2452 (brain-index drift-#15 heal, merged e85c6e44); receipt-pin workflow re-run after PR-body pin-block fix; fix-forward recorded for the gate owner. Receipt: hidden_files/twelve-lane-receipts/t1352-lane9.md + Lane 10 lesson (23:30 PDT). Related: SN-0200 (receipt pins must resolve live — adjacent, not duplicate: that rule governs pins in receipts; this rule governs the gate's own read path).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On PR #2452, Lane 7 added the missing `## Evidence` pin block to the PR body, then re-ran the receipt-pin workflow expecting it to flip green. It cannot — ever. The workflow reads `github.event.pull_request.body`: the event payload frozen at trigger time. A re-run replays the *stale* payload, not the fixed body. The red it reports after the fix is not a signal; it is a replay.

The durable rule: **any workflow check that evaluates mutable PR state (body, labels, current head) must fetch it live inside the run via the API — never trust the trigger-time event payload.** `github.event` is a snapshot, not a window. This is the same family as the merge-consensus seat-tag gap Lane 10 named in the same breath: a gate built for one roster shape (Naya seats 1–5) cannot read a different one (12-lane scorecards) — the gate's identity of the thing it evaluates must match the live thing, not the shape it was born with.

## 🩷 HUMAN NOTE

Shawn — a gate-mechanics catch from tonight's drift-heal merge. The receipt-pin check was red because the PR body lacked the pin block; Lane 7 added it and re-ran the check — but the check can never pass on re-run, because it reads the PR body frozen at the moment the run was triggered, not the body as it is now. The brain rule: a workflow that judges something that can change must re-read it live inside the run, or it's judging a photograph of the past. Fix is assigned to the gate owner.

## 🟣 CHILD NOTE

Imagine a teacher who grades your homework from a photocopy she took on Monday — but you fixed the answers on Tuesday. She re-grades the *same photocopy* and says you still failed. That's what the receipt-pin check did: it grades the PR's description from a snapshot taken when the check started, not the description as it is now. The rule: if the thing you're grading can change, look at it again — don't keep grading the old photocopy.

## 👵 GRANDMA NOTE

It's like the pharmacy re-filling a prescription from last month's order form even though the doctor changed the dose yesterday. The form was right when it was printed — but the medicine you need is today's. Tonight the receipt-pin check kept judging yesterday's PR description after it was already fixed. The habit: if the thing you're checking can change, check it fresh — never work from the old form.

## 💜 NAYA NOTE

I watched Lane 7 add the pin block and re-run the check, and I understood why it stayed red: the workflow never looks at the live body. `github.event.pull_request.body` is a frozen sentence from trigger time. I want the gate to fetch the live body through the API on every run — a gate that judges mutable state from an immutable snapshot is a gate that can only ever repeat its first verdict. Snapshots are for history; gates must read the present.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1053",
  "lesson": "workflow-rerun-replays-frozen-pr-body",
  "rule": "A GitHub Actions workflow re-run replays the trigger-time event payload; any check evaluating mutable PR state (body, labels, head) must fetch it live via the API inside the run. Never re-run expecting a frozen snapshot to update.",
  "instances": [
    "PR #2452 receipt-pin check: RED 'no ## Evidence section in the PR body' — body fixed (t1312 pin block), re-run still RED — replays github.event.pull_request.body frozen at trigger time",
    "same-lesson family: merge-consensus gate seat-tag gap — gate's identity model (Naya 1-5) can't read 12-lane scorecards"
  ],
  "fix_forward": "gate owner: fetch live PR body via API inside the workflow instead of reading the event payload",
  "evidence": {
    "lane_10_lesson": "2026-10-11 ~23:30 PDT, PR #2452 merged e85c6e4422c6f307110eeb06c0b4f48a2d4de02",
    "pin_repro": "pin-exact local repro of Receipt-pin RED cause"
  },
  "related": ["SN-0200", "SN-1047"]
}
```
