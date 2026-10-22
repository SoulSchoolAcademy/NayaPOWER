Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The distill-daily boot-gate fix cured three defects in one sitting: a regex miss (fixed with re.I + bold-tolerance), an off-by-one in the defense-in-depth context window (the guard regex could never match — defense in depth that cannot fire is not depth), and a conflated failure note ("snapshot unreadable") that had hidden the regex miss — the snap-note was split with a loud degraded exit. The durable rule: **a gate's fallback or degraded path must name its degraded state** — a non-zero exit or an explicit DEGRADED marker naming which probe failed. A silent fallback is a lie with exit 0: downstream literal readers treat exit 0 as success and will "fix" good bytes on the gate's false word. And a conflated failure note attributes blame wrongly — split the failure signal by stage before anyone diagnoses.

## 🩷 HUMAN NOTE

Shawn — the boot gate was crying wolf: a literal reader following its FAILs would have "fixed" good boot bytes pointing at the live board #2793. The fix landed three changes: the real regex miss repaired, the failure signal split so each stage says what it probed, and the degraded path given a loud exit instead of a silent one. The gate now passes on good bytes and names the live board it read; when it degrades, it says so. The standing rule: no fallback path in a gate may exit 0 while masking a skipped or misfired probe — the next Naya writing a gate's fallback makes it loud, not silent.

## 🟣 CHILD NOTE

Imagine a smoke detector that, when its battery is low, stays silent instead of chirping — you'd think the room is safe, but the detector just isn't watching. And when it does beep, it says "something somewhere is wrong" without telling you whether it's smoke or battery. The good detector does two things: it chirps loudly when it's degraded (low battery), and it says exactly what it sees — "smoke in the kitchen." Gates work the same way: say when you're degraded, and say what you found.

## 🔵 GRANDMA NOTE

It's like a traffic light that goes dark instead of flashing yellow — drivers can't tell whether it's broken or the street is just empty, so they guess, and guessing causes crashes. A good light flashes yellow: "I'm degraded, proceed with care." And when the mechanic reads the fault log, it says which bulb failed — not "light unreadable." A gate's fallback must say it's degraded, and a failure note must name the failing part.

## 🟠 NAYA NOTE

Gate-conclusion discipline, Naya to Naya: a fallback path that exits 0 while masking a skipped or misfired probe manufactures false evidence — downstream seats inherit "PASS" for bytes the gate never actually checked. The boot-gate case is the worked proof: an off-by-one meant the defense-in-depth regex could never match (a guard that can't fire is a story, not a guard), and the conflated note "snapshot unreadable" sent the diagnosis at the wrong defect — the regex was the trigger, the conflated note was the real bug. Two moves, always together: (1) the degraded path exits non-zero or carries an explicit DEGRADED marker naming the failed probe; (2) failure signals split by stage — each probe names what it probed and what it found, never one merged "unreadable." The fix was proven the hard way: 3 code changes, 4 function probes, a full end-to-end PASS on a fresh clone, and a synthetic DEGRADED run with exit 1.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1824-degraded-gate-must-name-degradation",
  "lesson": "A gate's fallback or degraded path must name its degraded state: non-zero exit or an explicit DEGRADED marker naming which probe failed. A silent fallback is a lie with exit 0. Failure signals split by stage — each probe names what it probed — never one conflated note.",
  "applies_when": ["gate", "boot-gate", "guard", "fallback-path", "degraded-mode", "failure: silent-fallback"],
  "enforcement": "Every gate fallback path exits non-zero or emits an explicit DEGRADED marker naming the failed probe; gate review asserts no exit-0 path can mask a skipped or misfired probe. Failure notes name the failing stage (probe + bytes), never a conflated aggregate. Caught live in distill-daily-20261022-lane0: the defense-in-depth context window had an off-by-one so the guard regex could never match, and 'snapshot unreadable' hid the real regex miss.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/distill-daily-20261022-lane0.md (mirror lesson: 'the regex was the trigger, the conflated note was the real bug'; fix: regex re.I + bold-tolerant, snap-note split with loud degraded exit, defense-in-depth off-by-one cured; proven: 3 code changes, 4 function probes, fresh-clone e2e PASS, synthetic-degraded run exit 1)"
  ]
}
```
