# One Lane, One Receipt Per Tick — Mid-Tick Head Moves Get a Named Handoff, Not Silent Adoption

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1137-one-lane-one-receipt-per-tick
**Smart Note:** SN-1137
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## IN A NUTSHELL

When the main tip moves under a lane mid-tick, the lane does not silently adopt the new head. The move is flagged explicitly as a named handoff (who moved it, from what pin to what pin, at what time), and the verifying lane re-verifies on the NEW head in the same cycle — with one receipt per lane per tick, each pinned to the exact head it actually tested. A receipt without a matching head pin is a claim about the wrong bytes.

## HUMAN NOTE

On 2026-10-12, Shawn merged PR #2459 himself (revert of #2455), moving the tip `dbe06f9e` → `dd6f2d92` mid-tick and resolving the M1 merge hold. Two lanes were working underneath that move. The wire lane flagged the unannounced head move on the board; the verify lane (Lane 9) re-verified kernel tests on the NEW head within the same cycle and reported SUCCESS with the new pin — the receipt was pinned to `dd6f2d92`, not to the head the tick started on. That is the adopted rule: one lane, one receipt per tick.

The failure mode this kills: a lane reports "green" on a head that no longer exists, and the next reader treats it as a certificate for the live tip. Silent head adoption is how a board drifts one full merge out of phase with reality, with every receipt technically honest and every conclusion stale.

## CHILD NOTE

If the finish line moves while you're running, don't pretend you finished at the old line. Say out loud that the line moved, tell everyone where it moved to, run to the new line, and write down the new line in your report. One runner, one report — and the report always names the exact line it ran to.

## GRANDMA NOTE

It's like stamping a letter: the stamp is only good if it says today's date and the right address. If the address changed mid-delivery, you don't keep the old stamp — you say the address changed, take the letter to the new address, and get a fresh stamp. Every delivery gets exactly one stamp, and the stamp names the place it actually went.

## NAYA NOTE

Head-move protocol, one lane, one receipt per tick:

1. **Flag the move.** When the tip changes mid-tick (by anyone, including Shawn), post a named handoff: old pin → new pin, mover, timestamp, what was invalidated. Unannounced adoption is a protocol breach.
2. **Re-verify on the new head.** The verifying lane re-runs its checks on the NEW tip in the same cycle. In-flight verification results on the old head are stale certificates — they do not transfer.
3. **One receipt per lane per tick, head-pinned.** The sign-out receipt carries the exact head SHA tested. If the head moved mid-tick, the receipt says so and names the new head. A reader trusts the receipt only for the pin it names.

**Antipattern (dead):** "tip moved dbe06f9e → dd6f2d92 mid-tick, my checks were green on dbe06f9e, calling it green" — green on dead bytes is not evidence for live bytes.

## MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "smart_note": "SN-1137",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "evidence": [
    {
      "type": "board_comment",
      "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6135228767",
      "summary": "INTELLIGENT EVENT 2026-10-12: one-lane-one-receipt adopted — #2459 head-move handoff: wire flagged unannounced head move, verify re-verified new head 9.0/10 in ~10 min"
    },
    {
      "type": "board_comment",
      "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6135284479",
      "summary": "Lane 9 t0552 sign-out: tip moved mid-tick dbe06f9e -> dd6f2d92 (Shawn merged #2459 himself, revert of #2455, M1 hold RESOLVED); CI kernel-tests SUCCESS on the NEW tip dd6f2d92; local 599/599 both tips"
    }
  ],
  "rule": "one_lane_one_receipt_per_tick_head_pinned",
  "mechanical_check": "signout.receipt.head_sha == head bytes actually tested; mid-tick tip move -> named handoff event posted AND re-verification on new head in the same cycle",
  "anti_pattern": "silent_head_adoption_with_stale_certificate",
  "cousins": ["SN-0351", "SN-0969", "SN-1134"],
  "master_nodes": ["VERIFY", "CONNECT", "PROVE"]
}
```
