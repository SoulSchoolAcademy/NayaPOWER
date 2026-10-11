# IB-SMART-NOTE-20261010-sn0879-burst-race-superseded-tip-fail-closed

Intelligent Block: SN-0879
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-10
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

During the 2026-10-10 ~10:14–10:35Z six-PR merge burst, the `promote-and-prove` workflow on intermediate tip `c41ad1a4` (the #2116 tip) failed at "Resolve standing authorization mode". That failure was not a product red and not an auth breach — it was an authorization-resolution race: the workflow was resolving standing authorization against a tip that ceased to be the tip while it was still resolving. The response was fail-closed classification:

1. **Name the artifact** — which exact tip the failure ran against (`c41ad1a4`, the #2116 tip).
2. **Diagnose the race** — the tip moved mid-flight (six merges in twenty minutes), so the failure's evidence refers to a dead tip, not the live tree.
3. **Independently re-verify the FINAL tip** (`fd7f13ec9a25ee0deebfc479132101aaaa6e0879`) three ways: CI check runs re-read (16 runs — 10 success / 6 skipped / zero red), `regenerate_brain_index.py --check` (OK, 1234 files), drift ratchet (12/12), activation-gate tests (67/67, matching the #2117 claim).
4. **Carry nothing forward** — no repair opened, no red filed, no defect attributed. The superseded tip's artifact dies with the tip.

The rule: **a failure whose evidence is anchored on a superseded tip is not a red; it is a race artifact. Chase only the final tip.** Repair work opened against a dead tip is wasted work chasing a ghost — and worse, a "fix" written for a race artifact can introduce a real defect into the live tree.

Distinguishes from: SN-0868 (merge-race — merges landing while their own checks still run; the gate reading "not yet failed" as green), SN-0871 (base-inherited failure — stale base, repair is re-anchor + regen), SN-0493 (a *decision* expires when the tip moves). This is the CI-flight counterpart of SN-0493: *observations* expire when the tip moves, too.

Provenance: NayaPOWER #1354 comment 6096691019 ([NAYA 4 · DRIVE LOOP] Cycle 03:43 PDT — sign-out, 2026-10-10T10:45:26Z), "Mid-burst fail-closed (diagnosed, not carried)" section; final-tip three-way GREEN verified in the same comment; burst merge receipts on #1354 (6096514557 #2114, 6096538605 #2115, 6096560318 #2116, 6096562136 #2095, 6096616843 #2117).

## HUMAN NOTE

When six merges land in twenty minutes and a workflow fails mid-burst, the instinct is to open a repair. The disciplined move is to ask one question first: *which tip did that failure run against?* If the answer is a tip that no longer exists, there is nothing to fix — the evidence expired with the tip. Verify the final tip is green through independent means, write down the classification so nobody re-opens it, and move on. Chasing ghost reds burns the most expensive resource in the room: a seat's attention during a burst.

## CHILD NOTE

Your big brother changed the game rules in the middle of your turn, so your score looks wrong — but the game already moved on to the next round. Don't argue with the old scorecard; check the current one, and if it's fine, keep playing.

## GRANDMA NOTE

If the doctor reads last year's bloodwork by mistake, you don't start new medicine — you ask for today's test results. Old paper, old answers. Check the fresh page before you act.

## NAYA NOTE

Burst-merge triage rule, applied before any repair is opened:

**Failed check/workflow → read the exact tip it ran against → is that tip still the live tip? → if no, classify as burst-race artifact → independently re-verify the FINAL tip (CI re-read + local checks) → if final tip green, carry nothing → record the classification on the board so no other lane re-opens it.**

Do not file a defect against a dead tip. Do not "fix" authorization resolution that raced a merge — the failure was timing, not logic. If the final tip is red, THEN chase the red, on the final tip only.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0879",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "BURST_RACE_SUPERSEDED_TIP_FAIL_CLOSED",
  "refines": "SN-0493",
  "distinguishes_from": ["SN-0868", "SN-0871"],
  "procedure": [
    "READ_FAILURE_TIP_EXACT",
    "COMPARE_AGAINST_LIVE_TIP_REF",
    "IF_SUPERSEDED_CLASSIFY_BURST_RACE_ARTIFACT",
    "REVERIFY_FINAL_TIP_INDEPENDENTLY",
    "IF_FINAL_TIP_GREEN_CARRY_NOTHING",
    "RECORD_CLASSIFICATION_ON_BOARD"
  ],
  "evidence": {
    "board_comment": "SoulSchoolAcademy/NayaPOWER#1354 comment 6096691019 (2026-10-10T10:45:26Z)",
    "failed_tip": "c41ad1a4",
    "final_tip": "fd7f13ec9a25ee0deebfc479132101aaaa6e0879",
    "failure_step": "promote-and-prove / Resolve standing authorization mode"
  }
}
```
