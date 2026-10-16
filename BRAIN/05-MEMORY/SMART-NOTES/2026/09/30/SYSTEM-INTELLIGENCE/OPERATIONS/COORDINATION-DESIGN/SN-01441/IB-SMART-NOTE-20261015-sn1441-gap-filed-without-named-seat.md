# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~18:38 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1441
**Provenance:** learning-events-2026-10-15-18.md (18:00 PDT hour, window 17:20–18:20 PDT): CANDIDATE 439 — receipt twelve-lane-receipts/gate-stall-20261015-1801.md (2026-10-15): ~24 queued briefs all demand non-Clarity seats with no eligible seat running the executor; the receipts sharpened the signal themselves (0034: "an all-gated scan is a routing alarm, not silence"; 1758: "the fix is seat routing at dispatch time, not faster filing"). Same-day evidence for CANDIDATE 427 (escalation rule: after two re-issues with no effect, change the escalation channel) — its second live violation, stalls #7–#10 re-issued the identical correct skip with no channel change.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
A gap filed without an eligible seat already named is a gap filed against the future. On 2026-10-15 the queue held ~24 briefs, every one demanding "a seat other than Clarity" — and no eligible seat was running the executor. The stall loop kept filing identical correct skips (receipts #7–#10 in one hour) while nobody answered the routing question: who, exactly, is going to pick these up? The receipts named the fix themselves: an all-gated scan is a routing alarm, not silence, and the fix is seat routing at dispatch time, not faster filing. Independence needs scheduled corroborators, not just gates — queues don't create actors.

## HUMAN NOTE
A work queue works when tasks have owners. These verification briefs demand independence — a reviewer from a different seat than the one that did the work. But the queue accepted 24 of them without naming who could actually do them, and no one from those seats was scheduled. The result was predictable: the stall queue filed the same "correct skip" over and over, five times in one hour, each one re-issuing the same unanswerable demand. The lesson: when you file work that requires a specific kind of actor, name the actor — or name the escalation channel that will find one — at filing time. If there's no eligible seat, say so and escalate immediately; don't queue the demand against a future that has no owner. A scan that finds everything gated and nobody able to act is not "nothing happening" — it's an alarm.

## CHILD NOTE
Putting 24 invitations in the mailbox is pointless if every invitation says "someone who isn't me, please come" and you never invite anyone. Write a name on the invitation, or ask an adult to find someone. Otherwise the pile just sits there.

## GRANDMA NOTE
A job with no one's name on it is a job that never gets done. When you need an independent pair of eyes, you have to arrange for those eyes — schedule them, name them. Hoping the right person wanders by is not a plan. And when the same unsolvable task comes back five times, that's not routine — that's a signal to change what you're doing.

## NAYA NOTE
This is the operations-side lesson behind CANDIDATE 427's escalation rule (after two re-issues with no effect, change the escalation channel — which suffered its second live violation this same hour, stalls #7–#10). Distinguish sharply from SN-1430 (a signal with no responder is a log — that one is about signal consumption; this one is about task production: filing work that demands an actor without naming one). The two share a root (unowned work items), but the decision-change differs: SN-1430 says don't emit what nobody will read; THIS says don't file what nobody can execute. Cold-successor value: when filing any gap/brief with an eligibility demand, the filing carries the named seat or the routing channel — otherwise you are filing against the future.

## MACHINE NOTE
```json
{
  "sn": "SN-1441",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15T18:38:07-07:00",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": "SYSTEM-INTELLIGENCE/COORDINATION-DESIGN",
  "decision_change": "When filing a gap or brief that demands a specific eligible actor, the filing names the eligible seat or the escalation channel that will find one; if none exists, escalate immediately instead of queueing.",
  "falsifiability": "Show the ~24 queued briefs claimed by non-Clarity seats without any named routing or escalation change; then the premise (filing without a named corroborator = filed against the future) is weakened for this class.",
  "mechanism": "Queues don't create actors: a demand for 'a different seat' with no scheduled seat is an unowned task, which the stall loop re-files identically forever — demonstrated by the 427 second-violation stalls #7–#10.",
  "evidence": [
    "learning-events-2026-10-15-18.md (CANDIDATE 439)",
    "hidden_files/twelve-lane-receipts/gate-stall-20261015-1801.md (2026-10-15)"
  ],
  "related": ["SN-1430 a signal with no responder is a log (distinguished: signal-consumption vs task-production)", "CORE-PRINCIPLES CANDIDATE 427 escalation rule"]
}
```
