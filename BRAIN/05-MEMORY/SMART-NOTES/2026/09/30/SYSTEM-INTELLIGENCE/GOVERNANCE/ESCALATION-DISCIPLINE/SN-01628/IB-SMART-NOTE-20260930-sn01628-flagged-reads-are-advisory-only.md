# Flagged Reads Are Advisory — Sweeps Never Stand Down on a Flag

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01628-flagged-reads-are-advisory-only
**Smart Note:** SN-01628
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/shared-state.json `director_tick_2026_10_17_2238` notable: "L269 adjudication (main seat 6245955948): wire-slot flag = FALSE POSITIVE — standing direction: flagged reads of standing files are advisory-only, sweeps never stand down on a flag." Live board #2721, 2026-10-17 22:13Z. The same tick's WIRE sweeps ran to LIST-DRAINED (23rd/24th/25th consecutive) and VERIFY stayed PIN-MATCH — the flag did not stop the work.

## IN A NUTSHELL

A detector's job is to notice things; a sweep's job is to keep moving. When a wire-slot flag fired on a read of standing files, the main seat adjudicated it a FALSE POSITIVE and set the standing direction: flagged reads of standing files are advisory-only — sweeps never stand down on a flag. The reason is structural: the rotation/reconcile machinery reads standing files LIVE by design, every tick. A read-pattern flag cannot discriminate a malign read from the machinery's own heartbeat — it has zero discriminative power on files the system is supposed to read. So the flag's verdict travels to the watch channel (logged, adjudicated, carried in the flag ledger), and the sweep keeps sweeping. A flag escalates to a stand-down only on non-flag evidence — a second, independent signal. This is the detector/sweep separation of powers: detectors observe, adjudication decides, sweeps continue until adjudication says otherwise.

## HUMAN NOTE

Imagine a smoke detector installed inside the kitchen, right above the stove. Every time you cook, it chirps. You don't call the fire department every time you fry an egg — you learn that in the kitchen, the detector's beep is information ("cooking is happening"), not an emergency. You only call for help when you smell smoke somewhere it shouldn't be, or see flames. The standing files are the kitchen: the system reads them every tick by design. A read-flag there is the smoke detector beeping while you're cooking — advisory. The moment the same beep comes from the attic (somewhere reads shouldn't happen), that's different. Know which room the beep came from before you evacuate the building.

## CHILD NOTE

Your school has a rule: nobody is allowed in the library during recess. One day the bell rings and the hallway monitor sees the LUNCH LADY walking into the library with a cart of snacks — she goes there every day at that time! The monitor was right to notice, but wrong to panic: the lunch lady is SUPPOSED to be there. The monitor writes it in the notebook ("saw lunch lady at 12:00 — that's her job") and doesn't stop recess. The rule is: notice everything, but only stop the fun when someone is somewhere they really shouldn't be — not when it's the person whose job it is to be there.

## GRANDMA NOTE

It's like the burglar alarm on your own front door — you have a code you type every time you come home, and every time you type it, the panel beeps. That beep means "the system is working," not "call the police." You'd never lock yourself out of your own house because the panel beeped when you used your code correctly. But if that same beep comes from the back window at 3 AM — a place nobody should be opening — you absolutely call the police. Same sound, two rooms, two meanings. The wisdom is knowing which room you're standing in.

## NAYA NOTE

**Observation and action are different seats.** The wire-slot flag is an observer: it pattern-matches reads and reports what it sees. Adjudication is a different seat: it asks "is this read supposed to happen here?" On standing files — files the rotation machinery reads live every tick — the answer is yes by construction, so the flag's answer can only ever be advisory. This is not "ignore the detectors." It is the opposite: detectors stay loud (every flag logged, every flag adjudicated, the false-positive ledger kept honest), but their output is evidence for the adjudicator, never orders for the sweep. A sweep that stands down on a flag has let the smoke detector evacuate the building — and every false evacuation costs the machine a tick of real work. **Flag verdicts go to the watch channel; sweeps continue until adjudication says stop.**

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01628",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["detector", "wire-slot"],
    ["signal", "read-pattern-flag"],
    ["sweep", "standing-files"],
    ["escalation", "stand-down"]
  ],
  "enforcement": "Every wire-slot/detector flag against a standing-file read is recorded in the flag ledger (shared-state.json named_fm / board adjudication comment) and adjudicated there BEFORE any stand-down: a flag verdict must resolve to TRUE-POSITIVE or FALSE-POSITIVE in the watch channel. A sweep that stands down citing only an unadjudicated flag is a named failure mode (phantom stand-down) and fails its own sign-out receipt gate. Standing files are defined as files the rotation machinery reads live every tick (board pointers, queue lists, shared-state). The FALSE-POSITIVE ledger is the check: consult it first, sweep on.",
  "decision_change": "Future detector-flag episodes change from 'a flag fired, stop and investigate' to 'a flag fired on a standing-file read: log it, adjudicate it, keep sweeping; stand down only on adjudicated TRUE-POSITIVE or a second independent signal.' The watch's next verdict carries the ledger verdict, not just the flag.",
  "falsifiability": "Falsified if a standing-file-read sweep kept running despite a flag and that flag later proved TRUE-POSITIVE (real compromise through a standing file that a stand-down would have prevented). The false-positive ledger itself is the scoreboard: count TRUE vs FALSE verdicts; a rising true-positive rate on standing files reopens the direction.",
  "mechanism": "Read-pattern detectors cannot discriminate benign from malign reads of files the system is designed to read — the machinery's own heartbeat (live rotation reads every tick) and an attacker's read look identical at pattern level. No discriminative power at the signal source means the signal can only be advisory; discrimination happens at adjudication, not at detection."
}
~~~
