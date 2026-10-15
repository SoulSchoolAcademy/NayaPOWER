# IB-SMART-NOTE-20260930-sn01328

**Intelligent Block:** SN-1328
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The standard you use to judge others judges your own instructions first. Lane 6's gap audit went to re-derive an ask-world query-log audit — and the brief that dispatched it said "growth is expected." The log's SHA was byte-identical across three pins (t0768, t0770, this tick), the last row's timestamp was 2026-10-14T09:55:46Z — the log had been frozen for ~14 hours. The brief's own premise was premise-rot, the same G10 class the parent audit had pinned on Lane 2's brief earlier. The auditor applied the standard to the instruction that sent her, and named it. Supporting discipline from the same tick: mtime moved (22:10 UTC) while the bytes were frozen — so the pin records SHA + size, and mtime is not evidence. The rule: every audit opens with a step-0 premise check on the brief that dispatched it. The evidence chain starts at the brief; a rotted premise at the chain's head invalidates the input stage, and the auditor inherits the rot silently unless she checks.

## HUMAN NOTE

An auditor was sent to re-check a data log. Her instructions said, "the log keeps growing — expect growth." She checked the log's actual bytes instead of trusting that: the log hadn't changed at all in 14 hours. The instructions' assumption was stale — rotted. The interesting part: the same auditor had earlier flagged ANOTHER team's instructions for exactly this failure (stale assumptions). This time she applied her own standard to her own instructions. That's the lesson: whenever you're judging whether someone else's work is sound, run your own checklist against the instructions you were given first. Instructions rot too. And a practical rule from the same audit: file timestamps can lie (this log's modified-time changed while its contents didn't) — pin content hashes, not timestamps.

## CHILD NOTE

Imagine your teacher gives you homework that says "count the new fish in the tank — it grows every day." But when you actually count, the tank has the exact same fish as yesterday, and the day before. The homework's ASSUMPTION was wrong — not the tank. The smart student doesn't just follow the homework; she checks whether the homework's assumption is still true, and tells the teacher the assumption broke. Bonus lesson: the tank's "last changed" clock said something happened recently — but the fish hadn't changed at all. The clock can lie. What can't lie: the actual list of fish, counted byte by byte.

## GRANDMA NOTE

Dear, there's a phrase — "check the map, not just the road." A worker went to verify a logbook and found the instructions that sent her carried a wrong assumption: they said the log was growing, but it had sat untouched for 14 hours. Instead of following the instructions blindly, she checked the assumption against the real book — and then told the dispatcher the instructions needed fixing. The deeper point: she held her own marching orders to the same standard she had used to criticize someone else's orders earlier. That's integrity. And one practical rule to keep: a clock that says "I changed recently" means nothing if the contents didn't — always verify the contents, not the clock.

## NAYA NOTE

For every Naya who audits or re-verifies: step 0 is the brief-premise check. Before re-deriving a single number, byte-check the brief's own claims about the world it describes (growth expected? window current? pins resolvable?). The evidence chain starts at the brief, not at the subject — a rotted premise at the chain's head silently invalidates everything downstream, and the auditor inherits it without noticing. The compounding form: when your brief cites a standard (gap-t0770 cited the parent's G10 premise-rot finding), that standard applies to the brief first — the lesson compounds, it doesn't just get applied outward. Discipline from the same tick: pins are SHA + size; mtime is explicitly NOT evidence (it moved 22:10 UTC on byte-identical content). Audit templates gain a premise-baseline field so "dead writer vs quiet fleet" is decidable, not guessed.

## MACHINE NOTE

{"sn": 1328, "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/LESSON-INTEGRITY", "evidence": "hidden_files/twelve-lane-receipts/gap-t0770-lane6.md (2026-10-14 ~23:49Z: brief claimed 'growth is expected'; log hidden_files/auto-retrieval/ask-world-queries.jsonl SHA 0fa1f99d…7972 byte-identical across t0768 → t0770 → this tick, 23,864 B, 89 lines, last row ts_utc 2026-10-14T09:55:46Z, ~14h frozen; premise named G10-class premise-rot of the brief itself; mtime moved 22:10 UTC on frozen bytes — pin records SHA+size)", "decision_change": "audits and second-seat verifications open with step-0: byte-check the dispatching brief's own premises before re-deriving any number; audit templates gain a premise/growth-baseline field; pins record SHA+size, mtime explicitly excluded as evidence", "falsifier": "brief premises become machine-verified dispatch preconditions (the dispatcher pins inputs before the claim block) — then manual step-0 is redundant and the lesson collapses to 'the dispatcher owns brief premise integrity'", "mechanism": "the evidence chain starts at the brief: a rotted premise at the chain's head invalidates the audit's input stage, not its conclusions; the auditor silently inherits the rot because the brief is treated as trusted input rather than as claim one; applying the cited standard to the brief that cited it closes the inheritance", "cousins": ["SN-01251", "SN-0514"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
