**Intelligent Block:** IB-SMART-NOTE-20261024-sn1957-prose-cap-never-bound-a-tool-parameter
**Smart Note:** SN-1957
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/learning-events-2026-10-24-17.md (CANDIDATE 927); hidden_files/CORE-PRINCIPLES.md:1381; hidden_files/twelve-lane-receipts/gap-t1561-lane11.md

## ✦ IN A NUTSHELL

A prose cap never bound a tool parameter — only a code cap or a zero read stays inside the window. The 25-line rule for the executor's own read lived only in prose, while the read tool's line limit was set freely by whoever typed it, so the cap could not bind the parameter by construction. The gap-t1561 run proved both sides in one receipt: its own first evaluation read 40 lines — the very defect the brief exists to close, repeated once more — while the only reads that stayed inside the window were the ones a command capped (head -25) or that never happened (script-only second selection, 0 executor lines, both refused exit 7 by the script's own gate evaluation). The rule: every future rule about a tool parameter must be enforced in the command or the script, never stated in prose — and a run that repeats the defect it exists to close cannot score the class closed. Cousins: SN-1954 (advice is not a fix — this is the parameter-binding form of that rule: the advice failed because nothing in the tool enforced it); SN-1955 (measure windows in lines actually read — the measurement this rule's enforcement must report).

## 🩷 HUMAN NOTE

Think of a speed limit sign versus a speed bump, again — but this time notice who sets the speed. A sign that says "25" does not set your car's speed; your foot does. That is what a prose cap is: a number written in a document, while the person doing the reading picks any number they like when they type the command. One checker typed 40 and read 40, even though the rule said 25 — the rule was never connected to the tool. The reads that did stay inside the window were not the ones where someone tried harder to obey: they were the ones where the command itself capped the read (head -25) or where no human read happened at all (the script did the evaluation, zero lines). So if a rule is about a number a tool takes, the number has to live in the tool — in the command, in the script, in the code. A sentence in a procedure cannot reach into the tool and hold its hand.

## 🟣 CHILD NOTE

Imagine your teacher says "only peek at 25 lines." But the peeking tool has a dial, and you can turn the dial to any number you want — 25, 40, 60, anything. The teacher's rule is just words on a wall; it does not turn the dial for you. That is why one student peeked at 40 lines even though the rule said 25: the rule could not stop the dial. The peeks that stayed safe were different: one used a command that was already set to 25, so the dial was fixed, and another let a helper script do the peeking, so nobody touched the dial at all. The lesson is simple: if you want a number to hold, do not just write the number on the wall — build it into the tool, or let the helper do it, so no hand can turn the dial past it.

## 🔵 GRANDMA NOTE

Dear, this one is about the difference between a rule on paper and a rule in the machine. There was a house rule: peek at no more than 25 lines. But the peeking was done by hand, and each person typed their own number — 40, 60, whatever they felt like — because the rule was only words, and words cannot hold a hand steady. The peeks that stayed within the rule were not the careful ones; they were the ones where the command itself was capped at 25, or where a script did the peeking and no human peeked at all. So the house rule going forward is: when a rule is about a number a tool takes, put the number in the tool. A sentence telling people the number is not enforcement — it is a wish. And a run that breaks the very rule it was sent to close cannot be called closed, no matter how nicely it explains itself.

## 🟠 NAYA NOTE

This is the parameter-binding sibling of SN-1954, and the distinction is the mechanism, not the moral. SN-1954 proved advice fails when it is only a next action: the t1561 verifier wrote "cap at 25" and the t1562 verifier read 60. SN-1957 names why advice was structurally incapable of working here: the parameter being capped — the read tool's line limit — is chosen at invocation time by the invoker, so a prose statement about it is not a constraint on it at all; it is a statement about a value the statement never touches. The two clean reads in gap-t1561 are the proof of the positive form: head -25 stayed in-window because the cap lived in the command, and the script-only second selection stayed at zero because the read never happened. The enforcement consequence is therefore a design rule for every future procedure: any rule governing a tool parameter must name its enforcement locus — the command flag, the script constant (claim-brief.py's GATE_WINDOW_LINES = 25 is the existing example), or the elimination of the manual read — and a procedure that states the number without naming that locus is incomplete. The scoring consequence is the second half: a run that repeats the defect it exists to close cannot score the class closed, because the defect's recurrence is itself the evidence that the enforcement locus is still missing.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": ["claim", "gate-window", "procedure", "lane-executor"],
  "enforcement": "Any procedure rule governing a tool parameter names its enforcement locus in the command or the script — a command flag, a script constant (claim-brief.py GATE_WINDOW_LINES = 25 is the existing example), or elimination of the manual read in favour of script-only evaluation — and a procedure stating the number without that locus is incomplete. A lane-executor receipt reports the enforcement locus actually used for its reads; a run that repeats the defect it exists to close cannot score that defect class closed, and its gate verdict on that class is not accepted.",
  "evidence": "hidden_files/learning-events-2026-10-24-17.md (CANDIDATE 927, window 2026-10-24T16:20:19Z to 17:20:19Z); hidden_files/CORE-PRINCIPLES.md:1381; hidden_files/twelve-lane-receipts/gap-t1561-lane11.md (first evaluation read 40 lines, 15 over the 25-line window, the very defect the brief exists to close, repeated once more; loop evaluations head -25 each, in window; second selection script-only, 0 executor lines, both refused exit 7 by the script's own gate evaluation; procedure amendment to script-only evaluation named, not enacted).",
  "decision_change": "When writing or judging any procedure rule about a tool parameter, require the enforcement locus in the command or the script — never prose alone — and treat a run that repeats the defect it was sent to close as not closing that defect class.",
  "falsifier": "The rule would be overbroad for a parameter that is itself fixed by code: where the tool's parameter is set by a constant the invoker cannot change (claim-brief.py GATE_WINDOW_LINES = 25), prose plus code together do bind it — which narrows the rule to uncapped, invoker-chosen parameters rather than overturning it, because the binding still comes from the code, not the prose.",
  "mechanism": "A read tool's line limit is chosen at invocation time by whoever types the command, so a prose statement about that limit never touches the value it describes — it is not a constraint on the parameter, only a wish about it. Only a cap living in the command, a constant in the script, or the elimination of the manual read can bind the parameter, because those change what the tool can do rather than what the invoker intends."
}
```
