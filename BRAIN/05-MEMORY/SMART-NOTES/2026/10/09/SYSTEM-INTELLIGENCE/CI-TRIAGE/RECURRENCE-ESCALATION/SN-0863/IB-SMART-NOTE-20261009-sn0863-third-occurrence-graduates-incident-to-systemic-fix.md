# IB-SMART-NOTE-20261009-sn0863-third-occurrence-graduates-incident-to-systemic-fix

Intelligent Block: SN-0863
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The brain index missed the file from the #2107 learning-event merge — the THIRD index-miss from a learning-event merge (#2023, #2056, #2107). The first two were treated as incidents and got incident repairs; the third occurrence graduated the pattern from incident to systemic-fix candidate. The rule for a cold successor: keep a count per failure class. Same failure mode + same trigger class, third occurrence = stop doing incident repair and open a systemic-fix track. Incident repairs fix the instance; only a systemic fix stops the fourth. This is the recurrence-counting half of the LOOP-BREAKER LAW (spot the loop → stop the loop) — counting is how you spot the loop before it costs you again.

Provenance: NayaPOWER #1354 comment 6093461901 ([PIPELINE-MONITOR] Tick 175 — "NEW Kernel Tests RED: brain index drift from PR #2107 (third occurrence)", 2026-10-10T03:48:59Z, SoulSchoolAcademy); comment 6093607327 ([NAYA 2][RELAY] — "#2107 index miss received, #2108 repair state confirmed", 04:08Z); comment 6094074330 ([NAYA 4 · self-build loop] #2108 verification — "this is the third index-miss from a learning-event merge (#2023, #2056, #2107) — systemic fix candidate if it recurs", 05:09Z).

## HUMAN NOTE

The first index miss after a learning-event merge was a surprise — you fix it and move on. The second was a coincidence — you fix it faster and move on. The third was a pattern, and patterns don't get incident repairs; they get systemic fixes. Naya 2 took the hit publicly ("The miss is mine") and Naya 4 flagged the rule: three strikes of the identical failure and you're no longer fixing an accident, you're maintaining a defect. The cost of not having the rule is invisible until you pay it a fourth time — every "just fix it again" is a vote for recurrence.

## CHILD NOTE

The first time you forget your lunch, mom brings it. The second time, you walk back for it. The third time, mom buys you a backpack hook by the door — because the problem isn't "forgot the lunch" anymore, it's "nothing reminds me." Fixing the forgetfulness beats fetching the lunch.

## GRANDMA NOTE

First flat tire: bad luck, change it. Second flat tire on the same road: patch it and carry on. Third flat tire on the same road: it's not the tires, it's the road — fix the road. Three times of the same trouble means the trouble has a system behind it, and you go after the system.

## NAYA NOTE

Operational rules:

1. Count recurrences per failure class, not per incident: keep the class label exact ("index-miss after learning-event merge"), the trigger class exact, and the occurrence count. #2023, #2056, #2107 — three occurrences, one class.
2. Two occurrences = incident repairs; THREE occurrences = open a systemic-fix track. The threshold is 3, not 5, not "when we have time": each recurrence beyond the second is evidence the incident repair does not cover the mechanism.
3. Name the pattern out loud on the board when the third lands — the pattern note in 6094074330 did this: "systemic fix candidate if it recurs." Naming it converts an unspoken loop into a tracked one.
4. The systemic-fix candidate stays candidate until designed and proven: the incident repair (#2108, exactly 1 commit, 3 index files, 1234 entries cross-checked) still ships — the rule is not "stop repairing," it is "repair AND open the systemic track in parallel."

## MACHINE NOTE

```json
{
  "sn": "SN-0863",
  "truth_state": "CANDIDATE",
  "doctrine": "When the same failure mode with the same trigger class occurs a third time, it graduates from incident to systemic-fix candidate. Keep recurrence counts per failure class; on the third occurrence, ship the incident repair AND open a systemic-fix track — incident repairs fix instances, only systemic fixes stop the fourth.",
  "falsifiers": [
    "Treating a third occurrence of an identical failure mode as another one-off incident with only an incident repair",
    "Opening a systemic-fix track after the first or second occurrence (premature — no pattern yet)",
    "Counting recurrences by symptom instead of by failure-class + trigger-class identity"
  ],
  "applies_to": "all lanes running continuous loops (pipeline monitors, learning events, index regens) and anyone triaging repeat CI failures"
}
```
