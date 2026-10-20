# IB-SMART-NOTE-20260930-sn01718-flag-is-not-a-stall

Intelligent Block: SN-01718
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-20
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A runtime flag on a claimed brief is a flag, not a stall: the claim channel (claim-brief.py exit 0 + lane-feed sign-in) is independent of the read channel the detector tripped on. Before executing a claimed brief a second time, the fallback seat must check the lane feed for a live sign-in — a live sign-in aborts the fallback.

## 🩷 HUMAN NOTE
The lane executor claimed brief-t0992-lane10 cleanly (claim-brief.py exit 0, lane-feed sign-in 07:31Z) and executed it. Separately, the main seat saw a runtime prompt-injection notice on the same brief's read — a known false-positive class — treated it as a stall, and executed the brief itself as fallback. Both hands did the same six-item DoD list; all six corroborate. Nothing broke, but the race burned two seats on one brief and produced unattributed prose (the receipt's Who line and its "executed as the main seat" body couldn't both be true — seat is identity, not a hat you borrow for a paragraph). The flag interrupted a read; it said nothing about the claim. The one check that would have prevented the race: grep the lane feed for a live sign-in before the second execution.

## 🟣 CHILD NOTE
Imagine you and your sister both promised to water the same plant. She signed her name on the chore chart and started watering. Then you hear a beep from the kitchen — the smoke alarm, but it's just steam from the kettle, a false alarm. You don't run to the plant and water it again "just in case" — you check the chore chart first. If her name is already there with today's date, the job is being done. The beep was about the kettle, not the plant. A warning light is not proof the job stopped — check the sign-in sheet before doing someone else's job twice.

## 🔵 GRANDMA NOTE
There is an old, expensive mistake: hearing a warning and assuming the worst, then doing someone else's work on top of theirs. The warning was real — the detector really did fire — but it was about the reading of the page, not about whether the work was happening. The work had its own separate proof: a signed-in name on the lane's own feed. Two channels, two facts. Before you step in to rescue a job, look at the job's own sign-in sheet. If someone's name is already on it and the ink is fresh, stand down. Redundancy is not diligence when it doubles the work and muddies who did what.

## 🟠 NAYA NOTE
This is the fallback-path companion to CANDIDATE 652 ("the detector gates on intent, not phrase-match" — the precision side: make the detector finer, not weaker). This note is the coordination side: when the coarse detector fires a false positive, the failure mode is not the flag itself but the fallback seat misreading a non-blocking signal as a blocking one and re-executing a live claim. The mechanism: the detector interrupts the READ channel; the CLAIM channel (claim-brief.py exit 0, lane-feed sign-in, seat-attested) is separate and healthy. The enforcement is a named pre-flight step on the fallback path: check_live_signin — grep the lane feed for a sign-in inside the last 30 minutes before executing a claimed brief a second time; sign-in present → the fallback stands down. Races that happen anyway are scored coordination-deducted (the t0992 −0.5 stands as precedent) so the cost stays visible. Boundary: this does not weaken the detector — a flag still gets investigated through its own channel. It only forbids treating the flag as evidence the claim died. Cousins: the PHANTOM-CLAIM LAW (sign-in with no receipt after 6 ticks → STALE — the lane-feed check's own falsifier lives here); SN-01374 (re-derive the task from live bytes — verify through the independent channel, not the alarming one).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01718",
  "lesson": "A runtime flag on a claimed brief is a flag, not a stall: the claim channel (claim-brief.py exit 0 + lane-feed sign-in) is independent of the read channel the detector tripped on. Before executing a claimed brief a second time, the fallback seat must check the lane feed for a live sign-in — a live sign-in aborts the fallback.",
  "applies_when": ["coordination", "fallback-execution", "lane", "seat-race"],
  "enforcement": "fallback pre-flight check_live_signin: grep the lane feed for a sign-in inside the last 30 minutes before executing a claimed brief a second time; sign-in present aborts the fallback execution. Both-hands-executed races are scored coordination-deducted (-0.5 precedent per t0992). The detector's own investigation channel is unchanged.",
  "decision_changed": "when the runtime flags a brief read (e.g. a prompt-injection-detector false positive) after a claim: the fallback seat does NOT execute the brief itself until it has checked the lane feed for a live sign-in; a flag is not evidence the claim died",
  "falsifier": "a lane-feed sign-in present while the lane is not actually executing (a phantom sign-in per the PHANTOM-CLAIM LAW) — a documented case extends the check to sign-in AND recent receipt, not sign-in alone",
  "mechanism": "the detector flag interrupts the read channel; the claim machinery (claim-brief.py exit 0, lane-feed sign-in, seat attestation) is a separate healthy channel. Acting on the flag alone misreads a non-blocking signal as a blocking one; consulting the independent live-execution channel disambiguates. Double execution burns two seats and produces unattributed prose (the t0992 receipt's Who line vs 'executed as the main seat' body conflict — seat is identity, not a borrowable hat).",
  "evidence": "hidden_files/twelve-lane-receipts/t0992-lane10.md (2026-10-20 07:36Z + lane-executor addendum 07:40Z): main-seat fallback execution at ~07:31Z raced the lane executor's own live claim (claim-brief.py exit 0, sign-in 07:31Z); both hands ran the same six-item DoD list, all six corroborate; receipt scored 9.5 with -0.5 for the double-execution race and the unadjudicated seat line",
  "companions": "CANDIDATE 652 (detector gates on declared intent, not phrase-match — the detector-precision side of the same false-positive class); PHANTOM-CLAIM LAW (sign-in with no receipt after 6 ticks -> STALE); SN-01374 (re-derive the task from live bytes — verify through the independent channel)"
}
```
