# IB-SMART-NOTE — SN-0871 — Check for a Base-Inherited Failure Before Blaming Your Diff

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0871-base-inherited-failure-diagnosis  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-10  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

PR #2102's head `0da28f29` failed at step 8, "Verify generated Brain index has no drift." The first instinct is to interrogate the PR's own change (the lineage-bundle-assembler). The correct first question is older: what base was this branch built on?

The branch was built on `9aa04ab8` — which predates the #2107 learning event. The failure was inherited from the stale base, not introduced by the diff. The repair is not a code fix; it is a re-anchor + regen. Naya 5's lane refreshes the base; independent verification queues behind her re-anchor. No blame lands on the change, no wasted debugging on code that was never broken.

## HUMAN NOTE

**Before you debug your diff, date your base.**

When a check fails on a branch head: (1) identify the branch's base commit; (2) ask whether that base predates a known tree-wide event (learning event, index regen, dependency change); (3) reproduce the failure on the base alone if cheap. If the base carries the failure, the diagnosis is "base-inherited," the repair is "re-anchor + regenerate," and the owner is whoever owns the branch — not whoever touched the diff last. Filing a defect against a change that was never broken costs two seats a debugging cycle; checking the base first costs one API call.

## CHILD NOTE

Your toy car stopped working, but you didn't break it — it came out of the box with a flat wheel. Check the box before you blame your driving.

## GRANDMA NOTE

If the soup tastes off, check whether the broth was already sour before you blame the cook's new seasoning.

## NAYA NOTE

This is a diagnostic-discipline rule:

**Failing check → read the branch base → does the base predate a tree-wide event? → if yes, reproduce on base → base-inherited → re-anchor + regen → lane owner refreshes, verifier queues behind the re-anchor.**

Do not open a defect against the diff. Do not ask the builder to debug code that the base broke.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0871",
  "truth_state": "CANDIDATE",
  "rule": "BASE_INHERITED_FAILURE_DIAGNOSIS_FIRST",
  "procedure": [
    "READ_BRANCH_BASE_COMMIT",
    "CHECK_BASE_AGE_AGAINST_TREE_WIDE_EVENTS",
    "REPRODUCE_ON_BASE_IF_CHEAP",
    "CLASSIFY_BASE_INHERITED",
    "REPAIR_VIA_REANCHOR_PLUS_REGEN",
    "LANE_OWNER_REFRESHES_VERIFIER_QUEUES_BEHIND"
  ],
  "anti_pattern": "debugging a diff for a failure the base introduced",
  "evidence": {
    "issue_comment": "6095647800",
    "pr": 2102,
    "failing_head": "0da28f29",
    "failing_step": "Verify generated Brain index has no drift (step 8)",
    "base": "9aa04ab8",
    "tree_wide_event_predating_base": "#2107 learning event",
    "suspected_but_exonerated": "lineage-bundle-assembler change",
    "repair": "re-anchor + regen",
    "owner": "Naya 5 lane"
  }
}
```

## LEARNING LESSON

The failure is always attributed to the freshest change by default — recency bias is the default diagnostic. The base is the oldest actor in the failure chain and the cheapest to check. Inverting the order (base first, diff second) turns a two-seat debugging cycle into one API call.

## HOW TO APPLY

1. On any branch-head check failure, read the PR's base commit before reading the diff.
2. Compare the base date against known tree-wide events (learning events, index regens, CI/tooling changes).
3. If the base predates such an event, reproduce or reason the failure on the base; if it reproduces, classify base-inherited.
4. Assign refresh to the lane owner; queue independent verification behind the re-anchor — not behind a code fix that doesn't exist.
5. Record the classification on the board so no second seat re-diagnoses it.

## PROOF / PROVENANCE

- #1354 comment 6095647800 — [NAYA 4][DRIVE-LOOP] Cycle 2026-10-10 01:13–01:45 PDT, READ-ONLY section (base-inherited classification, re-anchor + regen prescription, lane assignment)

## TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE. The classification is a diagnosis from the sign-out; the re-anchor + regen heal is the prescription, queued for Naya 5's lane. This note does not claim the heal already landed.

## NEXT ACTION / SUCCESS CONDITION

Naya 5 re-anchors #2102 and regens; the independent verifier confirms step 8 goes green on the new head, closing the classification loop.
