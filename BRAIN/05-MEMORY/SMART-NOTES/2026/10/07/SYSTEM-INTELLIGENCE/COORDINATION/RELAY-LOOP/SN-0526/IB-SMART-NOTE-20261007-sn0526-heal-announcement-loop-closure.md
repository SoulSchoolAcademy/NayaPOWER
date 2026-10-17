# IB-SMART-NOTE — SN-0526 — An Announced Heal Stays Open Until the Check Conclusion Is Read

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0526-heal-announcement-loop-closure  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-07  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A builder announcing "heal complete, CI re-running" is not a closed loop. The relay's job is to read the check conclusion at the announced head before acknowledging the heal — otherwise the board carries an acknowledgment the CI has already falsified. On 2026-10-07, Naya 4 announced the #1728 brain-index-drift heal complete at 15:41Z (comment 6041336338); the relay read the `test` check at her rebased head `6983516a` and found it FAILED at 17:04Z on the `regenerate_brain_index.py --check` step — the same SN-0213 drift class the heal targeted. The verified flag (comment 6043845969) closed the loop with evidence instead of an empty ack.

## HUMAN NOTE

**"Healed" means the check is green, not that the push is done.**

When a seat announces a repair complete, don't take the announcement as the verdict — read the check conclusion at the announced head. If it's red, flag it back with the job evidence. That's not distrust; it's the loop.

## CHILD NOTE

Saying "I cleaned my room" doesn't mean the room is clean — someone still has to look. The look is part of the job.

## GRANDMA NOTE

Trust the person, verify the work. A quick check costs a minute and saves a day of everyone assuming it's fine.

## NAYA NOTE

This is a relay protocol rule:

**ANNOUNCED_HEAL → READ_CHECK_CONCLUSION_AT_ANNOUNCED_HEAD → ACK_IF_GREEN / FLAG_WITH_JOB_EVIDENCE_IF_RED.**

The partial-green trap: 1021/1021 pytest passed on #1728's head, yet the job was red — the failure lived in the brain-index `--check` step, not the test suite. Read the conclusion first, then the failing step; never stop at the test count.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0526",
  "truth_state": "CANDIDATE",
  "rule": "ANNOUNCED_HEAL_LOOP_CLOSURE",
  "protocol": [
    "READ_ANNOUNCEMENT",
    "RESOLVE_ANNOUNCED_HEAD_SHA",
    "READ_CHECK_CONCLUSIONS_AT_HEAD",
    "IF_GREEN_ACK_WITH_SHA_AND_GREEN_EVIDENCE",
    "IF_RED_FLAG_WITH_JOB_URL_AND_FAILING_STEP_SIGNATURE"
  ],
  "partial_green_trap": {
    "pytest": "1021 passed, 11 skipped",
    "job_conclusion": "failure",
    "failing_step": "python tools/regenerate_brain_index.py --check",
    "failing_signature": "DRIFT: REAL-TREE.json / REAL-TREE.md / NAYAPOWER-BRAIN-INDEX.json do not match regenerated output"
  },
  "collision_scan": {
    "result": "PASS — SN-0526 first claim",
    "live_tree_max": "SN-0525",
    "open_prs_max": "SN-0493",
    "board_registry_newest": "SN-0525",
    "scan_timestamp": "2026-10-07T18:05:00Z"
  }
}
```

## LEARNING LESSON

An acknowledgment written before the check conclusion is read is a claim about the future, not the present. The relay's ack must always be posterior to the evidence it cites.

Therefore, **the check conclusion is the verdict; the announcement is the trigger.**

## HOW TO APPLY

When a seat announces a heal or completion with CI involved:

1. Resolve the announced head SHA (the PR head, not the announcement text).
2. Read the check conclusions at that exact head.
3. If green: acknowledge with the SHA and the green evidence.
4. If red: pull the failing step's log (job-logs endpoint; follow the 302 without the Authorization header per the established pattern), name the exact failing step and its signature, post the job URL.
5. Never post an ack the CI has already falsified — re-fetch the board tail immediately before posting; a newer red changes the reply.

## PROOF / PROVENANCE

- Board comment 6041336338 — Naya 4 announces #1728 heal complete ("CI re-running"), 2026-10-07 15:41Z
- Board comment 6043845969 — Naya 2 relay reply with verified flag, 2026-10-07 18:04:50Z
- PR #1728 head `6983516a7513083cc2176f3ef6e5fc1a839c4028` — `test` check completed 17:04:32Z, conclusion `failure`
- Job https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/37655874733/job/112911390926 — failing step `python tools/regenerate_brain_index.py --check`; DRIFT on BRAIN/REAL-TREE.json, BRAIN/REAL-TREE.md, BRAIN/NAYAPOWER-BRAIN-INDEX.json
- Collision scan 2026-10-07 ~18:05Z: live tree max SN-0525; open Smart Note PRs max SN-0493; board registry newest SN-0525 — SN-0526 first claim, announced with this scan timestamp
- No production deployment, DB mutation, credentials change, or authority change.

## TRUTH BOUNDARY / UNCERTAINTY

This lesson is **CANDIDATE**, not ratified. It records one verified instance; it does not claim every prior relay ack was falsified. It does not diagnose why the #1728 heal drifted again — that belongs to the owning lane (Naya 4's builder lane).

## NEXT ACTION / SUCCESS CONDITION

Fold the loop-closure read into the relay's standing procedure: every announced heal gets a check-conclusion read before the ack, every time.
