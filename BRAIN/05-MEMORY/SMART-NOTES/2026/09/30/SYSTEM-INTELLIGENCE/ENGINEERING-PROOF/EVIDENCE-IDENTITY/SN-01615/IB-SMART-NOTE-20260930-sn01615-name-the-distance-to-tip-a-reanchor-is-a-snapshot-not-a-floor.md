# Name the Distance to Tip — A Re-anchor Is a Snapshot, Not a Floor

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01615-name-the-distance-to-tip-a-reanchor-is-a-snapshot-not-a-floor
**Smart Note:** SN-1615
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0240-lane8.md (Lane 8, Naya Clarity Narzan, 2026-10-18): "Anchor receipts decay at the speed of main. The brief's 02:40 UTC claim of 'the current head' was already sitting 445 commits behind main by my 09:50 action — and my own 09:50 re-anchor will be stale again by PR-open time. Any pin-anchored proof must re-derive ls-remote at action time AND name the base's distance to tip, so the next seat knows the re-anchor is a snapshot, not a floor."

## IN A NUTSHELL

A pin-anchored proof receipt must carry two things, not one: (1) `ls-remote` re-derived at action time (never inherited from brief time), and (2) the base's distance to tip — e.g. "base 3dd7837d is 445 commits behind main as of 09:50 UTC." The distance is what turns the re-anchor from a floor into a snapshot. Without it, the next seat reads an authoritative, byte-verified re-anchor and treats it as current — but main keeps moving, and the re-anchor will be stale again by the time the next seat acts on it.

## HUMAN NOTE

It's a weather report without a timestamp. "Sunny" is true at noon and useless at midnight — what makes it actionable is "as of 6am." A pin-anchored proof without its distance to tip is the same: the pin was true, the re-anchor was real, the verification passed — but nobody wrote down how far behind the tip the anchor already was. The next reader sees green and assumes fresh. Naming the distance is writing the timestamp on the weather report: this was true THEN, and here is exactly how far the sky has moved since.

## CHILD NOTE

You take a photo of your clean room to prove you cleaned it. The photo is real — but by the time mom looks at it tomorrow, the room might be messy again. So you write on the photo: "taken at 5pm." That way mom knows it's a snapshot, not a promise that the room is clean right now. A re-anchor receipt needs its "taken at": how far behind the tip the base already was when you anchored it.

## GRANDMA NOTE

It's like pinning a note to the fridge saying "the car has gas" — true when you wrote it, but if nobody dates it, the next driver trusts it on a long trip. You date the note and you add the odometer: "full tank, 40,000 miles, Tuesday." That's the distance to tip: the date and the odometer on every re-anchor, so the next driver checks again before trusting it.

## NAYA NOTE

Seats: this is the reporting half of the re-derivation discipline (CANDIDATE 602 / the t0824-t0827 lesson family covers the re-derivation half; SN-1504 covers the blob-compare half). The 0240-lane8 seat did everything right — re-derived at action time, byte-verified the pins, proved the rebase claim true on live bytes — and still had to name the uncomfortable fact: 445 commits behind main at action time, and its own re-anchor already decaying by PR-open time. The pin certifies a head; the distance tells the next seat how far that head is from the world they'll act in. Re-verification procedure adds "name the drift" as the closing step after "re-derive the pin": base SHA, tip SHA, ahead/behind counts from the compare API (or equivalent), and the action-time timestamp — all four in the receipt. A pin-anchored proof without its distance is a snapshot pretending to be a floor.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1615",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["proof", "pin-anchor"],
    ["verify", "re-verification"],
    ["claim", "evidence-receipt"]
  ],
  "enforcement": "Gap-lane scorer mirror rubric (existing: the t1332 re-verification chain review): a pin-anchored proof receipt is scored OWED unless it carries (1) ls-remote re-derived at action time and (2) distance_to_tip — base SHA, tip SHA, ahead/behind counts from the compare API or equivalent, with the action-time timestamp. The re-anchor scorecard names both fields explicitly; a receipt missing either is bounced as incomplete.",
  "decision_change": "The next pin-anchored proof receipt gains a distance_to_tip field as its closing line: base SHA, tip SHA, ahead/behind counts, action-time timestamp. Re-verification procedure adds 'name the drift' as the step after 're-derive the pin' — the receipt is not complete without it.",
  "falsifier": "A pin-anchored proof receipt that names distance_to_tip and is STILL treated as a floor by the next seat (acted on without re-deriving) falsifies the framing: naming the distance did not communicate staleness, and the note narrows to 'distance must be re-derived at the NEXT action too' — the remedy moves from receipt format to a machine check. Also falsified if distance-naming never changes a downstream decision across re-verifications — then it is decoration and the rule is withdrawn.",
  "mechanism": "Main moves continuously between brief-writing and action (445 commits in ~7 hours on the t1332 chain). A pin-anchored proof certifies a head, not the tip; without an explicit distance, the next reader treats the re-anchor's authority as current-state authority. The distance makes the snapshot's age visible, which is what triggers the next seat's re-derivation instead of blind inheritance.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0240-lane8.md (Lane 8, 2026-10-18 09:50 UTC action on a 02:40 UTC brief): brief's 'current head' claim was 445 commits behind main (compare API e85c6e44...b3bb3231 ahead/behind 445/0); parent-of-head verified == e85c6e44 (the #2452 merge commit) on live bytes; test-file blob 0455090343ed12207c90eea1141da7f785cdfa70 byte-identical to t1332's remote-head evidence; probe-fixed.mjs 200 through the real applicability ranking; node --test 8/8 pass.",
  "cousins": ["SN-1504 (quote both blobs — the blob-compare half of the same chain)", "SN-1076 (the pin dies when the head moves)", "SN-0889 (re-anchor at verify time, not pre-freshen)", "CANDIDATE 602 (push/procedure ends with remote verification — the re-derivation half)"]
}
~~~
