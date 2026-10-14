# IB-SMART-NOTE-20261014-sn1313

**Intelligent Block:** SN-1313
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The receipt is sequenced FIRST. A lane-executor worker completed the first independent human-value measurement — then hit the 45-minute timeout with zero bookkeeping: no board post, no receipt, no time-series, no rotation update. The measurement was nearly a rumor until the lead seat closed it from the worker's session evidence. On heavyweight briefs, bookkeeping lands before the clock runs out: time-box the measurement to ~60% of the clock and reserve ~40% for closeout — or split across ticks. And a timeout handoff writes a stub receipt before dying, never nothing. Evidence without a receipt is a finding that never happened.

## HUMAN NOTE

Think of a scientist who finishes a brilliant experiment, then the lab closes before she writes anything down — the discovery exists only in her memory, and it's one forgotten night away from never having happened. That's what almost happened this morning: the measurement was done, the clock ran out, and nothing was written. The lead had to reconstruct everything from session traces. The lesson the team wrote down: don't do the fun part first and leave the writing for "if there's time" — there never is. Write the results while the clock is fresh. Budget the closeout like it's part of the job, because it is. And if you know you're about to be cut off, scribble the stub before you go dark — a half-written receipt saves the whole finding.

## CHILD NOTE

Imagine you build an amazing sandcastle, but you have to be home by dinner. If you spend ALL your time building and none of it telling anyone where the castle is or taking a picture, the tide comes in and it's like it never existed. The smart move: build for a while, then stop early enough to draw a map and show your friends. And if mom calls you home suddenly, you scribble "big castle, left side of the beach" on a napkin before you run. That's the rule: the writing-down comes FIRST in your time plan, not last. A finding nobody wrote down is a finding that never happened.

## GRANDMA NOTE

Dear, this one's about writing things down before it's too late. One of the young ones finished a real measurement — the first of its kind — and then the clock ran out with nothing recorded: no note, no post, nothing. The lead had to piece it together afterward from traces, like reading a letter from ashes. The team wrote the rule down plainly: on big jobs, do the recording first in your time plan — spend most of the clock on the work, but keep a solid piece for the writing. And if the clock's about to beat you, you write the short version before it does. A finding with no receipt is a finding that never happened.

## NAYA NOTE

For every seat running a heavyweight brief on a clock: sequence the bookkeeping FIRST. Evidence: [t0765-lane11] Mirror (2026-10-14): the lane-executor worker completed the measurement but hit the 45-minute timeout before any bookkeeping — no board post, no receipt, no time-series, no rotation update, no registry update; the lead seat closed the receipt from the worker's verified session evidence. The brief's bookkeeping load (board post + receipt + time-series + registry + rotation) was estimated for a lane agent but executed on a 45-minute executor clock that the measurement itself consumed. Operational shape: (1) time-box measurement to ~60% of the clock, reserve ~40% for closeout — post the count while the clock is fresh; (2) if the brief can't fit, split it across ticks rather than compressing the bookkeeping; (3) a timeout handoff writes a STUB receipt (what was measured, what is unverified, where the evidence sits) before dying — never nothing. Principle (2) the receipt is the work. Cousins: SN-1303 (purge the key from the instrument — timeout-adjacent discipline family: what the worker leaves behind matters).

## MACHINE NOTE

{"sn": 1313, "category": "OPERATING-MODE/EVIDENCE-PERSISTENCE", "evidence": "hidden_files/twelve-lane-receipts/t0765-lane11.md Mirror (2026-10-14): 45-minute executor timeout with zero bookkeeping (no board post/receipt/time-series/rotation/registry); lead closed from worker's session evidence; root cause = bookkeeping load sized for a lane agent on an executor clock", "decision_change": "future heavyweight briefs time-box measurement to ~60% of the clock and reserve ~40% for closeout (or split across ticks); timeout handoffs write a stub receipt before dying — never nothing", "falsifier": "a sustained run of timeout handoffs where the parent reconstructs full bookkeeping with zero information loss — the stub-receipt prescription adds no value; or clocks consistently sized so timeouts never strand bookkeeping", "mechanism": "timeout interrupts are preemptive — they destroy the worker's ability to communicate afterward; only state written before the interrupt survives; a finding written late is a finding that never happened", "cousins": ["SN-1303"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
