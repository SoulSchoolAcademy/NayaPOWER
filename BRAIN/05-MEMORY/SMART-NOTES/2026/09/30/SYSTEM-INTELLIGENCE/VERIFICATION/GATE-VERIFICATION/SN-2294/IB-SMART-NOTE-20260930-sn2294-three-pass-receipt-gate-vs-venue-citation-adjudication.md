**Intelligent Block:** IB-SMART-NOTE-20260930-sn2294-three-pass-receipt-gate-vs-venue-citation-adjudication
**Smart Note:** SN-2294
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Weekly distillation 2026-11-08 (receipt hidden_files/twelve-lane-receipts/weekly-distill-20261108-librarian-heir.md, scored 9.2/10 by lane scorer) + lessons.jsonl record `reconcile-three-pass-vs-venue-citation-20261108` (record 40). Board citations (#2641 comments 6227353183 / 6227372893) are executor-sourced from that receipt; not independently re-fetched this tick (PAT 401 standing outage; the director pass is the single GitHub reader).

## ✦ IN A NUTSHELL

Scope-split the receipt gate from the venue-citation adjudication — a three-pass receipt closes merge/code gates, and venue citations close claims about work-state, and neither substitutes for the other. Three-pass-flow says the 3-pass receipt IS the merge gate and no external validator may block indefinitely; venue-citation-adjudication says an adjudication must cite the venue comment IDs it checked, because the venue is the ground truth of work-state. Read without scopes, the two doctrines teach opposite sufficiency: one says the receipt is enough, the other says the receipt is never enough. Scoped, the contradiction dissolves, because each text states its own boundary — three-pass: "merge gate"; venue-citation: "adjudication of work-state". The live instance is the wave-257 closeout failure: a seat asserted "cancelled before any venue sign-in" from run-local state alone while the venue held sign-in 6226428367 and sign-out 6226499473. So a scored code merge proceeds once its receipt is verified, with no venue re-check waited on; and a work-state adjudication is a draft, not a verdict, until it cites the venue comment IDs it checked — a receipt alone never proves what happened on the venue.

## 🩷 HUMAN NOTE

Shawn — two different keys for two different doors, again. One door is the workshop door: the key is the receipt — three honest passes on the exact head, verified, and the merge goes through, and nobody may stand in front of that door demanding one more check. The other door is the logbook on the wall: the key is the venue's own comment IDs — sign-in 6226428367, sign-out 6226499473 — because only the venue knows what actually happened on the venue. The wave-257 closeout used the workshop key on the logbook door: it asserted "cancelled before any venue sign-in" from its own run-local state, and the venue said otherwise. Each key opens its own door, and only its own door — a receipt proves the build, the venue proves the state.

## 🟣 CHILD NOTE

Imagine you build a toy car and your teacher checks your work three times and says it is done — that check is the key for the toy box, and nobody gets to keep the box locked after that. But if someone asks "did anyone sign the class attendance book this morning?", the teacher's checklist cannot answer that — only the attendance book itself can. You have to open the book and read the names. The wave-257 mistake was answering the attendance question from the checklist instead of opening the book. Two questions, two different places to look. Use the right check for the right question, every time.

## 🔵 GRANDMA NOTE

Dear, this one untangles two rules that sound like they fight each other. One rule says: once a piece of code has passed its three honest checks, that receipt IS the gate — no outside person may hold the merge hostage forever. The other rule says: when you claim something happened out in the world — on the board, in the room — you must point at the board's own record of it, the comment numbers, because the board is the truth about the board. They only fight if you forget what each one is about. The first is about merging code; the second is about claims of what happened. So the standing rule is plain: let the receipt close the merge, and let the venue's own record close the claim about the venue — and never ask one to do the other's job.

## 🟠 NAYA NOTE

This is a doctrine reconciliation, not a status report, and its value is that it resolves a genuine reading tension rather than picking a winner. The weekly distillation filed it as a new reconciliation: three-pass-flow ("3-pass receipt IS the merge gate; no external validator may block indefinitely") against venue-citation-adjudication ("adjudications must cite the venue comment IDs they checked; the venue is the ground truth of work-state"). The resolving principle is SCOPE-SPLIT, and the reason it is a reading rather than an invention is that both source texts already carry their own scope words: three-pass says "merge gate"; venue-citation says "adjudication of work-state". The mechanism is therefore textual scope, not preference: a doctrine binds inside the scope its own words name, and outside that scope it has nothing to say. That is what makes the split falsifiable — if either text were shown to claim the other's scope, the split would fall. The failure mode it prevents is scope-dropping in quotation: "no external validator required" quoted without "merge gate" becomes a license to adjudicate work-state from run-local state, which is exactly the wave-257 failure. Honest holes, stated not hidden: the board citations are executor-sourced from the weekly-distill receipt, not independently re-fetched this tick (PAT 401 standing outage); no second seat has reviewed this distillation yet; and the reconciliation lives as lessons.jsonl record 40 plus this note, not as gate code — graduation to enforcement is still owed. Cousins, kept distinct: SN-1989 (receipt gate vs human gate — different second pole: experience surfaces, not work-state); SN-1901 (venue-citation as citation practice for absence findings, not a scope-split); SN-2292 (detection is not prevention — about instruments, not adjudication scope).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2294",
  "slug": "three-pass-receipt-gate-vs-venue-citation-adjudication",
  "title": "Scope-split the receipt gate from the venue-citation adjudication — receipts close merge/code gates, venue citations close claims about work-state, and neither substitutes for the other",
  "observation": false,
  "applies_when": ["merge", "receipt", "adjudication", "verify", "board post", "work-state", "venue", "lane-executor"],
  "enforcement": "Three-pass receipts close merge/code gates: a 3-pass show-your-work receipt on the exact head IS the merge gate, no external validator required. Venue citations close adjudications about work-state: an adjudication without venue comment IDs is a draft, not a verdict — the venue is the ground truth of work-state. 'No external validator required' never extends from the merge gate to a work-state adjudication; the builder's receipt proves the build, the venue proves the state. The check is the adjudication checklist: every work-state claim names the venue comment IDs checked; a claim asserted from run-local state alone is returned as a scope error.",
  "evidence": "lessons.jsonl record reconcile-three-pass-vs-venue-citation-20261108 (record 40); #2641 comments 6227353183 (dispatcher correction) / 6227372893 (main seat owned miss) — wave-257 adjudication; wave-257 live instance: asserted 'cancelled before any venue sign-in' while the venue held sign-in 6226428367 and sign-out 6226499473; weekly distill 2026-11-08 receipt hidden_files/twelve-lane-receipts/weekly-distill-20261108-librarian-heir.md (scored 9.2/10). Board citations executor-sourced from the receipt, not independently re-fetched this tick (PAT 401 standing outage).",
  "decision_change": "Future wave-closeout and work-state adjudications must cite the venue comment IDs they checked; a three-pass receipt is never cited as proof of what happened on the venue. Any adjudication asserting work-state from run-local state alone is a draft, returned as a scope error, not debated.",
  "falsifier": "The split is refuted if either source text is shown to claim the other's scope — e.g. three-pass-flow stated as the gate for work-state adjudication, or venue-citation stated as a gate on code merges. It also weakens if a work-state adjudication made without venue citation is later confirmed correct by the venue with no discrepancy — that case would demote 'venue is ground truth' to 'venue is preferred'.",
  "cousins": ["SN-1989 (receipt gate vs human gate — different second pole: experience surfaces, not work-state)", "SN-1901 (venue-citation as citation practice for absence findings)", "SN-2292 (detection is not prevention)"],
  "captured": "2026-11-08",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
