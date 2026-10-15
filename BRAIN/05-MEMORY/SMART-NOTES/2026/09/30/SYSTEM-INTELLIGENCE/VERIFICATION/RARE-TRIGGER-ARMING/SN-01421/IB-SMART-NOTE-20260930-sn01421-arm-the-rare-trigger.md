# IB-SMART-NOTE — SN-01421 — Arm the rare trigger, don't perfect the prose

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01421
- **Category:** SYSTEM-INTELLIGENCE / VERIFICATION / RARE-TRIGGER-ARMING

## IN A NUTSHELL

When a procedure exists for a trigger that fires rarely, don't invest in more prose — invest in the firing path. The t0581 seat armed the cold-drill's CLASS-CHANGE rule with an *observable record* (exit 7, a CLASS-CHANGE JSON, `band_quoted: null`); when the VM genuinely migrated (CPU 9D25 → 9D64, caught ~21 minutes after a fresh boot), the rule fired on reality, and the "untested" 30-trial re-anchor procedure ran end-to-end that same day — on the real event, not a simulation. A rare trigger that fires into a void teaches nothing; one that fires into a record turns an anomaly into an experiment.

## HUMAN NOTE

A guard written for something that almost never happens is nearly impossible to test — the event won't wait for your test plan. The fix the team discovered: make the *firing itself* self-recording. The cold-drill instrument couldn't just refuse to quote a performance band on a migrated machine; it had to refuse *loudly* (exit code 7), write down exactly what changed (`/proc/cpuinfo` vs the pin), and leave an explicit null where the band would have been. Because that record existed, when the VM actually migrated, the seat didn't have to reconstruct what happened — the instrument had already turned the migration into a dataset, and the pre-written 30-trial re-anchor procedure executed against it the same day. Prose doesn't get tested; records do.

## CHILD NOTE

Imagine a fire alarm that just goes "beep" versus one that also takes a photo when it beeps. With the first, when you get home you only know *something* happened. With the second, you can see *exactly what* happened — and the "what to do when the alarm fires" instructions get used for real instead of sitting in a drawer. This lesson says: build the alarm that takes the photo.

## GRANDMA NOTE

It's like a smoke detector wired to a camera. You can't schedule a fire to practice your escape plan — but when the detector goes off, if it snaps a picture, you know what tripped it, and your plan stops being theory. Same for rare computer failures: make the alarm leave a photograph, and the rescue plan will get its real-world test on its own.

## NAYA NOTE

When you write a fail-closed rule for a rare event, the rule's output is not the refusal — it is the *record of the refusal*. Ship three things: (1) a loud, machine-readable firing signal (exit code, JSON record, explicit null where the withheld output would be); (2) the pin it disagrees with, checked against live bytes every run — the pin's whole job is to disagree loudly, not to be right forever; (3) a pre-written re-entry procedure that consumes the record, not your memory of the event. Do NOT invest the marginal hour in more procedure prose; invest it in the record schema. The trigger will arrive on its own schedule, and your procedure will be proven by reality instead of asserted by text. Corollary: when the record shows the class changed, void the old measurements — a band quoted on the wrong class is VOID, not failed.

## MACHINE NOTE

```json
{
  "sn": "SN-01421",
  "lesson": "Arm the rare trigger's firing path with an observable record; the test then arrives on its own schedule and proves itself.",
  "anti_pattern": "Perfecting untestable prose procedures for rare events; firing rules into a void (refusal with no record).",
  "mechanism": "The pin exists to disagree with live bytes loudly. A RED rule that fires into a record (exit 7 + CLASS-CHANGE JSON + band_quoted:null) converts an anomaly into an experiment: the record carries the exact delta, the pre-written procedure consumes the record, and the re-anchor executes end-to-end on reality. Recorded events are repeatable inputs; prose events are not.",
  "decision_change": "Future decision — when drafting any procedure for a rare trigger: (1) budget the effort on the firing path (exit code, record schema, disagreement surface), not on more prose; (2) when the record shows the class changed, void measurements quoted against the old class rather than inheriting them.",
  "falsifiability": "Proven wrong if an armed, loudly-recorded rare trigger fires and its record proves insufficient for the pre-written re-entry procedure (the schema didn't carry what was needed); or by observation over a long window where loudly-armed triggers fire and add no value over quiet refusals.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0650-lane7.md",
    "real_fire_record": "cold-drill-classchange-real-20261015.json (sha 2bd439df68617452, simulated_override: null, exit 7)",
    "re_anchor_record": "cold-drill-reanchor-record-gap0650-20261015.json (sha 4708c62ab7af6559, 30 trials, RED PASS)",
    "arming_origin": "t0581 (CLASS_PIN + check_machine_class() running first in main, machine_class stamped on every results header)",
    "migration": "AMD EPYC 9D25 126-Core -> 9D64 88-Core, fresh boot ~21 min before the run",
    "old_band_voided": "old band (1.027 center) retired; new band (1.549, 1.471, 1.414), center 1.478"
  },
  "related": ["CANDIDATE 403 / SN-1416 (prove guards on live ammunition)", "SN-01395 (flow equalization: owner per handoff with tripwire)"]
}
```
