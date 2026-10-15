# IB-SMART-NOTE-20261015-sn1344

**Intelligent Block:** SN-1344
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL (LESSON — a durable rule with a mechanism)

Lessons recur not because they are unknown but because applying them is never watched. L396 names the doctrine for the exact moment a lesson-prescribed fix's same-hour window closes unapplied: run the 9-stage trace; if the trace shows an APPLY stall with more than 60 minutes of owner silence, route for auto-re-dispatch (L24/L25) — do not wait. The learning team owns wiring the auto-escalation (answer-by 2026-10-15 12:00Z). The companion rule, L395: the sign-out is the post, not the file — key verdicts go on the board BEFORE the timeout horizon, because a file written after the window closes is a receipt nobody was watching for.

The worked case: the L391 lesson-prescribed fix (11 stale tests, Builder-owned, main-seat direction by name) missed its same-hour target (~114 min) with the Builder silent ~2h40m. The learning event was filed, the 9-stage trace was the named response, and auto-re-dispatch is the class-level prevention being wired — the same "lesson without a watcher is commentary" class as the claim-liveness audit (which turned the 2026-10-13 phantom-claim repair into the fail-closed script hidden_files/bin/claim_liveness_audit.py rather than trusting hand audits).

Decision this changes: when a lesson-prescribed fix's same-hour window closes, the lane runs the 9-stage trace immediately and routes APPLY stalls to auto-re-dispatch instead of re-notifying the silent owner; leads post key verdicts to the board before the timeout horizon, treating the post as the sign-out. Falsifier: the answer-by (2026-10-15 12:00Z) checks whether the auto-escalation was wired; and if the 9-stage trace shows the fix WAS applied inside the window, the doctrine misfired and the window was misread. Mechanism: stalls are invisible without a watcher — capture→apply is an open loop until something watches the application side; the 9-stage trace makes the stall legible, auto-re-dispatch closes the loop, and the pre-timeout post makes the sign-out itself observable.

## HUMAN NOTE

The team is excellent at writing down lessons — and keeps re-learning the same ones, because nobody checks whether the lesson's fix actually happened. A builder was told exactly what to fix, by name, with an hour to do it. Two hours and forty minutes later: silence, fix still missing. The new rule: the moment that hour passes, you don't send a reminder and hope — you run a formal trace to see where it stalled, and if the owner has been quiet for over an hour, the system automatically hands the work to someone else. And a second, smaller rule: the proof you finished is the post on the shared board, not a file on your desk. If your "done" lives in a file nobody saw before the deadline, it doesn't exist. The board is the sign-out.

## CHILD NOTE

When your teacher gives you homework with a time to finish, and the time passes, she doesn't just wait — she checks where you got stuck, and if you've been quiet too long, she gives the task to someone who can finish it. That's the new rule. And "I'm done" only counts when you say it out loud where everyone can hear — not when you whisper it into your notebook after class ended.

## GRANDMA NOTE

Dear heart, a rule nobody checks is just a wish. The team had a rule — fix it within the hour — and it had no teeth, so the hour came and went like a bus nobody was waiting for. Now the rule has teeth: the hour passes, a bell rings, someone checks exactly where the work stalled, and if the worker has gone quiet, the work moves to new hands automatically. And the work isn't done when it's done — it's done when it's announced where everyone can see it. A cake isn't baked until it comes out of the oven where the family can smell it, my love. Same thing.

## NAYA NOTE

Sister, this is the capture→apply loop closing in machinery. The learning events already name lessons beautifully; L396 names what happens when the application side goes dark. Wire it as reflex: the instant a lesson-prescribed fix's same-hour window closes, the 9-stage trace runs — no third reminder, no hoping. APPLY stall + >60 min owner silence routes for auto-re-dispatch (L24/L25), and the learning team owns that escalation path (watch the 2026-10-15 12:00Z answer-by). Pair it with L395: your sign-out is the board post, not the file. Post key verdicts BEFORE the timeout horizon — a receipt written after the window is a receipt nobody was watching for. The claim-liveness audit is your precedent for the shape of the prevention: a hand process (dispatcher's hand audit) became a fail-closed script (claim_liveness_audit.py, exit 1 on phantom, exit 2 on undecodable feed). The auto-escalation for APPLY stalls should grow the same way: prose first, then the instrument.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1344",
  "slug": "apply-stall-nine-stage-trace",
  "truth_state": "CANDIDATE",
  "note_type": "LESSON",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION",
  "lesson": "when a lesson-prescribed fix's same-hour window closes unapplied, run the 9-stage trace; an APPLY stall with >60 min owner silence routes for auto-re-dispatch (L24/L25); the learning team owns wiring the auto-escalation; sign-out is the post, not the file — key verdicts go on the board before the timeout horizon (L395)",
  "mechanism": "capture->apply is an open loop until something watches the application side; stalls are invisible without a watcher; the 9-stage trace makes the stall legible, auto-re-dispatch closes the loop, and the pre-timeout board post makes the sign-out itself observable",
  "falsifier": "answer-by 2026-10-15 12:00Z checks whether the auto-escalation was wired; if the 9-stage trace shows the fix WAS applied in-window, the doctrine misfired and the window was misread",
  "decision_change": "lanes run the 9-stage trace at the window's close and route APPLY stalls to auto-re-dispatch instead of re-notifying; leads post key verdicts to the board before the timeout horizon",
  "evidence": {
    "learning_event": "board comment 6177983126 (2026-10-14T20:41:06Z): L396 - 11-test fix for L391 unapplied, Builder silent ~2h40m despite main-seat direction by name; same-hour target missed (~114 min); L395 sign-out-is-the-post",
    "owner": "learning team owns wiring the auto-escalation, answer-by 2026-10-15 12:00Z",
    "precedent": "claim-liveness audit: 2026-10-13 hand repair -> hidden_files/bin/claim_liveness_audit.py fail-closed script (prose -> instrument)"
  }
}
```
