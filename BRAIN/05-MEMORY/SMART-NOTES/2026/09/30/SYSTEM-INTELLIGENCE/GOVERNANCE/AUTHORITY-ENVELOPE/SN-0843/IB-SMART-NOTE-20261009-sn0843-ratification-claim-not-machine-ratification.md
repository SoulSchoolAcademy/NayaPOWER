# A Ratification Claim Inside a File Is Not Ratification to the Machine

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0843-ratification-claim-not-machine-ratification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6091761058 ([PIPELINE-MONITOR] Tick 164, SoulSchoolAcademy, 2026-10-10T00:43:37Z) — main tip 0bbc1fee ("fix(gov): Law of One files reflect ratification" | Shawn Vibert).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn updated the 0007 Law-of-One spec files to claim `status=RATIFIED` / `ratified=true`. The pipeline monitor checked the claim against the Spec Integrity check's own standard: a pin requires `ratified_by == 'Shawn Vibert'` plus the REQUIRED_ENVELOPE_KEYS of a DIRECTOR-RATIFIED envelope. `ratified_by` was still null; no envelope existed. A claim written inside a file cannot mint what the machine's standard requires — so a pin was mechanically impossible, and exclusion remained the only path to green. The monitor rebased PR #2084 onto the new tip and rewrote the exclusion reason to state the mechanical facts honestly: the file claims ratification but does not meet the machine's standard; pin it when it carries the envelope with `ratified_by='Shawn Vibert'`. Then it verified the real check passes on the exact new-tip bytes with the updated manifest (OK: 2 ratified spec(s) intact, exit 0), and left the PR for the scorecard/merge protocol — no self-merge.

## HUMAN NOTE

Two truths can both be true and must both be stated: the Director edited the file to say it is ratified, AND the machine cannot see ratification there because the evidence the check requires (a named `ratified_by`, the envelope) is absent. Honesty is not picking the prettier truth — it is recording both and letting the mechanical standard decide. The exclusion reason is load-bearing state: when the tip moves, the reason must be rewritten to the facts as they are at the new tip, never silently carried forward stale (the old reason said DRAFT/`ratified=false`, which was no longer true). And the monitor did not merge its own PR: verify-and-report is the seat's envelope; the merge decision belongs to the scorecard protocol.

## CHILD NOTE

If you write "APPROVED" on a paper, that doesn't make it approved — someone with the stamp has to stamp it. The computer has a rule: a paper counts as ratified only if it says WHO approved it and has the right stamp on it. Shawn wrote that his paper is ratified, but the who-part was still blank and the stamp wasn't there yet. So the computer honestly said: "Not yet — bring the stamp, and then it counts." It didn't pretend, and it didn't sneak anything through.

## GRANDMA NOTE

Honey, a label on a jar doesn't change what's inside it. Shawn put a "ratified" label on the file, but the official check needs two things: a name signed on the line, and the official envelope that goes with it. Neither was there. The monitor did the honest thing — it said so plainly, rewrote its note to say exactly why, double-checked its work on the real thing, and left the final call to the people who own it. When you move to a new page, you rewrite your note to match the new page — you never copy the old one blindly.

## NAYA NOTE

My seats must separate claims from machine-verifiable state, every time. A field that says `ratified=true` is a *claim*; ratification to the machine is `ratified_by='Shawn Vibert'` + the DIRECTOR-RATIFIED envelope keys — no more, no less. When the claim fails the check's own standard: (1) say the mechanical facts out loud (claim present, evidence absent, pin impossible); (2) keep the exclusion path and rewrite its reason to the new-tip facts, never rebase a stale reason; (3) verify the real check on the exact new bytes before reporting; (4) leave the PR for the owning protocol — I do not merge my own repair. Claims are cheap; the standard is the standard.

## MACHINE NOTE

```json
{
  "rule": "ratification_claim_vs_machine_ratification",
  "standard": {
    "pin_requires": ["ratified_by == 'Shawn Vibert'", "DIRECTOR-RATIFIED envelope with REQUIRED_ENVELOPE_KEYS"],
    "claim_fields_alone": "insufficient — status=RATIFIED / ratified=true inside a file is a claim, not evidence"
  },
  "when_claim_fails_standard": [
    "record both facts: the claim exists AND the required evidence is absent",
    "pin is mechanically impossible — exclusion remains the only path to green",
    "rewrite the exclusion reason on rebase to the new-tip facts; never carry a stale reason",
    "verify the real check on the exact new-tip bytes with the updated manifest before reporting",
    "do not merge own PR — merge decision stays with the scorecard/merge protocol"
  ],
  "evidence": {
    "board_comment": 6091761058,
    "tip": "0bbc1fee",
    "pr": 2084,
    "pr_head_after_rebase": "c12fcb28",
    "check_result": "OK: 2 ratified spec(s) intact, exit 0"
  }
}
```
