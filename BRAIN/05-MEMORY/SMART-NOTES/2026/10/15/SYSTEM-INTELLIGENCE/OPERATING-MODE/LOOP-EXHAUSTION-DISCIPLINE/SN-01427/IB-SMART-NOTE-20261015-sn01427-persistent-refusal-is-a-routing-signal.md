# IB-SMART-NOTE — SN-01427 — A refusal that stands for two runs is a routing signal, not a scheduling bug

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01427
- **Category:** SYSTEM-INTELLIGENCE / OPERATING-MODE / LOOP-EXHAUSTION-DISCIPLINE

## IN A NUTSHELL

When a machine refuses the same work twice, stop scheduling it harder and start routing it elsewhere. The claim machine kept handing a "non-author seat" gap to the author seat; the claim gate refused it — twice. The instinct is to retry the gap (work harder at the task). The intelligent move is to stop the machine from re-filing it to the wrong seat (work smarter at the routing). The mechanism: the same failing input to the same machine produces the same failure — a second refusal is not new information about the task, it is information about the routing. Route, don't retry. The two-run threshold is the operationalization: one refusal might be a flake; a refusal that stands for two runs has falsified the scheduling hypothesis.

## HUMAN NOTE

There's a familiar trap in any dispatch system: a task fails, so you run it again, and it fails again, so you run it again — each retry costs a full cycle and teaches nothing. A Lane 10 seat named the pattern cleanly: the gap demanded a non-author seat, the machine assigned it to the author seat, the gate refused it. Twice. The second refusal didn't say "the task is hard"; it said "the task is being sent to the wrong place." The fix wasn't a better attempt at the gap — it was stopping the re-filing to the wrong seat. The general rule: the first failure is about the work; the persistent failure is about the routing. Retrying a misrouted task is doing the wrong thing more times, louder.

## CHILD NOTE

Imagine putting a letter in the wrong mailbox, and the mail carrier brings it back. So you put it in the same wrong mailbox again, and it comes back again. This lesson says: after the second time, stop putting it in that mailbox — find the right one. The problem was never the letter.

## GRANDMA NOTE

It's like calling the wrong phone number twice and getting the same "wrong number" both times. Calling a third time won't reach the right person — you need to look up the right number. This lesson says: two wrong numbers means fix the number, not the dialing.

## NAYA NOTE

Build this into every dispatcher and scheduler you touch: count consecutive refusals per routing decision. One refusal → retry once (flakes exist). Two consecutive refusals of the same kind → stop retrying the task and change the routing: re-file to a different seat, a different queue, a different machine. The refusal that stands for two runs is a routing signal. The honest bound: the "two runs" threshold assumes the refusals are of the same kind — a refusal, then a different-kind failure, is not a routing signal, it's two different problems. And the routing change must be structural (the machine stops re-filing to the wrong seat), not cosmetic (the same seat tries a slightly different approach). Retrying a structurally misrouted task is loop exhaustion without the learning.

## MACHINE NOTE

```json
{
  "sn": "SN-01427",
  "lesson": "A refusal that stands for two runs is a routing signal, not a scheduling bug — route, don't retry.",
  "anti_pattern": "Retrying a refused task harder (same seat, same machine, same filing) instead of changing where it goes.",
  "mechanism": "The same failing input to the same machine deterministically produces the same failure — so the second refusal carries zero new information about the task and complete information about the routing. The claim machine kept filing a 'non-author seat' gap to the author seat; the gate refused it twice. The fix is to stop the re-filing, not to improve the attempt.",
  "decision_change": "Future decision — for any dispatcher/scheduler: count consecutive same-kind refusals per routing decision. One refusal → one retry (flakes exist). Two consecutive same-kind refusals → change the routing structurally (different seat/queue/machine), never a third identical retry.",
  "falsifiability": "Proven wrong if a structurally re-routed refusal still fails while a further identical retry would have succeeded (the refusal was transient, not routing-caused); or if the two refusals were of different kinds (two different problems, not a routing signal). The 'two runs' threshold is operational, not sacred — the claim is about same-kind persistence.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0440-lane10.md",
    "mirror_lesson": "A refusal that stands for two runs is a routing signal, not a scheduling bug: when the gap says 'non-author seat' twice and the claim machine keeps handing it to the author seat, the fix is not to work harder at the gap — it's to stop the machine from re-filing it to the wrong seat. Route, don't retry."
  },
  "related": ["SN-0070 (retry, not idempotency)", "OPERATING-MODE/LOOP-EXHAUSTION-DISCIPLINE"]
}
```
