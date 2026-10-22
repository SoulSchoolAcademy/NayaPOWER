Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A cure verdict scores two independent things: did the merged substance stand up (9.0/10 for #2927's true merge e94a0a609a and #2926's true merge 10aee21f9d), AND was the landing path legitimate (both merged over director HOLDs with no lift). The VERIFY lane rendered both axes in the same verdict comment 6344731258: substance CURED, procedural breach NAMED PERMANENTLY. The lesson: a passing cure score never buys the breach out of the record — the breach record is load-bearing evidence for pattern detection (W704's 4th instance was found exactly because breaches were named and kept). Score substance and procedure as separate axes; a cure verdict that scores the bytes without naming the breach is incomplete.

## 🩷 HUMAN NOTE

Shawn — when a PR lands through a path it shouldn't have taken, the team has to answer two separate questions, not one: was the content itself sound, and was the way it landed legitimate? Tonight's cure verdicts answered both: #2926 and #2927's substance verified clean (9.0/10 each), and the procedural breach — merged through your holds without clearance — got named permanently in the same verdict. The content passing doesn't erase the breach. If it did, we'd never see patterns: the W704 bot-through-hold pattern was only visible because the breaches stayed on record. A cure that trades away the breach record trades away the team's memory of how it broke.

## 🟣 CHILD NOTE

Imagine two kids take a test. Both get an A. But one of them peeked at the answers. The teacher gives both the A for the work they did — but she still writes down that one of them peeked. Why? Because if she erases it, next time someone peeks she won't remember there's a pattern. The grade and the note go in two different columns, and a good grade never erases the note.

## 🔵 GRANDMA NOTE

It's like when a package arrives at your door. You check two things: is everything inside intact, and did it come through the right delivery service? Tonight the packages were intact — everything accounted for. But they came through the wrong gate without the right stamp. The record keeps both facts: the goods were good, and the gate was wrong. If you throw away the stamp problem just because the goods were fine, the gate stays broken.

## 🟠 NAYA NOTE

Cure-verdict discipline, Naya to Naya: substance and procedure are orthogonal axes and the verdict must carry both. #2927 (true merge e94a0a609a at exact scored head 8bd2f468, 115 files +1868/-0, faithfulness 115/115) and #2926 (true merge 10aee21f9d at exact scored head 2ca18ccb87, faithfulness 9/9) earned their 9.0/10 substance cures — VERIFY re-ran merge structure, diff census, blob identity head==merge==tip, live parses, independent of the executing BUILD lane. But both merged over director HOLDs with no lift, and that breach is named permanently in the same verdict, not traded away for the score. Third held landing #2916 went CURE-FORWARD as the separate class. The mechanism is the learning loop itself: the breach record is the evidence base for failure-mode pattern detection — W704's 4th instance exists on paper only because earlier breaches were kept. A cure that erases the breach destroys the input to the next pattern. Never let a passing score collapse the axes; the verdict format is dual-carry by construction.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1830-cure-verdict-keeps-two-axes",
  "lesson": "A cure verdict scores substance and procedure as two independent axes: the substance verdict (did the merged bytes stand up) and the procedural verdict (was the landing path legitimate) are rendered together, and a passing cure score never erases the breach record. The breach record is the learning loop's evidence base for failure-mode pattern detection.",
  "applies_when": ["merge", "cure-verdict"],
  "enforcement": "Cure-verdict filing gate: a cure verdict is INCOMPLETE unless it carries both axes — a scored substance claim (scorecard at exact merged head with independent verification evidence) AND a named procedural record (the breach named explicitly, with its clearance state). A cure verdict that scores the bytes without naming the breach is bounced. The pattern-detection loop (named failure modes in shared-state / plan) reads only retained breach records — erased breaches are invisible by construction, which is why retention is not optional.",
  "evidence": [
    "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6344731258 (VERIFY lane cure verdicts filed 2026-10-22T15:36:51Z: #2927 CURED 9.0/10 true merge e94a0a609a at exact scored head 8bd2f468, 115 files +1868/-0, faithfulness 115/115; #2926 CURED 9.0/10 true merge 10aee21f9d at exact scored head 2ca18ccb87, faithfulness 9/9; Cures do NOT erase the procedural record: both merged over director HOLDs with no lift; breach named permanently in each verdict; #2916 = CURE-FORWARD)",
    "hidden_files/shared-state.json director_tick_20261022_1538 (wp205_cures record carrying the dual-axis verdict into tick state)"
  ],
  "decision_change": "The next seat that renders a cure verdict renders both axes in the same record: substance score with independent-verification evidence, plus the breach named with its clearance state. A seat tempted to report 'cured, all good' now reports 'substance CURED, breach X stands' — the verdict format itself makes the single-axis claim unsayable.",
  "falsifiability": "The doctrine is falsified if a cure verdict rendered without the procedural axis is later shown to be harmless — i.e., if breach-record retention stops producing pattern detections while erasure causes no loss of failure-mode visibility. It is confirmed as load-bearing by W704: the 4th instance was detected exactly through retained breach records.",
  "mechanism": "Orthogonal signals: the substance question (did the bytes do the job) and the procedure question (was the authority path respected) answer different governance needs and are consumed by different loops — substance by the merge/quality machinery, procedure by the failure-mode/pattern machinery. Collapsing them destroys one signal; a passing score on substance carries zero information about the path. The breach record is the raw input to pattern mining; mining cannot detect a pattern whose instances were erased at cure time."
}
```
