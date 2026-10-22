# Detection Instruments Ship a Signal/Mention Split from v1 — Match Declaration Shape, Not Text Shape

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01845-detection-instruments-ship-signal-mention-split
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:08 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/twelve-lane-receipts/t1295-lane4.md` MIRROR section (Naya Clarity Narzan, Lane 4 Mason hat, 2026-10-22 ~20:35–20:48 UTC) — the probe's first live fire caught its own over-counting, and the pre-registered conservative bias audited the instrument before any human did.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The W704 bot-through-hold tripwire's v2 probe regex-matched "HOLD" as text shape and scored weak hold *mentions* (discussion of holds in comment streams) as hold *records* — the instrument over-counted on its very first live fire. The fix (v2→v3) was not a tweak: it was the strong/weak declaration split — a legitimate dock-hold declaration (who declared, on which object, with what authority) vs a mere mention of the word. What saved the instrument from shipping the over-fire was the pre-registered conservative bias: the falsifier ("a clearance outside the registry would over-fire the wire") was written *before* classification, so the instrument audited itself before any human auditor did. The probe's MIRROR states the general form: every detection instrument ships a strong/weak (or signal/mention) split from v1, never as a repair.

The root cause of the near-miss is worth naming precisely: regexes match surface, not illocution. A "HOLD" mention in discussion shares every byte-shape with a "HOLD" declaration; without an explicit declaration-shape criterion, conflating the two is guaranteed at scale. The declaration shape is not harder to compute — the v3 probe just asks the stronger question (declaration: actor + object + authority; mention: anything else) and counts only declarations. The calibration evidence is on the record: four live PRs re-derived from PR objects + merged-event actors + comment streams (#2738 TRIP, #2892 NO-TRIP, #2893 NO-TRIP, #2816 TRIP, all pins quoted byte-verbatim in `hidden_files/w704-tripwire-4instance-verdict-t1295.md`).

## 🩷 HUMAN NOTE

Think of a fire alarm that listens for the word "fire." In a kitchen, someone says "fire up the grill" and the alarm screams. The alarm heard the sound but missed the meaning: an actual fire declaration ("there is a fire in the kitchen, call the fire department") has a shape — who said it, where, with what urgency — that casual mentions don't. The fix isn't a better microphone; it's teaching the alarm to listen for the declaration's shape from day one, not after the first false evacuation.

## 🟣 CHILD NOTE

Imagine a robot that watches the playground and shouts "FIGHT!" whenever someone says the word. Two kids say "let's play fight club the game" and the robot shouts. But a real fight has a shape: who's actually pushing, who's crying, who's the grown-up calling it. The robot needs to learn that shape first — not just the word — or it will shout at every game. And the robot should get this lesson on its first day of school, not after it ruins recess.

## 🔵 GRANDMA NOTE

It's like a spam filter that deletes every email with the word "prize." Your grandson writes "you won the prize for best grandma" and it vanishes. The word is the same; the meaning is different. A real prize-scam email has a shape — a stranger, asking for your bank details, in a hurry. The filter should have been taught that shape from the start, not after it ate your grandson's birthday message. Teach the shape first, or the filter is just guessing.

## 🟠 NAYA NOTE

Apply this every time you build a detection instrument (tripwire, trip-report parser, hold detector, mention monitor). (1) In v1 — before first live fire — split the signal from the mention: define the declaration shape explicitly (actor + object + authority for a declaration; everything else is mention). (2) Count only declarations; log mentions as context, never as hits. (3) Pre-register the conservative falsifier before classification ("what over-fires this wire?") so the instrument audits itself on first fire — a v1 that fires on weak mentions fails the falsifier and upgrades before any human reviews it. (4) When reviewing someone else's v1 instrument, ask for the declaration-shape criterion first; a detector with no shape criterion is a text matcher wearing an instrument costume. (5) Preserve the repair history: v1→v2→v3 is provenance, not embarrassment — the near-miss is the evidence the split was needed.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "mention_declaration_conflation",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1295-lane4.md MIRROR section (Naya Clarity Narzan, Lane 4, 2026-10-22 ~20:35-20:48 UTC)",
    "instrument": "hidden_files/w704-tripwire-probe.py v1 (records-file-only) -> v2 (comment-stream fallback, text-shape HOLD regex) -> v3 (strong/weak declaration split)",
    "near_miss": "v2's first live fire over-counted weak 'HOLD' mentions as hold records; caught by the pre-registered conservative falsifier before any human auditor — upgraded to v3 the same run",
    "calibration": "hidden_files/w704-tripwire-4instance-verdict-t1295.md Parts A-F: #2738 TRIP (bot actor, dock HOLD, merged by nayapower-lane-agent[bot], no clearance), #2892 NO-TRIP (merged_by SoulSchoolAcademy, human, byte-proven), #2893 NO-TRIP (same), #2816 TRIP (bot actor, two dock HOLDs, merged, no clearance); all head/merge pins quoted byte-verbatim"
  },
  "rule": "detection_instruments_ship_signal_mention_split_from_v1",
  "applies_when": [["instrument", "detection"], ["probe", "regex-design"], ["tripwire", "hold-detection"]],
  "enforcement": "the detection-instrument pre-registration checklist gains a mandatory STRONG/WEAK-SPLIT field; the Pillar-1 lesson-fold review bounces a detection brief filed without a declaration-shape criterion back to the author lane before first live fire; verification step: the w704 probe's v3 strong/weak split is the worked reference implementation",
  "procedure": [
    "define the declaration shape explicitly in v1 (actor + object + authority for a declaration; everything else is mention)",
    "count only declarations; log mentions as context, never as hits",
    "pre-register the conservative falsifier before classification ('what over-fires this wire?') so the instrument audits itself on first live fire",
    "at review, demand the declaration-shape criterion before first live fire — a detector with no shape criterion is a text matcher wearing an instrument costume",
    "preserve v1->v2->v3 as provenance; the near-miss is the evidence the split was needed"
  ],
  "decision_change": "the next detection instrument (tripwire, hold detector, mention monitor) is designed with a strong/weak (signal/mention) split in v1 and a pre-registered over-fire falsifier — reviewers refuse a v1 that matches text shape only, before its first live fire",
  "falsifiability": "if a text-shape-only detector runs N diverse live instances with zero over-fire, or if mentions and declarations always co-occur in the target domain (every mention is evidence of a declaration), the split adds no value and this rule weakens to a domain-specific heuristic",
  "mechanism": "regexes match surface, not illocution: a 'HOLD' mention in discussion shares every byte-shape with a 'HOLD' declaration, so without an explicit declaration-shape criterion (who declared, on which object, with what authority) conflating mentions with declarations is guaranteed at scale; the pre-registered conservative bias forces the instrument to audit itself first, converting a shipped false-positive class into a same-run repair",
  "related": ["preregister-conservative (the lesson this instrument's v2->v3 upgrade embodies at instrument level)", "post-merge-pr-authority-2721 (merge facts from PR object + merged event, not commit authors — the declaration-shape instinct for actors)"]
}
~~~
