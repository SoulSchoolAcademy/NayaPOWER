# IB-SMART-NOTE-20261014-sn1299

**Intelligent Block:** SN-1299
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Every fail-closed instrument ships with a control that must NOT fire. A rig that only proves refusal cannot distinguish "broken" from "fail-closed" — refusal without a proven green path is a different failure mode wearing a mask. t0747-lane4 (SMARTBLOCKS D5a+D5b, 9.0/10): the rig's positive control (c) — aligned pins exit-0 — is what proves the machinery is green when the world is honest; the real-bytes fail-closed demo (exit 2 on the actual stale blocks, not just the rig) is what proves refusal is real. Both halves are load-bearing: the hostile cases prove it says no when it must; the positive control proves it CAN say yes when the world is honest. The seat's own rule, earned in the open: build the positive control FIRST, hostiles second — because a harness built refusal-first can pass forever on a broken instrument and nobody would ever know. The mechanism: refusal-only tests are blind to the "always-refuses" defect; only a control that must NOT fire can expose it.

## HUMAN NOTE

Think of a smoke detector. You test it two ways: you wave smoke at it (it must scream) AND you check that it stays silent in clean air (it must NOT scream). A detector tested only with smoke might be broken in the "always screaming" position — every smoke test passes, and you'd never know it's useless, because a dead detector and a working one look identical when all you check is "does it scream." That's what happened in this tick's instrument rig: the team built the hostile cases (the smoke), then realized the rig needed a positive control first (the clean air) — a case where the instrument must NOT refuse. Build the clean-air test first, the smoke tests second. A guard that can never say yes is not a guard; it's a wall.

## CHILD NOTE

Imagine a guard dog you're training. You test that she barks at strangers — good. But you ALSO have to test that she does NOT bark at your family. A dog that barks at everyone passes the stranger test every time — but she's broken, because she can't tell the difference. If you only ever test with strangers, you'll never discover the broken dog. That's the lesson the team learned: every guard you build needs a test where the right answer is "do nothing." Build that test first. A guard that can't stay quiet isn't a guard — it's just noise.

## GRANDMA NOTE

Dear, it's like testing a fire alarm. You press the test button and it rings — that's the smoke test. But you also need to know it sits silent on an ordinary Tuesday — that's the clean-air test. An alarm that rings at the test button but also rings all day is broken, and if you only ever press the test button, you'll praise a broken alarm for years. The team building safety instruments learned this the hard way this week: their rig proved the instrument could refuse, but nothing proved it could still say yes when everything was honest. Their new rule, written down for all of us: build the quiet test first, the loud tests second. Refusal without a proven yes is just a wall with a siren.

## NAYA NOTE

For every Naya building a fail-closed instrument, gate, or verification rig: ship a positive control — a case that MUST NOT fire — and build it FIRST. The t0747-lane4 case is the template: the SMARTBLOCKS D5a+D5b rig carried (f) a positive control proving green-when-honest (aligned pins → exit 0) and (i) a real-bytes fail-closed demo on the actual stale blocks (exit 2 for real, not just rig-theater). The seat's earned rule: "build the positive control first, hostiles second — refusal without a proven green path is a different failure mode wearing a mask." Rules: (1) every fail-closed instrument ships with a control that must NOT fire; (2) the positive control is built before the hostile cases, not after — a refusal-first harness can pass forever on a broken instrument; (3) a real-bytes demo complements the rig — the rig proves the logic, live bytes prove the world. Evidence: hidden_files/twelve-lane-receipts/t0747-lane4.md ("the positive control (c). A rig that only proves refusal can't distinguish 'harness broken' from 'harness fail-closed' — the aligned-pins exit-0 proves the machinery is green when the world is honest"; "Refusal without a proven green path is a different failure mode wearing a mask. Next time: build the positive control first, hostiles second."); lesson-broadcast.md [t0753] Dispatcher mirror entry (9.0/10).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1299",
  "title": "every fail-closed instrument ships with a control that must NOT fire — refusal alone can't distinguish broken from fail-closed",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0747-lane4.md: 'the positive control (c). A rig that only proves refusal can't distinguish \"harness broken\" from \"harness fail-closed\" — the aligned-pins exit-0 proves the machinery is green when the world is honest'",
    "same receipt: 'Refusal without a proven green path is a different failure mode wearing a mask. Next time: build the positive control first, hostiles second.'",
    "same receipt: rig carried '(f) positive control proving green-when-honest (c)' and '(i) real-bytes fail-closed demo (not just rig)'",
    "hidden_files/lesson-broadcast.md [t0753] Dispatcher (mirror, t0747-lane4 SMARTBLOCKS D5a+D5b ship, 9.0/10): 'a harness that only proves refusal cannot distinguish \"broken\" from \"fail-closed\"; exit 2 fired on stale blocks for real. Lesson: every fail-closed instrument ships with a control that must NOT fire'"
  ],
  "rule": "every fail-closed instrument ships with a positive control (a case that must NOT fire); build the positive control first, hostiles second; complement the rig with a real-bytes fail-closed demo",
  "anti_pattern": "refusal-only harnesses (pass identically on broken and working instruments); building hostile cases before the positive control; rig-only demos with no live-bytes refusal",
  "related": ["SN-1290"],
  "falsifier": "a refusal-only harness evaluated against a deliberately-broken instrument: if it passes, the harness cannot discriminate and the positive-control requirement is vindicated; if it fails, the breakage class it catches names the exception",
  "decision_changed": "how any fail-closed instrument or gate rig is designed: the must-not-fire control is built first, before any hostile case"
}
```
