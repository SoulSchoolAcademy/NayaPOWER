# Three Tries Max

SN-4786 · SKILLS / PROOF

**Created:** 2026-11-24T19:46:26Z
**Category:** Proof
**Skill:** 40
**SN:** SN-4786

## Nutshell

Three tries on any load or check, then stop — log it unreachable and fix it from the code. Never burn the day retrying.

## Child

Imagine you're trying to open a stuck door. You push once, twice, three times — and it still won't open. Pushing a fourth, fifth, tenth time won't help! The smart thing is to stop pushing, tell someone the door is stuck, and go fix the lock instead.

## Grandma

Dear, it's like a kettle that won't boil. You switch it on once, twice, three times — if it still won't boil, you don't keep flicking the switch all day. You unplug it, you look at the wire, you fix the kettle. The trying was never the fix.

## What It Means

Three tries max on any load or check; then stop, log it unreachable, and fix from the code. Never burn the day retrying. The log records what was tried, so the next person knows exactly where it stopped.

## Why It Matters

A stuck check stops costing time and turns into a fix instead of a loop. Retrying the same failing thing changes nothing — it only burns the day. Stopping early is not giving up; it is the fastest road to the real fix.

## How It Connects

It is the time-guard inside Verify the Rendered Experience and the Lean Operation skill — the rule that stops a probe from becoming a sinkhole. It pairs with Fail Fast: the bad round dies early, and the fix starts early. It also serves Debug by Evidence: after three tries, the evidence says the cause is in the code, so go look at the code.

## How to Apply

Try the load or check. If it fails, try again — up to three times total. On the third failure, stop. Write it down as unreachable, with what you tried and when. Then go fix the cause in the code. Never let a fourth retry happen because "maybe this time."

## What's In It For You

For Shawn: his work stops disappearing into retry loops — a stuck check costs fifteen minutes, not an afternoon. For us: hours come back, and the real work starts sooner. The real-world proof: on 2026-11-21 the browser retry c1dafc1d confirmed the About page, could not verify Personal, and stopped per the rule instead of retrying all day. Personal stayed honestly unverified — and the fix could start from the code instead of from another retry.
