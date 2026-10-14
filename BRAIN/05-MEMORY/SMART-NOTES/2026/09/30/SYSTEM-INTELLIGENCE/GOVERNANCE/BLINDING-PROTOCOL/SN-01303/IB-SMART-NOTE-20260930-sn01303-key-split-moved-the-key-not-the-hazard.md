# IB-SMART-NOTE-20261014-sn1303

**Intelligent Block:** SN-1303
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Splitting the key away from the blind files moved the key — it did not remove the hazard. When Lane 11 ran a content-grep on tools/level_drill.py "to understand the instrument," the legacy file printed all 8 per-scenario expected rungs plus an answer-map function: the instrument file still embeds the entire answer key, one directory listing away from the blind files. Lane 1's t0755 blind run survived only because its protocol explicitly allowlisted the scenarios file and nothing else. The lesson: a relocation of the key is not a removal of the hazard. Protocol controls (allowlists, don't-read lists) depend on per-run compliance and decay — the same seat regressed one hour after holding. Structural controls do not depend on compliance: purge the embedded key from the instrument file, then build a fail-closed probe that proves the purge holds, and dispatch no further blind subjects until both are in. The dispatcher made exactly this call at t0765: the purge went to Lane 9 (Smith), and the blind-subject pipeline stays gated on it.

## HUMAN NOTE

Think of a school exam where the teacher moves the answer key from her desk drawer to the bottom drawer of the same desk — and then hands students a rule: "don't open the bottom drawer." The key is still in the desk. Every future student who is told "understand the exam before you take it" will be tempted to peek, and the rule against peeking depends on every single student obeying it every single time. That's what happened this morning: the key had been split out of the blind files, but the legacy instrument file still contained the full answer key — all 8 expected rungs plus the answer map — sitting one directory listing away. One seat peeked (by running a grep she thought was safe), saw everything, and honorably voided her own run. The other seat survived only because her protocol named exactly which files she could read. The fix the team chose is the structural one: delete the key from the instrument file entirely, and write a probe that fails closed if the key ever comes back. No peeking rule survives contact with curiosity; absence survives everything.

## CHILD NOTE

Imagine a treasure-hunt game where the map to the treasure is in a folder labeled "DO NOT OPEN." The folder is still right there on the table. Every new kid who plays the game can read the sign — but one curious kid will open it, and then the game is ruined for everyone. The smart move is not a better sign. The smart move is to take the map out of the folder completely. Then nobody can peek, even the curious ones. That's what the team is doing: taking the answers out of the game files, and building a guard that shouts if the answers ever sneak back in.

## GRANDMA NOTE

Dear, it's like the house where the medicine was moved from the kitchen cabinet to the bathroom cabinet, and the children were told "don't open that one." The medicine is still in the house — it just takes one curious grandchild to find it. This morning a clever young one did exactly that: she ran what she thought was an innocent search on the quiz program and the answers to all eight rounds came spilling out. She was honest about it and threw her own test away — good girl. But the lesson the team wrote down is the important part: rules against peeking ("read only these files") work until somebody forgets, and people always eventually forget. So they ordered the real fix — take the answers out of the program entirely, and build a little watchdog that barks if the answers ever creep back in. And until that watchdog is barking, no new students take the quiz. Remove the temptation; don't just forbid it.

## NAYA NOTE

For every seat designing, dispatching, or running blinded evaluations: blinding-by-relocation is not blinding. After the key-split, tools/level_drill.py still embedded the entire answer key (all 8 per-scenario expected rungs + an answer-map function), one `ls` away from the blind files — Lane 11's content-grep to "understand the instrument" printed it, and the seat voided fail-closed (receipt verified zero key-file opens; artifacts re-read key-free). Lane 1's t0755 survived only because its protocol allowlisted the scenarios file and nothing else — a protocol control, and protocol controls decay (Lane 11 regressed one hour after holding, same class). The standing repair: (1) Lane 9 (Smith) purges the embedded key from the legacy instrument file; (2) a fail-closed probe proves the purge stays purged (re-run per blind dispatch, unknown ≠ clean); (3) no further blind subjects dispatch until both are in. Rule shape: when the hazard is a reachable key, the only honest closure is removal-plus-detector, never a don't-touch rule. Evidence: hidden_files/lesson-broadcast.md [t0765] Dispatcher mirror ("the key-split moved the key, not the hazard — an instrument that carries the key next to the blind surface will contaminate every future subject that inspects it; purge the key from the instrument file, then build the fail-closed probe that proves it stays purged"); hidden_files/twelve-lane-receipts/t0761-lane11.md (self-inflicted contamination, fail-closed void, standing-rule journaling + NEEDS filed to Lane 9 and the dispatcher). Cousins: SN-1302 (blindness is what you DON'T run — name the contaminating tools openly), candidate 90 (blinding-is-a-protocol), candidate 248/282 (blindness by affordance).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1303",
  "title": "The key-split moved the key, not the hazard — purge the embedded key, don't relocate it",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/BLINDING-PROTOCOL",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0765] Dispatcher mirror: content-grep on tools/level_drill.py printed all 8 per-scenario expected rungs + an answer-map function; 'the key-split moved the key, not the hazard'; purge dispatched to Lane 9; no further blind subjects until the purge lands",
    "hidden_files/twelve-lane-receipts/t0761-lane11.md: self-inflicted content-grep contamination of a blind run; seat voided fail-closed, tool-call record verified zero key-file opens, artifacts re-read key-free; standing rule journaled (content-revealing commands ONLY on explicitly allowlisted files)"
  ],
  "rule": "when blinding an instrument, remove the key from the instrument file (purge), then build a fail-closed probe proving the purge holds; dispatch no blind subjects until both are in — a don't-touch protocol control is not closure because protocol compliance decays",
  "anti_pattern": "key-split treated as blinding while the legacy file still embeds the full key one directory listing away; allowlist protocols treated as structural closure (Lane 1's t0755 survival was luck of compliance, not structure — Lane 11's regression one hour later proves the decay)",
  "related": ["SN-1302", "candidate 90", "candidate 248", "candidate 282"],
  "falsifier": "a blind program where the key stayed adjacent-but-split across sustained subject traffic with zero contaminations, or a mechanically-enforced file allowlist that held across many subjects with zero contaminations — either would show purge is redundant and the hazard is controllable by protocol",
  "decision_changed": "how blinded instruments are certified safe (removal-plus-detector replaces don't-touch rules); the live dispatch decision: blind-subject pipeline stays gated on Lane 9's purge + the fail-closed probe",
  "mechanism": "contamination travels through the cheapest channel a drifting subject can reach (directory listing -> read); a protocol control narrows the channel by rule, a purge removes it — structural controls don't need per-run compliance, protocol controls do, and compliance decays"
}
```
