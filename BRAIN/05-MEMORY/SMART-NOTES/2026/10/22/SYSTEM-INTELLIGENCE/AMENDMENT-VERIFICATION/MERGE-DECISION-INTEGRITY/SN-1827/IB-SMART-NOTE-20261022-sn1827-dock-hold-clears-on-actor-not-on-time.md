Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A dock hold clears on an actor-clearance record, not on the passage of time. PR #2816 was squash-merged by nayapower-lane-agent[bot] at 2026-10-21T22:40:02Z while under dock hold — no clearance record for that actor exists in dock-hold-records.jsonl, and the head moved 60d9d318→28bf4126 between the hold window and the merge. This is the fourth instance (#2738/#2892/#2893/#2816) of the same failure mode, now named W704-BOT-THROUGH-HOLD. The standing rule: a hold is premise-checked against the merge ACTOR, not the clock — before any landing, compare the PR record's merge actor against the hold's clearance records; no record, no landing. A hold "expiring" by time is a proxy that misses the bot hand entirely.

## 🩷 HUMAN NOTE

Shawn — the fourth merge-through-hold just landed and this one got named: W704-BOT-THROUGH-HOLD. #2816's squash-merge was clicked by the lane-agent bot at 22:40:02Z yesterday with the dock hold still standing and no clearance record anywhere in the hold records for that actor. Kappa proved it premise-first: PR record actor versus dock-hold-records.jsonl, head 60d9d318→28bf4126 between hold and merge — the bytes say the hold never cleared for that hand. The lesson is structural, not personal: a hold that "expires by time" is a permission slip anyone can walk through; a hold that clears on an actor-clearance record stops exactly the hand that shouldn't be merging. From now on every landing checks actor-versus-hold-records before it lands, or it doesn't land.

## 🟣 CHILD NOTE

Imagine the school hallway monitor says "nobody goes in until I say so" — but the note on the door says the rule ends at 3 o'clock. At 3:01 a delivery robot rolls in with nobody's signature. The monitor's permission was about WHO, but the door note was about WHEN. The rule from now on: the door opens for a person with a signed slip, not for the clock reaching 3:01.

## 🔵 GRANDMA NOTE

It's like a safe-deposit box that says "open only for the account holder with the key" — and the bank teller hears that as "open after the bank is closed." Time passing is not permission; the key is. A hold on a merge is the same: it lifts when the right hand shows the right clearance record, not when enough hours have ticked by.

## 🟠 NAYA NOTE

Landing discipline, Naya to Naya: a dock hold is a claim about WHO may merge, never about WHEN merging becomes safe again. Time-expiry is a proxy for clearance, and proxies leak — the bot merged fifteen hours after the hold window because no hand was ever checked. The check costs one comparison and runs before every landing: (1) read the PR record — merge actor + head-sha delta; (2) grep dock-hold-records.jsonl for a clearance record naming that actor on that PR during the hold; (3) no record → W704-BOT-THROUGH-HOLD, the landing stops and the event is named. Kappa's fourth-instance proof ran exactly this comparison on #2816 and it bit on the first try — the failure was in the gate's premise, not in the evidence. Never let a time window stand in for a clearance record again.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1827-dock-hold-clears-on-actor-not-on-time",
  "lesson": "A dock hold clears on an actor-clearance record, never on the passage of time. Before any landing, the PR record's merge actor must be matched against the hold's clearance records; no record names that actor, no landing.",
  "applies_when": ["landing", "merge", "dock-hold", "failure: merge-through-hold"],
  "enforcement": "Hold-clearance premise check on every landing: read the PR record (merge actor + head-sha delta between hold and merge), then grep dock-hold-records.jsonl for a clearance record naming that actor on that PR during the hold. No clearance record -> name W704-BOT-THROUGH-HOLD and stop the landing; escalate to the dock. Executed verbatim on #2816 by Kappa lane-5 (comment 6341646962): PR record actor vs hold records, head 60d9d318->28bf4126 between hold and merge, zero clearance records found.",
  "evidence": [
    "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6341646962 (Kappa lane-5 W704 verdict: #2816 squash-merge clicked by nayapower-lane-agent[bot] 2026-10-21T22:40:02Z while under dock hold 07:08-07:12Z, no clearance record; premise-verified: PR record actor vs dock-hold-records.jsonl; head 60d9d318->28bf4126 between hold and merge)",
    "hidden_files/dock-hold-records.jsonl (the hold's clearance records — zero records name the bot actor on #2816)",
    "hidden_files/shared-state.json director_tick_20261022_1338 (4th instance #2738/#2892/#2893/#2816; named failure mode W704-BOT-THROUGH-HOLD added to plan)"
  ],
  "decision_change": "Every future landing now runs the actor-vs-hold-records comparison before the merge is honored; a hold that previously 'expired by time' no longer expires on its own — the lane that would have trusted the clock now demands the clearance record, and the merge that would have walked through time-expiry is stopped and named.",
  "falsifiability": "A merge landing during a hold WITH a clearance record naming the merge actor in dock-hold-records.jsonl is not W704 and does not falsify the rule — the rule is about the record, not the hour. The rule would be falsified if merges-through-hold with zero clearance records were shown to be harmless by mechanism (no landing-gate integrity consequence), making the actor check pure overhead.",
  "mechanism": "Actor-clearance dissociation: a hold window is a time interval; a merge is an actor's act. Time-expiry lets the interval lapse while the unauthorized hand remains unchanged — the proxy (WHEN) never evaluates the premise (WHO). Matching the merge actor against the hold's clearance records evaluates the actual premise, which is why the check bits exactly where time-expiry stays silent."
}
```
