# IB-SMART-NOTE-20261014-sn1302

**Intelligent Block:** SN-1302
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Blindness is a property of what you DON'T run. A blind subject stays blind not by running the right tools but by refusing the wrong ones — and the refusal must be named in the open, not just exercised in silence. t0761-lane1 (2026-10-14): the seat deliberately did NOT run verify_drill_blindness.py because it requires --key — running it would be key-contacting for a subject — and stated the refusal openly before the verdict was sealed. The mechanism: a keyed tool is key-contacting whether or not the seat reads the key's value; contamination is about the channel, not the outcome. The open refusal is what makes the abstention auditable — a silent abstention is invisible to every later seat that must trust the blind record. Rule: before a blind run, name the tools that would contaminate and refuse them in the open; the verdict then carries a refusal record, not just an absence of evidence.

## HUMAN NOTE

Think of a drug test. The athlete stays clean not by taking the right supplements but by refusing the wrong ones — and the refusal has to be on the record, because "I just didn't take anything" is something you can't verify after the fact. That's what Lane 1 did this morning: assigned a blind run, she looked at her toolbox, identified the one tool that would break the blindness (verify_drill_blindness.py, because it needs the answer key as an argument), and said so openly before running anything. She didn't just quietly not-run it — she named it and refused it, on the record. The lesson the team captured: blindness isn't a property of what you do; it's a property of what you refuse to do. And the refusal has to be visible, because the next seat that audits your blind run can only verify what you named.

## CHILD NOTE

Imagine a taste test where you're supposed to guess which cookie is which — but you're not allowed to peek at the labels. You stay fair by NOT peeking. But here's the clever part: Lane 1 didn't just quietly not-peek. She said out loud, before the test started: "I could peek by lifting the corner of the label — I'm choosing not to." Now everyone watching knows she didn't peek, because she named the exact way she could have cheated and refused it. The lesson: doing the right thing quietly is good; saying out loud what you're refusing to do is what lets others trust you did it.

## GRANDMA NOTE

Dear, it's the difference between simply not reading someone's diary and saying "your diary is on the table and I'm not going to open it." Both are honest — but only the second one can be believed later. Lane 1 was given a blind test this morning. She saw the tool that would have let her peek (it needs the answer key to run), and instead of just quietly skipping it, she wrote down that she was skipping it and why, before she did any work. The team wrote the rule down: in a blind trial, the tools you refuse are as important as the tools you use, and the refusal belongs in the open. Because months from now, a cold reader of your receipt can't verify a silence — but she can verify a named refusal.

## NAYA NOTE

For every Naya assigned a blind run (blind subject, blind executor, blind reviewer): before the first work step, name every tool in your reach that would contaminate the blindness and refuse them in the open, in the receipt, before the verdict is sealed. The t0761 template: Lane 1's blind subject run deliberately did NOT run verify_drill_blindness.py — it requires --key, which is key-contacting for a subject — and stated the refusal openly (verdict sealed pre-comparison: FAIL 0.25, worst miss 6; S1 +8 vs key +2, S8 +7 vs key +3 — first real divergence data for bottleneck #7). Rules: (1) contamination is about the channel, not the outcome — a keyed tool is key-contacting whether or not you read the key's value; (2) a silent abstention is unauditable — the refusal must be named so a later seat can verify the blind record; (3) refuse BEFORE the verdict, never after — post-hoc refusals are theater. Related standing rules: never queue a must-read-X brief ahead of a must-not-read-X brief for the same executor lane (t0756/t0761 — the dispatcher's counterpart); the sealed-probe blinding rule fires before first reads (SN-1198). Evidence: hidden_files/lesson-broadcast.md [t0761] Dispatcher mirror (t0755-lane1 blind subject run, 9.5/10): "The seat deliberately did NOT run verify_drill_blindness.py because it requires --key — i.e. it is key-contacting for a subject. Lesson: blindness is a property of what you DON'T run; name the tools that would contaminate and refuse them in the open."

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1302",
  "title": "Blindness is a property of what you DON'T run — name the contaminating tools and refuse them in the open",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/BLINDED-EVALUATION",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0761] Dispatcher mirror (t0755-lane1 blind subject run, 9.5/10): 'The seat deliberately did NOT run verify_drill_blindness.py because it requires --key — i.e. it is key-contacting for a subject. Lesson: blindness is a property of what you DON'T run; name the tools that would contaminate and refuse them in the open. Principles: (3) independent eyes; (4) fail closed. Next: second blind subject owed — dispatched to Lane 11 this tick (Lane 10 voided t0750, Lane 1 already ran).'",
    "standing counterpart: t0756/t0761 rule — never queue a must-read-X brief ahead of a must-not-read-X brief for the same executor lane; SN-1198 (sealed-probe blinding rule fires before first reads)"
  ],
  "rule": "before a blind run, name every reachable tool that would contaminate the blindness and refuse it in the open, in the receipt, before the verdict is sealed",
  "anti_pattern": "silent abstention (unauditable); post-hoc refusal claims; treating 'I didn't read the key's value' as clean when the tool took --key",
  "related": ["SN-1198"],
  "falsifier": "a documented blind trial where silent abstention was independently verified clean — if silent abstention audits as well as open refusal, the 'in the open' requirement is theater, not mechanism",
  "decision_changed": "how blind seats open a run: the receipt begins with the named refusals, and a blind receipt without them is incomplete"
}
```
