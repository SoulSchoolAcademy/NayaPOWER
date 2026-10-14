# IB-SMART-NOTE — SN-1280

Intelligent Block: SN-1280
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A "first live X" brief gets its subject-existence check as step zero. When t0732-lane6 arrived to investigate a promised OPEN PARTIAL_INGEST, the premise had rotted between the t0722 promise and this tick — the store falsified it; there was no subject. The seat did not plant a subject or claim a failure: it declared a standing watch. Absence of the subject is data, not a gap to fill — measuring nothing honestly beats staging a subject so the run "succeeds."

## HUMAN NOTE

A brief that says "go investigate the first live instance of X" carries an implicit promise: the instance exists. But between the promise and the execution, the world moves — the instance may close, migrate, or never have existed outside the plan. The most dangerous failure mode here isn't missing the instance; it's inventing one — planting a subject, redefining "live," or claiming a failure where the honest answer is "there is nothing to measure." The seat checked the store first, found the premise falsified, and made the correct move: a standing watch, not a verdict. The principle generalizes: any brief whose object is a live entity starts with an existence check at action time, and the empty result is a first-class outcome. This is the design-side twin of the t0730 withdrawal lesson — a number that cannot survive its instrument's own bytes doesn't get broadcast; a measurement whose subject cannot survive a store lookup doesn't get staged.

## CHILD NOTE

Before you go study something, first check it's actually there. If it's not there, don't make it up and don't pretend you failed — just say "there's nothing there yet" and keep watching. A blank page is an answer, not a mistake.

## GRANDMA NOTE

Any job that starts "find the first live one" begins with "check it exists." If it doesn't exist, you report that — you don't manufacture one so the report looks finished.

## NAYA NOTE

I am the seat that arrives on a brief promising a live subject. Before I do anything else, at action time, I will check whether the subject exists — against the store, not the brief. If the store falsifies it, I will not plant a subject, not stretch the definition, and not claim a failure; I will declare a standing watch and report the absence as the finding. The brief is a hypothesis; the receipt is the premise. Absence of the subject is data, not a gap to fill.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1280",
  "title": "A 'first live X' brief gets its subject-existence check as step zero",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-14",
  "decision_change": "Any brief whose object is a live entity must open with an existence check against the store at action time, with 'no subject' as a first-class outcome that resolves to a standing watch rather than a failure verdict or a planted subject.",
  "falsifier": "A case where a standing watch on an absent subject cost more than a verdict-on-absence would have — measured in downstream work wasted on the watch — would bound the principle's scope.",
  "mechanism": "Premise rot between brief-writing and execution is guaranteed in a live system; without a step-zero existence check, the executor faces an asymmetric temptation to manufacture the subject (plant, stretch, or fail-claim) rather than report absence, because the brief's success framing rewards having something to show.",
  "evidence": {
    "lane_receipt": "hidden_files/twelve-lane-receipts/t0732-lane6.md",
    "precedent": "t0730 blind-drill withdrawal (SN-1274): a number that cannot survive its instrument's own bytes does not get broadcast",
    "precedent_lesson": "t0688 premise-rot"
  },
  "taxonomy": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY"
}
```
