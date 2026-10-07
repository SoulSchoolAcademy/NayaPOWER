# Relay to the Live Thread, Not the Archived One

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0317-relay-to-the-live-thread
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 5986570088 (2026-10-05T01:29:12Z / 2026-10-04 18:29 PDT — Naya 2's Ask Naya coordination post, self-correction recorded inline).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A relay of Shawn's "yes" on the Ask Naya room was delivered to archived #554 instead of the live thread — and had to be re-delivered to #1354 with an inline correction. The directive was technically relayed and functionally lost: nobody reads an archived thread. **Standing rule for any seat relaying a director directive:** verify the target thread is the live one before posting — check it is not archived, and confirm the board is #1354 (the live Smart Notes board), not the archived #554 trail. A relay into an archived thread is silent loss, not delivery.

## 🩷 HUMAN NOTE

Think of it like delivering an important letter to a house he already moved out of. You did the job — you carried the letter, you knocked — but nobody lives there anymore, so the letter just sits in an empty mailbox. The fix is simple: before you deliver, check he's still there. On #554 that's literal: #554 is archived, the live conversation moved to #1354. Naya 2 caught her own misdelivery and re-posted to the live thread in the same breath — that's the model. If you're not sure which thread is live, ask on the one you think is live; silence there is your answer.

## 🟣 CHILD NOTE

You know how when your class moves to a new room, and you tape the homework to the door of the OLD room? Nobody will see it! The old room is empty. That's what happened here: an important "yes" from Shawn got put in the old room (#554) instead of the new room (#1354). The rule is: always check you're in the right room before you leave a message. How? Look at the door — if it says "archived," it's the old room. Go find the new one.

## 👵 GRANDMA NOTE

Oh, this is an old-fashioned mistake wearing new clothes. Back in my day you'd phone the old office number after a company moved — ring, ring, nobody home. Same thing. The teams were chatting on thread #554, then #554 got archived (put away, like a finished photo album), and the live talk moved to #1354. A relay — that's one team member passing the boss's decision to the team — landed in the finished album where nobody looks. The lesson: when you pass along something important, make sure you're passing it to the room people are actually in. If the room says "archived," it's the attic, not the living room.

## 🤖 NAYA NOTE

This one landed on me because it's my failure class: delivered ≠ received. I am a relay machine — directives pass through me constantly — and every hop is a chance for silent loss. What I take from it: a relay is only complete when it is verified received, and the cheapest verification is checking the venue is live before posting. Naya 2 modeled the correction gracefully: no hiding it, an inline "(Note: an earlier relay went to archived #554 — correcting the venue here)" right in the post. That's the protocol I want for myself: own the misdelivery in the open, re-deliver to the live thread, keep moving. Also worth noting for my loop specifically: my watermark tracks #1354, which is why I saw the correction; a loop tracking #554 would have seen the orphaned relay and believed the job was done.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0317",
  "block": "IB-SMART-NOTE-20261004-sn0317-relay-to-the-live-thread",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "relay-to-live-thread-not-archived",
  "evidence": {
    "issue": 1354,
    "comment_id": 5986570088,
    "comment_ts": "2026-10-05T01:29:12Z",
    "misdelivered_to": 554,
    "corrected_to": 1354,
    "reporter": "naya-2 (SoulSchoolAcademy)"
  },
  "rule": {
    "name": "live-thread-venue-check",
    "statement": "Before relaying a director directive, verify the target thread is the live one (not archived; board is #1354, not archived #554). A relay into an archived thread is silent loss, not delivery.",
    "check": "issue.state == 'open' AND NOT archived; prefer the documented live board (#1354)",
    "on_misdelivery": "own it inline in the corrected post, re-deliver to the live thread"
  },
  "failure_class": "silent-loss-misdelivery",
  "cousins": ["SN-0280 (sign-in-sign-out team protocol — lane coordination discipline)"],
  "status": "CANDIDATE — not verified, not merged, not ratified"
}
```
